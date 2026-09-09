# Agent behavior evals

Evals validate procedure routing and behavior rather than only file presence.

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
