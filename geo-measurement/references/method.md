# Metric rules and example

An observation is one retained answer for one panel prompt/provider/settings/time.
Keep a planned observation ledger including failures and exclusions. Use exact
entity aliases and predeclare whether duplicates in 1 answer count once (the
usual answer-level rate) or as occurrences. Never mix those units.

Example: 6 planned unbranded observations, 4 usable responses, 1 provider error,
1 refusal. Of the 4 usable responses, 2 mention Acme and 1 cites an Acme-owned URL.
Report coverage 4/6, mention rate among usable answers 2/4 = 50%, and owned-domain
citation rate among usable answers 1/4 = 25%. Also report 2 missing responses and
why they are excluded. These are conditional sample rates; counting failures as
nonmentions would instead give 2/6, a different predeclared metric.

If one citation links an Acme page without supporting the associated assertion,
it remains an observed URL citation but fails claim-support verification. Keep
owned-domain citation, any supporting citation about the entity and mention rates
separate. Do not label 50% “market share” or infer a change caused by an edit.

Matched repeats: compare the same provider/prompt/settings cells, report unmatched
cells separately and retain all raw observations. Do not pool branded and unbranded
panels or different model versions without a clear breakdown.

Current [Google AI features guidance](https://developers.google.com/search/docs/appearance/ai-features)
describes its own eligibility and reporting. It is not a cross-provider measurement
standard or proof of observed inclusion.
