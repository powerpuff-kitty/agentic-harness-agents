# Self-contained reviews and guidance

The five enrolled documentation bundles are `codebase-audit`, `security-review`, `design-system-compliance`, `agentic-improvement` and `decision-intelligence`. Review procedures advance agents #25; the two guidance bundles advance #32/#36. Enrollment is not publication, installation or proof of host loading.

Each enrolled skill has a compact procedure and local references. Review skills retain their report templates and counterexamples; guidance skills retain the efficiency or decision guide without requiring the full collection, a Harness executable or provider credentials. Applicable target-owned context remains an input and retains authority.

## Build a standalone skill

From a reviewed checkout, with Python 3.10 or newer:

```sh
python3 .github/scripts/skill_bundle.py agentic-improvement --output /tmp/agentic-improvement.skill.zip
python3 .github/scripts/skill_bundle.py decision-intelligence --output /tmp/decision-intelligence.skill.zip
```

The same command supports the three review skills. Choose an existing output directory outside the checkout. Existing outputs are never overwritten. A write error can leave an incomplete newly created output; inspect it before a manual retry. This repository packaging helper does not install files, execute skills/tools, create parent directories or publish a release.

The ZIP contains one skill directory, its declared documentation, the exact MIT notice and a SHA-256 inventory. Repeated identical inputs produce identical stored ZIP bytes with fixed metadata. The inventory detects corruption relative to itself; it is not a signature or proof of trusted authorship. Distribution metadata `bundle.json`/`bundle-lock.json` is Harness-owned, not an extension to the Agent Skills standard.

## Dependencies and shared guidance

The packager permits declared documentation only. Local inline Markdown links must resolve inside the payload; required files cannot be missing or undeclared. Optional tools require an explicit fallback. `decision-intelligence` documents `typesafe-ai` as independently optional: guidance-only use never calls it, and an unavailable provider for an actual Jev-only task requires abstention, not invented results or automatic installation.

Design-system compliance retains a byte-identical local copy of `references/design-intelligence.md`; its shared-reference map detects drift during builds. The two guidance bundles have no collection-wide shared-reference dependency. The optional comparative-evaluation scripts are repository development tools and are deliberately not part of skill payloads.

Copy the entire verified skill directory, not just SKILL.md. Use a reviewed revision, compare existing local content before replacement and preserve customisations. Do not replace a device-global installation merely because a project-local update was requested. Confirm the host's actual discovery/loading behaviour separately; copying bytes does not prove activation or enforcement. No existing project/device or downstream source pin is updated by this change.

## Validation

```sh
python3 -m unittest discover -s .github/scripts -p test_skill_bundles.py
python3 .github/scripts/validate_agents.py
python3 .github/scripts/package_plugin.py
```

The existing validation entrypoint verifies all five documentation bundles. The collection packager checks that every enrolled document and license survives in its ZIP. The guidance regression copies each new skill into a disposable source tree, checks deterministic bytes, rejects a missing guide, deletes the disposable source and verifies the already-created archive without reading the collection.

Other tests retain malformed/duplicate JSON, symlink/reparse detection, shared-reference drift, tampering, missing entries, packaging invocation and no-overwrite checks. Reparse metadata tests are not Windows host evidence. Neither these tests nor paired-observation arithmetic execute an agent or establish token savings.

Bounds remain 65,536 bytes per file, 1,048,576 input bytes, 64 entries and four nested levels. This is a documentation subset: simple skill-root-relative inline Markdown links are checked, not full Markdown/HTML semantics, fragments, prose file mentions or external HTTPS sources. Not all 31 registered skills are standalone-complete. Scripts and binary assets are outside this packager's supported payload.

The code assumes a trusted, quiescent checkout. It rejects observed links and changed metadata but is not hostile-filesystem isolation. ZIP verification reads bounded stored entries without extracting them; `model_execution` remains `not-run`. Author/source review remains separate from archive consistency.

## Source basis

[Agent Skills specification](https://agentskills.io/specification), reviewed 2026-09-20: skill-root-relative references and progressive disclosure. Packaging metadata is project-specific. Canonical project truth remains owned by the target project; no provider availability or automatic host behaviour is inferred.
