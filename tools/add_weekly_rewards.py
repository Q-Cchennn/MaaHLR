import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ocr(text, roi):
    return {'recognition': 'OCR', 'expected': text, 'roi': roi}


page = ocr('本周任务', [180, 60, 350, 130])
helpers = ['[JumpBack]今日任务奖励确认', '[JumpBack]今日任务奖励关闭']
nodes = {
    '周常领取': {'recognition': 'DirectHit', 'action': 'DoNothing',
        'next': ['周常主页入口', '周常面板已打开'], 'timeout': 8000},
    '周常主页入口': {'recognition': 'And', 'all_of': ['完成启动_确认'],
        'action': 'Click', 'target': [235, 55, 2, 2], 'post_delay': 1300,
        'max_hit': 1, 'next': ['周常切换周常'], 'timeout': 10000},
    '周常面板已打开': {**ocr('签到|日|常|周', [10, 140, 90, 440]),
        'action': 'DoNothing', 'next': ['周常切换周常'], 'timeout': 5000},
    '周常切换周常': {'recognition': 'DirectHit', 'action': 'Click',
        'target': [48, 525, 2, 2], 'pre_delay': 400, 'post_delay': 1000,
        'max_hit': 1, 'next': ['周常页面检查'], 'timeout': 10000},
    '周常页面检查': {**page, 'action': 'DoNothing',
        'next': helpers + ['周常首项已变前往', '周常一键领取'], 'timeout': 8000},
    '周常首项已变前往': {'recognition': 'And', 'all_of': [page,
        ocr('前往', [1010, 155, 180, 85])], 'action': 'DoNothing',
        'post_delay': 700, 'next': ['周常完成复核'], 'timeout': 5000},
    '周常完成复核': {'recognition': 'And', 'all_of': [page,
        ocr('前往', [1010, 155, 180, 85])], 'action': 'DoNothing',
        'next': ['周常补领完成数第一次'], 'timeout': 5000},
    '周常一键领取': {'recognition': 'And', 'all_of': [page,
        ocr('一?键|领取', [1180, 590, 100, 125])], 'action': 'Click',
        'target': [1228, 640, 2, 2], 'pre_delay': 500, 'post_delay': 1200,
        'max_hit': 12, 'next': helpers + ['周常页面检查'], 'timeout': 10000},
    '周常返回主页': {**page, 'action': 'Click', 'target': [63, 45, 2, 2],
        'post_delay': 1000, 'max_hit': 3,
        'next': ['完成启动_确认', '周常返回主页'], 'timeout': 8000},
}
for suffix, next_node in [('第一次', '周常补领完成数第二次'), ('第二次', '周常返回主页')]:
    click_name = f'周常补领完成数{suffix}'
    check_name = f'周常补领后检查{suffix}'
    nodes[click_name] = {'recognition': 'And', 'all_of': [page,
        ocr('一?键|领取', [1180, 590, 100, 125])], 'action': 'Click',
        'target': [1228, 640, 2, 2], 'pre_delay': 500, 'post_delay': 1200,
        'max_hit': 1, 'next': helpers + [check_name], 'timeout': 10000}
    nodes[check_name] = {**page, 'action': 'DoNothing', 'post_delay': 500,
        'next': helpers + [next_node], 'timeout': 8000}
path = ROOT / 'assets/resource/pipeline/weekly_rewards.json'
path.write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
path = ROOT / 'assets/interface.json'
data = json.loads(path.read_text(encoding='utf-8'))
if not any(task['name'] == '周常领取' for task in data['task']):
    data['task'].append({'name': '周常领取', 'label': '周常领取',
        'entry': '周常领取'})
for task in data['task']:
    if task['name'] == '周常领取':
        task['description'] = '先切换周常并确认本周任务，循环一键领取；第一项显示前往后额外领取两次任务完成数奖励，再返回主页。'
path.write_text(json.dumps(data, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
path = ROOT / 'TODO.md'
todo = path.read_text(encoding='utf-8')
item = '- [ ] 周常领取：验证周常页签切换、本周任务标题、重复领取、首项前往判断及返回主页。'
if item not in todo:
    path.write_text(todo.rstrip() + '\n\n' + item + '\n', encoding='utf-8')
