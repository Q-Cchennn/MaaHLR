import json
from pathlib import Path
import unittest


class HolidayTransitionTests(unittest.TestCase):
    def test_dialogs_precede_switch_retry_and_retry_is_bounded(self):
        path = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline/holiday.json'
        nodes = json.loads(path.read_text(encoding='utf-8'))
        click = nodes['假日点击计划']
        self.assertEqual(click['next'][:2], [
            '[JumpBack]假日过渡奖励确认', '[JumpBack]假日过渡奖励关闭',
        ])
        self.assertIn('假日切换计划重试', click['next'])
        self.assertEqual(click['max_hit'], 3)
        retry = nodes['假日切换计划重试']
        self.assertEqual(retry['all_of'][1]['expected'], '每日清单|每周清单')
        self.assertEqual(retry['max_hit'], 2)
        self.assertFalse(nodes['假日过渡奖励确认'].get('next'))
        self.assertFalse(nodes['假日过渡奖励关闭'].get('next'))


if __name__ == '__main__':
    unittest.main()
