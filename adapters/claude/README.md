# Claude Code adapter

[`files/CLAUDE.md`](files/CLAUDE.md) contains the active root import `@AGENTS.md`. Copy it to the target root only when no `CLAUDE.md` exists; otherwise merge the import once without replacing existing content. The imported router selects `.agentic/` context, so this adapter does not duplicate product or architecture truth.

An optional typed-UI rule is provided at `files/.claude/rules/agentic-typed-ui.md`; review its patterns before installing at the corresponding project path. It is not enabled by the base profile.

The repository itself uses the shipped root import. Automated CLI installation and live-host confirmation remain unfinished. See [native adapter guidance](../../references/native-adapters.md) and [`assets.json`](../assets.json) for exact scope and source provenance. Instruction files are context, not runtime enforcement.
