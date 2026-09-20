"""Definition navigation and actual excerpt workflows; not model-performance trials."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / 'skills/agentic-improvement/scripts/extract_context.py'
READER = HELPER.with_name('evidence_snapshot.py')
extractor = types.ModuleType('outline_under_test')
extractor.__file__ = str(HELPER)
exec(compile(HELPER.read_bytes(), str(HELPER), 'exec'), extractor.__dict__)


def digest(raw):
    return 'sha256:' + hashlib.sha256(raw).hexdigest()


class PythonOutline(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.raw = b'def first():\n    return 1\n\ndef second():\n    return 2\n'
        self.pin = self.put('source.py', self.raw)

    def put(self, name, raw):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        return digest(raw)

    def run_helper(self, *args, helper=HELPER):
        return subprocess.run([sys.executable, str(helper), '--root', str(self.root), *args],
                              capture_output=True, timeout=10)

    def outline(self, selections=None, budget=65536):
        return extractor.outline(self.root, selections or [['source.py', self.pin]], budget)

    def test_names_and_exact_inclusive_ranges(self):
        result = self.outline()
        items = result['files'][0]['definitions']
        self.assertEqual([(i['name'], i['start_line'], i['end_line']) for i in items],
                         [('first', 1, 2), ('second', 4, 5)])
        self.assertEqual(result['files'][0]['sha256'], self.pin)
        self.assertEqual(result['files'][0]['total_lines'], 5)
        self.assertEqual(result['parser']['version'], sys.version.split()[0])

    def test_nested_class_async_and_function_parent_identities(self):
        raw = b'class Client:\n    async def fetch(self):\n        def decode():\n            return 1\n        return decode()\n'
        pin = self.put('source.py', raw)
        items = self.outline([['source.py', pin]])['files'][0]['definitions']
        self.assertEqual([i['qualified_name'] for i in items],
                         ['Client', 'Client.fetch', 'Client.fetch.<locals>.decode'])
        self.assertEqual([i['kind'] for i in items], ['class', 'async-function', 'function'])
        self.assertIsNone(items[0]['parent_id'])
        self.assertEqual(items[1]['parent_id'], items[0]['id'])
        self.assertEqual(items[2]['parent_id'], items[1]['id'])

    def test_parenthesized_multiline_decorator_includes_at_line(self):
        raw = b'@(\n    decorate\n)\n@other(\n    value=1\n)\nasync def work():\n    return 1\n'
        pin = self.put('source.py', raw)
        item = self.outline([['source.py', pin]])['files'][0]['definitions'][0]
        self.assertEqual((item['start_line'], item['definition_line'], item['end_line']), (1, 7, 8))
        self.assertEqual(item['decorator_count'], 2)
        span = ['source.py', item['start_line'], item['end_line'], pin]
        actual = extractor.extract(self.root, [span], required_spans=[span])
        self.assertEqual(actual['files'][0]['excerpts'][0]['text'].encode(), raw)

    def test_decorator_comments_blank_lines_and_indentation(self):
        raw = b'class Box:\n    @first\n    # keep qualifier\n\n    @(\n        second\n    )\n    def item(self):\n        pass\n'
        pin = self.put('source.py', raw)
        items = self.outline([['source.py', pin]])['files'][0]['definitions']
        self.assertEqual(items[1]['start_line'], 2)
        self.assertEqual(items[1]['definition_line'], 8)
        self.assertEqual(items[1]['end_line'], 9)

    def test_matrix_operator_and_docstring_cannot_invent_definitions(self):
        raw = b'"""def imaginary():\n @fake\n"""\nx = (left\n @ right)\ndef real():\n    return "def fake():"\n'
        pin = self.put('source.py', raw)
        items = self.outline([['source.py', pin]])['files'][0]['definitions']
        self.assertEqual([(i['name'], i['start_line']) for i in items], [('real', 6)])

    def test_duplicate_conditional_names_remain_distinct(self):
        raw = b'if flag:\n    def choose(): return 1\nelse:\n    def choose(): return 2\n'
        pin = self.put('source.py', raw)
        items = self.outline([['source.py', pin]])['files'][0]['definitions']
        self.assertEqual([i['name'] for i in items], ['choose', 'choose'])
        self.assertNotEqual(items[0]['id'], items[1]['id'])
        self.assertFalse(self.outline([['source.py', pin]])['limits']['dependencies_resolved'])

    def test_utf8_bom_crlf_and_missing_final_newline_use_extractor_lines(self):
        raw = '\ufeff@tag\r\ndef café():\r\n    return "例\u2028text"'.encode()
        pin = self.put('source.py', raw)
        item = self.outline([['source.py', pin]])['files'][0]['definitions'][0]
        self.assertEqual(item['name'], 'café')
        self.assertEqual((item['start_line'], item['end_line']), (1, 3))
        value = extractor.extract(self.root, [['source.py', 1, 3, pin]])
        self.assertEqual(value['files'][0]['excerpts'][0]['text'].encode(), raw)

    def test_bare_cr_is_rejected_instead_of_misaligned_ranges(self):
        pin = self.put('source.py', b'def f():\r    return 1\r')
        with self.assertRaisesRegex(extractor.OutlineError, 'unsupported-line-endings'):
            self.outline([['source.py', pin]])

    def test_unsupported_language_fails_before_target_read(self):
        with patch.object(extractor.evidence, 'read_text', side_effect=AssertionError('no reads')):
            for path in ('source.ts', 'source.vue', 'README.md'):
                with self.assertRaisesRegex(extractor.OutlineError, 'unsupported-language'):
                    self.outline([[path, self.pin]])

    def test_syntax_error_has_no_source_leak(self):
        pin = self.put('source.py', b'def dont_leak_this(:\n')
        run = self.run_helper('--outline', 'source.py', pin)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, b'')
        self.assertEqual(json.loads(run.stderr)['code'], 'unsupported-python-source')
        self.assertNotIn(b'dont_leak_this', run.stderr)

    def test_empty_and_non_definition_modules_are_explicitly_partial(self):
        for raw in (b'', b'x = 1\n', b'# no definitions\n'):
            pin = self.put('source.py', raw)
            result = self.outline([['source.py', pin]])
            self.assertEqual(result['files'][0]['definitions'], [])
            self.assertEqual(result['limits']['coverage'], 'named-definitions-only')
            self.assertFalse(result['limits']['required_evidence_emitted'])
            self.assertIsNone(result['limits']['evidence_sufficient'])

    def test_default_literals_docstrings_and_bodies_are_not_returned(self):
        raw = b'def f(value="PRIVATE_DEFAULT"):\n    "PRIVATE_DOCSTRING"\n    return "PRIVATE_BODY"\n'
        pin = self.put('source.py', raw)
        data = extractor.evidence.encoded(self.outline([['source.py', pin]]))
        for word in (b'PRIVATE_DEFAULT', b'PRIVATE_DOCSTRING', b'PRIVATE_BODY'):
            self.assertNotIn(word, data)

    def test_parser_warnings_cannot_echo_source_literals(self):
        raw = b'value = "PRIVATE_LITERAL\\q"\n' + self.raw
        pin = self.put('source.py', raw)
        run = subprocess.run([sys.executable, '-W', 'always', str(HELPER), '--root', str(self.root),
                              '--outline', 'source.py', pin], capture_output=True, timeout=10)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stderr, b'')
        self.assertNotIn(b'PRIVATE_LITERAL', run.stdout)

    def test_target_module_and_decorators_never_execute(self):
        marker = self.root / 'target-executed'
        raw = ('from pathlib import Path\nPath(%r).write_text("bad")\n'
               '@unavailable_decorator()\ndef f(): return 1\n' % str(marker)).encode()
        pin = self.put('source.py', raw)
        run = self.run_helper('--outline', 'source.py', pin)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse(marker.exists())
        self.assertEqual((self.root / 'source.py').read_bytes(), raw)

    def test_repeated_file_is_read_once_without_discovery(self):
        self.put('unselected.py', b'raise RuntimeError("not selected")\n')
        with patch.object(extractor.evidence, 'read_text', wraps=extractor.evidence.read_text) as read:
            result = self.outline([['source.py', self.pin]] * 2)
        self.assertEqual(read.call_count, 1)
        self.assertEqual(read.call_args.args[0], self.root / 'source.py')
        self.assertEqual(len(result['files']), 1)

    def test_multiple_file_order_is_stable_and_identity_is_not_collapsed(self):
        self.put('other.py', self.raw)
        selections = [['source.py', self.pin], ['other.py', self.pin]]
        result = self.outline(selections)
        self.assertEqual(result, self.outline(list(reversed(selections))))
        self.assertEqual([item['path'] for item in result['files']], ['other.py', 'source.py'])

    def test_pin_conflict_and_alias_fail_before_reads(self):
        for selections in ([['source.py', self.pin], ['source.py', digest(b'other')]],
                           [['source.py', self.pin], ['SOURCE.py', self.pin]]):
            with patch.object(extractor.evidence, 'read_text', side_effect=AssertionError('no reads')):
                with self.assertRaises(ValueError):
                    self.outline(selections)

    def test_same_size_restored_mtime_change_refuses_outline(self):
        path = self.root / 'source.py'
        before = path.stat()
        path.write_bytes(self.raw.replace(b'return 1', b'return 9'))
        os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
        run = self.run_helper('--outline', 'source.py', self.pin)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, b'')

    def test_later_invalid_file_prevents_partial_outline(self):
        pin = self.put('z.py', b'def broken(:\n')
        run = self.run_helper('--outline', 'source.py', self.pin, '--outline', 'z.py', pin)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, b'')
        self.assertNotIn(b'first', run.stderr)

    def test_limits_reject_invalid_inputs(self):
        for selections in ([], None, {}, [['source.py']], [['source.py', 'not-a-pin']],
                           [['../source.py', self.pin]], [['source.py', self.pin]] * 129):
            with self.subTest(selection=str(selections)[:50]), self.assertRaises(ValueError):
                extractor.outline(self.root, selections)
        for budget in (0, -1, True, 1.0, None, extractor.MAX_BUDGET + 1):
            with self.assertRaises(ValueError):
                self.outline(budget=budget)

    def test_byte_and_aggregate_read_limits(self):
        with patch.object(extractor, 'MAX_OUTLINE_FILE_BYTES', 2), self.assertRaises(ValueError):
            self.outline()
        self.put('other.py', self.raw)
        with patch.object(extractor.evidence, 'MAX_TOTAL_BYTES', len(self.raw)), self.assertRaises(ValueError):
            self.outline([['source.py', self.pin], ['other.py', self.pin]])

    def test_node_definition_and_name_limits(self):
        with patch.object(extractor, 'MAX_OUTLINE_AST_NODES', 2), self.assertRaisesRegex(ValueError, 'outline-structure-limit'):
            self.outline()
        with patch.object(extractor, 'MAX_OUTLINE_DEFINITIONS', 1), self.assertRaisesRegex(ValueError, 'outline-structure-limit'):
            self.outline()
        pin = self.put('source.py', ('def ' + 'a' * 513 + '(): pass\n').encode())
        with self.assertRaisesRegex(ValueError, 'outline-structure-limit'):
            self.outline([['source.py', pin]])

    def test_budget_defers_all_metadata_without_false_evidence_delivery(self):
        run = self.run_helper('--outline', 'source.py', self.pin, '--budget-bytes', '1')
        self.assertEqual(run.returncode, 1, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result['files'], [])
        self.assertFalse(result['required_evidence_emitted'])
        self.assertNotIn(b'first', run.stdout)
        self.assertGreater(result['required_output_bytes'], 1)

    def test_budget_counts_the_complete_envelope(self):
        result = self.outline()
        budget = len(extractor.evidence.encoded(result))
        for _ in range(4):
            result['measurement']['budget_bytes'] = budget
            budget = len(extractor.evidence.encoded(result))
        self.assertEqual(self.outline(budget=budget)['status'], 'ready')
        self.assertEqual(self.outline(budget=budget - 1)['status'], 'budget-exceeded')

    def test_cli_modes_and_required_evidence_are_not_interchangeable(self):
        for args in (['--outline', 'source.py', self.pin, '--span', 'source.py', '1', '2', self.pin],
                     ['--outline', 'source.py', self.pin, '--require-span', 'source.py', '1', '2', self.pin]):
            run = self.run_helper(*args)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(run.stdout, b'')

    def test_symlink_source_and_linked_parent_are_rejected(self):
        try:
            (self.root / 'alias.py').symlink_to(self.root / 'source.py')
            (self.root / 'linked').symlink_to(self.root, target_is_directory=True)
        except OSError:
            self.skipTest('symlinks unavailable')
        for path in ('alias.py', 'linked/source.py'):
            with self.assertRaises(ValueError):
                self.outline([[path, self.pin]])

    def test_real_capture_outline_guarded_extraction_and_stale_refusal(self):
        folder = self.root / 'helpers'
        folder.mkdir()
        for source in (HELPER, READER):
            shutil.copyfile(source, folder / source.name)
        raw = b'@reviewed\ndef target():\n    return 42\n\ndef unrelated():\n    return "skip"\n'
        self.put('source.py', raw)
        before = {p.relative_to(self.root).as_posix(): p.read_bytes()
                  for p in self.root.rglob('*') if p.is_file()}
        capture = subprocess.run([sys.executable, str(folder / READER.name), 'capture', '--root',
                                  str(self.root), '--scope', 'outline fixture', '--file', 'source.py'],
                                 capture_output=True, timeout=10)
        self.assertEqual(capture.returncode, 0, capture.stderr)
        pin = json.loads(capture.stdout)['files'][0]['sha256']
        mapped = self.run_helper('--outline', 'source.py', pin, helper=folder / HELPER.name)
        self.assertEqual(mapped.returncode, 0, mapped.stderr)
        definition = json.loads(mapped.stdout)['files'][0]['definitions'][0]
        span = ['source.py', str(definition['start_line']), str(definition['end_line']), pin]
        excerpt = self.run_helper('--span', *span, '--require-span', *span, helper=folder / HELPER.name)
        self.assertEqual(excerpt.returncode, 0, excerpt.stderr)
        value = json.loads(excerpt.stdout)
        self.assertEqual(value['files'][0]['excerpts'][0]['text'].encode(), b'@reviewed\ndef target():\n    return 42\n')
        self.assertTrue(value['required_evidence']['emitted'])
        after = {p.relative_to(self.root).as_posix(): p.read_bytes()
                 for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(after, before)
        self.assertEqual(list(folder.rglob('*.pyc')), [])
        self.put('source.py', raw.replace(b'return 42', b'return 99'))
        stale = self.run_helper('--span', *span, '--require-span', *span, helper=folder / HELPER.name)
        self.assertEqual(stale.returncode, 2)
        self.assertEqual(stale.stdout, b'')


if __name__ == '__main__':
    unittest.main()
