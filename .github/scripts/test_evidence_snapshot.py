"""Selected-byte freshness tests, not model quality, auth, or whole-repo coverage."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / 'skills/agentic-improvement/scripts/evidence_snapshot.py'
spec = importlib.util.spec_from_file_location('evidence_snapshot_tested', HELPER)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class EvidenceSnapshot(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        self.root = self.base / 'project'
        self.root.mkdir()
        self.paths = ['AGENTS.md', 'src/service.py']
        self.put('AGENTS.md', b'Keep object access scoped.\n')
        self.put('src/service.py', b'return allowed\n')
        self.scope = 'review object access; criteria v1'
        self.before = helper.capture(self.root, self.paths, self.scope)

    def put(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return target

    def compare(self, **kwargs):
        return helper.compare(kwargs.get('root', self.root), kwargs.get('paths', self.paths),
                              kwargs.get('scope', self.scope), kwargs.get('previous', self.before))

    def resign(self, record):
        record['inventory_digest'] = helper.sha(helper.encoded(
            {key: value for key, value in record.items() if key != 'inventory_digest'}))
        return record

    def test_deterministic_capture_and_order(self):
        self.assertEqual(self.before, helper.capture(self.root, list(reversed(self.paths)), self.scope))
        self.assertEqual(helper.validate(json.loads(helper.encoded(self.before))), self.before)

    def test_unchanged_is_not_a_verified_finding(self):
        result = self.compare()
        self.assertEqual(result['status'], 'unchanged-selected-bytes')
        self.assertEqual(result['unchanged'], sorted(self.paths))
        self.assertFalse(result['limits']['prior_observations_authenticated'])
        self.assertFalse(result['limits']['checks_verified'])
        self.assertFalse(result['limits']['retained_model_context_verified'])
        self.assertIsNone(result['limits']['evidence_sufficient'])
        self.assertIsNone(result['limits']['model_tokens'])

    def test_same_size_edit_with_restored_mtime_is_detected(self):
        path = self.root / self.paths[1]
        before = path.stat()
        path.write_bytes(b'return blocked\n')
        os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
        result = self.compare()
        self.assertEqual(result['status'], 'refresh-required')
        self.assertEqual(result['changed'][0]['path'], self.paths[1])
        self.assertEqual(result['changed'][0]['before']['bytes'], result['changed'][0]['after']['bytes'])

    def test_policy_only_change_is_detected(self):
        self.put('AGENTS.md', b'Deny access without an owner match.\n')
        result = self.compare()
        self.assertEqual([item['path'] for item in result['changed']], ['AGENTS.md'])
        self.assertEqual(result['unchanged'], ['src/service.py'])

    def test_mtime_change_without_byte_change_is_unchanged(self):
        os.utime(self.root / self.paths[0], (1, 1))
        self.assertEqual(self.before, helper.capture(self.root, self.paths, self.scope))

    def test_missing_selected_file_forces_refresh(self):
        (self.root / self.paths[1]).unlink()
        result = self.compare()
        self.assertEqual(result['status'], 'refresh-required')
        self.assertEqual(result['unavailable'][0]['path'], self.paths[1])
        with self.assertRaises(helper.SnapshotError):
            helper.capture(self.root, self.paths, self.scope)

    def test_dropping_old_path_never_reads_it_or_hides_selection_change(self):
        with patch.object(helper, 'entry', wraps=helper.entry) as read:
            result = self.compare(paths=['AGENTS.md'])
        self.assertEqual([call.args[1] for call in read.call_args_list], ['AGENTS.md'])
        self.assertEqual(result['removed_from_selection'], ['src/service.py'])
        self.assertFalse(result['selection_matches'])
        self.assertEqual(result['status'], 'refresh-required')

    def test_new_selection_is_reported(self):
        self.put('tests/access.py', b'assert permitted is False\n')
        result = self.compare(paths=self.paths + ['tests/access.py'])
        self.assertEqual(result['added'][0]['path'], 'tests/access.py')
        self.assertEqual(result['status'], 'refresh-required')

    def test_changed_scope_requires_refresh(self):
        result = self.compare(scope='review object access; criteria v2')
        self.assertFalse(result['scope_matches'])
        self.assertEqual(result['status'], 'refresh-required')

    def test_new_root_is_not_silently_equivalent(self):
        target = self.base / 'other-project'
        shutil.copytree(self.root, target)
        result = self.compare(root=target)
        self.assertFalse(result['root_matches'])
        self.assertEqual(result['status'], 'refresh-required')

    def test_no_bodies_absolute_root_or_scope_text_in_reports(self):
        for result in (self.before, self.compare()):
            raw = helper.encoded(result)
            for private in (str(self.root).encode(), self.scope.encode(), b'Keep object access scoped.', b'return allowed'):
                self.assertNotIn(private, raw)

    def test_invalid_paths_and_duplicate_aliases(self):
        for value in ('../outside', '/etc/passwd', 'a/../b', './file', 'a//b',
                      'C:/file', 'a\\b', 'a\n', '*', 'src/[a].py', 'a./file', 'a/ file'):
            with self.subTest(path=value), self.assertRaises(helper.SnapshotError):
                helper.capture(self.root, [value], self.scope)
        for paths in ([], ['a'] * 2, ['A', 'a'], ['a'] * (helper.MAX_FILES + 1)):
            with self.assertRaises(helper.SnapshotError):
                helper.selection(paths)

    def test_unicode_and_space_paths_and_crlf(self):
        self.put('src/cafe café.py', 'é\r\nsecond\nlast'.encode())
        record = helper.capture(self.root, ['src/cafe café.py'], self.scope)
        self.assertEqual(record['files'][0]['sha256'], helper.sha('é\r\nsecond\nlast'.encode()))

    def test_empty_files_are_valid(self):
        self.put('empty.txt', b'')
        record = helper.capture(self.root, ['empty.txt'], self.scope)
        self.assertEqual(record['files'][0]['bytes'], 0)

    def test_nontext_capture_refuses_and_comparison_reports_unavailable(self):
        for raw in (b'\xff', b'a\0b'):
            self.put('AGENTS.md', raw)
            with self.assertRaises(helper.SnapshotError):
                helper.capture(self.root, self.paths, self.scope)
            self.assertEqual(self.compare()['unavailable'][0]['reason'], 'non-text-input')

    def test_file_and_ancestor_links_are_refused(self):
        path = self.root / 'AGENTS.md'
        outside = self.base / 'outside.txt'
        outside.write_bytes(path.read_bytes())
        path.unlink()
        try:
            path.symlink_to(outside)
        except OSError:
            self.skipTest('symlinks unavailable')
        self.assertEqual(self.compare()['status'], 'refresh-required')
        with self.assertRaises(helper.SnapshotError):
            helper.capture(self.root, self.paths, self.scope)
        linked_root = self.base / 'linked-project'
        linked_root.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(helper.SnapshotError):
            helper.capture(linked_root, self.paths, self.scope)

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'FIFO unavailable')
    def test_fifo_refused_without_blocking(self):
        os.mkfifo(self.root / 'pipe')
        with self.assertRaises(helper.SnapshotError):
            helper.capture(self.root, ['pipe'], self.scope)

    def test_per_file_bound(self):
        self.put('big.txt', b'x' * (helper.MAX_FILE_BYTES + 1))
        with self.assertRaises(helper.SnapshotError):
            helper.capture(self.root, ['big.txt'], self.scope)

    def test_total_bound_and_unavailable_reporting(self):
        self.put('one', b'x' * 6)
        self.put('two', b'x' * 6)
        with patch.object(helper, 'MAX_TOTAL_BYTES', 10):
            with self.assertRaises(helper.SnapshotError):
                helper.capture(self.root, ['one', 'two'], self.scope)
        with patch.object(helper, 'MAX_TOTAL_BYTES', 50):
            result = self.compare(paths=self.paths + ['one', 'two'])
            self.assertTrue(result['unavailable'])
            self.assertLessEqual(result['measurement']['hashed_source_bytes'], 50)

    def test_malformed_or_tampered_record_refused_before_reads(self):
        variants = [None, {}, {**self.before, 'extra': 1}, {**self.before, 'format_version': True}]
        altered = copy.deepcopy(self.before)
        altered['files'][0]['sha256'] = 'sha256:' + '0' * 64
        variants.append(altered)
        for record in variants:
            with self.subTest(record=type(record).__name__), patch.object(helper, 'entry') as read:
                with self.assertRaises(helper.SnapshotError):
                    self.compare(previous=record)
                read.assert_not_called()

    def test_record_paths_cannot_expand_read_selection(self):
        altered = copy.deepcopy(self.before)
        altered['files'][1]['path'] = 'unrequested/private.txt'
        self.resign(altered)
        with patch.object(helper, 'entry', wraps=helper.entry) as read:
            result = self.compare(paths=['AGENTS.md'], previous=altered)
        self.assertEqual([call.args[1] for call in read.call_args_list], ['AGENTS.md'])
        self.assertEqual(result['removed_from_selection'], ['unrequested/private.txt'])

    def test_unsafe_record_path_refused_even_with_recalculated_digest(self):
        altered = copy.deepcopy(self.before)
        altered['files'][0]['path'] = '../outside'
        self.resign(altered)
        with self.assertRaises(helper.SnapshotError):
            self.compare(previous=altered)

    def test_record_boolean_size_unsorted_and_duplicate_paths_refused(self):
        for modify in (lambda x: x['files'][0].update(bytes=True),
                       lambda x: x['files'].reverse(),
                       lambda x: x['files'].append(copy.deepcopy(x['files'][0]))):
            record = copy.deepcopy(self.before)
            modify(record)
            self.resign(record)
            with self.assertRaises(helper.SnapshotError):
                helper.validate(record)

    def test_loader_rejects_duplicate_nonfinite_and_oversized_json(self):
        path = self.base / 'record.json'
        for raw in (b'{"x":0,"x":1}', b'{"x":NaN}', b'{"x":Infinity}',
                    b'x' * (helper.MAX_RECORD_BYTES + 1)):
            path.write_bytes(raw)
            with self.assertRaises((helper.SnapshotError, ValueError)):
                helper.load(path)

    def test_record_file_symlink_refused(self):
        path = self.base / 'record.json'
        path.write_bytes(helper.encoded(self.before))
        link = self.base / 'link.json'
        try:
            link.symlink_to(path)
        except OSError:
            self.skipTest('symlinks unavailable')
        with self.assertRaises(helper.SnapshotError):
            helper.load(link)

    def test_no_execution_or_writes_of_source_content(self):
        self.put('script.py', b'raise AssertionError("NEVER EXECUTE")\n')
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        helper.capture(self.root, ['script.py'], self.scope)
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_change_between_stat_and_open_rejected(self):
        real_open = os.open
        def changed(path, flags):
            Path(path).write_bytes(b'changed input\n')
            return real_open(path, flags)
        with patch.object(helper.os, 'open', side_effect=changed):
            with self.assertRaises(helper.SnapshotError):
                helper.capture(self.root, ['AGENTS.md'], self.scope)

    def test_real_subprocess_capture_compare_exit_codes_and_no_writes(self):
        command = [sys.executable, str(HELPER), 'capture', '--root', str(self.root), '--scope', self.scope]
        for name in self.paths:
            command += ['--file', name]
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        run = subprocess.run(command, capture_output=True, timeout=10)
        self.assertEqual(run.returncode, 0, run.stderr)
        record = self.base / 'snapshot.json'
        record.write_bytes(run.stdout)  # Test-owned persistence, not a helper write.
        command[2] = 'compare'
        command.append(str(record))
        run = subprocess.run(command, capture_output=True, timeout=10)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['status'], 'unchanged-selected-bytes')
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
        self.put('src/service.py', b'return blocked\n')
        run = subprocess.run(command, capture_output=True, timeout=10)
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(json.loads(run.stdout)['changed'][0]['path'], 'src/service.py')
        record.write_text('{invalid')
        run = subprocess.run(command, capture_output=True, timeout=10)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, b'')
        self.assertNotIn(b'{invalid', run.stderr)

    def test_script_runs_when_copied_alone(self):
        copied = self.base / 'standalone.py'
        shutil.copyfile(HELPER, copied)
        run = subprocess.run([sys.executable, str(copied), 'capture', '--root', str(self.root),
                              '--scope', self.scope, '--file', 'AGENTS.md'],
                             capture_output=True, timeout=10)
        self.assertEqual(run.returncode, 0, run.stderr)
        helper.validate(json.loads(run.stdout))

    def test_unselected_changes_are_not_falsely_certified(self):
        self.put('unselected.py', b'changed dependency\n')
        report = self.compare()
        self.assertEqual(report['status'], 'unchanged-selected-bytes')
        self.assertFalse(report['limits']['unselected_files_checked'])
        self.assertIsNone(report['limits']['evidence_sufficient'])

    def test_scope_and_input_limits(self):
        for scope in ('', ' spaced ', 'line\nbreak', 'x' * 4097):
            with self.assertRaises(helper.SnapshotError):
                helper.scope_hash(scope)


if __name__ == '__main__':
    unittest.main()
