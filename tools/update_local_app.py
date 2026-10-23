"""Sync project resources into the standalone Windows client, preserving user config."""
import argparse
import json
import shutil
from pathlib import Path
from task_descriptions import apply_descriptions
from default_daily_config import configure_defaults, seed_config
from update_release_metadata import apply_release_metadata

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=ROOT / 'install/MaaHLR-Windows')
    args = parser.parse_args()
    target = args.destination.resolve()
    if not (target / 'MFAAvalonia.exe').is_file():
        parser.error('Extract the official MFAAvalonia Windows client into the destination first.')
    model = ROOT / 'assets/resource/model/ocr'
    for name in ('det.onnx', 'rec.onnx', 'keys.txt'):
        if not (model / name).is_file():
            parser.error(f'Missing OCR model: {model / name}')
    shutil.copytree(ROOT / 'assets/resource', target / 'resource', dirs_exist_ok=True)
    interface = json.loads((ROOT / 'assets/interface.json').read_text(encoding='utf-8'))
    apply_descriptions(interface)
    configure_defaults(interface)
    apply_release_metadata(interface)
    seed_config(target, interface)
    shutil.copy2(ROOT / 'assets/logo.ico', target / 'logo.ico')
    shutil.copy2(ROOT / 'assets/logo-conch-transparent.png', target / 'logo.png')
    shutil.copy2(ROOT / 'assets/announcement.md', target / 'announcement.md')
    # MFAAvalonia extension: replace its default multi-part window heading.
    interface['custom_title'] = interface.get('label', interface['name'])
    (target / 'interface.json').write_text(json.dumps(interface, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
    for name in ('README.md', 'LICENSE', 'TODO.md'):
        shutil.copy2(ROOT / name, target / name)
    manifest = {'client': 'MFAAvalonia v2.16.2', 'version': interface['version'], 'task_count': len(interface['task']),
                'tasks': [task['name'] for task in interface['task']]}
    (target / 'MaaHLR-resources.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Updated {len(interface["task"])} tasks: {target}')


if __name__ == '__main__':
    main()
