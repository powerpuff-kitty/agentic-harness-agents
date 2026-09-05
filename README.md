# Agentic Harness Agents

[![Status: Beta](https://img.shields.io/badge/status-beta-orange)](.agentic/PRODUCT.md)
[![Validate agents](https://github.com/powerpuff-kitty/agentic-harness-agents/actions/workflows/validate.yml/badge.svg)](https://github.com/powerpuff-kitty/agentic-harness-agents/actions/workflows/validate.yml)

**Installable Agent Skills for Codex, plus compatible procedures and adapters for Claude Code, Cursor, GitHub Copilot, Gemini CLI, and other coding agents.**

Current distribution version: **`0.4.0-beta.1`**.

This repository owns **procedure**, not canonical project architecture. Canonical project truth lives in [`agentic-harness`](https://github.com/powerpuff-kitty/agentic-harness); deterministic composition and audits live in [`agentic-harness-cli`](https://github.com/powerpuff-kitty/agentic-harness-cli).

```text
agentic-harness
project contract + catalog + policies + schemas + model registry
        ↓
agentic-harness-agents
skills + prompts + adapters + behavior evals
        ↓
agentic-harness-cli
deterministic composition, migration, audit, validation
```

## Quick start

### Install one skill in Codex

Use Codex's built-in `$skill-installer` with a GitHub skill directory, then restart Codex so the skill is rediscovered:

```text
$skill-installer install https://github.com/powerpuff-kitty/agentic-harness-agents/tree/main/skills/agentic-app
```

Replace `agentic-app` with any directory under [`skills/`](skills/). For reproducible team installs, prefer a release tag instead of `main`.

### Use skills project-locally

Codex discovers repository skills from real directories under `.agents/skills/`:

```text
project/
├── AGENTS.md
├── .agentic/
└── .agents/
    └── skills/
        ├── agentic-app/
        │   └── SKILL.md
        └── security-review/
            └── SKILL.md
```

`agentic-harness-cli` installs selected skills into that location during composition.

### Install the whole collection as a Codex plugin

This repository is a skills-only Codex plugin. Its native manifest is [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json), and its GitHub marketplace manifest is [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json).

Workspace admins can import the repository as a GitHub plugin marketplace from **Workspace settings → Plugins → Add → Import marketplace**. Use the repository URL, leave Path empty, and select a branch, tag, or commit depending on whether you want automatic updates or an immutable version.

No external app or account authorization is required because this plugin contains skills only.

## Canonical target model

```text
project/
├── AGENTS.md
├── normal project files
├── .agentic/       project truth, governance, decisions, plans, tasks, docs, evals
└── .agents/skills/ installed reusable procedures
```

Skills read only the context relevant to the current task. Root `AGENTS.md` stays compact, `.agentic/` remains canonical project truth, and vendor adapters remain thin.

## Repository map

```text
skills/                     installable Agent Skills
prompts/                    short task entrypoints
adapters/                   vendor-specific integration guidance
references/                 shared source, safety, context, and skill-contract rules
evals/                      behavior and routing acceptance criteria
.codex-plugin/plugin.json   native Codex plugin manifest
.agents/plugins/            GitHub marketplace manifest
manifest.json               version, compatibility, and skill inventory
.agentic/                   this repository's own project context
```

## Skill contract

Every `skills/<name>/SKILL.md` follows the Agent Skills format:

- YAML frontmatter with only `name` and `description`;
- the description owns triggering and exclusions;
- concise procedural body using progressive disclosure;
- explicit `Objective`, `Inputs`, `Context`, `Procedure`, `Output`, and `Completion` sections;
- project truth remains external to the skill.

See [`references/skill-contract.md`](references/skill-contract.md) and [`references/context-engineering.md`](references/context-engineering.md).

## Core workflows

- `agentic-app` — initialize, migrate, upgrade, or audit an agent-native project.
- `agentic-structure-audit` — score Agentic Readiness without conflating it with ordinary code quality.
- `model-fit` — compare evidence-backed model profiles for a repository or task.
- `agentic-improvement` — plan and apply targeted agentic-structure improvements.
- `migration` — migrate legacy repository layouts safely and idempotently.
- `adr-management` — create, supersede, and index durable decisions.
- `adapter-sync` — keep vendor adapters thin and canonical.
- specialist review/design/delivery skills cover security, accessibility, performance, API/data, product, design systems, releases, incidents, and research.

See [`manifest.json`](manifest.json) for the complete inventory.

## Validation

CI validates skill frontmatter, required procedural sections, trigger overlap, behavior-eval coverage, plugin manifests, canonical-version pins, adapters, prompts, and the repository's own `.agentic/` contract.

```bash
python3 .github/scripts/validate_agents.py
python3 .github/scripts/package_plugin.py
```

The package command produces a versioned plugin ZIP and SHA-256 checksum under `dist/`.
