# Model Fit

Use when the user asks which supported model best fits a repository or task, or asks to compare models for the current project.

Use the canonical model registry from `agentic-harness` and CLI analysis. Do not invent model rankings from reputation or stale prompt lore.

For each candidate model, distinguish:

1. project/task suitability;
2. compatibility with the repository's current agentic structure;
3. expected compatibility after proposed structural improvements.

Support task-scoped comparison such as frontend work, refactoring, architecture, security review, migration work, or routine implementation.

Always expose evidence/confidence behind model-specific claims and state that rankings are repository/task specific, not a universal leaderboard.

When no target model is supplied, compare supported evidence-backed profiles. When evidence is insufficient, say so instead of manufacturing a score.
