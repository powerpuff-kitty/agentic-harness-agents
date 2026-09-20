"""Inspect real archives and copied helper dependencies, not model behaviour."""
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

import skill_bundle as bundle

NAME = 'agentic-improvement'
HELPERS = ('extract_context.py', 'evidence_snapshot.py')


class SourceExcerptDistribution(unittest.TestCase):
    def test_standalone_archive_runs_after_copy_without_source_checkout(self):
        data = bundle.build_archive(bundle.ROOT, NAME)
        self.assertEqual(bundle.verify_archive(data)['script_execution'], 'not-run')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'scripts').mkdir()
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for name in HELPERS:
                    content = archive.read(NAME + '/scripts/' + name)
                    self.assertEqual(content, (bundle.ROOT / 'skills' / NAME / 'scripts' / name).read_bytes())
                    (root / 'scripts' / name).write_bytes(content)
            raw = b'first\nnecessary context\nlast\n'
            (root / 'source.txt').write_bytes(raw)
            run = subprocess.run([sys.executable, str(root / 'scripts/extract_context.py'),
                                  '--root', str(root), '--span', 'source.txt', '2', '2',
                                  'sha256:' + hashlib.sha256(raw).hexdigest()],
                                 capture_output=True, timeout=10, cwd=root)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)['files'][0]['excerpts'][0]['text'], 'necessary context\n')
            self.assertEqual(list(root.rglob('__pycache__')), [])

    def test_missing_local_dependency_blocks_packaging(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'skills').mkdir()
            shutil.copytree(bundle.ROOT / 'skills' / NAME, root / 'skills' / NAME)
            shutil.copyfile(bundle.ROOT / 'LICENSE', root / 'LICENSE')
            (root / 'skills' / NAME / 'scripts/evidence_snapshot.py').unlink()
            with self.assertRaises(bundle.BundleError):
                bundle.build_archive(root, NAME)

    def test_collection_retains_exact_helper_and_dependency(self):
        run = subprocess.run([sys.executable, str(bundle.ROOT / '.github/scripts/package_plugin.py')],
                             capture_output=True, timeout=30)
        self.assertEqual(run.returncode, 0, run.stderr)
        version = json.loads((bundle.ROOT / 'manifest.json').read_text())['version']
        with zipfile.ZipFile(bundle.ROOT / 'dist' / f'agentic-harness-agents-v{version}.zip') as archive:
            for name in HELPERS:
                path = f'skills/{NAME}/scripts/{name}'
                self.assertEqual(archive.read(path), (bundle.ROOT / path).read_bytes())

    def test_prepared_read_only_trials_carry_same_inert_helpers(self):
        from prepare_guidance_trial import build_packet
        full, _ = build_packet(bundle.ROOT, 'budget-preserves-policy', 'full')
        progressive, _ = build_packet(bundle.ROOT, 'budget-preserves-policy', 'progressive')
        for name in HELPERS:
            path = 'guidance/scripts/' + name
            self.assertEqual(full[path], progressive[path])
        for packet in (full, progressive):
            self.assertIn(b'Do not execute bundled helpers', packet['TASK.md'])


if __name__ == '__main__':
    unittest.main()
