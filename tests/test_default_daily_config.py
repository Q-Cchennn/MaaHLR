import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('default_daily_config', ROOT / 'tools/default_daily_config.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DailyDefaultsTests(unittest.TestCase):
    def setUp(self):
        self.interface = module.configure_defaults(json.loads((ROOT / 'assets/interface.json').read_text(encoding='utf-8')))

    def test_every_task_in_preset_and_instance(self):
        instance = module.make_instance(self.interface)
        self.assertEqual(instance['InstanceName'], '日常任务')
        self.assertEqual([t['name'] for t in instance['TaskItems']], [t['name'] for t in self.interface['task']])
        self.assertEqual([t['name'] for t in self.interface['preset'][0]['task']], [t['name'] for t in instance['TaskItems']])
        self.assertNotIn('AdbDevice', instance)
        exhibition = next(t for t in instance['TaskItems'] if t['name'] == '画展')
        self.assertEqual(exhibition['option'][0]['index'], 2)

    def test_sync_preserves_existing_user_configuration(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'install') as folder:
            self.assertTrue(module.seed_config(folder, self.interface))
            path = Path(folder) / 'config/instances/default.json'
            path.write_text('{"InstanceName":"用户修改"}', encoding='utf-8')
            self.assertFalse(module.seed_config(folder, self.interface))
            self.assertEqual(json.loads(path.read_text(encoding='utf-8'))['InstanceName'], '用户修改')
