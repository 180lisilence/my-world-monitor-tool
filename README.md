# windows 分支 · MC 服务器监控面板 Windows 端

本分支只放 **Windows 桌面端**的完整内容。项目介绍页见 `main` 分支或本分支根目录 `index.html`；Android 端在 `android` 分支。

## 文件清单

| 文件 | 作用 |
| --- | --- |
| `MC-Server-Panel-Windows.exe` / `MC服务器监控面板.exe` | 启动器（同一文件的两种命名），用默认浏览器打开 `monitor.html` |
| `monitor.html` | 监控面板前端页面（真实运行的页面） |
| `index.html` | 项目介绍页（含下载按钮与原理说明） |
| `mc_server.py` | 本地状态服务，HTTPServer 监听 `0.0.0.0:8765` |
| `启动面板.vbs` | 一键静默启动 Python 服务 + 打开面板（相对脚本所在目录，无硬编码路径） |
| `MonitorPanel/Program.cs` | exe 启动器的 C# WinForms 源码 |
| `bg-pattern.png` | 面板背景图 |
| `test_logs.py` | 日志读取测试脚本 |

## 运行

```bash
pip install mcstatus
# 按实际开服环境修改 mc_server.py 顶部常量：
#   MC_HOST / MC_PORT / SERVICE_PORT / LOG_FILE
python mc_server.py
# 双击 MC服务器监控面板.exe，或直接运行 启动面板.vbs
```

服务接口：

- `GET http://localhost:8765/status` → 在线状态、人数、版本、延迟（5 秒缓存）
- `GET http://localhost:8765/logs` → `latest.log` 最后 80 行中译结果
- `GET http://localhost:8765/` → 服务自检页

面板里的 API 地址存在 `localStorage` 的 `mc_api_url`，默认 `http://localhost:8765/status`，可在页面「设置」中修改。防火墙需放行 8765 端口。

## 说明

根目录 `index.html` 是项目介绍页；原来的面板页面完整保留为 `monitor.html`，exe 与 VBS 都已指向它，功能不受影响。
