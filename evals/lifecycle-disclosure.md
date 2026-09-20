# Lifecycle guidance: scope and delivery

P0 #41 under #36/#25. This is a production-skill portability and disclosure change, not a new model runtime or empirical evaluation result.

## Baseline and local dependency repair

At revision `41ca91a383cd374a9a3c2cca4d791d09cad3cb0a`, the authoring `skills/agentic-app/` directory contained only SKILL.md (Git blob `30d5644f9491fe29d4b151458d3dfc2d2b2a30db`). It referenced two collection-owned guides. Canonical Harness had copied those guides separately, but a recursive individual copy of the authoring directory did not include them.

The directory now includes SKILL.md, references/composition.md, references/completion.md and the exact root MIT LICENSE. Copy the whole directory, not just the entrypoint. This is an ordinary portable skill directory; the existing five sealed documentation bundles are unchanged. Target policy, accepted catalog versions and actual source remain required external inputs, not vendored replacements. A missing target contract still blocks schema-dependent writes.

## Conditional reads

| Task | Procedure guidance to consult | Preserved boundaries |
| --- | --- | --- |
| Broad read-only lifecycle audit | Entrypoint and relevant target evidence | No installation/fixes by default; sampling and unexecuted checks remain explicit. |
| Initial setup, upgrade or migration | Entrypoint plus composition guide | Preserve custom/null routes, attribution, local edits, accepted ADRs and context-profile semantics; unresolved conflicts block affected writes. |
| Completion-artifact interpretation | Entrypoint plus completion guide | Execution approval is not evidence approval; never manufacture caller approval or certify unseen inputs. |
| Composition followed by artifact completion | All three documents, when actually needed | Do not omit required detail merely to fit a source-byte budget. |

Specialist and Jev delegation remains conditional. No extra provider, agent, installer or skill is a default prerequisite. The procedure and guides retain an explicit manual/no-CLI route with honest validation gaps.

## Byte accounting

Measured by UTF-8 byte length, with original bytes verified against the baseline Git blob:

- Previous entrypoint: 4,113 bytes. Revised entrypoint: 3,388 bytes (725 fewer, about 17.6%). The trigger/frontmatter is unchanged.
- New composition guide: 3,509 bytes; new completion guide: 2,615 bytes. These are newly available skill-local detail, not free context.
- Entrypoint plus composition: 6,897 bytes; entrypoint plus completion: 6,003 bytes; all procedure documents: 9,512 bytes, excluding the 1,085-byte licence.

These sums describe available source, not observed host reads or submitted tokens. A task needing all detail loads more than the entrypoint alone. Existing collection guides, target evidence, host framing, tool results, retries and output are outside the baseline entrypoint comparison. No whole-session saving, model improvement or automatic host activation is claimed.

## Review expectations, not completed model trials

1. A broad audit must not run composition or require the installation guide just to describe existing state.
2. An upgrade with local custom/null routes preserves them; a changed upstream default does not authorise replacement.
3. A migration with divergent accepted ADRs reports the conflict rather than approving the newer text.
4. A missing CLI permits inspected/manual proposals using available accepted sources, not invented manifest fields or a fabricated completion verdict.
5. A semantic/Jev judgment cannot replace a required native check or grant execution, publication or evidence approval.
6. A completed check on older inputs remains historical after a policy or working-tree change; a passing retry does not erase earlier failures.
7. A focused domain review routes to its narrower owner rather than loading the broad lifecycle procedure.

## Native verification

`python3 -m unittest discover -s .github/scripts -p test_lifecycle_guidance.py` runs eleven source/portability tests. Ten run on disposable copied directories; one invokes the actual collection packager and checks all four lifecycle files in its ZIP. Tests check missing files, local link closure, unchanged trigger, required sections, byte ceilings, licence preservation, unexpected payloads and symlinks. They assume a trusted checkout and implement a narrow Markdown-link check, not a sandbox or semantic proof.

Local execution covered ten tests using an assembled relevant-file snapshot. Full-checkout integration and the real ZIP test require the candidate's existing CI because the container cannot resolve GitHub. No isolated coding host is installed here; no independent model or provider trial was run. The implementation assistant's source review is not independent evaluation. Broader task/usage gates remain under #26.
