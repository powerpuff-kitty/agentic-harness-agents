# ADR Management

Create and maintain Architecture Decision Records under `.agentic/decisions/`.

Use an ADR for a durable consequential choice with meaningful alternatives or trade-offs—not routine implementation detail or temporary task state.

1. Read `.agentic/decisions/README.md`, `index.yaml`, related current truth, evidence, and earlier ADRs.
2. Allocate the next zero-padded ID and a stable kebab-case filename.
3. Record status, date, deciders, context, drivers, credible options, precise decision, consequences, evidence, and verification.
4. Add the ADR to `index.yaml` without reordering historical IDs.
5. When accepted, update current truth to reflect the resulting state.
6. To replace an accepted ADR, create a new ADR and link `Supersedes`/`Superseded by`; do not rewrite history.
7. Validate filename, heading, status, index entry, and links.

Facts remain facts, proposals remain proposed, and user approval is required for consequential decisions not already accepted.
