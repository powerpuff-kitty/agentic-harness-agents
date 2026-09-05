#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
version = manifest["version"]
dist = ROOT / "dist"
dist.mkdir(exist_ok=True)
archive = dist / f"agentic-harness-agents-v{version}.zip"

roots = [
    ROOT / ".codex-plugin",
    ROOT / ".agents" / "plugins",
    ROOT / "skills",
    ROOT / "prompts",
    ROOT / "adapters",
    ROOT / "references",
    ROOT / "evals",
]
files = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "manifest.json", ROOT / "CHANGELOG.md"]

if archive.exists():
    archive.unlink()
with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for file in files:
        zf.write(file, file.relative_to(ROOT))
    for root in roots:
        for path in sorted(root.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                zf.write(path, path.relative_to(ROOT))

digest = hashlib.sha256(archive.read_bytes()).hexdigest()
checksum = archive.with_suffix(archive.suffix + ".sha256")
checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
print(archive.relative_to(ROOT))
print(checksum.relative_to(ROOT))
