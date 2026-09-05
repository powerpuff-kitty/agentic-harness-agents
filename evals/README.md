# Agent behavior evals

Evals validate procedure routing and behavior rather than only file presence.

- `routing.json` gives at least one positive routing case for every registered skill and explicit nearby skills that must not be selected.
- `skill-quality.md` defines cross-skill behavior expectations for context discipline, evidence, approvals, output, and completion.
- `layout-v1.md` continues to cover the Agentic Harness filesystem contract.

CI verifies that every registered skill has routing coverage and that routing references only known skills.
