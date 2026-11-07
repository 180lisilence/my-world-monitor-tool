# android 分支 · MC 服务器监控面板 Android 端

本分支只放 **Android 移动端**的完整内容。项目介绍页见 `main` 分支或本分支根目录 `index.html`；Windows 端在 `windows` 分支。

## 文件清单

| 文件 | 作用 |
| --- | --- |
| `MC-Server-Panel-beta.apk` / `MC服务器面板-beta.apk` | 已编译安装包（同一文件的两种命名，versionName = beta） |
| `MCServerPanel/` | Android Studio 工程（Gradle 8.2 / AGP 8.2.0） |
| `MCServerPanel/app/src/main/assets/index.html` | 面板前端页面（与 Windows 端 `monitor.html` 为同一份） |
| `MCServerPanel/app/src/main/java/com/msll/mcpanel/MainActivity.java` | 全屏 WebView 壳 |
| `apk_check/` | APK 解包后的结构检查产物（Manifest / dex / resources 等） |
| `index.html` | 项目介绍页（含下载按钮与原理说明） |

## 工程参数

- `applicationId` / namespace：`com.msll.mcpanel`
- `compileSdk 34` / `targetSdk 34` / `minSdk 24` / `versionCode 1` / `versionName beta`
- 依赖：`androidx.appcompat:appcompat:1.6.1`、`com.google.android.material:material:1.11.0`、`androidx.webkit:webkit:1.10.0`
- 权限：`INTERNET`、`ACCESS_NETWORK_STATE`；`android:usesCleartextTraffic="true"` 允许访问 `http://` 局域网服务

`MainActivity` 创建一个全屏 `WebView`，开启 JavaScript、DOM Storage、文件访问与 `MIXED_CONTENT_ALWAYS_ALLOW`，然后加载 `file:///android_asset/index.html`。状态栏设为 `#6b46c1`，返回键走 WebView 回退栈。

## 构建

用 Android Studio 打开 `MCServerPanel/`，或命令行：

```bash
cd MCServerPanel
./gradlew assembleDebug
# 产物：app/build/outputs/apk/debug/app-debug.apk
```

## 使用

1. 在开服电脑上运行 `windows` 分支里的 `mc_server.py`，确认监听 `0.0.0.0:8765`，防火墙放行该端口。
2. 手机与电脑处于同一局域网，安装 APK 并打开。
3. 点面板「设置」，把 API 地址从 `http://localhost:8765/status` 改成 `http://电脑局域网IP:8765/status`（例如 `http://192.168.1.100:8765/status`），保存。
4. 即可看到在线人数、最大人数、版本、延迟与实时中文日志。本地接口 2 秒不通时，面板会自动回退到 `https://api.mcstatus.io/v2/status/java/HOST:PORT` 公共查询。

## 说明

Gradle 构建产物（`app/build/`、`.gradle/`）与 IDE 缓存（`.vs/`）未纳入版本管理；`.gitignore` 已列好规则。`app/proguard-rules.pro` 为补充的默认混淆规则占位文件，供 `build.gradle` 引用。
