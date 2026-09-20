"""Declared graph inspection tests; no inference, scheduler or project checks."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / 'skills/decision-intelligence/scripts/review_graph.py'
spec = importlib.util.spec_from_file_location('graph_review', HELPER)
graph = importlib.util.module_from_spec(spec)
spec.loader.exec_module(graph)


def fixture():
    return {'format_version': 1, 'kind': 'decision-graph', 'id': 'review.sample', 'revision': 1,
            'nodes': [
                {'id': 'a', 'spec_id': 'evidence.support', 'spec_revision': 1, 'depends_on': []},
                {'id': 'b', 'spec_id': 'evidence.support', 'spec_revision': 1, 'depends_on': []},
                {'id': 'c', 'spec_id': 'triage.gap', 'spec_revision': 2, 'depends_on': ['b']}],
            'reducers': [{'id': 'summary', 'type': 'deterministic', 'inputs': ['a', 'c']}]}


def review(value, width=4):
    return graph.inspect(graph.encoded(value), width)


class DecisionGraphReview(unittest.TestCase):
    def test_layers_preserve_dependencies(self):
        result = review(fixture())
        self.assertEqual(result['layers'], [{'depth': 0, 'groups': [['a', 'b']]},
                                           {'depth': 1, 'groups': [['c']]}])
        self.assertEqual(result['reducers'][0]['declared_inputs_after_layer'], 1)

    def test_repeated_specs_are_not_deduplicated(self):
        result = review(fixture())
        self.assertEqual(result['counts']['nodes'], 3)
        self.assertEqual(result['repeated_spec_references'][0]['nodes'], ['a', 'b'])

    def test_group_width_does_not_change_layers(self):
        result = review(fixture(), 1)
        self.assertEqual(result['layers'][0]['groups'], [['a'], ['b']])
        self.assertEqual(result['layers'][1]['groups'], [['c']])
        self.assertFalse(result['boundaries']['batching_authorized'])

    def test_identical_bytes_are_deterministic(self):
        self.assertEqual(review(fixture()), review(fixture()))

    def test_node_order_only_changes_source_fingerprint(self):
        value = fixture()
        one = review(value)
        value['nodes'].reverse()
        two = review(value)
        self.assertNotEqual(one.pop('source'), two.pop('source'))
        self.assertEqual(one, two)

    def test_full_source_bytes_are_fingerprinted(self):
        data = graph.encoded(fixture())
        result = graph.inspect(data)
        self.assertEqual(result['source'], {'bytes': len(data), 'sha256':
                         'sha256:' + hashlib.sha256(data).hexdigest()})

    def test_unknown_dependency_blocks_all_groups(self):
        value = fixture()
        value['nodes'][2]['depends_on'] = ['absent']
        result = review(value)
        self.assertIn('unknown-dependency', result['problems'])
        self.assertEqual(result['layers'], [])
        self.assertEqual(result['reducers'], [])

    def test_self_dependency_is_explicit(self):
        value = fixture()
        value['nodes'][0]['depends_on'] = ['a']
        self.assertIn('self-dependency', review(value)['problems'])

    def test_cycle_discards_even_acyclic_prefix(self):
        value = fixture()
        value['nodes'][1]['depends_on'] = ['c']
        result = review(value)
        self.assertIn('cycle-or-cycle-blocked-nodes', result['problems'])
        self.assertEqual(result['layers'], [])

    def test_duplicate_nodes_rejected(self):
        value = fixture()
        value['nodes'].append(copy.deepcopy(value['nodes'][0]))
        with self.assertRaisesRegex(graph.GraphError, 'duplicate-node'):
            review(value)

    def test_duplicate_dependencies_rejected(self):
        value = fixture()
        value['nodes'][2]['depends_on'] = ['b', 'b']
        with self.assertRaisesRegex(graph.GraphError, 'duplicate-reference'):
            review(value)

    def test_unknown_reducer_input_blocks(self):
        value = fixture()
        value['reducers'][0]['inputs'] = ['missing']
        self.assertIn('unknown-reducer-input', review(value)['problems'])

    def test_reducer_cannot_reference_another_reducer(self):
        value = fixture()
        value['reducers'].append({'id': 'other', 'type': 'deterministic', 'inputs': ['summary']})
        self.assertEqual(review(value)['status'], 'blocked')

    def test_duplicate_reducers_rejected(self):
        value = fixture()
        value['reducers'].append(copy.deepcopy(value['reducers'][0]))
        self.assertIn('duplicate-reducer', review(value)['problems'])

    def test_nondeterministic_reducer_rejected(self):
        value = fixture()
        value['reducers'][0]['type'] = 'semantic'
        with self.assertRaisesRegex(graph.GraphError, 'unsupported-reducer'):
            review(value)

    def test_extension_fields_cannot_hide_semantics(self):
        for target in ('graph', 'node', 'reducer'):
            value = fixture()
            obj = value if target == 'graph' else value['nodes' if target == 'node' else 'reducers'][0]
            obj['execute'] = 'untrusted arbitrary command'
            with self.subTest(target=target), self.assertRaisesRegex(graph.GraphError, 'unsupported-fields'):
                review(value)

    def test_boolean_versions_and_revisions_rejected(self):
        for obj in ('graph', 'node'):
            value = fixture()
            if obj == 'graph':
                value['revision'] = True
            else:
                value['nodes'][0]['spec_revision'] = True
            with self.assertRaises(graph.GraphError):
                review(value)
        value = fixture()
        value['format_version'] = True
        with self.assertRaises(graph.GraphError):
            review(value)

    def test_invalid_group_limits(self):
        for width in (True, 0, -1, 33, '4', 1.5):
            with self.subTest(width=width), self.assertRaises(graph.GraphError):
                review(fixture(), width)

    def test_wrong_contract_rejected(self):
        value = fixture()
        value['kind'] = 'decision-receipt'
        with self.assertRaisesRegex(graph.GraphError, 'unsupported-contract'):
            review(value)

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaisesRegex(graph.GraphError, 'duplicate-json-key'):
            graph.inspect(b'{"kind":1,"kind":2}')

    def test_nonfinite_and_malformed_input_rejected(self):
        for data in (b'NaN', b'Infinity', b'-Infinity', b'\x00', b'\xff', b'[', b'[]', b'null', b'1' * 5000):
            with self.subTest(data=data[:10]), self.assertRaises(graph.GraphError):
                graph.inspect(data)

    def test_node_and_edge_bounds(self):
        for count, cap in ((129, 'node-count-limit'), (100, 'edge-count-limit')):
            value = fixture()
            value['nodes'] = [{'id': f'n{i}', 'spec_id': 'x', 'spec_revision': 1,
                               'depends_on': [f'n{j}' for j in range(i)]} for i in range(count)]
            with self.assertRaisesRegex(graph.GraphError, cap):
                review(value)

    def test_reducer_count_bound(self):
        value = fixture()
        value['reducers'] *= 33
        with self.assertRaisesRegex(graph.GraphError, 'reducer-count-limit'):
            review(value)

    def test_input_size_bound(self):
        with self.assertRaisesRegex(graph.GraphError, 'input-size-limit'):
            graph.inspect(b' ' * (graph.MAX_BYTES + 1))

    def test_missing_fields_and_bad_labels(self):
        for value in ({}, {'kind': 'decision-graph'}):
            with self.assertRaises(graph.GraphError):
                review(value)
        for bad in ('', 'A', 'a\n', 'x' * 257, []):
            value = fixture()
            value['nodes'][0]['id'] = bad
            with self.assertRaises(graph.GraphError):
                review(value)

    def test_empty_graph_and_empty_reducer_inputs_rejected(self):
        value = fixture()
        value['nodes'] = []
        with self.assertRaises(graph.GraphError):
            review(value)
        value = fixture()
        value['reducers'][0]['inputs'] = []
        with self.assertRaises(graph.GraphError):
            review(value)

    def test_random_acyclic_graphs_preserve_every_edge_and_node(self):
        rng = random.Random(731)
        for _ in range(30):
            n = rng.randrange(1, 60)
            nodes = [{'id': f'n{i}', 'spec_id': 'same', 'spec_revision': 1,
                      'depends_on': [f'n{j}' for j in range(i) if rng.random() < 0.1]} for i in range(n)]
            value = fixture()
            value.update(nodes=nodes, reducers=[])
            result = review(value, rng.randrange(1, 33))
            depths = {node: layer['depth'] for layer in result['layers'] for group in layer['groups'] for node in group}
            self.assertEqual(len(depths), n)
            for node in nodes:
                for dep in node['depends_on']:
                    self.assertLess(depths[dep], depths[node['id']])

    def test_matching_spec_revisions_are_not_conflated(self):
        value = fixture()
        value['nodes'][1]['spec_revision'] = 2
        self.assertEqual(review(value)['repeated_spec_references'], [])

    def test_state_provider_and_authority_remain_unverified(self):
        boundaries = review(fixture())['boundaries']
        self.assertEqual(boundaries['execution'], 'not-performed')
        self.assertEqual(boundaries['scope'], 'declared-dependencies-only')
        self.assertTrue(all(value is False for key, value in boundaries.items() if key not in ('scope', 'execution')))

    def test_record_references_do_not_trigger_reads(self):
        value = fixture()
        value['nodes'][0]['spec_id'] = '/nonexistent/spec.json'
        self.assertEqual(review(value)['status'], 'reviewable')
        self.assertFalse(review(value)['boundaries']['spec_contents_checked'])

    def test_actual_copied_helper_subprocess_and_no_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            helper = root / 'review_graph.py'
            shutil.copyfile(HELPER, helper)
            source = root / 'graph.json'
            data = graph.encoded(fixture())
            source.write_bytes(data)
            run = subprocess.run([sys.executable, str(helper), str(source), '--group-size', '1'],
                                 capture_output=True, timeout=10)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)['layers'][0]['groups'], [['a'], ['b']])
            self.assertEqual(set(p.name for p in root.iterdir()), {'graph.json', 'review_graph.py'})
            self.assertEqual(source.read_bytes(), data)
            self.assertNotIn(str(root).encode(), run.stdout)

    def test_actual_blocked_and_invalid_exit_codes(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / 'graph.json'
            value = fixture()
            value['nodes'][0]['depends_on'] = ['missing']
            source.write_bytes(graph.encoded(value))
            run = subprocess.run([sys.executable, str(HELPER), str(source)], capture_output=True, timeout=10)
            self.assertEqual(run.returncode, 1)
            self.assertEqual(json.loads(run.stdout)['layers'], [])
            source.write_bytes(b'private source marker invalid JSON')
            run = subprocess.run([sys.executable, str(HELPER), str(source)], capture_output=True, timeout=10)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(run.stdout, b'')
            self.assertNotIn(b'private source marker', run.stderr)
            self.assertNotIn(str(source).encode(), run.stderr)

    def test_linked_file_parent_and_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            folder = root / 'real'
            folder.mkdir()
            source = folder / 'graph.json'
            source.write_bytes(graph.encoded(fixture()))
            linked = root / 'link'
            try:
                linked.symlink_to(folder, target_is_directory=True)
            except OSError:
                self.skipTest('symlinks unavailable')
            for path in (linked / 'graph.json', folder / '..' / 'real' / 'graph.json'):
                with self.assertRaises(graph.GraphError):
                    graph.read_graph(path)
            direct = root / 'direct'
            direct.symlink_to(source)
            with self.assertRaises(graph.GraphError):
                graph.read_graph(direct)

    def test_unavailable_directory_fifo_and_large_input(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for path in (root / 'missing', root):
                with self.assertRaises(graph.GraphError):
                    graph.read_graph(path)
            source = root / 'large'
            source.write_bytes(b'x' * (graph.MAX_BYTES + 1))
            with self.assertRaises(graph.GraphError):
                graph.read_graph(source)
            if hasattr(os, 'mkfifo'):
                pipe = root / 'pipe'
                os.mkfifo(pipe)
                with self.assertRaises(graph.GraphError):
                    graph.read_graph(pipe)


if __name__ == '__main__':
    unittest.main()
