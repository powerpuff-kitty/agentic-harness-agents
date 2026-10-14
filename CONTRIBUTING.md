# Contributing to Skills

Thanks for improving the installable agent procedures. This repository owns **skills, reusable procedures, prompts, thin adapters, and behaviour evaluations**. Canonical project context, profiles, schemas and readiness policies belong in [Agentic Harness](https://github.com/powerpuff-kitty/agentic-harness); native CLI behaviour belongs in [Agentic Harness CLI](https://github.com/powerpuff-kitty/agentic-harness-cli).

## Before making changes

1. Read [AGENTS.md](AGENTS.md), [the skill contract](references/skill-contract.md) and [context engineering guidance](references/context-engineering.md).
2. Decide whether the change belongs in `skills/`, `prompts/`, `adapters/`, `references/`, `evals/` or an upstream canonical repository.
3. Keep trigger descriptions narrow and procedures explicit about inputs, outputs, completion, side effects, and model/tool assumptions.
4. Never store credentials, private project context or customer information in examples or fixtures.
5. Explain any cross-repository compatibility requirements in the pull request.

## Validation

Use Python 3 to run the same checks present in the repository's CI workflow:

```sh
python3 .github/scripts/validate_agents.py
python3 .github/scripts/validate_design_intelligence.py
python3 .github/scripts/package_plugin.py
```

The packaging step generates `dist/` artifacts. Review the generated bundle and hashes before publishing. Update manifests and behavioural evaluations when procedures are renamed or materially changed. Do not claim that a package is released simply because a local zip was built.

## Pull requests

Describe the user task, affected skills, the source of canonical truth, backward-compatibility impact, how validation was run, and any remaining gaps. Small focused changes with evidence are easier to review than unrelated skill bundles.

Security vulnerabilities should be disclosed privately to maintainers rather than through a public issue.
