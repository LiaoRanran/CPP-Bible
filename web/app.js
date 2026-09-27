// 653 B · 共享工具（无框架、无构建、无后端）
export const STATE_COLORS = {
  pass: '#58c6b2',
  pass_with_exception: '#d8a657',
  fail: '#d96b6b',
  unknown: '#7a838c',
};
export const STATE_LABELS = {
  pass: 'pass · 通过',
  pass_with_exception: 'pass_with_exception · 带例外通过',
  fail: 'fail · 不通过',
  unknown: 'unknown · 未知',
};
export const KIND_LABELS = { card: '卡（原子知识）', prop: '命题', misconception: '误解（攻击者）' };
export const LINK_STYLE = {
  attack:   { color: '217,107,107', width: 0.6, alpha: 0.55 },  // 攻击边
  defend:   { color: '88,198,178',  width: 0.5, alpha: 0.30 },  // 防御边
  asserts:  { color: '138,180,248', width: 0.7, alpha: 0.35 },  // 卡→命题
};

export async function fetchJSON(url) {
  const r = await fetch(url, { cache: 'no-store' });
  if (!r.ok) throw new Error(`${url} → HTTP ${r.status}`);
  return r.json();
}

export function fmtInt(n) {
  return (n ?? 0).toLocaleString('en-US');
}

export function shortHash(h, n = 16) {
  return h ? h.slice(0, n) + '…' : '—';
}

/** 生成顶栏（避免每页重复） */
export function mountNav(current) {
  const items = [['index.html', '总览'], ['starmap.html', '星图'], ['verify.html', '现场验哈希']];
  const nav = document.createElement('nav');
  nav.className = 'nav';
  nav.innerHTML = `<span class="brand">QueYi · CPP-Bible</span>` +
    items.map(([h, t]) => `<a href="${h}"${h === current ? ' aria-current="page"' : ''}>${t}</a>`).join('') +
    `<span class="spacer"></span><span class="pill">静态站 · 无后端</span>`;
  document.body.prepend(nav);
}

export function el(tag, attrs = {}, html = '') {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (html) e.innerHTML = html;
  return e;
}
