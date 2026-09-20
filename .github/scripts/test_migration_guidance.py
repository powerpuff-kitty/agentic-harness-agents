"""Migration content/distribution regressions, not observed model adherence."""
import copy
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import skill_bundle as bundle
from guidance_eval import evaluate
from prepare_guidance_trial import build_packet
from test_guidance_efficiency import cases, synthetic_observation

NAME = 'migration'
ROOT = bundle.ROOT
SKILL = ROOT / 'skills' / NAME
CASE_IDS = {'migration-divergent-target', 'migration-stale-plan',
            'migration-identical-source', 'migration-read-only'}


class MigrationGuidance(unittest.TestCase):
    def test_trigger_is_preserved_and_entrypoint_is_bounded(self):
        raw = (SKILL / 'SKILL.md').read_bytes()
        self.assertEqual(hashlib.sha256(raw.split(b'\n---\n', 1)[0]).hexdigest(),
                         'ba3c7f75b98c2ae94842870497a559301381f9373290fa0e9e730fc2306be1f4')
        self.assertLessEqual(len(raw), 2600)
        self.assertIn(b'references/migration-guide.md', raw)

    def test_bundle_is_documentation_only_and_local(self):
        declaration = json.loads((SKILL / 'bundle.json').read_bytes())
        self.assertEqual(declaration['format_version'], 1)
        self.assertEqual(declaration['files'], ['SKILL.md', 'references/migration-guide.md'])
        self.assertEqual(declaration['shared_references'], {})
        self.assertEqual(declaration['optional_tools'], [])
        self.assertNotIn('optional_scripts', declaration)

    def test_actual_standalone_archive_retains_guide_and_license(self):
        data = bundle.build_archive(ROOT, NAME)
        report = bundle.verify_archive(data)
        self.assertEqual(report['name'], NAME)
        self.assertEqual(report['script_execution'], 'not-run')
        self.assertEqual(report['model_execution'], 'not-run')
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            self.assertEqual(archive.read('migration/references/migration-guide.md'),
                             (SKILL / 'references/migration-guide.md').read_bytes())
            self.assertEqual(archive.read('migration/LICENSE'), (ROOT / 'LICENSE').read_bytes())

    def test_build_is_deterministic(self):
        self.assertEqual(bundle.build_archive(ROOT, NAME), bundle.build_archive(ROOT, NAME))

    def test_missing_local_guide_blocks_packaging(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copytree(SKILL, root / 'skills/migration')
            shutil.copyfile(ROOT / 'LICENSE', root / 'LICENSE')
            (root / 'skills/migration/references/migration-guide.md').unlink()
            with self.assertRaises(bundle.BundleError):
                bundle.build_archive(root, NAME)

    def test_sealed_bundle_verifies_without_original_source(self):
        data = bundle.build_archive(ROOT, NAME)
        with patch.object(bundle, 'read_file', side_effect=AssertionError('source read')):
            self.assertEqual(bundle.verify_archive(data)['name'], NAME)

    def test_copy_keeps_payload_without_sibling_skills(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copytree(SKILL, root / 'skills/migration')
            shutil.copyfile(ROOT / 'LICENSE', root / 'LICENSE')
            self.assertEqual(bundle.build_archive(root, NAME), bundle.build_archive(ROOT, NAME))

    def test_existing_preparer_accepts_migration_cases_and_keeps_all_evidence(self):
        selected = [case for case in cases() if case['id'] in CASE_IDS]
        self.assertEqual({case['id'] for case in selected}, CASE_IDS)
        for case in selected:
            with self.subTest(case=case['id']):
                full, full_report = build_packet(ROOT, case['id'], 'full')
                progressive, progress_report = build_packet(ROOT, case['id'], 'progressive')
                self.assertEqual(full_report['guidance_snapshot'], progress_report['guidance_snapshot'])
                self.assertEqual(full['TASK-INPUT.json'], progressive['TASK-INPUT.json'])
                task = json.loads(full['TASK-INPUT.json'])
                self.assertEqual(task['evidence'], case['sources'])
                self.assertFalse(task['permissions']['project_mutation'])
                self.assertEqual(task['permissions']['provider_calls'], 0)
                self.assertNotIn('outcome', task)
                self.assertIn('guidance/references/migration-guide.md', progressive)
                self.assertGreater(len(full['TASK.md']), len(progressive['TASK.md']))
                self.assertEqual(full_report['observations']['model_execution'], 'not-performed')

    def test_grader_detects_missing_evidence_and_invented_verification(self):
        for case in cases():
            if case['id'] not in CASE_IDS:
                continue
            good = synthetic_observation(case)
            self.assertTrue(evaluate(case, good)['passed'])
            for key in case['required']:
                bad = copy.deepcopy(good)
                del bad['sources'][key]
                self.assertIn('required-evidence-missing', evaluate(case, bad)['failures'])
            bad = copy.deepcopy(good)
            bad['verification_claimed'] = True
            self.assertIn('unobserved-verification', evaluate(case, bad)['failures'])
            bad = copy.deepcopy(good)
            bad['provider_calls'] = 1
            self.assertFalse(evaluate(case, bad)['passed'])

    def test_packaging_command_is_existing_tool_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'migration.zip'
            command = [sys.executable, str(ROOT / '.github/scripts/skill_bundle.py'),
                       NAME, '--output', str(output)]
            first = subprocess.run(command, capture_output=True, timeout=15)
            self.assertEqual(first.returncode, 0, first.stderr)
            data = output.read_bytes()
            second = subprocess.run(command, capture_output=True, timeout=15)
            self.assertEqual(second.returncode, 1)
            self.assertEqual(output.read_bytes(), data)
            self.assertEqual(bundle.verify_archive(data)['name'], NAME)


if __name__ == '__main__':
    unittest.main()
