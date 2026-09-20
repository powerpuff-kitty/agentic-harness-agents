"""Synthetic lifecycle regressions; no Codex, provider or project command runs."""
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import codex_usage as usage

HERE = Path(__file__).resolve().parent


def item(event='completed', kind='command_execution', identity='test-item', **fields):
    return {'type': 'item.' + event,
            'item': {'id': identity, 'type': kind, **fields}}


def terminal():
    return {'type': 'turn.completed', 'usage': {
        'input_tokens': 1000, 'cached_input_tokens': 500, 'output_tokens': 100}}


def stream(*body):
    return [{'type': 'thread.started', 'thread_id': 'synthetic-thread'},
            {'type': 'turn.started'}, *body, terminal()]


def encode(events):
    return b''.join(json.dumps(event, ensure_ascii=False).encode() + b'\n'
                    for event in events)


def inspect(events):
    raw = encode(events)
    return usage.inspect_trace(raw, expected_sha256=usage.digest(raw),
                               evidence_kind='synthetic')


def warning(identity='warning'):
    return item(kind='error', identity=identity, message='PRIVATE_WARNING_BODY')


class CodexUsageLifecycle(unittest.TestCase):
    def test_null_exit_is_unknown_not_success_or_failure(self):
        result = inspect(stream(item(status='completed', exit_code=None)))
        self.assertIn('command-outcome-unverified', result['reasons'])
        self.assertEqual(result['recorded_command_failures'], 0)
        self.assertIsNone(result['commands'][0]['exit_code'])
        self.assertFalse(result['whole_task_usage_complete'])

    def test_absent_exit_is_not_defaulted_to_zero(self):
        result = inspect(stream(item(status='completed')))
        self.assertIn('command-outcome-unverified', result['reasons'])
        self.assertIsNone(result['commands'][0]['exit_code'])

    def test_reconciled_running_item_is_retained_for_review(self):
        result = inspect(stream(item(event='started', status='in_progress'),
                                item(status='in_progress', exit_code=None)))
        self.assertIn('command-outcome-unverified', result['reasons'])
        self.assertEqual(result['commands'][0]['status'], 'in_progress')
        self.assertEqual(result['open_items'], 0)  # envelope closed, not process success
        self.assertTrue(result['terminal_sequence_observed'])

    def test_running_status_with_zero_exit_does_not_claim_finished(self):
        result = inspect(stream(item(status='in_progress', exit_code=0)))
        self.assertIn('command-outcome-unverified', result['reasons'])
        self.assertEqual(result['commands'][0]['exit_code'], 0)
        self.assertFalse(result['task_acceptance_verified'])

    def test_known_failure_is_preserved_alongside_incomplete_status(self):
        result = inspect(stream(item(status='in_progress', exit_code=2)))
        self.assertIn('command-outcome-unverified', result['reasons'])
        self.assertIn('command-failure-reported', result['reasons'])
        self.assertEqual(result['recorded_command_failures'], 1)

    def test_type_change_cannot_erase_command(self):
        for event in ('updated', 'completed'):
            with self.subTest(event=event), self.assertRaisesRegex(
                    usage.TraceError, '^item-type-changed$'):
                inspect(stream(item(event='started'), item(event, kind='agent_message')))

    def test_type_change_cannot_disguise_external_work(self):
        with self.assertRaisesRegex(usage.TraceError, '^item-type-changed$'):
            inspect(stream(item(event='started', kind='mcp_tool_call'),
                           item(kind='agent_message')))

    def test_cross_turn_completion_is_flagged_with_original_location(self):
        rows = stream(item(event='started')) + [
            {'type': 'turn.started'}, item(status='completed', exit_code=0), terminal()]
        result = inspect(rows)
        self.assertIn('items-open-at-turn-boundary', result['reasons'])
        self.assertIn('item-crosses-turn-boundary', result['reasons'])
        issue = next(i for i in result['item_lifecycle_issues']
                     if i['reason'] == 'item-crosses-turn-boundary')
        self.assertEqual((issue['first_event'], issue['first_turn'],
                          issue['event_line'], issue['observed_turn']), (3, 1, 6, 2))
        self.assertEqual(result['commands'][0]['turn'], 2)  # observed terminal event
        self.assertEqual(result['open_items'], 0)

    def test_open_item_boundary_remains_after_unrelated_successful_turn(self):
        result = inspect(stream(item(event='started')) + [
            {'type': 'turn.started'}, item(identity='other', status='completed', exit_code=0),
            terminal()])
        self.assertIn('items-open-at-turn-boundary', result['reasons'])
        self.assertIn('items-without-terminal-events', result['reasons'])
        self.assertEqual(result['open_items'], 1)

    def test_duplicate_starts_are_diagnostic_not_extra_commands(self):
        result = inspect(stream(item(event='started'), item(event='started'),
                                item(status='completed', exit_code=0)))
        self.assertIn('duplicate-item-start', result['reasons'])
        self.assertEqual(len(result['commands']), 1)
        self.assertEqual(result['last_snapshot_input_plus_output'], 1100)

    def test_update_without_start_is_retained_as_missing_lifecycle_evidence(self):
        result = inspect(stream(item(event='updated'), item(status='completed', exit_code=0)))
        self.assertIn('item-update-without-start', result['reasons'])
        self.assertEqual(result['open_items'], 0)

    def test_completed_only_items_remain_supported(self):
        result = inspect(stream(item(kind='reasoning', identity='reason'),
                                item(status='completed', exit_code=0)))
        self.assertEqual(result['reasons'], [])
        self.assertNotIn('item_lifecycle_issues', result)
        self.assertNotIn('warning_item_events', result)

    def test_same_turn_start_updates_and_completion_stay_clean(self):
        result = inspect(stream(item(event='started'), item(event='updated'),
                                item(event='updated'), item(status='completed', exit_code=0)))
        self.assertEqual(result['reasons'], [])
        self.assertNotIn('item_lifecycle_issues', result)

    def test_warning_inside_turn_is_not_silently_ignored(self):
        result = inspect(stream(warning()))
        self.assertIn('warning-item-reported', result['reasons'])
        self.assertEqual(result['warning_item_events'], [3])
        self.assertEqual(result['stream_error_events'], [])
        self.assertEqual(result['recorded_command_failures'], 0)

    def test_warning_before_turn_is_supported_without_inventing_a_turn(self):
        rows = stream(); rows.insert(1, warning())
        result = inspect(rows)
        self.assertEqual(result['warning_item_events'], [2])
        self.assertEqual(len(result['turns']), 1)
        self.assertEqual(result['turns'][0]['start_event'], 3)
        self.assertEqual(result['last_snapshot_input_plus_output'], 1100)

    def test_warnings_between_and_after_turns_keep_event_positions(self):
        rows = stream() + [warning('between'), {'type': 'turn.started'}, terminal(), warning('after')]
        result = inspect(rows)
        self.assertEqual(result['warning_item_events'], [4, 7])
        self.assertEqual(len(result['turns']), 2)
        self.assertTrue(result['terminal_sequence_observed'])

    def test_only_completed_warning_items_are_allowed_outside_turns(self):
        for row in (item(kind='agent_message'), item(event='started', kind='error'),
                    item(event='updated', kind='error'), item(status='completed', exit_code=0)):
            with self.subTest(row=row), self.assertRaises(usage.TraceError):
                inspect([stream()[0], row, *stream()[1:]])

    def test_warning_message_must_be_text_but_is_never_replayed(self):
        for value in (None, {}, 0):
            with self.subTest(value=value), self.assertRaises(usage.TraceError):
                inspect(stream(item(kind='error', message=value)))
        result = inspect(stream(warning()))
        self.assertNotIn('PRIVATE_WARNING_BODY', json.dumps(result))
        self.assertIsNone(result['model_identity'])
        self.assertFalse(result['producer_profile_verified'])

    def test_warning_ids_remain_subject_to_duplicate_terminal_checks(self):
        with self.assertRaisesRegex(usage.TraceError, '^item-after-completion$'):
            inspect(stream(warning(), warning()))

    def test_unknown_then_failed_then_passed_attempts_all_survive(self):
        result = inspect(stream(item(identity='a', status='completed', exit_code=None),
                                item(identity='b', status='failed', exit_code=1),
                                item(identity='c', status='completed', exit_code=0)))
        self.assertEqual([c['exit_code'] for c in result['commands']], [None, 1, 0])
        self.assertEqual(result['recorded_command_failures'], 1)
        self.assertIn('command-outcome-unverified', result['reasons'])
        self.assertIn('command-failure-reported', result['reasons'])

    def test_issue_metadata_does_not_replay_item_identifiers_or_bodies(self):
        rows = stream(item(event='started', identity='PRIVATE_ID')) + [
            {'type': 'turn.started'}, item(identity='PRIVATE_ID', status='completed',
                                          exit_code=0, command='PRIVATE_COMMAND'), terminal()]
        result = inspect(rows)
        self.assertNotIn('PRIVATE_', json.dumps(result))
        self.assertFalse(result['usage_measurement_verified'])

    def test_byte_inspection_has_no_file_network_or_process_effects(self):
        with patch('builtins.open', side_effect=AssertionError('file access')), \
             patch.object(Path, 'open', side_effect=AssertionError('file access')), \
             patch.object(socket, 'socket', side_effect=AssertionError('network access')), \
             patch.object(subprocess, 'run', side_effect=AssertionError('process execution')):
            result = inspect(stream(warning(), item(status='in_progress', exit_code=None)))
        self.assertEqual(result['last_snapshot_input_plus_output'], 1100)
        self.assertFalse(result['whole_task_usage_complete'])

    def test_actual_command_exit_codes_reflect_incomplete_and_inconsistent_items(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'trace.jsonl'
            cases = [(stream(item(status='completed', exit_code=0)), 0),
                     (stream(item(status='completed', exit_code=None)), 1),
                     (stream(item(status='in_progress', exit_code=None)), 1),
                     (stream(warning()), 1),
                     (stream(item(event='started'), item(kind='agent_message')), 2)]
            for rows, code in cases:
                raw = encode(rows); path.write_bytes(raw)
                result = subprocess.run([sys.executable, str(HERE / 'codex_usage.py'),
                    str(path), '--expected-sha256', usage.digest(raw),
                    '--evidence-kind', 'synthetic'], capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, code, result.stdout + result.stderr)
                self.assertNotIn('PRIVATE_', result.stdout + result.stderr)
                self.assertEqual(path.read_bytes(), raw)


if __name__ == '__main__':
    unittest.main()
