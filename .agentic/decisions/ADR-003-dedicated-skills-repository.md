# ADR-003: Name the dedicated procedure repository skills

- Status: accepted
- Date: 2026-10-14
- Deciders: project owner
- Supersedes: none

## Context

The name `agentic-harness-agents` obscured that this repository distributes
reusable skills. Specialist roles and team workflows are managed separately. The owner accepted
a dedicated `skills` repository with clear ownership.

## Decision

Rename the existing GitHub repository to `powerpuff-kitty/skills`, preserving
history, issues and tags. Keep reusable procedures, skill references, prompts,
skill adapters and behavior evaluations here. Keep project-specific procedures
in their project repositories. Harness contracts remain owned by `agentic-harness`
and deterministic tooling by `agentic-harness-cli`.

Update current links, plugin/marketplace identity and new collection archive names.
Keep individual skill names, installation paths, existing published assets and
pinned content unchanged. Historical provenance may retain the former repository
name. Existing plugin imports require explicit host-side migration and loading
verification; the rename alone does not update installed copies.

## Alternatives

Retain the old name, or create a new repository and move the collection. Renaming
makes ownership clearer while preserving the existing repository and its history.

## Consequences

The repository name identifies its skill collection. Downstream source declarations and
current documentation must use the new repository URL, while provenance and old
release archives remain reproducible. The rename publishes no new release and
changes no target-project contract or skill behavior.
