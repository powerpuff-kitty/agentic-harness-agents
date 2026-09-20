#!/usr/bin/env python3
"""Prepare matched skill inputs and an empty pinned series; never run a model."""
from __future__ import annotations

import argparse
import copy
import os
from pathlib import Path
import sys
from typing import Any

from guidance_comparison import fingerprint
from guidance_series import _bounded, validate_plan
from prepare_guidance_trial import (
    MAX_PACKET, ROOT, build_packet, encode, identities, participant_task,
    real_directory_chain, sha,
)
from skill_bundle import BundleError, decode, read_file, safe_path

MAX_OUTPUT = 4 * MAX_PACKET
CONFIG_FIELDS = {'format_version', 'kind', 'evidence_kind', 'identity',
                 'required_checks', 'pair_ids'}


class SeriesPreparationError(ValueError):
    """Fixed diagnostics contain no configuration, evidence or rejected paths."""


def require(condition: bool, code: str) -> None:
    if not condition:
        raise SeriesPreparationError(code)


def _checked_packet(files: dict, report: dict, mode: str) -> None:
    """Check the builder's file/metadata boundary before composing either input."""
    require(type(files) is dict and bool(files) and all(
        type(name) is str and safe_path(name) and type(raw) is bytes
        for name, raw in files.items()), 'invalid-participant-files')
    require(sum(map(len, files.values())) <= MAX_PACKET, 'participant-packet-limit')
    require({'TASK.md', 'TASK-INPUT.json', 'guidance/SKILL.md'} <= set(files)
            and all(name in ('TASK.md', 'TASK-INPUT.json') or name.startswith('guidance/')
                    for name in files), 'unexpected-participant-file')
    require(type(report) is dict and type(report.get('format_version')) is int
            and report['format_version'] == 1
            and report.get('kind') == 'guidance-trial-preparation', 'invalid-preparation-record')
    require(report.get('participant_files') == identities(files), 'participant-file-identity-mismatch')
    require(report.get('treatment') == {'mode': mode, 'sha256': sha(files['TASK.md'])},
            'treatment-identity-mismatch')
    task_bytes = encode(participant_task(report['case']))
    require(files['TASK-INPUT.json'] == task_bytes and report.get('task_snapshot') == sha(task_bytes),
            'task-projection-mismatch')
    guidance = {name[len('guidance/'):]: raw for name, raw in files.items()
                if name.startswith('guidance/')}
    require(report.get('guidance_snapshot') == sha(encode(identities(guidance))),
            'guidance-identity-mismatch')


def build_series(root: Path, case_id: str, configuration: Any) -> tuple[dict[str, bytes], dict]:
    """Compose existing full/progressive packets and evaluator-owned plan v1.

    Environment identity and check definitions are explicit caller declarations,
    not inferred from a working directory or asserted as observed host behavior.
    Input files must remain quiescent. No participant responses are generated.
    """
    _bounded(configuration)
    require(type(configuration) is dict and set(configuration) == CONFIG_FIELDS,
            'invalid-series-configuration')
    require(type(configuration['format_version']) is int and configuration['format_version'] == 1
            and configuration['kind'] == 'guidance-series-configuration',
            'unsupported-series-configuration')
    config = copy.deepcopy(configuration)
    full_files, full = build_packet(root, case_id, 'full')
    progressive_files, progressive = build_packet(root, case_id, 'progressive')
    for files, report, mode in ((full_files, full, 'full'),
                                (progressive_files, progressive, 'progressive')):
        _checked_packet(files, report, mode)
    require(full['case'] == progressive['case'], 'different-case-or-grading')
    require(full['task_snapshot'] == progressive['task_snapshot'], 'different-task-projection')
    require(full['guidance_snapshot'] == progressive['guidance_snapshot'], 'different-guidance')
    require({name: raw for name, raw in full_files.items() if name != 'TASK.md'} ==
            {name: raw for name, raw in progressive_files.items() if name != 'TASK.md'},
            'different-available-evidence-or-guidance')
    plan = {
        'format_version': 1, 'kind': 'guidance-series-plan',
        'spec': {'case': copy.deepcopy(full['case']), 'required_checks': config['required_checks']},
        'evidence_kind': config['evidence_kind'], 'identity': config['identity'],
        'treatments': {
            'baseline': {'name': 'full', 'sha256': sha(full_files['TASK.md'])},
            'candidate': {'name': 'progressive', 'sha256': sha(progressive_files['TASK.md'])},
        },
        'pair_ids': config['pair_ids'],
    }
    pin = fingerprint(plan)
    validate_plan(plan, pin)
    pairs = [{'id': pair_id, 'baseline': None, 'candidate': None} for pair_id in plan['pair_ids']]
    artifacts = {'review/plan.json': encode(plan), 'review/plan.sha256': (pin + '\n').encode(),
                 'review/pairs.json': encode(pairs)}
    for files, preparation, mode in ((full_files, full, 'full'),
                                     (progressive_files, progressive, 'progressive')):
        artifacts.update({f'treatments/{mode}/participant/{name}': raw for name, raw in files.items()})
        artifacts[f'review/{mode}-preparation.json'] = encode(preparation)
    report = {
        'format_version': 1, 'kind': 'guidance-series-preparation',
        'plan_sha256': pin, 'configuration_sha256': sha(encode(config)),
        'task_snapshot': full['task_snapshot'], 'guidance_snapshot': full['guidance_snapshot'],
        'planned_pairs': len(pairs), 'artifacts': identities(artifacts),
        'participant_directories': {'baseline': 'treatments/full/participant',
                                    'candidate': 'treatments/progressive/participant'},
        'model_execution': 'not-performed', 'observed_sessions': 0,
        'host_identity_verified': False, 'host_isolation_verified': False,
        'plan_preregistration_authenticated': False, 'outcome_verified': False,
        'token_savings_verified': False,
        'limits': ['configuration identities are caller declarations',
                   'plans and grading metadata are reviewer-only',
                   'directory separation is not a sandbox or independent session',
                   'copy only one participant template into each fresh authorized session',
                   'all planned trial records remain null until evidence is independently reviewed'],
    }
    require(sum(map(len, artifacts.values())) + len(encode(report)) <= MAX_OUTPUT,
            'series-output-limit')
    return artifacts, report


def prepare_series(root: Path, case_id: str, configuration: Any, output: Path) -> dict:
    """Write a new private experiment directory; never repair existing output."""
    require(isinstance(output, Path) and '..' not in output.parts, 'unsafe-output-path')
    root = real_directory_chain(root)
    target = Path(os.path.abspath(output))
    real_directory_chain(target.parent)
    require(target != root and root not in target.parents, 'output-inside-checkout')
    require(not target.exists() and not target.is_symlink(), 'output-already-exists')
    files, report = build_series(root, case_id, configuration)
    target.mkdir(mode=0o700, exist_ok=False)
    # REVIEWER.json is deliberately last. Failed I/O may leave a partial new
    # directory, never a claimed completed preparation or an automatic cleanup.
    for name, raw in [*sorted(files.items()), ('REVIEWER.json', encode(report))]:
        destination = target / name
        destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
    return {'kind': 'guidance-series-prepared', 'directory': str(target),
            'reviewer_sha256': sha(encode(report)),
            'plan_sha256': report['plan_sha256'], 'planned_pairs': report['planned_pairs'],
            'observed_sessions': 0, 'model_execution': 'not-performed',
            'token_savings_verified': False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True, dest='case_id')
    parser.add_argument('--config', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        require('..' not in args.config.parts, 'unsafe-configuration-path')
        real_directory_chain(args.config.parent)
        configuration = decode(read_file(args.config))
        result = prepare_series(ROOT, args.case_id, configuration, args.output)
    except (ValueError, BundleError, OSError, TypeError, KeyError, RecursionError, OverflowError):
        result = {'kind': 'guidance-series-preparation-error', 'code': 'invalid-input-or-output',
                  'partial_new_directory_possible': True}
        sys.stdout.buffer.write(encode(result))
        return 2
    sys.stdout.buffer.write(encode(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
