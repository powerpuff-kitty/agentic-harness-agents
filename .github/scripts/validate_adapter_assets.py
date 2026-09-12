#!/usr/bin/env python3
"""Validate shipped adapter bytes, not host execution or instruction adherence."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = {
    'claude': [
        ('claude/files/CLAUDE.md', 'CLAUDE.md', 'base'),
        ('claude/files/.claude/rules/agentic-typed-ui.md', '.claude/rules/agentic-typed-ui.md', 'typed-ui'),
    ],
    'cursor': [('cursor/files/.cursor/rules/agentic-typed-ui.mdc', '.cursor/rules/agentic-typed-ui.mdc', 'typed-ui')],
    'codex': [],
}
PATTERNS = ['**/*.ts', '**/*.tsx', '**/*.vue']
SOURCES = {
    'claude': 'https://code.claude.com/docs/en/memory',
    'cursor': 'https://cursor.com/docs/rules',
    'codex': 'https://developers.openai.com/codex/guides/agents-md',
}


def frontmatter(text: str) -> tuple[dict, str]:
    """Parse the deliberately restricted JSON-valued YAML subset used by these assets."""
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ValueError('missing or incomplete frontmatter')
    header, body = text[4:].split('\n---\n', 1)
    result = {}
    for line in header.splitlines():
        key, separator, value = line.partition(':')
        if not separator or key in result or not key.strip():
            raise ValueError('ambiguous frontmatter')
        result[key] = json.loads(value)
    return result, body


def validate_bundle(index: object, assets: dict[str, str]) -> list[str]:
    errors = []
    if not isinstance(index, dict) or type(index.get('format_version')) is not int or index.get('format_version') != 1:
        return ['adapters: invalid asset manifest version']
    if set(index) != {'format_version','kind','installation','profiles','adapters','modifies_host_permissions','executes_commands'}:
        errors.append('adapters: missing or unknown manifest fields')
    if index.get('kind') != 'native-adapter-assets' or index.get('installation') != 'manual-review':
        errors.append('adapters: unsupported distribution claims')
    if index.get('modifies_host_permissions') is not False or index.get('executes_commands') is not False:
        errors.append('adapters: assets must not claim permissions or command execution')
    if not isinstance(index.get('profiles'), dict):
        return errors + ['adapters: invalid profiles']
    if any(not isinstance(value, dict) for value in index['profiles'].values()):
        return errors + ['adapters: invalid profile record']
    if index.get('profiles') != {'base': {'default': True}, 'typed-ui': {'default': False, 'patterns': PATTERNS}} or any(
        type((index.get('profiles') or {}).get(key, {}).get('default')) is not bool for key in ['base', 'typed-ui']
    ):
        errors.append('adapters: typed-ui must remain explicitly opt-in with reviewed patterns')
    entries = index.get('adapters')
    if not isinstance(entries, list):
        return errors + ['adapters: missing adapter list']
    ids = [entry.get('id') if isinstance(entry, dict) else None for entry in entries]
    if len(ids) != 3 or set(x for x in ids if isinstance(x, str)) != set(FILES):
        return errors + ['adapters: missing, duplicate or unsupported host']
    for entry in entries:
        host = entry['id']
        if set(entry) != {'id','router','router_loading','files','documentation','reviewed_at','host_execution'}:
            errors.append(f'{host}: missing or unknown adapter fields')
        if entry.get('router') != 'AGENTS.md' or entry.get('router_loading') != ('import' if host == 'claude' else 'native'):
            errors.append(f'{host}: canonical router or native loading mismatch')
        expected = [{'source':s,'target':t,'profile':p} for s,t,p in FILES[host]]
        if entry.get('files') != expected:
            errors.append(f'{host}: unexpected asset, target or profile (details omitted)')
        if entry.get('documentation') != SOURCES[host] or entry.get('reviewed_at') != '2026-09-12':
            errors.append(f'{host}: source review metadata drift')
        if entry.get('host_execution') != {'status':'not-run','version':None,'evidence':[]}:
            errors.append(f'{host}: host execution requires separately reviewed evidence')
    expected_sources = {s for entries in FILES.values() for s,_,_ in entries}
    if set(assets) != expected_sources:
        errors.append('adapters: missing or unexpected shipped asset')
    if assets.get('claude/files/CLAUDE.md') != '@AGENTS.md\n':
        errors.append('claude: root import must be active and project-relative, not fenced or copied truth')
    bodies = []
    for host in ['claude', 'cursor']:
        source = FILES[host][-1][0]
        text = assets.get(source)
        if not isinstance(text, str) or len(text.encode('utf-8')) > 1500:
            errors.append(f'{host}: missing or oversized scoped rule')
            continue
        try:
            meta, body = frontmatter(text)
        except (ValueError, TypeError):
            errors.append(f'{host}: invalid scoped-rule frontmatter')
            continue
        if host == 'claude' and meta != {'paths': PATTERNS}:
            errors.append('claude: path-scoped rule metadata mismatch')
        if host == 'cursor' and (meta.get('alwaysApply') is not False or meta != {
            'description':'Use accepted project architecture and design context for typed UI changes.',
            'globs':','.join(PATTERNS), 'alwaysApply':False,
        }):
            errors.append('cursor: scoped rule must not be always applied or widen its patterns')
        for token in ['`AGENTS.md`', '`.agentic/`', 'custom routes', 'not runtime enforcement']:
            if token not in body:
                errors.append(f'{host}: missing canonical routing or evidence boundary')
        if '@' in body or '```' in body:
            errors.append(f'{host}: scoped rules must not import unreviewed files or commands')
        bodies.append(body)
    if len(bodies) == 2 and bodies[0] != bodies[1]:
        errors.append('adapters: shared scoped guidance has diverged between hosts')
    return errors


def load_bundle(root: Path = ROOT) -> tuple[dict, dict[str, str]]:
    index = json.loads((root / 'adapters/assets.json').read_text(encoding='utf-8'))
    # Read only the reviewed product paths, never source paths supplied by a manifest.
    assets = {s: (root / 'adapters' / s).read_text(encoding='utf-8')
              for entries in FILES.values() for s,_,_ in entries}
    return index, assets


def validate_repository(root: Path = ROOT) -> list[str]:
    try:
        index, assets = load_bundle(root)
        errors = validate_bundle(index, assets)
        if (root / 'CLAUDE.md').read_text(encoding='utf-8') != assets['claude/files/CLAUDE.md']:
            errors.append('adapters: self-hosting CLAUDE.md differs from the shipped root import')
        return errors
    except (OSError, UnicodeError, ValueError):
        return ['adapters: unreadable or malformed product assets (details omitted)']


if __name__ == '__main__':
    errors = validate_repository()
    if errors:
        raise SystemExit('\n'.join(errors))
    print('Native adapter assets valid; host execution and instruction adherence remain unverified')
