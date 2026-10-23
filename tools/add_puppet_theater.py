"""Configure the explicitly requested watch/like/comment theater task."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
nodes = {}


def ocr(text, roi):
    return {'recognition': 'OCR', 'expected': text, 'roi': roi}


def node(name, recognition, action='DoNothing', next_nodes=None, **kwargs):
    nodes[name] = {**recognition, 'action': action, **kwargs}
    if next_nodes:
        nodes[name]['next'] = next_nodes


def click(name, recognition, target, next_nodes, **kwargs):
    node(name, recognition, 'Click', next_nodes, target=target,
         post_delay=kwargs.pop('post_delay', 800), **kwargs)


social = {'recognition': 'And', 'all_of': [
    ocr('观影券', [160, 185, 180, 80]),
    ocr('观看一次他人的视频|点赞一次他人的视频|评论一次他人的视频', [160, 350, 460, 230])]}
hot = ocr('热门剧场', [150, 105, 220, 65])
controls = ocr('在这里留下|想说的话', [470, 610, 650, 90])
direct = {'recognition': 'DirectHit'}

node('手偶剧场', direct, next_nodes=['手偶剧场社交入口', '手偶剧场打开作品', '手偶剧场热门加载完成'], timeout=8000)
node('手偶剧场社交入口', {'recognition': 'And', 'all_of': [
    '完成启动_确认', ocr('社交', [690, 460, 160, 85])], 'box_index': 1},
    'Click', ['手偶剧场打开作品'], post_delay=1200, max_hit=1, timeout=10000)
click('手偶剧场打开作品', social, [607, 385, 35, 35], ['手偶剧场热门加载完成'],
      post_delay=2000, max_hit=1, timeout=30000)
click('手偶剧场热门加载完成', hot, [560, 200, 200, 150], ['手偶剧场显示控制栏'],
      post_delay=3500, max_hit=1, timeout=60000)
click('手偶剧场显示控制栏', direct, [590, 555, 100, 55], ['手偶剧场暂停视频'],
      post_delay=500, max_hit=1, timeout=10000)
click('手偶剧场暂停视频', controls, [40, 635, 35, 40], ['手偶剧场点赞第一次'],
      post_delay=600, max_hit=1, timeout=10000)
click('手偶剧场点赞第一次', controls, [1216, 402, 22, 22], ['手偶剧场点赞第二次'],
      post_delay=400, max_hit=1, timeout=8000)
click('手偶剧场点赞第二次', controls, [1216, 402, 22, 22], ['手偶剧场打开留言'],
      post_delay=500, max_hit=1, timeout=8000)
click('手偶剧场打开留言', controls, [550, 635, 400, 35], ['手偶剧场输入留言'],
      post_delay=800, max_hit=1, timeout=8000)
send_icon = {'recognition': 'TemplateMatch', 'template': '手偶剧场/发送纸飞机.png',
             'roi': [1170, 10, 110, 110], 'threshold': 0.8}
click('手偶剧场输入留言', send_icon, [250, 57, 2, 2], ['手偶剧场填写句号'],
      post_delay=1200, max_hit=2, timeout=10000)
node('手偶剧场填写句号', direct, 'InputText',
     ['手偶剧场检查留言'], input_text='.', pre_delay=500, post_delay=1200, max_hit=2, timeout=10000)
node('手偶剧场检查留言', send_icon, next_nodes=['手偶剧场留言仍为空', '手偶剧场留言已填写'], timeout=8000)
click('手偶剧场留言仍为空', ocr('在这里留下|想说的话', [110, 25, 900, 70]),
      [250, 57, 2, 2], ['手偶剧场按键输入句号'], post_delay=1000, max_hit=1, timeout=5000)
node('手偶剧场按键输入句号', direct, 'Shell', ['手偶剧场检查留言'],
     cmd='input text .', shell_timeout=5000, post_delay=1200, max_hit=1, timeout=8000)
node('手偶剧场留言已填写', {**ocr('在这里留下|想说的话', [110, 25, 900, 70]), 'inverse': True},
     next_nodes=['手偶剧场发送留言'], timeout=5000)
click('手偶剧场发送留言', send_icon, [1227, 55, 2, 2],
      ['手偶剧场发送后检查'], pre_delay=500, post_delay=1500, max_hit=3, timeout=10000)
node('手偶剧场发送后检查', direct,
     next_nodes=['手偶剧场留言编辑已关闭', '手偶剧场发送留言'], timeout=8000)
node('手偶剧场留言编辑已关闭', {**send_icon, 'inverse': True},
     next_nodes=['手偶剧场返回视频列表'], post_delay=500, timeout=8000)
# A hidden back arrow consumes the first click by revealing controls. The same
# bounded action then retries; the list marker always wins before another click.
click('手偶剧场返回视频列表', direct, [39, 55, 2, 2],
      ['手偶剧场返回社交', '手偶剧场结束页返回', '手偶剧场重新显示控制栏'], post_delay=1000, max_hit=5, timeout=15000)
click('手偶剧场结束页返回', {'recognition': 'And', 'all_of': [
    ocr('重播', [780, 335, 130, 90]), ocr('下一个', [880, 335, 150, 90])]},
      [39, 55, 2, 2], ['手偶剧场返回社交', '手偶剧场结束页返回'],
      post_delay=1200, max_hit=3, timeout=10000)
click('手偶剧场重新显示控制栏', direct, [590, 555, 100, 55],
      ['手偶剧场返回视频列表'], post_delay=500, max_hit=2, timeout=8000)
click('手偶剧场返回社交', hot, [70, 55, 30, 45], ['手偶剧场完成'],
      post_delay=1000, max_hit=1, timeout=15000)
click('手偶剧场完成', social, [520, 295, 45, 45],
      ['手偶剧场观影券奖励确认', '手偶剧场观影券奖励关闭', '手偶剧场退出社交'],
      post_delay=1200, max_hit=1, timeout=10000)
node('手偶剧场观影券奖励确认', {'recognition': 'And', 'all_of': [
    ocr('恭喜获得|领取成功|获得奖励', [250, 65, 800, 300]),
    ocr('^确认$|^确定$', [300, 450, 700, 220])], 'box_index': 1},
    'Click', ['手偶剧场退出社交'], post_delay=1000, max_hit=1, timeout=8000)
click('手偶剧场观影券奖励关闭', ocr('恭喜获得|领取成功|获得奖励', [250, 65, 800, 300]),
      [1100, 620, 40, 35], ['手偶剧场退出社交'], post_delay=1000, max_hit=1, timeout=8000)
click('手偶剧场退出社交', social, [70, 55, 30, 45],
      ['完成启动_确认', '手偶剧场退出社交'], post_delay=1200, max_hit=3, timeout=10000)

path = ROOT / 'assets/resource/pipeline/puppet.json'
path.write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
path = ROOT / 'assets/interface.json'
data = json.loads(path.read_text(encoding='utf-8'))
if not any(task['name'] == '手偶剧场' for task in data['task']):
    data['task'].append({'name': '手偶剧场', 'label': '手偶剧场', 'entry': '手偶剧场',
        'description': '观看热门视频、暂停、点击爱心两次，公开发送一条“。”留言，最后返回社交界面。'})
for task in data['task']:
    if task['name'] == '手偶剧场':
        task['description'] = '观看热门视频、暂停、点击爱心两次，公开发送一条英文句号“.”留言；返回社交领取观影券后返回主页。'
path.write_text(json.dumps(data, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
path = ROOT / 'TODO.md'
text = path.read_text(encoding='utf-8').replace('- [ ] 手偶剧场。\n', '')
text = '\n'.join(line for line in text.splitlines() if not line.startswith('- [ ] 手偶剧场：'))
text += '\n\n- [ ] 手偶剧场：验证热门剧场加载、暂停、两次爱心、发送“。”、领取观影券及返回主页。\n'
path.write_text(text, encoding='utf-8')
