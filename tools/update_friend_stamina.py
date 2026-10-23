"""Distinguish the enabled brown button from the claimed gray button."""
import copy
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline/friend.json'
nodes = json.loads(path.read_text(encoding='utf-8'))
text = {'recognition': 'OCR', 'roi': [940, 625, 250, 85], 'expected': '赠领'}
button = [970, 645, 160, 35]
nodes['点击领取体力'] = {
    'recognition': 'And',
    'all_of': [text, {
        'recognition': 'ColorMatch', 'method': 4, 'roi': button,
        'lower': [50, 35, 20], 'upper': [155, 130, 110], 'count': 1500,
    }],
    'box_index': 0, 'action': 'Click',
    'pre_wait_freezes': {'time': 500, 'target': [940, 625, 250, 85], 'timeout': 4000},
    'pre_delay': 1000, 'post_delay': 1200,
    'max_hit': 2, 'timeout': 10000,
    'next': ['确认领取成功-好友', '好友赠领已完成'],
    'on_error': ['好友体力异常分流'],
}
nodes['好友赠领已完成'] = {
    'recognition': 'And',
    'all_of': [text, {
        'recognition': 'ColorMatch', 'method': 4, 'roi': button,
        'lower': [175, 175, 175], 'upper': [245, 245, 245], 'count': 2000,
    }],
    'action': 'DoNothing', 'next': ['好友关闭页面'],
}
nodes['进入好友']['post_delay'] = 1200
nodes['好友体力异常分流'] = {
    'next': ['确认领取成功-好友', '好友赠领已完成', '好友体力领取重试检查'],
}
nodes['好友体力领取重试检查'] = {
    'recognition': 'And',
    'all_of': copy.deepcopy(nodes['点击领取体力']['all_of']),
    'action': 'DoNothing', 'post_delay': 800, 'max_hit': 1,
    'next': ['确认领取成功-好友', '好友赠领已完成', '点击领取体力'],
    'timeout': 5000,
}
path.write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
