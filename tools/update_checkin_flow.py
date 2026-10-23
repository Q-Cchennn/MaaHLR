"""Apply startup/check-in handling for the monthly-calendar screens."""
import json
from pathlib import Path


root = Path(__file__).resolve().parents[1]
path = root / 'assets/resource/pipeline/start.json'
startup = json.loads(path.read_text(encoding='utf-8'))
startup['启动抵达签到页面'] = {
    'recognition': 'And',
    'all_of': [
        '签到页面标识',
        {'recognition': 'OCR', 'roi': [10, 130, 90, 160], 'expected': '签到'},
    ],
    'action': 'DoNothing',
}
for name in ('启动游戏', '启动界面检查', '完成启动'):
    refs = startup[name]['next']
    if '启动抵达签到页面' not in refs:
        refs.insert(0, '启动抵达签到页面')
path.write_text(json.dumps(startup, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')

path = root / 'assets/resource/pipeline/checkin.json'
checkin = json.loads(path.read_text(encoding='utf-8'))
# Always switch tabs after entering the calendar; it remembers the last tab.
checkin['进入日历']['next'] = ['签到切换左侧签到']
checkin['进入日历']['post_delay'] = 1000
checkin['签到切换左侧签到'] = {
    'recognition': 'OCR', 'expected': '^签$|签到', 'roi': [15, 140, 75, 135],
    'action': 'Click', 'target': [48, 215, 2, 2],
    'pre_delay': 600, 'post_delay': 900, 'max_hit': 3,
    'next': ['签到页签已打开', '签到切换左侧签到'], 'timeout': 8000,
}
checkin['签到页签已打开'] = {
    'recognition': 'And', 'all_of': ['签到页面标识'], 'action': 'DoNothing',
    'next': ['确认领取成功-签到', '检测弹窗', '签到今日已领取', '签到今日可领取'],
    'timeout': 8000,
}
checkin['检测弹窗'] = {
    'recognition': 'And',
    'all_of': [
        {'recognition': 'OCR', 'roi': [280, 300, 730, 100], 'expected': '月卡|签到奖励双倍'},
        {'recognition': 'OCR', 'roi': [350, 425, 225, 100], 'expected': '直接领取'},
    ],
    'box_index': 1, 'action': 'Click', 'pre_delay': 200, 'post_delay': 600,
    'max_hit': 1,
    'next': ['确认领取成功-签到', '签到今日已领取'], 'timeout': 5000,
}
checkin['确认领取成功-签到'].update(post_delay=500, timeout=5000)
checkin['签到关闭页面'] = {
    'recognition': 'And',
    'all_of': [
        '签到页面标识',
        {'recognition': 'OCR', 'roi': [10, 130, 90, 160], 'expected': '签到'},
    ],
    'action': 'Click', 'target': [45, 25, 35, 35],
    'pre_delay': 200, 'post_delay': 800, 'max_hit': 3,
    'next': ['签到返回主页确认', '签到关闭页面'], 'timeout': 5000,
}
path.write_text(json.dumps(checkin, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')

path = root / 'assets/resource/pipeline/checkin_days.json'
days = json.loads(path.read_text(encoding='utf-8'))
for name, node in days.items():
    if name.endswith('可领取'):
        # Encoded ADB screenshots may render the unclaimed white tile warm white.
        # Keep this disjoint from the claimed tile's upper RGB [248,240,239].
        node['all_of'][2]['lower'] = [249, 245, 240]
        # The day is selected by its red ring, never by the computer's date.
        node['next'] = ['检测弹窗', '确认领取成功-签到', '签到今日已领取']
        node.update(post_delay=700, timeout=6000, max_hit=1)
path.write_text(json.dumps(days, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
