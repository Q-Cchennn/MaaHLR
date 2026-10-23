import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1] / 'assets/resource/pipeline'


class CheckinFlowTests(unittest.TestCase):
    def test_startup_accepts_calendar_without_claiming(self):
        startup = json.loads((ROOT / 'start.json').read_text(encoding='utf-8'))
        for name in ('启动游戏', '启动界面检查', '完成启动'):
            self.assertIn('启动抵达签到页面', startup[name]['next'])
        finished = startup['启动抵达签到页面']
        self.assertEqual(finished['action'], 'DoNothing')
        self.assertFalse(finished.get('next'))

    def test_each_day_handles_both_popup_and_direct_claim(self):
        days = json.loads((ROOT / 'checkin_days.json').read_text(encoding='utf-8'))
        for day in range(1, 32):
            node = days[f'签到{day:02d}日可领取']
            self.assertEqual(node['next'], ['检测弹窗', '确认领取成功-签到', '签到今日已领取'])
            self.assertEqual(node['max_hit'], 1)

    def test_month_card_prompt_clicks_free_claim(self):
        checkin = json.loads((ROOT / 'checkin.json').read_text(encoding='utf-8'))
        node = checkin['检测弹窗']
        self.assertEqual(node['all_of'][node['box_index']]['expected'], '直接领取')
        self.assertNotIn('订购月卡', json.dumps(node, ensure_ascii=False))

    def test_close_calendar_clicks_back_and_retries_only_on_calendar(self):
        checkin = json.loads((ROOT / 'checkin.json').read_text(encoding='utf-8'))
        node = checkin['签到关闭页面']
        self.assertIn('签到页面标识', node['all_of'])
        self.assertEqual(node['target'], [45, 25, 35, 35])
        self.assertEqual(node['next'], ['签到返回主页确认', '签到关闭页面'])
        self.assertEqual(node['max_hit'], 3)


if __name__ == '__main__':
    unittest.main()
