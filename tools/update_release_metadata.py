"""Keep the public beta version and in-app announcement in one place."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = '2.0.0-beta.1'


def apply_release_metadata(interface):
    interface['version'] = VERSION
    interface['description'] = 'Maa海螺肉 · 时空中的绘旅人B服日常助手，新版公开测试版。'
    interface['welcome'] = (ROOT / 'assets/announcement.md').read_text(encoding='utf-8').strip()
    return interface


if __name__ == '__main__':
    path = ROOT / 'assets/interface.json'
    interface = apply_release_metadata(json.loads(path.read_text(encoding='utf-8')))
    path.write_text(json.dumps(interface, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
