# Market-data validation guide

Load only the checks relevant to the instrument, dataset and intended decision.
Examples are synthetic; they establish expected reasoning, not observed outcomes.

## Minimum data contract

Record source/provider, exact file/query/version/hash when available, retrieval
UTC time, intended decision/as-of time, covered interval, instrument and venue,
currency, units, observation frequency, timestamp semantics, publication/availability
fields, revision policy, adjustment method, universe and calendar. Identify what
is unavailable rather than guessing. An HTTP success or plausible schema does not
prove provider completeness, a data license, or historical availability.

For equities, symbols can change or be reused. For futures, distinguish an actual
contract from a synthetic continuous series and document roll construction. For
options, expiry/strike/type/multiplier and exercise conventions matter. For crypto,
identify chain/token contract and venue/pair; a ticker is insufficient. Do not apply
an equity calendar to continuously traded crypto or a weekday calendar to every
exchange. FX translation requires rate direction and a matching observation time.

## Temporal availability

At decision time T, use only inputs available by T under the strategy's actual
latency assumptions. A bar labeled 10:00 may describe the interval ending 10:01;
its close cannot inform a fill at 10:00. Separate event time, complete-bar time,
source publication, revision, ingestion and action. Timezone-aware UTC conversion
must preserve original venue/session semantics, especially daylight-saving changes.

Synthetic case: a filing for a quarter ending June 30 is published August 8 at
20:05Z. An August 8 14:00Z decision cannot use it even though its fiscal period
ended earlier. A restated September observation cannot silently replace the value
known in August. If only the latest snapshot exists, classify historical
availability as unverified; shifting all timestamps by one row does not fix it.

Corporate fundamentals may have multiple fiscal periods, units, filings and
amendments. Match entity, fiscal interval, publication and accounting meaning.
[SEC EDGAR API documentation](https://www.sec.gov/edgar/sec-api-documentation)
describes submissions and XBRL data access; source APIs still require semantic
and point-in-time checks. Reference reviewed 2026-10-14, not a provider SLA.

## Structural and numerical checks

For conventional OHLC bars, verify low <= open/close <= high, declared timestamp
ordering, duplicate instrument/time keys, finite numeric observations and declared
volume conventions. Zero volume can be valid; missing volume is different. Negative
prices need instrument-specific interpretation rather than unconditional deletion.
Missing periods need an applicable calendar and listing/halt status before being
called data loss. Do not forward-fill prices across delistings, closures or unknown
intervals just to make a backtest run.

A plausible file may still have a price scale, currency, contract multiplier or
volume-unit error. Compare selected boundary records, unusually large changes,
corporate-action dates and aggregate totals with the provider contract or another
approved source. Disagreement without equivalent adjustment/venue/time conventions
is a conditional discrepancy, not automatically an erroneous provider.

## Corporate actions, returns and universes

Synthetic split case: an asset closes at 100 before a 2-for-1 split and 50 after it.
A holder of one pre-split share then owns two shares worth 100 in total. The raw
price ratio alone suggests -50%, while the split-adjusted economic price return
is 0%, before costs/dividends. Check exactly which series the provider adjusted;
do not split-adjust again or add dividends twice to a total-return series.

For a long cash holding, a simple return can be (P1 - P0 + cash distribution)/P0
when prices, shares, currency and distribution timing are consistently defined.
That formula is not a universal futures, options, FX or leveraged-account return.
A log return requires a positive ratio; unsupported prices must remain explicit.

Use membership known at each decision date, including failures/delistings and
instrument-specific settlement. A current constituent list creates survivorship
bias in a historical universe. Benchmark and portfolio comparisons must align
calendar, currency, return type, rebalance timestamps and fees.

## Example report decisions

- Confirmed: the same instrument/time key appears twice with conflicting closes.
  Preserve both raw records and identify a source resolution rule before deduping.
- Conditional: one provider differs on a split date; its adjustment convention is
  missing. Do not choose the series with the better strategy return.
- Not checked: no historical constituent or publication archive is available.
  A price-quality pass cannot support a point-in-time backtest claim.
- Suitable with scope: a declared synthetic series passes structural checks for
  testing a parser. It does not establish suitability for investment research.

Use actual provider/tool versions and commands in a real report. Do not install
connectors, upload account data or alter source files without task authority.
