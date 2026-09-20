"""Exercise real preparation-to-series composition; no model sessions are run."""
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

import prepare_guidance_series as series
from guidance_comparison import fingerprint
from guidance_series import summarize, validate_plan
from prepare_guidance_trial import build_packet, encode, sha

HERE = Path(__file__).resolve().parent


def configuration():
    return {'format_version': 1, 'kind': 'guidance-series-configuration',
            'evidence_kind': 'synthetic',
            'identity': {'host': 'synthetic-host', 'model': 'synthetic-model',
                         **{key: fingerprint(key) for key in ('source_snapshot', 'policy_snapshot',
                                                             'checks_snapshot', 'settings_snapshot')}},
            'required_checks': ['reviewed-acceptance'], 'pair_ids': ['r1', 'r2', 'r3']}


class GuidanceSeriesPreparation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name).resolve()
        self.root = self.parent / 'checkout'
        self.skill = self.root / 'skills/decision-intelligence'
        (self.skill / 'references').mkdir(parents=True)
        (self.root / 'evals').mkdir()
        (self.root / 'LICENSE').write_text('Synthetic license notice.\n')
        skill = ('---\nname: decision-intelligence\ndescription: "Review supplied evidence."\n---\n'
                 '# Decision intelligence\n\n' + ''.join('## ' + heading + '\n\n'
                 for heading in ('Objective', 'Inputs', 'Context', 'Procedure', 'Output', 'Completion'))
                 + '[Guide](references/guide.md)\n')
        (self.skill / 'SKILL.md').write_text(skill)
        (self.skill / 'references/guide.md').write_text('Keep missing and contradictory evidence visible.\n')
        self.bundle = {'format_version': 1, 'kind': 'standalone-skill', 'name': 'decision-intelligence',
                       'files': ['SKILL.md', 'references/guide.md'], 'shared_references': {},
                       'optional_tools': []}
        (self.skill / 'bundle.json').write_bytes(encode(self.bundle))
        self.case = {'id': 'test-case', 'prompt': 'Review the supplied claim.',
                     'skill': 'decision-intelligence', 'route': 'current-agent',
                     'outcome': 'review-required',
                     'sources': {'policy': 'Claims need evidence.', 'source': 'The claim has one source.',
                                 'contrary': 'A second source contradicts it.'},
                     'required': ['policy', 'source'], 'provider_authorized': False, 'max_provider_calls': 0}
        self.save_case()
        self.config = configuration()

    def save_case(self):
        (self.root / 'evals/guidance-efficiency.json').write_bytes(encode({
            'format_version': 1, 'evidence_kind': 'synthetic-rubric', 'cases': [self.case]}))

    def build(self, config=None):
        return series.build_series(self.root, 'test-case', self.config if config is None else config)

    def plan(self, files):
        return json.loads(files['review/plan.json'])

    def test_plan_uses_exact_prompt_bytes_and_existing_validator(self):
        files, report = self.build()
        plan = self.plan(files)
        validate_plan(plan, report['plan_sha256'])
        for role, mode in [('baseline', 'full'), ('candidate', 'progressive')]:
            self.assertEqual(plan['treatments'][role], {'name': mode,
                'sha256': sha(files[f'treatments/{mode}/participant/TASK.md'])})
        self.assertEqual(plan['spec']['case'], self.case)
        self.assertEqual(plan['spec']['required_checks'], self.config['required_checks'])
        self.assertEqual(files['review/plan.sha256'].decode().strip(), fingerprint(plan))

    def test_empty_roster_is_incomplete_not_a_successful_trial(self):
        files, report = self.build()
        pairs = json.loads(files['review/pairs.json'])
        self.assertEqual(pairs, [{'id': i, 'baseline': None, 'candidate': None}
                                 for i in self.config['pair_ids']])
        result = summarize(self.plan(files), pairs, expected_plan_sha256=report['plan_sha256'])
        self.assertEqual(result['status'], 'incomplete-series')
        self.assertEqual(result['missing_records'], 6)
        self.assertIsNone(result['submitted_tokens'])
        self.assertEqual(result['acceptance']['candidate']['not-assessed'], 3)
        self.assertFalse(result['optimisation_verified'])

    def test_existing_participant_packets_are_byte_identical(self):
        files, _ = self.build()
        for mode in ('full', 'progressive'):
            expected, _ = build_packet(self.root, 'test-case', mode)
            prefix = f'treatments/{mode}/participant/'
            actual = {name[len(prefix):]: raw for name, raw in files.items() if name.startswith(prefix)}
            self.assertEqual(actual, expected)

    def test_every_evidence_source_is_retained_not_only_required_subset(self):
        files, _ = self.build()
        for mode in ('full', 'progressive'):
            task = json.loads(files[f'treatments/{mode}/participant/TASK-INPUT.json'])
            self.assertEqual(task['evidence'], self.case['sources'])
            self.assertIn('contrary', task['evidence'])
            self.assertFalse(task['permissions']['network'])
            self.assertEqual(task['permissions']['provider_calls'], 0)

    def test_grading_and_environment_changes_never_leak_into_participant_input(self):
        before, first = self.build()
        self.case.update(outcome='REVIEWER_ONLY_ANSWER', required=['contrary'], route='abstain')
        self.save_case()
        self.config['identity']['model'] = 'REVIEWER_ONLY_MODEL'
        self.config['pair_ids'] = ['REVIEWER_ONLY_RUN']
        after, second = self.build()
        participant = lambda files: {k: v for k, v in files.items() if '/participant/' in k}
        self.assertEqual(participant(before), participant(after))
        self.assertNotEqual(first['plan_sha256'], second['plan_sha256'])
        for raw in participant(after).values():
            self.assertNotIn(b'REVIEWER_ONLY', raw)
        self.assertNotIn('case', first)

    def test_mismatched_case_between_disclosure_modes_is_rejected(self):
        full = build_packet(self.root, 'test-case', 'full')
        self.case['sources']['contrary'] = 'Changed evidence.'
        self.save_case()
        progressive = build_packet(self.root, 'test-case', 'progressive')
        with patch.object(series, 'build_packet', side_effect=[full, progressive]):
            with self.assertRaisesRegex(series.SeriesPreparationError, 'different-case'):
                self.build()

    def test_mismatched_guidance_between_modes_is_rejected(self):
        full = build_packet(self.root, 'test-case', 'full')
        (self.skill / 'references/guide.md').write_text('Changed reference.\n')
        progressive = build_packet(self.root, 'test-case', 'progressive')
        with patch.object(series, 'build_packet', side_effect=[full, progressive]):
            with self.assertRaisesRegex(series.SeriesPreparationError, 'different-guidance'):
                self.build()

    def test_changed_prompt_bytes_are_rejected_before_output(self):
        full = build_packet(self.root, 'test-case', 'full')
        progressive = build_packet(self.root, 'test-case', 'progressive')
        full[0]['TASK.md'] += b'Changed after preparation.'
        with patch.object(series, 'build_packet', side_effect=[full, progressive]):
            with self.assertRaisesRegex(series.SeriesPreparationError, 'file-identity-mismatch'):
                self.build()

    def test_treatment_hash_cannot_be_supplied_independently_of_prompt(self):
        full = build_packet(self.root, 'test-case', 'full')
        progressive = build_packet(self.root, 'test-case', 'progressive')
        full[1]['treatment']['sha256'] = sha(b'not the prompt')
        with patch.object(series, 'build_packet', side_effect=[full, progressive]):
            with self.assertRaisesRegex(series.SeriesPreparationError, 'treatment-identity-mismatch'):
                self.build()

    def test_unsafe_or_reviewer_files_cannot_enter_participant_map(self):
        for name in ('../escape', 'REVIEWER.json', '/absolute'):
            full = build_packet(self.root, 'test-case', 'full')
            progressive = build_packet(self.root, 'test-case', 'progressive')
            full[0][name] = b'not participant input'
            with self.subTest(name=name), patch.object(series, 'build_packet', side_effect=[full, progressive]):
                with self.assertRaises(series.SeriesPreparationError):
                    self.build()

    def test_invalid_config_fields_version_and_unbounded_values_rejected(self):
        for change in ({'format_version': True}, {'kind': 'unknown'}, {'extra': 1}):
            config = copy.deepcopy(self.config); config.update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.build(config)
        for invalid in ({}, [], None, {'x': 'x' * 1_048_577}):
            with self.assertRaises(ValueError):
                series.build_series(self.root, 'test-case', invalid)

    def test_unknown_host_or_source_identity_is_not_guessed(self):
        for key in self.config['identity']:
            config = copy.deepcopy(self.config); config['identity'][key] = None
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.build(config)

    def test_invalid_repetition_ids_and_required_checks_rejected(self):
        for key, values in [('pair_ids', [[], ['same', 'same'], ['x'] * 129, [None]]),
                            ('required_checks', [[], ['same', 'same'], [True]])]:
            for value in values:
                config = copy.deepcopy(self.config); config[key] = value
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    self.build(config)

    def test_provider_fixture_cannot_authorize_runtime_calls(self):
        self.case.update(route='jev', provider_authorized=True, max_provider_calls=1)
        self.save_case()
        with self.assertRaises(ValueError):
            self.build()

    def test_optional_scripts_are_copied_without_execution(self):
        (self.skill / 'scripts').mkdir()
        code = b'raise RuntimeError("HELPER_MUST_NOT_EXECUTE")\n'
        (self.skill / 'scripts/helper.py').write_bytes(code)
        self.bundle['format_version'] = 2
        self.bundle['files'].append('scripts/helper.py')
        self.bundle['optional_scripts'] = [{'path': 'scripts/helper.py',
            'execution': 'explicit-invocation-only', 'fallback': 'Read source manually.'}]
        (self.skill / 'bundle.json').write_bytes(encode(self.bundle))
        files, _ = self.build()
        self.assertEqual(files['treatments/full/participant/guidance/scripts/helper.py'], code)
        self.assertIn(b'Do not execute bundled helpers', files['treatments/progressive/participant/TASK.md'])

    def test_deterministic_output_and_input_preservation(self):
        before = copy.deepcopy(self.config)
        a, one = self.build()
        b, two = self.build(dict(reversed(list(self.config.items()))))
        self.assertEqual(a, b); self.assertEqual(one, two)
        one['artifacts'].clear()
        self.assertEqual(self.config, before)
        self.assertTrue(two['artifacts'])

    def test_preparation_never_launches_process_or_network(self):
        with patch.object(subprocess, 'run', side_effect=AssertionError('no process')), \
             patch.object(socket, 'socket', side_effect=AssertionError('no network')):
            _, report = self.build()
        self.assertEqual(report['observed_sessions'], 0)
        self.assertEqual(report['model_execution'], 'not-performed')
        for field in ('host_identity_verified', 'host_isolation_verified', 'outcome_verified',
                      'token_savings_verified', 'plan_preregistration_authenticated'):
            self.assertIs(report[field], False)

    def test_complete_output_inventory_and_private_file_modes(self):
        output = self.parent / 'prepared'
        result = series.prepare_series(self.root, 'test-case', self.config, output)
        report = json.loads((output / 'REVIEWER.json').read_bytes())
        self.assertEqual(result['plan_sha256'], report['plan_sha256'])
        actual = {p.relative_to(output).as_posix(): p.read_bytes()
                  for p in output.rglob('*') if p.is_file() and p.name != 'REVIEWER.json'}
        self.assertEqual(series.identities(actual), report['artifacts'])
        if os.name == 'posix':
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE((output / 'review/plan.json').stat().st_mode), 0o600)

    def test_existing_output_is_never_overwritten(self):
        output = self.parent / 'existing'; output.mkdir()
        sentinel = output / 'keep'; sentinel.write_bytes(b'unchanged')
        with self.assertRaisesRegex(ValueError, 'output-already-exists'):
            series.prepare_series(self.root, 'test-case', self.config, output)
        self.assertEqual(sentinel.read_bytes(), b'unchanged')
        self.assertEqual(len(list(output.iterdir())), 1)

    def test_checkout_traversal_and_linked_paths_are_refused(self):
        link = self.parent / 'linked'; link.symlink_to(self.parent, target_is_directory=True)
        for output in (self.root / 'new', link / 'new', self.parent / '..' / 'new'):
            with self.subTest(output=output), self.assertRaises(ValueError):
                series.prepare_series(self.root, 'test-case', self.config, output)
        self.assertFalse((self.root / 'new').exists())

    def test_missing_guide_creates_no_output(self):
        (self.skill / 'references/guide.md').unlink()
        output = self.parent / 'new'
        with self.assertRaises(ValueError):
            series.prepare_series(self.root, 'test-case', self.config, output)
        self.assertFalse(output.exists())

    def test_budget_failure_creates_no_output_or_partial_plan(self):
        output = self.parent / 'new'
        with patch.object(series, 'MAX_OUTPUT', 1), self.assertRaises(ValueError):
            series.prepare_series(self.root, 'test-case', self.config, output)
        self.assertFalse(output.exists())

    def test_io_failure_keeps_partial_output_without_completion_marker(self):
        output = self.parent / 'partial'; original = os.open; calls = 0
        def fail_second(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError('synthetic interrupted write')
            return original(*args, **kwargs)
        with patch.object(series.os, 'open', side_effect=fail_second), self.assertRaises(OSError):
            series.prepare_series(self.root, 'test-case', self.config, output)
        self.assertTrue(output.exists())
        self.assertFalse((output / 'REVIEWER.json').exists())
        kept = {p: p.read_bytes() for p in output.rglob('*') if p.is_file()}
        self.assertTrue(kept)
        with self.assertRaises(ValueError):
            series.prepare_series(self.root, 'test-case', self.config, output)
        self.assertEqual(kept, {p: p.read_bytes() for p in output.rglob('*') if p.is_file()})

    def test_real_file_command_prepares_existing_case_and_evaluator_reports_missing_runs(self):
        config = self.parent / 'config.json'; config.write_bytes(encode(self.config))
        output = self.parent / 'command-output'
        command = [sys.executable, str(HERE / 'prepare_guidance_series.py'), '--case', 'supported-claim',
                   '--config', str(config), '--output', str(output)]
        result = subprocess.run(command, capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        pin = (output / 'review/plan.sha256').read_text().strip()
        checked = subprocess.run([sys.executable, str(HERE / 'guidance_series.py'),
            str(output / 'review/plan.json'), str(output / 'review/pairs.json'),
            '--expected-plan-sha256', pin], capture_output=True, timeout=20)
        self.assertEqual(checked.returncode, 1, checked.stderr)
        self.assertEqual(json.loads(checked.stdout)['status'], 'incomplete-series')
        self.assertEqual(subprocess.run(command, capture_output=True, timeout=20).returncode, 2)

    def test_command_rejects_duplicate_json_and_does_not_echo_contents(self):
        config = self.parent / 'bad.json'
        config.write_bytes(b'{"secret":"DO_NOT_ECHO", "secret":2}')
        output = self.parent / 'no-output'
        result = subprocess.run([sys.executable, str(HERE / 'prepare_guidance_series.py'),
            '--case', 'supported-claim', '--config', str(config), '--output', str(output)],
            capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertNotIn(b'DO_NOT_ECHO', result.stdout + result.stderr)
        self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
