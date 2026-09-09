#!/usr/bin/env python3
"""Offline fixture/contract checks. Does not execute or evaluate an AI model."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

AFFECTED = {"agentic-app", "accessibility-audit", "design-system-compliance", "design-analysis", "design-intelligence"}
SECTIONS = ("Objective", "Inputs", "Context", "Procedure", "Output", "Completion")


def evaluate_enrichment_fixture(base: dict, enriched: dict) -> list[str]:
    """Test handoff invariants, not JSON Schema conformance or production ingestion."""
    errors = []
    for field in ("format_version", "source", "domains", "checks", "reviews"):
        if base.get(field) != enriched.get(field):
            errors.append(f"original {field} changed")
    if not isinstance(base.get("findings"), list) or not isinstance(enriched.get("findings"), list):
        return errors + ["findings must be arrays"]
    all_findings = enriched["findings"]
    ids = [f.get("id") if isinstance(f, dict) else None for f in all_findings]
    if any(not isinstance(x, str) or not x for x in ids) or len(set(ids)) != len(ids):
        return errors + ["invalid or duplicate finding IDs"]
    by_id = dict(zip(ids, all_findings))
    original_ids = set()
    for finding in base["findings"]:
        original_ids.add(finding["id"])
        if by_id.get(finding["id"]) != finding:
            errors.append(f"original finding changed: {finding['id']}")
    measurement_ids = {m["id"] for d in base.get("domains", {}).values() for m in d.get("measurements", [])}
    for finding in all_findings:
        if finding["id"] not in original_ids:
            if finding.get("source_type") != "ai":
                errors.append("new interpretation must have AI provenance")
            refs = finding.get("measurement_refs", [])
            if not isinstance(refs, list) or any(not isinstance(x, str) or x not in measurement_ids for x in refs):
                errors.append("dangling or invalid measurement reference")
            if not refs and not finding.get("evidence") and finding.get("classification") != "unknown":
                errors.append("new interpretation lacks evidence")
            if finding.get("classification") in {"observed", "uncertain"}:
                errors.append("human-facing label used as classification enum")
    return errors


def validate(root: Path) -> list[str]:
    errors = []
    def load(rel: str):
        try:
            return json.loads((root / rel).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"cannot load {rel}: {exc}")
            return None
    manifest = load("manifest.json")
    plugin = load(".codex-plugin/plugin.json")
    suite = load("evals/design-intelligence.json")
    if not all(isinstance(v, dict) for v in (manifest, plugin, suite)):
        return errors + ["manifest, plugin and suite must be objects"]
    declared = manifest.get("skills", [])
    if not isinstance(declared, list) or any(not isinstance(x, str) for x in declared):
        return errors + ["manifest skills must be strings"]
    inventory = set(declared)
    if len(inventory) != len(declared) or not AFFECTED <= inventory:
        errors.append("missing or duplicated registered skill")
    plugin_paths = plugin.get("skills", [])
    if not isinstance(plugin_paths, list) or any(not isinstance(x, str) for x in plugin_paths):
        return errors + ["plugin skills must be strings"]
    if {Path(x).name for x in plugin_paths} != inventory or len(plugin_paths) != len(inventory):
        errors.append("plugin inventory differs from manifest")
    if plugin.get("version") != manifest.get("version"):
        errors.append("plugin version differs from manifest")
    for name in sorted(AFFECTED):
        path = root / "skills" / name / "SKILL.md"
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            errors.append(f"missing procedure: {name}")
            continue
        match = re.match(r'---\nname: ([a-z-]+)\ndescription: ("[^\n]*")\n---\n', text)
        if not match or match.group(1) != name:
            errors.append(f"invalid frontmatter: {name}")
            continue
        try:
            description = json.loads(match.group(2))
        except ValueError:
            errors.append(f"invalid description: {name}")
            continue
        if not 40 <= len(description) <= 1024 or "Do not use" not in description or "Use when" not in description:
            errors.append(f"invalid trigger boundaries: {name}")
        for section in SECTIONS:
            if f"## {section}" not in text:
                errors.append(f"missing section: {name}/{section}")
        for relative in re.findall(r'\]\((references/[^)]+)\)', text):
            resolved = (path.parent / relative).resolve()
            if not resolved.is_relative_to(path.parent.resolve()) or not resolved.is_file():
                errors.append(f"missing or unsafe local reference: {name}/{relative}")
    if suite.get("format_version") != 1 or suite.get("kind") != "acceptance-scenarios" or suite.get("model_evaluations") != "not_run":
        errors.append("scenario fixtures must not claim model evaluation results")
    cases = suite.get("cases", [])
    if not isinstance(cases, list) or not cases:
        return errors + ["scenario cases must be a nonempty array"]
    case_ids, covered = set(), set()
    for case in cases:
        if not isinstance(case, dict):
            errors.append("invalid scenario object")
            continue
        id = case.get("id")
        if not isinstance(id, str) or not id or id in case_ids:
            errors.append("missing or duplicate scenario ID")
        else:
            case_ids.add(id)
        expected = case.get("expected_skill")
        if not isinstance(expected, str) or expected not in inventory:
            errors.append(f"unknown scenario skill: {expected}")
        else:
            covered.add(expected)
        for field in ("required_behavior", "forbidden_behavior", "must_not_use"):
            values = case.get(field)
            if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v.strip() for v in values):
                errors.append(f"invalid {field}: {id}")
            elif field == "must_not_use" and (expected in values or not set(values) <= inventory):
                errors.append(f"invalid routing exclusion: {id}")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"missing scenario prompt: {id}")
    design_suite = AFFECTED | {"identity-design", "design-research", "component-resolution", "design-system", "product-design"}
    if not design_suite <= covered:
        errors.append("missing design scenario coverage")
    base, enriched = load("evals/fixtures/design-analysis.base.json"), load("evals/fixtures/design-analysis.enriched.json")
    if isinstance(base, dict) and isinstance(enriched, dict):
        try:
            errors.extend(evaluate_enrichment_fixture(base, enriched))
        except (KeyError, TypeError, AttributeError) as exc:
            errors.append(f"malformed enrichment fixture: {exc}")
    else:
        errors.append("enrichment fixtures must be objects")
    return errors


if __name__ == "__main__":
    if len(sys.argv) != 1:
        raise SystemExit("usage: python3 .github/scripts/validate_design_skills.py")
    findings = validate(Path(__file__).resolve().parents[2])
    if findings:
        print("Design fixture validation failed:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        raise SystemExit(1)
    print("Design fixtures valid: procedure structure, registry parity, routing/safety scenarios and enrichment invariants. Model evaluations: not run.")
