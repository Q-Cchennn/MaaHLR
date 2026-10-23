"""Recognize the home travel entrance without requiring identical background art."""
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline/travel.json'
nodes = json.loads(path.read_text(encoding='utf-8'))
branches = ['出行门口有人过渡页', '确定人物', '人物选择', '出行选择']
nodes['出行门口有人过渡页'] = {
    'recognition': 'And',
    'all_of': [
        {'recognition': 'OCR', 'roi': [95, 10, 330, 80], 'expected': '课后出行'},
        {'recognition': 'OCR', 'roi': [400, 310, 500, 100], 'expected': '家门口.*有人找你|似乎有人找你'},
    ],
    'action': 'Click', 'target': [600, 525, 80, 50],
    'pre_delay': 400, 'post_delay': 1000, 'max_hit': 2,
    'next': branches, 'timeout': 10000,
}
for name in ('出行', '进入出行', '出行选择'):
    refs = nodes[name]['next']
    if '出行门口有人过渡页' not in refs:
        refs.insert(0, '出行门口有人过渡页')
entry = nodes['进入出行']
for key in ('template', 'roi', 'threshold'):
    entry.pop(key, None)
entry.update(
    recognition='Or',
    any_of=[
        {'recognition': 'OCR', 'roi': [10, 350, 130, 130], 'expected': '出行'},
        {'recognition': 'TemplateMatch', 'template': '日常/主页出行入口.png',
         'roi': [10, 345, 130, 140], 'threshold': 0.84},
    ],
    target=[40, 375, 40, 45],
    pre_delay=600,
    post_delay=1200,
    timeout=8000,
)
path.write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
