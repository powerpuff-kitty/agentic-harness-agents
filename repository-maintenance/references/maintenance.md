# Acceptance and cleanup evidence

For an issue, compare the actual acceptance criteria with the current source and
relevant observed checks. Use a requirement/evidence/status table for a complex
case. “Implemented” is weaker than tested delivery; tested delivery is weaker than
a supported release or a measured model outcome. Keep live-host and empirical
claims open when static fixtures are all that exist.

A superseded packaging PR can be obsolete when its sole change targets a workflow
removed by an accepted folder-only layout. A branch with other useful commits is
not disposable just because its original PR closed. A merged PR whose head changed
after merge is also not covered by that merge's evidence.

A branch cleanup candidate needs current repository/default-branch identity and
one of: its exact tip is an ancestor of the accepted base, or a merged PR records
that exact tip (including squash merges). Always preserve active open-PR heads and
protected branches. Revalidate remote tips immediately before deletion and use
conditional deletion where the host supports it. A stale remote-tracking ref or
commit-message similarity is insufficient. Keep the plan reviewable and do not
turn a bulk branch deletion into a history rewrite.

Commit/push/merge/delete are distinct actions. Use existing explicit authorization;
never add another approval gate merely because a checklist says so. When authority
is missing, finish the read-only analysis and prepare the exact mutation first.
Closing a tracker item preserves its history; deleting the issue is not required
for an ordinary obsolete-backlog cleanup.
