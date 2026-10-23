"""Remove obsolete development suffixes without changing task identifiers."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'assets/interface.json'
interface = json.loads(path.read_text(encoding='utf-8'))
for task in interface['task']:
    if 'label' in task:
        task['label'] = task['label'].replace(' · 待实测', '')
path.write_text(json.dumps(interface, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
for path in (ROOT / 'tools').glob('add_*.py'):
    source = path.read_text(encoding='utf-8')
    updated = source.replace(' · 待实测', '')
    if updated != source:
        path.write_text(updated, encoding='utf-8')
