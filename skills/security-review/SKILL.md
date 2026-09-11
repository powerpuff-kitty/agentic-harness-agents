---
name: security-review
description: "Review an existing implementation or change for security weaknesses in authentication, authorization, tenancy, inputs/outputs, secrets, cryptography, privacy, dependencies, CI/release, logging, recovery, and abuse resistance. Use when a concrete security review or secure-by-default code assessment is requested. Do not use primarily for pre-implementation threat modeling or broad non-security code review."
---
# Security Review

## Objective

Identify actionable security defects and unsafe defaults in the implemented scope using repository evidence and deterministic tooling where available.

## Inputs

Required: target repository/change scope. Optional: threat model, data classification, deployment environment, security baseline, scanner results, and supported languages/frameworks.

## Context

Read `.agentic/SECURITY.md`, manifest permissions, installed policies, affected architecture/data/API docs, relevant ADRs, lockfiles, and implementation files. Load additional context only when a finding requires it.

## Procedure

1. Establish assets/trust boundaries already documented and the exact code/config under review.
2. Inspect authentication, authorization, tenancy, validation, output encoding, secrets, crypto, privacy/retention, dependencies/supply chain, CI/release, logging, backups/recovery, and abuse cases as applicable.
3. Run available security/static/dependency/secret tooling and record its scope/version.
4. Verify high-severity findings against source/config to control false positives.
5. Separate confirmed defects, unsafe design assumptions, missing controls, and scanner-only signals.
6. Recommend smallest effective remediation and note compatibility/operational impact.
7. Escalate architecture/security-policy decisions instead of silently rewriting them.

## Output

Return severity-ranked findings with evidence, exploit/precondition description where appropriate, confidence, remediation, checks performed/skipped, and residual risk.

## Completion

High-impact findings are evidence-backed, secrets are never exposed in output, scanner absence/presence is not treated as proof of safety, and policy-changing fixes require explicit approval.
