import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ocr(text, roi):
    return {'recognition': 'OCR', 'expected': text, 'roi': roi}


campus = ocr('校园', [110, 10, 180, 80])
selecting = ocr('退出速写', [1090, 640, 190, 80])
nodes = {
    '速写': {'recognition': 'DirectHit', 'action': 'DoNothing',
           'next': ['速写架子鼓题目', '速写一键收集', '速写选择男主', '速写点击入口', '速写进入校园'], 'timeout': 10000},
    '速写进入校园': {'recognition': 'And', 'all_of': ['完成启动_确认'],
        'action': 'Click', 'target': [47, 275, 2, 2],
        'pre_delay': 400, 'post_delay': 1200, 'max_hit': 2,
        'next': ['速写点击入口', '速写进入校园'], 'timeout': 10000},
    '速写点击入口': {'recognition': 'And', 'all_of': [campus,
        ocr('速写', [800, 600, 150, 120])], 'box_index': 1,
        'action': 'Click', 'post_delay': 1000, 'max_hit': 1,
        'next': ['速写一键收集', '速写选择男主'], 'timeout': 10000},
    '速写选择男主': {'recognition': 'And', 'all_of': [campus, selecting,
        {'recognition': 'TemplateMatch', 'template': '速写/艾因.png',
         'roi': [0, 85, 1280, 545], 'threshold': 0.85}], 'box_index': 2,
        'action': 'Click',
        'pre_delay': 400, 'post_delay': 1500, 'max_hit': 1,
        'next': ['速写一键收集'], 'timeout': 15000},
    '速写一键收集': {**ocr('一?键收集', [1010, 40, 250, 130]),
        'action': 'Click', 'pre_delay': 500, 'post_delay': 1200,
        'max_hit': 1, 'timeout': 20000, 'next': ['速写架子鼓题目']},
    '速写架子鼓题目': {**ocr('架子鼓鼓手', [0, 20, 700, 90]),
        'action': 'DoNothing', 'next': ['速写清除旧连线', '速写灵感音符'], 'timeout': 10000},
    '速写清除旧连线': {**ocr('重.*画', [260, 620, 300, 90]),
        'action': 'Click', 'post_delay': 600, 'max_hit': 1,
        'next': ['速写灵感音符'], 'timeout': 5000},
}
for icon in ['音符', '鼓', '手臂', '星星', '土星', '放大镜']:
    nodes[f'速写灵感{icon}'] = {'recognition': 'TemplateMatch',
        'template': f'速写/灵感/{icon}.png', 'roi': [100, 130, 1100, 480],
        'threshold': 0.8, 'action': 'DoNothing', 'timeout': 5000}
nodes['速写灵感音符']['next'] = ['速写灵感鼓']
nodes['速写灵感鼓']['next'] = ['速写灵感手臂']
nodes['速写灵感手臂']['next'] = ['速写架子鼓连线']
nodes['速写架子鼓连线'] = {**ocr('架子鼓鼓手', [0, 20, 700, 90]),
    'action': 'Swipe', 'begin': '速写灵感音符',
    'end': ['速写灵感鼓', '速写灵感手臂'], 'duration': [700, 700],
    'end_hold': 200, 'post_delay': 800, 'max_hit': 1,
    'next': ['速写架子鼓确认'], 'timeout': 5000}
nodes['速写架子鼓确认'] = {'recognition': 'And', 'all_of': [
    ocr('架子鼓鼓手', [0, 20, 700, 90]), ocr('确.*定', [730, 620, 300, 90])],
    'box_index': 1, 'action': 'Click', 'post_delay': 1500, 'max_hit': 1,
    'next': ['速写结果退出'], 'timeout': 30000}
nodes['速写']['next'].insert(0, '速写天体观测题目')
nodes['速写一键收集']['next'].append('速写天体观测题目')
nodes['速写天体观测题目'] = {**ocr('天体观测', [0, 20, 700, 90]),
    'action': 'DoNothing', 'next': ['速写天体观测重画', '速写灵感星星'], 'timeout': 10000}
nodes['速写天体观测重画'] = {**ocr('重.*画', [260, 620, 300, 90]),
    'action': 'Click', 'post_delay': 600, 'max_hit': 1,
    'next': ['速写灵感星星'], 'timeout': 5000}
nodes['速写灵感星星']['next'] = ['速写灵感土星']
nodes['速写灵感土星']['next'] = ['速写灵感放大镜']
nodes['速写灵感放大镜']['next'] = ['速写天体观测连线']
nodes['速写天体观测连线'] = {**ocr('天体观测', [0, 20, 700, 90]),
    'action': 'Swipe', 'begin': '速写灵感星星',
    'end': ['速写灵感土星', '速写灵感放大镜'], 'duration': [700, 700],
    'end_hold': 200, 'post_delay': 800, 'max_hit': 1,
    'next': ['速写天体观测确认'], 'timeout': 5000}
nodes['速写天体观测确认'] = {'recognition': 'And', 'all_of': [
    ocr('天体观测', [0, 20, 700, 90]), ocr('确.*定', [730, 620, 300, 90])],
    'box_index': 1, 'action': 'Click', 'post_delay': 1500, 'max_hit': 1,
    'next': ['速写结果退出'], 'timeout': 30000}
nodes['速写结果退出'] = {'recognition': 'And', 'all_of': [
    ocr('速写结果', [420, 120, 450, 120]),
    ocr('点击屏幕退出', [420, 590, 450, 100])],
    'action': 'Click', 'target': [630, 635, 2, 2], 'pre_delay': 600,
    'post_delay': 1200, 'max_hit': 2,
    'next': ['速写赠送选择第一位', '完成启动_确认', '速写结果退出', '速写校园返回主页', '速写离开场景'], 'timeout': 15000}
nodes['速写赠送选择第一位'] = {**ocr('速写赠送', [420, 120, 450, 120]),
    'action': 'Click', 'target': [430, 290, 2, 2], 'pre_delay': 400,
    'post_delay': 600, 'max_hit': 1, 'next': ['速写点击赠送'], 'timeout': 10000}
nodes['速写点击赠送'] = {'recognition': 'And', 'all_of': [
    ocr('速写赠送', [420, 120, 450, 120]), ocr('赠.*送', [520, 480, 230, 100])],
    'box_index': 1, 'action': 'Click', 'target': [640, 520, 2, 2],
    'pre_delay': 400, 'post_delay': 1500, 'max_hit': 1,
    'next': ['完成启动_确认', '速写校园返回主页', '速写赠送后离开场景', '速写离开场景'], 'timeout': 15000}
nodes['速写赠送后离开场景'] = {**ocr('速写', [1120, 600, 160, 120]),
    'action': 'Click', 'target': [63, 45, 2, 2], 'pre_delay': 500,
    'post_delay': 1200, 'max_hit': 3,
    'next': ['完成启动_确认', '速写校园返回主页', '速写赠送后离开场景'], 'timeout': 10000}
nodes['速写离开场景'] = {**ocr('一?键收集', [1010, 40, 250, 130]),
    'action': 'Click', 'target': [63, 55, 2, 2], 'post_delay': 1200,
    'max_hit': 2, 'next': ['完成启动_确认', '速写校园返回主页', '速写离开场景'],
    'timeout': 10000}
nodes['速写校园返回主页'] = {**campus, 'action': 'Click',
    'target': [63, 55, 2, 2], 'post_delay': 1200, 'max_hit': 2,
    'next': ['完成启动_确认', '速写校园返回主页'], 'timeout': 10000}
names = ['艾因', '路辰', '罗夏', '司岚', '叶瑄']
path = ROOT / 'assets/resource/pipeline/sketch.json'
path.write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
path = ROOT / 'assets/interface.json'
data = json.loads(path.read_text(encoding='utf-8'))
if not any(task['name'] == '速写' for task in data['task']):
    data['task'].append({'name': '速写', 'label': '速写 · 选择男主地点（开发中）',
        'entry': '速写', 'option': ['速写男主'],
        'description': '进入校园速写并选择男主头像。目前接入到地点选择，后续流程待补充。'})
for task in data['task']:
    if task['name'] == '速写':
        task['label'] = '速写'
        task['description'] = '按所选男主头像进入速写并收集灵感。目前支持架子鼓鼓手、天体观测连线题，关闭结果后选择第一位赠送，再返回主页；未知题目停止。'
data['option']['速写男主'] = {'type': 'select', 'label': '速写男主', 'default_case': '艾因',
    'description': '在校园地图中识别所选男主头像并点击，支持头像随机出现在不同地点。识别不到时停止。',
    'cases': [{'name': name, 'pipeline_override': {'速写选择男主': {'all_of': [campus, selecting,
        {'recognition': 'TemplateMatch', 'template': f'速写/{name}.png',
         'roi': [0, 85, 1280, 545], 'threshold': 0.85}]}}}
              for name in names]}
path.write_text(json.dumps(data, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
