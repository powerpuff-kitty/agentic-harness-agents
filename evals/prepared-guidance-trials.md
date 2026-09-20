# Prepared full/progressive guidance trials

Preparation for P0 agents #39 under #26/#36, not a model runner or another
required skill. Production skill directories, triggers and source pins are
unchanged. The existing observation grader and paired comparator remain the
owners of their record formats.

## Prepare the same case twice

From a reviewed agents checkout, choose two NEW paths outside the checkout with
existing, non-symlinked parents:

```sh
python3 .github/scripts/prepare_guidance_trial.py --case supported-claim --mode full --output /tmp/guidance-full
python3 .github/scripts/prepare_guidance_trial.py --case supported-claim --mode progressive --output /tmp/guidance-progressive
```

Each produces `participant/TASK.md`, `participant/TASK-INPUT.json`, the complete
validated skill under `participant/guidance/`, and a separate `REVIEWER.json`.
Existing paths are refused. Failure during writing can leave a partial NEW
output directory; absence of REVIEWER.json means preparation did not finish.
Inspect partial output rather than retrying into or automatically removing it.

Full mode supplies SKILL.md and all local reference contents in the initial
prompt. Progressive mode supplies the same SKILL.md plus the guide filenames;
the same reference files remain available for selective reads. Both modes
include EVERY scenario evidence source, not just the grader's required subset.
Task text, evidence, available skill bytes, and offline permissions are identical.
This compares disclosure strategy, NOT Harness versus no Harness.

## Participant/reviewer separation

Supply only the participant directory to a fresh, separately isolated session,
and provide TASK.md as the initial input. Do not supply the checkout, this guide,
REVIEWER.json, the original scenario JSON, walkthroughs or an earlier answer.
Avoid automatic native skill loading on top of manual prompt injection; record
any additional host instructions or loads that actually occur.

An explicit allowlist copies only task text and evidence into the participant
input. Expected route/outcome, case ID and required-source labels stay with the
reviewer. Permission descriptions are generated independently: every prepared
trial is offline review-only. Scenarios simulating authorised provider use are
rejected; fictional consent in test data is not a real permission grant.

This is file separation, not filesystem sandboxing or proof of blinding. The
fixture prompts may describe desired behaviour, and the corpus and guides are
public. Prior model/trainer/author exposure is unknown. A clean session with only
the participant directory is necessary but not sufficient for an independent
experiment; record limitations rather than claiming a secret holdout.

## Identity and measurement

REVIEWER.json binds the actual task projection, all available guidance and every
participant file by SHA-256 and UTF-8 byte count. Absolute output paths and
wall-clock timestamps do not affect packet bytes. Changing only the grading
labels cannot change the participant input. Reference/source changes must change
their snapshots. Hashes establish byte identity, not trusted authorship.

`initial_prompt_bytes` is the exact size of TASK.md, not observed model input or
billing. Progressive reads, repeated input, retries, extra calls, output and host
framing may erase an apparent reduction. Host/model/settings, token observations
and trace are null; execution and savings verification are false at preparation.
No result record or synthetic model response is generated.

After a separately authorised real session, retain the redacted raw answer,
actual tool trace, all required checks and complete observed usage. A reviewer
must derive the existing observation fields from that evidence, not the answer
key. Follow `paired-guidance.md` for matched records and independent review. Do
not convert a preparation record to a passing trial merely by filling flags.

## Native checks and limits

```sh
python3 -m unittest discover -s .github/scripts -p test_guidance_trial.py
python3 .github/scripts/validate_agents.py
```

Tests inspect actual prepared files, change only grading fields, compare the two
treatments, retain contrary sources, and exercise missing guides, mutations,
linked paths, duplicate keys, input/output limits and no-overwrite failures.
The real preparation entrypoint is exercised with an existing scenario; it does
not execute that scenario's model or project commands.

The preparer reuses the bounded documentation-bundle validator and the existing
case validator. It does not fetch URLs, read credentials, launch agents, execute
commands from evidence, replace an installation or change permissions. Only
already-enrolled self-contained documentation skills are supported. A trusted,
quiescent checkout and output parent are assumed; observed-link checks do not
provide isolation from hostile concurrent filesystem changes.
