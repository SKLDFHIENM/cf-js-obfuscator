// Cloudflare Worker: cf-js-obfuscator
// 托管纯前端 JS 混淆工具，支持二次混淆与原生 Cloudflare Workers 脚本防护

const HTML_CONTENT = `${html.replace(/\\/g, "\\\\").replace(/\`/g, "\\\`").replace(/\\$/g, "\\\$")}`;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // 路由 1: 静态资源代理与分发 (index.browser.js)
    if (url.pathname === "/index.browser.js") {
      const cdnUrl = "https://cdnjs.cloudflare.com/ajax/libs/javascript-obfuscator/4.1.1/index.browser.js";
      
      const cache = caches.default;
      let response = await cache.match(request);
      if (!response) {
        try {
          const fetchResp = await fetch(cdnUrl, {
            headers: {
              "User-Agent": request.headers.get("User-Agent") || "Mozilla/5.0"
            }
          });
          if (fetchResp.ok) {
            response = new Response(fetchResp.body, {
              headers: {
                "content-type": "application/javascript; charset=utf-8",
                "cache-control": "public, max-age=604800, immutable",
                "access-control-allow-origin": "*"
              }
            });
            ctx.waitUntil(cache.put(request, response.clone()));
          } else {
            return Response.redirect(cdnUrl, 302);
          }
        } catch (e) {
          return Response.redirect(cdnUrl, 302);
        }
      }
      return response;
    }

    // 路由 2: 健康检查
    if (url.pathname === "/healthz" || url.pathname === "/ping") {
      return new Response("OK", { status: 200 });
    }

    // 路由 3: 默认展示混淆工具网页
    return new Response(HTML_CONTENT, {
      headers: {
        "content-type": "text/html; charset=utf-8",
        "cache-control": "public, max-age=3600",
        "x-content-type-options": "nosniff"
      }
    });
  }
};
