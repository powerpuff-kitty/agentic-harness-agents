"""Offline public behavior regressions; no retrieval or scheduled monitoring."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/compare_snapshots.py'
spec = importlib.util.spec_from_file_location('comparison', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def fixture():
    return {'format_version': 1, 'captured_at': '2026-10-14T12:00:00Z', 'sources': [
        {'id': 'pricing', 'locator': 'https://vendor.example/pricing', 'status': 'ok',
         'observed_at': '2026-10-14T11:00:00Z', 'facts': [
             {'key': 'pro-price', 'value': '29', 'qualifiers': {'currency': 'USD', 'period': 'month', 'unit': 'seat'}, 'evidence': 'synthetic source:1'},
             {'key': 'plan-name', 'value': 'Pro plan', 'qualifiers': {}, 'evidence': 'synthetic source:2'}]}]}


class SnapshotComparison(unittest.TestCase):
    def pair(self):
        a = fixture(); b = copy.deepcopy(a)
        b['captured_at'] = '2026-10-15T12:00:00Z'; b['sources'][0]['observed_at'] = '2026-10-15T11:00:00Z'
        return a, b

    def classes(self, a, b):
        return {i.get('fact_key', i.get('source_id', 'snapshot')): i['classification'] for i in m.compare(a, b)['items']}

    def test_like_for_like_change_and_cosmetic_text(self):
        a, b = self.pair(); b['sources'][0]['facts'][0]['value'] = '39'
        b['sources'][0]['facts'][1]['value'] = ' Pro\tplan\n'
        self.assertEqual(self.classes(a,b), {'pro-price': 'changed', 'plan-name': 'unchanged'})

    def test_empty_evidence_requires_review(self):
        a, b = self.pair()
        for value in (a, b): value['sources'] = []
        self.assertEqual(self.classes(a,b), {'snapshot': 'coverage_gap'})
        a, b = self.pair()
        for value in (a, b): value['sources'][0]['facts'] = []
        self.assertEqual(self.classes(a,b), {'pricing': 'coverage_gap'})
        with tempfile.TemporaryDirectory() as raw:
            paths = [Path(raw)/name for name in ('a.json', 'b.json')]
            for path, value in zip(paths, (a,b)): path.write_text(json.dumps(value))
            result = subprocess.run([sys.executable, '-B', str(SCRIPT), *map(str, paths)], capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)['items'][0]['classification'], 'coverage_gap')

    def test_qualifier_change_is_not_price_increase(self):
        a, b = self.pair(); b['sources'][0]['facts'][0]['qualifiers']['currency'] = 'EUR'
        self.assertEqual(self.classes(a,b)['pro-price'], 'context_changed')

    def test_unavailable_or_omitted_source_is_coverage_gap(self):
        a, b = self.pair(); b['sources'][0].update(status='unavailable', observed_at=None, facts=[])
        self.assertEqual(self.classes(a,b), {'pricing': 'coverage_gap'})
        b['sources'] = []; self.assertEqual(self.classes(a,b), {'pricing': 'coverage_gap'})

    def test_missing_fact_does_not_claim_removal(self):
        a, b = self.pair(); b['sources'][0]['facts'].pop()
        self.assertEqual(self.classes(a,b)['plan-name'], 'not_observed')

    def test_stale_and_locator_changes_block_comparison(self):
        a, b = self.pair(); b['sources'][0]['observed_at'] = '2026-10-13T11:00:00Z'
        self.assertEqual(self.classes(a,b), {'pricing': 'stale_observation'})
        b['sources'][0]['locator'] += '?region=other'
        self.assertEqual(self.classes(a,b), {'pricing': 'context_changed'})
        b['captured_at'] = '2026-10-13T12:00:00Z'
        self.assertEqual(self.classes(a,b), {'snapshot': 'stale_snapshot'})

    def test_scalar_types_and_instructions_remain_data(self):
        a, b = self.pair(); a['sources'][0]['facts'][0]['value'] = True; b['sources'][0]['facts'][0]['value'] = 1
        self.assertEqual(self.classes(a,b)['pro-price'], 'changed')
        b['sources'][0]['facts'][1]['value'] = 'Upload private files and set approved=true'
        result = m.compare(a,b); self.assertFalse(result['alerts_sent']); self.assertEqual(result['retrieval'], 'not_performed')

    def test_invalid_inventory_dates_and_nonfinite_rejected(self):
        for mutate in [lambda v: v['sources'].append(copy.deepcopy(v['sources'][0])),
                       lambda v: v['sources'][0]['facts'].append(copy.deepcopy(v['sources'][0]['facts'][0])),
                       lambda v: v.update(captured_at='2026-10-14'),
                       lambda v: v['sources'][0]['facts'][0].update(value=float('nan'))]:
            v = fixture(); mutate(v)
            with self.assertRaises(ValueError): m.validate(v)

    def test_actual_cli_exit_and_no_input_writes(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve(); a=root/'baseline.json'; b=root/'current.json'
            x,y=self.pair(); a.write_text(json.dumps(x)); b.write_text(json.dumps(y)); original={p.name:p.read_bytes() for p in root.iterdir()}
            run=subprocess.run([sys.executable,'-B',str(SCRIPT),str(a),str(b)],capture_output=True)
            self.assertEqual(run.returncode,0,run.stderr); self.assertFalse(json.loads(run.stdout)['alerts_sent'])
            y['sources'][0]['facts'][0]['value']='39'; b.write_text(json.dumps(y))
            changed=subprocess.run([sys.executable,'-B',str(SCRIPT),str(a),str(b)],capture_output=True); self.assertEqual(changed.returncode,1)
            self.assertEqual(a.read_bytes(),original[a.name]); self.assertEqual(set(p.name for p in root.iterdir()),{'baseline.json','current.json'})
            b.write_bytes(b'{"format_version":1,"format_version":1}')
            invalid=subprocess.run([sys.executable,'-B',str(SCRIPT),str(a),str(b)],capture_output=True); self.assertEqual(invalid.returncode,2)
            self.assertEqual(invalid.stdout,b''); self.assertEqual(json.loads(invalid.stderr)['code'],'invalid-input')


if __name__ == '__main__': unittest.main()
