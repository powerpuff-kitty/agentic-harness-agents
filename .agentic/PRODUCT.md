# Product

Agentic Harness Agents is the installable procedure layer of the Agentic Harness ecosystem.

It provides reusable Agent Skills for Codex and compatible workflow guidance for other coding agents without owning project architecture or business truth.

## Goals

- make individual skills directly installable and auto-discoverable by Codex;
- provide a skills-only plugin that can be imported and synchronized from GitHub;
- keep triggers narrow, non-overlapping, and evidence-backed;
- use progressive disclosure so routine tasks load minimal context;
- provide explicit procedures, outputs, and completion criteria;
- keep releases versioned and compatible with canonical Agentic Harness and CLI revisions;
- expose Design Intelligence as specialist procedures over canonical Design Analysis, Design Genome, Design Task, research/provider, and drift contracts;
- keep design evidence, identity/art direction, product UX, reusable UI systems, component providers, compliance, and accessibility as separate responsibilities.

## Design Intelligence product boundary

The agent layer orchestrates and interprets design work; it does not replace deterministic measurement/compilation or become a second source of design truth.

```text
Analyze → Preserve → Compile → Verify
          │
          └─ approved Design Genome remains project-owned truth
```

References, external components, market patterns, and AI interpretations can propose changes but require review before becoming approved project rules.

## Non-goals

- redefining canonical project structure or policy;
- embedding model-specific product truth;
- replacing deterministic CLI validation, design measurement, or prompt compilation with prompt prose;
- imposing one reusable Agentic Harness visual aesthetic across unrelated products;
- treating external UI libraries or reference prevalence as product/design authority.
