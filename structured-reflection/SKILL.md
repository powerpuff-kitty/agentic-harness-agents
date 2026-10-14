---
name: structured-reflection
description: "Review an attempted task against observed tests/findings, separate facts from assumptions, and propose a bounded correction with explicit verification. Use after a failed attempt or requested reflection; do not require reflection for routine success or expose private reasoning traces."
---
# Structured Reflection

Turn an observed failure or risk into a short, inspectable correction proposal.
Start with the attempt identity/snapshot, accepted requirement, actual evidence and
available finding/evaluation. A reflection is neither a new requirement nor permission
to edit code, change policy, persist memory or repeat an external action.

1. Establish whether reflection adds value. For a mechanically obvious fix, act
   within existing task scope and verify it; do not create an analysis ritual. If
   no meaningful finding exists, explain that briefly and abstain.
2. Inspect the actual evidence and distinguish observed behavior, an unsupported
   assumption, plausible cause and unknowns. A failed test can establish a symptom
   without establishing its cause. Missing evidence supports insufficient evidence,
   not a confident diagnosis. Read the [method](references/method.md).
3. Propose the smallest correction that addresses the supported cause. Record
   target/scope, prerequisite, next check and stop/retry condition. Separate a
   proposal from an action actually taken and existing authority from new scope.
4. Verify requested corrections with actual relevant checks. Preserve the original
   attempt/evaluation; attach a new result rather than rewriting a previous failure.
   Independent verification requires another actual reviewer/check, not self-labeling.
5. Suggest memory only when a reusable, project-specific lesson has evidence and is
   absent from current truth. Keep it a candidate; project-memory can guide review
   when available. Do not persist a transcript or private chain-of-thought.
6. Deliver the [reflection record](assets/report-template.md), evidence references,
   observed facts, uncertainty, proposed/performed corrections and actual rechecks.
   Use the optional [protocol mapping](references/protocol.md) only when that
   serialization is requested; a concise report otherwise suffices.

## Completion

Every correction traces to an observed risk or explicitly tentative hypothesis.
No diagnosis, successful recheck, memory promotion or runtime enforcement is invented.
