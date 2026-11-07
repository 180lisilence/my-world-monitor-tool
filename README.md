# MC 服务器监控面板 · My World Monitor Tool

双端 Minecraft 服务器实时监控：**Windows 桌面端 + Android 移动端**。

本地 Python 服务直连 MC 服务器采集状态与日志，同一个 HTML 面板在 PC 上由浏览器打开、在手机上由 WebView 加载。没有云端账号，没有第三方后台，数据留在自己的局域网里。

在线介绍页：https://180lisilence.github.io/my-world-monitor-tool/

## 分支结构

| 分支 | 内容 |
| --- | --- |
| `main` | 本文件 + 根目录 `index.html` 项目介绍页（GitHub Pages 站点根） |
| `windows` | Windows 端：exe 启动器、C# 启动器源码、`mc_server.py`、`monitor.html` 面板页、VBS 启动脚本、背景图 |
| `android` | Android 端：Android Studio 工程 `MCServerPanel/`、已编译 APK、APK 解包检查产物 |

## 下载

- Windows：`https://raw.githubusercontent.com/180lisilence/my-world-monitor-tool/windows/MC-Server-Panel-Windows.exe`
- Android：`https://raw.githubusercontent.com/180lisilence/my-world-monitor-tool/android/MC-Server-Panel-beta.apk`

两个分支里同时保留了原始中文文件名。

## 工作原理

```
MC 服务器 (Java, localhost:43906, logs/latest.log)
        ↓  mcstatus Server List Ping / 读日志 + 英译中词典
本地状态服务 mc_server.py → HTTPServer 0.0.0.0:8765
        ↓  GET /status  GET /logs   (JSON, CORS *)
面板前端 index.html / monitor.html
        ├─ Windows：默认浏览器（exe 启动器 / VBS 一键启动）
        └─ Android：WebView 加载 file:///android_asset/index.html
```

- `/status`：在线/最大人数、版本名、延迟，5 秒缓存；离线返回 `online:false`。
- `/logs`：`latest.log` 最后 80 行，按内置词典翻译成中文。
- 面板设置项 `mc_api_url` 默认 `http://localhost:8765/status`，存于 localStorage；手机端改成 `http://电脑局域网IP:8765/status` 即可远程查看。本地接口 2 秒不通时自动回退到 `api.mcstatus.io` 公共查询。

## 快速开始

Windows：
```bash
pip install mcstatus
python mc_server.py
# 双击 MC服务器监控面板.exe，或运行 启动面板.vbs 一键静默启动
```

Android：安装 APK → 面板「设置」→ API 地址填 `http://电脑IP:8765/status` → 保存。

可调常量都在 `mc_server.py` 顶部：`MC_HOST` / `MC_PORT` / `SERVICE_PORT` / `LOG_FILE` / `CACHE_TTL`。改完重启服务生效；防火墙需放行 8765 端口。

## 说明

仓库未纳入 IDE 缓存（`.vs/`）、Gradle 构建产物（`app/build/`、`.gradle/`）以及第三方 MSL 项目的本地 git 副本（`MSLGITHUB/`），这些不属于本项目源码或成品。
