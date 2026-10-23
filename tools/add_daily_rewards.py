import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ocr(text, roi):
    return {'recognition': 'OCR', 'expected': text, 'roi': roi}


page = ocr('今日任务', [180, 60, 350, 130])
purple = {'recognition': 'ColorMatch', 'roi': [578, 560, 36, 40],
          'lower': [80, 40, 165], 'upper': [205, 160, 255], 'count': 25}
gray = {'recognition': 'ColorMatch', 'roi': [578, 560, 36, 40],
        'lower': [145, 145, 145], 'upper': [215, 215, 215], 'count': 55}
claimed = ocr('已领取', [548, 535, 95, 70])
helpers = ['[JumpBack]今日任务奖励确认', '[JumpBack]今日任务奖励关闭']
nodes = {
    '领取今日任务奖励': {'recognition': 'DirectHit', 'action': 'DoNothing',
        'next': ['今日任务主页入口', '今日任务面板已打开'], 'timeout': 8000},
    '今日任务主页入口': {'recognition': 'And', 'all_of': ['完成启动_确认'],
        'action': 'Click', 'target': [235, 55, 2, 2], 'post_delay': 1300,
        'max_hit': 1, 'next': ['今日任务切换日常'], 'timeout': 10000},
    '今日任务面板已打开': {**ocr('签到|日|常|周', [10, 140, 90, 440]),
        'action': 'DoNothing', 'next': ['今日任务切换日常'], 'timeout': 5000},
    '今日任务切换日常': {'recognition': 'DirectHit',
        'action': 'Click', 'target': [48, 365, 2, 2], 'pre_delay': 400,
        'post_delay': 1000, 'max_hit': 1,
        'next': ['今日任务页面检查'], 'timeout': 10000},
    '今日任务页面检查': {**page, 'action': 'DoNothing',
        'next': helpers + ['今日任务八档已领取', '今日任务一键领取'], 'timeout': 8000},
    '今日任务八档已领取': {'recognition': 'And', 'all_of': [page, claimed],
        'action': 'DoNothing', 'next': ['今日任务返回主页'], 'timeout': 5000},
    '今日任务一键领取': {'recognition': 'And', 'all_of': [page,
        ocr('一?键|领取', [1180, 590, 100, 125])], 'action': 'Click',
        'target': [1228, 640, 2, 2], 'pre_delay': 500, 'post_delay': 1200,
        'max_hit': 12, 'next': helpers + ['今日任务页面检查'], 'timeout': 10000},
    '今日任务奖励确认': {'recognition': 'And', 'all_of': [
        ocr('恭喜获得|领取成功|获得奖励', [250, 60, 800, 300]),
        ocr('^确认$|^确定$', [300, 450, 700, 220])], 'box_index': 1,
        'action': 'Click', 'post_delay': 1000, 'max_hit': 15},
    '今日任务奖励关闭': {**ocr('恭喜获得|领取成功|获得奖励', [250, 60, 800, 300]),
        'action': 'Click', 'target': [1100, 640, 2, 2], 'post_delay': 1000, 'max_hit': 15},
    '今日任务返回主页': {**page, 'action': 'Click', 'target': [63, 45, 2, 2],
        'post_delay': 1000, 'max_hit': 3,
        'next': ['完成启动_确认', '今日任务返回主页'], 'timeout': 8000},
}
path = ROOT / 'assets/resource/pipeline/daily_rewards.json'
path.write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
path = ROOT / 'assets/interface.json'
data = json.loads(path.read_text(encoding='utf-8'))
if not any(task['name'] == '领取今日任务奖励' for task in data['task']):
    data['task'].append({'name': '领取今日任务奖励', 'label': '领取今日任务奖励',
        'entry': '领取今日任务奖励'})
for task in data['task']:
    if task['name'] == '领取今日任务奖励':
        task['description'] = '反复一键领取，直到完成数8上方显示已领取，再返回主页；最多点击12次。'
path.write_text(json.dumps(data, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
path = ROOT / 'TODO.md'
todo = path.read_text(encoding='utf-8').replace('- [ ] 领取日常奖励。',
    '- [ ] 领取今日任务奖励：验证一键领取循环、奖励弹窗、8档已领取判断及返回主页。')
todo = todo.replace('8档钻石灰色判断', '8档已领取判断')
path.write_text(todo, encoding='utf-8')
