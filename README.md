# Agentic Harness Agents

[![Status: Beta](https://img.shields.io/badge/status-beta-orange)](.agentic/PRODUCT.md)
[![Validate agents](https://github.com/powerpuff-kitty/agentic-harness-agents/actions/workflows/validate.yml/badge.svg)](https://github.com/powerpuff-kitty/agentic-harness-agents/actions/workflows/validate.yml)

Reusable skills, prompts, adapters, references, and agent-behavior evaluations for Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, and other coding agents.

This repository owns **procedure**, not canonical project architecture. The source of truth is [`agentic-harness`](https://github.com/powerpuff-kitty/agentic-harness); deterministic mechanics live in [`agentic-harness-cli`](https://github.com/powerpuff-kitty/agentic-harness-cli).

```text
agentic-harness
project contract + catalog + policies + schemas
        ↓
agentic-harness-agents
skills + prompts + adapters + agent evals
        ↓
agentic-harness-cli
deterministic composition, migration, audit, validation
```

## Canonical target model

```text
project/
├── AGENTS.md
├── normal project files
├── .agentic/       project truth, governance, decisions, plans, tasks, docs, evals
└── .agents/skills/ installed reusable procedures
```

Skills must read `.agentic/manifest.yaml`, follow `.agentic/README.md` routing and precedence, and preserve project-owned truth. Vendor files are adapters only.

## Repository map

```text
skills/       durable reusable procedures
prompts/      short task entrypoints
adapters/     vendor-specific integration guidance
references/   shared safety, discovery, precedence, and source-resolution rules
evals/        agent-behavior acceptance criteria
manifest.json versioned skill inventory
.agentic/     this repository's own project context
```

## Core workflows

- `agentic-app`: initialize, migrate, upgrade, and audit an agent-native project.
- `codebase-audit`: evidence-backed technical and harness compliance audit.
- `migration`: conflict-aware migration to the `.agentic/` contract.
- `adr-management`: create, supersede, and index durable decisions.
- `documentation`: maintain the truth → ADR → plan → task lifecycle.
- `adapter-sync`: keep vendor adapters thin and deterministic.
- `security-review`, `threat-model`, `release`, and `release-review`: higher-risk review procedures.
- `design-system` and `design-system-compliance`: plan and enforce UI system usage.

See [`manifest.json`](manifest.json) for the full inventory.

## Typical use

```text
Prompt selects a task
        ↓
Skill defines the procedure
        ↓
References define shared safety/source rules
        ↓
Canonical project context supplies truth
        ↓
CLI/repository checks supply deterministic evidence
```

A skill may explain how to work with an ADR or architecture document; it may not decide the project's architecture merely because the skill is newer.
