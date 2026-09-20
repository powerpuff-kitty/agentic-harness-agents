"""Authoring regressions only: source bytes and trigger identity, not model behaviour."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
NAMES = frozenset({"codebase-audit", "security-review", "design-system-compliance",
                   "implementation-plan", "documentation"})
HEADINGS = ("Objective", "Inputs", "Context", "Procedure", "Output", "Completion")


def distinct_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate budget key")
        result[key] = value
    return result


def budgets():
    # Fixed repository-owned input. This helper performs no arbitrary-path reads.
    value = json.loads((ROOT / "evals/skill-entrypoint-budgets.json").read_text(encoding="utf-8"),
                       object_pairs_hook=distinct_keys)
    validate_budgets(value)
    return value


def validate_budgets(value):
    if not isinstance(value, dict) or set(value) != {
        "format_version", "scope", "baseline_revision", "skills"
    }:
        raise ValueError("invalid budget fields")
    if type(value["format_version"]) is not int or value["format_version"] != 1:
        raise ValueError("unsupported budget version")
    if value["scope"] != "selected-entrypoint-source-bytes":
        raise ValueError("source bytes must not be represented as provider tokens")
    if not isinstance(value["baseline_revision"], str) or not re.fullmatch(
        r"[0-9a-f]{40}", value["baseline_revision"]
    ):
        raise ValueError("baseline revision required")
    items = value["skills"]
    if not isinstance(items, dict) or set(items) != NAMES:
        raise ValueError("budget selection changed; review explicit enrollment")
    for item in items.values():
        if not isinstance(item, dict) or set(item) != {
            "max_bytes", "trigger_sha256", "baseline_bytes", "baseline_blob"
        }:
            raise ValueError("invalid per-skill budget")
        for field in ("max_bytes", "baseline_bytes"):
            if type(item[field]) is not int or not 500 <= item[field] <= 65536:
                raise ValueError("invalid byte limit")
        if item["max_bytes"] > item["baseline_bytes"]:
            raise ValueError("growth requires an explicit baseline review")
        for field, length in (("trigger_sha256", 64), ("baseline_blob", 40)):
            if not isinstance(item[field], str) or not re.fullmatch(
                rf"[0-9a-f]{{{length}}}", item[field]
            ):
                raise ValueError("invalid source identity")


def check_entrypoint(name, data, budget):
    if not isinstance(data, bytes) or len(data) > budget["max_bytes"]:
        raise ValueError("entrypoint exceeds reviewed source-byte budget")
    text = data.decode("utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("invalid frontmatter")
    frontmatter, body = text[4:].split("\n---\n", 1)
    lines = frontmatter.splitlines()
    if len(lines) != 2 or lines[0] != "name: " + name or not lines[1].startswith("description: "):
        raise ValueError("unexpected frontmatter fields")
    description = json.loads(lines[1][len("description: "):])
    if not isinstance(description, str) or hashlib.sha256(description.encode()).hexdigest() != budget["trigger_sha256"]:
        raise ValueError("routing trigger changed; review routing fixtures and budget together")
    if "\x00" in text or len(body.strip()) < 500 or any(
        body.splitlines().count("## " + heading) != 1 for heading in HEADINGS
    ):
        raise ValueError("required procedure structure missing")
    return len(data)


class SkillEntrypointBudgets(unittest.TestCase):
    def test_selected_repository_entrypoints(self):
        value = budgets()
        total = 0
        for name, limit in value["skills"].items():
            with self.subTest(skill=name):
                total += check_entrypoint(name, (ROOT / "skills" / name / "SKILL.md").read_bytes(), limit)
        self.assertLess(total, sum(item["baseline_bytes"] for item in value["skills"].values()))

    def test_invalid_budget_shape_and_scope_are_rejected(self):
        valid = budgets()
        for field, bad in [("format_version", True), ("scope", "provider-tokens"),
                           ("baseline_revision", None), ("skills", {})]:
            changed = copy.deepcopy(valid)
            changed[field] = bad
            with self.assertRaises(ValueError):
                validate_budgets(changed)

    def test_invalid_limits_and_source_identities_are_rejected(self):
        for field, bad in [("max_bytes", True), ("max_bytes", -1), ("max_bytes", 65537),
                           ("baseline_bytes", "5000"), ("baseline_blob", "main"),
                           ("trigger_sha256", None)]:
            changed = copy.deepcopy(budgets())
            changed["skills"]["documentation"][field] = bad
            with self.assertRaises(ValueError):
                validate_budgets(changed)

    def test_duplicate_budget_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"max_bytes": 1, "max_bytes": 2}', object_pairs_hook=distinct_keys)

    def test_over_budget_cannot_pass(self):
        value = budgets()["skills"]["documentation"]
        with self.assertRaises(ValueError):
            check_entrypoint("documentation", b"x" * (value["max_bytes"] + 1), value)

    def test_trigger_changes_need_review(self):
        name = "documentation"
        data = (ROOT / "skills" / name / "SKILL.md").read_bytes()
        with self.assertRaises(ValueError):
            check_entrypoint(name, data.replace(b"durable project", b"all project", 1), budgets()["skills"][name])

    def test_short_but_incomplete_procedure_is_rejected(self):
        name = "documentation"
        data = (ROOT / "skills" / name / "SKILL.md").read_bytes().replace(b"## Completion", b"## Done")
        with self.assertRaises(ValueError):
            check_entrypoint(name, data, budgets()["skills"][name])


if __name__ == "__main__":
    unittest.main()
