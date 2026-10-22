"""Validate schemas, node references and image dependencies without game input.

Dependency: pip install jsonschema
"""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
if (ROOT / '.validation-deps').is_dir():
    sys.path.insert(0, str(ROOT / '.validation-deps'))

from jsonschema import validators
from referencing import Registry, Resource


def main():
    schema_dir = ROOT / 'deps/tools'
    registry = Registry()
    for path in schema_dir.glob('*.schema.json'):
        value = json.loads(path.read_text(encoding='utf-8-sig'))
        value.setdefault('$schema', 'https://json-schema.org/draft/2020-12/schema')
        registry = registry.with_resource(path.resolve().as_uri(), Resource.from_contents(value))
    nodes = {}
    errors = []
    interface = ROOT / 'assets/interface.json'
    paths = [interface, *sorted((ROOT / 'assets/resource/pipeline').glob('*.json'))]
    for path in paths:
        data = json.loads(path.read_text(encoding='utf-8-sig'))
        schema_path = schema_dir / ('interface.schema.json' if path == interface else 'pipeline.schema.json')
        schema = json.loads(schema_path.read_text(encoding='utf-8-sig'))
        schema['$id'] = schema_path.resolve().as_uri()
        for error in validators.validator_for(schema)(schema, registry=registry).iter_errors(data):
            errors.append(f'{path.name} {list(error.path)}: {error.message}')
        if path != interface:
            for name, node in data.items():
                if name in nodes:
                    errors.append(f'Duplicate node: {name}')
                nodes[name] = node
    for name, node in nodes.items():
        for key in ('next', 'on_error'):
            refs = node.get(key, [])
            for ref in ([refs] if isinstance(refs, str) else refs):
                target = ref if isinstance(ref, str) else ref['name']
                target = re.sub(r'^(\[[^]]+\])+', '', target)
                if target not in nodes:
                    errors.append(f'{name}: missing node {target}')
        if node.get('recognition') == 'TemplateMatch':
            templates = node.get('template', [])
            for template in ([templates] if isinstance(templates, str) else templates):
                if not (ROOT / 'assets/resource/image' / template).is_file():
                    errors.append(f'{name}: missing template {template}')
    for task in json.loads(interface.read_text(encoding='utf-8'))['task']:
        if task['entry'] not in nodes:
            errors.append(f'Missing task entry: {task["entry"]}')
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'PASS: schemas, task entries, node references, templates ({len(nodes)} nodes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
