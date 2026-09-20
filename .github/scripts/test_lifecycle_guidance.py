"""Source/portability regressions, not model behaviour or observed token savings."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / 'skills/agentic-app'
FILES = {'SKILL.md', 'LICENSE', 'references/composition.md', 'references/completion.md'}
FRONTMATTER = '84c58d563c48582e38f5ccd853be50adef3f6714bfee46eec430c0e2feb50042'
LIMITS = {'SKILL.md': 3450, 'references/composition.md': 3600,
          'references/completion.md': 2700, 'LICENSE': 1200}
LINK = re.compile(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)')


def inspect(folder):
    """Check a copied known documentation payload. Not a hostile-filesystem sandbox."""
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError('real skill directory required')
    files = {}
    for path in folder.rglob('*'):
        if path.is_symlink():
            raise ValueError('linked payload refused')
        if path.is_dir():
            if path.relative_to(folder).as_posix() != 'references':
                raise ValueError('unexpected directory')
            continue
        name = path.relative_to(folder).as_posix()
        if name not in FILES or not path.is_file():
            raise ValueError('unexpected file')
        data = path.read_bytes()
        if len(data) > LIMITS[name]:
            raise ValueError('source byte ceiling exceeded')
        files[name] = data
    if set(files) != FILES:
        raise ValueError('missing document')
    body = files['SKILL.md'].decode('utf-8')
    if not body.startswith('---\n') or '\n---\n' not in body:
        raise ValueError('invalid frontmatter')
    front = body.split('\n---\n', 1)[0] + '\n---\n'
    if hashlib.sha256(front.encode()).hexdigest() != FRONTMATTER:
        raise ValueError('trigger changed without review')
    for heading in ('Objective', 'Inputs', 'Context', 'Procedure', 'Output', 'Completion'):
        if '## ' + heading + '\n' not in body:
            raise ValueError('missing procedure section')
    for name, data in files.items():
        text = data.decode('utf-8')
        if '\x00' in text:
            raise ValueError('invalid document')
        for target in LINK.findall(text):
            if target.startswith(('https://', '#')):
                continue
            if target.split('#', 1)[0] not in FILES:
                raise ValueError('unresolved skill-local reference')
    return files


class LifecycleGuidance(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name) / 'skill'
        shutil.copytree(SKILL, self.folder)

    def test_complete_directory_is_self_contained(self):
        self.assertEqual(set(inspect(self.folder)), FILES)
        self.assertFalse((self.folder.parent / 'references').exists())
        self.assertFalse((self.folder.parent / 'catalog').exists())

    def test_every_required_file_is_checked(self):
        for name in FILES:
            with self.subTest(name=name):
                path = self.folder / name
                data = path.read_bytes()
                path.unlink()
                with self.assertRaisesRegex(ValueError, 'missing document'):
                    inspect(self.folder)
                path.write_bytes(data)

    def test_entrypoint_growth_fails_without_rewriting_it(self):
        path = self.folder / 'SKILL.md'
        path.write_bytes(path.read_bytes() + b'x' * LIMITS['SKILL.md'])
        before = path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'ceiling'):
            inspect(self.folder)
        self.assertEqual(before, path.read_bytes())

    def test_original_trigger_is_retained(self):
        inspect(self.folder)
        path = self.folder / 'SKILL.md'
        path.write_text(path.read_text().replace('name: agentic-app', 'name: other'))
        with self.assertRaisesRegex(ValueError, 'trigger'):
            inspect(self.folder)

    def test_missing_section_is_rejected(self):
        path = self.folder / 'SKILL.md'
        path.write_text(path.read_text().replace('## Completion', '## Removed'))
        with self.assertRaisesRegex(ValueError, 'section'):
            inspect(self.folder)

    def test_external_local_dependency_is_rejected(self):
        path = self.folder / 'references/completion.md'
        for target in ('../other.md', '/absolute.md', 'references/missing.md'):
            original = path.read_bytes()
            path.write_bytes(original + ('\n[Missing](' + target + ')\n').encode())
            with self.subTest(target=target), self.assertRaisesRegex(ValueError, 'reference'):
                inspect(self.folder)
            path.write_bytes(original)

    def test_undeclared_payload_is_rejected(self):
        (self.folder / 'unexpected.md').write_text('Unexpected payload.')
        with self.assertRaisesRegex(ValueError, 'unexpected'):
            inspect(self.folder)

    def test_symlink_is_rejected(self):
        path = self.folder / 'references/completion.md'
        target = self.folder.parent / 'outside.md'
        target.write_bytes(path.read_bytes())
        path.unlink()
        try:
            path.symlink_to(target)
        except OSError:
            self.skipTest('symlink creation unavailable')
        with self.assertRaises(ValueError):
            inspect(self.folder)

    def test_attribution_matches_collection_license(self):
        self.assertEqual(inspect(self.folder)['LICENSE'], (ROOT / 'LICENSE').read_bytes())

    def test_documentation_copy_can_be_inspected_without_original_source(self):
        before = inspect(self.folder)
        archived = self.folder.parent / 'archived'
        shutil.copytree(self.folder, archived)
        shutil.rmtree(self.folder)  # Disposable copy owned by this test only.
        self.assertEqual(inspect(archived), before)

    def test_real_plugin_zip_preserves_every_lifecycle_file(self):
        result = subprocess.run([sys.executable, str(ROOT / '.github/scripts/package_plugin.py')],
                                cwd=ROOT, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))
        version = json.loads((ROOT / 'manifest.json').read_text())['version']
        archive_path = ROOT / 'dist' / ('agentic-harness-agents-v' + version + '.zip')
        with zipfile.ZipFile(archive_path) as archive:
            for name, data in inspect(SKILL).items():
                self.assertEqual(archive.read('skills/agentic-app/' + name), data)


if __name__ == '__main__':
    unittest.main()
