# Agent Adapter Synchronization

Keep vendor-required instruction files as deterministic, thin adapters to root `AGENTS.md` and `.agentic/`.

1. Detect supported vendor locations without inventing unsupported files.
2. Preserve unrelated vendor configuration.
3. Generate only the minimal routing statement required by the vendor.
4. Do not copy product, architecture, security, policies, packs, or full skills into adapters.
5. Report divergent existing adapters as conflicts unless explicit replacement is authorized.
6. Re-run synchronization to prove idempotence.
7. Audit adapter length, router references, and contradictory authority claims.
