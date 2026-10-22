import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ExhibitionRetryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = json.loads((ROOT / 'assets/resource/pipeline/shows.json').read_text(encoding='utf-8'))
        cls.interface = json.loads((ROOT / 'assets/interface.json').read_text(encoding='utf-8'))

    def test_percentage_states_do_not_overlap(self):
        for slot in (1, 2):
            full = self.nodes[f'画展{slot}地点1满加成']
            low = self.nodes[f'画展{slot}地点1低加成']
            for percentage in range(101):
                text = f'{percentage}%'
                self.assertEqual(bool(re.search(full['expected'], text)), percentage == 100)
                self.assertEqual(bool(re.search(low['expected'], text)), percentage < 100)
            for text in ('', '等级加成', '100', '180%', '1000%', '未知'):
                self.assertIsNone(re.search(full['expected'], text))
                self.assertIsNone(re.search(low['expected'], text))

    def test_retry_is_bounded_and_last_location_is_kept(self):
        for slot in (1, 2):
            for attempt in range(1, 5):
                full = self.nodes[f'画展{slot}地点{attempt}满加成']
                self.assertEqual(full['next'], [f'画展进行中{slot}'])
                low = self.nodes[f'画展{slot}地点{attempt}低加成']
                if attempt == 4:
                    self.assertEqual(low['next'], [f'画展进行中{slot}'])
                    self.assertNotIn(f'画展{slot}地点4取消宣传', self.nodes)
                else:
                    cancel = self.nodes[low['next'][0]]
                    self.assertEqual(cancel['all_of'][cancel['box_index']]['expected'], '取消宣传')
                    confirm = self.nodes[cancel['next'][0]]
                    self.assertEqual(confirm['all_of'][confirm['box_index']]['expected'], '取消宣传')
                    self.assertEqual(confirm['next'], [f'选择地点{slot}_地点{attempt + 1}'])

    def test_all_retries_use_user_duration(self):
        for case in self.interface['option']['画展宣传时长']['cases']:
            for slot in (1, 2):
                expected = case['pipeline_override'][f'选择画展时长{slot}']
                for attempt in (2, 3, 4):
                    self.assertEqual(case['pipeline_override'][f'选择画展时长{slot}_地点{attempt}'], expected)


if __name__ == '__main__':
    unittest.main()
