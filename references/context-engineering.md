# Context engineering

Canonical authority is `agentic-harness/.agentic/docs/context-engineering.md`. This reference translates that standard into procedure-authoring rules for this repository; it does not replace the canonical source.

## Progressive disclosure

Give the agent the smallest relevant context that lets it complete the task safely and correctly.

- Root `AGENTS.md` is a router and precedence map, not an encyclopedia.
- A skill should load only the project truth needed for its current procedure.
- Do not instruct agents to read all of `.agentic/`, all ADRs, or the whole repository before routine work.
- Large skills should keep `SKILL.md` concise and move specialist tables, examples, checklists, or scripts into skill-local `references/`, `scripts/`, or `assets/` when needed.
- Prefer outcome constraints and explicit completion criteria over unnecessary reasoning recipes.
- Project truth is model-independent. Model/profile guidance may change context density or procedure selection, never architecture, policy, or accepted decisions.

## Source precedence

Unless a stricter project rule applies:

1. user instruction and installed mandatory policy;
2. target repository's accepted `.agentic/` truth and ADRs;
3. installed packs and canonical defaults;
4. skill procedure;
5. task prompt.

A newer skill is not automatically more authoritative than local accepted project truth.

## Safe autonomy

Local inspection, scoped edits, and non-destructive verification may proceed when the project permits them. Secret access, destructive operations, production/release actions, irreversible migrations, policy changes, and broad rewrites require the approvals declared by the target project.

## Completion

A task is complete when requested behavior or analysis is delivered, applicable verification has run, durable truth is updated when it actually changed, and unresolved risks or skipped checks are stated.
