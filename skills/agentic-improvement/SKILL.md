# Agentic Improvement

Use when the user asks to improve a repository's agentic structure, optimize it for a target model, or plan migration between model profiles.

Start from canonical CLI findings. Produce a previewable plan before modifying files.

Group changes as:

- remove — stale, duplicate, contradictory, or unconditional guidance;
- change — narrow triggers, improve routing, clarify completion/autonomy boundaries;
- add — missing router/index, completion semantics, evidence-backed adapter guidance, or validation hooks.

Keep canonical project truth model-independent. Model-specific changes belong only in thin adapters/profiles and may not redefine architecture, business rules, security policy, or accepted decisions.

For model migration, compare source and target profiles, identify only guidance affected by the change, and show current versus expected compatibility.

Do not perform destructive, broad, release, secret, or production changes without explicit approval. Prefer deterministic transformations; present uncertain changes as recommendations rather than applying them automatically.
