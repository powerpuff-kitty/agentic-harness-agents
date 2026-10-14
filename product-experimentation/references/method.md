# Experiment validity and readout

Declare the estimand and unit before calculation. User randomization does not make
session rows independent; account/household/market interactions can require cluster
assignment/analysis. Assignment counts and exposure counts are different ledgers.
Define who is eligible for each, when exposure occurs and how missing logs are handled.
Do not condition on a post-treatment event without explaining selection effects.

A fixed-horizon design needs its declared duration/sample policy; repeated peeking
requires an appropriate predeclared sequential method. State planned allocation,
minimum practical effect, baseline assumptions, power/precision, tails and alpha
when used. Multiple variants/metrics/segments need a declared error policy. These
are inputs to appropriate statistics, not universal numeric defaults.

Check SRM on the actual assignment unit and planned ratio with a suitable method.
Investigate logging, eligibility, bucketing, bots, join loss and exposure filters;
a mismatch cannot identify its own cause. Mark interpretation blocked while an
unresolved validity issue can change the answer. Retain the descriptive numbers.
Also check interference, sample/identity duplication, denominator changes, delayed
outcomes, novelty and mature follow-up. A passing SRM check alone does not validate
randomization or the experiment.

An effect is an absolute difference in declared rates/units plus relative change
where its denominator is meaningful. Report uncertainty and practical thresholds;
no significant difference is not equivalence without an appropriate design. Guardrail
harm can block launch despite a favorable primary metric. External validity to
other users/platforms remains a separate claim. Do not invent a p-value, sample
size, participant or deployment observation when a tool/data input is missing.

Primary reference: [Microsoft on diagnosing SRM](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/)
(reviewed 2026-10-14). Use appropriate current primary statistical documentation
for the actual method, rather than treating this procedure as a statistics runtime.
The fixture is synthetic assignment/outcome data, not a completed live experiment.
