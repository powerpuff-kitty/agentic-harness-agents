# Design conformance: decision guide

The target project supplies the design authority. This guide specifies how to review evidence; it does not define the project's colors, spacing, components or architecture.

## Routing examples

Use: "Check these components against our approved tokens and variants"; "Review whether this change violates our accepted design-system rules." Do not use for "Invent a new visual identity" (identity-design), "Build a new component library" (design-system), or "Perform a full screen-reader audit" (accessibility-audit). These are author-defined routing expectations, not measured model decisions; route only when that separate scope is actually requested.

## Establish authority first

Record the accepted file/artifact/version and the target's approval designation. Follow custom manifest paths. If DESIGN.md, an accepted decision and a Genome disagree, present the disagreement and stop issuing conformance scores. A candidate Genome, a screenshot reference, frequently used values and a recent analysis are observations until the project approves them.

## Rule-to-evidence decisions

| Candidate | Evidence needed for a violation | Countercheck |
|---|---|---|
| Token bypass | Applicable accepted token rule and the exact unsupported value/use | Literal values may be valid inside token definitions, assets, fixtures or a scoped exception. |
| Raw control | Approved requirement to use a particular primitive, plus the actual product path and missing required behavior | Native controls, platform adapters and one-off semantics may be intentional. A tag name alone is insufficient. |
| Duplicate primitive | Two owners implementing the same approved responsibility with consequential divergence | Similar styling or names do not prove a shared abstraction is appropriate. |
| Invalid variant | Component contract and a supplied variant outside that contract | Check generated types, dynamic resolution and compatibility shims before treating a string as a runtime value. |
| Missing interaction state | Accepted state/behavior requirement and source or executed evidence showing it is absent | Static grep cannot prove focus trapping, keyboard order or responsive behavior. |
| Expired or out-of-scope exception | Exception identity, approved scope/expiry and the use outside those limits | Honor valid exceptions; do not quietly widen or renew one during review. |

Example: an approved rule requires semantic surface tokens in product components. A component introduces a literal color. Trace whether the file is a token definition, generated asset or product component; inspect any exception. Only the last unexcepted case is a policy violation. A changed color frequency in an analysis report is merely drift unless tied to that rule.

## Coverage and remediation

Record which screens, paths, themes, states and viewports were actually inspected. Separate structural checks, browser tests, visual comparison and accessibility verification. A static CLI analysis is useful evidence but not a screenshot or a browser session.

Use existing approved primitives when their contract fits. A missing capability is a proposed system change, not permission to invent a new primitive or auto-approve an external component. Explore/revise scope can legitimately diverge; state the experiment and approval still needed before canonical changes.

A report from a different revision, changed token source or different scope cannot certify the present implementation. Record the exact mismatch and redo the relevant inspection when possible. No suitable browser/tool available means that layer remains not checked.

## Acceptance scenarios for later host evaluations

These are fixture expectations, not measured host/model results.

| Input | Expected decision | Forbidden conclusion |
|---|---|---|
| Approved token use in the sampled component | No structural violation found in that sample | Entire visual system verified |
| Literal color forbidden by an applicable approved rule | Rule-linked violation with file/range and repair | Any literal anywhere is a violation |
| New value appears only in a diff; no prohibiting rule | Observed drift or a question for approval | Automatically score a compliance failure |
| Valid scoped exception covers the occurrence | Record exception and reviewed scope | Ignore, broaden or revoke exception silently |
| Genome is candidate or conflicts with accepted design document | Authority conflict; conformance score unknown | Treat candidate as newest truth |
| Static markup looks correct; browser unavailable | Runtime interaction and visual results not checked | Keyboard, responsiveness or accessibility passed |
| Approved rules changed after prior report | Prior conformance evidence is stale | Reuse old pass against new authority |
