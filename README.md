# Agentic Harness Agents

[![Status: Beta](https://img.shields.io/badge/status-beta-orange)](https://github.com/powerpuff-kitty/agentic-harness-agents)
[![Validate agents](https://github.com/powerpuff-kitty/agentic-harness-agents/actions/workflows/validate-agents.yml/badge.svg)](https://github.com/powerpuff-kitty/agentic-harness-agents/actions/workflows/validate-agents.yml)

**Reusable coding-agent skills, prompts, workflows, and thin adapters for Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, and other agentic development tools.**

This repository is the procedural layer of Agentic Harness. It teaches agents **how to work** while [`agentic-harness`](https://github.com/powerpuff-kitty/agentic-harness) remains the canonical source for project architecture, boilerplates, modules, policies, profiles, presets, and schemas.

> **Status: Beta.** Skills are usable today, but the skill catalog and adapter surface may evolve before 1.0.

## Works with

- OpenAI Codex
- Claude Code
- Cursor
- GitHub Copilot
- Gemini CLI
- other filesystem/tool-using coding agents

## Ecosystem

```text
agentic-harness          what is true
        ↓
agentic-harness-agents   what agents should do
        ↓
agentic-harness-cli      how it is applied and checked
```

- **[agentic-harness](https://github.com/powerpuff-kitty/agentic-harness):** canonical boilerplates, architecture and modules
- **This repository:** reusable skills, prompts, adapters and agent workflows
- **[agentic-harness-cli](https://github.com/powerpuff-kitty/agentic-harness-cli):** native Rust `ah` CLI and deterministic enforcement

## Repository shape

```text
skills/       reusable SKILL.md procedures
prompts/      reusable task prompts
adapters/     thin agent/vendor adapters
references/   shared agent-operating guidance
evals/        agent-behavior evaluation guidance
manifest.json versioned skill inventory
```

## Skill catalog

The repository includes procedures for areas such as:

- agent-native project setup and upgrades
- codebase audits and implementation planning
- security review and threat modeling
- design systems and product design
- accessibility and performance audits
- API and database design
- migrations and dependency upgrades
- releases, documentation and incident review
- competitive research and marketing

Browse [`skills/`](skills) for the current catalog.

## Source-of-truth rule

Before a skill or prompt makes architectural assumptions, it resolves the canonical source in [`agentic-harness`](https://github.com/powerpuff-kitty/agentic-harness):

```text
agentic-harness/
├── base/
├── web-app/
├── backend-api/
├── saas/
├── monorepo/
├── library-sdk/
├── modules/
│   ├── packs/
│   ├── policies/
│   └── profiles/
├── presets/
└── schema/
```

Skills describe procedure; they do not silently redefine canonical architecture. Prompts should be short entry points, durable workflow belongs in skills, and vendor adapters should remain thin.

## Contributing

New skills should be reusable across projects, explicit about evidence and safety boundaries, and avoid duplicating canonical architecture from the static repository. Issues and pull requests are welcome during beta.
