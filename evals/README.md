# Agent behavior evals

These files define procedure-routing and behavior acceptance criteria. Deterministic validation checks fixtures, supplied records and packaging; it does not establish that a model follows the procedures.

- `routing.json` gives at least one positive routing case for every registered skill and explicit nearby skills that must not be selected.
- `design-intelligence.json` contains synthetic, network-free safety/handoff scenarios for Design Intelligence: candidate approval, evidence-vs-inference, `not_checked`, unavailable tooling, untrusted providers, cross-framework component compatibility, dataset rights, feature slop, drift-vs-violation, accessibility evidence, and public-export privacy.
- `skill-quality.md` defines cross-skill behavior expectations for context discipline, evidence, approvals, output, and completion.
- `layout-v1.md` continues to cover the Agentic Harness filesystem contract.

Local deterministic validation:

```bash
python3 .github/scripts/validate_agents.py
python3 .github/scripts/validate_design_intelligence.py
```

The Design Intelligence scenario file is a **behavior contract fixture**, not a recorded model run. It must not be cited as evidence that any model passes the scenarios. Fixtures are synthetic and do not copy restricted provider screens or datasets.

## Existing context-efficiency workflow

Use [matched-treatment preparation](prepared-guidance-trials.md), then
[checked participant staging](staged-guidance-trials.md). Expose only the selected
participant directory to each separately authorized fresh session. Review actual
outcomes using [paired](paired-guidance.md) or [repeated-trial reporting](repeated-guidance-trials.md).
The [Codex usage inspector](codex-usage-import.md) supplies supporting trace evidence,
not a complete per-call ledger. Preparation and staging do not execute models,
reserve independent sessions or establish token savings.

## Skills-first completion gates

The next acceptance step is evidence from representative sessions, not another
preparer or reporting layer. Reuse the existing tools unless a concrete failed
workflow demonstrates a missing capability. Keep these gates separate:

| Gate | Required evidence | Owner |
| --- | --- | --- |
| Task outcomes | Fresh matched sessions, retained failures, rule adherence and independently reviewed outcomes; public fixtures are not unseen benchmarks. | [#26](https://github.com/powerpuff-kitty/agentic-harness-agents/issues/26) |
| Host delivery | Exact host version, actual loaded instruction sources, nested/scoped routing and preservation checks; copied files are not proof of activation or isolation. | [#24](https://github.com/powerpuff-kitty/agentic-harness-agents/issues/24), [#36](https://github.com/powerpuff-kitty/agentic-harness-agents/issues/36) |
| Task-scoped accounting | Complete observed input/output usage, retries, auxiliary work and instruction loading; unknown usage stays unknown and cumulative snapshots are not summed. | [#26](https://github.com/powerpuff-kitty/agentic-harness-agents/issues/26), [#36](https://github.com/powerpuff-kitty/agentic-harness-agents/issues/36) |

[Decision guidance #32](https://github.com/powerpuff-kitty/agentic-harness-agents/issues/32)
remains distinct from live Jev inference. The current-agent path can be evaluated
without a TypeSafe provider, but cannot be relabeled as a Jev result. Hosted
inference and downstream runtime work remain separate, explicitly authorized work.
Do not make either a prerequisite for evaluating the installed guidance.

Full versus progressive inputs compare disclosure of the same skill, not Harness
versus no Harness. A claim about the latter requires its own matched control.
Close a delivered content/contract ticket once its own acceptance is evidenced;
keep unresolved empirical gates open under their existing owners. Epic counts,
merged PR counts and synthetic test counts are not a production-readiness score.
