"""Exercise the new navigation mode from real standalone archives, not model sessions."""
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


class PythonOutlineDistribution(unittest.TestCase):
    def test_archive_retains_guide_and_runs_outline_without_checkout(self):
        data = bundle.build_archive(bundle.ROOT, NAME)
        self.assertEqual(bundle.verify_archive(data)['script_execution'], 'not-run')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'scripts').mkdir()
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                guide = 'references/python-outline.md'
                self.assertEqual(archive.read(NAME + '/' + guide),
                                 (bundle.ROOT / 'skills' / NAME / guide).read_bytes())
                for name in ('extract_context.py', 'evidence_snapshot.py'):
                    content = archive.read(NAME + '/scripts/' + name)
                    self.assertEqual(content, (bundle.ROOT / 'skills' / NAME / 'scripts' / name).read_bytes())
                    (root / 'scripts' / name).write_bytes(content)
            raw = b'@unresolved\ndef target():\n    return 42\n'
            (root / 'source.py').write_bytes(raw)
            run = subprocess.run([sys.executable, str(root / 'scripts/extract_context.py'),
                                  '--root', str(root), '--outline', 'source.py',
                                  'sha256:' + hashlib.sha256(raw).hexdigest()],
                                 capture_output=True, timeout=10, cwd=root)
            self.assertEqual(run.returncode, 0, run.stderr)
            item = json.loads(run.stdout)['files'][0]['definitions'][0]
            self.assertEqual((item['name'], item['start_line'], item['end_line']), ('target', 1, 3))
            self.assertNotIn(b'return 42', run.stdout)
            self.assertEqual((root / 'source.py').read_bytes(), raw)
            self.assertEqual(list(root.rglob('*.pyc')), [])

    def test_declared_outline_guide_cannot_be_omitted(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'skills').mkdir()
            shutil.copytree(bundle.ROOT / 'skills' / NAME, root / 'skills' / NAME)
            shutil.copyfile(bundle.ROOT / 'LICENSE', root / 'LICENSE')
            (root / 'skills' / NAME / 'references/python-outline.md').unlink()
            with self.assertRaises(bundle.BundleError):
                bundle.build_archive(root, NAME)


if __name__ == '__main__':
    unittest.main()
