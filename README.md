# Agentic Harness Agents

Agent-facing skills, prompts, adapters, and reusable workflows for Agentic Harness.

This repository **does not own canonical architecture**. The main source of truth is [`powerpuff-kitty/agentic-harness`](https://github.com/powerpuff-kitty/agentic-harness). Skills must resolve canonical boilerplates, packs, policies, profiles, presets, schemas, and architecture from that repository before inventing project rules.

Deterministic tooling lives in [`powerpuff-kitty/agentic-harness-cli`](https://github.com/powerpuff-kitty/agentic-harness-cli).

```text
agentic-harness (truth + boilerplates)
        ↓
agentic-harness-agents (procedures)
        ↓
agentic-harness-cli (deterministic enforcement)
```

## Repository shape

```text
skills/       reusable SKILL.md procedures
prompts/      reusable task prompts
adapters/     thin agent/vendor adapters
references/   shared agent-operating guidance
evals/        agent-behavior evaluation guidance
manifest.json versioned skill inventory
```

Prompts should be short task entry points. Durable procedure belongs in skills. Durable architecture/product knowledge and boilerplate definitions belong in `agentic-harness`, not here.
