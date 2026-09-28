import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validate', ROOT / 'scripts/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class CatalogValidationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in ['marketplace.json', 'README.md', 'README.zh-CN.md', 'LICENSE']:
            shutil.copy2(ROOT / name, self.root / name)
        shutil.copytree(ROOT / 'plugins', self.root / 'plugins')

    def test_current_catalog(self):
        self.assertEqual(validator.validate(self.root), (3, 4))

    def test_catalog_boundaries(self):
        original = json.loads((self.root / 'marketplace.json').read_text())
        cases = {
            'duplicate identity': lambda m: m['plugins'].append(copy.deepcopy(m['plugins'][0])),
            'path traversal': lambda m: m['plugins'][0]['source'].update(path='../escape'),
            'absolute path': lambda m: m['plugins'][0]['source'].update(path='/tmp/escape'),
            'remote entry': lambda m: m['plugins'][0]['source'].update(source='git'),
            'entry mismatch': lambda m: m['plugins'][0].update(name='different'),
            'missing plugin': lambda m: m['plugins'][0]['source'].update(path='./plugins/missing'),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                manifest = copy.deepcopy(original)
                mutate(manifest)
                (self.root / 'marketplace.json').write_text(json.dumps(manifest))
                with self.assertRaises(ValueError):
                    validator.validate(self.root)

    def test_bundle_boundaries(self):
        plugin = self.root / 'plugins/docs-lookup'
        manifest_path = plugin / '.codex-plugin/plugin.json'
        original = json.loads(manifest_path.read_text())
        for field, value in [('name', 'different'), ('version', 'latest'), ('license', 'unknown'),
                             ('skills', '../skills'), ('mcpServers', './connector.json'),
                             ('apps', './bindings.json')]:
            with self.subTest(field=field):
                manifest = {**original, field: value}
                manifest_path.write_text(json.dumps(manifest))
                with self.assertRaises(ValueError):
                    validator.validate(self.root)
        manifest_path.write_text(json.dumps(original))
        license_path = plugin / 'LICENSE'
        license_path.write_text('incomplete license')
        with self.assertRaises(ValueError):
            validator.validate(self.root)
        license_path.unlink()
        with self.assertRaises(ValueError):
            validator.validate(self.root)
        license_path.write_text((self.root / 'LICENSE').read_text())
        (plugin / '.mcp.json').write_text('{}')
        with self.assertRaises(ValueError):
            validator.validate(self.root)
        (plugin / '.mcp.json').unlink()
        (plugin / 'escaped').symlink_to(self.root.parent)
        with self.assertRaises(ValueError):
            validator.validate(self.root)

    def test_skill_and_documentation_contract(self):
        skill = self.root / 'plugins/docs-lookup/skills/library-docs/SKILL.md'
        original = skill.read_text()
        skill.write_text(original.replace('name: library-docs', 'name: wrong'))
        with self.assertRaises(ValueError):
            validator.validate(self.root)
        skill.write_text(original)
        skill.write_text(original.replace('description:', 'description: ' + 'x' * 301))
        with self.assertRaises(ValueError):
            validator.validate(self.root)
        skill.write_text(original)
        readme = self.root / 'README.zh-CN.md'
        readme.write_text(readme.read_text().replace('(plugins/docs-lookup)', '(plugins/missing)'))
        with self.assertRaises(ValueError):
            validator.validate(self.root)


if __name__ == '__main__':
    unittest.main()
