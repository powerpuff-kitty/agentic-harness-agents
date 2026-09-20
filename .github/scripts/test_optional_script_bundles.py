"""v1 compatibility and v2 opaque-script packaging; never import bundled scripts."""
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

NAME = 'sample-skill'


def fixture(root):
    folder = root / 'skills' / NAME
    folder.mkdir(parents=True)
    (root / 'LICENSE').write_text('Synthetic licence for regression fixture.\n')
    body = '---\nname: sample-skill\ndescription: "Synthetic fixture only."\n---\n# Sample\n\n'
    body += ''.join('## ' + heading + '\n\nFixture.\n\n' for heading in bundle.HEADINGS)
    (folder / 'SKILL.md').write_text(body)
    declaration = {'format_version': 1, 'kind': 'standalone-skill', 'name': NAME,
                   'files': ['SKILL.md'], 'optional_tools': [], 'shared_references': {}}
    (folder / 'bundle.json').write_text(json.dumps(declaration, sort_keys=True) + '\n')
    return folder


class OptionalScriptBundles(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'source'
        self.folder = fixture(self.root)

    def alter(self, change):
        p = self.folder / 'bundle.json'
        d = json.loads(p.read_text())
        change(d)
        p.write_text(json.dumps(d, sort_keys=True) + '\n')

    def v2(self):
        (self.folder / 'scripts').mkdir()
        # This source must never be executed by validation or packaging.
        (self.folder / 'scripts/helper.py').write_text('raise AssertionError("must never execute")\n')
        self.alter(lambda d: d.update(format_version=2, files=['SKILL.md', 'scripts/helper.py'],
                                      optional_scripts=[{'path': 'scripts/helper.py',
                                       'execution': 'explicit-invocation-only',
                                       'fallback': 'Use the manual procedure.'}]))

    def reject(self):
        with self.assertRaises(bundle.BundleError):
            bundle.build_archive(self.root, NAME)

    def test_v1_archive_bytes_remain_compatible(self):
        # Computed with the exact pre-change skill_bundle.py Git blob 67b49fd.
        expected = 'a7bb2c38f2b48a775291a40766dae6882e08ada04b68f11e853059ca6622b2df'
        data = bundle.build_archive(self.root, NAME)
        self.assertEqual(hashlib.sha256(data).hexdigest(), expected)
        result = bundle.verify_archive(data)
        self.assertEqual(result['model_execution'], 'not-run')

    def test_v1_still_rejects_scripts(self):
        (self.folder / 'scripts').mkdir()
        (self.folder / 'scripts/helper.py').write_text('pass\n')
        self.alter(lambda d: d['files'].append('scripts/helper.py'))
        self.reject()

    def test_v2_build_and_verify_never_execute_script(self):
        self.v2()
        data = bundle.build_archive(self.root, NAME)
        self.assertEqual(data, bundle.build_archive(self.root, NAME))
        result = bundle.verify_archive(data)
        self.assertEqual(result['script_execution'], 'not-run')
        self.assertIn('payload bytes', result['verified'])
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            info = archive.getinfo(NAME + '/scripts/helper.py')
            self.assertEqual(info.external_attr >> 16, 0o100644)
            self.assertIn(b'must never execute', archive.read(info))

    def test_v2_sealed_verification_needs_no_checkout(self):
        self.v2()
        data = bundle.build_archive(self.root, NAME)
        shutil.rmtree(self.root)
        with patch.object(bundle, 'read_file', side_effect=AssertionError('source read')):
            bundle.verify_archive(data)

    def test_missing_and_undeclared_script_rejected(self):
        self.v2()
        p = self.folder / 'scripts/helper.py'
        original = p.read_bytes()
        p.unlink()
        self.reject()
        p.write_bytes(original)
        (self.folder / 'scripts/other.py').write_text('pass\n')
        self.reject()

    def test_v2_requires_explicit_nonempty_declaration(self):
        self.v2()
        self.alter(lambda d: d.update(optional_scripts=[]))
        self.reject()

    def test_automatic_execution_and_missing_fallback_rejected(self):
        self.v2()
        original = (self.folder / 'bundle.json').read_text()
        for field, value in [('execution', 'on-load'), ('execution', True), ('fallback', ''),
                             ('path', '../outside.py'), ('path', 'scripts/helper.sh')]:
            (self.folder / 'bundle.json').write_text(original)
            self.alter(lambda d: d['optional_scripts'][0].update({field: value}))
            self.reject()

    def test_duplicate_script_declarations_rejected(self):
        self.v2()
        self.alter(lambda d: d['optional_scripts'].append(copy.deepcopy(d['optional_scripts'][0])))
        self.reject()

    def test_boolean_and_unknown_versions_rejected(self):
        for value in [True, 3, '2']:
            self.alter(lambda d: d.update(format_version=value))
            self.reject()

    def test_script_bytes_tampering_rejected(self):
        self.v2()
        data = bundle.build_archive(self.root, NAME)
        output = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(data)) as src, zipfile.ZipFile(output, 'w') as dst:
            for info in src.infolist():
                content = src.read(info)
                if info.filename.endswith('helper.py'):
                    content += b'#changed\n'
                dst.writestr(info, content)
        with self.assertRaises(bundle.BundleError):
            bundle.verify_archive(output.getvalue())

    def test_script_not_a_shared_document(self):
        self.v2()
        self.alter(lambda d: d.update(shared_references={'scripts/helper.py': 'references/code.md'}))
        self.reject()

    def test_actual_efficiency_skill_archive_contains_helper(self):
        data = bundle.build_archive(bundle.ROOT, 'agentic-improvement')
        bundle.verify_archive(data)
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            name = 'agentic-improvement/scripts/compact_log.py'
            self.assertEqual(archive.read(name),
                             (bundle.ROOT / 'skills/agentic-improvement/scripts/compact_log.py').read_bytes())

    def test_prepared_trials_keep_helpers_inert(self):
        from prepare_guidance_trial import build_packet
        full, _ = build_packet(bundle.ROOT, 'budget-preserves-policy', 'full')
        progressive, _ = build_packet(bundle.ROOT, 'budget-preserves-policy', 'progressive')
        helper = 'guidance/scripts/compact_log.py'
        self.assertEqual(full[helper], progressive[helper])
        for packet in (full, progressive):
            self.assertIn(b'Do not execute bundled helpers', packet['TASK.md'])
            self.assertIn(b'"network": false', packet['TASK-INPUT.json'])

    def test_real_collection_packager_retains_helper(self):
        proc = subprocess.run([sys.executable, str(bundle.ROOT / '.github/scripts/package_plugin.py')],
                              capture_output=True, timeout=30)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        version = json.loads((bundle.ROOT / 'manifest.json').read_text())['version']
        archive = bundle.ROOT / 'dist' / f'agentic-harness-agents-v{version}.zip'
        with zipfile.ZipFile(archive) as z:
            path = 'skills/agentic-improvement/scripts/compact_log.py'
            self.assertEqual(z.read(path), (bundle.ROOT / path).read_bytes())


if __name__ == '__main__':
    unittest.main()
