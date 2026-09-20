"""Synthetic repeated-record tests, not real host or provider evaluations."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from guidance_comparison import compare, fingerprint
from guidance_series import MAX_BYTES, MAX_TOKEN_COUNT, summarize

HERE = Path(__file__).resolve().parent


def digest(value):
    return 'sha256:' + hashlib.sha256(value.encode()).hexdigest()


def reference(value):
    return {'reference': 'fixture://' + value, 'sha256': digest(value)}


def fixtures(count=3, recorded=False):
    spec = {'case': {'id': 'repeated-guidance', 'prompt': 'Assess the supplied boundary.',
                    'skill': 'decision-intelligence', 'route': 'current-agent', 'outcome': 'supported',
                    'sources': {'policy': 'Views call services.', 'source': 'View calls service.'},
                    'required': ['policy', 'source'], 'provider_authorized': False, 'max_provider_calls': 0},
            'required_checks': ['acceptance']}
    plan = {'format_version': 1, 'kind': 'guidance-series-plan', 'spec': spec,
            'evidence_kind': 'recorded-session' if recorded else 'synthetic',
            'identity': {'source_snapshot': digest('source'), 'policy_snapshot': digest('policy'),
                         'checks_snapshot': digest('checks'), 'host': 'synthetic-host',
                         'model': 'synthetic-model', 'settings_snapshot': digest('settings')},
            'treatments': {role: {'name': role, 'sha256': digest(role)} for role in ('baseline', 'candidate')},
            'pair_ids': ['repeat-' + str(i + 1) for i in range(count)]}
    pairs = []
    for pair_id in plan['pair_ids']:
        pair = {'id': pair_id}
        for role in ('baseline', 'candidate'):
            run_id = pair_id + '-' + role
            pair[role] = {'format_version': 1, 'kind': 'guidance-trial-record',
                          'evidence_kind': plan['evidence_kind'], 'spec_digest': fingerprint(spec),
                          'identity': copy.deepcopy(plan['identity']),
                          'treatment': copy.deepcopy(plan['treatments'][role]),
                          'trace': reference(run_id + '-trace') if recorded else None,
                          'observation': {'case_id': spec['case']['id'], 'route': 'current-agent',
                                          'outcome': 'supported', 'sources': {k: digest(v) for k, v in spec['case']['sources'].items()},
                                          'provider_calls': 0, 'confidence': None, 'policy_promoted': False,
                                          'verification_claimed': False, 'verification_observed': False},
                          'checks': {'acceptance': {'status': 'passed', 'evidence': reference(run_id + '-check')}},
                          'usage': {'complete': True, 'basis': 'observed-submitted-tokens',
                                    'evidence': reference(run_id + '-usage'),
                                    'calls': [{'id': run_id + '-call', 'input_tokens': 100 if role == 'baseline' else 50,
                                               'output_tokens': 0}]}}
        pairs.append(pair)
    return plan, pairs


class RepeatedGuidance(unittest.TestCase):
    def setUp(self):
        self.plan, self.pairs = fixtures()
        self.pin = fingerprint(self.plan)

    def run_summary(self):
        return summarize(self.plan, self.pairs, expected_plan_sha256=self.pin)

    def test_complete_series_describes_all_repetitions_and_sample_variation(self):
        self.pairs[2]['candidate']['usage']['calls'][0]['input_tokens'] = 80
        result = self.run_summary()
        self.assertEqual(result['status'], 'descriptive-comparison')
        self.assertEqual(result['planned_pairs'], 3)
        self.assertEqual(result['acceptance']['candidate'], {'planned': 3, 'passed': 3, 'failed': 0, 'not-assessed': 0})
        tokens = result['submitted_tokens']
        self.assertEqual(tokens['baseline']['total'], 300)
        self.assertEqual(tokens['candidate']['total'], 180)
        self.assertEqual(tokens['paired_reduction']['mean'], 40)
        self.assertEqual(tokens['paired_reduction']['median'], 50)
        self.assertAlmostEqual(tokens['paired_reduction']['sample_standard_deviation'], 17.320508075688775)
        self.assertEqual(tokens['total_reduction_fraction'], .4)

    def test_failed_expensive_run_is_not_dropped_from_cost(self):
        failed = self.pairs[2]['candidate']
        failed['checks']['acceptance']['status'] = 'failed'
        failed['usage']['calls'][0]['input_tokens'] = 300
        result = self.run_summary()
        self.assertEqual(result['status'], 'acceptance-not-satisfied')
        self.assertEqual(result['acceptance']['candidate']['failed'], 1)
        self.assertEqual(result['submitted_tokens']['candidate']['total'], 400)
        self.assertEqual(result['submitted_tokens']['paired_reduction']['total'], -100)
        self.assertTrue(result['submitted_tokens']['includes_failed_acceptance'])
        self.assertFalse(result['optimisation_verified'])

    def test_missing_pair_retains_planned_denominator_and_no_subset_savings(self):
        self.pairs.pop()
        result = self.run_summary()
        self.assertEqual(result['status'], 'incomplete-series')
        self.assertEqual(result['planned_pairs'], 3)
        self.assertEqual(result['supplied_pairs'], 2)
        self.assertEqual(result['missing_records'], 2)
        self.assertEqual(result['acceptance']['candidate'], {'planned': 3, 'passed': 2, 'failed': 0, 'not-assessed': 1})
        self.assertIsNone(result['submitted_tokens'])
        self.assertEqual(result['pairs'][-1]['id'], 'repeat-3')

    def test_null_record_and_empty_series_remain_missing_not_zero(self):
        self.pairs[0]['candidate'] = None
        self.assertEqual(self.run_summary()['missing_records'], 1)
        self.pairs = []
        result = self.run_summary()
        self.assertEqual(result['missing_records'], 6)
        self.assertIsNone(result['submitted_tokens'])

    def test_plan_cannot_shrink_or_change_after_pin(self):
        for change in ('ids', 'spec', 'treatment'):
            plan = copy.deepcopy(self.plan)
            if change == 'ids':
                plan['pair_ids'].pop()
            elif change == 'spec':
                plan['spec']['required_checks'] = ['easier-check']
            else:
                plan['treatments']['candidate']['sha256'] = digest('changed')
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, 'plan digest mismatch'):
                summarize(plan, self.pairs, expected_plan_sha256=self.pin)

    def test_unplanned_or_duplicate_pair_rejected_not_silently_filtered(self):
        self.pairs.append(copy.deepcopy(self.pairs[0]))
        with self.assertRaisesRegex(ValueError, 'duplicate pair'):
            self.run_summary()
        self.pairs[-1]['id'] = 'extra-repeat'
        with self.assertRaisesRegex(ValueError, 'unplanned pair'):
            self.run_summary()

    def test_changed_model_settings_source_and_treatment_prevent_pooling(self):
        for key in ('model', 'settings_snapshot', 'source_snapshot', 'policy_snapshot', 'checks_snapshot', 'host'):
            plan, pairs = fixtures()
            for role in ('baseline', 'candidate'):
                pairs[1][role]['identity'][key] = 'changed' if key in ('model', 'host') else digest('changed')
            result = summarize(plan, pairs, expected_plan_sha256=fingerprint(plan))
            self.assertEqual(result['status'], 'not-comparable', key)
            self.assertIsNone(result['submitted_tokens'])
        self.pairs[0]['candidate']['treatment']['sha256'] = digest('different')
        self.assertEqual(self.run_summary()['status'], 'not-comparable')

    def test_mixed_evidence_and_unknown_record_identity_remain_unassessed(self):
        self.pairs[0]['candidate']['evidence_kind'] = 'recorded-session'
        self.assertEqual(self.run_summary()['status'], 'not-comparable')
        self.pairs[0]['candidate']['identity']['model'] = None
        result = self.run_summary()
        self.assertEqual(result['acceptance']['candidate']['not-assessed'], 1)
        self.assertIsNone(result['submitted_tokens'])

    def test_reused_record_or_trace_cannot_inflate_repetition_count(self):
        self.pairs[1]['candidate'] = copy.deepcopy(self.pairs[0]['candidate'])
        result = self.run_summary()
        self.assertEqual(result['status'], 'not-comparable')
        for row in result['pairs'][:2]:
            self.assertIn('reused-record', row['candidate']['reasons'])
        plan, pairs = fixtures(recorded=True)
        pairs[1]['candidate']['trace']['sha256'] = pairs[0]['candidate']['trace']['sha256']
        result = summarize(plan, pairs, expected_plan_sha256=fingerprint(plan))
        self.assertEqual(result['status'], 'not-comparable')
        self.assertIn('reused-trace', result['pairs'][0]['candidate']['reasons'])

    def test_shared_usage_evidence_blocks_series_but_shared_check_log_is_allowed(self):
        plan, pairs = fixtures(recorded=True)
        pairs[1]['candidate']['checks'] = copy.deepcopy(pairs[0]['candidate']['checks'])
        self.assertEqual(summarize(plan, pairs, expected_plan_sha256=fingerprint(plan))['status'], 'descriptive-comparison')
        pairs[1]['candidate']['usage']['evidence']['sha256'] = pairs[0]['candidate']['usage']['evidence']['sha256']
        result = summarize(plan, pairs, expected_plan_sha256=fingerprint(plan))
        self.assertEqual(result['status'], 'not-comparable')
        self.assertIn('reused-usage', result['pairs'][1]['candidate']['reasons'])

    def test_missing_trace_in_recorded_session_prevents_cost_comparison(self):
        plan, pairs = fixtures(recorded=True)
        pairs[0]['candidate']['trace'] = None
        result = summarize(plan, pairs, expected_plan_sha256=fingerprint(plan))
        self.assertEqual(result['status'], 'not-comparable')
        self.assertIsNone(result['submitted_tokens'])

    def test_unknown_or_incomplete_usage_blocks_aggregate_without_hiding_acceptance(self):
        for mutate in (lambda r: r['usage'].update(complete=False),
                       lambda r: r['usage'].update(basis='unknown'),
                       lambda r: r['usage'].update(evidence=None),
                       lambda r: r['usage']['calls'][0].update(output_tokens=None),
                       lambda r: r['usage'].update(calls=[])):
            plan, pairs = fixtures()
            mutate(pairs[1]['candidate'])
            result = summarize(plan, pairs, expected_plan_sha256=fingerprint(plan))
            self.assertEqual(result['status'], 'usage-unavailable')
            self.assertEqual(result['acceptance']['candidate']['passed'], 3)
            self.assertIsNone(result['submitted_tokens'])

    def test_retries_and_auxiliary_calls_erase_apparent_reduction(self):
        self.pairs[0]['candidate']['usage']['calls'].append({'id': 'retry-or-auxiliary', 'input_tokens': 200, 'output_tokens': 30})
        result = self.run_summary()
        self.assertEqual(result['submitted_tokens']['candidate']['total'], 380)
        self.assertEqual(result['submitted_tokens']['paired_reduction']['total'], -80)

    def test_weighted_total_fraction_is_not_average_of_percentages(self):
        plan, pairs = fixtures(2)
        pairs[1]['baseline']['usage']['calls'][0]['input_tokens'] = 1000
        pairs[1]['candidate']['usage']['calls'][0]['input_tokens'] = 990
        result = summarize(plan, pairs, expected_plan_sha256=fingerprint(plan))
        self.assertAlmostEqual(result['submitted_tokens']['total_reduction_fraction'], 60 / 1100)
        self.assertNotEqual(result['submitted_tokens']['total_reduction_fraction'], (.5 + .01) / 2)

    def test_one_pair_has_unknown_sample_deviation_and_zero_control_no_fraction(self):
        plan, pairs = fixtures(1)
        for role in ('baseline', 'candidate'):
            pairs[0][role]['usage']['calls'][0]['input_tokens'] = 0
        result = summarize(plan, pairs, expected_plan_sha256=fingerprint(plan))
        self.assertIsNone(result['submitted_tokens']['paired_reduction']['sample_standard_deviation'])
        self.assertIsNone(result['submitted_tokens']['total_reduction_fraction'])

    def test_wrong_outcome_missing_policy_and_unrun_check_remain_failures(self):
        self.pairs[0]['candidate']['observation']['outcome'] = 'wrong'
        del self.pairs[1]['candidate']['observation']['sources']['policy']
        self.pairs[2]['baseline']['checks']['acceptance']['status'] = 'not-run'
        result = self.run_summary()
        self.assertEqual(result['acceptance']['candidate']['failed'], 2)
        self.assertEqual(result['acceptance']['baseline']['failed'], 1)
        self.assertEqual(result['status'], 'acceptance-not-satisfied')
        self.assertIsNotNone(result['submitted_tokens'])

    def test_extra_failed_check_and_unverified_check_evidence_stay_failed(self):
        self.pairs[0]['candidate']['checks']['extra'] = {'status': 'failed', 'evidence': reference('extra')}
        self.pairs[1]['candidate']['checks']['acceptance']['evidence'] = None
        self.assertEqual(self.run_summary()['acceptance']['candidate']['failed'], 2)

    def test_synthetic_and_recorded_reports_never_authenticate_or_certify(self):
        for recorded in (False, True):
            plan, pairs = fixtures(recorded=recorded)
            result = summarize(plan, pairs, expected_plan_sha256=fingerprint(plan))
            self.assertEqual(result['model_execution'], 'not-performed')
            for key in ('trace_authenticated', 'plan_preregistration_authenticated', 'independence_verified',
                        'model_quality_verified', 'billing_savings_verified', 'optimisation_verified'):
                self.assertIs(result[key], False)

    def test_no_source_reads_network_or_execution_and_no_input_mutation(self):
        before = copy.deepcopy((self.plan, self.pairs))
        with patch('builtins.open', side_effect=AssertionError('no reads')), \
             patch.object(Path, 'open', side_effect=AssertionError('no reads')), \
             patch('socket.socket', side_effect=AssertionError('no network')), \
             patch('subprocess.run', side_effect=AssertionError('no execution')):
            result = self.run_summary()
        result['pairs'][0]['candidate']['reasons'].append('changed')
        self.assertEqual((self.plan, self.pairs), before)

    def test_each_complete_pair_reuses_existing_comparator_unchanged(self):
        result = self.run_summary()
        for row, pair in zip(result['pairs'], self.pairs):
            expected = compare(self.plan['spec'], pair['baseline'], pair['candidate'])
            self.assertEqual(row['pair_comparison'], {'status': expected['status'], 'reasons': expected['reasons']})

    def test_reordered_input_keeps_plan_order_and_statistics(self):
        first = self.run_summary()
        self.pairs.reverse()
        second = self.run_summary()
        self.assertEqual(first['pairs'], second['pairs'])
        self.assertEqual(first['submitted_tokens'], second['submitted_tokens'])
        self.assertNotEqual(first['pairs_digest'], second['pairs_digest'])

    def test_bounds_malformed_records_and_invalid_token_counts_fail(self):
        self.pairs[0]['candidate']['usage']['calls'][0]['input_tokens'] = MAX_TOKEN_COUNT + 1
        with self.assertRaisesRegex(ValueError, 'token count limit'):
            self.run_summary()
        for value in (None, {}, [None], 'x' * (MAX_BYTES + 1)):
            with self.subTest(value=type(value)), self.assertRaises((TypeError, ValueError)):
                summarize(self.plan, value, expected_plan_sha256=self.pin)
        self.pairs = [{'id': 'repeat-1', 'baseline': {}, 'candidate': None}]
        with self.assertRaises(ValueError):
            self.run_summary()

    def test_invalid_plan_pin_version_identity_and_duplicate_ids_rejected(self):
        with self.assertRaisesRegex(ValueError, 'reviewed plan digest required'):
            summarize(self.plan, self.pairs, expected_plan_sha256='')
        for key, value in (('format_version', True), ('pair_ids', ['x', 'x']), ('pair_ids', []),
                           ('evidence_kind', []), ('identity', {}), ('treatments', {})):
            plan = copy.deepcopy(self.plan)
            plan[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                summarize(plan, self.pairs, expected_plan_sha256=fingerprint(plan))

    def test_nested_cycle_and_non_json_values_are_bounded(self):
        cycle = []
        cycle.append(cycle)
        for value in (cycle, [{'id': {'bad'}}], [{'x': float('nan')}], [{'x': '\ud800'}]):
            with self.assertRaises((ValueError, UnicodeError)):
                summarize(self.plan, value, expected_plan_sha256=self.pin)

    def test_retained_worked_example_keeps_expensive_failure(self):
        folder = HERE.parents[1] / 'evals/fixtures/guidance-series'
        plan = json.loads((folder / 'plan.json').read_text())
        pairs = json.loads((folder / 'pairs.json').read_text())
        pin = (folder / 'plan-fingerprint.txt').read_text().strip()
        result = summarize(plan, pairs, expected_plan_sha256=pin)
        self.assertEqual(result['evidence_kind'], 'synthetic')
        self.assertEqual(result['status'], 'acceptance-not-satisfied')
        self.assertEqual(result['acceptance']['candidate']['failed'], 1)
        self.assertEqual(result['submitted_tokens']['paired_reduction']['total'], -100)

    def test_jev_observation_without_provider_call_cannot_pass(self):
        self.plan['spec']['case'].update(route='jev', provider_authorized=True, max_provider_calls=1)
        self.pin = fingerprint(self.plan)
        for pair in self.pairs:
            for role in ('baseline', 'candidate'):
                pair[role]['spec_digest'] = fingerprint(self.plan['spec'])
                pair[role]['observation'].update(route='jev', provider_calls=1)
        self.pairs[1]['candidate']['observation']['provider_calls'] = 0
        result = self.run_summary()
        self.assertEqual(result['status'], 'acceptance-not-satisfied')
        self.assertIn('jev-output-without-call', result['pairs'][1]['candidate']['reasons'])
        self.assertEqual(result['model_execution'], 'not-performed')

    def test_named_file_command_output_and_exit_codes(self):
        with tempfile.TemporaryDirectory() as folder:
            plan_file, pairs_file = (Path(folder) / name for name in ('plan.json', 'pairs.json'))
            plan_file.write_text(json.dumps(self.plan))
            pairs_file.write_text(json.dumps(self.pairs))
            command = [sys.executable, str(HERE / 'guidance_series.py'), str(plan_file), str(pairs_file),
                       '--expected-plan-sha256', self.pin]
            def invoke():
                return subprocess.run(command, capture_output=True, text=True, timeout=10)
            result = invoke()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), self.run_summary())
            pairs_file.write_text('[]')
            result = invoke()
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout)['missing_records'], 6)
            pairs_file.write_text('{"private":"DO_NOT_ECHO","private":1}')
            result = invoke()
            self.assertEqual(result.returncode, 2)
            self.assertNotIn('DO_NOT_ECHO', result.stdout + result.stderr)

    def test_symlink_input_rejected_and_command_does_not_rewrite_inputs(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            plan_file, pairs_file = path / 'plan.json', path / 'pairs.json'
            plan_file.write_text(json.dumps(self.plan))
            pairs_file.write_text(json.dumps(self.pairs))
            before = (plan_file.read_bytes(), pairs_file.read_bytes())
            link = path / 'link.json'
            link.symlink_to(plan_file)
            result = subprocess.run([sys.executable, str(HERE / 'guidance_series.py'), str(link), str(pairs_file),
                                     '--expected-plan-sha256', self.pin], capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(before, (plan_file.read_bytes(), pairs_file.read_bytes()))


if __name__ == '__main__':
    unittest.main()
