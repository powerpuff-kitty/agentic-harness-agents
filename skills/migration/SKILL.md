# Harness Migration

Migrate legacy Agentic Harness layouts to root `AGENTS.md` plus canonical `.agentic/` context.

## Required behavior

1. Inventory legacy root truth, `agentic.yaml`, `docs/decisions`, `docs/plans`, `docs/tasks`, root `evals`, packs/policies, skills, and vendor adapters.
2. Map each source to its new destination and generate a dry-run report.
3. Classify destinations as absent, byte-identical duplicate, or content conflict.
4. Stop apply when unresolved canonical conflicts exist.
5. When applying, optionally create a backup, write destinations, verify content, then remove only successfully migrated legacy sources.
6. Create/update `.agentic/README.md`, `manifest.yaml`, `lock.json`, root router, and thin adapters without replacing project-specific truth with generic content.
7. Run migration again; the second run must make no semantic changes.
8. Run doctor, validation, repository checks, and audit.

Never hide uncertainty about which legacy file is authoritative.
