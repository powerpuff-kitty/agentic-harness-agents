# Design lifecycle handoff

This is procedure guidance, not a schema or an implementation of the CLI/app.

## Locate authority and tools

Use target AGENTS.md → .agentic/manifest.yaml → relevant design/product truth.
Locate the approved Genome/Task/Analysis artifacts from project configuration; do not
invent a universal target filename. If DESIGN.md and a Genome disagree, stop the
conflicting promotion and request a recorded resolution. Do not resolve conflicts
by recency alone.

The canonical schema owner is `powerpuff-kitty/agentic-harness`, under
`catalog/schema/`. Use the project's pinned version. Do not copy schemas into this
skills repository as new authoritative definitions.

The reviewed source implementation at CLI revision
`0c7897b229a44783e8be3db66d2e54d24afcf41c` exposes these experimental operations:

```bash
# Only inside a trusted CLI source checkout after inspecting its launcher/help.
./ah design analyze /path/to/project --level static --output /path/to/before.json
./ah design preserve --analysis /path/to/before.json --output /path/to/candidate.json
# Pause for explicit review and produce an approved Genome. No approval CLI assumed.
./ah design prompt --genome /path/to/approved.json --task /path/to/task.json --output /path/to/brief.md
# After authorized implementation, run static analysis to a NEW after.json.
./ah design diff /path/to/before.json /path/to/after.json --output /path/to/diff.json
```

Do not run a target project's arbitrary `./ah` as if it were this trusted launcher.
For installed binaries inspect their help/version first. The source launcher and
released `ah` are not assumed to have identical subcommands. Never overwrite
before/approved artifacts using a generated output path; request approval for any
existing destination. Local analysis does not require a paid model or provider.

## Capability limits at that revision

- Static measurements: hexadecimal declarations, font-size/spacing/radius pixel
  values, CSS custom-property definition/reference evidence.
- Preserve: candidate only; no automatic intent inference or approval.
- Prompt: approved Genome plus structured Task, task-scoped model-neutral Markdown.
- Diff: measured vocabulary/count/finding/check changes, not a subjective score.
- Do not assume runtime contrast/accessibility scans, provider browsing/install,
  external-AI ingestion, model-specific adapters, full token exports or research
  indexing. Discover later capabilities rather than inventing commands.
- The initial compiler does not serialize every Genome field or fully implement
  all rule exception/precedence semantics. Inspect the emitted brief for missing
  visual values, sources, accessibility/anti-pattern fields and exceptions. A
  missing required constraint blocks claiming a complete implementation brief.
  Supply the approved canonical context separately and report the compiler gap;
  do not silently rewrite generated output or remove the required constraint.

## Handoff sequence

| Stage | Input | Output | Stop/gate |
| --- | --- | --- | --- |
| Analyze | Scoped source or supplied evidence | Analysis with provenance and check boundary | Invalid/stale/unsupported evidence |
| Preserve | Validated Analysis | Candidate Genome and unresolved intent | Exact candidate review required |
| Compile | Approved project-designated Genome + Task | Deterministic brief + coverage report | Missing approval/required context |
| Verify | Comparable before/after evidence | Diff + scoped review | No automatic baseline replacement |

A candidate can be reviewed manually or with an independently available app.
No stage requires uploading source or sharing an AI account. Before sending an
analysis to an external model, review paths, snippets, personal data and secrets;
share only the subset authorized for that destination. Keep original evidence
local and immutable. Artifact exchange is interoperability, not proven feature
parity between app and CLI.

## Approval and uncertainty

The agent may propose edits but cannot invent a human reviewer or set approval
because a file says it is approved. Respect project-designated authority, the
actual review event and any signatures/hashes the project requires. Approval of
one revision does not authorize a changed revision. Record unknowns explicitly;
acknowledging a missing check does not mean it passed.
