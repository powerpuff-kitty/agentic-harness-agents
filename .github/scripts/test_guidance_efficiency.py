"""Synthetic rubric/grader regressions; never a model-behaviour pass rate."""
import copy
import json
from pathlib import Path
import unittest

from guidance_eval import digest, evaluate, submitted_tokens, validate_case

ROOT = Path(__file__).resolve().parents[2]


def cases():
    fixture = json.loads((ROOT / 'evals/guidance-efficiency.json').read_text(encoding='utf-8'))
    assert fixture['format_version'] == 1
    assert fixture['evidence_kind'] == 'synthetic-rubric'
    return fixture['cases']


def synthetic_observation(case):
    return {'case_id': case['id'], 'route': case['route'], 'outcome': case['outcome'],
            'sources': {key: digest(value) for key, value in case['sources'].items()},
            'provider_calls': 1 if case['route'] == 'jev' else 0, 'confidence': None,
            'policy_promoted': False, 'verification_claimed': False,
            'verification_observed': False}


class GuidanceEfficiency(unittest.TestCase):
    def test_fixture_coverage_and_grader_baselines(self):
        fixtures = cases()
        self.assertGreaterEqual(len(fixtures), 10)
        self.assertEqual(len(fixtures), len({case['id'] for case in fixtures}))
        for case in fixtures:
            with self.subTest(case=case['id']):
                validate_case(case)
                self.assertTrue((ROOT / 'skills' / case['skill'] / 'SKILL.md').is_file())
                result = evaluate(case, synthetic_observation(case))
                self.assertTrue(result['passed'], result)
                self.assertEqual(result['model_execution'], 'not-performed')
                self.assertFalse(result['trace_authenticated'])

    def test_omitted_required_evidence_cannot_pass(self):
        case = cases()[0]
        observation = synthetic_observation(case)
        observation['sources'].pop(case['required'][0])
        self.assertIn('required-evidence-missing', evaluate(case, observation)['failures'])

    def test_stale_source_cannot_pass(self):
        case = cases()[0]
        observation = synthetic_observation(case)
        observation['sources'][case['required'][0]] = digest('changed source')
        self.assertIn('stale-or-invented-source', evaluate(case, observation)['failures'])

    def test_missing_observation_fields_fail_closed(self):
        case = cases()[0]
        for field in synthetic_observation(case):
            observation = synthetic_observation(case)
            del observation[field]
            self.assertFalse(evaluate(case, observation)['passed'], field)
        self.assertFalse(evaluate(case, None)['passed'])

    def test_wrong_route_outcome_and_case_are_detected(self):
        case = cases()[0]
        for field, value in [('route', 'unknown'), ('outcome', 'invented'), ('case_id', 'other')]:
            observation = synthetic_observation(case)
            observation[field] = value
            self.assertFalse(evaluate(case, observation)['passed'])

    def test_no_automatic_provider_calls(self):
        case = cases()[0]
        for value in [1, -1, True, '0']:
            observation = synthetic_observation(case)
            observation['provider_calls'] = value
            self.assertFalse(evaluate(case, observation)['passed'])

    def test_current_agent_does_not_fabricate_confidence(self):
        case = cases()[0]
        observation = synthetic_observation(case)
        observation['confidence'] = 0.99
        self.assertIn('unsupported-confidence', evaluate(case, observation)['failures'])

    def test_no_policy_promotion_or_unexecuted_pass(self):
        case = cases()[0]
        for field in ['policy_promoted', 'verification_claimed']:
            observation = synthetic_observation(case)
            observation[field] = True
            self.assertFalse(evaluate(case, observation)['passed'])
        observation = synthetic_observation(case)
        observation['verification_observed'] = None
        self.assertFalse(evaluate(case, observation)['passed'])

    def test_declared_jev_output_requires_observed_call(self):
        case = next(case for case in cases() if case['route'] == 'jev')
        observation = synthetic_observation(case)
        observation['provider_calls'] = 0
        self.assertIn('jev-output-without-call', evaluate(case, observation)['failures'])

    def test_invalid_cases_are_rejected(self):
        case = cases()[0]
        for field, value in [('required', ['absent']), ('max_provider_calls', True),
                             ('provider_authorized', None), ('route', 'jev')]:
            invalid = copy.deepcopy(case)
            invalid[field] = value
            with self.assertRaises(ValueError):
                validate_case(invalid)

    def test_usage_includes_auxiliary_calls_and_retries_without_double_counting_tools(self):
        self.assertEqual(submitted_tokens([
            {'input_tokens': 100, 'output_tokens': 20},
            {'input_tokens': 30, 'output_tokens': 5},
        ]), 155)
        self.assertIsNone(submitted_tokens([]))
        self.assertIsNone(submitted_tokens([{'input_tokens': 100, 'output_tokens': None}]))
        with self.assertRaises(ValueError):
            submitted_tokens([{'input_tokens': True, 'output_tokens': 2}])

    def test_skill_local_references_are_present_and_entrypoints_bounded(self):
        for name, reference in [('decision-intelligence', 'decision-guide.md'),
                                ('agentic-improvement', 'efficiency.md')]:
            folder = ROOT / 'skills' / name
            text = (folder / 'SKILL.md').read_text(encoding='utf-8')
            self.assertLessEqual(len(text.encode('utf-8')), 6000)
            self.assertIn('references/' + reference, text)
            self.assertTrue((folder / 'references' / reference).is_file())


if __name__ == '__main__':
    unittest.main()
