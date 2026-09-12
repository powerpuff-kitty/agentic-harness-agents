# Native context adapters

Status: experimental assets; manual installation after review. Tracking: agents #24. No CLI adapter-install command, hooks, permission mutations or host-execution results are implied.

## Delivered files and ownership

`adapters/assets.json` is the versioned inventory of these procedure-layer assets. It lists only reviewed public host documentation, source files, destinations and explicitly selected profiles. Canonical target structure and precedence still belong to the project and `agentic-harness`; deterministic synchronization belongs to `agentic-harness-cli`.

| Host | Base installation | Optional typed-UI profile |
| --- | --- | --- |
| Claude Code | `adapters/claude/files/CLAUDE.md` to project-root `CLAUDE.md` | Matching relative `.claude/rules/agentic-typed-ui.md` |
| Cursor | Keep the existing root `AGENTS.md`; no extra base file | Matching relative `.cursor/rules/agentic-typed-ui.mdc` |
| Codex | Keep the existing root `AGENTS.md`; no generated override | Not supplied in this slice |

The optional profile covers TypeScript, TSX and Vue filenames. It supplies a reminder to consult accepted context, not universal layer or UI requirements. Do not install it for unrelated work merely to increase the number of rules.

## Installation without replacing project truth

Review the destination and existing instructions before copying an asset. For an absent destination, copy the matching file from the selected host's `files/` tree. For an existing Claude root file, preserve its content and add the root import once only if it is absent; do not replace it. Resolve conflicting project instructions explicitly. For existing scoped files, compare and merge by review, retaining local changes. These manual steps are not claimed as an idempotent automatic installer.

Do not copy this repository's AGENTS.md into an application: each target owns its router. Keep its custom document paths and optional context routes. Do not generate global host settings or an AGENTS.override.md merely to force these instructions above existing rules. Keep required MIT notices when copying substantial authored procedure content.

## Native loading facts and sources

Documentation reviewed on 2026-09-12; host sessions not run.

[Claude Code memory documentation](https://code.claude.com/docs/en/memory) documents root CLAUDE.md imports and paths-scoped rules. The one-line bridge uses a relative import outside a code fence. After installing, inspect the host's `/context` memory list; the import syntax alone does not prove it loaded. Project exclusions and other instruction sources can affect delivery.

[Cursor rules documentation](https://cursor.com/docs/rules) documents native AGENTS.md and `.mdc` files with `globs` and `alwaysApply`. The optional asset uses comma-separated patterns with `alwaysApply: false`; no always-on duplicate router is generated. Check the rule's attachment in the installed host for a matching and nonmatching file.

[Codex AGENTS.md documentation](https://developers.openai.com/codex/guides/agents-md) documents native discovery and the precedence of AGENTS.override.md. Inspect existing ancestor/nested instructions and configured limits; do not silently delete overrides or change global preferences to make a test pass.

## Tests and evidence boundaries

Run `python3 .github/scripts/validate_agents.py` for existing structural/skill checks plus adapter asset validation and the regression suite. Direct entrypoints are `validate_adapter_assets.py` and unittest discovery for `test_adapter_assets.py` in that directory.

The tests exercise shipped bytes, active import syntax, scoped metadata, shared content, opt-in defaults, allowed destinations and explicit unverified host metadata. They do not emulate native glob engines, execute agents, install into a real user's checkout, test actual instruction adherence, or establish enforced controls. Documentation review and asset tests are not live-host compatibility certification.

A recorded host test must identify its exact version, asset revision and synthetic fixture, inspect the loaded instruction sources and both matching/nonmatching scope, and distinguish observed delivery from any measured task outcome. Do not record model self-report alone as proof of loading. No live-host result is included yet; every registry entry retains `host_execution.status: not-run` with no version or evidence.

## Remaining work

CLI-owned installation/synchronization must handle conflicts, repeat application, removal and unrelated user settings without loss; it must not interpret asset discovery as execution consent. Recorded host fixtures and optional host-specific enforcement integrations remain open in #24. The blocked draft check executor is not a dependency for shipping these context-only assets and is not changed here.
