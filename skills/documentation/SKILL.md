# Documentation

Maintain the Agentic Harness information lifecycle:

```text
evidence → ADR → current truth → plan → task → implementation/validation
```

- `.agentic/REFERENCE.md` and `docs/research/` hold evidence and provenance.
- `.agentic/decisions/` records why durable choices were made.
- `.agentic/PRODUCT.md`, `ARCHITECTURE.md`, `DESIGN.md`, and `SECURITY.md` describe current accepted truth.
- `.agentic/plans/` holds temporary strategy.
- `.agentic/tasks/` holds active coordination state.
- `.agentic/docs/` holds deeper supporting knowledge.

Keep canonical files concise and link deeper detail. Do not use an ADR as current-state documentation or a plan as a durable decision. Detect stale links and contradictions, and update only documents whose truth actually changed.
