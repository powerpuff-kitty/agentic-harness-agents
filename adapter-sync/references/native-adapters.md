# Native context adapter resources

Use these resources only when synchronizing a requested host's context files.
The inventory is [assets/assets.json](../assets/assets.json); its source paths are
relative to this skill's `assets/` directory. Target `AGENTS.md` and project-owned
context remain authoritative. These assets configure no hooks, permissions, MCP
servers or executable commands. The typed-UI profile remains explicitly opt-in.

Review the matching host guide: [Claude](claude.md),
[Cursor](cursor.md), [Codex](codex.md),
[Copilot](copilot.md) or [Gemini](gemini.md).
Copy a supplied asset only after reviewing its target and existing instructions.
Preserve unrelated settings and resolve conflicting project instructions explicitly.
Retain the skill's MIT [LICENSE](../LICENSE) when copying substantial content.

Installed trusted CLI versions may provide deterministic synchronization. Check
their actual help and version before use; copying files does not prove native host
loading, instruction adherence or runtime enforcement. No real host session is
included with these assets. Documentation provenance in the inventory records the
original review date of 2026-09-12; it is not a fresh compatibility certification.

Run the skill-local asset checks with `python3 tests/validate_adapter_assets.py`
and `python3 -m unittest discover -s tests` from this skill's directory. These checks
validate shipped bytes and metadata, not live host behavior.
