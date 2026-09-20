"""Test actual guide distribution and unchanged default entrypoints, not model use."""
import hashlib
import io
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

import skill_bundle as bundle

NAME = 'agentic-improvement'
GUIDE = 'references/continuation.md'


class ContinuationGuidance(unittest.TestCase):
    def test_default_skill_unchanged_and_guide_is_conditionally_linked(self):
        folder = bundle.ROOT / 'skills' / NAME
        self.assertEqual(hashlib.sha256((folder / 'SKILL.md').read_bytes()).hexdigest(),
                         'fb6f6d798aa420167debe34dac0f3b7af3859bb9bbcb220be5dcff631ecd9ab5')
        self.assertIn('(' + GUIDE + ')', (folder / 'references/efficiency.md').read_text())

    def test_standalone_archive_retains_local_guide_and_fallback(self):
        data = bundle.build_archive(bundle.ROOT, NAME)
        self.assertEqual(bundle.verify_archive(data)['script_execution'], 'not-run')
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            self.assertEqual(archive.read(NAME + '/' + GUIDE),
                             (bundle.ROOT / 'skills' / NAME / GUIDE).read_bytes())
            self.assertIn(NAME + '/references/evidence-reuse.md', archive.namelist())

    def test_missing_continuation_guide_refuses_packaging(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'skills').mkdir()
            shutil.copytree(bundle.ROOT / 'skills' / NAME, root / 'skills' / NAME)
            shutil.copyfile(bundle.ROOT / 'LICENSE', root / 'LICENSE')
            (root / 'skills' / NAME / GUIDE).unlink()
            with self.assertRaises(bundle.BundleError):
                bundle.build_archive(root, NAME)

    def test_both_prepared_treatments_retain_same_optional_guide(self):
        from prepare_guidance_trial import build_packet
        full, _ = build_packet(bundle.ROOT, 'budget-preserves-policy', 'full')
        progressive, _ = build_packet(bundle.ROOT, 'budget-preserves-policy', 'progressive')
        path = 'guidance/' + GUIDE
        self.assertEqual(full[path], progressive[path])
        self.assertEqual(full[path], (bundle.ROOT / 'skills' / NAME / GUIDE).read_bytes())
        for packet in (full, progressive):
            self.assertIn(b'Do not execute bundled helpers', packet['TASK.md'])


if __name__ == '__main__':
    unittest.main()
