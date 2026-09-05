#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors: list[str] = []
REQUIRED_SECTIONS = ["## Objective", "## Inputs", "## Context", "## Procedure", "## Output", "## Completion"]
STOPWORDS = {"use","when","after","before","the","user","asks","to","a","an","and","or","for","this","that","of","in","on","with","from","do","not","skill","repository","project","review","work"}


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


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    body = read(path)
    if not body.startswith("---\n"):
        fail(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
        return {}, body
    end = body.find("\n---\n", 4)
    if end < 0:
        fail(f"unterminated YAML frontmatter: {path.relative_to(ROOT)}")
        return {}, body
    raw = body[4:end]
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            fail(f"invalid frontmatter line in {path.relative_to(ROOT)}: {line}")
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except Exception:
                fail(f"invalid quoted frontmatter value in {path.relative_to(ROOT)}: {key}")
        meta[key.strip()] = value
    return meta, body[end + 5:]


def tokens(description: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", description.lower()) if len(w) > 2 and w not in STOPWORDS}


required_files = ["AGENTS.md", "README.md", "manifest.json", ".agentic/README.md", ".agentic/manifest.yaml", ".agentic/lock.json", ".agentic/PRODUCT.md", ".agentic/ARCHITECTURE.md", ".agentic/SECURITY.md", ".agentic/decisions/index.yaml", "references/context-engineering.md", "references/skill-contract.md", ".codex-plugin/plugin.json", ".agents/plugins/marketplace.json", "evals/routing.json"]
for path in required_files:
    if not (ROOT / path).is_file():
        fail(f"missing required file: {path}")

manifest = load_json(ROOT / "manifest.json")
declared = set(manifest.get("skills", [])) if isinstance(manifest, dict) else set()
actual = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
if declared != actual:
    fail(f"skill manifest mismatch: declared={sorted(declared)} actual={sorted(actual)}")

descriptions: dict[str, str] = {}
for skill in sorted(actual):
    path = ROOT / "skills" / skill / "SKILL.md"
    if not path.is_file():
        fail(f"skill missing SKILL.md: {skill}")
        continue
    meta, body = parse_frontmatter(path)
    if set(meta) != {"name", "description"}:
        fail(f"{skill} frontmatter must contain only name and description")
    if meta.get("name") != skill:
        fail(f"{skill} frontmatter name mismatch: {meta.get('name')!r}")
    description = meta.get("description", "")
    descriptions[skill] = description
    if not 40 <= len(description) <= 1024:
        fail(f"{skill} description must be 40..1024 characters")
    lower = description.lower()
    has_use_guidance = re.search(r"\buse\s+(when|after|before|for)\b", lower) is not None
    if not has_use_guidance or "do not use" not in lower:
        fail(f"{skill} description must include both use and exclusion guidance")
    for heading in REQUIRED_SECTIONS:
        if heading not in body:
            fail(f"{skill} missing required section {heading}")
    if len(body.strip()) < 500:
        fail(f"{skill} body is too small for a durable procedure")

names = sorted(descriptions)
for i, left in enumerate(names):
    lt = tokens(descriptions[left])
    for right in names[i + 1:]:
        rt = tokens(descriptions[right])
        union = lt | rt
        similarity = len(lt & rt) / len(union) if union else 0.0
        if similarity >= 0.72:
            fail(f"trigger descriptions overlap too strongly: {left} vs {right} ({similarity:.2f})")

routing = load_json(ROOT / "evals" / "routing.json")
covered: set[str] = set()
if isinstance(routing, dict):
    if routing.get("format_version") != 1:
        fail("evals/routing.json format_version must be 1")
    for case in routing.get("cases", []):
        expected = case.get("expected_skill")
        forbidden = set(case.get("must_not_use", []))
        if expected not in actual:
            fail(f"routing case {case.get('id')} references unknown expected skill {expected}")
        else:
            covered.add(expected)
        unknown = forbidden - actual
        if unknown:
            fail(f"routing case {case.get('id')} has unknown must_not_use skills {sorted(unknown)}")
        if expected in forbidden:
            fail(f"routing case {case.get('id')} forbids its expected skill")
if covered != actual:
    fail(f"routing eval coverage mismatch: missing={sorted(actual-covered)} extra={sorted(covered-actual)}")

plugin = load_json(ROOT / ".codex-plugin" / "plugin.json")
if isinstance(plugin, dict):
    if plugin.get("name") != "agentic-harness-agents":
        fail("Codex plugin name mismatch")
    if isinstance(manifest, dict) and plugin.get("version") != manifest.get("version"):
        fail("Codex plugin version must match manifest version")
    plugin_skills = {Path(x).name for x in plugin.get("skills", [])}
    if plugin_skills != actual:
        fail(f"Codex plugin skill inventory mismatch: {sorted(plugin_skills)}")

marketplace = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
if isinstance(marketplace, dict):
    entries = marketplace.get("plugins", [])
    if len(entries) != 1 or entries[0].get("name") != "agentic-harness-agents":
        fail("marketplace must expose exactly the agentic-harness-agents plugin")
    source = entries[0].get("source", {}) if entries else {}
    if source.get("source") != "local" or source.get("path") != "./../..":
        fail("marketplace source must resolve to the repository root")

lock = load_json(ROOT / ".agentic" / "lock.json")
if isinstance(manifest, dict) and isinstance(lock, dict):
    compat = manifest.get("compatibility", {})
    canonical_revision = ((compat.get("agentic_harness") or {}).get("revision"))
    cli_revision = ((compat.get("agentic_harness_cli") or {}).get("revision"))
    if (lock.get("canonical_source") or {}).get("revision") != canonical_revision:
        fail("self-hosting canonical lock revision differs from manifest compatibility revision")
    if (lock.get("cli_source") or {}).get("revision") != cli_revision:
        fail("self-hosting CLI lock revision differs from manifest compatibility revision")

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

index = read(ROOT / ".agentic" / "decisions" / "index.yaml")
for path in (ROOT / ".agentic" / "decisions").glob("ADR-[0-9][0-9][0-9]-*.md"):
    if path.name == "ADR-000-template.md":
        continue
    if path.name not in index:
        fail(f"unindexed self-hosting ADR: {path.name}")

if errors:
    print("Agent validation failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Agents valid: {len(actual)} installable skills, routing coverage complete, plugin version {manifest.get('version') if isinstance(manifest, dict) else '?'}")
