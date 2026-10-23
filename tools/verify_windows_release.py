"""Check the distributable ZIP without modifying its contents."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def verify(path):
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f'Corrupt ZIP entry: {bad}')
        names = archive.namelist()
        prefixes = {name.split('/')[0] for name in names}
        assert len(prefixes) == 1, 'Expected a single app folder'
        prefix = prefixes.pop() + '/'

        def read_json(relative):
            return json.loads(archive.read(prefix + relative).decode('utf-8-sig'))

        interface = read_json('interface.json')
        instance = read_json('config/instances/default.json')
        settings = read_json('appsettings.json')
        manifest = read_json('MaaHLR-release.json')
        assert interface['version'] == manifest['version'] == '2.0.0-beta.1'
        assert instance['InstanceName'] == '日常任务'
        assert len(instance['TaskItems']) == len(interface['task']) == 18
        assert all(item['default_check'] for item in instance['TaskItems'])
        assert settings['NoAutoStart'] == 'True'
        assert 'AdbDevice' not in instance
        expected_config = {prefix + relative for relative in (
            'config/config.json', 'config/instances/default.json')}
        assert {name for name in names if name.startswith(prefix + 'config/')} == expected_config
        assert hashlib.sha256(archive.read(prefix + 'libs/MFAAvalonia.Core.dll')).hexdigest() == manifest['core_sha256']
        assert archive.read(prefix + 'logo.ico')[:4] == b'\x00\x00\x01\x00'
        assert archive.read(prefix + 'logo.png')[:8] == b'\x89PNG\r\n\x1a\n'
        pipeline = {}
        for name in names:
            if name.startswith(prefix + 'resource/pipeline/') and name.endswith('.json'):
                pipeline.update(json.loads(archive.read(name).decode('utf-8-sig')))
        assert all(task['entry'] in pipeline for task in interface['task'])

        def templates(value):
            if isinstance(value, dict):
                if value.get('recognition') == 'TemplateMatch':
                    items = value.get('template', [])
                    for item in ([items] if isinstance(items, str) else items):
                        assert prefix + 'resource/image/' + item in names, f'Missing template: {item}'
                for child in value.values():
                    templates(child)
            elif isinstance(value, list):
                for child in value:
                    templates(child)

        templates(pipeline)
        templates(interface)
        for name in names:
            relative = Path(name.removeprefix(prefix))
            assert not {'logs', 'debug', 'screenshots', 'backup', 'temp', '__pycache__'}.intersection(relative.parts)
            assert not name.endswith(('.lnk', '.bak', '.log'))
    with path.open('rb') as stream:
        sha256 = hashlib.file_digest(stream, 'sha256').hexdigest()
    assert path.with_suffix('.zip.sha256').read_text(encoding='ascii').split()[0] == sha256
    return {'archive': path.name, 'bytes': path.stat().st_size, 'sha256': sha256,
            'zip_crc': 'passed', 'task_count': 18, 'pipeline_nodes': len(pipeline),
            'resource_dependencies': 'passed', 'default_configuration': '日常任务',
            'personal_configuration': 'absent', 'auto_run_tasks': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    args = parser.parse_args()
    report = verify(args.archive)
    args.archive.with_suffix('.validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
