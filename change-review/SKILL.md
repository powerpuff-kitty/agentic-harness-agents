---
name: change-review
description: "Review a specified diff, branch, PR or pending change against accepted requirements for defects, regressions and compatibility. Use for focused code review and review-feedback verification. Do not use for whole-repository audits, lint-only cleanup, or release readiness; review does not authorize fixes, approval or merge."
---
# Change Review

## Objective

Find actionable defects and material verification gaps in the requested change, tied to the actual diff and accepted behavior.

## Inputs

Required: repository and change scope. Optional: PR, base/head revisions, requirement, reviewer feedback and excluded areas. Infer the comparison from available task/PR context when clear; ask only if competing bases materially change the review.

## Context

Read project review rules, current worktree state, the change and affected callers/tests. Use the [review method](references/review-method.md) for base selection, uncertain findings and feedback disagreements. Specialist procedures are optional when their exact question is needed and available.

## Procedure

1. Pin the compared source states. A branch review commonly uses the merge-base diff; a commit review or pending worktree review may need another comparison. Include staged, unstaged and relevant new files when in scope, and disclose exclusions.
2. Establish the intended behavior from the request, issue/spec and accepted project contracts. Distinguish requested changes from unrelated baseline defects. Do not use the author's explanation or green checks as proof of correctness.
3. Trace changed inputs, outputs and important side effects through callers and tests. Look for concrete failure cases in boundaries, errors, resource ownership, concurrency, persistence and public compatibility relevant to this diff.
4. Verify a suspected finding by source tracing, a safe reproduction or applicable native check. State preconditions and counterevidence. A possible concern without an established impact belongs in questions or limitations, not an invented high-severity bug.
5. Report location, triggering condition, impact, evidence, priority and a focused correction/verification direction. Prefer the smallest relevant line span in the changed code; explain when an unchanged caller makes the defect observable. Omit unsupported stylistic preferences.
6. Check that important changed behavior has meaningful verification. Keep unavailable checks explicit. Do not expand every review into a full security, performance or repository audit.
7. Review requests are read-only by default. Apply fixes or resolve feedback only when authorized, recheck the affected snapshot and preserve independent-review boundaries. Approving, merging or posting comments requires the existing task's action scope; a role or skill name grants none.

## Independent reviewer context

When an independent pass is requested, use a separate fresh reviewer session with
history inheritance disabled when supported. Pass accepted requirements, project
rules and raw compared source; omit the author’s diagnosis, desired verdict and
prior review conclusions until the initial report is retained. Report unavailable
isolation honestly. Reproduce findings and recheck after source changes; changing
role names within the author session does not establish independence.

## Output

Lead with prioritized findings and exact source references, then questions and verification gaps. If no actionable defect is established, say so with the inspected scope and check limits. Separate comments considered, confirmed, refuted and unresolved when reviewing feedback.

## Completion

The specified change and relevant dependencies have been reviewed, findings have concrete evidence and the report does not imply whole-product readiness or checks that did not run.
