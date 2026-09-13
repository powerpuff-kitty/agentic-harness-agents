#!/usr/bin/env python3
"""Bounded documentation-only skill bundles. Never execute tools or skill content."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
MAX_FILE = 65_536
MAX_TOTAL = 1_048_576
MAX_FILES = 64
NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
PATH = re.compile(r'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\Z')
LINK = re.compile(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)')
HEADINGS = ('Objective', 'Inputs', 'Context', 'Procedure', 'Output', 'Completion')


class BundleError(ValueError):
    """Fixed diagnostics deliberately omit source contents and rejected values."""


def require(ok: bool, message: str) -> None:
    if not ok:
        raise BundleError(message)


def safe_path(value: object) -> bool:
    return (isinstance(value, str) and len(value) <= 256 and bool(PATH.fullmatch(value))
            and all(p not in ('.', '..') and not p.startswith('.') for p in value.split('/')))


def object_only(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'bundle: duplicate JSON key')
        result[key] = value
    return result


def decode(data: bytes):
    try:
        return json.loads(data.decode('utf-8'), object_pairs_hook=object_only)
    except (UnicodeError, json.JSONDecodeError):
        raise BundleError('bundle: invalid UTF-8 JSON') from None


def is_link(meta) -> bool:
    return stat.S_ISLNK(meta.st_mode) or bool(getattr(meta, 'st_file_attributes', 0) & 0x400)


def read_file(path: Path, limit: int = MAX_FILE) -> bytes:
    try:
        before = path.lstat()
        require(stat.S_ISREG(before.st_mode) and not is_link(before), 'bundle: non-regular file refused')
        with path.open('rb') as source:
            data = source.read(limit + 1)
        after = path.lstat()
    except OSError:
        raise BundleError('bundle: unreadable input') from None
    require(len(data) <= limit, 'bundle: file size limit exceeded')
    require(stat.S_ISREG(after.st_mode) and not is_link(after) and before.st_size == after.st_size == len(data)
            and before.st_mtime_ns == after.st_mtime_ns,
            'bundle: input changed while reading')
    return data


def directory(path: Path) -> None:
    try:
        meta = path.lstat()
        require(stat.S_ISDIR(meta.st_mode) and not is_link(meta), 'bundle: real directory required')
    except OSError:
        raise BundleError('bundle: missing directory') from None


def payload(root: Path, name: str) -> dict[str, bytes]:
    require(isinstance(name, str) and len(name) <= 64 and bool(NAME.fullmatch(name)),
            'bundle: invalid skill name')
    directory(root)
    directory(root / 'skills')
    base = root / 'skills' / name
    directory(base)
    files = {}
    visited = 0

    def walk(folder: Path, depth: int):
        nonlocal visited
        require(depth <= 4, 'bundle: directory depth limit exceeded')
        try:
            entries = []
            for entry in folder.iterdir():
                require(visited + len(entries) < MAX_FILES, 'bundle: entry limit exceeded')
                entries.append(entry)
            entries.sort()
        except OSError:
            raise BundleError('bundle: unreadable directory') from None
        for path in entries:
            visited += 1
            require(visited <= MAX_FILES, 'bundle: entry limit exceeded')
            relative = path.relative_to(base).as_posix()
            require(safe_path(relative), 'bundle: unsupported input path')
            try:
                meta = path.lstat()
                require(not is_link(meta), 'bundle: linked input refused')
                mode = meta.st_mode
            except OSError:
                raise BundleError('bundle: unreadable entry') from None
            if stat.S_ISDIR(mode):
                walk(path, depth + 1)
            else:
                files[relative] = read_file(path)
                require(sum(map(len, files.values())) <= MAX_TOTAL, 'bundle: total size limit exceeded')
    walk(base, 0)
    validate_payload(name, files)
    shared = decode(files['bundle.json'])['shared_references']
    for destination, source in shared.items():
        parent = root
        for part in source.split('/')[:-1]:
            parent = parent / part
            directory(parent)
        require(files[destination] == read_file(root / source), 'bundle: shared reference drift')
    require('LICENSE' not in files and 'bundle-lock.json' not in files,
            'bundle: reserved distribution filename')
    files['LICENSE'] = read_file(root / 'LICENSE')
    require(bool(files['LICENSE'].strip()), 'bundle: missing license text')
    require(sum(map(len, files.values())) <= MAX_TOTAL, 'bundle: total size limit exceeded')
    return files


def validate_payload(name: str, files: dict[str, bytes]) -> None:
    require('bundle.json' in files, 'bundle: standalone declaration required')
    declaration = decode(files['bundle.json'])
    require(isinstance(declaration, dict) and set(declaration) == {
        'format_version', 'kind', 'name', 'files', 'optional_tools', 'shared_references'}, 'bundle: invalid declaration fields')
    require(type(declaration['format_version']) is int and declaration['format_version'] == 1
            and declaration['kind'] == 'standalone-skill' and declaration['name'] == name,
            'bundle: incompatible declaration')
    declared = declaration['files']
    require(isinstance(declared, list) and 1 <= len(declared) <= MAX_FILES
            and all(safe_path(p) for p in declared), 'bundle: invalid declared paths')
    require(len(set(declared)) == len(declared) and 'SKILL.md' in declared
            and all(p == 'SKILL.md' or (p.startswith('references/') and p.endswith('.md')) for p in declared),
            'bundle: only declared documentation is supported')
    require(set(files) == set(declared) | {'bundle.json'}, 'bundle: missing or undeclared file')
    shared = declaration['shared_references']
    require(isinstance(shared, dict) and len(shared) <= 8
            and all(safe_path(p) and p in declared and safe_path(source)
                    and source.startswith('references/') and source.endswith('.md')
                    for p, source in shared.items()), 'bundle: invalid shared references')
    tools = declaration['optional_tools']
    require(isinstance(tools, list) and len(tools) <= 8, 'bundle: invalid optional tools')
    names = set()
    for tool in tools:
        require(isinstance(tool, dict) and set(tool) == {'name', 'fallback'}, 'bundle: invalid tool declaration')
        require(isinstance(tool['name'], str) and bool(NAME.fullmatch(tool['name']))
                and tool['name'] not in names, 'bundle: invalid or duplicate tool name')
        names.add(tool['name'])
        require(isinstance(tool['fallback'], str) and 0 < len(tool['fallback']) <= 1024
                and tool['fallback'].strip() == tool['fallback'], 'bundle: explicit tool fallback required')
    for path in declared:
        try:
            text = files[path].decode('utf-8')
        except UnicodeError:
            raise BundleError('bundle: documentation must be UTF-8') from None
        require('\x00' not in text, 'bundle: NUL in documentation')
        # Authoring subset: plain inline, skill-root-relative Markdown links.
        # This is not a complete Markdown parser or a semantic dependency detector.
        for match in LINK.finditer(text):
            target = match.group(1)
            if target.startswith(('https://', '#')):
                continue
            target = target.split('#', 1)[0]
            require(safe_path(target) and target in declared, 'bundle: unresolved local reference')
    text = files['SKILL.md'].decode('utf-8')
    require(text.startswith('---\n') and '\n---\n' in text[4:], 'bundle: invalid skill frontmatter')
    frontmatter, body = text[4:].split('\n---\n', 1)
    lines = frontmatter.splitlines()
    require(len(lines) == 2 and lines[0] == 'name: ' + name and lines[1].startswith('description: '),
            'bundle: expected name/description frontmatter only')
    try:
        description = json.loads(lines[1][len('description: '):])
    except json.JSONDecodeError:
        raise BundleError('bundle: use a quoted description') from None
    require(isinstance(description, str) and 0 < len(description) <= 1024,
            'bundle: invalid description')
    require(all('## ' + heading + '\n' in body for heading in HEADINGS), 'bundle: missing procedure section')


def enrolled(root: Path = ROOT) -> dict[str, dict[str, bytes]]:
    directory(root / 'skills')
    result = {}
    for folder in sorted((root / 'skills').iterdir()):
        if (folder / 'bundle.json').exists() or (folder / 'bundle.json').is_symlink():
            result[folder.name] = payload(root, folder.name)
    require(bool(result), 'bundle: no standalone skills declared')
    return result


def build_archive(root: Path, name: str) -> bytes:
    files = payload(root, name)
    lock = {'format_version': 1, 'kind': 'skill-bundle-lock', 'name': name,
            'files': {p: hashlib.sha256(data).hexdigest() for p, data in sorted(files.items())},
            'verification_scope': 'document bytes and declared local links; no host or model execution'}
    files['bundle-lock.json'] = (json.dumps(lock, sort_keys=True, indent=2) + '\n').encode()
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_STORED) as archive:
        for path, data in sorted(files.items()):
            info = zipfile.ZipInfo(name + '/' + path, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return output.getvalue()


def verify_archive(data: bytes) -> dict:
    require(len(data) <= MAX_TOTAL * 2, 'bundle: archive size limit exceeded')
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()
            require(1 <= len(entries) <= MAX_FILES and len({e.filename for e in entries}) == len(entries),
                    'bundle: invalid archive entry count')
            require(all(safe_path(e.filename) and e.compress_type == zipfile.ZIP_STORED
                        and stat.S_ISREG(e.external_attr >> 16) and e.file_size <= MAX_FILE for e in entries),
                    'bundle: unsupported archive entry')
            require(sum(e.file_size for e in entries) <= MAX_TOTAL, 'bundle: expanded size limit exceeded')
            names = {e.filename.split('/')[0] for e in entries}
            require(len(names) == 1, 'bundle: one skill root required')
            name = names.pop()
            require(bool(NAME.fullmatch(name)), 'bundle: invalid archive root')
            files = {e.filename[len(name) + 1:]: archive.read(e) for e in entries}
    except (zipfile.BadZipFile, OSError, RuntimeError):
        raise BundleError('bundle: unreadable archive') from None
    require('bundle-lock.json' in files and 'LICENSE' in files, 'bundle: distribution metadata missing')
    lock = decode(files.pop('bundle-lock.json'))
    require(isinstance(lock, dict) and set(lock) == {'format_version', 'kind', 'name', 'files', 'verification_scope'}
            and type(lock['format_version']) is int and lock['format_version'] == 1
            and lock['kind'] == 'skill-bundle-lock' and lock['name'] == name
            and lock['verification_scope'] == 'document bytes and declared local links; no host or model execution', 'bundle: invalid lock')
    require(lock['files'] == {p: hashlib.sha256(b).hexdigest() for p, b in sorted(files.items())},
            'bundle: archive content identity mismatch')
    require(bool(files.pop('LICENSE').strip()), 'bundle: missing license text')
    validate_payload(name, files)
    return {'name': name, 'file_count': len(entries), 'sha256': hashlib.sha256(data).hexdigest(),
            'verified': 'document bytes and declared local links only', 'model_execution': 'not-run'}


def verify_collection(archive_path: Path, bundles: dict[str, dict[str, bytes]]) -> None:
    """Verify enrolled payloads in the real collection archive, not a second packaging simulation."""
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        require(len(set(names)) == len(names), 'bundle: duplicate collection member')
        for name, files in bundles.items():
            for path, expected in files.items():
                member = 'LICENSE' if path == 'LICENSE' else f'skills/{name}/{path}'
                require(member in names, 'bundle: collection is missing a declared dependency')
                info = archive.getinfo(member)
                require(info.file_size == len(expected) and archive.read(member) == expected,
                        'bundle: collection payload differs from validated input')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('skill')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        data = build_archive(ROOT, args.skill)
        report = verify_archive(data)
        require(not args.output.resolve().is_relative_to(ROOT.resolve()),
                'bundle: choose an output outside the source repository')
        # No implicit installation, parent creation, overwrite or rollback.
        with args.output.open('xb') as output:
            output.write(data)
            output.flush()
        print(json.dumps(report, sort_keys=True))
        return 0
    except (BundleError, OSError):
        print('Skill packaging failed; existing output is never overwritten. Inspect any incomplete new output before retrying.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
