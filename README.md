# MaaHLR · 绘旅人助手

基于 MaaFramework 的《时空中的绘旅人》B服日常助手。模拟器实例名 MaaHLR，原始分辨率 1600×900；资源按短边 720 处理，使用 1280×720 的识别和点击坐标。

**当前为旧资源迁移开发版，未在真实模拟器验证。** 已接入启动、签到、好友体力、免费礼包、日程、画展、画灵及绘卷升级、出行赠礼。请逐项运行并核对结果，不应直接视为一键日常可用版。升级会消耗材料，赠礼会消耗礼物。

## 调试

安装 MaaFramework VS Code 扩展或 MaaDebugger，加载 `assets/interface.json`，选择实际的 ADB 设备。实例名并不是 ADB 地址。先运行连接检查，再从单项任务开始验证。当前工程没有捆绑新版 GUI 或运行库。

B服启动目标继承旧工程的 `com.netease.skzdhlr.bilibili/com.netease.game.MessiahNativeActivity`。需要确认当前安装版本仍使用该入口。

```powershell
& 'C:\Users\qzc03\Maa\platform-tools\adb.exe' devices
python tools/capture.py --adb 'C:\Users\qzc03\Maa\platform-tools\adb.exe' --serial 设备地址 --name home
```

截图保存到本地 `screenshots/`，不提交版本控制。框架已按短边 720 缩放，请勿将 1600×900 原图坐标直接填入现有流水线。

## 迁移范围

以旧运行目录 `C:/Users/qzc03/Maa/MFAAvalonia-v1.5.2-win-x64` 为资源来源，保留原目录。新的模板基线为 MaaPracticeBoilerplate 的 `3c61ba2172f0415e9562783e8362fead04f82c5b`。

- 更新 ProjectInterface v2，配置安卓控制器和 B服资源。
- 使用官方迁移逻辑将旧 `is_sub`、`interrupt` 转成 `[JumpBack]`。
- 修正 OCR 的文本字段及 replace 格式，迁移超时字段；将 post_check 拆为显式确认节点，移除静默忽略错误。
- 补齐签到页面间缺失的 next 连线；实际领取与已签状态仍需实测。
- 社交发评论流程、免费十连和未完成的任务奖励保存在 `docs/legacy/`，不加载执行。原“免费十连”只识别“绘制十次”，不能证明免费，暂不开放。

已复制原有图像和 OCR 模型；模型为本地忽略文件。未复制旧 GUI、运行库、个人配置、账号数据和调试日志。打包工具和 GitHub Actions 沿用模板，发布前需准备并验证当前运行库、OCR 模型和 UI 的版本组合。

验证方法见 `tools/validate_project.py`；需要 `jsonschema`。静态协议校验不代表画面识别、循环终止或任务结果已经实测。原流程的页面判断、超时路径、部分硬编码人物和地点仍需逐项复核。

## 上游

- https://github.com/MaaXYZ/MaaFramework
- https://github.com/MaaXYZ/MaaPracticeBoilerplate
- 官方迁移脚本：`tools/migrate_pipeline_v5.py`

保留上游 MIT 许可证；本项目为非官方开发项目。

## 画展时长

在画展任务选项中设置“画展宣传时长”：2小时、4小时或8小时，默认8小时。仅影响新申请的展览；进行中的展览不取消、不加速。新申请流程为地点图标（默认律政楼）→ 选择时长 → 快速选择 → 申请 → 确认倒计时。尚需逐项实测。
