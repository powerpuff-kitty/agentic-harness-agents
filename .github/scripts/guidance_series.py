"""Describe a caller-pinned series of supplied trials; do not execute a model.

Reuse guidance-trial-record v1 and its comparator. This is repository evaluation
support, not a provider adapter, credential reader or production skill payload.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import statistics
import sys
from typing import Any

from guidance_comparison import (
    DIGEST, IDENTITY_KEYS, compare, fingerprint, load_record, require, text,
    validate_record, validate_spec,
)
from guidance_eval import submitted_tokens

MAX_BYTES = 1_048_576
MAX_PAIRS = 128
MAX_TOKEN_COUNT = 1_000_000_000_000
ROLES = ('baseline', 'candidate')
PAIR_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}\Z')


def _bounded(value: Any) -> None:
    """Reject non-JSON, cyclic/deep or oversized direct API inputs before grading."""
    stack = [(value, 0)]
    nodes = size = 0
    while stack:
        item, depth = stack.pop()
        nodes += 1
        require(nodes <= 100_000 and depth <= 32, 'series: structure limit')
        if type(item) in (dict, list):
            require(len(item) <= 100_000, 'series: structure limit')
            if type(item) is dict:
                require(all(type(k) is str for k in item), 'series: JSON keys required')
                stack.extend((k, depth + 1) for k in item)
                stack.extend((v, depth + 1) for v in item.values())
            else:
                stack.extend((v, depth + 1) for v in item)
        elif type(item) is str:
            size += len(item.encode('utf-8'))
            require(size <= MAX_BYTES, 'series: size limit')
        else:
            require(type(item) in (int, float, bool, type(None)), 'series: JSON values required')
    raw = json.dumps(value, ensure_ascii=True, separators=(',', ':'), allow_nan=False)
    require(len(raw) <= MAX_BYTES, 'series: size limit')


def validate_plan(plan: Any, expected_plan_sha256: str) -> None:
    _bounded(plan)
    require(type(expected_plan_sha256) is str and bool(DIGEST.fullmatch(expected_plan_sha256)),
            'series: reviewed plan digest required')
    require(fingerprint(plan) == expected_plan_sha256, 'series: plan digest mismatch')
    require(type(plan) is dict and set(plan) == {
        'format_version', 'kind', 'spec', 'evidence_kind', 'identity', 'treatments', 'pair_ids'},
        'series: invalid plan fields')
    require(type(plan['format_version']) is int and plan['format_version'] == 1
            and plan['kind'] == 'guidance-series-plan', 'series: unsupported plan')
    validate_spec(plan['spec'])
    require(plan['evidence_kind'] in ('synthetic', 'recorded-session'), 'series: invalid evidence kind')
    identity = plan['identity']
    require(type(identity) is dict and set(identity) == IDENTITY_KEYS, 'series: incomplete identity')
    require(all(text(v) and (k in ('host', 'model') or bool(DIGEST.fullmatch(v)))
                for k, v in identity.items()), 'series: known plan identity required')
    treatments = plan['treatments']
    require(type(treatments) is dict and set(treatments) == set(ROLES), 'series: invalid treatments')
    for treatment in treatments.values():
        require(type(treatment) is dict and set(treatment) == {'name', 'sha256'}
                and text(treatment['name']) and type(treatment['sha256']) is str
                and bool(DIGEST.fullmatch(treatment['sha256'])), 'series: invalid treatment')
    require(treatments['baseline']['sha256'] != treatments['candidate']['sha256'],
            'series: distinct treatment identities required')
    ids = plan['pair_ids']
    require(type(ids) is list and 1 <= len(ids) <= MAX_PAIRS
            and all(type(i) is str and PAIR_ID.fullmatch(i) for i in ids), 'series: invalid pair ids')
    require(len(ids) == len(set(ids)), 'series: duplicate planned pair id')


def _usage(record: dict) -> int | None:
    usage = record['usage']
    if not usage['complete'] or usage['basis'] != 'observed-submitted-tokens' or usage['evidence'] is None:
        return None
    return submitted_tokens([{k: c[k] for k in ('input_tokens', 'output_tokens')}
                             for c in usage['calls']])


def _assess(plan: dict, role: str, record: dict | None) -> dict:
    if record is None:
        return {'record_digest': None, 'acceptance': 'not-assessed',
                'submitted_tokens': None, 'reasons': ['missing-record'], 'matches_plan': False}
    validate_record(record)
    for call in record['usage']['calls']:
        require(all(call[k] is None or call[k] <= MAX_TOKEN_COUNT
                    for k in ('input_tokens', 'output_tokens')), 'series: token count limit')
    reasons = []
    for key in ('identity', 'evidence_kind'):
        if record[key] != plan[key]:
            reasons.append('mismatched-plan:' + key)
    if record['treatment'] != plan['treatments'][role]:
        reasons.append('mismatched-plan:treatment')
    # Self-comparison reuses the established acceptance checks without pretending
    # that this is an independent baseline/candidate experiment.
    assessed = compare(plan['spec'], record, record)
    if assessed['status'] == 'not-comparable':
        reasons.extend(sorted({reason.split(':', 1)[-1] if reason.startswith(('baseline:', 'candidate:'))
                               else reason for reason in assessed['reasons']}))
    matches = not reasons
    acceptance = 'not-assessed'
    if matches:
        acceptance = 'failed' if assessed['status'] == 'acceptance-not-satisfied' else 'passed'
        reasons.extend(sorted({reason.split(':', 1)[-1] for reason in assessed['reasons']
                               if assessed['status'] == 'acceptance-not-satisfied'}))
    return {'record_digest': fingerprint(record), 'acceptance': acceptance,
            'submitted_tokens': _usage(record), 'reasons': reasons, 'matches_plan': matches}


def _stats(values: list[int]) -> dict:
    return {'n': len(values), 'total': sum(values), 'mean': statistics.mean(values),
            'median': statistics.median(values),
            'sample_standard_deviation': statistics.stdev(values) if len(values) > 1 else None,
            'minimum': min(values), 'maximum': max(values)}


def summarize(plan: Any, pairs: Any, *, expected_plan_sha256: str) -> dict:
    """Retain planned repetitions; never silently select a passing/known-cost subset.

    Input pairs are {id, baseline, candidate}; null or absent pairs remain missing.
    Pin the reviewed plan before trials. A supplied digest is not authenticated
    preregistration, and records cannot prove all calls/attempts were reported.
    """
    validate_plan(plan, expected_plan_sha256)
    _bounded(pairs)
    require(type(pairs) is list and len(pairs) <= MAX_PAIRS, 'series: invalid pairs')
    supplied = {}
    for pair in pairs:
        require(type(pair) is dict and set(pair) == {'id', *ROLES}
                and type(pair['id']) is str and pair['id'] in plan['pair_ids'], 'series: unplanned pair')
        require(pair['id'] not in supplied, 'series: duplicate pair')
        supplied[pair['id']] = pair
    rows = []
    evidence_owners: dict[tuple, list[dict]] = {}
    for pair_id in plan['pair_ids']:
        pair = supplied.get(pair_id, {'baseline': None, 'candidate': None})
        row = {'id': pair_id}
        for role in ROLES:
            record = pair[role]
            summary = _assess(plan, role, record)
            row[role] = summary
            if record is None:
                continue
            # Distinct paths with the same trace/usage digest do not establish
            # independent repetitions. Shared check logs are not session identity.
            keys = [('record', summary['record_digest'])]
            if plan['evidence_kind'] == 'recorded-session':
                for kind, ref in (('trace', record['trace']), ('usage', record['usage']['evidence'])):
                    if ref is not None:
                        keys.append((kind, ref['sha256']))
            for key in keys:
                evidence_owners.setdefault(key, []).append(summary)
        if all(pair[r] is not None for r in ROLES):
            result = compare(plan['spec'], pair['baseline'], pair['candidate'])
            row['pair_comparison'] = {'status': result['status'], 'reasons': result['reasons']}
        else:
            row['pair_comparison'] = {'status': 'missing-record', 'reasons': []}
        rows.append(row)
    for (kind, _), owners in evidence_owners.items():
        if len(owners) > 1:
            for owner in owners:
                owner['matches_plan'] = False
                owner['acceptance'] = 'not-assessed'
                owner['reasons'].append('reused-' + kind)
    count = len(rows)
    acceptance = {}
    for role in ROLES:
        acceptance[role] = {'planned': count, **{
            state: sum(row[role]['acceptance'] == state for row in rows)
            for state in ('passed', 'failed', 'not-assessed')}}
    missing = sum(row[r]['record_digest'] is None for row in rows for r in ROLES)
    matched = all(row[r]['matches_plan'] for row in rows for r in ROLES)
    complete_usage = matched and all(row[r]['submitted_tokens'] is not None for row in rows for r in ROLES)
    all_passed = all(acceptance[r]['passed'] == count for r in ROLES)
    tokens = None
    if complete_usage:
        baseline = [row['baseline']['submitted_tokens'] for row in rows]
        candidate = [row['candidate']['submitted_tokens'] for row in rows]
        deltas = [before - after for before, after in zip(baseline, candidate)]
        total_before, total_after = sum(baseline), sum(candidate)
        tokens = {'baseline': _stats(baseline), 'candidate': _stats(candidate),
                  'paired_reduction': _stats(deltas),
                  'total_reduction_fraction': (total_before - total_after) / total_before if total_before else None,
                  'includes_failed_acceptance': not all_passed}
    status = ('incomplete-series' if missing else 'not-comparable' if not matched else
              'acceptance-not-satisfied' if not all_passed else
              'usage-unavailable' if not complete_usage else 'descriptive-comparison')
    return {'format_version': 1, 'kind': 'guidance-series-summary', 'status': status,
            'scope': 'supplied-record-fields', 'evidence_kind': plan['evidence_kind'],
            'plan_digest': expected_plan_sha256, 'pairs_digest': fingerprint(pairs),
            'planned_pairs': count, 'supplied_pairs': len(pairs), 'missing_records': missing,
            'acceptance': acceptance, 'pairs': rows, 'submitted_tokens': tokens,
            'model_execution': 'not-performed', 'trace_authenticated': False,
            'plan_preregistration_authenticated': False, 'independence_verified': False,
            'model_quality_verified': False, 'billing_savings_verified': False,
            'optimisation_verified': False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('pairs', type=Path)
    parser.add_argument('--expected-plan-sha256', required=True)
    args = parser.parse_args()
    try:
        result = summarize(load_record(args.plan), load_record(args.pairs),
                           expected_plan_sha256=args.expected_plan_sha256)
        output = json.dumps(result, sort_keys=True, allow_nan=False)
    except (ValueError, OSError, TypeError, RecursionError, OverflowError):
        print(json.dumps({'kind': 'guidance-series-error', 'code': 'invalid-input'}))
        return 2
    print(output)
    # Zero means a complete descriptive comparison, not improvement or approval.
    return 0 if result['status'] == 'descriptive-comparison' else 1


if __name__ == '__main__':
    sys.exit(main())
