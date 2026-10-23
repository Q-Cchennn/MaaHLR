"""Dismiss interaction rewards before returning from travel."""
import copy
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline/travel.json'
nodes = json.loads(path.read_text(encoding='utf-8'))
reward = {'recognition': 'OCR', 'roi': [200, 65, 900, 500], 'expected': '领取成功|恭喜获得'}
nodes['出行奖励点击确认'] = {
    'recognition': 'And', 'all_of': [reward, {
        'recognition': 'OCR', 'roi': [350, 450, 600, 220], 'expected': '^确认$|^确定$',
    }],
    'box_index': 1, 'action': 'Click', 'pre_delay': 300, 'post_delay': 1000, 'max_hit': 4,
}
nodes['出行奖励点击空白'] = {
    **copy.deepcopy(reward), 'action': 'Click', 'target': [1100, 500, 40, 30],
    'pre_delay': 300, 'post_delay': 1000, 'max_hit': 4,
}
handlers = ['[JumpBack]出行奖励点击确认', '[JumpBack]出行奖励点击空白']
for name in ('返回人物', '出行点击人物互动', '出行好感已达上限',
             '出行无互动提示', '出行无互动提示复核'):
    refs = nodes[name]['next']
    nodes[name]['next'] = handlers + [ref for ref in refs if ref not in handlers]
nodes['出行点击人物互动']['post_delay'] = 1200
nodes['出行返回主页'].update(
    pre_delay=1000, post_delay=1000, max_hit=3, timeout=8000,
    next=handlers + ['出行返回主页确认', '出行返回主页'],
)
path.write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
