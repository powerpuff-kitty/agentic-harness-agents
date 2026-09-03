# Design System Compliance

Use when a project has or wants a design system.

1. Discover tokens, primitives, component library, docs, examples, and framework conventions.
2. Infer required components from product surfaces and flows; verify with `ah design-system-components` when available.
3. Map each required component to existing, planned, or intentionally native implementation.
4. Prefer design-system components/tokens in product code; do not duplicate primitives locally without a documented reason.
5. Audit raw controls, hard-coded visual values, duplicated components, token bypasses, accessibility regressions, and missing required components.
6. Treat exceptions as explicit decisions.

Use deterministic audit evidence plus manual visual/accessibility review.
