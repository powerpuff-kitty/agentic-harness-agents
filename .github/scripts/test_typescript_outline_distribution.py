"""Check real optional-helper packaging; never load a parser during packaging."""
import io
import shutil
import tempfile
import unittest
from pathlib import Path
import zipfile

import skill_bundle as bundle

NAME = 'agentic-improvement'


class TypescriptOutlineDistribution(unittest.TestCase):
    def test_standalone_retains_exact_helper_guide_and_reader(self):
        data = bundle.build_archive(bundle.ROOT, NAME)
        self.assertEqual(bundle.verify_archive(data)['script_execution'], 'not-run')
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for path in ['scripts/outline_typescript.py', 'scripts/evidence_snapshot.py',
                         'references/typescript-outline.md']:
                self.assertEqual(archive.read(NAME + '/' + path),
                                 (bundle.ROOT / 'skills' / NAME / path).read_bytes())

    def test_missing_reader_cannot_be_hidden_by_optional_tools(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'skills').mkdir()
            shutil.copytree(bundle.ROOT / 'skills' / NAME, root / 'skills' / NAME)
            shutil.copyfile(bundle.ROOT / 'LICENSE', root / 'LICENSE')
            (root / 'skills' / NAME / 'scripts/evidence_snapshot.py').unlink()
            with self.assertRaises(bundle.BundleError):
                bundle.build_archive(root, NAME)

    def test_read_only_trials_carry_equal_inert_helper(self):
        from prepare_guidance_trial import build_packet
        full, _ = build_packet(bundle.ROOT, 'budget-preserves-policy', 'full')
        progressive, _ = build_packet(bundle.ROOT, 'budget-preserves-policy', 'progressive')
        for path in ['guidance/scripts/outline_typescript.py', 'guidance/references/typescript-outline.md']:
            self.assertEqual(full[path], progressive[path])
        self.assertIn(b'Do not execute bundled helpers', progressive['TASK.md'])


if __name__ == '__main__':
    unittest.main()
