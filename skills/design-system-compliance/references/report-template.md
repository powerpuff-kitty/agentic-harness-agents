# Human conformance report template

This report is not a Design Analysis, Genome or Diff artifact. Do not manufacture measured values or approval metadata to fit a schema.

## Authority and scope

Accepted source/version and approval designation; precedence conflicts; source/dirty-worktree identity; reviewed components/screens/themes/states; design mode; applicable exceptions; omitted areas.

## Rule-evidence map

| ID | Rule / authority | Implementation evidence | Classification | Verification / limits |
|---|---|---|---|---|
| ... | exact approved rule | exact path/range or executed browser result | violation / observed / risk / exception / not_checked | actual method and scope |

Synthetic example: accepted `project-context/design.md:20` requires semantic text tokens for product UI. `src/components/Notice.vue:24` adds an unexcepted literal in a product style. Report the rule and occurrence, propose the existing semantic token, and record that visual/browser verification did not run. These paths are illustrative, not reviewed repository evidence.

Counterexample: a new analysis value appears in a token-definition file and is not prohibited by any accepted rule. Record drift or request the missing approval context; do not label it a violation because it is new.

## Outcome

Separate repairs for confirmed violations from proposals for identity/system evolution. List required approvals and regressions. Unknown runtime, accessibility or visual behavior stays unknown. A compliance score needs an accepted formula and adequate measured coverage; otherwise omit the number and explain the exact gap.
