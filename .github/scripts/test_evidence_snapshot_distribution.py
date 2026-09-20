"""Actual optional-helper distribution checks; packaging never executes helpers."""
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

RELATIVE = 'scripts/evidence_snapshot.py'
GUIDE = 'references/evidence-reuse.md'


class EvidenceSnapshotDistribution(unittest.TestCase):
    def test_declared_helper_and_guide_survive_archive_without_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'source'
            shutil.copytree(bundle.ROOT / 'skills/agentic-improvement', root / 'skills/agentic-improvement')
            shutil.copyfile(bundle.ROOT / 'LICENSE', root / 'LICENSE')
            data = bundle.build_archive(root, 'agentic-improvement')
            source = root / 'skills/agentic-improvement'
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for path in (RELATIVE, GUIDE):
                    self.assertEqual(archive.read('agentic-improvement/' + path), (source / path).read_bytes())
            (source / GUIDE).unlink()
            with self.assertRaises(bundle.BundleError):
                bundle.build_archive(root, 'agentic-improvement')
            shutil.rmtree(root)  # Only this test's private temporary source.
            with patch.object(bundle, 'read_file', side_effect=AssertionError('source read')):
                result = bundle.verify_archive(data)
            self.assertEqual(result['script_execution'], 'not-run')

    def test_prepared_trials_keep_both_helpers_inert_and_available(self):
        from prepare_guidance_trial import build_packet
        full, _ = build_packet(bundle.ROOT, 'budget-preserves-policy', 'full')
        progressive, _ = build_packet(bundle.ROOT, 'budget-preserves-policy', 'progressive')
        for path in (RELATIVE, 'scripts/compact_log.py'):
            self.assertEqual(full['guidance/' + path], progressive['guidance/' + path])
        for packet in (full, progressive):
            self.assertIn(b'Do not execute bundled helpers', packet['TASK.md'])

    def test_real_collection_zip_contains_exact_helper_and_guide(self):
        run = subprocess.run([sys.executable, str(bundle.ROOT / '.github/scripts/package_plugin.py')],
                             capture_output=True, timeout=30)
        self.assertEqual(run.returncode, 0, run.stderr)
        version = json.loads((bundle.ROOT / 'manifest.json').read_text())['version']
        with zipfile.ZipFile(bundle.ROOT / 'dist' / f'agentic-harness-agents-v{version}.zip') as archive:
            for name in (RELATIVE, GUIDE):
                path = 'skills/agentic-improvement/' + name
                self.assertEqual(archive.read(path), (bundle.ROOT / path).read_bytes())


if __name__ == '__main__':
    unittest.main()
