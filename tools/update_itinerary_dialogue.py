"""Advance itinerary dialogue until the final completion button appears."""
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline/itinerary.json'
nodes = json.loads(path.read_text(encoding='utf-8'))
nodes['进入日程'].update(
    recognition='And', all_of=[{'recognition': 'OCR', 'expected': '校园', 'roi': [110, 10, 180, 80]}],
    target=[1088, 666, 2, 2], post_delay=1000, max_hit=1,
)
nodes['进入日程'].pop('expected', None)
nodes['进入日程'].pop('roi', None)
title = {'recognition': 'OCR', 'roi': [125, 15, 135, 70], 'expected': '日程'}
tail = ['完成日程', '日程对话继续']
nodes['点击信封']['next'] = tail
nodes['点击信封']['post_delay'] = 700
nodes['点击信封']['timeout'] = 10000
nodes['日程对话继续'] = {
    'recognition': 'And',
    'all_of': [title, {
        'recognition': 'OCR', 'roi': [680, 530, 350, 140], 'expected': '[一-龥]{2,}',
    }],
    'action': 'Click', 'target': [730, 580, 150, 45],
    'pre_delay': 200, 'post_delay': 900, 'max_hit': 40,
    'next': tail, 'timeout': 10000,
}
for name in ('点击对话1', '点击对话2', '点击对话3'):
    nodes[name] = {'recognition': 'DirectHit', 'action': 'DoNothing', 'next': tail, 'timeout': 10000}
nodes['完成日程'] = {
    'recognition': 'And',
    'all_of': [title, {
        'recognition': 'OCR', 'roi': [1060, 535, 150, 85], 'expected': '^完成$',
    }],
    'box_index': 1, 'action': 'Click', 'pre_delay': 300, 'post_delay': 800,
    'max_hit': 1, 'next': ['日程关闭页面'], 'timeout': 5000,
}
refs = nodes['日程']['next']
nodes['日程']['next'] = tail + [r for r in refs if r not in tail]
nodes['日程今日已完成'] = {
    'recognition': 'And',
    'all_of': [
        title,
        {'recognition': 'OCR', 'roi': [1050, 90, 150, 110], 'expected': '月'},
        {'recognition': 'OCR', 'roi': [440, 185, 560, 125], 'expected': '[一-龥]{3,}'},
        {'recognition': 'OCR', 'roi': [440, 425, 560, 110], 'expected': '[一-龥]{3,}'},
    ],
    'action': 'DoNothing', 'next': ['日程关闭页面'], 'timeout': 5000,
}
path.write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
