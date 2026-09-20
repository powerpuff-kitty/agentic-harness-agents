#!/usr/bin/env python3
"""Actual packet and mutation tests; no model, provider or fixture command runs."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import prepare_guidance_trial as trial
from skill_bundle import ROOT, BundleError


class GuidanceTrial(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / 'source'
        (self.root / 'evals').mkdir(parents=True)
        shutil.copytree(ROOT / 'skills/agentic-improvement', self.root / 'skills/agentic-improvement')
        shutil.copyfile(ROOT / 'LICENSE', self.root / 'LICENSE')
        self.case = {
            'id': 'reviewer-only-case-marker', 'prompt': 'Assess the supplied project guidance.',
            'skill': 'agentic-improvement', 'route': 'current-agent',
            'outcome': 'reviewer-only-answer-marker',
            'sources': {'policy': 'Preserve permission boundaries.',
                        'contrary': 'An alternate route contradicts the claim.'},
            'required': ['policy'], 'provider_authorized': False, 'max_provider_calls': 0,
        }
        self.fixture = self.root / 'evals/guidance-efficiency.json'
        self.write_cases([self.case])
        self.output = self.base / 'prepared'

    def write_cases(self, cases):
        self.fixture.write_bytes(trial.encode({'format_version': 1,
                                               'evidence_kind': 'synthetic-rubric', 'cases': cases}))

    def build(self, mode='progressive'):
        return trial.build_packet(self.root, self.case['id'], mode)

    def prepare(self, mode='progressive', output=None):
        return trial.prepare(self.root, self.case['id'], mode, output or self.output)

    def reject(self):
        with self.assertRaises((trial.PreparationError, BundleError, ValueError)):
            self.prepare()
        self.assertFalse(self.output.exists())

    def test_answer_labels_and_case_ids_are_not_in_participant_files(self):
        files, reviewer = self.build()
        for data in files.values():
            self.assertNotIn(b'reviewer-only-answer-marker', data)
            self.assertNotIn(b'reviewer-only-case-marker', data)
        public = json.loads(files['TASK-INPUT.json'])
        self.assertEqual(set(public), {'task', 'evidence', 'permissions'})
        self.assertEqual(reviewer['case'], self.case)

    def test_changing_only_grading_fields_cannot_change_participant_inputs(self):
        before, _ = self.build()
        changed = copy.deepcopy(self.case)
        changed.update(id='another-private-case', outcome='another-private-answer',
                       route='abstain', required=['contrary'])
        self.write_cases([changed])
        after, _ = trial.build_packet(self.root, changed['id'], 'progressive')
        self.assertEqual(before, after)

    def test_all_evidence_is_preserved_not_only_the_expected_required_subset(self):
        files, _ = self.build()
        self.assertEqual(json.loads(files['TASK-INPUT.json'])['evidence'], self.case['sources'])
        self.assertIn(self.case['sources']['contrary'].encode(), files['TASK.md'])

    def test_full_and_progressive_have_identical_task_and_available_guidance(self):
        full, first = self.build('full')
        progressive, second = self.build('progressive')
        self.assertEqual(first['task_snapshot'], second['task_snapshot'])
        self.assertEqual(first['guidance_snapshot'], second['guidance_snapshot'])
        self.assertEqual({k: v for k, v in full.items() if k != 'TASK.md'},
                         {k: v for k, v in progressive.items() if k != 'TASK.md'})
        self.assertGreater(len(full['TASK.md']), len(progressive['TASK.md']))
        self.assertNotEqual(first['treatment']['sha256'], second['treatment']['sha256'])

    def test_progressive_lists_guides_without_inlining_them(self):
        files, report = self.build()
        guide = files['guidance/references/efficiency.md']
        self.assertNotIn(guide, files['TASK.md'])
        self.assertIn(b'guidance/references/efficiency.md', files['TASK.md'])
        self.assertEqual(report['input_measurements']['initially_included_guide_bytes'], 0)
        full, _ = self.build('full')
        self.assertIn(guide, full['TASK.md'])

    def test_output_contains_actual_files_and_exact_hashes(self):
        result = self.prepare()
        report = json.loads((self.output / 'REVIEWER.json').read_bytes())
        participant = self.output / 'participant'
        files = {p.relative_to(participant).as_posix(): p.read_bytes()
                 for p in participant.rglob('*') if p.is_file()}
        self.assertEqual(trial.identities(files), report['participant_files'])
        self.assertEqual(result['initial_prompt_bytes'], len(files['TASK.md']))
        self.assertEqual(files['guidance/LICENSE'], (ROOT / 'LICENSE').read_bytes())
        self.assertFalse((participant / 'REVIEWER.json').exists())

    def test_packaged_inputs_survive_removal_of_original_source(self):
        self.prepare()
        shutil.rmtree(self.root)
        participant = self.output / 'participant'
        self.assertTrue((participant / 'guidance/references/efficiency.md').is_file())
        self.assertTrue((participant / 'guidance/SKILL.md').is_file())
        self.assertIn('task', json.loads((participant / 'TASK-INPUT.json').read_bytes()))

    def test_repeated_preparation_is_byte_deterministic(self):
        self.prepare()
        other = self.base / 'other'
        self.prepare(output=other)
        for path in self.output.rglob('*'):
            if path.is_file():
                self.assertEqual(path.read_bytes(), (other / path.relative_to(self.output)).read_bytes())

    def test_unknown_usage_identity_and_execution_remain_unknown(self):
        _, report = self.build()
        observed = report['observations']
        for key in ('host', 'model', 'settings', 'input_tokens', 'output_tokens', 'trace'):
            self.assertIsNone(observed[key])
        self.assertEqual(observed['model_execution'], 'not-performed')
        for key in ('host_isolation_verified', 'outcome_verified', 'token_savings_verified'):
            self.assertFalse(observed[key])

    def test_reference_changes_change_guidance_identity_not_task_identity(self):
        _, before = self.build()
        path = self.root / 'skills/agentic-improvement/references/efficiency.md'
        path.write_bytes(path.read_bytes() + b'\nSynthetic additional guidance.\n')
        _, after = self.build()
        self.assertEqual(before['task_snapshot'], after['task_snapshot'])
        self.assertNotEqual(before['guidance_snapshot'], after['guidance_snapshot'])

    def test_missing_guide_fails_before_output_creation(self):
        (self.root / 'skills/agentic-improvement/references/efficiency.md').unlink()
        self.reject()

    def test_unlisted_payload_is_rejected(self):
        (self.root / 'skills/agentic-improvement/extra.md').write_text('unreviewed')
        self.reject()

    def test_case_id_does_not_become_a_filesystem_path(self):
        with self.assertRaises(trial.PreparationError):
            trial.prepare(self.root, '../outside', 'progressive', self.output)
        self.assertFalse(self.output.exists())

    def test_unsupported_mode_is_rejected(self):
        with self.assertRaises(trial.PreparationError):
            self.prepare(mode='unknown')
        self.assertFalse(self.output.exists())

    def test_duplicate_case_ids_are_rejected(self):
        self.write_cases([self.case, self.case])
        self.reject()

    def test_duplicate_json_keys_are_rejected(self):
        self.fixture.write_bytes(b'{"cases":[],"cases":[]}')
        self.reject()

    def test_unsupported_fixture_version_is_rejected(self):
        value = json.loads(self.fixture.read_bytes())
        value['format_version'] = True
        self.fixture.write_bytes(trial.encode(value))
        self.reject()

    def test_simulated_provider_consent_never_becomes_live_permission(self):
        for changes in ({'provider_authorized': True},
                        {'route': 'jev', 'provider_authorized': True, 'max_provider_calls': 1}):
            case = {**self.case, **changes}
            self.write_cases([case])
            self.reject()

    def test_existing_directory_and_file_are_never_overwritten(self):
        self.output.mkdir()
        sentinel = self.output / 'keep.txt'
        sentinel.write_bytes(b'local content')
        with self.assertRaises(trial.PreparationError):
            self.prepare()
        self.assertEqual(sentinel.read_bytes(), b'local content')
        sentinel.unlink()
        self.output.rmdir()
        self.output.write_bytes(b'existing file')
        with self.assertRaises(trial.PreparationError):
            self.prepare()
        self.assertEqual(self.output.read_bytes(), b'existing file')

    def test_source_checkout_is_not_an_output_location(self):
        with self.assertRaises(trial.PreparationError):
            self.prepare(output=self.root / 'generated')
        self.assertFalse((self.root / 'generated').exists())

    def test_linked_guide_is_rejected(self):
        path = self.root / 'skills/agentic-improvement/references/efficiency.md'
        data = path.read_bytes()
        path.unlink()
        external = self.base / 'outside.md'
        external.write_bytes(data)
        try:
            path.symlink_to(external)
        except OSError:
            self.skipTest('symlink creation unavailable')
        self.reject()

    def test_linked_output_parent_is_rejected(self):
        target = self.base / 'linked'
        try:
            target.symlink_to(self.root, target_is_directory=True)
        except OSError:
            self.skipTest('symlink creation unavailable')
        with self.assertRaises(BundleError):
            self.prepare(output=target / 'generated')
        self.assertFalse((self.root / 'generated').exists())

    def test_linked_fixture_parent_is_rejected(self):
        folder = self.root / 'evals'
        moved = self.base / 'fixture'
        folder.rename(moved)
        try:
            folder.symlink_to(moved, target_is_directory=True)
        except OSError:
            self.skipTest('symlink creation unavailable')
        self.reject()

    def test_oversized_input_is_rejected(self):
        self.fixture.write_bytes(b'x' * 65537)
        self.reject()

    def test_packet_limit_is_checked_before_any_write(self):
        with patch.object(trial, 'MAX_PACKET', 1):
            self.reject()

    def test_failed_write_is_not_marked_complete_or_silently_retried(self):
        original = Path.open
        def failing_open(path, mode='r', *args, **kwargs):
            if mode == 'xb' and path.name == 'TASK.md':
                raise OSError('synthetic disk error')
            return original(path, mode, *args, **kwargs)
        with patch.object(Path, 'open', failing_open), self.assertRaises(OSError):
            self.prepare()
        self.assertTrue(self.output.is_dir())
        self.assertFalse((self.output / 'REVIEWER.json').exists())
        with self.assertRaises(trial.PreparationError):
            self.prepare()

    def test_real_entrypoint_prepares_existing_fixture_without_credentials(self):
        result = subprocess.run([
            sys.executable, str(ROOT / '.github/scripts/prepare_guidance_trial.py'),
            '--case', 'supported-claim', '--mode', 'progressive', '--output', str(self.output),
        ], capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['model_execution'], 'not-performed')
        self.assertTrue((self.output / 'participant/TASK.md').is_file())


if __name__ == '__main__':
    unittest.main()
