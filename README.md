# AI Skills

[![Format: SKILL.md](https://img.shields.io/badge/format-SKILL.md-blue)](INSTALL.md)
[![Version: 0.6.1-beta.1](https://img.shields.io/badge/version-0.6.1--beta.1-blue)](https://github.com/powerpuff-kitty/ai-skills/releases/tag/v0.6.1-beta.1)
[![AI Skills: 62](https://img.shields.io/badge/AI%20Skills-62-blue)](#skill-catalog)
[![License: MIT per skill](https://img.shields.io/badge/license-MIT-green)](INSTALL.md)

62 portable task procedures for AI agents, covering engineering, design,
repository maintenance, decisions and delivery. Each skill lives directly at the
repository root in `<name>/SKILL.md`, alongside its MIT license and any local
references, helpers, assets or checks.

## Install

Use the [copyable installation prompt](INSTALL.md). Install selected skills or the
whole collection, preserve local customizations and record the source revision.
Install directly from a reviewed Git checkout by copying complete skill folders.
No CLI, AI Agents checkout or Harness project is required. The
[optional CLI](INSTALL.md#optional-managed-installation-domains-and-updates) supports
domain presets, managed updates, previews and rollback for its bundled snapshot.
OpenCode supports the native `SKILL.md` format; no skill adapter is required.
An isolated persistent OpenCode v2.0.27 check registered all 62 skills with matching
paths and instruction bodies; allow its configuration plugins time to initialize.
See [installation and verification details](INSTALL.md#opencode-placement-and-verification).
Use an [independent release](INSTALL.md#versions-and-release-history) to pin a reviewed
snapshot; updating the CLI or AI Agents is a separate choice.

AI Skills provides procedures. The procedures do not supply model access, tools or additional
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
| [structured-reflection](structured-reflection/SKILL.md) | Turn observed failures into bounded corrections and rechecks. |
| [project-memory](project-memory/SKILL.md) | Retrieve and curate scoped, current project lessons with explicit promotion. |
| [model-fit](model-fit/SKILL.md) | Compare evidence-backed model profiles for a task. |

### Implementation and repository work

| Skill | Purpose |
| --- | --- |
| [systematic-debugging](systematic-debugging/SKILL.md) | Reproduce defects, establish causes and verify fixes. |
| [native-app-delivery](native-app-delivery/SKILL.md) | Implement and verify scoped iOS/Android lifecycle, offline and device delivery. |
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
| [user-research](user-research/SKILL.md) | Plan and synthesize participant-based research without inventing studies. |
| [design-research](design-research/SKILL.md) | Research design references and supporting evidence. |
| [design-extraction](design-extraction/SKILL.md) | Extract evidence, taste profiles and candidate design-system reports from existing interfaces. |
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
| [agent-security-review](agent-security-review/SKILL.md) | Review agent/tool trust boundaries, prompt injection and exfiltration paths. |
| [security-review](security-review/SKILL.md) | Review concrete implementations for security weaknesses. |
| [threat-model](threat-model/SKILL.md) | Map threats, trust boundaries and controls during design. |
| [incident-review](incident-review/SKILL.md) | Review incidents and identify corrective actions. |
| [release-review](release-review/SKILL.md) | Assess release readiness against documented gates. |
| [release](release/SKILL.md) | Prepare and execute an explicitly approved release. |
| [competitor-monitoring](competitor-monitoring/SKILL.md) | Compare dated competitor baselines and hand off authorized repeat runs. |
| [market-opportunity-research](market-opportunity-research/SKILL.md) | Assess segments, demand evidence and bottom-up opportunity ranges. |
| [competitive-research](competitive-research/SKILL.md) | Research current competitors and alternatives. |
| [marketing](marketing/SKILL.md) | Write positioning and messaging from approved facts. |
| [seo-audit](seo-audit/SKILL.md) | Audit crawlability, indexing and search retrieval readiness. |

### Content and AI visibility

| Skill | Purpose |
| --- | --- |
| [content-brief](content-brief/SKILL.md) | Define an evidence-backed editorial assignment. |
| [copy-editing](copy-editing/SKILL.md) | Edit drafts while preserving intent and substantiating claims. |
| [content-repurposing](content-repurposing/SKILL.md) | Adapt approved source content for distinct channels. |
| [geo-measurement](geo-measurement/SKILL.md) | Measure observed AI-answer mentions, citations and representation. |

### Product measurement

| Skill | Purpose |
| --- | --- |
| [product-instrumentation](product-instrumentation/SKILL.md) | Define event contracts, identity/retry semantics and payload QA. |
| [product-analytics](product-analytics/SKILL.md) | Reproduce product funnels, cohorts and retention with honest denominators. |
| [product-experimentation](product-experimentation/SKILL.md) | Plan and assess controlled product experiments and validity gates. |

### Financial research and validation

| Skill | Purpose |
| --- | --- |
| [market-data-validation](market-data-validation/SKILL.md) | Validate instrument, timestamp, availability, corporate-action and universe data. |
| [financial-model-review](financial-model-review/SKILL.md) | Review statement, forecast, valuation and portfolio-risk calculations. |
| [backtest-validation](backtest-validation/SKILL.md) | Check trading simulations for leakage, execution assumptions, costs and research bias. |

These are analytical procedures with worked references and report templates.
They do not connect accounts or execute financial transactions.

### Crypto, DeFi and probabilistic analysis

| Skill | Purpose |
| --- | --- |
| [onchain-data-analysis](onchain-data-analysis/SKILL.md) | Analyze chain/state/events with block, finality, units and attribution evidence. |
| [smart-contract-review](smart-contract-review/SKILL.md) | Review scoped EVM/Solidity control paths, accounting and upgrade risks. |
| [defi-risk-analysis](defi-risk-analysis/SKILL.md) | Assess protocol/position mechanisms, collateral, liquidity and dependency scenarios. |
| [odds-analysis](odds-analysis/SKILL.md) | Convert quotes, inspect margin and calculate conditional fee-adjusted payoffs. |
| [forecast-calibration](forecast-calibration/SKILL.md) | Evaluate recorded probabilities with proper scores, calibration counts and uncertainty. |
| [settlement-rule-review](settlement-rule-review/SKILL.md) | Compare event definitions, payout terms and actual resolution/finality evidence. |

Each includes focused references, synthetic worked examples and a report template.
The procedures do not supply wallet/account, trade, betting or resolution execution.

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

[AI Agents](https://github.com/powerpuff-kitty/ai-agents) provides optional role profiles
and teams. [Agentic Harness](https://github.com/powerpuff-kitty/agentic-harness) owns
its project contract; related skills use that contract when the task calls for it.
These integrations do not control installation or releases of this collection.
The CLI consumes a pinned AI Skills snapshot and validates it in its own CI; that
consumer check is separate from current source validation. Each skill carries its
own MIT [license](systematic-debugging/LICENSE).
