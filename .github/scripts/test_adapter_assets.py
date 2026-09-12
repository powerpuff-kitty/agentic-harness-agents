#!/usr/bin/env python3
"""Tests of actual shipped bytes and registry constraints; no coding host is run."""
import copy
import unittest
from validate_adapter_assets import FILES, ROOT, frontmatter, load_bundle, validate_bundle, validate_repository


class AdapterAssetsTests(unittest.TestCase):
    def setUp(self):
        self.index, self.assets = load_bundle()

    def invalid(self):
        self.assertTrue(validate_bundle(self.index, self.assets))

    def test_shipped_bundle_is_valid(self):
        self.assertEqual(validate_bundle(self.index, self.assets), [])

    def test_self_hosting_import_matches_distribution(self):
        self.assertEqual(validate_repository(), [])
        self.assertEqual((ROOT / 'CLAUDE.md').read_text(), '@AGENTS.md\n')

    def test_codex_and_cursor_do_not_install_redundant_root_overrides(self):
        for entry in self.index['adapters'][1:]:
            self.assertEqual(entry['router_loading'], 'native')
            self.assertFalse(any(f['profile'] == 'base' for f in entry['files']))

    def test_scoped_assets_share_body_but_use_different_native_metadata(self):
        a = frontmatter(self.assets[FILES['claude'][-1][0]])
        b = frontmatter(self.assets[FILES['cursor'][-1][0]])
        self.assertNotEqual(a[0], b[0])
        self.assertEqual(a[1], b[1])

    def test_private_or_external_source_paths_cannot_be_declared(self):
        self.index['adapters'][0]['files'][0]['source'] = '../unapproved/file'
        self.invalid()

    def test_canonical_router_is_never_an_install_destination(self):
        self.index['adapters'][0]['files'][0]['target'] = 'AGENTS.md'
        self.invalid()

    def test_settings_hooks_and_override_targets_are_not_permitted(self):
        original = copy.deepcopy(self.index)
        for target in ['.claude/settings.json', '.cursor/rules/override.md', 'AGENTS.override.md']:
            self.index = copy.deepcopy(original)
            self.index['adapters'][0]['files'][0]['target'] = target
            self.invalid()

    def test_duplicate_or_unknown_hosts_are_rejected(self):
        self.index['adapters'][1]['id'] = 'claude'
        self.invalid()

    def test_missing_asset_is_rejected(self):
        self.assets.pop('claude/files/CLAUDE.md')
        self.invalid()

    def test_unlisted_asset_is_rejected(self):
        self.assets['unapproved.txt'] = 'synthetic'
        self.invalid()

    def test_inactive_fenced_import_is_rejected(self):
        self.assets['claude/files/CLAUDE.md'] = '```\n@AGENTS.md\n```\n'
        self.invalid()

    def test_absolute_import_is_rejected(self):
        self.assets['claude/files/CLAUDE.md'] = '@/synthetic/AGENTS.md\n'
        self.invalid()

    def test_scoped_rule_cannot_become_always_on(self):
        key = FILES['cursor'][-1][0]
        self.assets[key] = self.assets[key].replace('alwaysApply: false', 'alwaysApply: true')
        self.invalid()

    def test_numeric_boolean_is_rejected(self):
        key = FILES['cursor'][-1][0]
        self.assets[key] = self.assets[key].replace('alwaysApply: false', 'alwaysApply: 0')
        self.invalid()

    def test_scoped_profile_is_opt_in(self):
        self.index['profiles']['typed-ui']['default'] = True
        self.invalid()

    def test_glob_widening_is_rejected(self):
        key = FILES['claude'][-1][0]
        self.assets[key] = self.assets[key].replace('**/*.ts', '**/*')
        self.invalid()

    def test_duplicate_frontmatter_fields_are_rejected(self):
        key = FILES['cursor'][-1][0]
        self.assets[key] = self.assets[key].replace('alwaysApply: false', 'alwaysApply: false\nalwaysApply: true')
        self.invalid()

    def test_missing_canonical_boundary_is_rejected(self):
        key = FILES['claude'][-1][0]
        self.assets[key] = self.assets[key].replace('not runtime enforcement', 'verified control')
        self.invalid()

    def test_host_claims_require_separate_evidence_work(self):
        self.index['adapters'][0]['host_execution']['status'] = 'passed'
        self.invalid()

    def test_documentation_provenance_cannot_silently_drift(self):
        self.index['adapters'][0]['documentation'] = 'https://example.invalid/spec'
        self.invalid()

    def test_no_command_or_permission_mutation_claim(self):
        for key in ['modifies_host_permissions', 'executes_commands']:
            with self.subTest(key=key):
                self.index[key] = True
                self.invalid()
                self.index[key] = False

    def test_malformed_manifest_inputs_return_errors(self):
        for value in [None, [], {}, {'format_version':True}, {'format_version':1,'profiles':[]},
                      {'format_version':1,'profiles':{'base':False}}]:
            with self.subTest(value=value):
                self.assertTrue(validate_bundle(value, self.assets))

    def test_shared_rule_guidance_cannot_diverge_silently(self):
        key = FILES['cursor'][-1][0]
        self.assets[key] += '\nAn unrelated synthetic instruction.\n'
        self.invalid()


if __name__ == '__main__':
    unittest.main()
