# Agent instructions

This repository owns Agentic Harness procedures, prompts, and adapters—not the canonical project contract.

1. Read `.agentic/README.md` and `.agentic/manifest.yaml` for this repository's own context.
2. Resolve canonical project structure, packs, policies, profiles, presets, and schemas from `powerpuff-kitty/agentic-harness`.
3. The canonical target contract is root `AGENTS.md` plus `.agentic/`; reusable procedures install under `.agents/skills/`.
4. Put durable procedure in `skills/`, short invocation entrypoints in `prompts/`, vendor guidance in `adapters/`, shared operating guidance in `references/`, and agent-behavior acceptance criteria in `evals/`.
5. Do not duplicate or redefine canonical architecture, product truth, policies, or catalog content here.
6. Keep adapters thin and route them to the target repository's `AGENTS.md` and `.agentic/` context.
7. Treat legacy root-level truth and `docs/decisions` as migration inputs, not current canonical paths.
8. Update the manifest and validation whenever skills or prompts change.
9. Run repository validation before completion and surface any cross-repository contract mismatch.
