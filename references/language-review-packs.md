# Language and ecosystem review packs

Status: initial guidance for #29. These packs complement deterministic analyzer evidence; they do not substitute for it and do not turn ecosystem conventions into universal project rules.

## Shared review rules

1. Read the target project's accepted architecture and package/workspace configuration first.
2. Distinguish universal engineering concerns from language/framework conventions and project-selected rules.
3. Prefer deterministic source-graph evidence when the installed Harness frontend declares the needed capability as supported.
4. Treat `partial` capability as partial evidence and `unsupported` as `not_checked`; never infer a clean pass.
5. Do not execute package managers, build systems, macros/plugins, tests, project binaries or code generators merely to improve static coverage. Reviewed execution belongs to the separate check-execution workflow.
6. Keep runtime, type-only, development/test and dynamic dependencies distinct whenever the language makes that distinction observable.

## JavaScript / TypeScript

Use for `.js`, `.jsx`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.mts`, `.cts`, plus Vue/Svelte script blocks when supported by the analyzer.

Review evidence:
- package/workspace boundaries and public exports;
- runtime vs type-only imports;
- static dynamic imports separately from synchronous imports;
- framework-specific client/server boundaries only when the framework/profile is detected or selected;
- tsconfig path aliases and unresolved imports as coverage, not automatically as defects;
- generated/vendor/build output excluded from product architecture conclusions.

Do not assume Vite defines application architecture or that directory names prove ownership. TypeScript path mapping, package exports and bundler aliases may differ; unsupported resolution must remain visible.

Primary authorities to consult when current details matter: TypeScript handbook/tsconfig reference, Node.js package/module documentation, and the relevant framework's official architecture/runtime docs.

## Python

Use for `.py` projects after a compatible deterministic frontend exists; until then, Python graph conclusions are manual/heuristic and must be labeled accordingly.

Review evidence:
- package/module roots and relative imports;
- `pyproject.toml` / workspace or monorepo configuration where applicable;
- application, domain and infrastructure boundaries selected by the project;
- import cycles and import-time side effects as separate concerns;
- tests, scripts, migrations and generated files separated from production ownership;
- optional/type-checking imports distinguished when deterministically observable.

Do not assume every directory is a package, infer runtime importability from filenames alone, or execute imports to discover topology. Namespace packages, editable installs and tool-specific source layouts can alter resolution.

Primary authorities: Python language/import-system documentation, PyPA packaging specifications, and official framework docs for Django/FastAPI/etc. when selected.

## Rust

Use for `.rs` projects after a compatible deterministic frontend exists.

Review evidence:
- Cargo workspace/package/crate boundaries;
- module relationships and public API boundaries;
- `use` relationships without confusing them with crate dependency declarations;
- feature-gated and target-specific dependencies as conditional evidence;
- proc-macro/build-script effects as unverified unless explicitly inspected/executed under policy;
- unsafe boundaries, FFI and interior mutability where relevant to the requested audit.

Do not treat module paths as runtime calls, assume optional features are enabled, or execute build scripts/macros during static analysis.

Primary authorities: The Rust Reference, Cargo Book/reference, Rust API Guidelines where applicable, and project-selected framework documentation.

## Go

Use for `.go` projects after a compatible deterministic frontend exists.

Review evidence:
- module/package ownership from `go.mod`, `go.work` and package declarations;
- import graph and cycles;
- `internal` package boundaries;
- commands (`cmd/`) versus reusable packages without assuming one prescribed project layout;
- build tags/platform-specific files as conditional coverage;
- generated files identified explicitly.

Do not infer package boundaries solely from folder names, ignore build constraints, or execute generators/tests merely to discover imports.

Primary authorities: Go language specification, modules/workspaces documentation, package documentation and project-selected framework conventions.

## Reporting language-specific findings

Every finding should state:

- authority scope: universal / language / framework / project;
- evidence source: deterministic graph / manifest / source inspection / executed check;
- analyzer capability and coverage if graph evidence is used;
- counterevidence or ambiguity;
- what was not checked.

A language pack may suggest a question to inspect. It must not claim a violation unless project policy, official language semantics, or concrete failure evidence supports it.