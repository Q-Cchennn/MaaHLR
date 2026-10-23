"""Build a clean portable Windows bundle without copying local user settings."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

from default_daily_config import configure_defaults, seed_config
from task_descriptions import apply_descriptions
from update_release_metadata import apply_release_metadata, VERSION

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    name = f'MaaHLR-win-x86_64-v{VERSION}'
    stage = output / name
    archive = output / f'{name}.zip'
    if stage.exists() or archive.exists():
        raise RuntimeError('Output already exists; choose a fresh --output directory.')
    gui_zip = ROOT / 'install/downloads/MFAAvalonia-v2.16.2-win-x64.zip'
    patched_core = ROOT / 'install/MaaHLR-Windows/libs/MFAAvalonia.Core.dll'
    if not patched_core.with_suffix('.dll.before-title-version.bak').exists():
        raise RuntimeError('The verified title/version GUI patch must be applied before packaging.')
    stage.mkdir()
    with zipfile.ZipFile(gui_zip) as source:
        for member in source.infolist():
            if not (stage / member.filename).resolve().is_relative_to(stage.resolve()):
                raise RuntimeError('Unsafe archive path')
        source.extractall(stage)
    # Only the known display-patched GUI assembly comes from the local app.
    shutil.copy2(patched_core, stage / 'libs/MFAAvalonia.Core.dll')
    shutil.copytree(ROOT / 'assets/resource', stage / 'resource',
                    ignore=shutil.ignore_patterns('*.lnk', '*.log', '*.bak', '__pycache__'))
    interface = json.loads((ROOT / 'assets/interface.json').read_text(encoding='utf-8'))
    apply_descriptions(interface)
    configure_defaults(interface)
    apply_release_metadata(interface)
    interface['custom_title'] = interface['label']
    (stage / 'interface.json').write_text(json.dumps(interface, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
    seed_config(stage, interface)
    (stage / 'config/config.json').write_text(json.dumps({
        'CurrentLanguage': 'zh-CN', 'GPUOption': 1, 'AdbControlScreenCapType': 4,
    }, indent=2) + '\n', encoding='utf-8')
    (stage / 'appsettings.json').write_text(json.dumps({
        'Instances.List': 'default', 'Instances.Order': 'default',
        'Instances.LastActive': 'default', 'Instances.LastActiveName': '日常任务',
        'NoAutoStart': 'True',
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for source, target in [
        ('assets/logo.ico', 'logo.ico'), ('assets/logo-conch-transparent.png', 'logo.png'),
        ('assets/announcement.md', 'announcement.md'), ('README.md', 'README.md'),
        ('LICENSE', 'LICENSE'), ('TODO.md', 'TODO.md'),
        ('assets/logo-conch-transparent.png', 'assets/logo-conch-transparent.png'),
        ('assets/announcement.md', 'assets/announcement.md'),
        ('docs/local-app.md', 'docs/local-app.md'), ('docs/development.md', 'docs/development.md'),
    ]:
        destination = stage / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / source, destination)
    (stage / 'Maa海螺肉.cmd').write_text('@echo off\ncd /d "%~dp0"\nstart "" "MFAAvalonia.exe"\n', encoding='ascii')
    (stage / '开始使用.txt').write_text(
        f'Maa海螺肉 v{VERSION}\n\n'
        '1. 完整解压，双击 Maa海螺肉.cmd 或 MFAAvalonia.exe。\n'
        '2. 打开MuMu模拟器和绘旅人B服，使用1600×900横屏。\n'
        '3. 选择自己的设备并连接，先只勾选连接检查。\n'
        '4. 默认日常任务包含18项任务，运行前按需取消不需要的项目。\n'
        '5. 升级及赠礼会消耗材料；手偶剧场会公开发送英文句号留言。\n'
        '6. 速写仅支持架子鼓鼓手、天体观测题。\n\n'
        '需要.NET 10运行环境；不能启动时可运行随附的依赖安装脚本。\n'
        '此包不包含个人账号、设备记录和运行日志，不会首次启动自动执行日常。\n', encoding='utf-8-sig')
    manifest = {
        'version': VERSION, 'platform': 'win-x86_64', 'gui': 'MFAAvalonia v2.16.2',
        'gui_source': 'https://github.com/MaaXYZ/MFAAvalonia/releases/tag/v2.16.2',
        'gui_archive_sha256': digest(gui_zip),
        'gui_customization': 'Custom heading keeps native small resource version; conch icon.',
        'core_sha256': digest(patched_core), 'tasks': len(interface['task']),
        'default_configuration': '日常任务',
    }
    (stage / 'MaaHLR-release.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    required = ['MFAAvalonia.exe', 'logo.ico', 'resource/model/ocr/det.onnx',
                'resource/model/ocr/rec.onnx', 'resource/model/ocr/keys.txt',
                'runtimes/win-x64/native/MaaFramework.dll']
    for relative in required:
        if not (stage / relative).is_file():
            raise RuntimeError(f'Missing runtime dependency: {relative}')
    forbidden = {'debug', 'logs', 'backup', 'temp', 'screenshots', '__pycache__'}
    for file in stage.rglob('*'):
        relative = file.relative_to(stage)
        if forbidden.intersection(relative.parts) or file.name.endswith(('.bak', '.log', '.lnk')):
            raise RuntimeError(f'Unexpected local data: {relative}')
    for relative in ['config/config.json', 'config/instances/default.json', 'appsettings.json', 'interface.json']:
        text = (stage / relative).read_text(encoding='utf-8')
        if any(needle in text for needle in ['qzc03', '127.0.0.1:16384', 'AdbDevice', 'AdbSerial', 'AnnouncementInfo.WelcomeSnapshot']):
            raise RuntimeError(f'Unexpected personal configuration: {relative}')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as result:
        for file in sorted(stage.rglob('*')):
            if file.is_file():
                result.write(file, (Path(name) / file.relative_to(stage)).as_posix())
    checksum = digest(archive)
    archive.with_suffix('.zip.sha256').write_text(f'{checksum}  {archive.name}\n', encoding='ascii')
    print(json.dumps({'archive': str(archive), 'bytes': archive.stat().st_size,
                      'sha256': checksum, 'tasks': len(interface['task'])}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'install/releases')
    build(parser.parse_args().output.resolve())
