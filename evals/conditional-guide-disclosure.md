# Conditional reference disclosure — 2026-09-20

Scope: existing P0 #36 and #32. This changes production reference loading, not the
model runner, provider integration or everyday SKILL.md entrypoints.

The efficiency parent keeps evidence sufficiency, source scope, manual diagnostic
review, required checks, handoff and measurement rules. Rule IR API details move
to `references/rule-review.md`; compactor invocation/format details move to
`references/log-compaction.md`, with its manual fallback included locally.
The decision parent keeps current-agent versus Jev distinctions, required vendor
review, evidence/permission boundaries and failure handling. Existing-receipt
validation moves to `references/recorded-results.md` and is routed before review
or proposed reuse. Do not skip a deferred guide when its operation is in scope.

All 37 original prose blocks are retained byte-for-byte across each parent and its
deferred guides. `conditional-guide-baselines.json` records hashes from the two
parent files at upstream revision `5e35bc52c338baf4a6b6fa2ce25a814ebc574ce3`.
Tests compare those exact blocks; this is text preservation, not a proof that a
model reads or correctly applies them. New headings and routing text are additional.

| UTF-8 source scope | Previous parent | New parent | Parent plus all deferred guides |
| --- | ---: | ---: | ---: |
| Efficiency guide | 8,536 | 5,416 | 10,416 |
| Decision guide | 6,873 | 4,919 | 7,596 |

The reduced parent reads save 3,120 and 1,954 source bytes respectively. Reading
all guides is more expensive; the extra routing and self-contained fallback text
must count. These are file-size measurements, not observed tokens, complete
session cost or measured quality improvement. Tasks that never read the original
parents have no source-loading reduction from this change. SKILL.md files, trigger
text, helper code, optional-tool permissions and existing package format stay intact.

The unchanged packager retains all deferred guides in standalone and collection
archives. Existing full/progressive trial preparation exposes the same available
files to both treatments; full mode includes their bodies and progressive mode
only the original filename routes until read. Neither mode executes a helper or
provider. No actual model session or TypeSafe inference is claimed here.

Run `python3 .github/scripts/test_conditional_guides.py` and normal repository
validation. Content tests run without other repository modules; distribution tests
use the actual packager and preparer. The local checkout could not be cloned due
to GitHub DNS, so local checks cover selected hash-verified files and full integration
is a separate CI requirement. Broader #26/#32/#36 evidence gates remain open.
