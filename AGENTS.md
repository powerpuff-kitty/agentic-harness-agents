# Agent instructions

This repository owns Agentic Harness procedures, prompts, adapters, and behavior evals—not the canonical project contract.

1. Read `.agentic/README.md` and `.agentic/manifest.yaml` for this repository's own context.
2. Resolve canonical project structure, packs, policies, profiles, presets, schemas, Agentic Readiness rules, and model profiles from `powerpuff-kitty/agentic-harness`.
3. The canonical target contract is root `AGENTS.md` plus `.agentic/`; reusable procedures install under `.agents/skills/`.
4. Every skill must follow `references/skill-contract.md`: Agent Skills YAML frontmatter (`name`, `description` only), narrow trigger description, explicit procedure/output/completion sections, and progressive disclosure.
5. Follow `references/context-engineering.md`: load only task-relevant context and never require blanket reading of `.agentic/` or the repository.
6. Put durable procedure in `skills/`, short invocation entrypoints in `prompts/`, vendor guidance in `adapters/`, shared operating guidance in `references/`, and behavior acceptance criteria in `evals/`.
7. Do not duplicate or redefine canonical architecture, product truth, policies, readiness scoring, model profiles, or catalog content here.
8. Keep adapters thin and route them to the target repository's `AGENTS.md` and `.agentic/` context.
9. Treat legacy root-level truth and `docs/decisions` as migration inputs, not current canonical paths.
10. Update `manifest.json`, plugin manifests, routing evals, and validation whenever skills are added, removed, renamed, or materially retargeted.
11. Run `python3 .github/scripts/validate_agents.py` before completion and surface any cross-repository contract mismatch.
