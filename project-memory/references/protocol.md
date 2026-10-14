# Optional Harness memory contracts

Use the pinned canonical [Project Memory contracts](https://github.com/powerpuff-kitty/agentic-harness/tree/864e5fde38557217e7e3564b3bf47532fc8b922d/registry/project-memory)
only when that serialization/store is requested. memory records carry stable ID,
class/state, statement, project/repository/path/tag scope, source/evidence provenance,
validity, nullable confidence/importance, sensitivity, usage and lineage. Queries,
results and operations are separate records; a report is not a performed operation.

A result explains inclusion/exclusion and matched scope. Proposed changes map to
promotion, reverification, supersession, invalidation, consolidation or expiry with
source/lineage preserved. Validate both schemas and semantic privacy/lineage rules
when tooling is available. Never fabricate provider IDs, action receipts or evidence.
The fixture contains canonical-format synthetic records, not a deployed memory store.
