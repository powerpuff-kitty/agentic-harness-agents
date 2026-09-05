# Skill contract v1

Every `skills/<name>/SKILL.md` must be a valid Agent Skill and a durable, narrow procedure.

## Frontmatter

The file starts with YAML frontmatter containing **only**:

```yaml
---
name: skill-name
description: "What the skill does. Use when ... Do not use for ..."
---
```

`name` must match the directory. `description` is the primary Codex trigger and therefore owns all use/exclusion language. Keep it specific enough to distinguish adjacent skills.

## Required body sections

After the title, include:

- `## Objective` — the outcome this procedure owns;
- `## Inputs` — required and optional inputs;
- `## Context` — the minimal canonical context to load;
- `## Procedure` — ordered execution steps;
- `## Output` — required result shape/content;
- `## Completion` — verification and stopping conditions.

Do not add a redundant "when to use" body section; Codex decides whether to load the body from the frontmatter description.

## Routing

Adjacent skills must have explicit exclusions in their descriptions. Examples:

- `codebase-audit` owns broad technical quality; `agentic-structure-audit` owns agent-readiness structure.
- `security-review` owns implementation/configuration review; `threat-model` owns pre-change system threat analysis.
- `migration` owns filesystem/contract migration; `dependency-upgrade` owns package/dependency changes.
- `design-system` owns creation/evolution; `design-system-compliance` owns conformance checking.

## Procedure quality

- Prefer repository evidence and deterministic tools over generic advice.
- Preserve project-owned truth.
- State approvals before high-impact writes.
- Use progressive disclosure from `references/context-engineering.md`.
- Separate deterministic findings from heuristic judgment.
- Do not claim checks ran when they did not.
