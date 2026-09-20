#!/usr/bin/env python3
"""Filesystem/packaging regressions; no agent, model or project command executes."""
import copy
import io
import json
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import zipfile

import skill_bundle as bundle

SKILLS = ('codebase-audit', 'design-system-compliance', 'security-review',
          'agentic-improvement', 'decision-intelligence', 'migration')


class SkillBundles(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / 'source'
        (self.root / 'skills').mkdir(parents=True)
        self.name = 'codebase-audit'
        shutil.copytree(bundle.ROOT / 'skills' / self.name, self.root / 'skills' / self.name)
        shutil.copyfile(bundle.ROOT / 'LICENSE', self.root / 'LICENSE')
        self.skill = self.root / 'skills' / self.name

    def declaration(self, mutate):
        path = self.skill / 'bundle.json'
        value = json.loads(path.read_text())
        mutate(value)
        path.write_text(json.dumps(value))

    def reject_source(self):
        with self.assertRaises(bundle.BundleError):
            bundle.build_archive(self.root, self.name)

    def rewrite_zip(self, data, transform):
        out = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(data)) as old, zipfile.ZipFile(out, 'w') as new:
            for info in old.infolist():
                info, content = transform(copy.copy(info), old.read(info))
                if info is not None:
                    new.writestr(info, content)
        return out.getvalue()

    def test_all_enrolled_skills_have_closed_dependencies(self):
        actual = bundle.enrolled()
        self.assertEqual(set(actual), set(SKILLS))
        for name in SKILLS:
            with self.subTest(name=name):
                result = bundle.verify_archive(bundle.build_archive(bundle.ROOT, name))
                self.assertEqual(result['name'], name)
                self.assertEqual(result['model_execution'], 'not-run')

    def test_guidance_bundles_are_independent_and_detect_missing_reference(self):
        for name, guide in [('agentic-improvement', 'efficiency.md'),
                             ('decision-intelligence', 'decision-guide.md')]:
            with self.subTest(name=name):
                target = self.root / 'skills' / name
                shutil.copytree(bundle.ROOT / 'skills' / name, target)
                data = bundle.build_archive(self.root, name)
                self.assertEqual(data, bundle.build_archive(self.root, name))
                (target / 'references' / guide).unlink()
                with self.assertRaises(bundle.BundleError):
                    bundle.build_archive(self.root, name)
                shutil.rmtree(target)  # Disposable test-owned copy only.
                with patch.object(bundle, 'read_file', side_effect=AssertionError('source dependency')):
                    self.assertEqual(bundle.verify_archive(data)['name'], name)

    def test_repeated_build_is_byte_deterministic(self):
        self.assertEqual(bundle.build_archive(self.root, self.name), bundle.build_archive(self.root, self.name))

    def test_input_content_change_changes_bundle_hash(self):
        before = bundle.build_archive(self.root, self.name)
        path = self.skill / 'references/review-guide.md'
        path.write_text(path.read_text() + '\nA synthetic amendment.\n')
        self.assertNotEqual(before, bundle.build_archive(self.root, self.name))

    def test_mtime_does_not_change_archive_identity(self):
        import os
        before = bundle.build_archive(self.root, self.name)
        os.utime(self.skill / 'SKILL.md', (1, 1))
        self.assertEqual(before, bundle.build_archive(self.root, self.name))

    def test_archive_retains_exact_license_and_safe_metadata(self):
        data = bundle.build_archive(self.root, self.name)
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            self.assertEqual(archive.read(self.name + '/LICENSE'), (bundle.ROOT / 'LICENSE').read_bytes())
            for info in archive.infolist():
                self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertEqual(info.external_attr >> 16, 0o100644)
                self.assertEqual(info.compress_type, zipfile.ZIP_STORED)

    def test_verification_survives_removal_of_original_checkout(self):
        data = bundle.build_archive(self.root, self.name)
        shutil.rmtree(self.root)  # This test owns the disposable source directory.
        with patch.object(bundle, 'read_file', side_effect=AssertionError('source dependency')):
            self.assertEqual(bundle.verify_archive(data)['name'], self.name)

    def test_extracted_skill_links_resolve_without_collection(self):
        data = bundle.build_archive(self.root, self.name)
        bundle.verify_archive(data)
        destination = self.root.parent / 'isolated-install'
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            archive.extractall(destination)  # Only this test's validated generated bytes.
        folder = destination / self.name
        files = {p.relative_to(folder).as_posix(): p.read_bytes() for p in folder.rglob('*') if p.is_file()}
        del files['LICENSE'], files['bundle-lock.json']
        bundle.validate_payload(self.name, files)

    def test_missing_declared_reference_fails(self):
        (self.skill / 'references/report-template.md').unlink()
        self.reject_source()

    def test_undeclared_file_is_not_silently_omitted(self):
        (self.skill / 'unreviewed.md').write_text('Unreviewed data.')
        self.reject_source()

    def test_local_link_to_sibling_or_missing_file_fails(self):
        original = (self.skill / 'SKILL.md').read_text()
        for target in ('../other/SKILL.md', 'references/missing.md', '/absolute.md',
                       'references/%2e%2e/private.md', 'references/review-guide.md?other=1'):
            with self.subTest(target=target):
                (self.skill / 'SKILL.md').write_text(original + f'\n[Dependency]({target})\n')
                self.reject_source()

    def test_https_source_and_fragment_do_not_create_runtime_dependency(self):
        path = self.skill / 'SKILL.md'
        path.write_text(path.read_text() + '\n[Source](https://agentskills.io/specification) [Section](#objective)\n')
        bundle.verify_archive(bundle.build_archive(self.root, self.name))

    def test_duplicate_or_wrong_declaration_fields_fail(self):
        original = (self.skill / 'bundle.json').read_bytes()
        for key, value in [('format_version', True), ('kind', 'other'), ('name', 'other'),
                           ('files', []), ('files', ['SKILL.md', 'SKILL.md']),
                           ('files', ['../outside.md']), ('extra', 1), ('optional_tools', 'ah')]:
            with self.subTest(key=key, value=value):
                data = json.loads(original)
                data[key] = value
                (self.skill / 'bundle.json').write_text(json.dumps(data))
                self.reject_source()
        (self.skill / 'bundle.json').write_bytes(b'{"format_version":1,"format_version":1}')
        self.reject_source()

    def test_required_tool_without_explicit_fallback_is_rejected(self):
        self.declaration(lambda d: d.update(optional_tools=[{'name':'ah','fallback':''}]))
        self.reject_source()

    def test_duplicate_tool_declarations_are_rejected(self):
        self.declaration(lambda d: d['optional_tools'].append(d['optional_tools'][0]))
        self.reject_source()

    def test_script_declaration_cannot_enable_execution(self):
        (self.skill / 'script.py').write_text('raise RuntimeError("must not run")')
        self.declaration(lambda d: d['files'].append('script.py'))
        self.reject_source()

    def test_frontmatter_or_required_heading_change_fails(self):
        path = self.skill / 'SKILL.md'
        original = path.read_text()
        for changed in (original.replace('name: codebase-audit','name: other'),
                        original.replace('## Completion','## Missing'),
                        original.replace('---\nname:', 'name:', 1)):
            path.write_text(changed)
            self.reject_source()

    def test_non_utf8_and_nul_text_fail(self):
        for data in (b'\xff', b'text\0'):
            (self.skill / 'references/review-guide.md').write_bytes(data)
            self.reject_source()

    def test_oversized_file_fails(self):
        (self.skill / 'references/review-guide.md').write_bytes(b'x' * (bundle.MAX_FILE + 1))
        self.reject_source()

    def test_cumulative_size_limit_fails(self):
        with patch.object(bundle, 'MAX_TOTAL', 1):
            self.reject_source()

    def test_entry_count_and_depth_limits_fail(self):
        with patch.object(bundle, 'MAX_FILES', 1):
            self.reject_source()
        (self.skill / 'references/a/b/c/d/e').mkdir(parents=True)
        self.reject_source()

    def test_symlink_file_and_parent_fail_without_following(self):
        outside = self.root.parent / 'outside.md'
        outside.write_text('synthetic outside data')
        ref = self.skill / 'references/report-template.md'
        ref.unlink()
        try:
            ref.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest('Symlink creation unavailable')
        self.reject_source()
        ref.unlink()
        shutil.rmtree(self.skill / 'references')
        (self.skill / 'references').symlink_to(self.root.parent, target_is_directory=True)
        self.reject_source()

    def test_reparse_marker_is_rejected_by_shared_link_predicate(self):
        meta = types.SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0x400)
        self.assertTrue(bundle.is_link(meta))  # Predicate test, not a Windows host test.
        self.assertFalse(bundle.is_link(types.SimpleNamespace(st_mode=stat.S_IFDIR)))

    def test_unsafe_skill_name_does_not_read_outside_source(self):
        for name in ('../outside', '/outside', 'Uppercase', '', 'x' * 65):
            with self.subTest(name=name), self.assertRaises(bundle.BundleError):
                bundle.build_archive(self.root, name)

    def test_empty_or_missing_license_fails(self):
        (self.root / 'LICENSE').write_text('')
        self.reject_source()
        (self.root / 'LICENSE').unlink()
        self.reject_source()

    def test_shared_reference_copy_cannot_drift(self):
        name = 'design-system-compliance'
        shutil.copytree(bundle.ROOT / 'skills' / name, self.root / 'skills' / name)
        (self.root / 'references').mkdir()
        source = self.root / 'references/design-intelligence.md'
        source.write_bytes((bundle.ROOT / 'references/design-intelligence.md').read_bytes())
        bundle.build_archive(self.root, name)
        source.write_text('Changed shared contract')
        with self.assertRaisesRegex(bundle.BundleError, 'shared reference drift'):
            bundle.build_archive(self.root, name)

    def test_shared_reference_path_cannot_escape(self):
        self.declaration(lambda d: d.update(shared_references={'SKILL.md':'../outside.md'}))
        self.reject_source()

    def test_missing_shared_source_fails_build_but_not_sealed_verification(self):
        data = bundle.build_archive(bundle.ROOT, 'design-system-compliance')
        with patch.object(bundle, 'read_file', side_effect=AssertionError('outside dependency')):
            bundle.verify_archive(data)

    def test_archive_tampering_fails_hash_validation(self):
        data = bundle.build_archive(self.root, self.name)
        bad = self.rewrite_zip(data, lambda i,b: (i, b + b'changed' if i.filename.endswith('SKILL.md') else b))
        with self.assertRaisesRegex(bundle.BundleError, 'identity mismatch'):
            bundle.verify_archive(bad)

    def test_archive_missing_dependency_fails(self):
        data = bundle.build_archive(self.root, self.name)
        bad = self.rewrite_zip(data, lambda i,b: (None,b) if i.filename.endswith('report-template.md') else (i,b))
        with self.assertRaises(bundle.BundleError):
            bundle.verify_archive(bad)

    def test_archive_traversal_and_link_metadata_fail(self):
        data = bundle.build_archive(self.root, self.name)
        for mode in ('traversal', 'link'):
            def change(info, content):
                if info.filename.endswith('SKILL.md'):
                    if mode == 'traversal':
                        info.filename = '../outside.md'
                    else:
                        info.external_attr = 0o120777 << 16
                return info, content
            with self.subTest(mode=mode), self.assertRaises(bundle.BundleError):
                bundle.verify_archive(self.rewrite_zip(data, change))

    def test_malformed_or_oversized_archive_fails(self):
        for data in (b'not a zip', b'x' * (bundle.MAX_TOTAL * 2 + 1)):
            with self.assertRaises(bundle.BundleError):
                bundle.verify_archive(data)

    def test_collection_payload_check_catches_omission_and_change(self):
        bundles = bundle.enrolled()
        archive_path = self.root.parent / 'collection.zip'
        def collection(mutate=False, omit=False):
            with zipfile.ZipFile(archive_path, 'w') as archive:
                archive.writestr('LICENSE', (bundle.ROOT / 'LICENSE').read_bytes())
                for name, files in bundles.items():
                    for path, data in files.items():
                        if path == 'LICENSE' or (omit and path == 'SKILL.md'):
                            continue
                        archive.writestr(f'skills/{name}/{path}', data + (b'x' if mutate else b''))
        collection()
        bundle.verify_collection(archive_path, bundles)
        for mutate, omit in ((True, False), (False, True)):
            collection(mutate, omit)
            with self.assertRaises(bundle.BundleError):
                bundle.verify_collection(archive_path, bundles)

    def test_command_writes_verified_bundle_and_refuses_overwrite(self):
        output = self.root.parent / 'review.skill.zip'
        args = [sys.executable, str(bundle.ROOT / '.github/scripts/skill_bundle.py'),
                self.name, '--output', str(output)]
        first = subprocess.run(args, capture_output=True, timeout=15)
        self.assertEqual(first.returncode, 0, first.stderr)
        before = output.read_bytes()
        self.assertEqual(json.loads(first.stdout)['sha256'], bundle.verify_archive(before)['sha256'])
        second = subprocess.run(args, capture_output=True, timeout=15)
        self.assertEqual(second.returncode, 1)
        self.assertEqual(before, output.read_bytes())

    def test_command_rejects_source_output_and_missing_parent(self):
        for output in (bundle.ROOT / 'unwanted.skill.zip', self.root.parent / 'absent/out.zip'):
            result = subprocess.run([sys.executable, str(bundle.ROOT / '.github/scripts/skill_bundle.py'),
                                     self.name, '--output', str(output)], capture_output=True, timeout=15)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()