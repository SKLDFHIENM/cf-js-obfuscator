# Cloudflare JS 混淆工具 (cf-js-obfuscator)

专为 Cloudflare Workers、Pages 及现代前端脚本优化的纯客户端 JavaScript 混淆与自愈工具。

## 🌐 双地址官方访问入口 (高可用双活)

- **节点 1 (主地址)**：[https://js.205.dpdns.org](https://js.205.dpdns.org)
- **节点 2 (镜像地址)**：[https://js.201.dpdns.org](https://js.201.dpdns.org)

两个节点采用全自动化双地址推送机制（Dual-Push Deployment），代码和功能实时保持 100% 同步双活。

---

## ✨ 核心特性

1. **去掉原站页脚**：纯净界面无广告、无多余推广，保留原生专业混淆体验。
2. **零服务端存储**：全部混淆流程在浏览器端通过内存 AST 执行，不上传任何代码至云端，确保敏感节点配置与代码隐私安全。
3. **完美支持二次混淆（已混淆脚本无损再混淆）**：
   - 针对超大文件（>80KB）或已具有洗牌循环的脚本，自适应切换为零 CPU 开销保护，避免触发 Cloudflare `Script startup exceeded CPU time limit`。
   - 自动在顶层注入跨平台全局宿主兼容垫片（`var window = typeof globalThis !== 'undefined' ? globalThis : ...`），彻底解决第三方混淆脚本直接调用裸 `window` 导致的 10021 部署报错。
4. **单行注释智能翻译与同义改写 (// 注释专用模式)**：
   - 提取代码中的 `//` 注释，英文注释自动翻译为规范技术中文，中文注释自动同义改写。
   - 代码主体 100% 保持原生 AST 与逻辑，零语法改动风险。
5. **智能自愈非法损坏字符（\uFFFD 乱码修复）**：
   - 自动检测并修复因剪贴板/文件编码损坏导致的残损 `import` 语句与非法中文字符标识符，确保通过 Cloudflare 语法解析。
6. **Cloudflare Workers 100% 深度适配**：
   - 深度保护 ES Module 导出（`export default`、`export { ... }`）与底层 TCP Socket（`cloudflare:sockets`）。
   - 保留全局 Worker 保留字（`fetch`, `Request`, `Response`, `env`, `ctx`, `WebSocket` 等）。

---

## 🚀 双地址同步推送与部署

在本地或 CI/CD 环境中，运行项目根目录下的双地址同步部署脚本：

```bash
python deploy_dual_sync.py
```

该脚本将自动完成：
1. 校验两个域名（`205.dpdns.org` 与 `201.dpdns.org`）的 Cloudflare DNS 解析与橙色云朵代理状态。
2. 将最新 `worker.js` 并发上传至两个独立的 Cloudflare 账号。
3. 自动配置/维护对应域名的 Worker 路由。
4. 触发边缘健康检查（`GET /api/health`）验证全链路服务状态。

---

## 📦 开源仓库

- GitHub 仓库：[SKLDFHIENM/cf-js-obfuscator](https://github.com/SKLDFHIENM/cf-js-obfuscator)
