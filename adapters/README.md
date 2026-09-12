# Native adapter assets

Root `AGENTS.md` remains the compact router into project-owned `.agentic/` context. [`assets.json`](assets.json) records reviewed source/target paths, optional profiles and documentation provenance; it is distribution metadata, not a second project contract.

- Claude: a real root `CLAUDE.md` import plus an optional path-scoped typed-UI rule.
- Cursor: uses native `AGENTS.md`; optional `.mdc` scoped rule, no redundant always-on copy.
- Codex: uses native `AGENTS.md`; no generated override or global settings.

Files under each host's `files/` directory are ready to copy after reviewing destination conflicts. This release supplies assets, not automated CLI synchronization. Preserve existing instructions and settings. The typed-UI profile is opt-in.

See [installation and verification boundaries](../references/native-adapters.md). Asset validation is executable; actual host sessions and instruction adherence are not yet measured. No hook, permission, MCP or command execution is configured by these assets.
