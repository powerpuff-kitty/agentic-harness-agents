#!/usr/bin/env python3
"""Retain structural checks and validate native assets plus declared skill bundles."""
from pathlib import Path
import runpy
import unittest

from validate_adapter_assets import validate_repository
from skill_bundle import build_archive, enrolled, verify_archive

HERE = Path(__file__).resolve().parent
runpy.run_path(str(HERE / '_validate_agents_structure.py'), run_name='__main__')
errors = validate_repository()
if errors:
    raise SystemExit('\n'.join(errors))
for pattern in ['test_adapter_assets.py', 'test_skill_bundles.py', 'test_guidance_efficiency.py',
                'test_guidance_comparison.py', 'test_skill_entrypoints.py', 'test_context_scope.py',
                'test_guidance_trial.py', 'test_lifecycle_guidance.py',
                'test_compact_log.py', 'test_optional_script_bundles.py',
                'test_evidence_snapshot.py', 'test_evidence_snapshot_budget.py',
                'test_evidence_snapshot_distribution.py', 'test_decision_graph_review.py',
                'test_decision_graph_distribution.py', 'test_source_excerpts.py',
                'test_source_excerpt_distribution.py', 'test_excerpt_reader_source.py',
                'test_required_source_spans.py', 'test_continuation_guidance.py']:
    suite = unittest.defaultTestLoader.discover(str(HERE), pattern=pattern)
    if not unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful():
        raise SystemExit(1)
bundles = enrolled()
for name in bundles:
    verify_archive(build_archive(HERE.parents[1], name))
print(f'{len(bundles)} standalone payloads verified; no model task was executed')
print('Native adapter assets verified; live-host delivery and enforcement remain unverified')
