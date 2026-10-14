# Forecast evaluation methods

## Dataset and timing

Record event/question ID, exact outcome definition, forecast probability and
issue/cutoff time, information horizon, outcome source/resolution status/time,
scoring as-of, weights and exclusions. A later revision must not masquerade as an
earlier forecast. Repeated updates to one event are dependent observations; define
per-question snapshots, time weighting or another justified evaluation unit.

For binary events, p must be in [0,1] and resolved y in {0,1}. For categorical
mutually exclusive/exhaustive events, verify class definitions and Σp=1; independent
multi-label events need a different contract. Unresolved/cancelled records are not
y=0. A resolved-only sample can be selected/censored; retain excluded counts and
assess whether it represents the requested population.

## Proper scores and example

Binary mean Brier = mean((p-y)^2), lower is better. Natural-log loss =
-mean(y ln p + (1-y) ln(1-p)), interpreted by the realized label to avoid 0×ln(0)
undefined arithmetic. A zero probability for an observed outcome has infinite log
loss. Report that mathematical result; if a separate operational metric clips
probabilities, disclose epsilon and both definitions rather than silently improving
an overconfident model. Multiclass Brier conventions may sum or rescale class
errors, so do not compare differently defined scores.

Synthetic data p=[.8,.6,.2,.4], y=[1,0,0,1] has squared errors [.04,.36,.04,.36],
mean Brier .20. A predeclared constant .5 baseline has .25, giving Brier skill
1-.20/.25=.20 under that baseline. This tiny improvement is not evidence of
calibration, significance, profitability or future performance.

[Metaculus scoring documentation](https://www.metaculus.com/help/scores-faq/)
illustrates proper scoring and platform-specific conventions; it does not make
this generic Brier formula the platform's actual tournament score. Reference
reviewed 2026-10-14. Match the actual task/platform score and weighting when needed.

## Calibration and uncertainty

For the synthetic data, 2 bins [0,.5) and [.5,1] have means .3 and .7, while each
has observed event rate .5 and n=2. State bin edges/counts and wide sample
uncertainty. Low Brier does not by itself prove reliability; calibration error
estimates depend on bins and sampling. A constant base-rate predictor can be
calibrated yet uninformative. Sharpness/discrimination and calibration differ.

Use justified confidence/resampling methods that respect event/time dependence,
not an automatic independent-observation assumption. Small/selected samples may
permit descriptive results only. Predicted 80% events need not occur exactly 80%
of the time in a handful of cases.

## Fitting and claims

A calibration transform fitted on scored labels cannot be certified on those same
labels. Keep training, transform/method selection and final evaluation separate;
use temporal/rolling designs when relevant. Preserve all tried methods and reused
test periods. Compare a baseline under the same sample, horizon and weighting.
Probabilities, decision utility, transaction costs and settlement contracts are
different quantities; improved scores do not establish a positive betting return.
