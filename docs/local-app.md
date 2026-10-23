# 本地 Windows App

新发布包首次启动默认提供「日常任务」配置，加入并勾选全部18项任务，也可通过同名预设恢复任务选择。默认画展8小时、速写艾因、指定账号登录关闭。运行前按需取消升级、赠礼等任务；用户需自行连接设备，默认发布配置不包含本机设备地址或账号资料。后续资源同步保留用户已有配置。

独立客户端位于项目的 `install/MaaHLR-Windows/`，双击 `MFAAvalonia.exe` 或桌面「MaaHLR」快捷方式启动。

1. 先打开 MuMu 模拟器中的绘旅人。
2. 在 App 选择 B服资源及安卓模拟器控制器，搜索并连接设备。
3. 首次只勾选「连接检查」，确认连接正常。
4. 勾选需要的任务，在任务设置里选择速写男主、画展时长或已保存登录账号。
5. 点击开始任务。

升级和出行赠礼会消耗对应材料；速写目前支持架子鼓鼓手、天体观测两种题目，其他题目会停止。

修改项目资源后，关闭 App，在项目根目录执行：

```powershell
python tools/update_local_app.py
```

再打开 App 即可加载新资源。脚本保留 App 的 `config` 及用户任务设置。客户端和本地 OCR 模型不提交 Git。

本机兼容设置使用 CPU 推理和 ADB `RawWithGzip` 截图。GPU 自动推理曾出现异常耗时，停止中的旧任务会阻止新任务启动；遇到立即失败时先检查日志中的 `stopping, ignore new post`。本机标准截图约 0.4 秒，较 Encode 约 0.8 秒更快。

这是独立安装目录，原先的 MFAAvalonia 1.5.2 目录保留。App 的标题和任务来自 `interface.json`，程序文件名仍是 MFAAvalonia.exe。

本地 GUI 对自定义标题显示做了小范围修补：显示「Maa海螺肉」，并保留旁边原生浅色版本号。原始 `MFAAvalonia.Core.dll` 备份为同目录的 `.before-title-version.bak`，资源同步不会覆盖此修补；升级 GUI 后需重新应用 `tools/patch_gui_title.ps1`。GUI 和资源版本号未改动。
