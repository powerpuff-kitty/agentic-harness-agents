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
                'test_guidance_comparison.py', 'test_skill_entrypoints.py']:
    suite = unittest.defaultTestLoader.discover(str(HERE), pattern=pattern)
    if not unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful():
        raise SystemExit(1)
bundles = enrolled()
for name in bundles:
    verify_archive(build_archive(HERE.parents[1], name))
print(f'{len(bundles)} standalone documentation bundles verified; no model task was executed')
print('Native adapter assets verified; live-host delivery and enforcement remain unverified')
