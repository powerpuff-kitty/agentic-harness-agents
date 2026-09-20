# Self-contained reviews and guidance

The five enrolled bundles are `codebase-audit`, `security-review`, `design-system-compliance`, `agentic-improvement` and `decision-intelligence`. The three review skills retain documentation-only v1 declarations; both guidance skills use explicit optional-script v2 declarations. Review procedures advance agents #25; the two guidance bundles advance #32/#36. Enrollment is not publication, installation or proof of host loading.

Each enrolled skill has a compact procedure and local references. Review skills retain their report templates and counterexamples; guidance skills retain the efficiency or decision guide without requiring the full collection, a Harness executable or provider credentials. Applicable target-owned context remains an input and retains authority.

## Build a standalone skill

From a reviewed checkout, with Python 3.10 or newer:

```sh
python3 .github/scripts/skill_bundle.py agentic-improvement --output /tmp/agentic-improvement.skill.zip
python3 .github/scripts/skill_bundle.py decision-intelligence --output /tmp/decision-intelligence.skill.zip
```

The same command supports the three review skills. Choose an existing output directory outside the checkout. Existing outputs are never overwritten. A write error can leave an incomplete newly created output; inspect it before a manual retry. This repository packaging helper does not install files, execute skills/tools, create parent directories or publish a release.

The ZIP contains one skill directory, its declared payload, the exact MIT notice and a SHA-256 inventory. Repeated identical inputs produce identical stored ZIP bytes with fixed metadata. The inventory detects corruption relative to itself; it is not a signature or proof of trusted authorship. Distribution metadata `bundle.json`/`bundle-lock.json` is Harness-owned, not an extension to the Agent Skills standard.

## Dependencies and shared guidance

Version 1 permits declared documentation only. Version 2 additionally requires a nonempty `optional_scripts` list: each entry names one declared `scripts/*.py` file, `execution: explicit-invocation-only`, and a manual fallback. No auto-run hook or interpreter installation is provided. Other script types and undeclared files remain unsupported. Older v1-only packagers must reject v2 instead of silently omitting its helper; exact source pins still matter.

Validation and archive inspection treat scripts as opaque UTF-8 source bytes. They never import, compile or execute them and do not certify their safety. Script contents are hashed and retained with non-executable archive permissions; deliberate invocation still requires review, a permitted interpreter and target permission. The v1 archive format/bytes are unchanged. v2 lock scope explicitly includes script bytes without claiming execution. The optional helpers use the Python standard library; manual guidance remains usable without Python.

Local inline Markdown links must resolve inside the payload; required files cannot be missing or undeclared. Optional tools require an explicit fallback. `decision-intelligence` documents `typesafe-ai` as independently optional: guidance-only use never calls it, and an unavailable provider for an actual Jev-only task requires abstention, not invented results or automatic installation. Its optional graph reviewer inspects declared dependencies, not provider state, outcomes or authorization.

Design-system compliance retains a byte-identical local copy of `references/design-intelligence.md`; its shared-reference map detects drift during builds. The two guidance bundles have no collection-wide shared-reference dependency. Comparative-evaluation scripts remain repository development tools, not skill payloads. Unlike those evaluators, the optional log/freshness helpers and decision-graph reviewer ship inside their owning guidance skills.

Copy the entire verified skill directory, not just SKILL.md. Use a reviewed revision, compare existing local content before replacement and preserve customisations. Do not replace a device-global installation merely because a project-local update was requested. Confirm the host's actual discovery/loading behaviour separately; copying bytes does not prove activation or enforcement. No existing project/device or downstream source pin is updated by packaging.

## Validation

```sh
python3 -m unittest discover -s .github/scripts -p test_skill_bundles.py
python3 -m unittest discover -s .github/scripts -p test_optional_script_bundles.py
python3 .github/scripts/validate_agents.py
python3 .github/scripts/package_plugin.py
```

The validation entrypoint verifies all five bundles. The collection packager checks that every enrolled payload and licence survives in its ZIP. Guidance regressions copy each skill into a disposable source tree, check deterministic bytes, reject missing dependencies, delete the disposable source and verify the archive without reading the collection.

Tests retain malformed/duplicate JSON, symlink/reparse detection, shared-reference drift, tampering, missing entries and no-overwrite checks. v2 tests retain an inert script that raises on execution, verify it without executing it, and compare a v1 archive to its pre-change byte identity. Explicit helper tests separately execute only reviewed code on synthetic local inputs. Neither those tests nor paired-observation arithmetic execute a model or establish model-token savings.

Bounds remain 65,536 bytes per file, 1,048,576 input bytes, 64 entries and four nested levels. Simple skill-root-relative inline Markdown links are checked, not full Markdown/HTML semantics, fragments, prose file mentions or external HTTPS sources. Not all 32 registered skills are standalone-complete. Binary assets and arbitrary executable dependencies remain unsupported.

The code assumes a trusted, quiescent checkout. It rejects observed links and changed metadata but is not hostile-filesystem isolation. ZIP verification reads bounded stored entries without extracting them; `model_execution` remains `not-run`. Author/source review remains separate from archive consistency.

## Source basis

[Agent Skills specification](https://agentskills.io/specification), reviewed 2026-09-20: skill-root-relative references and progressive disclosure. Packaging metadata is project-specific. Canonical project truth remains owned by the target project; no provider availability or automatic host behaviour is inferred.
