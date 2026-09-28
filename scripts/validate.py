"""Validate the official skills-only catalog without third-party dependencies."""
import json
from pathlib import Path
import re
import sys

NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
VERSION = re.compile(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)\Z')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_object(path):
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        raise ValueError(f'{path}: {error}') from error
    require(isinstance(value, dict), f'{path}: expected a JSON object')
    return value


def validate(root):
    root = root.resolve()
    for path in root.rglob('*'):
        if '.git' in path.relative_to(root).parts:
            continue
        require(not path.is_symlink(), f'{path}: symlinks are not distributable')
    catalog = read_object(root / 'marketplace.json')
    require(catalog.get('name') == 'ducoro', 'marketplace identity must be ducoro')
    entries = catalog.get('plugins')
    require(isinstance(entries, list) and entries, 'catalog must contain plugins')
    require((root / 'LICENSE').is_file(), 'LICENSE is required')
    readmes = [(root / name).read_text(encoding='utf-8') for name in ['README.md', 'README.zh-CN.md']]
    require('(README.zh-CN.md)' in readmes[0], 'English README must link to Chinese')
    require('(README.md)' in readmes[1], 'Chinese README must link to English')
    plugin_names, skill_names = set(), set()
    for entry in entries:
        require(isinstance(entry, dict), 'plugin entry must be an object')
        name = entry.get('name')
        require(isinstance(name, str) and NAME.fullmatch(name), f'invalid plugin name: {name}')
        require(name not in plugin_names, f'duplicate plugin: {name}')
        plugin_names.add(name)
        source = entry.get('source')
        require(isinstance(source, dict), f'{name}: source must be an object')
        require(source.get('source') == 'local', f'{name}: source must be local')
        require(source.get('path') == f'./plugins/{name}', f'{name}: source must point to its bundle')
        bundle = root / 'plugins' / name
        license_path = bundle / 'LICENSE'
        require(license_path.is_file(), f'{name}: bundle LICENSE is required')
        require(license_path.read_bytes() == (root / 'LICENSE').read_bytes(),
                f'{name}: bundle must carry the full repository license')
        manifest = read_object(bundle / '.codex-plugin/plugin.json')
        require(manifest.get('name') == name, f'{name}: manifest identity mismatch')
        require(isinstance(manifest.get('version'), str) and VERSION.fullmatch(manifest['version']),
                f'{name}: version must be major.minor.patch')
        require(isinstance(manifest.get('description'), str) and manifest['description'].strip(),
                f'{name}: description is required')
        require(manifest.get('license') == 'Apache-2.0', f'{name}: license must be Apache-2.0')
        require(manifest.get('skills') == './skills/', f'{name}: skills must be ./skills/')
        require(not {'mcpServers', 'apps'} & manifest.keys(), f'{name}: connector components are not part of this skills-only catalog')
        for forbidden in ['.mcp.json', '.app.json']:
            require(not (bundle / forbidden).exists(), f'{name}: distribute connector dependencies through skill metadata')
        skills = bundle / 'skills'
        require(skills.is_dir(), f'{name}: missing skills directory')
        directories = sorted(skills.iterdir())
        require(directories, f'{name}: at least one skill is required')
        for skill in directories:
            require(skill.is_dir() and NAME.fullmatch(skill.name), f'{skill}: invalid skill directory')
            require(skill.name not in skill_names, f'duplicate skill: {skill.name}')
            skill_names.add(skill.name)
            try:
                body = (skill / 'SKILL.md').read_text(encoding='utf-8')
            except OSError as error:
                raise ValueError(f'{skill}: missing SKILL.md') from error
            parts = body.split('---', 2)
            require(len(parts) == 3 and not parts[0].strip(), f'{skill}: missing YAML frontmatter')
            require(re.search(rf'^name:\s*{re.escape(skill.name)}\s*$', parts[1], re.M),
                    f'{skill}: frontmatter name must match directory')
            require(re.search(r'^description:\s*\S.+$', parts[1], re.M), f'{skill}: description is required')
            require(parts[2].strip(), f'{skill}: instructions are required')
            require((skill / 'agents/openai.yaml').is_file(), f'{skill}: discovery metadata is required')
        for readme in readmes:
            require(f'(plugins/{name})' in readme, f'{name}: missing README catalog link')
    on_disk = {p.name for p in (root / 'plugins').iterdir() if p.is_dir()}
    require(on_disk == plugin_names, 'every plugin directory must be registered exactly once')
    return len(plugin_names), len(skill_names)


if __name__ == '__main__':
    try:
        plugins, skills = validate(Path(__file__).resolve().parents[1])
    except (ValueError, OSError) as error:
        print(f'Validation failed: {error}', file=sys.stderr)
        sys.exit(1)
    print(f'Validated {plugins} plugins and {skills} skills.')
