"""Synthetic staging and actual preparer integration; no host/model is executed."""
import copy
import json
import os
from pathlib import Path
import socket
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import stage_guidance_trial as staging

HERE = Path(__file__).resolve().parent


def identities(files):
    return {name: {'sha256': staging.digest(raw), 'bytes': len(raw)} for name, raw in files.items()}


def synthetic_series(root):
    """Use existing artifact shapes, with an intentionally conspicuous reviewer answer."""
    tasks = {'full': b'Full supplied instructions.\n', 'progressive': b'Read guides as needed.\n'}
    artifacts = {}
    for mode, prompt in tasks.items():
        files = {'TASK.md': prompt, 'TASK-INPUT.json': b'{"evidence":"Keep contradictory evidence."}\n',
                 'guidance/SKILL.md': b'Synthetic procedure.\n',
                 'guidance/references/guide.md': 'Retain qualifiers. 東京\r\n'.encode(),
                 'guidance/scripts/helper.py': b'raise RuntimeError("MUST_NOT_EXECUTE")\n',
                 'guidance/LICENSE': b'Synthetic attribution.\n'}
        artifacts.update({f'treatments/{mode}/participant/{k}': v for k, v in files.items()})
    plan = {'format_version': 1, 'kind': 'guidance-series-plan',
            'spec': {'case': {'outcome': 'REVIEWER_ONLY_ANSWER'}},
            'identity': {'model': 'REVIEWER_ONLY_MODEL'}, 'evidence_kind': 'synthetic',
            'pair_ids': ['r1', 'r2'], 'treatments': {
                role: {'name': mode, 'sha256': staging.digest(tasks[mode])}
                for role, mode in staging.MODES.items()}}
    artifacts['review/plan.json'] = staging.encoded(plan)
    artifacts['review/pairs.json'] = staging.encoded([
        {'id': p, 'baseline': None, 'candidate': None} for p in plan['pair_ids']])
    pin = staging.digest(staging.encoded(plan)[:-1])
    report = {'format_version': 1, 'kind': 'guidance-series-preparation', 'plan_sha256': pin,
              'planned_pairs': 2, 'artifacts': identities(artifacts), 'participant_directories': {
                  role: f'treatments/{mode}/participant' for role, mode in staging.MODES.items()}}
    for name, raw in artifacts.items():
        path = root / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
    (root / 'REVIEWER.json').write_bytes(staging.encoded(report))
    return artifacts, report


class StagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name).resolve()
        self.root = self.parent / 'series'
        self.artifacts, self.report = synthetic_series(self.root)
        self.pin = staging.digest((self.root / 'REVIEWER.json').read_bytes())
        self.output = self.parent / 'run'
        self.template = self.root / 'treatments/full/participant'

    def stage(self, **kwargs):
        return staging.stage_trial(self.root, kwargs.pop('output', self.output),
            expected_reviewer_sha256=kwargs.pop('pin', self.pin),
            pair_id=kwargs.pop('pair_id', 'r1'), role=kwargs.pop('role', 'baseline'), **kwargs)

    def repin(self):
        (self.root / 'REVIEWER.json').write_bytes(staging.encoded(self.report))
        self.pin = staging.digest((self.root / 'REVIEWER.json').read_bytes())

    def test_exact_selected_bytes_only_and_receipt_outside_participant(self):
        result = self.stage()
        expected = {k.split('/participant/', 1)[1]: v for k, v in self.artifacts.items()
                    if k.startswith('treatments/full/participant/')}
        actual = {p.relative_to(self.output / 'participant').as_posix(): p.read_bytes()
                  for p in (self.output / 'participant').rglob('*') if p.is_file()}
        self.assertEqual(actual, expected)
        self.assertEqual(result['files_staged'], len(expected))
        self.assertTrue((self.output / 'STAGING.json').is_file())
        combined = b''.join(actual.values())
        self.assertNotIn(b'REVIEWER_ONLY', combined)
        self.assertFalse((self.output / 'participant/STAGING.json').exists())
        self.assertEqual(result['observed_sessions'], 0)
        self.assertEqual(result['model_execution'], 'not-performed')
        receipt = json.loads((self.output / 'STAGING.json').read_bytes())
        for key in ('host_isolation_verified', 'host_loading_verified', 'entire_experiment_verified',
                    'source_authenticated', 'outcome_verified', 'token_savings_verified'):
            self.assertIs(receipt[key], False)

    def test_progressive_role_selects_other_exact_prompt(self):
        self.stage(role='candidate')
        self.assertEqual((self.output / 'participant/TASK.md').read_bytes(),
                         self.artifacts['treatments/progressive/participant/TASK.md'])

    def test_changed_reviewer_rejected_before_output(self):
        (self.root / 'REVIEWER.json').write_bytes(staging.encoded(self.report) + b' ')
        with self.assertRaisesRegex(staging.StagingError, 'reviewer-pin-mismatch'):
            self.stage()
        self.assertFalse(self.output.exists())

    def test_changed_plan_or_participant_rejected_before_output(self):
        for path in (self.root / 'review/plan.json', self.template / 'TASK.md',
                     self.template / 'guidance/references/guide.md'):
            raw = path.read_bytes(); path.write_bytes(raw + b'Changed.')
            with self.subTest(path=path.name), self.assertRaises(staging.StagingError): self.stage()
            path.write_bytes(raw)
            self.assertFalse(self.output.exists())

    def test_same_size_change_is_rejected(self):
        path = self.template / 'TASK.md'; path.write_bytes(path.read_bytes().replace(b'Full', b'Fake'))
        with self.assertRaises(staging.StagingError): self.stage()

    def test_missing_selected_file_rejected(self):
        (self.template / 'guidance/LICENSE').unlink()
        with self.assertRaises(staging.StagingError): self.stage()
        self.assertFalse(self.output.exists())

    def test_extra_selected_file_or_empty_directory_rejected(self):
        for relative, is_dir in [('AGENTS.md', False), ('REVIEWER.json', False), ('extra', True)]:
            path = self.template / relative
            path.mkdir() if is_dir else path.write_bytes(b'REVIEWER_ONLY_ANSWER')
            with self.subTest(relative=relative), self.assertRaises(staging.StagingError): self.stage()
            path.rmdir() if is_dir else path.unlink()
        self.assertFalse(self.output.exists())

    def test_selected_file_or_directory_symlink_rejected(self):
        target = self.parent / 'outside'; target.write_bytes(b'external')
        link = self.template / 'guidance/new'; link.symlink_to(target)
        with self.assertRaises(staging.StagingError): self.stage()
        link.unlink(); link.symlink_to(self.parent, target_is_directory=True)
        with self.assertRaises(staging.StagingError): self.stage()

    def test_source_and_output_parent_symlinks_rejected(self):
        link = self.parent / 'link'; link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(staging.StagingError):
            staging.stage_trial(link, self.output, expected_reviewer_sha256=self.pin, pair_id='r1', role='baseline')
        with self.assertRaises(staging.StagingError): self.stage(output=link / 'run')

    def test_unplanned_pair_bad_role_or_pin_rejected(self):
        for kwargs in ({'pair_id': 'r3'}, {'pair_id': '../r1'}, {'role': 'full'},
                       {'role': []}, {'pin': 'bad'}, {'pin': staging.digest(b'other')}):
            with self.subTest(kwargs=kwargs), self.assertRaises(staging.StagingError): self.stage(**kwargs)
        self.assertFalse(self.output.exists())

    def test_existing_output_never_overwritten(self):
        self.output.mkdir(); marker = self.output / 'keep'; marker.write_bytes(b'untouched')
        with self.assertRaises(staging.StagingError): self.stage()
        self.assertEqual(marker.read_bytes(), b'untouched')

    def test_inside_source_checkout_and_traversal_outputs_rejected(self):
        for output in (self.root / 'nested', staging.ROOT / 'new-trial', self.parent / '..' / 'unsafe'):
            with self.subTest(output=output.name), self.assertRaises(staging.StagingError):
                self.stage(output=output)

    def test_no_reads_of_other_treatment_or_answer_files(self):
        original = staging.read_regular; read = []
        def tracked(path, limit):
            read.append(path)
            return original(path, limit)
        with patch.object(staging, 'read_regular', side_effect=tracked): self.stage()
        self.assertNotIn(self.root / 'review/pairs.json', read)
        self.assertFalse(any('progressive' in p.parts for p in read))
        self.assertEqual(sum(p == self.root / 'review/plan.json' for p in read), 1)

    def test_no_helper_network_or_host_execution(self):
        with patch.object(socket, 'socket', side_effect=AssertionError('network')), \
             patch.object(subprocess, 'run', side_effect=AssertionError('process')):
            self.stage()
        self.assertFalse((self.parent / 'MUST_NOT_EXECUTE').exists())

    def test_extra_review_files_are_not_copied_or_certified(self):
        (self.root / 'review/secret-answer.txt').write_bytes(b'REVIEWER_ONLY_ANSWER')
        self.stage()
        self.assertFalse((self.output / 'participant/review').exists())
        self.assertFalse(json.loads((self.output / 'STAGING.json').read_bytes())['entire_experiment_verified'])

    def test_bad_manifest_paths_and_case_aliases_rejected(self):
        base = copy.deepcopy(self.report)
        for name in ('../outside', '/absolute', 'review/NUL.txt', 'review/name.',
                     'treatments/full/Participant/TASK.md'):
            self.report = copy.deepcopy(base)
            self.report['artifacts'][name] = {'bytes': 1, 'sha256': staging.digest(b'x')}
            self.repin()
            with self.subTest(name=name), self.assertRaises(staging.StagingError): self.stage()
        self.assertFalse(self.output.exists())

    def test_template_routes_cannot_redirect_reads(self):
        self.report['participant_directories']['baseline'] = 'review'
        self.repin()
        with self.assertRaises(staging.StagingError): self.stage()

    def test_limits_apply_before_creating_output(self):
        for name, value in [('MAX_TOTAL', 1), ('MAX_FILE', 1), ('MAX_METADATA', 1),
                            ('MAX_ARTIFACTS', 1), ('MAX_ENTRIES', 1)]:
            with self.subTest(name=name), patch.object(staging, name, value), self.assertRaises(staging.StagingError):
                self.stage()
            self.assertFalse(self.output.exists())

    def test_duplicate_json_and_false_version_rejected(self):
        for raw in (b'{"kind":1,"kind":2}', b'{"format_version":NaN}',
                    staging.encoded({**self.report, 'format_version': True})):
            (self.root / 'REVIEWER.json').write_bytes(raw)
            with self.assertRaises(staging.StagingError): self.stage(pin=staging.digest(raw))

    def test_missing_completion_marker_and_missing_plan_rejected(self):
        for path in (self.root / 'REVIEWER.json', self.root / 'review/plan.json'):
            raw = path.read_bytes(); path.unlink()
            with self.assertRaises(staging.StagingError): self.stage()
            path.write_bytes(raw)
        self.assertFalse(self.output.exists())

    def test_partial_failure_keeps_new_files_without_receipt(self):
        original = staging._write_new; writes = []
        def interrupted(path, raw):
            writes.append(path)
            if len(writes) == 2: raise OSError('DO_NOT_ECHO')
            original(path, raw)
        with patch.object(staging, '_write_new', side_effect=interrupted), self.assertRaises(staging.StagingError):
            self.stage()
        self.assertTrue(writes[0].is_file())
        self.assertFalse((self.output / 'STAGING.json').exists())
        with self.assertRaises(staging.StagingError): self.stage()
        self.assertTrue(writes[0].is_file())

    def test_private_modes_and_independent_copies(self):
        self.stage()
        destination = self.output / 'participant/TASK.md'
        if os.name == 'posix':
            self.assertEqual(stat.S_IMODE(destination.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(destination.parent.stat().st_mode), 0o700)
        destination.write_bytes(b'Changed only the copy.')
        self.assertEqual((self.template / 'TASK.md').read_bytes(), self.artifacts['treatments/full/participant/TASK.md'])
        self.stage(output=self.parent / 'another', pair_id='r2')
        self.assertEqual((self.parent / 'another/participant/TASK.md').read_bytes(), self.artifacts['treatments/full/participant/TASK.md'])

    def test_command_reports_zero_sessions_and_preserves_source(self):
        command = [sys.executable, str(HERE / 'stage_guidance_trial.py'), '--series', str(self.root),
                   '--output', str(self.output), '--expected-reviewer-sha256', self.pin,
                   '--pair-id', 'r1', '--role', 'baseline']
        result = subprocess.run(command, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['observed_sessions'], 0)
        self.assertNotIn(b'REVIEWER_ONLY', result.stdout + result.stderr)
        result = subprocess.run(command, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(b'REVIEWER_ONLY', result.stdout + result.stderr)
        self.assertEqual(staging.digest((self.root / 'REVIEWER.json').read_bytes()), self.pin)

    def test_reviewer_repin_does_not_hide_plan_treatment_mismatch(self):
        plan_path = self.root / 'review/plan.json'; plan = json.loads(plan_path.read_bytes())
        plan['treatments']['baseline']['sha256'] = staging.digest(b'wrong prompt')
        plan_path.write_bytes(staging.encoded(plan))
        self.report['plan_sha256'] = staging.digest(staging.encoded(plan)[:-1])
        self.report['artifacts']['review/plan.json'] = identities({'x': plan_path.read_bytes()})['x']
        self.repin()
        with self.assertRaisesRegex(staging.StagingError, 'treatment-prompt-mismatch'): self.stage()


class PreparedSeriesStagingIntegration(unittest.TestCase):
    def test_real_preparation_staging_and_empty_evaluation(self):
        from prepare_guidance_series import prepare_series, ROOT
        from guidance_series import summarize
        from test_guidance_series_preparation import configuration
        with tempfile.TemporaryDirectory() as folder:
            parent = Path(folder).resolve(); source = parent / 'series'
            prepared = prepare_series(ROOT, 'supported-claim', configuration(), source)
            self.assertEqual(prepared['reviewer_sha256'], staging.digest((source / 'REVIEWER.json').read_bytes()))
            for role, mode in staging.MODES.items():
                output = parent / role
                result = staging.stage_trial(source, output, expected_reviewer_sha256=prepared['reviewer_sha256'],
                                              pair_id='r1', role=role)
                template = source / f'treatments/{mode}/participant'
                expected = {p.relative_to(template): p.read_bytes() for p in template.rglob('*') if p.is_file()}
                actual = {p.relative_to(output / 'participant'): p.read_bytes()
                          for p in (output / 'participant').rglob('*') if p.is_file()}
                self.assertEqual(actual, expected)
                self.assertEqual(result['observed_sessions'], 0)
            summary = summarize(json.loads((source / 'review/plan.json').read_bytes()),
                                json.loads((source / 'review/pairs.json').read_bytes()),
                                expected_plan_sha256=prepared['plan_sha256'])
            self.assertEqual(summary['missing_records'], 6)
            self.assertEqual(summary['status'], 'incomplete-series')
            self.assertIsNone(summary['submitted_tokens'])


if __name__ == '__main__':
    unittest.main()
