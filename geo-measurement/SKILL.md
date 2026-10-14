---
name: geo-measurement
description: "Measure observed brand mentions, citations and factual representation in AI answers using a reproducible prompt panel and retained responses. Use for GEO baselines or repeat measurements; do not infer visibility from crawler eligibility or promise placement."
---
# GEO measurement

Define the brand/entity, audience, locale, query intent, comparison set, providers,
measurement window and authorized data access. Assess provided answers when live
access is unavailable. Do not send private material to external providers merely
to test visibility. Keep this answer-observation workflow separate from a technical
crawl/index audit or a general marketing rewrite.

Build a prompt panel reflecting actual audience tasks, with stable prompt IDs and
predeclared sampling/repetition. Separate branded prompts from unbranded discovery;
report their results separately. Record exact prompt, date/time, provider/model
identity where exposed, locale, search/browsing mode and relevant settings. Do not
hide failed, refused, empty or unavailable observations by silently reducing the
planned sample. Explain retries and exclusions.

Retain authorized raw responses and cited URLs, with hashes/identifiers and privacy
limits. Code mentions using a stated entity/alias rule; distinguish brand text from
an actual recommendation. Code answer citations separately from mentions, and
verify a cited source's support before calling it supporting evidence. Negative
representation and factual errors need quoted evidence and an approved fact source.

Use [the metric rules and worked example](references/method.md) and
[the observation/report template](assets/report-template.md). Define each numerator,
denominator and missing-response policy before calculating. Report small samples
as observations. Repetition from 1 provider is correlated and is not a market-wide
visibility estimate. A before/after observation alone cannot establish causality.

For repeat measurement, hold the panel/settings stable or report cohort changes.
Compare matched provider/prompt cells and dates. Separate observed differences,
source-content hypotheses and proposed fixes. Check current provider documentation
for access requirements; no special file or schema guarantees citation.

Complete with scope, raw evidence identities, transparent metrics, verified factual
representation gaps, uncertainty and a repeat plan. Missing access produces a
measurement plan or supplied-evidence review, not fabricated live results.
