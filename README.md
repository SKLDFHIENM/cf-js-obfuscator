# WebShield 代码安全加固平台 (WebShield Obfuscator & Armour)

专为现代 Web 前端开发、单页应用（SPA）、静态网页及 Cloudflare Workers / Pages 打造的纯客户端代码加固、混淆与自愈平台。

## 🌐 双地址官方访问入口 (高可用双活)

- **主地址 (节点 1)**：[https://js.205.dpdns.org](https://js.205.dpdns.org)
- **镜像地址 (节点 2)**：[https://js.201.dpdns.org](https://js.201.dpdns.org)

两个节点采用全自动化双地址同步推送机制（Dual-Push Deployment），代码与功能实时保持 100% 同步双活。

---

## ✨ 核心特性

### 1. 🌐 HTML 网页原生自解密加固 (零外部库依赖)
- **无需任何外部第三方库**：生成的加密 HTML 包含轻量原生自解密执行引擎，完全使用浏览器内置 API（`TextDecoder`、`atob`、`document.write`），**不需要任何外部 CDN、离线即可运行**。
- **本地双击即用**：加密生成的 `.html` 文件，无论是直接在本地电脑双击打开（`file://` 协议），还是部署在任意服务器、Cloudflare Pages/Workers 上，均能毫秒级完美还原渲染。
- **源码防审查与防爬虫**：访客右键“查看网页源代码”时只显示一屏密文加载器，无法提取任何原始 DOM 结构、样式与文本内容。

### 2. ⚡ JavaScript 脚本极致稳定混淆 (二次混淆自适应)
- **零 CPU 启动开销自适应**：检测到脚本体积 >80KB 或包含已混淆洗牌逻辑时，自动关闭二次嵌套的全局字符串字典与包装器，转为纯 AST 标识符乱序与语法重组，彻底杜绝 Cloudflare `Script startup exceeded CPU time limit`（523 报错）。
- **顶层全局宿主垫片注入**：自动识别并注入 `var window = typeof globalThis !== 'undefined' ? globalThis : ...`，解决因第三方已混淆脚本直接访问裸 `window` 导致的 10021 错误。
- **原生 ES Module 强保护**：深度保护 `import { connect } from 'cloudflare:sockets'` 等底层通信导入与 `export default` 模块规范。

### 3. 🛡️ 深度代码装甲模式
- **全量字符串 Base64 字典化**：提取敏感 URL、API 路径与配置参数转为加密数组，结合数组旋转与洗牌，静态分析难度倍增。
- **字符碎片化切割**：分割长字符串字面量，规避关键词模式匹配与特征检测。

### 4. 📝 // 单行注释智能翻译与同义改写
- **语义级双向转换**：精准提取代码中的 `//` 注释，英文技术注释自动翻译为规范技术中文，已有中文注释自动同义语义改写（改变说法，不改意思）。
- **零语法风险**：非注释的业务代码 100% 保持原生 AST 与逻辑，零语法变动。

### 5. 🎨 现代交互体验
- **白天 / 黑夜模式一键切换**：内置深色极客风与浅色科技风主题，平滑动画过渡，自动持久化存储。
- **简单实用的网页计数器**：实时展示今日加固次数、全网累计保护代码量及自愈修复次数。
- **折叠式使用说明文档**：内置完整加固指南与排障建议。

---

## 🚀 本地运行与双地址同步推送

本项目支持两种运行方式：
1. **纯本地离线运行**：直接使用浏览器打开 `index.html`，无需任何后端环境即可离线使用全部加固功能。
2. **自动化双地址同步推送**：
   ```bash
   python deploy_dual_sync.py
   ```
   自动为 `js.205.dpdns.org` 和 `js.201.dpdns.org` 同步编译上传最新 Worker 并完成健康检查。

---

## 📦 开源仓库

- GitHub 仓库：[SKLDFHIENM/cf-js-obfuscator](https://github.com/SKLDFHIENM/cf-js-obfuscator)
