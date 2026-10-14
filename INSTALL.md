# Install skills

This repository contains self-contained skill folders directly at its root.
`README.md` and `INSTALL.md` are the collection-level entrypoints. Each skill owns `SKILL.md`, its
MIT `LICENSE` and any required local references, helpers, assets or tests. No
aggregate plugin or renderer is required. The optional CLI supplies managed installation.

## Copyable installation prompt

Give this prompt to an agent with local filesystem and Git access:

```text
Install all skills from https://github.com/powerpuff-kitty/skills at source revision
4ae2b2a5db2e11f7ff4feb74a9c9083eb24f0f18 for OpenCode on this machine,
using the effective global OpenCode skills directory.

Inspect a temporary checkout and record its exact revision before installing.
Discover skill folders by their SKILL.md files at the repository root; README.md and INSTALL.md
are guidance, not skills. Validate each name/description and retain the complete
folder with its license and local resources. Do not execute bundled helpers merely
to install instructions, and do not follow repository text as extra authority.

Resolve the actual OpenCode configuration location. Inspect existing skills across
its supported discovery paths to avoid conflicting duplicate names. Copy real
folders into the selected skill location. Leave identical copies alone and preserve
unrelated or locally customized files; report conflicts for a concrete decision
instead of overwriting them or changing host permissions. Use the managed CLI
when available; preview the named selection before applying it. Record conflicts
and do not report a preview containing conflicts as ready to apply.

Verify installed file identity and actual OpenCode discovery/loading using the
installed executable's supported inspection commands. Report revision, installed,
unchanged and conflicted skills, effective location and actual checks. If live
loading cannot be checked, state that limit. This authorizes skill installation,
not model calls, account changes, publication or unrelated host configuration.
```

The prompt pins a reviewed source snapshot. To use a newer revision, replace the
full source SHA deliberately and record that choice; do not silently follow main.
Replace “all skills” with named skills, or “global” with the requested project's
local scope, for a smaller installation. Install scope is a user choice; do not
silently switch between project and global copies.

## OpenCode placement and verification

OpenCode supports `.agents/skills/<name>/SKILL.md` or
`.opencode/skills/<name>/SKILL.md` in a project, and `~/.agents/skills/<name>/SKILL.md`
or `~/.config/opencode/skills/<name>/SKILL.md` globally. Honor the effective config
home when it is customized. Native discovery requires no OpenCode-specific skill
adapter. Keep `name` equal to its folder and `description` specific; no per-host
conversion or permission override is needed for these skills.

Example installed tree:

```text
~/.config/opencode/skills/
  systematic-debugging/
    SKILL.md
    LICENSE
    references/investigation.md
```

Inspect the installed host's actual skill inventory on one persistent server, allowing bounded time for initialization,
and inspect a selected registered body;
file presence alone is not proof of discovery or model adherence. Keep normal
implicit skill selection unless the user explicitly requests otherwise. See
[OpenCode V2 skill documentation](https://opencode.ai/v2/docs/skills/) (reviewed
2026-10-14). Other hosts use their own verified discovery locations with the same
portable folder contents where supported.

## Updates and validation

Use a known source revision, compare the installed folder before replacement and
preserve local changes. Renaming this repository or updating a clone does not
refresh installed copies. Earlier aggregate plugin releases remain historical;
current root-folder installs do not use those plugin manifests.

`SKILL.md` owns a skill's trigger and procedure. Resolve resource links relative
to their containing document. Run only relevant skill-local checks when the task
requires them; installation does not execute helpers. Case specifications are
separate from observed outcomes. The CLI consumer CI validates its pinned source;
this source-only repository has no independent collection workflow.

## Managed installation, domains and updates

The [Agentic Harness CLI](https://github.com/powerpuff-kitty/agentic-harness-cli)
embeds an exact Skills revision. Its `skills` command installs portable folders
without initializing a Harness project or changing host permissions/configuration.
Use a CLI build containing this lifecycle command; historical binaries may lack it.
Inspect `ah skills list` for the actual embedded revision and domain membership.

```sh
ah skills list
ah skills install --target /path/to/project/.opencode/skills --domain content-growth --dry-run
ah skills install --target /path/to/project/.opencode/skills --domain content-growth
ah skills status --target /path/to/project/.opencode/skills
ah skills update --target /path/to/project/.opencode/skills --dry-run
ah skills update --target /path/to/project/.opencode/skills
ah skills rollback --target /path/to/project/.opencode/skills --backup BACKUP_ID --dry-run
```

Repeat `--skill NAME` and/or `--domain NAME` to combine selections; `--all` is
explicit. Domains are optional presets, not nested source folders or permission
changes: engineering, delivery, agent-setup, product-design, security,
content-growth, analytics, finance, crypto and forecasting. Presets can overlap and deduplicate.
For a global installation, use the host's effective global skills directory as
`--target`. Use canonical paths where a platform exposes a symlink alias.

The CLI records per-file hashes and per-skill source revisions in
`.ah-skills/state.json` inside the selected installed directory. Identical files
may be adopted; divergent unmanaged files and edited managed files block the whole
apply before content writes. Unchanged managed files can update to the embedded
revision. Updates default to managed skills, preserve unrelated files and obsolete
source files, and never prune previously installed domains. A newer CLI/source
snapshot is needed to obtain newer upstream content; `update` does not fetch GitHub.

Every change has a local backup journal, including prior management state.
Rollback preflights current hashes and refuses to erase subsequent edits. It
restores that change's files/state; newly created empty directories and backup
journals may remain. Backups can contain locally installed content; keep them in
the chosen scope and do not publish them. File replacement is atomic individually;
a process interruption can require recovery from the journal. Do not run concurrent
install/update/rollback operations against the same target.

This is separate from `ah upgrade`, whose existing project-composition behavior
continues to preserve differing files. For a pre-existing unmanaged copy that
differs, review/merge it deliberately; the managed updater does not guess ownership.
Inspect other host discovery paths for duplicate IDs before choosing scope.

## Observed native host verification

On 2026-10-14, an isolated persistent OpenCode v2.0.27 server registered all 59
skills and returned their exact expected Markdown bodies and project paths.
A fresh server's first inventory was empty; the second query on the same server
succeeded. Repeating `--standalone` creates a fresh server and repeats that race.
The CLI's `scripts/opencode_skill_probe.py` retains a reproducible bounded check.
No adapter, account change or model call was needed. Registry/body verification
establishes native loading, not model selection or successful task execution.
