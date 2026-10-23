"""Start at the first card and skip cards whose level is already full."""
import copy
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline/cards.json'
nodes = json.loads(path.read_text(encoding='utf-8'))
nodes['选择画灵']['target'] = [165, 190, 90, 60]
detail = {
    'recognition': 'And',
    'all_of': copy.deepcopy(nodes['画灵进入能力']['all_of']),
    'action': 'DoNothing',
}
nodes['画灵详情页标识'] = detail
full = {
    'recognition': 'And',
    'all_of': ['画灵详情页标识', {
        'recognition': 'OCR', 'roi': [1000, 150, 230, 150], 'expected': '等级已满',
    }],
}
nodes['画灵等级已满换下一张'] = {
    **copy.deepcopy(full), 'action': 'Click', 'target': [1210, 335, 30, 45],
    'pre_delay': 300, 'post_delay': 800, 'max_hit': 100,
    'next': ['画灵等级已满换下一张', '点击培养', '画灵满级搜索结束', '画灵进入能力'],
    'timeout': 5000,
}
nodes['画灵满级搜索结束'] = {
    **copy.deepcopy(full), 'action': 'DoNothing', 'next': ['等级提升'], 'timeout': 5000,
}
nodes['画灵进入能力']['next'] = ['画灵等级已满换下一张', '点击培养', '画灵满级搜索结束']
nodes['画灵进入能力']['max_hit'] = 102
path.write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
