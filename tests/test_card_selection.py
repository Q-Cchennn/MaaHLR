import json
from pathlib import Path
import unittest


class CardSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline/cards.json'
        cls.nodes = json.loads(path.read_text(encoding='utf-8'))

    def test_starts_with_first_card(self):
        target = self.nodes['选择画灵']['target']
        self.assertLess(target[0] + target[2], 300)

    def test_full_level_check_excludes_skill_section(self):
        node = self.nodes['画灵等级已满换下一张']
        region = node['all_of'][1]['roi']
        self.assertLessEqual(region[1] + region[3], 300)
        self.assertEqual(node['all_of'][1]['expected'], '等级已满')
        self.assertEqual(node['max_hit'], 100)
        self.assertGreater(node['target'][0], 1200)

    def test_selects_training_only_after_full_check(self):
        refs = self.nodes['画灵进入能力']['next']
        self.assertLess(refs.index('画灵等级已满换下一张'), refs.index('点击培养'))
        self.assertEqual(self.nodes['画灵满级搜索结束']['next'], ['等级提升'])


if __name__ == '__main__':
    unittest.main()
