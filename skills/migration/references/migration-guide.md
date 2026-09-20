# Migration decisions and preservation

Load this guide for apply, conflict resolution or recovery, not ordinary task routing.
The target's accepted contract and applicable instructions remain authoritative.
This is a manual procedure, not a filesystem migration engine or permission grant.

## Read-only review without a CLI

Use available native file reads, exact-byte comparison, Git status/diff and existing
project checks. Record the actual tools used; discovered configuration is not an
executed check. Do not install a CLI or improvise an unsupported migration command.
An available tool may be used only after checking its actual version, documented
syntax and target permission. An unavailable tool does not prevent source review,
but unavailable required validation prevents a verified-complete claim.

The reviewed canonical guide explicitly distinguishes filesystem migration from
`ah agentic migrate` model-profile comparison. Never substitute `upgrade` or assume
that a command named migrate moves project files. Canonical source basis:
[Migration to the .agentic layout](https://github.com/powerpuff-kitty/agentic-harness/blob/67a62e187c5f4be513e42a9ac135023b7bfde113/.agentic/docs/project/migration-v1.md),
reviewed 2026-09-20. This pinned reference is provenance, not a required remote read;
use the accepted target version, and report a conflict or missing contract instead
of treating this historical snapshot as current authority for every project.

## Discover before mapping

Inventory only the migration's affected sources, destinations and referring files.
Include dirty, untracked and ignored project context through permitted discovery;
a commit is not a backup of those files. Do not enumerate secrets or follow links
outside the authorized target. Linked, nonregular or unreadable entries require
review before any write. Preserve their status rather than guessing contents.

A reviewed root product document may map to `.agentic/PRODUCT.md`; that example is
not automatic ownership detection. Root `SECURITY.md` may be public vulnerability
reporting policy and must not be mistaken for an internal security model. Likewise,
`skills/` and `evals/` can be distributable product content, not misplaced project
context. Never sweep directories into `.agentic/` based on their names alone.

Keep root/nested instruction applicability separate. Moving an `AGENTS.md` into a
parent directory can broaden authority even when its bytes match. Record affected
scope and link resolution, not just destination paths. Preserve public repository
files, source code and local custom instructions unless explicitly included.

## Preview and approval

Use an existing approved task record or an in-session table containing source,
destination, exact-byte identities, current existence/type, proposed action and
reason, affected references, conflict status, backup and required checks. Do not
invent a new wire format; use a compatible canonical report only when requested
and available. A review record is not itself approval to execute it.

Identical bytes mean a duplicate is present, not permission to delete either copy.
Divergent accepted sources block apply until the owner resolves their authority.
Do not choose the newest file, longest text, catalog default or model preference.
A new destination is still a write requiring the project's approval. Bind approval
to the exact source/destination/policy state and permitted actions. Re-read that
state immediately before changes. Any unexpected drift requires a fresh review.

A disjoint subset may proceed only with separate explicit scope approval; retain
all unresolved conflicts and do not label the full migration complete. Review
links/dependencies before considering a subset independent.

## Backup, application and recovery

Create the approved backup outside the working target, preserving affected local
work, original routes and metadata needed for restore. Verify contents against the
reviewed inventory, including untracked files, and test restoration in a disposable
location when permitted. Backup creation alone is not demonstrated restorability.
Do not publish backup contents or credentials. If preservation cannot be verified,
stop before destructive changes.

Use reviewed native operations in a quiescent workspace. Write and verify an
approved destination first. Removing/archiving its old source is a separate action
within the approved plan and needs the verified backup. A successful copy does not
prove new router links, instruction scope or target-schema validity.

An I/O or check failure stops further writes. Record what actually changed and
recheck both target and backup before proposing recovery. Do not blindly overwrite
new local edits with a snapshot or delete partial output. Obtain approval for a
specific restore/reconciliation; backup files are evidence, not executable commands.

Convert manifest fields against the accepted schema instead of renaming YAML.
Preserve real lock/provenance identities; do not copy another project's lock or
manufacture a source revision. Keep thin vendor pointers thin and change only
references implicated by the migration. Never drop unresolved required checks.

## Worked decisions

| Evidence | Decision |
| --- | --- |
| Root PRODUCT.md differs from an accepted .agentic/PRODUCT.md. | Block that apply; retain both exact versions for owner review. |
| The source changes after preview, although the filename is unchanged. | Invalidate the approval; replan rather than applying old findings. |
| Identical source/destination bytes, no removal approval. | Report duplicate/no write; leave both files intact. |
| Destination was copied but verification failed. | Keep source and backup, stop writes and report partial state. |
| The approved copy is complete and a repeat plan has no actions. | Report a no-op for that scope only; an unrelated unresolved conflict still blocks whole-project completion. |
| Files and schema checks pass, but host loading was not observed. | Report the performed checks and unverified host delivery separately. |

## Completion evidence

Inspect source/destination identities, restored-backup evidence when performed,
route/manifest changes, the complete diff and each required check's actual result.
A second **read-only** plan checks idempotence without repeating mutations. It may
still contain duplicate/conflict entries; no additional actions in the approved
scope does not make those unresolved entries disappear. Do not claim that a
reviewed declaration proves model behavior, scope enforcement or token savings.
