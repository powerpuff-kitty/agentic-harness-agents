"""Real opt-in compiler trials plus parser-independent guards; never install tools."""
import hashlib
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
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / 'skills/agentic-improvement/scripts'
HELPER = SCRIPTS / 'outline_typescript.py'
module = types.ModuleType('tested_typescript_outline')
module.__file__ = str(HELPER)
exec(compile(HELPER.read_bytes(), str(HELPER), 'exec'), module.__dict__)


def sha(raw):
    return 'sha256:' + hashlib.sha256(raw).hexdigest()


class Guards(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.source = self.root / 'source.ts'
        self.source.write_bytes(b'export function load() { return 42; }\n')
        self.compiler = self.root / 'typescript.js'
        self.compiler.write_bytes(b'module.exports = {};\n')
        self.node = Path(sys.executable)  # Never invoked by preflight refusal tests.
        self.pair = ['source.ts', sha(self.source.read_bytes())]
        self.parser_pin = sha(self.compiler.read_bytes())

    def outline(self, pairs=None, **changes):
        args = {'root': self.root, 'selections': [self.pair] if pairs is None else pairs,
                'node': self.node, 'compiler': self.compiler, 'compiler_pin': self.parser_pin}
        args.update(changes)
        return module.outline(**args)

    def refused_before_process(self, **changes):
        with patch.object(module.subprocess, 'run', side_effect=AssertionError('must not execute')):
            with self.assertRaises((ValueError, OSError)):
                self.outline(**changes)

    def test_rejects_unsupported_and_unsafe_source_paths(self):
        for name in ['source.vue', 'source.py', '../source.ts', '/source.ts', '*.ts', 'a/../source.ts']:
            with self.subTest(name=name):
                self.refused_before_process(pairs=[[name, self.pair[1]]])

    def test_rejects_empty_malformed_and_conflicting_selection(self):
        for pairs in [[], {}, None, [['source.ts']], [self.pair, ['source.ts', 'sha256:' + '0' * 64]],
                      [self.pair, ['SOURCE.ts', self.pair[1]]], [self.pair] * 33]:
            if pairs is None:
                continue  # convenience wrapper uses None for its normal fixture
            with self.subTest(pairs=str(pairs)[:80]):
                self.refused_before_process(pairs=pairs)

    def test_rejects_relative_tool_paths_and_unknown_parser_hash(self):
        self.refused_before_process(node=Path('node'))
        self.refused_before_process(compiler=Path('typescript.js'))
        self.refused_before_process(compiler_pin='unknown')
        self.refused_before_process(compiler_pin='sha256:' + '0' * 64)

    def test_stale_source_same_size_and_restored_timestamp(self):
        meta = self.source.stat()
        self.source.write_bytes(self.source.read_bytes().replace(b'42', b'99'))
        os.utime(self.source, ns=(meta.st_atime_ns, meta.st_mtime_ns))
        self.refused_before_process()

    def test_later_missing_source_prevents_process_execution(self):
        self.refused_before_process(pairs=[self.pair, ['z.ts', 'sha256:' + '0' * 64]])

    def test_source_and_parser_size_limits(self):
        with patch.object(module, 'MAX_FILE_BYTES', 1):
            self.refused_before_process()
        with patch.object(module, 'MAX_PARSER_BYTES', 1):
            self.refused_before_process()
        with patch.object(module, 'MAX_TOTAL_BYTES', 1):
            self.refused_before_process()

    def test_symlink_source_and_parser_refused(self):
        alias = self.root / 'alias.ts'
        try:
            alias.symlink_to(self.source)
        except OSError:
            self.skipTest('symlink unavailable')
        self.refused_before_process(pairs=[['alias.ts', self.pair[1]]])
        parser_alias = self.root / 'alias.js'
        parser_alias.symlink_to(self.compiler)
        self.refused_before_process(compiler=parser_alias)

    def test_no_ambient_credentials_or_node_preloads_forwarded(self):
        with patch.dict(os.environ, {'NODE_OPTIONS': '--require unsafe.js', 'NODE_PATH': '/unsafe',
                                     'TYPESAFE_API_KEY': 'synthetic', 'OPENAI_API_KEY': 'synthetic'}):
            env = module.clean_environment()
        self.assertLessEqual(set(env), {'SystemRoot', 'WINDIR', 'SYSTEMDRIVE'})

    def test_process_timeout_is_fixed_safe_error(self):
        with patch.object(module.subprocess, 'run', side_effect=subprocess.TimeoutExpired('fixture', 15)):
            with self.assertRaisesRegex(module.OutlineError, '^parser-unavailable-or-timeout$'):
                self.outline()

    def test_malformed_parser_output_and_unknown_failure_do_not_leak(self):
        for result in [subprocess.CompletedProcess([], 1, b'SENSITIVE SOURCE', b'SENSITIVE SOURCE'),
                       subprocess.CompletedProcess([], 1, b'{"error":"SENSITIVE SOURCE"}', b''),
                       subprocess.CompletedProcess([], 0, b'{}', b'')]:
            with patch.object(module.subprocess, 'run', return_value=result):
                with self.assertRaises(ValueError) as error:
                    self.outline()
                self.assertNotIn('SENSITIVE', str(error.exception))

    def test_invalid_budget_refused_before_execution(self):
        for budget in [0, -1, True, 1.5, module.MAX_OUTPUT_BYTES + 1]:
            self.refused_before_process(budget=budget)

    def test_current_sibling_source_ignores_unchecked_bytecode(self):
        helper = self.root / HELPER.name
        reader = self.root / 'evidence_snapshot.py'
        shutil.copyfile(HELPER, helper)
        reader.write_bytes(b'VALUE = "old"\n')
        cache = Path(py_compile.compile(str(reader), doraise=True,
                     invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH))
        cache_bytes = cache.read_bytes()
        reader.write_bytes(b'VALUE = "current"\n')
        copy = types.ModuleType('copy')
        copy.__file__ = str(helper)
        exec(compile(helper.read_bytes(), str(helper), 'exec'), copy.__dict__)
        old = sys.dont_write_bytecode
        self.assertEqual(copy.load_reader().VALUE, 'current')
        self.assertEqual(cache.read_bytes(), cache_bytes)
        self.assertIs(sys.dont_write_bytecode, old)

    def test_missing_sibling_does_not_use_pythonpath(self):
        helper = self.root / HELPER.name
        shutil.copyfile(HELPER, helper)
        run = subprocess.run([sys.executable, str(helper), '--root', str(self.root), '--file', *self.pair,
                              '--node', str(self.node), '--typescript', str(self.compiler), self.parser_pin],
                             env=dict(os.environ, PYTHONPATH=str(SCRIPTS)), capture_output=True, timeout=10)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, b'')
        self.assertNotIn(b'export function', run.stderr)


class InstalledCompiler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Only test discovery: production always requires explicit absolute paths and a pin.
        cls.node = shutil.which('node')
        if not cls.node:
            raise unittest.SkipTest('real TypeScript tests require an already-installed Node; no installation attempted')
        supplied = os.environ.get('HARNESS_TEST_TYPESCRIPT')
        if supplied:
            cls.compiler = Path(supplied).resolve()
        else:
            probe = subprocess.run([cls.node, '-e', 'try {process.stdout.write(require.resolve("typescript"))} catch {}'],
                                   capture_output=True, timeout=10, cwd=ROOT)
            if not probe.stdout:
                raise unittest.SkipTest('real parser unavailable; set HARNESS_TEST_TYPESCRIPT to a reviewed installed entry')
            cls.compiler = Path(probe.stdout.decode()).resolve()
        if not cls.compiler.is_file():
            raise unittest.SkipTest('explicit test parser is unavailable')
        cls.pin = sha(cls.compiler.read_bytes())

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.source = self.root / 'source.ts'

    def invoke(self, raw, name='source.ts', extra=(), files=()):
        source = self.root / name
        source.write_bytes(raw)
        command = [sys.executable, str(HELPER), '--root', str(self.root), '--file', name, sha(raw),
                   '--node', self.node, '--typescript', str(self.compiler), self.pin]
        for file, data in files:
            (self.root / file).write_bytes(data)
            command.extend(['--file', file, sha(data)])
        return subprocess.run(command + list(extra), capture_output=True, timeout=20)

    def record(self, raw, name='source.ts'):
        run = self.invoke(raw, name)
        self.assertEqual(run.returncode, 0, run.stderr)
        return json.loads(run.stdout)

    def definitions(self, raw, name='source.ts'):
        return self.record(raw, name)['files'][0]['definitions']

    def test_all_supported_extensions(self):
        for suffix in sorted(module.EXTENSIONS):
            with self.subTest(suffix=suffix):
                definitions = self.definitions(b'export function read() { return 1; }\n', 'source' + suffix)
                self.assertEqual(definitions[0]['name'], 'read')

    def test_types_interfaces_enums_and_namespace(self):
        raw = b'namespace N { interface Api { fetch(): void } type State = { save(): void }; enum E { A } }\n'
        definitions = self.definitions(raw)
        self.assertEqual([d['qualified_name'] for d in definitions], ['N', 'N.Api', 'N.Api.fetch', 'N.State', 'N.State.save', 'N.E'])

    def test_overloads_and_same_line_definitions_keep_distinct_ids(self):
        definitions = self.definitions(b'function parse(x:string):string;\nfunction parse(x:any) {return x;}\nfunction a() {} function b() {}\n')
        self.assertEqual(len({d['id'] for d in definitions}), 4)
        self.assertEqual([d['name'] for d in definitions], ['parse', 'parse', 'a', 'b'])

    def test_decorator_and_split_line_binding_ranges(self):
        definitions = self.definitions(b'@wrap(\n  1\n)\nexport class Api {\n @flag\n async read() {}\n}\nexport const\n make = () => 1;\n')
        self.assertEqual((definitions[0]['start_line'], definitions[0]['end_line']), (1, 7))
        self.assertEqual((definitions[1]['start_line'], definitions[1]['end_line']), (5, 6))
        self.assertEqual((definitions[2]['start_line'], definitions[2]['end_line']), (8, 9))

    def test_callable_bindings_and_nested_callbacks(self):
        raw = b'const outer = (() => { function inner() {} queue(() => {function hidden() {}}); }) satisfies Callable;\n'
        definitions = self.definitions(raw)
        self.assertEqual(definitions[1]['qualified_name'], 'outer.inner')
        self.assertIn('<anonymous@', definitions[2]['qualified_name'])
        self.assertIsNone(definitions[2]['parent_id'])

    def test_methods_getters_setters_and_private_methods(self):
        names = [d['name'] for d in self.definitions(b'class A { constructor() {} get v(){return 1} set v(x:number){} #read(){} }')]
        self.assertEqual(names, ['A', 'constructor', 'v', 'v', '#read'])

    def test_jsx_and_tsx_hide_literals_and_bodies(self):
        for name in ['source.jsx', 'source.tsx']:
            run = self.invoke(b'export const View = () => <div title="PRIVATE_TEXT">SENSITIVE_BODY</div>;', name)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertNotIn(b'PRIVATE_TEXT', run.stdout)
            self.assertNotIn(b'SENSITIVE_BODY', run.stdout)
            self.assertEqual(json.loads(run.stdout)['files'][0]['definitions'][0]['name'], 'View')

    def test_never_executes_target_or_resolves_missing_imports(self):
        raw = b'import missing from "./does-not-exist";\nthrow new Error("TARGET_RAN");\nexport function safe() {}\n'
        run = self.invoke(raw)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertNotIn(b'TARGET_RAN', run.stdout + run.stderr)
        self.assertEqual(json.loads(run.stdout)['files'][0]['definitions'][0]['name'], 'safe')

    def test_later_syntax_error_emits_no_partial_map(self):
        run = self.invoke(b'function secretName() {}', files=[('z.ts', b'const PRIVATE_LITERAL = ;')])
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, b'')
        self.assertNotIn(b'PRIVATE_LITERAL', run.stderr)
        self.assertNotIn(b'secretName', run.stderr)

    def test_budget_defers_whole_map(self):
        run = self.invoke(b'function secretName() {}', extra=['--budget-bytes', '1'])
        self.assertEqual(run.returncode, 1, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result['files'], [])
        self.assertFalse(result['required_evidence_emitted'])
        self.assertNotIn(b'secretName', run.stdout)

    def test_unicode_crlf_and_js_separators_use_lf_ranges(self):
        raw = '\ufefffunction café() {}\r\nfunction x() {}\u2028function y() {}\n'.encode()
        definitions = self.definitions(raw)
        self.assertEqual([d['start_line'] for d in definitions], [1, 2, 2])
        self.assertEqual(definitions[0]['name'], 'café')

    def test_duplicate_requests_read_and_emit_once(self):
        raw = b'export function read() {}\n'
        run = self.invoke(raw, extra=['--file', 'source.ts', sha(raw)])
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(len(result['files']), 1)
        self.assertEqual(result['measurement']['source_bytes_read'], len(raw))

    def test_no_source_or_cache_writes_and_repeatable_output(self):
        raw = b'export function read() {}\n'
        first = self.invoke(raw)
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        second = self.invoke(raw)
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(before, after)
        self.assertEqual(list(self.root.rglob('*.pyc')), [])

    def test_real_parser_identity_and_uncertainty_are_reported(self):
        record = self.record(b'const value = 1;\n')
        self.assertEqual(record['parser']['sha256'], self.pin)
        self.assertTrue(record['parser']['version'].startswith(('5.', '6.')))
        self.assertEqual(record['files'][0]['definitions'], [])
        self.assertIsNone(record['limits']['evidence_sufficient'])
        self.assertIsNone(record['limits']['model_tokens'])
        self.assertEqual(record['limits']['provider_calls'], 0)

    def test_definition_limit_does_not_return_partial_map(self):
        run = self.invoke(b'function a() {}\n' * 2049)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, b'')
        self.assertEqual(json.loads(run.stderr)['code'], 'structure-limit')


if __name__ == '__main__':
    unittest.main()
