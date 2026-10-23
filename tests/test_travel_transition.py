import json
from pathlib import Path
import unittest


class TravelTransitionTests(unittest.TestCase):
    def test_rewards_are_handled_before_more_clicks_and_return_is_bounded(self):
        path = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline/travel.json'
        nodes = json.loads(path.read_text(encoding='utf-8'))
        for name in ('出行点击人物互动', '出行返回主页'):
            self.assertEqual(nodes[name]['next'][:2], [
                '[JumpBack]出行奖励点击确认', '[JumpBack]出行奖励点击空白',
            ])
        self.assertEqual(nodes['出行返回主页']['max_hit'], 3)
        self.assertIn('出行返回主页', nodes['出行返回主页']['next'])

    def test_intro_is_optional_and_rechecks_character_screen(self):
        path = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline/travel.json'
        nodes = json.loads(path.read_text(encoding='utf-8'))
        for name in ('出行', '进入出行', '出行选择'):
            self.assertIn('出行门口有人过渡页', nodes[name]['next'])
            self.assertIn('人物选择', nodes[name]['next'])
        node = nodes['出行门口有人过渡页']
        self.assertEqual(node['recognition'], 'And')
        self.assertIn('有人找你', node['all_of'][1]['expected'])
        self.assertEqual(node['max_hit'], 2)
        self.assertIn('确定人物', node['next'])
        self.assertIn('人物选择', node['next'])


if __name__ == '__main__':
    unittest.main()
