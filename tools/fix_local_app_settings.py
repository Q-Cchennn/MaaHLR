"""Apply local compatibility settings after the client has been closed."""
import json
import shutil
from pathlib import Path
from update_release_metadata import apply_release_metadata

ROOT = Path(__file__).resolve().parents[1]
app = ROOT / 'install/MaaHLR-Windows'
for relative in ['config/config.json', 'config/instances/default.json']:
    path = app / relative
    backup = path.with_suffix('.before-compatibility.json.bak')
    if not backup.exists():
        shutil.copy2(path, backup)
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    data['GPUOption'] = 1
    data['AdbControlScreenCapType'] = 4
    if 'AdbDevice' in data:
        data['AdbDevice']['ScreencapMethods'] = 4
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
path = ROOT / 'assets/interface.json'
data = json.loads(path.read_text(encoding='utf-8'))
apply_release_metadata(data)
path.write_text(json.dumps(data, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
print('CPU inference enabled; ADB RawWithGzip screenshot selected; config backups saved.')
