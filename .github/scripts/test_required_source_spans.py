"""Required-span and real helper-workflow regressions; not model-performance trials."""
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / 'skills/agentic-improvement/scripts'
HELPER = SCRIPTS / 'extract_context.py'
extractor = types.ModuleType('tested_required_source_spans')
extractor.__file__ = str(HELPER)
exec(compile(HELPER.read_bytes(), str(HELPER), 'exec'), extractor.__dict__)


class RequiredSourceSpans(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.raw = b'claim\ncontrary evidence\nqualification\noptional example\n'
        (self.root / 'source.txt').write_bytes(self.raw)

    def span(self, start=1, end=3, path='source.txt', raw=None):
        return [path, start, end, extractor.evidence.sha(self.raw if raw is None else raw)]

    def run_helper(self, spans, required=None, budget=65536, helper=HELPER):
        command = [sys.executable, str(helper), '--root', str(self.root), '--budget-bytes', str(budget)]
        for option, values in (('--span', spans), ('--require-span', required or [])):
            for span in values:
                command += [option, *map(str, span)]
        return subprocess.run(command, capture_output=True, timeout=10)

    def guarded(self, spans, required, budget=65536):
        return extractor.extract(self.root, spans, budget, required_spans=required)

    def test_complete_required_evidence_is_emitted_without_claiming_semantic_sufficiency(self):
        result = self.guarded([self.span(1, 4)], [self.span()])
        self.assertEqual(result['required_evidence']['lines'], 3)
        self.assertTrue(result['required_evidence']['emitted'])
        self.assertFalse(result['required_evidence']['requirements_authenticated'])
        self.assertIsNone(result['limits']['evidence_sufficient'])
        self.assertFalse(result['limits']['checks_verified'])
        self.assertIsNone(result['limits']['model_tokens'])

    def test_one_line_hole_cannot_hide_required_counterevidence(self):
        with patch.object(extractor.evidence, 'read_text', side_effect=AssertionError('target read')):
            with self.assertRaises(extractor.RequiredEvidenceError):
                self.guarded([self.span(1, 1), self.span(3, 3)], [self.span()])

    def test_missing_required_path_does_not_expand_reads(self):
        required = self.span(1, 1, 'unselected.txt', b'never read')
        with patch.object(extractor.evidence, 'read_text', side_effect=AssertionError('target read')):
            with self.assertRaises(extractor.RequiredEvidenceError):
                self.guarded([self.span()], [required])

    def test_required_pin_conflict_is_rejected_before_reads(self):
        with patch.object(extractor.evidence, 'read_text', side_effect=AssertionError('target read')):
            with self.assertRaises(extractor.RequiredEvidenceError):
                self.guarded([self.span()], [self.span(raw=b'other source')])

    def test_identical_content_at_different_paths_does_not_supply_required_identity(self):
        (self.root / 'copy.txt').write_bytes(self.raw)
        with self.assertRaises(extractor.RequiredEvidenceError):
            self.guarded([self.span(path='copy.txt')], [self.span()])

    def test_case_only_different_requirement_is_not_treated_as_same_path(self):
        with self.assertRaises(extractor.RequiredEvidenceError):
            self.guarded([self.span()], [self.span(path='SOURCE.txt')])

    def test_adjacent_and_overlapping_selected_ranges_cover_the_requirement(self):
        for selected in ([self.span(1, 1), self.span(2, 3)],
                         [self.span(1, 2), self.span(2, 3)]):
            result = self.guarded(selected, [self.span()])
            self.assertEqual(len(result['files'][0]['excerpts']), 1)
            self.assertTrue(result['required_evidence']['emitted'])

    def test_disjoint_required_ranges_do_not_require_the_gap(self):
        result = self.guarded([self.span(1, 1), self.span(3, 3)],
                              [self.span(1, 1), self.span(3, 3)])
        self.assertEqual(result['required_evidence']['lines'], 2)
        self.assertEqual(result['required_evidence']['ranges'], 2)
        self.assertEqual(result['files'][0]['omitted_lines'], 2)
        self.assertIsNone(result['limits']['evidence_sufficient'])

    def test_normalized_declarations_have_stable_identity_and_counts(self):
        first = self.guarded([self.span()], [self.span(1, 2), self.span(2, 3), self.span(1, 2)])
        second = self.guarded([self.span()], [self.span()])
        self.assertEqual(first, second)
        self.assertEqual(first['required_evidence']['ranges'], 1)
        self.assertEqual(first['required_evidence']['lines'], 3)

    def test_changed_required_coverage_changes_its_identity(self):
        one = self.guarded([self.span()], [self.span(1, 1)])
        two = self.guarded([self.span()], [self.span(2, 2)])
        self.assertNotEqual(one['required_evidence']['declaration_digest'],
                            two['required_evidence']['declaration_digest'])

    def test_requirement_checks_do_not_duplicate_source_reads(self):
        with patch.object(extractor.evidence, 'read_text', wraps=extractor.evidence.read_text) as read:
            self.guarded([self.span(), self.span(2, 4)], [self.span(1, 2), self.span(2, 3)])
        self.assertEqual(read.call_count, 1)

    def test_empty_malformed_and_oversized_requirements_fail_before_reads(self):
        invalid = [[], {}, [self.span()] * 129, [self.span(0, 2)], [self.span(3, 2)],
                   [self.span(True, 2)], [self.span('01', 2)], [self.span(path='../other.txt')],
                   [self.span(), self.span(raw=b'conflicting pin')]]
        with patch.object(extractor.evidence, 'read_text', side_effect=AssertionError('target read')):
            for required in invalid:
                with self.subTest(required=str(required)[:60]), self.assertRaises(ValueError):
                    self.guarded([self.span()], required)

    def test_full_coverage_cannot_hide_out_of_range_source(self):
        run = self.run_helper([self.span(1, 5)], [self.span(1, 5)])
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, b'')

    def test_structural_coverage_does_not_bypass_stale_pin(self):
        path = self.root / 'source.txt'
        metadata = path.stat()
        path.write_bytes(self.raw.replace(b'claim', b'other'))
        os.utime(path, ns=(metadata.st_atime_ns, metadata.st_mtime_ns))
        run = self.run_helper([self.span()], [self.span()])
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, b'')

    def test_cli_reports_missing_requirements_with_no_partial_source(self):
        run = self.run_helper([self.span(1, 1)], [self.span()])
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, b'')
        self.assertEqual(json.loads(run.stderr),
                         {'kind': 'source-excerpt-error', 'code': 'required-spans-not-covered'})
        self.assertNotIn(b'contrary evidence', run.stderr)

    def test_budget_defers_required_evidence_without_claiming_emission(self):
        run = self.run_helper([self.span()], [self.span()], budget=1)
        self.assertEqual(run.returncode, 1, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result['files'], [])
        self.assertFalse(result['required_evidence']['emitted'])
        self.assertFalse(result['source_payload_emitted'])
        self.assertIn('Keep declared required spans', result['next_step'])
        self.assertNotIn(b'contrary evidence', run.stdout)

    def test_complete_envelope_budget_includes_requirement_metadata(self):
        result = self.guarded([self.span()], [self.span()])
        for _ in range(8):
            size = len(extractor.evidence.encoded(result))
            result['measurement']['budget_bytes'] = size
        fits = self.guarded([self.span()], [self.span()], size)
        self.assertEqual(fits['status'], 'ready')
        self.assertEqual(len(extractor.evidence.encoded(fits)), size)
        deferred = self.guarded([self.span()], [self.span()], size - 1)
        self.assertEqual(deferred['status'], 'budget-exceeded')
        self.assertFalse(deferred['required_evidence']['emitted'])

    def test_unguarded_interface_has_no_requirement_metadata(self):
        normal = extractor.extract(self.root, [self.span()])
        explicit_none = extractor.extract(self.root, [self.span()], required_spans=None)
        self.assertEqual(normal, explicit_none)
        self.assertNotIn('required_evidence', normal)
        self.assertNotIn('required_evidence', extractor.extract(self.root, [self.span()], 1))

    def test_seeded_interval_coverage_matches_exact_line_sets(self):
        rng = random.Random(20260920)
        pin = extractor.evidence.sha(self.raw)
        for _ in range(150):
            selected, required = [], []
            expected_selected, expected_required = set(), set()
            for target, expected in ((selected, expected_selected), (required, expected_required)):
                for _ in range(rng.randint(1, 8)):
                    start = rng.randint(1, 30)
                    end = rng.randint(start, 30)
                    target.append(['source.txt', start, end, pin])
                    expected.update(range(start, end + 1))
            if expected_required.issubset(expected_selected):
                coverage = extractor.required_coverage(extractor.requests(selected), required)
                self.assertEqual(coverage['lines'], len(expected_required))
            else:
                with self.assertRaises(extractor.RequiredEvidenceError):
                    extractor.required_coverage(extractor.requests(selected), required)

    def test_copied_helpers_snapshot_extract_and_policy_change_workflow(self):
        folder = self.root / 'helpers'
        folder.mkdir()
        for name in ('extract_context.py', 'evidence_snapshot.py'):
            shutil.copyfile(SCRIPTS / name, folder / name)
        policy = self.root / 'AGENTS.md'
        policy.write_bytes(b'Preserve contrary evidence.\n')
        snapshot_command = [sys.executable, str(folder / 'evidence_snapshot.py'), 'capture',
                            '--root', str(self.root), '--scope', 'required-evidence fixture',
                            '--file', 'AGENTS.md', '--file', 'source.txt']
        snapshot_run = subprocess.run(snapshot_command, capture_output=True, timeout=10)
        self.assertEqual(snapshot_run.returncode, 0, snapshot_run.stderr)
        previous = self.root / 'snapshot.json'
        previous.write_bytes(snapshot_run.stdout)  # Test-owned persistence, not a helper write.
        pins = {entry['path']: entry['sha256'] for entry in json.loads(snapshot_run.stdout)['files']}
        selected = [['AGENTS.md', 1, 1, pins['AGENTS.md']], self.span()]
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        run = self.run_helper(selected, selected, helper=folder / 'extract_context.py')
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result['required_evidence']['files'], 2)
        self.assertIn('contrary evidence', result['files'][1]['excerpts'][0]['text'])
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        compare_command = snapshot_command.copy()
        compare_command[2] = 'compare'
        compare_command.append(str(previous))
        unchanged = subprocess.run(compare_command, capture_output=True, timeout=10)
        self.assertEqual(unchanged.returncode, 0, unchanged.stderr)
        # Unchanged files do not mean a newly narrowed selection is adequate.
        missing = self.run_helper([self.span(1, 1)], selected, helper=folder / 'extract_context.py')
        self.assertEqual(missing.returncode, 2)
        self.assertEqual(missing.stdout, b'')
        policy.write_bytes(b'Require independent review.\n')
        changed = subprocess.run(compare_command, capture_output=True, timeout=10)
        self.assertEqual(changed.returncode, 1, changed.stderr)
        self.assertEqual(json.loads(changed.stdout)['changed'][0]['path'], 'AGENTS.md')
        stale = self.run_helper(selected, selected, helper=folder / 'extract_context.py')
        self.assertEqual(stale.returncode, 2)
        self.assertEqual(stale.stdout, b'')
        self.assertEqual(previous.read_bytes(), snapshot_run.stdout)
        self.assertEqual(list(folder.rglob('*.pyc')), [])


if __name__ == '__main__':
    unittest.main()
