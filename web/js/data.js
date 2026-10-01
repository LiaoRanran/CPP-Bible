// 672b · 数据层单点（统一 fetch / 转义 / 指标格式化 / 百分比）
//
// 站点零构建（无框架、无打包、无后端）；本模块只在浏览器运行时被各页面 import。
// 把"取数 + 渲染前卫生"收口到一处，避免每个页面各写一套 fetch / esc / formatMetric。
//
// 纪律（与 home.js 注释一致）：前端**只渲染，不写死**。
//   · 拿不到的值 ⇒ 显示 `--`（绝不猜、绝不填 0 冒充真实值）；
//   · 真 0 ⇒ 显示 `0`（`--` 与 `0` 严格区分，缺失不是零）。
// 这与 robustness_core.formatMetric 的旧语义（0 也归 `--`）不同：旧实现把"真 0"
// 和"取不到"合并成 `--`，是在**撒谎**；这里把 0 还原成 0。

/**
 * 页内缓存：同源同路径只取一次，避免时间线 / 提交 / 指标反复拉同一份 JSON。
 * 缓存挂在 `window` 上（"页内"＝单页生命周期）：每次页面加载是一个新 window，
 * 缓存随之自然重置，不会跨"页面"泄漏。
 * 无 window 环境（纯 Node 测试）回退到模块级 Map，保证单进程内仍去重。
 */
function cacheFor() {
  if (typeof globalThis !== 'undefined' && globalThis.window) {
    if (!globalThis.window.__dataCache) globalThis.window.__dataCache = new Map();
    return globalThis.window.__dataCache;
  }
  return _fallbackCache;
}
const _fallbackCache = new Map();

/**
 * 统一取 JSON：失败重试 3 次、间隔 1s、单次超时 8s（AbortController）、页内 Map 缓存。
 * @param {string} url
 * @param {{retries?:number, retryDelay?:number, timeout?:number}} [opts]
 */
export async function fetchJSON(url, { retries = 3, retryDelay = 1000, timeout = 8000 } = {}) {
  const cache = cacheFor();
  if (cache.has(url)) return cache.get(url);
  let attempt = 0;
  let lastErr;
  while (true) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), timeout);
    try {
      const res = await fetch(url, { cache: 'no-store', signal: ctrl.signal });
      if (!res.ok) {
        // HTTP 状态码错误（404 / 5xx）是确定的，重试无意义 ⇒ 直接抛错、不重试。
        // 这对前端 boot() 很关键：源缺席（404）应当"快速失败"，
        // 否则每缺一个源都要重试 3×1s，页面与冒烟测试会假死在等待里。
        const err = new Error(`${url} → HTTP ${res.status}`);
        err.isHttp = true;
        throw err;
      }
      const data = await res.json();
      cache.set(url, data);
      return data;
    } catch (e) {
      lastErr = e;
      // 只对"网络/超时"类异常重试；HTTP 错误（e.isHttp）立即抛出。
      if (e.isHttp || attempt >= retries) break;
      await new Promise((r) => setTimeout(r, retryDelay));
      attempt++;
    } finally {
      clearTimeout(timer);
    }
  }
  throw lastErr;
}

/** HTML 转义：把来自 JSON 的字符串安全地塞进 innerHTML（防 XSS / 防 markup 注入）。 */
export function esc(s) {
  return String(s ?? '').replace(/[&<>"]/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

/**
 * 指标显示：缺失 ⇒ `--`；真 0 ⇒ `0`（缺失不是零，0 也不该被藏成 `--`）。
 * 空字符串同样视为"取不到"。
 */
export function formatMetric(v) {
  if (v === null || v === undefined || v === '') return '--';
  if (v === 0) return '0';
  return String(v);
}

/** 百分比包装：缺失 ⇒ `--`，否则 `数值%`（数值走 formatMetric 的 0/缺失区分）。 */
export function pct(v) {
  return v == null ? '--' : formatMetric(v) + '%';
}
