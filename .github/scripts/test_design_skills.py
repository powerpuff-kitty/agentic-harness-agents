#!/usr/bin/env python3
"""Unit tests of fixture-validation code, not of AI model behavior."""
from __future__ import annotations
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from validate_design_skills import evaluate_enrichment_fixture, validate

ROOT = Path(__file__).resolve().parents[2]


class EnrichmentTests(unittest.TestCase):
    def setUp(self):
        self.base = json.loads((ROOT / "evals/fixtures/design-analysis.base.json").read_text())
        self.enriched = json.loads((ROOT / "evals/fixtures/design-analysis.enriched.json").read_text())

    def test_accepts_append_only_ai_enrichment(self):
        original = copy.deepcopy(self.base)
        self.assertEqual(evaluate_enrichment_fixture(self.base, self.enriched), [])
        self.assertEqual(self.base, original)

    def test_rejects_measurement_tampering(self):
        self.enriched["domains"]["spacing"]["measurements"][0]["value"][0]["count"] = 99
        self.assertIn("original domains changed", evaluate_enrichment_fixture(self.base, self.enriched))

    def test_rejects_disappearing_verification_gaps(self):
        self.enriched["checks"]["not_checked"] = []
        self.assertIn("original checks changed", evaluate_enrichment_fixture(self.base, self.enriched))

    def test_rejects_forged_review(self):
        self.enriched["reviews"] = [{"reviewer_type": "human", "decision": "accepted"}]
        self.assertIn("original reviews changed", evaluate_enrichment_fixture(self.base, self.enriched))

    def test_rejects_changed_original_finding(self):
        self.enriched["findings"][0]["statement"] = "Everything passed"
        self.assertTrue(any("original finding changed" in x for x in evaluate_enrichment_fixture(self.base, self.enriched)))

    def test_rejects_provenance_relabeling(self):
        self.enriched["findings"][-1]["source_type"] = "runtime"
        self.assertIn("new interpretation must have AI provenance", evaluate_enrichment_fixture(self.base, self.enriched))

    def test_rejects_duplicate_ids(self):
        self.enriched["findings"][-1]["id"] = self.enriched["findings"][0]["id"]
        self.assertIn("invalid or duplicate finding IDs", evaluate_enrichment_fixture(self.base, self.enriched))

    def test_rejects_dangling_evidence(self):
        self.enriched["findings"][-1]["measurement_refs"] = ["invented"]
        self.assertIn("dangling or invalid measurement reference", evaluate_enrichment_fixture(self.base, self.enriched))

    def test_rejects_ui_labels_as_enums(self):
        for label in ("observed", "uncertain"):
            self.enriched["findings"][-1]["classification"] = label
            self.assertIn("human-facing label used as classification enum", evaluate_enrichment_fixture(self.base, self.enriched))


class ContractTests(unittest.TestCase):
    def test_current_fixtures(self):
        self.assertEqual(validate(ROOT), [])

    def changed_copy(self, modify):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "repo"
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", "__pycache__", "dist", "node_modules"))
            modify(target)
            return validate(target)

    def test_missing_local_reference(self):
        errors = self.changed_copy(lambda root: (root / "skills/design-intelligence/references/workflow.md").unlink())
        self.assertTrue(any("missing or unsafe local reference" in x for x in errors))

    def test_unknown_scenario_skill(self):
        def mutate(root):
            path = root / "evals/design-skill-regressions.json"
            data = json.loads(path.read_text())
            data["cases"][0]["expected_skill"] = "invented-provider-agent"
            path.write_text(json.dumps(data))
        self.assertTrue(any("unknown scenario skill" in x for x in self.changed_copy(mutate)))

    def test_model_result_claim_is_not_a_fixture(self):
        def mutate(root):
            path = root / "evals/design-skill-regressions.json"
            data = json.loads(path.read_text()); data["model_evaluations"] = "passed"
            path.write_text(json.dumps(data))
        self.assertTrue(any("must not claim model" in x for x in self.changed_copy(mutate)))

    def test_plugin_version_mismatch(self):
        def mutate(root):
            path = root / ".codex-plugin/plugin.json"
            data = json.loads(path.read_text()); data["version"] = "wrong"
            path.write_text(json.dumps(data))
        self.assertIn("plugin version differs from manifest", self.changed_copy(mutate))


if __name__ == "__main__":
    unittest.main()
