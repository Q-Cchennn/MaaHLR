import json
from pathlib import Path
import unittest


class ItineraryDialogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline/itinerary.json'
        cls.nodes = json.loads(path.read_text(encoding='utf-8'))

    def test_completion_checked_before_every_dialogue_click(self):
        node = self.nodes['日程对话继续']
        self.assertEqual(node['next'], ['完成日程', '日程对话继续'])
        self.assertEqual(node['max_hit'], 40)
        self.assertEqual(node['recognition'], 'And')
        self.assertNotIn('艾因', json.dumps(node, ensure_ascii=False))

    def test_completion_click_targets_button_not_page_title(self):
        node = self.nodes['完成日程']
        button = node['all_of'][node['box_index']]
        self.assertEqual(button['expected'], '^完成$')
        self.assertGreater(button['roi'][0], 1000)
        self.assertGreater(button['roi'][1], 500)
        self.assertEqual(node['next'], ['日程关闭页面'])

    def test_summary_accepts_records_without_affection_rewards(self):
        node = self.nodes['日程今日已完成']
        self.assertEqual(node['all_of'][1]['expected'], '月')
        self.assertTrue(all(part.get('recognition') != 'ColorMatch' for part in node['all_of']))
        self.assertEqual(node['next'], ['日程关闭页面'])


if __name__ == '__main__':
    unittest.main()
