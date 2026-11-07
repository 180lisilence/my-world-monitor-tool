"""
MC服务器本地状态服务
运行后，HTML面板会从 http://localhost:8765 读取真实服务器数据
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from mcstatus import JavaServer
import json
import time

MC_HOST = "localhost"
MC_PORT = 43906
SERVICE_PORT = 8765
LOG_FILE = r"E:\MSL\MSL\Server1\logs\latest.log"

# MC日志常用词翻译词典
TRANSLATIONS = {
    "joined the game": "加入了游戏",
    "left the game": "离开了游戏",
    "lost connection": "连接断开",
    "Disconnected": "断开连接",
    "Starting minecraft server": "正在启动MC服务器",
    "Done (": "启动完成，耗时 ",
    "Stopping server": "正在关闭服务器",
    "Saving players": "正在保存玩家数据",
    "Saving worlds": "正在保存世界",
    "Preparing spawn area": "正在生成出生点区域",
    "Preparing start region": "正在准备启动区域",
    "Loaded": "已加载",
    "recipes": "合成配方",
    "advancements": "成就",
    "recipes loaded": "个合成配方已加载",
    "Caught exception": "捕获到异常",
    "Exception": "异常",
    "Error": "错误",
    "WARN": "警告",
    "INFO": "信息",
    "Can't keep up": "服务器卡顿，tick跟不上",
    "memory": "内存",
    "out of memory": "内存不足",
    "There are": "当前",
    "of a max of": "人在线 / 最大",
    "players": "人",
    "UUID": "唯一ID",
    "game profile": "游戏档案",
    "authentication": "身份验证",
    "logged in": "已登录",
    "Server thread": "服务器主线程",
    "Network": "网络",
    "Connection": "连接",
    "accepted": "已接受",
    "thread": "线程",
    "level": "世界",
    "Chunk": "区块",
    "Loading": "正在加载",
    "Unloading": "正在卸载",
    "Time elapsed": "已用时",
    "TPS": "TPS",
    "Memory": "内存",
    "Heap": "堆内存",
    "Non-heap": "非堆内存",
    "Classes": "类",
    "Threads": "线程",
    "all the leaks": "泄漏检测",
    "Memory Leaks detected": "检测到内存泄漏",
    "force_refresh": "强制刷新",
    "Player": "玩家",
    "ServerPlayer": "在线玩家",
    "ChunkAccess": "区块访问",
    "LevelChunk": "区块数据",
    "minecraft": "我的世界",
}

def translate_line(line):
    """简单的MC日志中英翻译"""
    result = line
    # 按词典长度从长到短替换，避免短词覆盖长词
    for en, zh in sorted(TRANSLATIONS.items(), key=lambda x: -len(x[0])):
        result = result.replace(en, zh)
    return result

cache = {"data": None, "ts": 0}
CACHE_TTL = 5  # 5秒缓存

def get_logs(lines=80):
    try:
        with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
            all_lines = f.readlines()
        # 翻译每行日志
        translated = [translate_line(l.rstrip()) for l in all_lines[-lines:]]
        return {"logs": translated, "total": len(all_lines)}
    except Exception as e:
        return {"logs": [], "error": str(e)}

def get_status():
    global cache
    if cache["data"] and time.time() - cache["ts"] < CACHE_TTL:
        return cache["data"]
    try:
        s = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}", timeout=3)
        status = s.status()
        data = {
            "online": True,
            "players": {
                "online": status.players.online,
                "max": status.players.max
            },
            "version": {
                "name_clean": status.version.name
            },
            "ping": round(status.latency, 1)
        }
        cache = {"data": data, "ts": time.time()}
        return data
    except Exception as e:
        return {
            "online": False,
            "error": str(e)
        }

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            data = get_status()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        elif self.path.startswith("/logs"):
            data = get_logs()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<h1>MC状态服务运行中</h1><p>端口: {SERVICE_PORT}</p><p>MC服务器: {MC_HOST}:{MC_PORT}</p>".encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # 静默日志

if __name__ == "__main__":
    print(f"MC状态服务已启动: http://localhost:{SERVICE_PORT}")
    print(f"查询目标: {MC_HOST}:{MC_PORT}")
    print("按 Ctrl+C 停止")
    server = HTTPServer(("0.0.0.0", SERVICE_PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
