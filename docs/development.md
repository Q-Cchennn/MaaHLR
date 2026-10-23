# 开发说明

资源遵循 ProjectInterface v2，入口为 `assets/interface.json`。界面短边按720处理，16:9画面的识别和点击坐标为1280×720；不要直接使用1600×900原图坐标。

## 调试与检查

使用 MaaFramework VS Code 扩展或 MaaDebugger 加载资源入口，选择实际 ADB 设备。实例名不是 ADB 地址。

```powershell
python tools/validate_project.py
python -m unittest discover -s tests
python tools/update_local_app.py
```

静态校验需要 `jsonschema`；只能检查协议和引用，不能代替游戏内实测。OCR模型、本地运行库、配置和日志不提交到Git。

截图工具为 `tools/capture.py`，通过 `--adb` 指定自己的 ADB 路径，`--serial` 指定设备，截图保存在本地忽略的 `screenshots/`。

## 资源与打包

- `tools/task_descriptions.py` 维护任务说明及emoji显示名。
- `tools/default_daily_config.py` 维护「日常任务」预设和不含个人设备信息的首次启动配置。
- `tools/update_release_metadata.py` 从本版公告更新版本和欢迎消息。
- `tools/update_local_app.py` 同步到本地独立App，保留用户已有配置。
- `tools/install.py` 是CI资源安装脚本；发布前还需检查GUI、运行库、OCR模型和最终压缩包。
- `tools/build_windows_release.py` 从官方GUI原始压缩包及项目资源构建干净的Windows发行包，生成SHA-256校验文件；`tools/verify_windows_release.py` 检查压缩包完整性、资源引用、默认配置及本机数据排除情况。
- 本机GUI保留小字版本号的标题显示修补见 `tools/patch_gui_title.ps1`，升级GUI后需重新验证；它不改变GUI本身的版本号。

## 迁移来源

项目从旧MFAAvalonia资源迁移，模板基线为 MaaPracticeBoilerplate 的 `3c61ba2172f0415e9562783e8362fead04f82c5b`。旧资源归档在 `docs/legacy/`，不加载执行。

迁移包括 `is_sub` / `interrupt` 到 `[JumpBack]` 的转换、OCR文本字段和超时字段整理，以及页面分支和奖励弹窗处理。迁移工具为 `tools/migrate_pipeline_v5.py`。
