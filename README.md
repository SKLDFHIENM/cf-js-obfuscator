# Cloudflare JS 混淆工具 (cf-js-obfuscator)

专为 Cloudflare Workers、Pages 及现代前端脚本优化的纯客户端 JavaScript 混淆工具。

## ✨ 特性说明

1. **去掉原站页脚**：纯净无推广，完全复刻原站功能。
2. **零服务端存储**：全部混淆流程在浏览器端通过 Web Worker / AST 内存运行，不上传任何代码至云端。
3. **完美支持二次混淆（叠加混淆）**：
   - 每次混淆生成独立的随机前缀 `identifiersPrefix`，杜绝变量作用域冲突。
   - 禁用 `simplify`，防止破坏已混淆代码的 AST 结构与函数调用。
   - 保持属性不重命名（`renameProperties: false`），确保对外 API 与 JSON 解析安全。
4. **Cloudflare Workers 100% 兼容**：
   - 严格保护 Worker 全局与模块接口：`fetch`, `Request`, `Response`, `env`, `ctx`, `connect`, `WebSocket`, `HTMLRewriter` 等。
   - 禁用高 CPU 占用的控制流平坦化，彻底规避 `CPU time limit exceeded`。
   - 禁用自防御（`selfDefending`）与反调试（`debugProtection`），杜绝 Worker 运行时崩溃。

## 🌐 访问地址

- **绑定域名**：https://js.205.dpdns.org

## 🚀 部署与管理

由 Cloudflare Workers 原生驱动，开箱即用。
