# Assisted migration preservation exercise — 2026-09-20

Scope: existing flagship-skill issue #25, using native operations in the current
implementation-assistant session on a disposable synthetic project. This is not
an isolated model trial, independent outcome review, actual user-project migration,
a host-loading test, or a token-efficiency benchmark. The assistant had prior
exposure to the guide and selected the fixture operation scope itself. No real
user's approval was invented or inferred from the fixture.

## Inspected starting evidence

A temporary Git repository contained conflicting root/internal architecture text,
a public SECURITY.md, nested src/AGENTS.md instructions and a custom root router.
After the fixture commit, PRODUCT.md was modified, notes.txt was untracked and
local-context.note was ignored. Actual `git status --porcelain=v1 --ignored` showed
all three states. No secret material was used.

Reviewed bytes were read before selecting any changes. The architecture sources
remained divergent: root draft permitted direct view HTTP; accepted internal
context required services. The read-only plan reported that conflict and wrote
nothing. The exercise did not choose an architecture winner.

The product source was then deliberately amended after preview. Its actual hash
changed, the old preview was rejected, and no product destination existed yet.
After a new review, an external backup and a separate disposable restoration were
created and compared byte-for-byte against all nine affected fixture files,
including dirty, untracked and ignored content.

## Narrow operation and observed result

The synthetic operation scope allowed creating `.agentic/PRODUCT.md` and changing
only the corresponding link in root AGENTS.md. It did not permit deleting a source
or resolving the architecture conflict. The operation checked source/router hashes
and destination absence first, wrote the destination exclusively, verified its
bytes, then updated the single router link. The custom router rule was retained.

Ten local assertions passed: non-writing preview; conflict blocks whole apply;
stale-preview detection before destination write; backup includes local work;
disposable restore equality; only the selected copy/router changes; legacy sources
retained; public security and nested rules preserved; repeat read-only no-op; and
unresolved architecture conflict retained. The second plan did not run apply.

Actual created path: `.agentic/PRODUCT.md`. Actual changed existing path after
fresh review: `AGENTS.md`. All other reviewed bytes remained identical, including
both divergent architecture files. No existing file was deleted. Whole migration
completion remained false because the conflict, target manifest/schema validation
and native host-loading evidence were unresolved.

## Retained identities and limitations

Before the deliberate amendment, PRODUCT.md SHA-256 was
`337897632119a85e2db505b9d02ab8f05a5cd1e699461e84f7ada92e5dd3dbad`.
The preserved architecture source/destination hashes were
`66f335f53b66a08d1b6a62cdf3981e6a98c15f701ca6fd3113eae5d393939f13` and
`8f60421f7b2057f05dd893388c25c75175c29241ba3b9b803b9b4ef4f95c8d2d`.
The local result-record SHA-256 was
`46072cdcfd3c691209de6a2a2b8c02e2c7cbd659792f5468fe1f825ac2cbd820`.
These are supplied evidence identities, not independent authentication. The local
record is not a guidance-trial-record and is not included in repeated-trial totals.

Only the one-off native preservation exercise ran locally. New repository tests
must be reported separately from this exercise and from real model sessions.
A full source clone was unavailable due to container GitHub DNS failure; complete
collection validation therefore belongs to CI. No separate Codex/Claude/local-model
runner was available, and no credentials or hosted Jev calls were used.

The migration entrypoint grows from 1,914 to 2,492 UTF-8 bytes to state its missing
safety boundaries; its trigger is unchanged. The 6,595-byte guide is conditional.
This is a correctness/dependency-delivery improvement, not measured token savings.
Other production skill entrypoints and default routing remain unchanged. P0
#26/#32/#36 retain their independent execution and complete usage gates.
