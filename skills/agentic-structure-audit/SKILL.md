# Agentic Structure Audit

Use when the user asks to evaluate how agent-ready a repository is, or how well its current agentic structure fits a specific model.

Prefer machine-readable output from `agentic-harness-cli` (`ah-agentic audit --json`, or `ah agentic audit --json` when integrated) rather than reimplementing scoring in prompt text.

Report separately:

- Universal Agentic Structure Score;
- optional model compatibility score;
- highest-impact findings first;
- exact repository evidence;
- confidence (`deterministic`, `heuristic`, or `profile-backed`);
- concrete remediation.

Inspect only context relevant to findings. Do not force broad project-document loading just to audit agentic structure.

Key dimensions include context routing, `AGENTS.md`, skill overlap, completion semantics, decision boundaries, verification, architecture discoverability, decision history, model portability, instruction health, and agent security.

Do not treat ordinary code quality as the agentic score. If the CLI is unavailable, state that the result is a qualitative fallback rather than a canonical score.
