#!/usr/bin/env python3
"""Compare 2 explicit local fact snapshots; no network, schedule, alerts or writes."""
from __future__ import annotations
import argparse
from datetime import datetime
import json
from pathlib import Path
import sys

MAX_BYTES = 1_048_576


def require(ok, message):
    if not ok:
        raise ValueError(message)


def timestamp(value):
    require(isinstance(value, str), 'timestamp required')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(parsed.tzinfo is not None and parsed.utcoffset() is not None, 'timezone required')
    return parsed


def text(value, limit=4096):
    return isinstance(value, str) and 0 < len(value) <= limit


def validate(value):
    require(isinstance(value, dict) and set(value) == {'format_version', 'captured_at', 'sources'}, 'snapshot fields')
    require(type(value['format_version']) is int and value['format_version'] == 1, 'snapshot version')
    captured = timestamp(value['captured_at'])
    require(isinstance(value['sources'], list) and len(value['sources']) <= 128, 'source inventory')
    ids = set()
    for source in value['sources']:
        require(isinstance(source, dict) and set(source) == {'id', 'locator', 'status', 'observed_at', 'facts'}, 'source fields')
        require(text(source['id'], 128) and source['id'] not in ids and text(source['locator']), 'source identity')
        ids.add(source['id'])
        require(source['status'] in ['ok', 'unavailable'], 'source status')
        require(isinstance(source['facts'], list) and len(source['facts']) <= 2048, 'fact inventory')
        if source['status'] == 'unavailable':
            require(source['observed_at'] is None and not source['facts'], 'unavailable source cannot supply observations')
        else:
            require(timestamp(source['observed_at']) <= captured, 'future observation')
        keys = set()
        for fact in source['facts']:
            require(isinstance(fact, dict) and set(fact) == {'key', 'value', 'qualifiers', 'evidence'}, 'fact fields')
            require(text(fact['key'], 128) and fact['key'] not in keys and text(fact['evidence']), 'fact identity/evidence')
            keys.add(fact['key'])
            data = fact['value']
            require(type(data) in [str, int, float, bool] and (not isinstance(data, str) or len(data) <= 4096), 'scalar fact required')
            # Reject nonfinite programmatic inputs as well as JSON constants.
            json.dumps(data, allow_nan=False)
            qualifiers = fact['qualifiers']
            require(isinstance(qualifiers, dict) and len(qualifiers) <= 16 and
                    all(text(k, 128) and text(v, 512) for k, v in qualifiers.items()), 'qualifiers required')
    return value


def normalized(value):
    return ' '.join(value.split()) if isinstance(value, str) else value


def compare(baseline, current):
    validate(baseline)
    validate(current)
    items = []
    if timestamp(current['captured_at']) < timestamp(baseline['captured_at']):
        items.append({'classification': 'stale_snapshot', 'reason': 'current capture predates baseline'})
    else:
        old = {s['id']: s for s in baseline['sources']}
        new = {s['id']: s for s in current['sources']}
        if not old and not new:
            items.append({'classification': 'coverage_gap', 'reason': 'no sources supplied'})
        for source_id in sorted(old.keys() | new.keys()):
            a, b = old.get(source_id), new.get(source_id)
            entry = {'source_id': source_id, 'baseline_observed_at': a['observed_at'] if a else None,
                     'current_observed_at': b['observed_at'] if b else None}
            if a is None or b is None or a['status'] != 'ok' or b['status'] != 'ok':
                items.append({**entry, 'classification': 'coverage_gap',
                              'baseline_status': a['status'] if a else 'not_supplied',
                              'current_status': b['status'] if b else 'not_supplied'})
                continue
            if a['locator'] != b['locator']:
                items.append({**entry, 'classification': 'context_changed', 'reason': 'source locator changed'})
                continue
            if timestamp(b['observed_at']) < timestamp(a['observed_at']):
                items.append({**entry, 'classification': 'stale_observation'})
                continue
            previous = {f['key']: f for f in a['facts']}
            latest = {f['key']: f for f in b['facts']}
            if not previous and not latest:
                items.append({**entry, 'classification': 'coverage_gap', 'reason': 'no facts supplied'})
            for key in sorted(previous.keys() | latest.keys()):
                x, y = previous.get(key), latest.get(key)
                if x is None:
                    kind = 'new_observation'
                elif y is None:
                    kind = 'not_observed'
                elif x['qualifiers'] != y['qualifiers']:
                    kind = 'context_changed'
                elif type(x['value']) is type(y['value']) and normalized(x['value']) == normalized(y['value']):
                    kind = 'unchanged'
                else:
                    kind = 'changed'
                items.append({**entry, 'fact_key': key, 'classification': kind, 'baseline': x, 'current': y})
    return {'kind': 'competitor-snapshot-comparison', 'baseline_at': baseline['captured_at'],
            'current_at': current['captured_at'], 'items': items,
            'normalization': 'Collapse whitespace in string fact values only; qualifiers and scalar types remain exact.',
            'retrieval': 'not_performed', 'alerts_sent': False,
            'limits': 'Caller-supplied observations only; no fact verification, freshness SLA, removal inference, scheduler or business-cause judgment.'}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def bad_constant(value):
    raise ValueError('nonfinite JSON')


def load(path):
    # Explicit caller-selected files on a trusted filesystem; not a path sandbox.
    with path.open('rb') as stream:
        data = stream.read(MAX_BYTES + 1)
    require(len(data) <= MAX_BYTES, 'input exceeds limit')
    return json.loads(data.decode('utf-8'), object_pairs_hook=unique_object, parse_constant=bad_constant)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline', type=Path)
    parser.add_argument('current', type=Path)
    args = parser.parse_args()
    try:
        result = compare(load(args.baseline), load(args.current))
    except (ValueError, OSError, UnicodeError, TypeError, OverflowError, RecursionError):
        print('{"kind":"snapshot-error","code":"invalid-input"}', file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 1 if any(i['classification'] != 'unchanged' for i in result['items']) else 0


if __name__ == '__main__':
    raise SystemExit(main())
