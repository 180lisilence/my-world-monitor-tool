from mc_server import get_logs
r = get_logs()
print(f"行数: {len(r.get('logs', []))}")
if r.get('logs'):
    for l in r['logs'][-3:]:
        print(l[:80])
else:
    print("错误:", r.get('error', '无'))
