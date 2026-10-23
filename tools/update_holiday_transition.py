"""Handle delayed reward dialogs and verify the checklist-to-plan transition."""
import copy
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline/holiday.json'
nodes = json.loads(path.read_text(encoding='utf-8'))
nodes['假日返回主页'].update(target=[63, 50, 2, 2], pre_delay=400, post_delay=1000, max_hit=3)
nodes['假日返回主页']['next'] = ['假日返回主页确认', '假日返回主页']
confirm = copy.deepcopy(nodes['假日清单奖励弹窗'])
confirm.pop('next', None)
confirm.update(post_delay=1000, max_hit=6)
nodes['假日过渡奖励确认'] = confirm
nodes['假日过渡奖励关闭'] = {
    'recognition': 'OCR', 'roi': [300, 55, 650, 160],
    'expected': '恭喜获得|领取成功|获得奖励',
    'action': 'Click', 'target': [650, 660, 30, 25],
    'pre_delay': 300, 'post_delay': 1000, 'max_hit': 6,
}
handlers = ['[JumpBack]假日过渡奖励确认', '[JumpBack]假日过渡奖励关闭']
source = nodes['假日清单领取后检查']
nodes['假日切换计划重试'] = {
    'recognition': source['recognition'], 'all_of': copy.deepcopy(source['all_of']),
    'action': 'DoNothing', 'post_delay': 700, 'max_hit': 2,
    'next': ['假日点击计划'], 'timeout': 5000,
}
nodes['假日点击计划'].update(pre_delay=600, post_delay=1000, max_hit=3, timeout=8000)
refs = nodes['假日点击计划']['next']
if '假日切换计划重试' not in refs:
    refs.append('假日切换计划重试')
for name, node in nodes.items():
    if name in ('假日过渡奖励确认', '假日过渡奖励关闭'):
        continue
    refs = node.get('next')
    if refs:
        node['next'] = handlers + [ref for ref in refs if ref not in handlers]
path.write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
