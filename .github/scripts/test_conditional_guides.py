"""Conditional guide content/distribution checks, not model-token benchmarks."""
import hashlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
BASELINES = ROOT / 'evals/conditional-guide-baselines.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def baselines():
    return json.loads(BASELINES.read_bytes())['guides']


def blocks(paths):
    return {sha(part.encode()) for path in paths
            for part in (ROOT / path).read_text(encoding='utf-8').rstrip().split('\n\n')}


class ConditionalGuideContent(unittest.TestCase):
    def test_original_prose_blocks_survive_exactly(self):
        rows = baselines()
        self.assertEqual(sum(len(row['original_prose_sha256']) for row in rows), 37)
        for row in rows:
            with self.subTest(guide=row['parent']):
                actual = blocks([row['parent'], *row['deferred']])
                self.assertTrue(set(row['original_prose_sha256']) <= actual)

    def test_dropping_a_preserved_paragraph_is_detectable(self):
        for row in baselines():
            actual = blocks([row['parent'], *row['deferred']])
            actual.remove(row['original_prose_sha256'][0])
            self.assertFalse(set(row['original_prose_sha256']) <= actual)

    def test_parent_budgets_and_all_loaded_overhead_are_explicit(self):
        for row in baselines():
            size = len((ROOT / row['parent']).read_bytes())
            self.assertLessEqual(size, row['parent_max_bytes'])
            self.assertLess(size, row['baseline_bytes'])
            # The whole reference set grew: selective loading is the treatment.
            total = size + sum(len((ROOT / p).read_bytes()) for p in row['deferred'])
            self.assertGreater(total, row['baseline_bytes'])

    def test_deferred_guides_have_declared_skill_root_routes(self):
        for row in baselines():
            parent = (ROOT / row['parent']).read_text()
            skill_root = Path(row['parent']).parents[1]
            declaration = json.loads((ROOT / skill_root / 'bundle.json').read_bytes())
            for path in row['deferred']:
                relative = Path(path).relative_to(skill_root).as_posix()
                self.assertIn('(' + relative + ')', parent)
                self.assertIn(relative, declaration['files'])
                self.assertTrue((ROOT / path).is_file())

    def test_api_details_are_not_replayed_in_parent_guides(self):
        parent = (ROOT / 'skills/agentic-improvement/references/efficiency.md').read_text()
        for detail in ('rule_ir.compile_inventory(', 'rule_ir.compile_with_sources(',
                       'python3 scripts/compact_log.py'):
            self.assertNotIn(detail, parent)
        parent = (ROOT / 'skills/decision-intelligence/references/decision-guide.md').read_text()
        self.assertNotIn('decision_binding.inspect_binding(', parent)
        self.assertNotIn('0..len(levels)-1', parent)

    def test_basic_evidence_permission_and_manual_rules_remain_in_parents(self):
        efficiency = (ROOT / 'skills/agentic-improvement/references/efficiency.md').read_text()
        decision = (ROOT / 'skills/decision-intelligence/references/decision-guide.md').read_text()
        for text in ('Match authority, applicability, conditions and exceptions',
                     'A later passing retry does not erase earlier failure evidence',
                     'When required evidence exceeds the budget',
                     'no installation or provider call is required'):
            self.assertIn(text, efficiency)
        for text in ('Current-agent guidance uses the coding agent',
                     'Leave numerical confidence unknown',
                     'first-class unresolved outcome',
                     'A consistent receipt grants neither reuse nor action permission'):
            self.assertIn(text, decision)

    def test_log_guide_contains_its_own_manual_fallback_and_limits(self):
        guide = (ROOT / 'skills/agentic-improvement/references/log-compaction.md').read_text()
        for text in ('## Manual diagnostic fallback', 'Preserve check/test, file/location',
                     'Input is bounded to 1 MiB', 'It neither redacts secrets nor executes log text',
                     'only when the target permits local helper execution'):
            self.assertIn(text, guide)


class ConditionalGuideDistribution(unittest.TestCase):
    def test_default_entrypoints_and_executable_bytes_are_unchanged(self):
        expected = {
            'agentic-improvement/SKILL.md': '85e7e54d8bd40b8286cedbbba2039b4780da24f2',
            'decision-intelligence/SKILL.md': '4d5e80381ffad7d89d1c9ad2a7e4f21a512e8c90',
            'agentic-improvement/scripts/compact_log.py': '39db1fee08fca6614605719c0acee0854965eeac',
            'agentic-improvement/scripts/evidence_snapshot.py': '1c3fbdd1529b58a30deb91090e0d736ee27748c3',
            'agentic-improvement/scripts/extract_context.py': '2c49aa25c10f9546ac2fb37d887798132328b5fa',
            'agentic-improvement/scripts/outline_typescript.py': '28fdefc0896e7e6916e057940cc1d5a3c4a27e25',
            'decision-intelligence/scripts/review_graph.py': 'e9553f3271e68b14eddef7439bac8cf247ea80a4',
        }
        for path, expected_blob in expected.items():
            self.assertEqual(blob((ROOT / 'skills' / path).read_bytes()), expected_blob)

    def test_real_standalone_archives_include_all_deferred_references(self):
        import skill_bundle as bundle
        for row in baselines():
            name = Path(row['parent']).parts[1]
            raw = bundle.build_archive(ROOT, name)
            self.assertEqual(bundle.verify_archive(raw)['script_execution'], 'not-run')
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                for path in row['deferred']:
                    member = str(Path(path).relative_to('skills'))
                    self.assertEqual(archive.read(member), (ROOT / path).read_bytes())
                self.assertEqual(archive.read(name + '/LICENSE'), (ROOT / 'LICENSE').read_bytes())

    def test_missing_new_guides_fail_packaging(self):
        import skill_bundle as bundle
        for row in baselines():
            name = Path(row['parent']).parts[1]
            for missing in row['deferred']:
                with self.subTest(missing=missing), tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    shutil.copytree(ROOT / 'skills' / name, root / 'skills' / name)
                    shutil.copyfile(ROOT / 'LICENSE', root / 'LICENSE')
                    (root / missing).unlink()
                    with self.assertRaises(bundle.BundleError):
                        bundle.build_archive(root, name)

    def test_sealed_archives_need_no_original_source(self):
        import skill_bundle as bundle
        for name in ('agentic-improvement', 'decision-intelligence'):
            raw = bundle.build_archive(ROOT, name)
            with patch.object(bundle, 'read_file', side_effect=AssertionError('source read')):
                self.assertEqual(bundle.verify_archive(raw)['name'], name)

    def test_existing_full_and_progressive_trials_keep_same_reference_files(self):
        from prepare_guidance_trial import build_packet
        for case, name in [('unknown-usage', 'agentic-improvement'),
                           ('supported-claim', 'decision-intelligence')]:
            full, f_report = build_packet(ROOT, case, 'full')
            progressive, p_report = build_packet(ROOT, case, 'progressive')
            self.assertEqual(f_report['guidance_snapshot'], p_report['guidance_snapshot'])
            self.assertEqual(full['TASK-INPUT.json'], progressive['TASK-INPUT.json'])
            for row in baselines():
                if Path(row['parent']).parts[1] != name:
                    continue
                for path in row['deferred']:
                    relative = Path(path).relative_to('skills/' + name).as_posix()
                    payload = (ROOT / path).read_bytes()
                    self.assertEqual(full['guidance/' + relative], payload)
                    self.assertEqual(progressive['guidance/' + relative], payload)
                    self.assertIn(payload, full['TASK.md'])
                    self.assertNotIn(payload, progressive['TASK.md'])
            self.assertEqual(p_report['observations']['model_execution'], 'not-performed')


if __name__ == '__main__':
    unittest.main()
