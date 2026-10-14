---
name: agent-security-review
description: "Review an AI agent integration for prompt-injection paths, tool authority, untrusted retrieval, data exfiltration and memory/supply-chain risks. Use for concrete agent/tool/RAG security assessment and isolated adversarial checks; general application review stays with security-review."
---
# Agent Security Review

Assess reachable agent-specific attack paths using the real integration's controls.
Establish target/change, task authority, attacker-controlled inputs, tools, sensitive
assets, environment and permitted testing. Use [the review method](references/method.md)
and [report template](assets/report-template.md); no provider or scanner is required.

1. Map trusted task/policy inputs versus repository files, web/retrieval content,
   tool outputs, attachments, generated plans and stored memories. Trace each from
   source through model interpretation to a tool/action or sensitive-output sink.
2. Identify actual tool enforcement: operation, argument/path/destination, identity/
   tenant, credential scope, sandbox, confirmation and runtime authorization. A
   prompt, tool description or model-returned approved flag is not enforcement.
3. Review indirect instructions, forged role delimiters, misleading tool results,
   output-to-code/HTML/SQL execution, cross-tenant memory, secret/PII logging and
   exfiltration destinations. Include installed skill/plugin provenance where relevant.
4. Check authorization independently of model content at the action boundary, with
   least privilege and constrained data flow. Keep authorized benign behavior viable.
   A string filter, citation or successful single refusal does not establish safety.
5. Use synthetic canaries and isolated local stubs for permitted adversarial cases.
   Pair attacks with benign controls and retain failed/skipped attempts. Never fetch
   an attacker URL, read real secrets, send a message or activate a production tool
   merely to prove an exploit. Source-supported risks remain distinct from reproduction.
6. Report preconditions, path, control evidence, impact, confidence and remediation.
   If fixes are authorized, use the smallest change and rerun the attack plus benign
   controls. Preserve the original finding and state uncovered surfaces.

## Completion

Findings trace to reachable sources/sinks and actual control behavior or explicit
unverified assumptions. No sandbox, model robustness, full red-team coverage or
production protection is inferred from instructions or a few local test cases.
