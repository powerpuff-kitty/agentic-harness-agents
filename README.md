# Reusable skills

38 portable task procedures for coding agents, covering engineering, design,
repository maintenance, decisions and delivery. Each skill lives directly at the
repository root in `<name>/SKILL.md`, alongside its MIT license and any local
references, helpers, assets or checks.

## Install

Use the [copyable installation prompt](INSTALL.md). Install selected skills or the
whole collection, preserve local customizations and record the source revision.
OpenCode supports the native `SKILL.md` format; no skill adapter is required.
Verify discovery with your installed host: an isolated OpenCode v2.0.27 check
returned an empty inventory, so live loading remains unverified in that environment.
See [installation and verification details](INSTALL.md#opencode-placement-and-verification).

Skills define procedures. They do not supply model access, tools or additional
permissions. A skill's frontmatter and instructions define its actual trigger,
scope and completion conditions. Helpers are run only when the task calls for them.

## Skill catalog

### Agent setup and context

| Skill | Purpose |
| --- | --- |
| [agentic-app](agentic-app/SKILL.md) | Set up or upgrade the Agentic Harness project contract. |
| [agentic-structure-audit](agentic-structure-audit/SKILL.md) | Assess agent readiness and instruction health. |
| [agentic-improvement](agentic-improvement/SKILL.md) | Improve context routing, instructions and token efficiency. |
| [adapter-sync](adapter-sync/SKILL.md) | Synchronize thin vendor instruction adapters. |
| [migration](migration/SKILL.md) | Migrate legacy Harness layouts. |
| [model-fit](model-fit/SKILL.md) | Compare evidence-backed model profiles for a task. |

### Implementation and repository work

| Skill | Purpose |
| --- | --- |
| [systematic-debugging](systematic-debugging/SKILL.md) | Reproduce defects, establish causes and verify fixes. |
| [test-engineering](test-engineering/SKILL.md) | Design meaningful tests and diagnose unreliable coverage. |
| [change-review](change-review/SKILL.md) | Review a scoped change for defects and regressions. |
| [ci-triage](ci-triage/SKILL.md) | Investigate failing or stuck CI with exact run evidence. |
| [repository-maintenance](repository-maintenance/SKILL.md) | Reconcile issues, PRs and branches against current evidence. |
| [code-quality](code-quality/SKILL.md) | Inspect and improve formatting, linting, types and maintainability. |
| [codebase-audit](codebase-audit/SKILL.md) | Audit broad technical quality and maintainability. |
| [component-resolution](component-resolution/SKILL.md) | Select reusable UI components and plan safe adaptation. |
| [api-design](api-design/SKILL.md) | Design or review API contracts. |
| [database-design](database-design/SKILL.md) | Design persistent data models and migrations. |
| [dependency-upgrade](dependency-upgrade/SKILL.md) | Upgrade dependencies with compatibility verification. |
| [performance-audit](performance-audit/SKILL.md) | Measure and diagnose performance bottlenecks. |

### Product and design

| Skill | Purpose |
| --- | --- |
| [product-design](product-design/SKILL.md) | Define product flows, behavior and interaction states. |
| [design-research](design-research/SKILL.md) | Research design references and supporting evidence. |
| [design-analysis](design-analysis/SKILL.md) | Analyze visual and interaction design evidence. |
| [design-intelligence](design-intelligence/SKILL.md) | Coordinate analysis, preservation, compilation and design verification. |
| [identity-design](identity-design/SKILL.md) | Develop brand identity and visual direction. |
| [design-system](design-system/SKILL.md) | Create or evolve shared tokens, components and patterns. |
| [design-system-compliance](design-system-compliance/SKILL.md) | Audit implementation against an existing design system. |
| [accessibility-audit](accessibility-audit/SKILL.md) | Audit accessibility with manual and automated evidence. |

### Decisions, delivery and communication

| Skill | Purpose |
| --- | --- |
| [decision-intelligence](decision-intelligence/SKILL.md) | Design bounded semantic judgments with explicit evidence and abstention. |
| [adr-management](adr-management/SKILL.md) | Maintain Architecture Decision Records and their history. |
| [implementation-plan](implementation-plan/SKILL.md) | Turn approved scope into an executable plan. |
| [documentation](documentation/SKILL.md) | Keep durable project documentation current. |
| [security-review](security-review/SKILL.md) | Review concrete implementations for security weaknesses. |
| [threat-model](threat-model/SKILL.md) | Map threats, trust boundaries and controls during design. |
| [incident-review](incident-review/SKILL.md) | Review incidents and identify corrective actions. |
| [release-review](release-review/SKILL.md) | Assess release readiness against documented gates. |
| [release](release/SKILL.md) | Prepare and execute an explicitly approved release. |
| [competitive-research](competitive-research/SKILL.md) | Research current competitors and alternatives. |
| [marketing](marketing/SKILL.md) | Write positioning and messaging from approved facts. |
| [seo-audit](seo-audit/SKILL.md) | Audit crawlability, indexing and search retrieval readiness. |

## Structure and maintenance

`README.md` provides the overview; [INSTALL.md](INSTALL.md) owns installation
guidance. All other collection content belongs to its skill folder. Copy the
complete folder to retain its resource links and license. Markdown links resolve
relative to the document containing them.

To improve a skill, update its procedure and relevant local checks together. Keep
triggers specific, reference real evidence and preserve the distinction between
acceptance specifications and observed model outcomes. Run applicable
[skill-local checks](INSTALL.md#updates-and-validation); source checks alone do not
establish host loading or model adherence. Earlier aggregate plugin releases are
historical; current installs use the root skill folders.

[Agentic Harness](https://github.com/powerpuff-kitty/agentic-harness) owns the
project contract and catalog. Its
[CLI](https://github.com/powerpuff-kitty/agentic-harness-cli) composes pinned sources.
Each skill carries its own MIT [license](systematic-debugging/LICENSE).
