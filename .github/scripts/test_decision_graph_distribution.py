"""Actual payload/disclosure tests; packaging never runs the graph helper."""
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

NAME = 'decision-intelligence'


class DecisionGraphDistribution(unittest.TestCase):
    def test_default_entrypoint_unchanged_and_bundle_has_both_dependencies(self):
        root = bundle.ROOT / 'skills' / NAME
        self.assertEqual(hashlib.sha256((root / 'SKILL.md').read_bytes()).hexdigest(),
                         '63f16f287818cf6a021ad00e0a6349dba0e47ee0a123a66ce8083cb41631af69')
        files = bundle.payload(bundle.ROOT, NAME)
        declaration = json.loads(files['bundle.json'])
        self.assertEqual(declaration['format_version'], 2)
        self.assertEqual(declaration['optional_scripts'][0]['execution'], 'explicit-invocation-only')
        self.assertIn('scripts/review_graph.py', files)
        self.assertIn('references/graph-review.md', files)

    def test_archive_is_standalone_and_missing_guide_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'source'
            target = root / 'skills' / NAME
            target.parent.mkdir(parents=True)
            shutil.copytree(bundle.ROOT / 'skills' / NAME, target)
            shutil.copyfile(bundle.ROOT / 'LICENSE', root / 'LICENSE')
            data = bundle.build_archive(root, NAME)
            (target / 'references/graph-review.md').unlink()
            with self.assertRaises(bundle.BundleError):
                bundle.build_archive(root, NAME)
            shutil.rmtree(root)  # Test-owned disposable files only.
            with patch.object(bundle, 'read_file', side_effect=AssertionError('source read')):
                result = bundle.verify_archive(data)
            self.assertEqual(result['script_execution'], 'not-run')

    def test_real_collection_retains_helper_and_guide(self):
        run = subprocess.run([sys.executable, str(bundle.ROOT / '.github/scripts/package_plugin.py')],
                             capture_output=True, timeout=30)
        self.assertEqual(run.returncode, 0, run.stderr)
        version = json.loads((bundle.ROOT / 'manifest.json').read_text())['version']
        with zipfile.ZipFile(bundle.ROOT / 'dist' / f'agentic-harness-agents-v{version}.zip') as archive:
            for relative in ('scripts/review_graph.py', 'references/graph-review.md'):
                path = f'skills/{NAME}/{relative}'
                self.assertEqual(archive.read(path), (bundle.ROOT / path).read_bytes())

    def test_both_review_treatments_keep_helper_inert(self):
        from prepare_guidance_trial import build_packet
        full, _ = build_packet(bundle.ROOT, 'supported-claim', 'full')
        progressive, _ = build_packet(bundle.ROOT, 'supported-claim', 'progressive')
        path = 'guidance/scripts/review_graph.py'
        self.assertEqual(full[path], progressive[path])
        for packet in (full, progressive):
            self.assertIn(b'Do not execute bundled helpers', packet['TASK.md'])
            self.assertIn(b'"network": false', packet['TASK-INPUT.json'])


if __name__ == '__main__':
    unittest.main()
