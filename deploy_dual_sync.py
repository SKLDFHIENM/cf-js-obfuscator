# -*- coding: utf-8 -*-
"""
Cloudflare JS 混淆工具 - 双地址同步推送与部署脚本 (安全隔离版)
优先从本地配置文件 cf_deploy_config.json 或环境变量加载 API 凭据，杜绝密钥泄露风险。
"""
import requests, json, time, os, sys

sys.stdout.reconfigure(encoding="utf-8")

def load_targets():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_file = os.path.join(script_dir, "cf_deploy_config.json")
    if os.path.exists(cfg_file):
        with open(cfg_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # 备选：从环境变量加载
    raw_env = os.environ.get("CF_DUAL_TARGETS_JSON")
    if raw_env:
        return json.loads(raw_env)
        
    print("错误: 未找到 cf_deploy_config.json 且未设置 CF_DUAL_TARGETS_JSON 环境变量！")
    sys.exit(1)

def deploy_to_node(node, worker_code):
    print(f"\n==========================================")
    print(f"🚀 开始同步推送: {node['name']} -> https://{node['domain']}/")
    print(f"==========================================")
    
    headers = {"X-Auth-Email": node["email"], "X-Auth-Key": node["key"]}
    
    # 1. 确保 DNS 记录已解析并开启代理
    r_dns = requests.get(f"https://api.cloudflare.com/client/v4/zones/{node['zone_id']}/dns_records?name={node['domain']}", headers=headers).json()
    recs = r_dns.get("result", [])
    if not recs:
        print(f"[*] 自动创建 DNS AAAA 记录: {node['domain']} -> 100:: (proxied=True)")
        requests.post(f"https://api.cloudflare.com/client/v4/zones/{node['zone_id']}/dns_records", headers=headers, json={
            "type": "AAAA",
            "name": node["domain"],
            "content": "100::",
            "ttl": 1,
            "proxied": True
        })
    else:
        print(f"[✓] DNS 记录已就绪 ({node['domain']} -> {recs[0]['type']} {recs[0]['content']})")

    # 2. 上传 Worker 脚本
    metadata = {
        "main_module": "worker.js",
        "compatibility_date": "2024-09-23"
    }
    files = {
        "metadata": (None, json.dumps(metadata), "application/json"),
        "worker.js": ("worker.js", worker_code.encode("utf-8"), "application/javascript+module")
    }
    print(f"[*] 正在上传 Worker: {node['worker_name']} 到账号 {node['email']}...")
    r_up = requests.put(f"https://api.cloudflare.com/client/v4/accounts/{node['account_id']}/workers/scripts/{node['worker_name']}", headers=headers, files=files).json()
    if r_up.get("success"):
        print(f"[✓] Worker 编译并上传成功！")
    else:
        print(f"[✗] Worker 上传失败: {r_up.get('errors')}")
        return False

    # 3. 确保路由绑定正确
    route_pattern = f"{node['domain']}/*"
    r_routes = requests.get(f"https://api.cloudflare.com/client/v4/zones/{node['zone_id']}/workers/routes", headers=headers).json()
    routes = r_routes.get("result", [])
    matched = next((r for r in routes if r.get("pattern") == route_pattern), None)
    if not matched:
        print(f"[*] 创建 Worker 路由: {route_pattern} -> {node['worker_name']}")
        requests.post(f"https://api.cloudflare.com/client/v4/zones/{node['zone_id']}/workers/routes", headers=headers, json={
            "pattern": route_pattern,
            "script": node["worker_name"]
        })
    else:
        print(f"[✓] 路由已存在并关联到: {matched.get('script')}")

    return True

def verify_node(node):
    url = f"https://{node['domain']}/"
    health_url = f"https://{node['domain']}/api/health"
    try:
        r = requests.get(url, timeout=10)
        rh = requests.get(health_url, timeout=10)
        print(f"[✓] 验证健康状态: {node['name']} ({url}) -> 页面 HTTP {r.status_code} | API: {rh.text}")
        return r.status_code == 200
    except Exception as e:
        print(f"[✗] 验证访问异常: {node['name']} ({url}) -> {e}")
        return False

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    worker_path = os.path.join(script_dir, "worker.js")
    if not os.path.exists(worker_path):
        worker_path = "worker.js"
    
    with open(worker_path, "r", encoding="utf-8") as f:
        code = f.read()

    print(f"读取 worker.js 成功，共 {len(code)} 字符。")
    targets = load_targets()
    all_ok = True
    for node in targets:
        ok = deploy_to_node(node, code)
        if not ok:
            all_ok = False

    print("\n等待 Cloudflare 全球边缘网络生效 3 秒...")
    time.sleep(3)

    print("\n=== 双地址实时连通性健康复查 ===")
    for node in targets:
        verify_node(node)

    if all_ok:
        print("\n🎉 双地址推送与同步部署全部成功！")
    else:
        print("\n⚠️ 部分节点部署存在异常，请检查输出日志。")

if __name__ == "__main__":
    main()
