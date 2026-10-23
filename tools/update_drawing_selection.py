"""Select the first drawing and skip full-level drawings before training."""
import copy
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline/drawings.json'
nodes = json.loads(path.read_text(encoding='utf-8'))
nodes['选择绘卷']['target'] = [165, 190, 90, 60]
nodes['绘卷详情页标识'] = {
    'recognition': 'And',
    'all_of': copy.deepcopy(nodes['绘卷进入能力']['all_of']),
    'action': 'DoNothing',
}
full = {
    'recognition': 'And',
    'all_of': ['绘卷详情页标识', {
        'recognition': 'OCR', 'roi': [1000, 150, 230, 150], 'expected': '等级已满',
    }],
}
nodes['绘卷等级已满'] = {
    **copy.deepcopy(full), 'action': 'Click', 'target': [1210, 335, 30, 45],
    'pre_delay': 300, 'post_delay': 800, 'max_hit': 100,
    'next': ['绘卷等级已满', '绘卷点击培养', '绘卷满级搜索结束', '绘卷进入能力'],
    'timeout': 5000,
}
nodes['绘卷满级搜索结束'] = {
    **copy.deepcopy(full), 'action': 'DoNothing', 'next': ['等级提升'], 'timeout': 5000,
}
nodes['绘卷进入能力']['next'] = ['绘卷等级已满', '绘卷点击培养', '绘卷满级搜索结束']
nodes['绘卷进入能力']['max_hit'] = 102
nodes['绘卷点击培养']['next'] = ['绘卷点击提升']
path.write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
