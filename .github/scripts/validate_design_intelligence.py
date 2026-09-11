#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENARIO_PATH = ROOT / "evals" / "design-intelligence.json"
MANIFEST_PATH = ROOT / "manifest.json"
REFERENCE_PATH = ROOT / "references" / "design-intelligence.md"

REQUIRED_SCENARIO_SKILLS = {
    "agentic-app",
    "accessibility-audit",
    "component-resolution",
    "design-analysis",
    "design-intelligence",
    "design-research",
    "design-system",
    "design-system-compliance",
    "identity-design",
    "product-design",
}

SPECIALIST_SKILLS = {
    "component-resolution",
    "design-analysis",
    "design-intelligence",
    "design-research",
    "design-system",
    "design-system-compliance",
    "identity-design",
    "product-design",
    "accessibility-audit",
}

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")
        return None


manifest = load(MANIFEST_PATH)
scenarios_doc = load(SCENARIO_PATH)
actual_skills = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
declared_skills = set(manifest.get("skills", [])) if isinstance(manifest, dict) else set()

if not REFERENCE_PATH.is_file():
    fail("missing references/design-intelligence.md")

if isinstance(scenarios_doc, dict):
    if scenarios_doc.get("format_version") != 1:
        fail("evals/design-intelligence.json format_version must be 1")
    if scenarios_doc.get("evaluation_kind") != "static-behavior-contract":
        fail("Design Intelligence scenarios must declare static-behavior-contract")
    if scenarios_doc.get("model_evaluation_performed") is not False:
        fail("static scenario fixture must not claim a model evaluation was performed")

    ids: set[str] = set()
    covered: set[str] = set()
    for scenario in scenarios_doc.get("scenarios", []):
        scenario_id = scenario.get("id")
        skill = scenario.get("skill")
        prompt = scenario.get("prompt")
        expected = scenario.get("expected_behaviors")
        forbidden = scenario.get("forbidden_behaviors")

        if not isinstance(scenario_id, str) or not scenario_id:
            fail("Design Intelligence scenario missing non-empty id")
        elif scenario_id in ids:
            fail(f"duplicate Design Intelligence scenario id: {scenario_id}")
        else:
            ids.add(scenario_id)

        if skill not in actual_skills or skill not in declared_skills:
            fail(f"scenario {scenario_id} references unknown/undeclared skill {skill}")
        else:
            covered.add(skill)

        if not isinstance(prompt, str) or len(prompt.strip()) < 20:
            fail(f"scenario {scenario_id} needs a concrete prompt")
        if not isinstance(expected, list) or not expected or not all(isinstance(x, str) and x.strip() for x in expected):
            fail(f"scenario {scenario_id} needs non-empty expected_behaviors")
        if not isinstance(forbidden, list) or not forbidden or not all(isinstance(x, str) and x.strip() for x in forbidden):
            fail(f"scenario {scenario_id} needs non-empty forbidden_behaviors")
        if scenario.get("network_required") is not False:
            fail(f"scenario {scenario_id} must remain runnable without network")

    missing = REQUIRED_SCENARIO_SKILLS - covered
    if missing:
        fail(f"Design Intelligence safety scenario coverage missing skills: {sorted(missing)}")
else:
    fail("evals/design-intelligence.json must be an object")

for skill in sorted(SPECIALIST_SKILLS):
    path = ROOT / "skills" / skill / "SKILL.md"
    if not path.is_file():
        fail(f"missing Design Intelligence specialist skill: {skill}")
        continue
    body = path.read_text(encoding="utf-8")
    if "references/design-intelligence.md" not in body:
        fail(f"{skill} must reference shared Design Intelligence boundaries")

if errors:
    print("Design Intelligence validation failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Design Intelligence valid: {len(scenarios_doc['scenarios'])} static scenarios, {len(REQUIRED_SCENARIO_SKILLS)} specialist/lifecycle skills covered; no model run claimed")
