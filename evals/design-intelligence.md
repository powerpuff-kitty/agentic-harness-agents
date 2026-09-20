# Design skill acceptance and regression checks

Tracks agent issues #12–#19. The initial 30-skill suite landed in PR #20, with baseline safety work in PR #21.
These tests harden its evidence, approval, routing and capability boundaries.

## Local validation

```bash
python3 .github/scripts/validate_agents.py
python3 .github/scripts/validate_design_skills.py
python3 .github/scripts/test_design_skills.py
```

The first command validates the entire installed collection and existing routing
inventory. The second checks the two procedures changed in this follow-up,
manifest/plugin parity, 17 acceptance scenarios covering all ten design/lifecycle
roles, skill-local references and the synthetic enrichment handoff. The third
runs unit tests including intentionally corrupted fixtures.

These are complementary checks: the focused checker does not replace full
collection validation. No GitHub Actions, model credentials or network are
required by these scripts. Run full collection checks from a complete checkout.

## What these tests do not prove

`evals/design-skill-regressions.json` is an acceptance scenario catalog, not a model
result log. Its prompts and expected/forbidden behavior can be used in later
manual or model evaluations. Validating fixture integrity does not test routing
by a real model and does not measure design originality, accessibility, visual
quality, app/CLI equivalence or live provider connectivity.

The fixture evaluator checks append-only AI enrichment invariants, not the
complete JSON Schema or a production importer. Validate real artifacts against
the project's pinned canonical schema separately. Do not distribute a duplicate
schema here. All fixture data is synthetic; no commercial screenshots/datasets
or actual human approvals are included.

## Evaluation records

For actual model evaluation, record the skill/source revision, model and settings,
input fixture hashes, exact output and a separate judgment of each criterion.
Keep these records distinct from the catalog's `model_evaluations: not_run` marker.
A stale/edited artifact or unrun check must never inherit a passing review.

## Rollout

This follow-up does not silently update installed skills, CLI embedded snapshots,
repository policy, provider connections or release metadata. Installation and
release rollout remain explicit follow-up actions. A skill procedure supports
manual/provider-neutral work even when the corresponding runtime adapter is
still only a backlog item.
