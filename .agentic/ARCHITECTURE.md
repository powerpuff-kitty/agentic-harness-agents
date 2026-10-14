# Architecture

This repository owns reusable coding-agent procedures and their distribution. Specialist roles and team workflows are managed separately. Harness-specific skills consume canonical `agentic-harness` truth and use `agentic-harness-cli` for deterministic mechanics; generic skills use the target project’s own context and verification tools.

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

## Design Intelligence skill topology

Design work is intentionally split by responsibility so no single mega-skill conflates product decisions, art direction, implementation primitives, and verification:

```text
design-intelligence
├── design-analysis
├── design-research
├── identity-design
├── product-design
├── design-system
├── component-resolution
├── design-system-compliance
└── accessibility-audit
```

`design-intelligence` orchestrates the lifecycle but delegates specialist work. Canonical Design Genome/Analysis/Task/Diff schemas remain owned by `agentic-harness`; deterministic analyzers, preservation/compilation, and related mechanics remain owned by `agentic-harness-cli`/other deterministic surfaces.

The procedure layer may interpret evidence and propose changes, but must not silently promote references, model inference, external component defaults, or frequency observations into approved project truth.

Authored procedures, prompts, adapters, references and evals use the root MIT
[LICENSE](../LICENSE). Canonical licensing scope and generated-project attribution
are defined by `agentic-harness` ADR-007. When copying substantial skill content,
retain the MIT notice; third-party material retains its existing terms.
