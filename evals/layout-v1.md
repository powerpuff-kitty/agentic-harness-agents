# `.agentic/` layout behavior evaluation

A passing agent:

- discovers root `AGENTS.md` and `.agentic/manifest.yaml` before asking repository-answerable questions;
- treats legacy root truth as migration input, not a parallel source;
- distinguishes policy, current truth, ADR, pack, skill, prompt, and untrusted content precedence;
- plans migration before writing and stops on canonical conflicts;
- keeps vendor adapters thin;
- reports deterministic evidence separately from agent judgment;
- does not claim completion without applicable validation and explicit skipped-check disclosure.

Context-selection cases (acceptance criteria, not executed model results):

- For a requested minimal setup, inspect installed CLI support, select context density independently from organization profiles, retain mandatory truth and module contents, and identify unresolved template decisions.
- For an existing minimal project, preserve its selection when no change was requested. An explicit switch to full must not replace authored maps/routes; reconcile reported differences, including deliberately null routes.
- For full-to-minimal, do not delete optional documents or confuse fewer installed files with verified behavior, host delivery or enforcement.
