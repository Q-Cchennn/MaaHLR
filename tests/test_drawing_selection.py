import json
from pathlib import Path
import unittest


class DrawingSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline/drawings.json'
        cls.nodes = json.loads(path.read_text(encoding='utf-8'))

    def test_first_drawing_and_bounded_full_level_skip(self):
        self.assertLess(sum(self.nodes['选择绘卷']['target'][::2]), 300)
        node = self.nodes['绘卷等级已满']
        region = node['all_of'][1]['roi']
        self.assertLessEqual(region[1] + region[3], 300)
        self.assertEqual(node['max_hit'], 100)
        self.assertGreater(node['target'][0], 1200)
        self.assertEqual(self.nodes['绘卷满级搜索结束']['next'], ['等级提升'])

    def test_does_not_switch_cards_from_open_training_panel(self):
        self.assertEqual(self.nodes['绘卷点击培养']['next'], ['绘卷点击提升'])
        self.assertEqual(self.nodes['绘卷点击提升']['next'], ['等级提升'])


if __name__ == '__main__':
    unittest.main()
