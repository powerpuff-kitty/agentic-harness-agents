# Staging one planned skill trial

P0 #74 under #26 supports #36 and #32. This optional evaluation tool copies the
chosen participant template from an already prepared series into a new workspace.
It does not start a host, run a helper, install skills globally or collect usage.

## Prepare, pin, then stage

Prepare the matched series as described in [prepared trials](prepared-guidance-trials.md).
Successful `prepare_guidance_series.py` output now includes `reviewer_sha256`, the
SHA-256 of the exact bytes written to `REVIEWER.json`. Retain this digest separately
with the successful preparation result before staging. This is additive output:
the existing participant files, preparation marker, plan and empty roster are unchanged.
For older preparations, independently review their original marker and artifacts
before establishing a pin; never refresh a pin merely to accept unexpected edits.

```sh
python3 .github/scripts/stage_guidance_trial.py \
  --series /reviewed/guidance-series \
  --expected-reviewer-sha256 "$REVIEWED_PREPARATION_SHA256" \
  --pair-id r1 \
  --role candidate \
  --output /new/location/r1-candidate
```

`--role baseline` selects full disclosure; `--role candidate` selects progressive
disclosure. The repetition ID must already be in the original plan. The output's
parent must exist, and the output itself must not exist. Each separately authorized
session needs a new workspace; the tool does not schedule or run those sessions.

```text
r1-candidate/
  participant/             only the selected original participant files
    TASK.md
    TASK-INPUT.json
    guidance/              original skill payload, license and optional helpers
  STAGING.json             reviewer-side file identities and planned slot
```

Supply **only `participant/`** to the session. Do not expose the prepared experiment
or the staging parent: reviewer metadata and expected answers belong outside the
participant's access. The participant's original prompt already prohibits helper
execution and provider calls in these read-only trials; copying a script grants
no permission to run it. File separation is not an OS sandbox. Configure actual
host permissions independently and record extra instructions or automatic loads.

## What is checked

The tool verifies the marker against the caller-retained byte digest, checks the
plan file against the marker's inventory, and compares the plan's canonical JSON
fingerprint with the recorded plan identity. It selects the fixed treatment path
rather than following an arbitrary directory supplied in metadata.

Every selected file must match its pinned size and SHA-256. The exact subtree must
contain the expected files and directories: missing files, added instructions,
symlinks, case-colliding paths, path traversal and nonregular entries fail before
output creation. TASK.md must also match its planned treatment digest. All selected
bytes are validated before copying, including optional scripts as inert bytes.
The destination files are read back for exact byte agreement before the receipt
is written. No participant text is edited or summarised, and no reviewer record,
expected answer, environment label or repetition ID is injected into its prompt.

Read/verification scope is the pinned marker, plan and **selected template only**.
Other treatments, later working results and reviewer answer files are not read or
certified. The original preparer owns full plan validation; this tool does not
rerun semantic graders or authenticate environment declarations. Keep the original
preparation immutable and store observed trial records in a separate working copy.

## Writes, bounds and failures

Exit 0 means checked staging finished, not that a trial ran. Exit 2 reports a fixed
error without rejected paths or source bodies. Validation errors create no output.
An I/O failure after creation can leave partial NEW files; the tool neither cleans
up nor repairs them. Existing output is always refused. STAGING.json is written
last and its hash is returned, but marker presence alone cannot certify later
unchanged bytes. Refresh identities before host use after intervening edits.

Directories use mode 0700 and files 0600 where supported. Sources and destination
parents must be trusted and quiescent: observed-link and file-identity checks do
not contain hostile concurrent filesystem replacement. A new directory outside
the source experiment and checkout is required. It is not necessarily outside
other instructions discovered by a host; host isolation/loading remain unverified.

Bounds: 256 inventory entries, 512 selected filesystem entries, 256 KiB marker and
receipt, 4 MiB per selected file and 4 MiB total participant bytes. Unknown or
unsupported preparation/plan versions and malformed metadata fail explicitly.
No dependency installation, network access, subprocess or credential lookup occurs.
Staging the same planned slot twice is not prohibited globally; the receipts
identify that slot, not independent executions or a reservation service.

## Evaluation boundary

Staging leaves `review/pairs.json` untouched. The existing series evaluator still
reports every unobserved baseline/candidate as missing and token totals unknown.
The receipt and success output record zero observed sessions. Source authentication,
whole-experiment validation, host loading/isolation, outcomes and savings remain
unverified. A caller who changes the source and its external pin can fabricate
agreement; hashes do not establish trusted authorship or preregistration.

Run `python3 .github/scripts/test_guidance_trial_staging.py` for synthetic filesystem
regressions and actual prepare-stage-evaluate integration. They do not invoke a
model, prove secret holdout isolation or measure end-to-end token savings.
