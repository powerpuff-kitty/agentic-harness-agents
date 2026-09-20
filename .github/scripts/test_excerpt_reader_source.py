"""Execute the real excerpt loader with test-owned cached readers, never models."""
import importlib.util
import json
import os
from pathlib import Path
import py_compile
import shutil
import subprocess
import sys
import tempfile
import types
import unittest

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / 'skills/agentic-improvement/scripts/extract_context.py'


class ExcerptReaderSource(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.helper = self.root / 'extract_context.py'
        self.reader = self.root / 'evidence_snapshot.py'
        shutil.copyfile(HELPER, self.helper)
        old_setting = sys.dont_write_bytecode
        self.addCleanup(setattr, sys, 'dont_write_bytecode', old_setting)

    def load(self):
        # Execute the actual extractor bytes without caching the test's outer import.
        module = types.ModuleType('tested_excerpt_source_loader')
        module.__file__ = str(self.helper)
        exec(compile(self.helper.read_bytes(), str(self.helper), 'exec'), module.__dict__)
        return module

    def cached(self, before, after, mode=py_compile.PycInvalidationMode.TIMESTAMP):
        self.reader.write_bytes(before)
        metadata = self.reader.stat()
        cache = Path(py_compile.compile(str(self.reader), doraise=True, invalidation_mode=mode))
        self.reader.write_bytes(after)
        os.utime(self.reader, ns=(metadata.st_atime_ns, metadata.st_mtime_ns))
        return cache

    def inventory(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob('*') if p.is_file()}

    def test_timestamp_cache_cannot_override_same_size_current_source(self):
        self.cached(b'VALUE = "stale"\n', b'VALUE = "fresh"\n')
        before = self.inventory()
        self.assertEqual(self.load().evidence.VALUE, 'fresh')
        self.assertEqual(self.inventory(), before)

    def test_unchecked_hash_cache_cannot_override_current_source(self):
        self.cached(b'VALUE = "old"\n', b'VALUE = "current source"\n',
                    py_compile.PycInvalidationMode.UNCHECKED_HASH)
        before = self.inventory()
        self.assertEqual(self.load().evidence.VALUE, 'current source')
        self.assertEqual(self.inventory(), before)

    def test_current_syntax_error_cannot_hide_behind_timestamp_cache(self):
        good = b'VALUE = "stale"\n'
        bad = b'VALUE = (      \n'
        self.assertEqual(len(good), len(bad))
        self.cached(good, bad)
        before = self.inventory()
        self.assertIsNone(self.load().evidence)
        self.assertEqual(self.inventory(), before)

    def test_current_syntax_error_cannot_hide_behind_unchecked_cache(self):
        self.cached(b'VALUE = "old"\n', b'not valid python!!!\n',
                    py_compile.PycInvalidationMode.UNCHECKED_HASH)
        self.assertIsNone(self.load().evidence)

    def test_cold_load_retains_module_metadata_without_writing_bytecode(self):
        self.reader.write_bytes(b'VALUE = "current"\n')
        before = self.inventory()
        reader = self.load().evidence
        self.assertEqual(reader.VALUE, 'current')
        self.assertEqual(reader.__file__, str(self.reader))
        self.assertEqual(reader.__spec__.origin, str(self.reader))
        self.assertEqual(self.inventory(), before)
        self.assertEqual(list(self.root.rglob('*.pyc')), [])

    def test_caller_bytecode_setting_is_preserved_on_success(self):
        self.reader.write_bytes(b'VALUE = "current"\n')
        for setting in (False, True):
            with self.subTest(setting=setting):
                sys.dont_write_bytecode = setting
                self.assertIsNotNone(self.load().evidence)
                self.assertIs(sys.dont_write_bytecode, setting)

    def test_caller_bytecode_setting_is_preserved_on_reader_import_failure(self):
        self.reader.write_bytes(b'raise ImportError("synthetic reader failure")\n')
        for setting in (False, True):
            with self.subTest(setting=setting):
                sys.dont_write_bytecode = setting
                self.assertIsNone(self.load().evidence)
                self.assertIs(sys.dont_write_bytecode, setting)

    def test_missing_reader_cannot_be_replaced_by_orphan_cache(self):
        self.cached(b'VALUE = "old"\n', b'VALUE = "new"\n')
        self.reader.unlink()
        before = self.inventory()
        self.assertIsNone(self.load().evidence)
        self.assertEqual(self.inventory(), before)

    def test_oversized_reader_is_not_executed(self):
        # Side effect is confined to a test-owned directory; it must never happen.
        marker = self.root / 'unexpected-execution'
        raw = ('from pathlib import Path\nPath(%r).write_text("unexpected")\n' % str(marker)).encode()
        self.reader.write_bytes(raw + b'#' * 65_537)
        self.assertIsNone(self.load().evidence)
        self.assertFalse(marker.exists())

    def test_directory_and_symlink_readers_are_refused(self):
        self.reader.mkdir()
        self.assertIsNone(self.load().evidence)
        self.reader.rmdir()
        other = self.root / 'outside-reader.py'
        other.write_bytes(b'VALUE = "unexpected"\n')
        try:
            self.reader.symlink_to(other)
        except OSError:
            self.skipTest('symlinks unavailable')
        self.assertIsNone(self.load().evidence)

    def test_cli_emits_no_source_when_current_reader_is_invalid(self):
        self.cached(b'VALUE = "old"\n', b'not valid python!!!\n',
                    py_compile.PycInvalidationMode.UNCHECKED_HASH)
        before = self.inventory()
        run = subprocess.run([sys.executable, str(self.helper), '--root', str(self.root),
                              '--span', 'not-read.txt', '1', '1', 'sha256:' + '0' * 64],
                             capture_output=True, timeout=10)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, b'')
        self.assertEqual(json.loads(run.stderr),
                         {'kind': 'source-excerpt-error', 'code': 'reader-unavailable'})
        self.assertEqual(self.inventory(), before)

    def test_old_cached_side_effect_is_not_executed(self):
        marker = self.root / 'cached-side-effect'
        old = ('from pathlib import Path\nPath(%r).write_text("unexpected")\nVALUE = "old"\n'
               % str(marker)).encode()
        self.cached(old, b'VALUE = "current"\n', py_compile.PycInvalidationMode.UNCHECKED_HASH)
        before = self.inventory()
        self.assertEqual(self.load().evidence.VALUE, 'current')
        self.assertFalse(marker.exists())
        self.assertEqual(self.inventory(), before)


if __name__ == '__main__':
    unittest.main()
