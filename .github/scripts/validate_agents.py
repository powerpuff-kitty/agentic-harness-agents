#!/usr/bin/env python3
"""Retain existing validation and add checks for the shipped native adapter assets."""
from pathlib import Path
import runpy
import unittest

from validate_adapter_assets import validate_repository

HERE = Path(__file__).resolve().parent
runpy.run_path(str(HERE / '_validate_agents_structure.py'), run_name='__main__')
errors = validate_repository()
if errors:
    raise SystemExit('\n'.join(errors))
suite = unittest.defaultTestLoader.discover(str(HERE), pattern='test_adapter_assets.py')
if not unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful():
    raise SystemExit(1)
print('Native adapter assets verified; live-host delivery and enforcement remain unverified')
