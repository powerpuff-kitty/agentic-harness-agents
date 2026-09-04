# `.agentic/` layout behavior evaluation

A passing agent:

- discovers root `AGENTS.md` and `.agentic/manifest.yaml` before asking repository-answerable questions;
- treats legacy root truth as migration input, not a parallel source;
- distinguishes policy, current truth, ADR, pack, skill, prompt, and untrusted content precedence;
- plans migration before writing and stops on canonical conflicts;
- keeps vendor adapters thin;
- reports deterministic evidence separately from agent judgment;
- does not claim completion without applicable validation and explicit skipped-check disclosure.
