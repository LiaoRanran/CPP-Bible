// 653 B · 共享工具（无框架、无构建、无后端）
// 666 B1：四态色与 LINK_STYLE 改为**与 css/design-tokens.css 同一组值**
//   （canvas 拿不到 CSS 变量，必须在这里镜像；改色请**同时**改两处 —— 
//    `tools/web_data_pipeline_656.py --check` 会算对比度，两处不一致时肉眼可见）。
export const STATE_COLORS = {
  pass: '#4ade80',
  pass_with_exception: '#fbbf24',
  fail: '#f87171',
  unknown: '#8b9299',
};
export const STATE_LABELS = {
  pass: 'pass · 通过',
  pass_with_exception: 'pass_with_exception · 带例外通过',
  fail: 'fail · 不通过',
  unknown: 'unknown · 未知',
};
export const KIND_LABELS = { card: '卡（原子知识）', prop: '命题', misconception: '误解（攻击者）' };
export const LINK_STYLE = {
  attack:   { color: '248,113,113', width: 0.6, alpha: 0.55 },  // 攻击边（fail 色）
  defend:   { color: '74,222,128',  width: 0.5, alpha: 0.30 },  // 防御边（pass 色）
  asserts:  { color: '91,141,239',  width: 0.7, alpha: 0.35 },  // 卡→命题（accent 色）
};

/* ── 671d：canvas 拿不到 CSS 变量，只能镜像；但**一套值不够用** ──────────
 * 深色底上够亮的绿（#4ade80，11.4:1）放到浅色底（#fafafa）只有 1.67:1，
 * 图形元素的 WCAG 阈值是 3:1 ⇒ 旧代码在浅色主题下的星图/首页图**不达标**。
 * 这里给出两套，由 stateColors() / linkStyle() 按当前主题返回。
 * 判定口径与 css/design-tokens.css 一致：`html[data-theme]`，否则跟随系统。 */
const STATE_COLORS_LIGHT = {
  pass: '#15803d',
  pass_with_exception: '#a16207',
  fail: '#b91c1c',
  unknown: '#5b6068',
};
const LINK_STYLE_LIGHT = {
  attack:   { color: '185,28,28',  width: 0.6, alpha: 0.55 },
  defend:   { color: '21,128,61',  width: 0.5, alpha: 0.30 },
  asserts:  { color: '37,99,235',  width: 0.7, alpha: 0.35 },
};

/** 当前是否浅色主题（与 qy-nav 的切换口径一致：`html[data-theme]`） */
export function isLightTheme() {
  if (typeof document === 'undefined') return false;
  const t = document.documentElement && document.documentElement.dataset
    ? document.documentElement.dataset.theme : null;
  if (t === 'light') return true;
  if (t === 'dark') return false;
  return !!(typeof matchMedia === 'function' && matchMedia('(prefers-color-scheme: light)').matches);
}

/** 当前主题下的四态色（canvas 用） */
export function stateColors() {
  return isLightTheme() ? STATE_COLORS_LIGHT : STATE_COLORS;
}

/** 当前主题下的连线样式（canvas 用） */
export function linkStyle() {
  return isLightTheme() ? LINK_STYLE_LIGHT : LINK_STYLE;
}

/** 主题切换后重绘用的订阅（返回取消函数） */
export function onThemeChange(fn) {
  if (typeof matchMedia !== 'function') return () => {};
  const mq = matchMedia('(prefers-color-scheme: light)');
  const handler = () => fn();
  mq.addEventListener ? mq.addEventListener('change', handler) : mq.addListener(handler);
  return () => (mq.removeEventListener ? mq.removeEventListener('change', handler) : mq.removeListener(handler));
}

// 672b：fetchJSON 统一到数据层单点 web/js/data.js（带重试 / 超时 / 页内缓存）。
// 这里仅做 re-export，保证旧调用方（card.js / cards.js / starmap.js / verdicts.js / verify.js …）零改动。
export { fetchJSON } from './js/data.js';

export function fmtInt(n) {
  return (n ?? 0).toLocaleString('en-US');
}

export function shortHash(h, n = 16) {
  return h ? h.slice(0, n) + '…' : '—';
}

export function el(tag, attrs = {}, html = '') {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (html) e.innerHTML = html;
  return e;
}
