#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        fail(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return ""


def load_json(path: Path):
    try:
        return json.loads(read(path))
    except Exception as exc:
        fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
        return None


for path in ["AGENTS.md", "README.md", "manifest.json", ".agentic/README.md", ".agentic/manifest.yaml", ".agentic/lock.json", ".agentic/PRODUCT.md", ".agentic/ARCHITECTURE.md", ".agentic/SECURITY.md", ".agentic/decisions/index.yaml"]:
    if not (ROOT / path).is_file():
        fail(f"missing required file: {path}")

manifest = load_json(ROOT / "manifest.json")
declared = set(manifest.get("skills", [])) if isinstance(manifest, dict) else set()
actual = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
if declared != actual:
    fail(f"skill manifest mismatch: declared={sorted(declared)} actual={sorted(actual)}")
for skill in sorted(actual):
    path = ROOT / "skills" / skill / "SKILL.md"
    if not path.is_file():
        fail(f"skill missing SKILL.md: {skill}")
    elif len(read(path).strip()) < 120:
        fail(f"skill is too small to define a durable procedure: {skill}")

required_prompts = {"init.md", "upgrade.md", "audit.md", "migrate.md", "doctor.md", "new-adr.md", "sync-adapters.md", "security.md", "design-system.md", "release.md"}
actual_prompts = {p.name for p in (ROOT / "prompts").glob("*.md")}
missing_prompts = required_prompts - actual_prompts
if missing_prompts:
    fail(f"missing prompts: {sorted(missing_prompts)}")

canonical = read(ROOT / "references" / "canonical-source.md")
for token in [".agentic/", "catalog/", "variants/<name>/files/", ".agents/skills/"]:
    if token not in canonical:
        fail(f"canonical-source reference missing {token}")

forbidden = ["agentic-harness/templates", "agentic-harness/boilerplates", "agentic-harness/modules/"]
for path in list((ROOT / "skills").rglob("*.md")) + list((ROOT / "prompts").rglob("*.md")) + list((ROOT / "adapters").rglob("*.md")):
    body = read(path)
    for token in forbidden:
        if token in body:
            fail(f"deprecated canonical source assumption in {path.relative_to(ROOT)}: {token}")

for path in (ROOT / "adapters").rglob("README.md"):
    body = read(path)
    if "AGENTS.md" not in body or ".agentic" not in body or len(body) > 1200:
        fail(f"adapter is not thin/canonical: {path.relative_to(ROOT)}")

self_manifest = read(ROOT / ".agentic" / "manifest.yaml")
for token in ["format_version: 1", "canonical_router: ../AGENTS.md", "vendor_files_must_be_thin: true"]:
    if token not in self_manifest:
        fail(f"self-hosting manifest missing {token}")
load_json(ROOT / ".agentic" / "lock.json")

index = read(ROOT / ".agentic" / "decisions" / "index.yaml")
for path in (ROOT / ".agentic" / "decisions").glob("ADR-[0-9][0-9][0-9]-*.md"):
    if path.name not in index:
        fail(f"unindexed self-hosting ADR: {path.name}")

if errors:
    print("Agent validation failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Agents valid: {len(actual)} skills, {len(actual_prompts)} prompts, canonical layout v1")
