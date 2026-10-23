import copy
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AccountLoginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.interface = json.loads((ROOT / 'assets/interface.json').read_text(encoding='utf-8'))
        cls.nodes = json.loads((ROOT / 'assets/resource/pipeline/account.json').read_text(encoding='utf-8'))

    def test_off_preserves_normal_startup(self):
        option = self.interface['option']['使用指定账号登录']
        self.assertEqual(option['default_case'], '关闭')
        self.assertFalse(option['cases'][0].get('pipeline_override'))
        enabled = option['cases'][1]['pipeline_override']
        self.assertNotIn('启动应用', enabled)
        for name in ('启动游戏', '启动界面检查'):
            self.assertEqual(enabled[name]['next'][0], '账号选择等待登录记录')
            self.assertIn('sub_开始游戏', enabled[name]['next'])
            self.assertIn('完成启动', enabled[name]['next'])
            self.assertIn('启动抵达签到页面', enabled[name]['next'])
        self.assertFalse(enabled['sub_登录账号']['enabled'])

    def test_input_is_nonempty_and_cannot_change_regex(self):
        item = self.interface['option']['B服登录账号昵称']['inputs'][0]
        for text in ('', '.*', 'foo|bar', 'foo(bar)', 'a.b', 'a'*33):
            self.assertIsNone(re.fullmatch(item['verify'], text))
        self.assertIsNotNone(re.fullmatch(item['verify'], '测试账号_2'))

    def test_selected_account_is_verified_before_login(self):
        overrides = self.interface['option']['B服登录账号昵称']['pipeline_override']
        node = copy.deepcopy(self.nodes['账号核对并登录'])
        node.update(overrides['账号核对并登录'])
        expected = node['all_of'][1]['expected'].replace('{账号昵称}', '测试账号')
        self.assertIsNotNone(re.search(expected, '测试账号'))
        self.assertIsNotNone(re.search(expected, '测试账号的完整昵称'))
        self.assertIsNone(re.search(expected, '另一个昵称'))
        self.assertEqual(node['all_of'][node['box_index']]['expected'], '^登录$')
        self.assertEqual(self.nodes['账号选择目标']['next'], ['账号核对并登录'])
        self.assertNotIn('on_error', self.nodes['账号选择目标'])
        self.assertLessEqual(node['all_of'][1]['roi'][0] + node['all_of'][1]['roi'][2], 745)

    def test_current_account_is_checked_before_opening_dropdown(self):
        self.assertEqual(self.nodes['账号选择等待登录记录']['next'][0], '账号核对并登录')
        self.assertEqual(self.nodes['账号核对并登录']['box_index'], 2)

    def test_popup_branch_requires_visible_login_records(self):
        node = self.nodes['账号选择等待登录记录']
        self.assertEqual(node['recognition'], 'And')
        self.assertIn('B服登录记录标识', node['all_of'])
        startup = json.loads((ROOT / 'assets/resource/pipeline/start.json').read_text(encoding='utf-8'))
        self.assertEqual(startup['启动应用']['next'], ['启动游戏'])
        self.assertEqual(startup['sub_开始游戏']['next'], ['启动界面检查'])


if __name__ == '__main__':
    unittest.main()
