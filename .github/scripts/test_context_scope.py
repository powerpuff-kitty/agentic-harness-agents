"""Synthetic scope/counterevidence regressions, not model execution or pass rates."""
import copy
import json
from pathlib import Path
import unittest

from guidance_eval import digest, evaluate, validate_case

ROOT = Path(__file__).resolve().parents[2]


def cases():
    fixture = json.loads((ROOT / 'evals/context-scope.json').read_text(encoding='utf-8'))
    if fixture['format_version'] != 1 or fixture['evidence_kind'] != 'synthetic-rubric':
        raise ValueError('scope cases must remain labelled synthetic')
    return fixture['cases']


def synthetic(case):
    # Construct only a grader control, never a supposed recorded model response.
    return {'case_id': case['id'], 'route': case['route'], 'outcome': case['outcome'],
            'sources': {key: digest(value) for key, value in case['sources'].items()},
            'provider_calls': 0, 'confidence': None, 'policy_promoted': False,
            'verification_claimed': False, 'verification_observed': False}


class ContextScope(unittest.TestCase):
    def test_controls_validate_without_claiming_execution(self):
        fixtures = cases()
        self.assertEqual(len(fixtures), 4)
        self.assertEqual(len({case['id'] for case in fixtures}), 4)
        for case in fixtures:
            validate_case(case)
            result = evaluate(case, synthetic(case))
            self.assertTrue(result['passed'])
            self.assertEqual(result['model_execution'], 'not-performed')
            self.assertFalse(result['trace_authenticated'])
            self.assertTrue((ROOT / 'skills' / case['skill'] / 'SKILL.md').is_file())

    def test_every_required_source_is_individually_required(self):
        for case in cases():
            for source in case['required']:
                with self.subTest(case=case['id'], source=source):
                    observation = synthetic(case)
                    del observation['sources'][source]
                    self.assertIn('required-evidence-missing', evaluate(case, observation)['failures'])

    def test_policy_or_diagnostic_source_changes_invalidate_observations(self):
        for case in cases():
            for source in case['required']:
                changed = copy.deepcopy(case)
                changed['sources'][source] += ' Changed input.'
                with self.subTest(case=case['id'], source=source):
                    self.assertIn('stale-or-invented-source',
                                  evaluate(changed, synthetic(case))['failures'])

    def test_compacted_output_cannot_claim_unobserved_verification(self):
        case = cases()[1]
        observation = synthetic(case)
        observation['verification_claimed'] = True
        self.assertIn('unobserved-verification', evaluate(case, observation)['failures'])

    def test_scope_compaction_cannot_promote_policy(self):
        case = cases()[0]
        observation = synthetic(case)
        observation['policy_promoted'] = True
        self.assertIn('policy-promotion', evaluate(case, observation)['failures'])

    def test_missing_provider_cannot_be_relabelled_current_agent_or_jev(self):
        case = cases()[3]
        for route in ('current-agent', 'jev'):
            observation = synthetic(case)
            observation['route'] = route
            self.assertIn('wrong-route', evaluate(case, observation)['failures'])
        observation = synthetic(case)
        observation['confidence'] = 0.95
        self.assertIn('unsupported-confidence', evaluate(case, observation)['failures'])


if __name__ == '__main__':
    unittest.main()
