---
name: migration
description: "Migrate legacy Agentic Harness repository layouts or canonical-context locations to the current root AGENTS.md plus .agentic contract with conflict detection, backup, and idempotence. Use when filesystem/project-contract migration is the primary task. Do not use for dependency upgrades, database migrations, or fresh project initialization."
---
# Agentic Harness Migration

## Objective

Migrate context without losing local work, broadening instruction scope or silently resolving divergent truth.

## Inputs

Required: target repository and reviewed target contract. Optional: approved scope, backup destination and available checks.

## Context

Read applicable root/nested rules and affected sources, destinations and references only. For apply, conflicts or recovery, load the [local guide](references/migration-guide.md). Read-only review needs no CLI or Jev; missing contract evidence blocks apply.

## Procedure

1. Inventory exact source/destination identities, ownership and dirty/untracked context. Classify absent, identical, divergent and unresolved entries; filenames alone do not establish authority.
2. Produce a non-writing plan, including references, conflicts, backup and required checks. Unresolved conflicts block apply; only a separately approved disjoint subset may proceed.
3. Bind approval to the plan and recheck inputs/policy before writes; drift requires fresh review. Verify a restorable backup outside the target, including affected local work.
4. Write and verify approved destinations before separately authorized source removal. Preserve custom routes. On failure stop and inspect partial state before approved recovery; never blind cleanup.
5. Update only implicated router/adapter links, schema-correct manifest fields, real provenance and decision indexes. Do not invent hashes, results or unsupported commands.
6. Review the diff and run available permitted checks. Repeat the read-only plan, not apply, for idempotence. Retain conflicts, unavailable validation and unverified host loading.

## Output

Report planned/applied changes, duplicates/conflicts, backup evidence, check attempts and remaining decisions. Reuse an approved record when needed; no routine transcript replay or extra report file.

## Completion

No source was lost; approved changes are verified and a repeat read-only plan proposes no further scoped changes. Missing validation is not success; partial migration is not whole-project completion.
