"""Portable first-run config: task choices only, no saved device or account."""
import copy
import argparse
import json
from pathlib import Path


def configure_defaults(interface):
    for task in interface['task']:
        task['default_check'] = True
    preset = {
        'name': '日常任务', 'label': '日常任务',
        'description': '包含全部18项任务。运行前可取消不需要的任务，并设置画展时长和速写男主；升级和赠礼会消耗材料。',
        'task': [{'name': task['name'], 'enabled': True} for task in interface['task']],
    }
    interface['preset'] = [preset] + [p for p in interface.get('preset', []) if p['name'] != '日常任务']
    return interface


def make_instance(interface):
    items = []
    for task in interface['task']:
        item = {key: copy.deepcopy(task[key]) for key in ('name', 'label', 'entry', 'description') if key in task}
        item['default_check'] = True
        if task.get('option'):
            item['option'] = []
            for name in task['option']:
                definition = interface['option'][name]
                cases = definition.get('cases', [])
                index = next((i for i, case in enumerate(cases) if case['name'] == definition.get('default_case')), 0)
                item['option'].append({'name': name, 'index': index})
        items.append(item)
    return {
        'InstanceName': '日常任务',
        'CurrentControllerName': interface['controller'][0]['name'],
        'Resource': interface['resource'][0]['name'],
        'CurrentTasks': [f'{task["name"]}<|||>{task["entry"]}' for task in interface['task']],
        'TaskItems': items,
    }


def seed_config(destination, interface):
    path = Path(destination) / 'config/instances/default.json'
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(make_instance(interface), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply-local', action='store_true')
    args = parser.parse_args()
    path = Path(__file__).resolve().parents[1] / 'assets/interface.json'
    data = configure_defaults(json.loads(path.read_text(encoding='utf-8')))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
    if args.apply_local:
        instance_path = path.parents[1] / 'install/MaaHLR-Windows/config/instances/default.json'
        old = json.loads(instance_path.read_text(encoding='utf-8')) if instance_path.exists() else {}
        backup = instance_path.with_suffix('.before-daily-preset.json.bak')
        if instance_path.exists() and not backup.exists():
            backup.write_text(instance_path.read_text(encoding='utf-8'), encoding='utf-8')
        old.update(make_instance(data))
        instance_path.parent.mkdir(parents=True, exist_ok=True)
        instance_path.write_text(json.dumps(old, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
