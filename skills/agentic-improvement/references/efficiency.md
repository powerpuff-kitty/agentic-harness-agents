# Evidence-preserving efficiency

## Working set

Start with task, scope, applicable rules, source locations and acceptance checks. Discover paths before fetching large bodies. Read the owning implementation/interface/test first, then expand to a caller, dependency, configuration or decision record when it can change the answer. Do not assume a lexical match is sufficient. Broad repository audits may legitimately need broad coverage; efficiency must not conceal that scope.

Keep the smallest useful source spans and their exact references. A short extract must retain necessary surrounding conditions. A path or hash does not magically supply content to a model; expand it when the host cannot retrieve it. Mark stale summaries and refresh after changed source, configuration, dependencies or task scope. A commit hash alone does not describe uncommitted edits.

## Instructions

Keep mandatory rules identifiable. Collapse exact duplicates with all sources retained; do not merge near-duplicates that differ in scope, exception or authority. Prefer narrow triggers and one specialised owner over additional overlapping skills. Put substantial examples behind conditional skill-local links. JSON/YAML is useful for validation but is not automatically smaller than prose.

## Checks and logs

Run a native formatter, linter, compiler or test where that is the authoritative mechanism. A semantic answer cannot substitute for an unexecuted check. Use command/scope, exit status, relevant failure IDs/locations and new versus repeated diagnostics in the working context. Retain a real log reference; never fabricate an artifact URI. Preserve omissions/truncation and all required failure evidence.

## Handoff

For a resumed nontrivial task, keep goal; accepted decisions; current source/revision references; changed files; checks actually run and their outcome; unresolved blockers; next evidence needed. Reuse the existing task record. Do not create permanent notes for every trivial operation or replay the whole conversation. Do not persist private data or summaries without the project's permission. A handoff cannot approve an action or override current source.

## Budget and evaluation

Reduce optional examples/background first. When required evidence alone exceeds the working budget, report the conflict and narrow the task or obtain more context; do not silently drop requirements or claim completion. Extra model calls, reranking, summarisation and retries can erase a saving.

Compare the same starting task/source/rules and acceptance checks. Record context supplied, model output and extra provider calls when observable. Account for tool-result tokens once if already included in model input. Separate estimated source size from observed submitted tokens and cached-input pricing. Unknown usage stays unknown. Lower tokens with failed checks or omitted evidence is not a successful optimisation.

Example: a failing test log has thousands of repeated lines. Keep each distinct failure and its source location in the working set, with an accessible full-log reference and truncation state. Do not replace it with 'tests passed' or a count that hides failures. Example: a changed service invalidates the previous service summary even when the repository's HEAD is unchanged.
