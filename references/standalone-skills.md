# Self-contained flagship reviews

Status: initial documentation-bundle implementation for agents #25. The enrolled skills are `codebase-audit`, `security-review` and `design-system-compliance`. Their trigger descriptions and inventory names are unchanged. Migration and verified-completion procedures remain separate unfinished work.

Each enrolled skill has a compact router procedure, local decision guide, human report template, counterexamples and expected decisions for future model evaluations. Concrete findings require project authority or a demonstrated failure mode; sampled inspection and missing tools never become universal quality/security/conformance claims. Target-owned context remains authoritative and follows the target's custom routes.

## Build a standalone skill

From a reviewed checkout, with Python 3.10 or newer:

```sh
python3 .github/scripts/skill_bundle.py codebase-audit --output /tmp/codebase-audit.skill.zip
python3 .github/scripts/skill_bundle.py security-review --output /tmp/security-review.skill.zip
python3 .github/scripts/skill_bundle.py design-system-compliance --output /tmp/design-system-compliance.skill.zip
```

Choose an existing output directory outside the checkout. Existing outputs are never overwritten. A write error can leave an incomplete newly created output; inspect it before a manual retry. The command does not install files in any project, execute a skill/tool, create parent directories or publish a release.

The ZIP contains one skill directory, its declared documentation, the exact repository MIT notice and an internal SHA-256 inventory. Repeated packaging of identical inputs produces identical uncompressed ZIP bytes with fixed metadata. The inventory detects byte corruption relative to itself; it is not a signature, proof of trusted authorship or evidence that a model followed the skill.

`bundle.json` and `bundle-lock.json` are this repository's distribution metadata, not additions to the Agent Skills standard or target-project architecture. Only the three declared documentation bundles are supported by this first packager. It does not claim that all 31 skills are standalone-complete or support arbitrary scripts, binary assets or external dependencies.

## Dependencies and shared guidance

`bundle.json` lists all required local documents and optional tools with an explicit offline/manual fallback. Required documents must be present, with no undeclared files; local inline Markdown links must resolve inside the declared skill payload. Target-owned files, such as a manifest-designated architecture document, are inputs in the procedure, not files to vendor into the skill.

Design-system compliance includes a byte-identical local copy of `references/design-intelligence.md`. Its `shared_references` map records the collection source. Build-time validation fails if either copy drifts. Runtime standalone use reads only the bundled copy; it does not need the original collection or a sibling skill. Review and update both copies together when the shared guidance changes.

All new references live below each skill folder, so a recursive single-skill or project-local copy can retain them. That layout compatibility is not by itself evidence for a particular CLI source pin or installer. Downstream pinned composition must be tested against the new agents revision before being recorded as verified.

## Validation

```sh
python3 -m unittest discover -s .github/scripts -p 'test_skill_bundles.py'
python3 .github/scripts/validate_agents.py
python3 .github/scripts/package_plugin.py
```

The existing validation entrypoint runs the bundle regressions without changing workflow YAML. The real collection packager then checks that every enrolled document and license survived into its actual ZIP with the validated bytes. Missing files or changed shared references fail packaging rather than silently producing an incomplete collection.

Tests cover deterministic archives, reference closure, extraction without the original collection, explicit tool fallback, raw input bounds, malformed/duplicate JSON, symlink/reparse detection, shared-reference drift, damaged/missing archive entries, real packager invocation and no-overwrite output. The reparse test exercises the predicate with synthetic metadata; it is not a recorded Windows host session.

Bounds: 65,536 bytes per file, 1,048,576 total input bytes, 64 entries and four nested directory levels. This is a documentation authoring subset: simple skill-root-relative inline Markdown links are checked, not full Markdown/HTML semantics, fragment correctness, prose file mentions, host loading or prompt interpretation. HTTPS source links are not fetched. Unknown semantic dependencies can still require human review.

The code assumes a trusted, quiescent source checkout. It rejects observed links and changed file metadata, but is not a sandbox against hostile concurrent filesystem mutation. ZIP verification reads bounded stored entries without extracting them; model execution remains `not-run` in its report. The guides' clean/violated/stale/missing-tool examples are acceptance expectations, not completed model evaluations.

## Source basis

Agent Skills specification, reviewed 2026-09-13: https://agentskills.io/specification. The optional reference-directory and progressive-disclosure convention is used here; no claim is made that this project's packaging manifest is a standard field. Canonical project truth and CLI analysis semantics remain owned by their respective repositories.
