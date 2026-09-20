"""Synthetic comparison tests. No recorded model or hosted provider trial is claimed."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from guidance_eval import digest, validate_case
from guidance_comparison import compare, fingerprint, load_record, MAX_INPUT

HERE = Path(__file__).resolve().parent


def specification():
    return {"case": {"id": "paired-guidance", "prompt": "Assess the supplied boundary.",
                    "skill": "decision-intelligence", "route": "current-agent", "outcome": "supported",
                    "sources": {"rule": "Views call services.", "source": "View calls service."},
                    "required": ["rule", "source"], "provider_authorized": False, "max_provider_calls": 0},
            "required_checks": ["acceptance"]}


def reference(name="synthetic-log"):
    return {"reference": name, "sha256": digest(name)}


def record(spec, name="baseline", tokens=100):
    case = spec["case"]
    return {"format_version": 1, "kind": "guidance-trial-record", "evidence_kind": "synthetic",
            "spec_digest": fingerprint(spec),
            "identity": {"source_snapshot": digest("source"), "policy_snapshot": digest("policy"),
                         "checks_snapshot": digest("checks"), "host": "synthetic-host",
                         "model": "synthetic-model", "settings_snapshot": digest("settings")},
            "treatment": {"name": name, "sha256": digest(name)}, "trace": None,
            "observation": {"case_id": case["id"], "route": case["route"], "outcome": case["outcome"],
                            "sources": {key: digest(value) for key, value in case["sources"].items()},
                            "provider_calls": 0, "confidence": None, "policy_promoted": False,
                            "verification_claimed": False, "verification_observed": False},
            "checks": {"acceptance": {"status": "passed", "evidence": reference()}},
            "usage": {"complete": True, "basis": "observed-submitted-tokens", "evidence": reference("usage"),
                      "calls": [{"id": "call-1", "input_tokens": tokens, "output_tokens": 20}]}}


class GuidanceComparison(unittest.TestCase):
    def setUp(self):
        self.spec = specification()
        self.base = record(self.spec)
        self.candidate = record(self.spec, "selected-guidance", 50)

    def run_comparison(self):
        return compare(self.spec, self.base, self.candidate)

    def assert_no_saving(self, status):
        result = self.run_comparison()
        self.assertEqual(result["status"], status, result)
        self.assertIsNone(result["submitted_tokens"]["reduction"])
        self.assertFalse(result["optimisation_verified"])

    def test_complete_pair_reports_arithmetic_not_empirical_success(self):
        result = self.run_comparison()
        self.assertEqual(result["status"], "lower-submitted-tokens")
        self.assertEqual(result["submitted_tokens"]["reduction"], 50)
        self.assertEqual(result["evidence_kind"], "synthetic")
        self.assertEqual(result["model_execution"], "not-performed")
        for key in ("trace_authenticated", "optimisation_verified", "model_quality_verified", "billing_savings_verified"):
            self.assertFalse(result[key])

    def test_same_record_pair_has_identical_output(self):
        self.assertEqual(self.run_comparison(), self.run_comparison())

    def test_metadata_changes_are_incomparable(self):
        for key in self.candidate["identity"]:
            with self.subTest(key=key):
                other = copy.deepcopy(self.candidate)
                other["identity"][key] = "different" if key in {"host", "model"} else digest("different")
                self.assertEqual(compare(self.spec, self.base, other)["status"], "not-comparable")

    def test_unknown_host_or_identity_stays_unknown(self):
        for key in self.candidate["identity"]:
            other = copy.deepcopy(self.candidate)
            other["identity"][key] = None
            self.assertEqual(compare(self.spec, self.base, other)["status"], "not-comparable")

    def test_task_or_required_check_spec_drift_is_rejected(self):
        self.candidate["spec_digest"] = digest("another-task")
        self.assert_no_saving("not-comparable")

    def test_recorded_and_synthetic_cannot_mix(self):
        self.candidate["evidence_kind"] = "recorded-session"
        self.candidate["trace"] = reference("trace")
        self.assert_no_saving("not-comparable")

    def test_recorded_sessions_require_trace_references(self):
        self.base["evidence_kind"] = self.candidate["evidence_kind"] = "recorded-session"
        self.assert_no_saving("not-comparable")

    def test_trace_reference_is_not_automatically_authenticated(self):
        for item in (self.base, self.candidate):
            item["evidence_kind"] = "recorded-session"
            item["trace"] = reference("unopened-trace")
        result = self.run_comparison()
        self.assertEqual(result["status"], "lower-submitted-tokens")
        self.assertFalse(result["trace_authenticated"])
        self.assertFalse(result["optimisation_verified"])

    def test_missing_evidence_prevents_success(self):
        del self.candidate["observation"]["sources"]["rule"]
        self.assert_no_saving("acceptance-not-satisfied")

    def test_changed_source_hash_prevents_success(self):
        self.candidate["observation"]["sources"]["source"] = digest("changed")
        self.assert_no_saving("acceptance-not-satisfied")

    def test_failed_unexecuted_unsupported_and_missing_checks(self):
        for status in ("failed", "not-run", "unsupported"):
            self.candidate["checks"]["acceptance"]["status"] = status
            self.assert_no_saving("acceptance-not-satisfied")
        self.candidate["checks"] = {}
        self.assert_no_saving("acceptance-not-satisfied")

    def test_passing_flag_without_log_reference_is_insufficient(self):
        self.candidate["checks"]["acceptance"]["evidence"] = None
        self.assert_no_saving("acceptance-not-satisfied")

    def test_failure_outside_required_checks_is_not_hidden(self):
        self.candidate["checks"]["extra"] = {"status": "failed", "evidence": reference()}
        self.assert_no_saving("acceptance-not-satisfied")

    def test_broken_baseline_is_not_a_valid_optimisation_control(self):
        self.base["checks"]["acceptance"]["status"] = "failed"
        self.assert_no_saving("acceptance-not-satisfied")

    def test_false_verification_policy_or_confidence_fails(self):
        for key, value in (("verification_claimed", True), ("policy_promoted", True), ("confidence", .99)):
            other = copy.deepcopy(self.candidate)
            other["observation"][key] = value
            self.assertEqual(compare(self.spec, self.base, other)["status"], "acceptance-not-satisfied")

    def test_incomplete_usage_stays_unknown(self):
        self.candidate["usage"]["complete"] = False
        self.assert_no_saving("usage-unavailable")

    def test_unknown_tokens_and_absent_calls_stay_unknown(self):
        self.candidate["usage"]["calls"][0]["output_tokens"] = None
        self.assert_no_saving("usage-unavailable")
        self.candidate["usage"]["calls"] = []
        self.assert_no_saving("usage-unavailable")

    def test_usage_reference_and_observed_basis_are_required(self):
        self.candidate["usage"]["basis"] = "unknown"
        self.assert_no_saving("usage-unavailable")
        self.candidate["usage"]["basis"] = "observed-submitted-tokens"
        self.candidate["usage"]["evidence"] = None
        self.assert_no_saving("usage-unavailable")

    def test_estimated_bytes_are_not_accepted_as_observed_tokens(self):
        self.candidate["usage"]["basis"] = "characters-div-four"
        with self.assertRaises(ValueError):
            self.run_comparison()

    def test_retries_can_erase_a_saving(self):
        self.candidate["usage"]["calls"].append({"id": "retry", "input_tokens": 100, "output_tokens": 20})
        result = self.run_comparison()
        self.assertEqual(result["status"], "no-reduction")
        self.assertEqual(result["submitted_tokens"]["reduction"], -70)

    def test_tool_tokens_are_not_added_twice(self):
        self.candidate["usage"]["calls"][0]["tool_tokens"] = 10
        with self.assertRaises(ValueError):
            self.run_comparison()

    def test_invalid_counts_and_duplicate_call_ids_are_rejected(self):
        for value in (True, -1, "50", 2.5):
            other = copy.deepcopy(self.candidate)
            other["usage"]["calls"][0]["input_tokens"] = value
            with self.assertRaises(ValueError):
                compare(self.spec, self.base, other)
        self.candidate["usage"]["calls"].append(copy.deepcopy(self.candidate["usage"]["calls"][0]))
        with self.assertRaises(ValueError):
            self.run_comparison()

    def test_zero_baseline_never_divides_by_zero(self):
        for item in (self.base, self.candidate):
            item["usage"]["calls"][0].update(input_tokens=0, output_tokens=0)
        result = self.run_comparison()
        self.assertEqual(result["status"], "no-reduction")
        self.assertIsNone(result["submitted_tokens"]["reduction_fraction"])

    def test_missing_fields_wrong_types_and_false_versions_fail(self):
        for key in self.candidate:
            other = copy.deepcopy(self.candidate)
            del other[key]
            with self.assertRaises(ValueError):
                compare(self.spec, self.base, other)
        for key, value in (("format_version", True), ("trace", {}), ("identity", []), ("checks", [])):
            other = copy.deepcopy(self.candidate)
            other[key] = value
            with self.assertRaises(ValueError):
                compare(self.spec, self.base, other)

    def test_invalid_case_route_has_controlled_error(self):
        for route in ([], {}, True, None):
            case = copy.deepcopy(self.spec["case"])
            case["route"] = route
            with self.assertRaises(ValueError):
                validate_case(case)

    def test_duplicate_json_nonfinite_and_oversize_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.json"
            for raw in ('{"id":1,"id":2}', '{"tokens":NaN}', '{"tokens":Infinity}', ' ' * (MAX_INPUT + 1)):
                path.write_text(raw)
                with self.assertRaises(ValueError):
                    load_record(path)

    def test_named_file_entrypoint_and_exit_codes(self):
        with tempfile.TemporaryDirectory() as folder:
            paths = [Path(folder) / name for name in ("spec.json", "baseline.json", "candidate.json")]
            def invoke():
                return subprocess.run([sys.executable, str(HERE / "guidance_comparison.py"), *map(str, paths)],
                                      capture_output=True, text=True, timeout=10)
            for path, value in zip(paths, (self.spec, self.base, self.candidate)):
                path.write_text(json.dumps(value))
            output = invoke()
            self.assertEqual(output.returncode, 0, output.stderr)
            self.assertEqual(json.loads(output.stdout)["scope"], "supplied-record-fields")
            self.candidate["usage"]["complete"] = False
            paths[2].write_text(json.dumps(self.candidate))
            self.assertEqual(invoke().returncode, 1)
            paths[2].write_text('{"private": "do not echo this", "private": 2}')
            output = invoke()
            self.assertEqual(output.returncode, 2)
            self.assertNotIn("do not echo", output.stdout + output.stderr)


if __name__ == '__main__':
    unittest.main()
