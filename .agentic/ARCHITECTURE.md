# Architecture

This repository is the procedure and distribution layer between canonical Agentic Harness truth and deterministic CLI enforcement.

```text
canonical agentic-harness
        ↓
references + skill frontmatter routing
        ↓
skills/ + prompts/ + adapters/
        ↓
Codex plugin / individual skill install
        ↓
target .agents/skills/
        ↓
CLI and repository-native verification
```

`skills/` contains Agent Skills with required YAML frontmatter and a common procedural contract. `references/` contains shared context/source rules loaded only when needed. `evals/` owns routing and behavior acceptance cases. `.codex-plugin/` and `.agents/plugins/` are distribution metadata only and do not become architecture authority.
