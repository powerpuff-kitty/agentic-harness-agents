"""Compare supplied skill-trial records; never execute models or authenticate traces.

Evaluation support only: not a Harness runtime, provider adapter or billing tool.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

from guidance_eval import evaluate, submitted_tokens, validate_case

DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
IDENTITY_KEYS = {"source_snapshot", "policy_snapshot", "checks_snapshot",
                 "host", "model", "settings_snapshot"}
STATUSES = {"passed", "failed", "not-run", "unsupported"}
MAX_INPUT = 1_048_576


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def text(value: Any) -> bool:
    return (isinstance(value, str) and 0 < len(value) <= 4096
            and value.strip() == value and not any(ord(c) < 32 or 127 <= ord(c) < 160 for c in value))


def fingerprint(value: Any) -> str:
    content = json.dumps(value, sort_keys=True, ensure_ascii=True,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(content).hexdigest()


def reference(value: Any) -> bool:
    return (isinstance(value, dict) and set(value) == {"reference", "sha256"}
            and text(value["reference"]) and isinstance(value["sha256"], str)
            and bool(DIGEST.fullmatch(value["sha256"])))


def validate_spec(spec: Any) -> None:
    require(isinstance(spec, dict) and set(spec) == {"case", "required_checks"},
            "comparison: invalid specification")
    validate_case(spec["case"])
    checks = spec["required_checks"]
    require(isinstance(checks, list) and 1 <= len(checks) <= 128
            and all(text(item) for item in checks), "comparison: required checks missing")
    require(len(checks) == len(set(checks)), "comparison: duplicate required checks")


def validate_record(record: Any) -> None:
    require(isinstance(record, dict) and set(record) == {
        "format_version", "kind", "evidence_kind", "spec_digest", "identity", "treatment",
        "observation", "checks", "trace", "usage"}, "comparison: invalid record fields")
    require(type(record["format_version"]) is int and record["format_version"] == 1
            and record["kind"] == "guidance-trial-record", "comparison: unsupported record")
    require(isinstance(record["evidence_kind"], str)
            and record["evidence_kind"] in {"synthetic", "recorded-session"},
            "comparison: invalid evidence kind")
    require(isinstance(record["spec_digest"], str)
            and bool(DIGEST.fullmatch(record["spec_digest"])), "comparison: invalid spec digest")
    identity = record["identity"]
    require(isinstance(identity, dict) and set(identity) == IDENTITY_KEYS,
            "comparison: incomplete identity")
    for key, value in identity.items():
        require(value is None or (text(value) and (key in {"host", "model"}
                or bool(DIGEST.fullmatch(value)))), "comparison: invalid identity")
    treatment = record["treatment"]
    require(isinstance(treatment, dict) and set(treatment) == {"name", "sha256"}
            and text(treatment["name"]) and isinstance(treatment["sha256"], str)
            and bool(DIGEST.fullmatch(treatment["sha256"])), "comparison: invalid treatment")
    require(record["trace"] is None or reference(record["trace"]),
            "comparison: invalid trace reference")
    checks = record["checks"]
    require(isinstance(checks, dict) and len(checks) <= 128,
            "comparison: invalid checks")
    for key, check in checks.items():
        require(text(key) and isinstance(check, dict) and set(check) == {"status", "evidence"},
                "comparison: invalid check fields")
        require(isinstance(check["status"], str) and check["status"] in STATUSES,
                "comparison: invalid check status")
        require(check["evidence"] is None or reference(check["evidence"]),
                "comparison: invalid check evidence")
    usage = record["usage"]
    require(isinstance(usage, dict) and set(usage) == {"complete", "basis", "evidence", "calls"},
            "comparison: invalid usage fields")
    require(type(usage["complete"]) is bool and isinstance(usage["basis"], str)
            and usage["basis"] in {"observed-submitted-tokens", "unknown"},
            "comparison: invalid usage basis")
    require(usage["evidence"] is None or reference(usage["evidence"]),
            "comparison: invalid usage evidence")
    require(isinstance(usage["calls"], list) and len(usage["calls"]) <= 4096,
            "comparison: invalid call inventory")
    seen = set()
    for call in usage["calls"]:
        require(isinstance(call, dict) and set(call) == {"id", "input_tokens", "output_tokens"}
                and text(call["id"]), "comparison: invalid call")
        require(call["id"] not in seen, "comparison: duplicate call identity")
        seen.add(call["id"])
    submitted_tokens([{key: call[key] for key in ("input_tokens", "output_tokens")}
                      for call in usage["calls"]])


def compare(spec: Any, baseline: Any, candidate: Any) -> dict[str, Any]:
    """Only issue arithmetic comparisons after matched identities and acceptance fields."""
    validate_spec(spec)
    for record in (baseline, candidate):
        validate_record(record)
    reasons = []
    if baseline["evidence_kind"] != candidate["evidence_kind"]:
        reasons.append("mixed-evidence-kinds")
    for key in sorted(IDENTITY_KEYS):
        if baseline["identity"][key] is None or candidate["identity"][key] is None:
            reasons.append("unknown-identity:" + key)
        elif baseline["identity"][key] != candidate["identity"][key]:
            reasons.append("mismatched-identity:" + key)
    for role, record in (("baseline", baseline), ("candidate", candidate)):
        if record["spec_digest"] != fingerprint(spec):
            reasons.append(role + ":mismatched-specification")
        if record["evidence_kind"] == "recorded-session" and record["trace"] is None:
            reasons.append(role + ":missing-trace")
    result = {"format_version": 1, "kind": "guidance-comparison", "status": "not-comparable",
              "scope": "supplied-record-fields", "evidence_kind": candidate["evidence_kind"],
              "spec_digest": fingerprint(spec),
              "record_digests": {"baseline": fingerprint(baseline), "candidate": fingerprint(candidate)},
              "reasons": reasons, "submitted_tokens": {"baseline": None, "candidate": None,
              "reduction": None, "reduction_fraction": None}, "trace_authenticated": False,
              "model_execution": "not-performed", "model_quality_verified": False,
              "billing_savings_verified": False, "optimisation_verified": False}
    if reasons:
        return result
    for role, record in (("baseline", baseline), ("candidate", candidate)):
        grade = evaluate(spec["case"], record["observation"])
        reasons.extend(role + ":" + failure for failure in grade["failures"])
        for name in spec["required_checks"]:
            check = record["checks"].get(name)
            if check is None or check["status"] != "passed" or check["evidence"] is None:
                reasons.append(role + ":required-check-unverified:" + name)
        # Never hide a known failure just because it was not in the required set.
        if any(check["status"] == "failed" for check in record["checks"].values()):
            reasons.append(role + ":reported-check-failure")
    if reasons:
        result["status"] = "acceptance-not-satisfied"
        return result
    totals = []
    for role, record in (("baseline", baseline), ("candidate", candidate)):
        usage = record["usage"]
        total = submitted_tokens([{key: call[key] for key in ("input_tokens", "output_tokens")}
                                  for call in usage["calls"]])
        if (not usage["complete"] or usage["basis"] != "observed-submitted-tokens"
                or usage["evidence"] is None or total is None):
            reasons.append(role + ":usage-unavailable-or-incomplete")
        totals.append(total)
    if reasons:
        result["status"] = "usage-unavailable"
        return result
    before, after = totals
    reduction = before - after
    result["submitted_tokens"] = {"baseline": before, "candidate": after, "reduction": reduction,
                                  "reduction_fraction": reduction / before if before else None}
    result["status"] = "lower-submitted-tokens" if reduction > 0 else "no-reduction"
    return result


def _object(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, "comparison: duplicate JSON key")
        value[key] = item
    return value


def _constant(value):
    raise ValueError("comparison: non-finite JSON number")


def load_record(path: Path) -> Any:
    # Named inputs only. Trace/evidence references are never opened or executed.
    require(path.is_file() and not path.is_symlink(), "comparison: regular input file required")
    with path.open("rb") as source:
        raw = source.read(MAX_INPUT + 1)
    require(len(raw) <= MAX_INPUT, "comparison: input size limit exceeded")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_object, parse_constant=_constant)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    try:
        result = compare(*(load_record(path) for path in (args.spec, args.baseline, args.candidate)))
    except (ValueError, OSError, TypeError, RecursionError):
        print(json.dumps({"kind": "guidance-comparison-error", "code": "invalid-input"}))
        return 2
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0 if result["status"] == "lower-submitted-tokens" else 1


if __name__ == "__main__":
    sys.exit(main())
