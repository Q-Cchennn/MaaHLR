import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
nodes = {}


def ocr(text, roi):
    return {'recognition': 'OCR', 'expected': text, 'roi': roi}


title = ocr('画廊', [110, 10, 180, 85])
pool = ocr('每日.*素材箱|每日免费抽取十次', [220, 500, 600, 145])
free = ocr('本次免费', [1010, 610, 250, 60])
nodes['画廊免费十连'] = {'recognition': 'DirectHit', 'action': 'DoNothing',
    'next': ['免费十连卡池检查', '免费十连进入画廊'], 'timeout': 8000}
nodes['免费十连进入画廊'] = {'recognition': 'And', 'all_of': ['完成启动_确认',
    ocr('画廊', [170, 390, 180, 90])], 'box_index': 1, 'action': 'Click',
    'post_delay': 1600, 'max_hit': 1, 'next': ['免费十连卡池检查'], 'timeout': 10000}
nodes['免费十连卡池检查'] = {'recognition': 'And', 'all_of': [title],
    'action': 'DoNothing', 'next': ['免费十连目标卡池', '免费十连切换左侧卡池'], 'timeout': 8000}
nodes['免费十连切换左侧卡池'] = {'recognition': 'And', 'all_of': [title],
    'action': 'Click', 'target': [35, 330, 50, 65], 'post_delay': 1200,
    'max_hit': 6, 'next': ['免费十连目标卡池', '免费十连切换左侧卡池'], 'timeout': 8000}
nodes['免费十连目标卡池'] = {'recognition': 'And', 'all_of': [title, pool],
    'action': 'DoNothing', 'post_delay': 700,
    'next': ['免费十连点击免费绘制', '免费十连没有免费次数'], 'timeout': 6000}
nodes['免费十连点击免费绘制'] = {'recognition': 'And', 'all_of': [title, pool, free,
    ocr('绘制十次|绘制10次', [1010, 565, 250, 75])], 'box_index': 3,
    'action': 'Click', 'pre_delay': 400, 'post_delay': 5000, 'max_hit': 1,
    'next': ['免费十连结果确认', '免费十连等待结果'], 'timeout': 20000}
nodes['免费十连没有免费次数'] = {**free, 'inverse': True, 'action': 'DoNothing',
    'post_delay': 700, 'next': ['免费十连免费复核'], 'timeout': 4000}
nodes['免费十连免费复核'] = {'recognition': 'And', 'all_of': [title, pool],
    'action': 'DoNothing', 'next': ['免费十连点击免费绘制', '免费十连返回主页'], 'timeout': 5000}
nodes['免费十连结果确认'] = {**ocr('^确认$|^确定$', [200, 480, 1000, 230]),
    'action': 'Click', 'post_delay': 1300, 'max_hit': 1,
    'next': ['免费十连返回主页'], 'timeout': 20000}
nodes['免费十连等待结果'] = {'recognition': 'DirectHit', 'action': 'Click',
    'target': [600, 300, 80, 80], 'post_delay': 2000, 'max_hit': 8,
    'next': ['免费十连结果确认', '免费十连等待结果'], 'timeout': 20000}
nodes['免费十连返回主页'] = {'recognition': 'And', 'all_of': [title],
    'action': 'Click', 'target': [40, 25, 40, 35], 'pre_delay': 400,
    'post_delay': 1000, 'max_hit': 3,
    'next': ['完成启动_确认', '免费十连返回主页'], 'timeout': 8000}

path = ROOT / 'assets/resource/pipeline/gallery.json'
path.write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
path = ROOT / 'assets/interface.json'
interface = json.loads(path.read_text(encoding='utf-8'))
if not any(task['name'] == '画廊免费十连' for task in interface['task']):
    interface['task'].append({'name': '画廊免费十连', 'label': '画廊免费十连',
        'entry': '画廊免费十连', 'description': '仅在每日素材箱显示“本次免费”时绘制十次；没有免费次数则返回主页。'})
interface['welcome'] = interface['welcome'].replace('原社交评论、免费十连和未完成奖励任务尚未接入。', '原社交评论和未完成奖励任务尚未接入。')
path.write_text(json.dumps(interface, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
path = ROOT / 'TODO.md'
todo = path.read_text(encoding='utf-8').replace('- [ ] 画廊免费十连：确认次数免费后再执行，避免消耗钻石或绘制道具。\n', '')
todo += '\n- [ ] 画廊免费十连：验证切换每日素材箱、本次免费判断、结果确认及返回主页；没有免费次数时直接返回。\n'
path.write_text(todo, encoding='utf-8')
