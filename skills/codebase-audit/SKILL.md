# Codebase Audit

Perform a read-only, evidence-backed audit unless repair is explicitly requested.

Evaluate:

- code quality and maintainability;
- architecture and dependency boundaries;
- tests, CI, coverage evidence, and release gates;
- security controls and secret/dependency scanning;
- operations, rollback, observability, backups, and incidents;
- documentation freshness and canonical project truth;
- root hygiene and valid `AGENTS.md` routing;
- duplicate or conflicting canonical files;
- ADR filename/status/index/supersession integrity;
- generic placeholder content in required truth files;
- declared maturity/profile requirements;
- thin vendor adapters;
- installed pack/policy/skill versus lockfile integrity;
- design-system component/token compliance when active.

For every finding state severity, dimension, repository evidence, why it matters, deterministic versus agent-assisted basis, and a repair path. Explicitly list checks not performed. Do not infer production readiness solely from file presence.
