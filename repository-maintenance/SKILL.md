---
name: repository-maintenance
description: "Reconcile repository issues, PRs and branches against current source and acceptance evidence; apply explicitly authorized tracker or branch cleanup. Use for stale backlog and merged-branch maintenance. Do not use for product-roadmap invention, general code cleanup, releases or Git history rewriting."
---
# Repository Maintenance

## Objective

Keep repository collaboration state consistent with actual delivery while preserving unmerged work and historical evidence.

## Inputs

Required: repositories and maintenance scope. Optional: issue/PR filters, base/default branch, acceptance criteria and existing cleanup authorization. A request to inspect or assess is read-only; identify source, tracker, merge and deletion authority separately.

## Context

Read project instructions, current working-tree state, default branch and only implicated issue/PR/source records. Use the [maintenance guide](references/maintenance.md) for evidence classifications and guarded branch deletion. No particular tracker, host CLI or sibling skill is required.

## Procedure

1. Resolve the repository set and action scope from the conversation. Do not interpret “all” as every repository or unrelated feature PR. Inspect first and ask only when the ambiguity materially changes mutations; continue useful independent work.
2. Fetch permitted current metadata and source identities without resetting local work. Distinguish open, merged, closed-unmerged and unavailable PR states. Commit/push only scoped changes when authorized; exclude generated caches and unrelated user edits.
3. Classify each requested issue from current acceptance evidence as absent, partial, implemented-unverified, verified, superseded or deferred. Distinguish source delivery, released availability and live/empirical verification. A commit, unchecked box, branch name or closed issue is not sufficient proof.
4. Identify obsolete PRs by their actual purpose and diff against accepted current scope. Files removed during a redesign can establish supersession, but inspect for other surviving work. Do not merge retired scaffolding back into a deliberately reduced repository.
5. Propose or apply only authorized issue/PR changes. Close verified completed work as completed; distinguish superseded/not-planned work. Preserve unresolved acceptance and empirical gates. Confirm saved state and retain links; send comments or other messages only when requested.
6. For authorized branch cleanup, protect default/protected branches, open-PR heads, active worktrees and unmerged work. Classify ancestry or an exact unchanged merged-PR tip, then recheck the current remote head before deletion. Use an expected-head guard when available; a changed head invalidates the plan.
7. Prune stale local remote-tracking refs after confirmed remote deletion. Delete local branches only when separately in scope, not checked out and proven included. Never force-reset, stash, clean unrelated work, rewrite shared history or delete releases/live data as a maintenance shortcut.

## Output

Give repository/source scope, issue/PR classifications, applied versus proposed actions, deleted and preserved branches with reasons, exact checks and unresolved evidence. Summarize counts while retaining an inspectable action list when many records change.

## Completion

Authorized maintenance is applied and read back; remaining work is preserved. Review-only tasks produce actionable classifications without mutations. Missing evidence or uncertain remote completion is not relabeled as successful cleanup.
