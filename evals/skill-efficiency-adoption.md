# Efficiency in everyday skills

P0 follow-through for agents #36 and #26. The specialised decision/improvement skills are not mandatory wrappers around ordinary work. The five existing entrypoints below now carry task-scoped evidence reuse and compact reporting directly, with unchanged trigger descriptions, six procedural sections and no new always-loaded reference.

## Reviewed source changes

Baseline: `2b7a442c38b882827d236469f18f48ae41b6494a`. Sizes include frontmatter and are UTF-8 source bytes, not provider tokens, host loads or model outcomes.

| Entrypoint | Before bytes | Candidate bytes | Reviewed ceiling |
| --- | ---: | ---: | ---: |
| codebase-audit | 5145 | 4324 | 4500 |
| security-review | 4258 | 4053 | 4200 |
| design-system-compliance | 4190 | 3956 | 4100 |
| implementation-plan | 1957 | 1878 | 1900 |
| documentation | 1891 | 1846 | 1850 |

The sum is 17,441 -> 16,057 bytes (1,384 fewer; about 7.9%). This is an inventory sum across five alternative entrypoints, not a recommendation to load all five for a task. Supporting guides were not changed or removed to obtain that difference. Additional retrieval, host instructions, tools, retries and generated output remain outside this measurement.

## Manual acceptance review and future task trials

| Skill | Changed operating behaviour | Boundaries retained |
| --- | --- | --- |
| codebase-audit | Reuse current observations, refresh changed callers/tests, summarise distinct diagnostics and bound specialist handoffs. | Sampling is not global compliance; exact command approval, counterevidence, language capability gaps and rubric-based scores remain explicit. |
| security-review | Refresh touched trust transitions and dependent findings; keep real redacted log references instead of repeated raw output. | Trace attacker-controlled values, early returns and alternate routes; no credential access, live probing, installs or fixes by default. |
| design-system-compliance | Follow token/component dependencies after a diff and keep a compact rule/evidence map. | Exact accepted authority, exceptions, platform adapters and static-versus-runtime coverage survive. No inferred identity approval. |
| implementation-plan | Minimal source references per task; continuation updates existing steps rather than recreating history. | Required checks, dependencies, approval gates, rollback and unresolved decisions remain required. |
| documentation | Refresh only supporting changed evidence, update its canonical owner, and avoid routine report churn. | Qualifiers, exceptions, contradictory evidence and ADR history survive; unexecuted checks and planned features never become delivered claims. |

Future recorded trials must exercise a rare failure in a noisy log, a changed service under the same HEAD, a global token affecting multiple screens, a resumed partial plan, and stale documentation claiming an unmerged feature is delivered. These are review expectations, not completed model trials. No default extra agents or hosted Jev calls are introduced.

## Authoring regression checks

`skill-entrypoint-budgets.json` retains baseline commit/blob/byte identities, explicit ceilings and unchanged trigger digests. `test_skill_entrypoints.py` checks the five selected files, prevents silent enrollment/trigger changes and rejects growth, malformed budgets, duplicate keys and missing procedure sections. It runs through existing `validate_agents.py`; no workflow or runtime change is required.

These checks cannot prove semantic equivalence or agent adherence. Baseline identities are retained review data, not fetched or independently authenticated by the test. Meaningful future corrections may require an explicit budget/trigger review; shorter text is never an excuse to delete required evidence or safety controls. Existing bundle and routing validators remain in force.
