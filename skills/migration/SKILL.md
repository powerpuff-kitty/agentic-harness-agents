---
name: migration
description: "Migrate legacy Agentic Harness repository layouts or canonical-context locations to the current root AGENTS.md plus .agentic contract with conflict detection, backup, and idempotence. Use when filesystem/project-contract migration is the primary task. Do not use for dependency upgrades, database migrations, or fresh project initialization."
---
# Agentic Harness Migration

## Objective

Move legacy harness content to the current canonical project contract without losing project-authored truth or silently resolving divergent sources.

## Inputs

Required: target repository. Optional: desired target contract version, dry-run/apply mode, backup location, conflict policy, and known legacy paths.

## Context

Read root/legacy instruction files, current `.agentic/` if present, canonical migration guidance, and only source/destination content implicated by the migration.

## Procedure

1. Detect legacy and current layouts and classify each source as canonical, duplicate, divergent, generated, or obsolete.
2. Produce a non-writing move/conflict plan first.
3. Compare content before deciding whether duplicates are identical; never overwrite divergent canonical truth silently.
4. Require explicit apply authorization where project policy or conflicts demand it.
5. Write/verify the destination before deleting or archiving a source; preserve conflicts in a backup/report location.
6. Update router links, manifest/lock metadata, ADR indexes, and thin adapters.
7. Run migration again to prove idempotence, then run doctor/validate/audit where available.

## Output

Return dry-run/apply report, moves, duplicates, conflicts, backups, router/metadata changes, verification, and remaining manual decisions.

## Completion

No source is lost before verification, divergent truth remains reviewable, the target contract validates, and a second migration produces no changes.
