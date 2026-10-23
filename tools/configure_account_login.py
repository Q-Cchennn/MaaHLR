"""Configure saved Bilibili account selection without storing credentials."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'assets/interface.json'
interface = json.loads(path.read_text(encoding='utf-8'))
startup = json.loads((root / 'assets/resource/pipeline/start.json').read_text(encoding='utf-8'))
interface['option'] = {k: v for k, v in interface['option'].items() if '?' not in k}
for task in interface['task']:
    if task['entry'] == '启动应用':
        task.setdefault('option', [])
        if '使用指定账号登录' not in task['option']:
            task['option'].append('使用指定账号登录')
interface['option']['使用指定账号登录'] = {
    'type': 'select', 'label': '使用指定账号登录（B服）',
    'description': '仅支持已添加并成功登录过的B服账号。启动时先点击屏幕开始，出现账号弹窗才核对、选择并登录；没有弹窗就继续正常启动。本功能不自动注销游戏中的账号。',
    'default_case': '关闭', 'cases': [
        {'name': '关闭'},
        {'name': '开启', 'option': ['B服登录账号昵称'], 'pipeline_override': {
            '启动游戏': {'next': ['账号选择等待登录记录'] + startup['启动游戏']['next']},
            '启动界面检查': {'next': ['账号选择等待登录记录'] + startup['启动界面检查']['next']},
            'sub_登录账号': {'enabled': False},
        }},
    ],
}
login = {'recognition': 'OCR', 'roi': [480, 365, 335, 85], 'expected': '^登录$'}
target = {'recognition': 'OCR', 'roi': [530, 270, 215, 195], 'expected': '请填写已保存账号昵称'}
selected = dict(target, roi=[530, 275, 215, 70])
interface['option']['B服登录账号昵称'] = {
    'type': 'input', 'label': '已保存账号的昵称片段',
    'description': '须为已添加且成功登录过的账号。可填昵称前三字或其他容易识别的唯一片段；如果多个昵称包含相同片段，请填写更长内容以区分。找不到或核对不符时停止。无需填写密码。',
    'inputs': [{'name': '账号昵称', 'label': '昵称前三字或唯一片段', 'default': '请填写已保存账号昵称',
                'pipeline_type': 'string', 'verify': '^[一-龥A-Za-z0-9_-]{1,32}$',
                'pattern_msg': '请填写1至32位昵称，支持汉字、字母、数字、下划线、短横线。'}],
    'pipeline_override': {
        '账号选择目标': {'all_of': ['B服登录记录标识', dict(target, expected='{账号昵称}')]},
        '账号核对并登录': {'all_of': ['B服登录记录标识', dict(selected, expected='{账号昵称}'), login]},
    },
}
nodes = {
    '账号选择等待登录记录': {'recognition': 'And', 'all_of': ['B服登录记录标识'], 'action': 'DoNothing',
                            'next': ['账号核对并登录', '账号展开登录记录', '账号选择目标'], 'timeout': 5000},
    'B服登录记录标识': {'recognition': 'OCR', 'roi': [525, 210, 255, 65], 'expected': '登录记录', 'action': 'DoNothing'},
    '账号展开登录记录': {'recognition': 'And', 'all_of': ['B服登录记录标识', login,
                         {'recognition': 'OCR', 'roi': [530, 275, 215, 70], 'expected': '[^ ]{2,}'}],
                         'box_index': 2, 'action': 'Click', 'pre_delay': 200,
                         'post_delay': 500, 'max_hit': 1, 'next': ['账号选择目标'], 'timeout': 5000},
    '账号选择目标': {'recognition': 'And', 'all_of': ['B服登录记录标识', target], 'box_index': 1,
                     'action': 'Click', 'pre_delay': 200, 'post_delay': 500, 'max_hit': 1,
                     'next': ['账号核对并登录'], 'timeout': 5000},
    '账号核对并登录': {'recognition': 'And', 'all_of': ['B服登录记录标识', selected, login], 'box_index': 2,
                       'action': 'Click', 'pre_delay': 200, 'post_delay': 1000, 'max_hit': 1,
                       'next': ['启动游戏'], 'timeout': 5000},
}
path.write_text(json.dumps(interface, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
(root / 'assets/resource/pipeline/account.json').write_text(json.dumps(nodes, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
readme = root / 'README.md'
text = readme.read_text(encoding='utf-8')
text = text.split('\n## ?????')[0]
if '## 指定账号登录（B服）' not in text:
    text += '\n## 指定账号登录（B服）\n\n在“启动游戏”的任务选项中开启“使用指定账号登录”，填写已保存账号的完整昵称。账号必须已在当前模拟器添加并成功登录过，无需输入密码。默认关闭。\n\n启用前请先手动退出至B服登录记录窗口；本次未实现从游戏主页自动注销。流程为展开记录 → 点击目标昵称 → 核对选中昵称 → 登录 → 继续启动。目标缺失、昵称不符或登录失效时停止，不改用其他账号。新功能尚待模拟器实测。\n'
readme.write_text(text, encoding='utf-8')
