"""Inspect pinned Codex exec JSONL usage snapshots; never run Codex or a model.

Offline evaluation support for the reviewed cumulative-counter producer. This is
not a general Codex protocol validator, a per-call ledger or a billing estimator.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any

MAX_BYTES = 4_194_304
MAX_LINE_BYTES = 262_144
MAX_EVENTS = 16_384
MAX_TURNS = 128
MAX_TOKENS = 1_000_000_000_000
DIGEST = re.compile(r'sha256:[0-9a-f]{64}\Z')
PRODUCER = 'openai/codex@5e5cadad6b90f90a999cbc49745a91c61bc0cdbf'
COUNTERS = ('input_tokens', 'cached_input_tokens', 'output_tokens',
            'reasoning_output_tokens', 'cache_write_input_tokens')
REQUIRED_COUNTERS = {'input_tokens', 'cached_input_tokens', 'output_tokens'}


class TraceError(ValueError):
    """Fixed error codes never echo trace bodies, paths or producer messages."""


def require(condition: bool, code: str) -> None:
    if not condition:
        raise TraceError(code)


def digest(raw: bytes) -> str:
    return 'sha256:' + hashlib.sha256(raw).hexdigest()


def _unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate-json-key')
        result[key] = value
    return result


def _number(value: str) -> int:
    require(len(value.lstrip('-')) <= 16, 'json-number-limit')
    return int(value)


def _constant(_):
    raise TraceError('nonfinite-json')


def _identifier(value: Any) -> bool:
    return (type(value) is str and 0 < len(value) <= 256
            and not any(ord(c) < 33 or 127 <= ord(c) <= 159 for c in value))


def _decode(raw: bytes) -> dict:
    try:
        event = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique,
                           parse_int=_number, parse_constant=_constant)
        stack = [(event, 0)]
        nodes = 0
        while stack:
            item, depth = stack.pop()
            nodes += 1
            require(nodes <= 32_768 and depth <= 32, 'event-structure-limit')
            if isinstance(item, dict):
                stack.extend((v, depth + 1) for v in item.values())
            elif isinstance(item, list):
                stack.extend((v, depth + 1) for v in item)
            elif isinstance(item, str):
                item.encode('utf-8')  # reject escaped surrogate code points
            elif type(item) is float:
                # Huge numeric exponents may overflow without using JSON NaN.
                require(-float('inf') < item < float('inf'), 'nonfinite-json')
        require(type(event) is dict and type(event.get('type')) is str,
                'event-object-required')
        return event
    except TraceError:
        raise
    except (UnicodeError, ValueError, TypeError, RecursionError, OverflowError):
        raise TraceError('invalid-jsonl') from None


def _usage(value: Any) -> dict | None:
    if value is None:
        return None
    require(type(value) is dict and REQUIRED_COUNTERS <= set(value) <= set(COUNTERS),
            'unsupported-usage-shape')
    result = {key: value.get(key) for key in COUNTERS}
    require(all(v is None or type(v) is int and 0 <= v <= MAX_TOKENS
                for v in result.values()), 'invalid-token-counter')
    for detail, total in (('cached_input_tokens', 'input_tokens'),
                          ('cache_write_input_tokens', 'input_tokens'),
                          ('reasoning_output_tokens', 'output_tokens')):
        require(result[detail] is None or result[total] is None
                or result[detail] <= result[total], 'counter-detail-exceeds-total')
    return result


def inspect_trace(raw: bytes, *, expected_sha256: str, evidence_kind: str) -> dict:
    """Inspect one explicitly selected stream under a caller-reviewed byte pin.

    Every terminal counter is a snapshot, not an additional model call. Resume
    history, missing usage defaulted to zero, subagent/provider accounting and
    capture completeness cannot be established from this stream alone.
    """
    require(type(raw) is bytes and 0 < len(raw) <= MAX_BYTES, 'trace-size-limit')
    require(type(expected_sha256) is str and DIGEST.fullmatch(expected_sha256) is not None,
            'expected-trace-digest-required')
    require(digest(raw) == expected_sha256, 'trace-digest-mismatch')
    require(type(evidence_kind) is str and evidence_kind in ('synthetic', 'recorded-session'),
            'explicit-evidence-kind-required')
    lines = raw.split(b'\n')
    newline = lines[-1] == b''
    if newline:
        lines.pop()
    require(len(lines) <= MAX_EVENTS, 'event-count-limit')
    turns: list[dict] = []
    commands: list[dict] = []
    thread_id = None
    active = None
    open_items: set[str] = set()
    completed_items: set[str] = set()
    errors: list[int] = []
    external_events: list[int] = []
    snapshots: list[dict] = []
    reasons: set[str] = set()
    previous: dict[str, int] = {}
    for line_number, line in enumerate(lines, 1):
        require(0 < len(line) <= MAX_LINE_BYTES and bool(line.strip()), 'event-size-or-empty-line')
        event = _decode(line)
        kind = event['type']
        if kind == 'thread.started':
            require(set(event) == {'type', 'thread_id'} and _identifier(event['thread_id']),
                    'invalid-thread-event')
            require(thread_id is None and line_number == 1, 'multiple-or-misplaced-thread')
            thread_id = event['thread_id']
            continue
        require(thread_id is not None, 'missing-thread-start')
        if kind == 'turn.started':
            require(set(event) == {'type'} and active is None, 'invalid-turn-start')
            require(len(turns) < MAX_TURNS, 'turn-count-limit')
            active = {'index': len(turns) + 1, 'start_event': line_number,
                      'end_event': None, 'status': 'open', 'usage_event': None}
            turns.append(active)
        elif kind in ('turn.completed', 'turn.failed'):
            require(active is not None, 'terminal-without-open-turn')
            if kind == 'turn.completed':
                require(set(event) == {'type', 'usage'}, 'unsupported-terminal-shape')
                usage = _usage(event['usage'])
                active['usage_event'] = line_number if usage is not None else None
                active['status'] = 'completed'
                if usage is not None:
                    if any(usage[k] is not None and k in previous and usage[k] < previous[k]
                           for k in COUNTERS):
                        reasons.add('nonmonotonic-cumulative-counters')
                    previous.update({k: v for k, v in usage.items() if v is not None})
                    if any(usage[k] is None for k in REQUIRED_COUNTERS):
                        reasons.add('incomplete-usage-counters')
                    snapshots.append({'event_line': line_number, 'turn': active['index'], 'usage': usage})
                else:
                    reasons.add('missing-reported-usage')
            else:
                require(set(event) == {'type', 'error'} and type(event['error']) is dict
                        and type(event['error'].get('message')) is str, 'invalid-failure-event')
                active['status'] = 'failed'
                reasons.add('failed-turn-usage-unavailable')
            active['end_event'] = line_number
            active = None
        elif kind in ('item.started', 'item.updated', 'item.completed'):
            require(set(event) == {'type', 'item'} and active is not None, 'invalid-item-event')
            item = event['item']
            require(type(item) is dict and _identifier(item.get('id'))
                    and _identifier(item.get('type')), 'invalid-item-shape')
            identity = item['id']
            require(identity not in completed_items, 'item-after-completion')
            if kind == 'item.completed':
                completed_items.add(identity)
                open_items.discard(identity)
                if item['type'] == 'command_execution':
                    status = item.get('status')
                    code = item.get('exit_code')
                    require(status in ('completed', 'failed', 'declined'), 'invalid-command-status')
                    require(code is None or type(code) is int and -(2**31) <= code < 2**31,
                            'invalid-command-exit')
                    commands.append({'event_line': line_number, 'turn': active['index'],
                                     'item_id_sha256': digest(identity.encode()), 'status': status,
                                     'exit_code': code,
                                     'reported_failure': status in ('failed', 'declined')
                                     or code is not None and code != 0})
            else:
                open_items.add(identity)
            if item['type'] in ('mcp_tool_call', 'collab_tool_call'):
                external_events.append(line_number)
        elif kind == 'error':
            require(set(event) == {'type', 'message'} and type(event['message']) is str,
                    'invalid-error-event')
            errors.append(line_number)
            reasons.add('stream-error-reported')
        else:
            raise TraceError('unsupported-event-type')
    require(thread_id is not None, 'missing-thread-start')
    if not newline:
        reasons.add('unterminated-last-line')
    if not turns or active is not None:
        reasons.add('missing-terminal-turn')
    if open_items:
        reasons.add('items-without-terminal-events')
    if any(command['reported_failure'] for command in commands):
        reasons.add('command-failure-reported')
    if external_events:
        reasons.add('external-work-accounting-unverified')
    last = snapshots[-1] if snapshots else None
    selected_total = None
    if last is not None:
        usage = last['usage']
        if usage['input_tokens'] is not None and usage['output_tokens'] is not None:
            if usage['input_tokens'] == usage['output_tokens'] == 0:
                reasons.add('zero-usage-may-be-producer-default')
            elif 'nonmonotonic-cumulative-counters' not in reasons:
                selected_total = usage['input_tokens'] + usage['output_tokens']
    if last is None:
        reasons.add('no-usage-snapshot')
    return {
        'format_version': 1, 'kind': 'codex-usage-inspection',
        'evidence_kind': evidence_kind, 'scope': 'supplied-jsonl-events',
        'producer_profile': PRODUCER, 'producer_profile_verified': False,
        'source_sha256': expected_sha256,
        'source_bytes': len(raw), 'events': len(lines),
        'thread_id_sha256': digest(thread_id.encode()),
        'turns': turns, 'usage_snapshots': snapshots,
        'last_snapshot_input_plus_output': selected_total,
        'counter_semantics': 'cumulative-thread-snapshots-not-additive-calls',
        'commands': commands, 'recorded_command_failures': sum(c['reported_failure'] for c in commands),
        'stream_error_events': errors, 'external_work_events': external_events,
        'open_items': len(open_items), 'reasons': sorted(reasons),
        'terminal_sequence_observed': bool(turns) and active is None and newline,
        'model_execution': 'not-performed', 'model_identity': None,
        'source_authenticated': False, 'capture_complete_verified': False,
        'usage_measurement_verified': False, 'whole_task_usage_complete': False,
        'task_acceptance_verified': False, 'billing_savings_verified': False,
        'optimisation_verified': False,
    }


def _read_trace(path: Path) -> bytes:
    """Read one named regular file in a trusted, quiescent filesystem.

    Reject links and observed changes; this is not OS-enforced containment against
    concurrent hostile ancestor replacement. No directories are enumerated.
    """
    require('..' not in path.parts, 'unsafe-input-path')
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        meta = current.lstat()
        require(not stat.S_ISLNK(meta.st_mode)
                and not getattr(meta, 'st_file_attributes', 0) & 0x400, 'linked-input')
    before = absolute.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_size <= MAX_BYTES, 'regular-bounded-file-required')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    fd = os.open(absolute, flags)
    with os.fdopen(fd, 'rb') as stream:
        opened = os.fstat(stream.fileno())
        require(stat.S_ISREG(opened.st_mode), 'regular-bounded-file-required')
        raw = stream.read(MAX_BYTES + 1)
        after = os.fstat(stream.fileno())
    final = absolute.lstat()
    def identity(s):
        return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_mode)
    require(identity(before) == identity(opened) == identity(after) == identity(final)
            and len(raw) == before.st_size and len(raw) <= MAX_BYTES, 'input-changed-or-oversized')
    return raw


def read_trace(path: Path) -> bytes:
    try:
        require(isinstance(path, Path), 'path-object-required')
        return _read_trace(path)
    except TraceError:
        raise
    except (OSError, ValueError):
        raise TraceError('unavailable-or-invalid-input') from None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trace', type=Path)
    parser.add_argument('--expected-sha256', required=True)
    parser.add_argument('--evidence-kind', required=True, choices=['synthetic', 'recorded-session'])
    args = parser.parse_args()
    try:
        result = inspect_trace(read_trace(args.trace), expected_sha256=args.expected_sha256,
                               evidence_kind=args.evidence_kind)
    except (TraceError, OSError, ValueError, TypeError, RecursionError, OverflowError):
        print(json.dumps({'kind': 'codex-usage-error', 'code': 'invalid-or-unsupported-trace'}))
        return 2
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    # 0 means a supported, closed event sequence with a nonzero terminal snapshot;
    # it does not mean observed model success or complete per-call accounting.
    return 0 if not result['reasons'] and result['last_snapshot_input_plus_output'] is not None else 1


if __name__ == '__main__':
    sys.exit(main())
