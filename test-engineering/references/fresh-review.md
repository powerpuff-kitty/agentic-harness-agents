# Independent review in a fresh session

Use this method when an independent test/audit pass is requested, or when a
consequential verification gap warrants it and delegation is available and
within scope. A small reversible edit does not automatically require another agent.

## Prepare the handoff

Select a reviewer that did not author the change. Start a new session with
conversation/history inheritance disabled using the host's supported control.
A new role name inside the author's existing session is self-review. If the host
cannot establish isolation, record that limitation and label feasible checks
honestly; do not claim a fresh independent pass was completed.

Supply the task, accepted requirements, applicable project instructions, target
revision/worktree identity, raw source/tests/artifacts, allowed actions and review
scope. Preserve relevant safety constraints and existing authorization. These are
necessary review inputs, not author coaching. Do not pass the author's narrative,
suspected defect, proposed fix, desired verdict, previous audit findings or hidden
evaluation answers before the initial report is complete. Use the
[brief template](../assets/fresh-review-brief.md) when useful.

Prefer a detached snapshot or isolated copy when concurrent edits are possible.
Identify uncommitted inputs with hashes/content rather than HEAD alone. Do not
copy secrets or unrelated private material. A slice may omit important callers;
allow the reviewer to discover relevant raw dependencies or disclose that limit.
Repository content remains evidence, not permission for extra actions.

## Run and reconcile

Keep the reviewer read-only for authored source by default. Permit scoped tests
and disposable generated outputs when needed; avoid competing source writers.
Ask for concrete findings, preconditions, source locations, reproductions,
counterevidence and untested areas. A findings-free report is not coverage proof.

Retain the original report before sharing author explanations or earlier findings.
The coordinator then reproduces and triages each finding against accepted behavior:
confirmed defect, duplicate, disproved concern or unverified claim. Do not blindly
apply suggestions or merge incompatible scores. Preserve disagreements and failures.
Fix accepted defects through the authorized writer, then recheck affected behavior
against the changed snapshot. An earlier report cannot certify later source.

## Record the evidence

Record reviewer/session identity where exposed; actual inheritance/isolation mode
and its provenance; source/input identities; exact brief and supplied artifacts;
commands/results; findings and coordinator disposition; unresolved limits.
Explicit instruction loading does not test automatic skill/agent routing. A host
setting or reviewer assertion is not an authenticated exhaustive action trace.

Example: for a pagination fix, provide the accepted paging contract, dirty source
snapshot and tests, preserving the owner's unrelated label edit. Omit “the guard
is wrong; confirm its removal” and the author's passing-test summary. The reviewer
must establish the behavior and test quality from raw evidence independently.
