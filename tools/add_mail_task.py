import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ocr(text, roi):
    return {'recognition': 'OCR', 'expected': text, 'roi': roi}


page = ocr('邮件', [110, 10, 200, 85])
helpers = ['[JumpBack]今日任务奖励确认', '[JumpBack]今日任务奖励关闭']
nodes = {
    '领取邮件': {'recognition': 'DirectHit', 'action': 'DoNothing',
        'next': ['邮件全部领取并已读', '邮件主页入口'], 'timeout': 8000},
    '邮件主页入口': {'recognition': 'And', 'all_of': ['完成启动_确认'],
        'action': 'Click', 'target': [145, 55, 2, 2], 'post_delay': 1300,
        'max_hit': 1, 'next': ['邮件全部领取并已读'], 'timeout': 10000},
    '邮件全部领取并已读': {'recognition': 'And', 'all_of': [page,
        ocr('全部领取|全部领|并已读', [1130, 460, 150, 150])],
        'action': 'Click', 'target': [1215, 545, 2, 2],
        'pre_delay': 600, 'post_delay': 1500, 'max_hit': 1,
        'next': helpers + ['邮件领取后检查'], 'timeout': 10000},
    '邮件领取后检查': {**page, 'action': 'DoNothing', 'post_delay': 800,
        'next': helpers + ['邮件返回主页'], 'timeout': 10000},
    '邮件返回主页': {**page, 'action': 'Click', 'target': [63, 45, 2, 2],
        'pre_delay': 300, 'post_delay': 1000, 'max_hit': 3,
        'next': helpers + ['完成启动_确认', '邮件返回主页'], 'timeout': 8000},
}
path = ROOT / 'assets/resource/pipeline/mail.json'
path.write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
path = ROOT / 'assets/interface.json'
data = json.loads(path.read_text(encoding='utf-8'))
if not any(task['name'] == '领取邮件' for task in data['task']):
    data['task'].append({'name': '领取邮件', 'label': '领取邮件',
        'entry': '领取邮件', 'description': '进入邮件，点击全部领取并已读，处理奖励弹窗后返回主页。'})
path.write_text(json.dumps(data, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
path = ROOT / 'TODO.md'
todo = path.read_text(encoding='utf-8')
item = '- [ ] 领取邮件：验证信封入口、全部领取并已读、奖励弹窗及返回主页。'
if item not in todo:
    path.write_text(todo.rstrip() + '\n\n' + item + '\n', encoding='utf-8')
