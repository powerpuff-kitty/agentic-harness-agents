#!/usr/bin/env python3
"""Stage one pinned participant template; never execute a host, helper or model.

Checks file identity for a prepared plan and selected template, not experiment
semantics, authentic authorship, host isolation or successful trial execution.
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

ROOT = Path(__file__).resolve().parents[2]
MAX_FILE = 4_194_304
MAX_TOTAL = 4_194_304
MAX_METADATA = 262_144
MAX_ARTIFACTS = 256
MAX_ENTRIES = 512
DIGEST = re.compile(r'sha256:[0-9a-f]{64}\Z')
PATH = re.compile(r'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\Z')
PAIR = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}\Z')
MODES = {'baseline': 'full', 'candidate': 'progressive'}


class StagingError(ValueError):
    """Fixed diagnostics omit rejected paths and source/answer content."""


def require(condition: bool, code: str) -> None:
    if not condition:
        raise StagingError(code)


def digest(raw: bytes) -> str:
    return 'sha256:' + hashlib.sha256(raw).hexdigest()


def encoded(value) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=True,
                       separators=(',', ':'), allow_nan=False) + '\n').encode()


def _unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate-json-key')
        result[key] = value
    return result


def _constant(_):
    raise StagingError('nonfinite-json')


def decode(raw: bytes):
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique, parse_constant=_constant)
    stack = [(value, 0)]
    nodes = 0
    while stack:
        item, depth = stack.pop()
        nodes += 1
        require(nodes <= 100_000 and depth <= 32, 'metadata-structure-limit')
        if type(item) is dict:
            stack.extend((v, depth + 1) for v in [*item, *item.values()])
        elif type(item) is list:
            stack.extend((v, depth + 1) for v in item)
        elif type(item) is str:
            item.encode('utf-8')
    # Also rejects numeric exponent overflow and escaped non-UTF-8 values.
    encoded(value)
    return value


def safe_path(value) -> bool:
    if type(value) is not str or len(value) > 512 or not PATH.fullmatch(value):
        return False
    reserved = {'con', 'prn', 'aux', 'nul', *(f'com{i}' for i in range(1, 10)),
                *(f'lpt{i}' for i in range(1, 10))}
    return all(not p.startswith('.') and not p.endswith('.')
               and p.split('.')[0].casefold() not in reserved for p in value.split('/'))


def _linked(meta) -> bool:
    return stat.S_ISLNK(meta.st_mode) or bool(getattr(meta, 'st_file_attributes', 0) & 0x400)


def directory(path: Path) -> Path:
    require(isinstance(path, Path) and '..' not in path.parts, 'unsafe-directory-path')
    absolute = Path(os.path.abspath(path))
    for parent in reversed((absolute, *absolute.parents)):
        meta = parent.lstat()
        require(stat.S_ISDIR(meta.st_mode) and not _linked(meta), 'real-directory-required')
    return absolute


def read_regular(path: Path, limit: int) -> bytes:
    """Explicit paths in a trusted quiescent tree; not a race-proof sandbox."""
    directory(path.parent)
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and not _linked(before)
            and before.st_size <= limit, 'regular-bounded-file-required')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    with os.fdopen(os.open(path, flags), 'rb') as stream:
        opened = os.fstat(stream.fileno())
        require(stat.S_ISREG(opened.st_mode), 'regular-bounded-file-required')
        raw = stream.read(limit + 1)
        after = os.fstat(stream.fileno())
    final = path.lstat()
    def identity(meta):
        return (meta.st_dev, meta.st_ino, meta.st_size, meta.st_mtime_ns, meta.st_ctime_ns, meta.st_mode)
    require(identity(before) == identity(opened) == identity(after) == identity(final)
            and len(raw) == before.st_size and len(raw) <= limit, 'input-changed-or-oversized')
    return raw


def _paths(folder: Path, expected: set[str]) -> None:
    """Inspect only the chosen participant subtree, including unexpected entries."""
    expected_dirs = {parent.as_posix() for name in expected for parent in Path(name).parents
                     if parent.as_posix() != '.'}
    found = set()
    pending = [(folder, '')]
    visited = 0
    while pending:
        parent, prefix = pending.pop()
        with os.scandir(parent) as entries:
            for entry in entries:
                visited += 1
                require(visited <= MAX_ENTRIES, 'participant-entry-limit')
                relative = prefix + entry.name
                require(safe_path(relative), 'unsafe-participant-path')
                meta = entry.stat(follow_symlinks=False)
                require(not _linked(meta), 'linked-participant-path')
                if stat.S_ISDIR(meta.st_mode):
                    require(relative in expected_dirs, 'unexpected-participant-directory')
                    pending.append((Path(entry.path), relative + '/'))
                else:
                    require(stat.S_ISREG(meta.st_mode) and relative in expected,
                            'unexpected-participant-file')
                    found.add(relative)
    require(found == expected, 'missing-participant-file')


def _checked_file(path: Path, identity: dict, limit: int) -> bytes:
    raw = read_regular(path, limit)
    require(len(raw) == identity['bytes'] and digest(raw) == identity['sha256'],
            'artifact-identity-mismatch')
    return raw


def _write_new(path: Path, raw: bytes) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), 'wb') as stream:
        require(stream.write(raw) == len(raw), 'incomplete-write')
    require(read_regular(path, max(len(raw), 1)) == raw, 'staged-byte-mismatch')


def _stage(series: Path, output: Path, reviewer_sha256: str, pair_id: str, role: str) -> dict:
    require(type(reviewer_sha256) is str and DIGEST.fullmatch(reviewer_sha256), 'reviewer-pin-required')
    require(type(pair_id) is str and PAIR.fullmatch(pair_id), 'invalid-pair-id')
    require(type(role) is str and role in MODES, 'invalid-trial-role')
    source = directory(series)
    require(isinstance(output, Path) and '..' not in output.parts, 'unsafe-output-path')
    target = Path(os.path.abspath(output))
    directory(target.parent)
    require(target != source and source not in target.parents
            and target != ROOT and ROOT not in target.parents, 'output-inside-input-or-checkout')
    require(not target.exists() and not target.is_symlink(), 'output-already-exists')
    raw_report = read_regular(source / 'REVIEWER.json', MAX_METADATA)
    require(digest(raw_report) == reviewer_sha256, 'reviewer-pin-mismatch')
    report = decode(raw_report)
    require(type(report) is dict and type(report.get('format_version')) is int
            and report['format_version'] == 1 and report.get('kind') == 'guidance-series-preparation',
            'unsupported-preparation')
    require(report.get('participant_directories') == {
        r: f'treatments/{m}/participant' for r, m in MODES.items()}, 'unexpected-template-routes')
    inventory = report.get('artifacts')
    require(type(inventory) is dict and 1 <= len(inventory) <= MAX_ARTIFACTS, 'invalid-artifact-inventory')
    aliases = {}
    for name, identity in inventory.items():
        require(safe_path(name) and type(identity) is dict and set(identity) == {'bytes', 'sha256'}
                and type(identity['bytes']) is int and 0 <= identity['bytes'] <= MAX_FILE
                and type(identity['sha256']) is str and DIGEST.fullmatch(identity['sha256']),
                'invalid-artifact-identity')
        # Detect case aliases in directory prefixes too, before platform-dependent writes.
        for path in (Path(name), *Path(name).parents):
            key = path.as_posix()
            require(aliases.setdefault(key.casefold(), key) == key, 'case-colliding-artifact-paths')
    require('review/plan.json' in inventory, 'missing-plan-identity')
    plan = decode(_checked_file(source / 'review/plan.json', inventory['review/plan.json'], MAX_FILE))
    # The original preparer owns full plan validation. These are staging selectors,
    # not a second schema or an assertion that task/environment declarations are true.
    require(type(plan) is dict and type(plan.get('format_version')) is int
            and plan['format_version'] == 1 and plan.get('kind') == 'guidance-series-plan', 'unsupported-plan')
    plan_pin = digest(encoded(plan)[:-1])  # Existing fingerprint excludes the trailing LF.
    require(plan_pin == report.get('plan_sha256'), 'plan-fingerprint-mismatch')
    pair_ids = plan.get('pair_ids')
    require(type(pair_ids) is list and 1 <= len(pair_ids) <= 128
            and all(type(p) is str and PAIR.fullmatch(p) for p in pair_ids)
            and len(set(pair_ids)) == len(pair_ids) and pair_id in pair_ids, 'unplanned-pair')
    require(type(report.get('planned_pairs')) is int and report['planned_pairs'] == len(pair_ids),
            'planned-count-mismatch')
    treatment = plan.get('treatments', {}).get(role)
    require(type(treatment) is dict and set(treatment) == {'name', 'sha256'}
            and treatment['name'] == MODES[role], 'unexpected-treatment')
    prefix = f'treatments/{MODES[role]}/participant/'
    selected = {name[len(prefix):]: identity for name, identity in inventory.items() if name.startswith(prefix)}
    require({'TASK.md', 'TASK-INPUT.json', 'guidance/SKILL.md'} <= set(selected)
            and all(p in ('TASK.md', 'TASK-INPUT.json') or p.startswith('guidance/') for p in selected),
            'invalid-participant-layout')
    require(sum(i['bytes'] for i in selected.values()) <= MAX_TOTAL, 'participant-byte-limit')
    template = directory(source / prefix)
    _paths(template, set(selected))
    files = {name: _checked_file(template / name, identity, MAX_FILE)
             for name, identity in sorted(selected.items())}
    require(digest(files['TASK.md']) == treatment['sha256'], 'treatment-prompt-mismatch')
    # All inputs are checked before creating output. Commands/scripts remain bytes.
    receipt = {'format_version': 1, 'kind': 'guidance-trial-staging',
               'reviewer_sha256': reviewer_sha256, 'plan_sha256': plan_pin,
               'pair_id': pair_id, 'role': role, 'treatment': treatment,
               'participant_files': selected, 'scope': 'pinned-plan-and-selected-participant-files',
               'model_execution': 'not-performed', 'observed_sessions': 0,
               'host_isolation_verified': False, 'host_loading_verified': False,
               'entire_experiment_verified': False, 'source_authenticated': False,
               'outcome_verified': False, 'token_savings_verified': False}
    receipt_bytes = encoded(receipt)
    require(len(receipt_bytes) <= MAX_METADATA, 'staging-receipt-limit')
    target.mkdir(mode=0o700, exist_ok=False)
    for name, raw in files.items():
        _write_new(target / 'participant' / name, raw)
    _write_new(target / 'STAGING.json', receipt_bytes)  # Last; partial output is never repaired/deleted.
    return {'kind': 'guidance-trial-staged', 'participant_directory': str(target / 'participant'),
            'staging_sha256': digest(receipt_bytes), 'plan_sha256': plan_pin,
            'pair_id': pair_id, 'role': role, 'files_staged': len(files),
            'model_execution': 'not-performed', 'observed_sessions': 0,
            'host_isolation_verified': False, 'token_savings_verified': False}


def stage_trial(series: Path, output: Path, *, expected_reviewer_sha256: str,
                pair_id: str, role: str) -> dict:
    """Copy a selected planned template, not reviewer answers, into a NEW workspace.

    Pin the successful preparation's reviewer bytes separately before staging.
    Permission for this copy is not permission to invoke any host or shipped helper.
    Trusted quiescent input/output ancestors are required; no OS sandbox is created.
    """
    try:
        return _stage(series, output, expected_reviewer_sha256, pair_id, role)
    except StagingError:
        raise
    except (OSError, ValueError, TypeError, KeyError, AttributeError, RecursionError, OverflowError):
        raise StagingError('invalid-or-unavailable-staging-input') from None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--series', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--expected-reviewer-sha256', required=True)
    parser.add_argument('--pair-id', required=True)
    parser.add_argument('--role', required=True)
    args = parser.parse_args()
    try:
        result = stage_trial(args.series, args.output, expected_reviewer_sha256=args.expected_reviewer_sha256,
                             pair_id=args.pair_id, role=args.role)
    except StagingError:
        sys.stdout.buffer.write(encoded({'kind': 'guidance-trial-staging-error',
            'code': 'invalid-input-or-output', 'partial_new_directory_possible': True}))
        return 2
    sys.stdout.buffer.write(encoded(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
