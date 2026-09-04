# Canonical source resolution

Use `powerpuff-kitty/agentic-harness` as the authority for the filesystem contract, current architecture, catalog variants, packs, policies, profiles, presets, and schemas.

Current source layout:

```text
agentic-harness/
├── AGENTS.md
├── .agentic/               self-hosting project context
└── catalog/
    ├── variants/<name>/files/
    ├── packs/
    ├── policies/
    ├── profiles/
    ├── presets/
    └── schema/
```

A target project uses root `AGENTS.md` and local `.agentic/` project truth. That local accepted truth has priority for the project unless it conflicts with an installed mandatory policy. Installed procedures live under `.agents/skills/`.

Do not infer that a prompt or skill is authoritative merely because it is newer. If this repository and the canonical source disagree about architecture, surface the conflict and follow the accepted canonical revision until the discrepancy is resolved.

Legacy paths such as root `PRODUCT.md`, root `agentic.yaml`, `docs/decisions`, `agentic-harness/templates`, `agentic-harness/boilerplates`, and `agentic-harness/modules` are migration inputs or historical references—not the current contract.
