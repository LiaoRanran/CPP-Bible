// 670c A6 · 对比度审计（纯逻辑，无 DOM —— 可在 Node 真跑）
//
// 目的：把"新组件文字与背景对比度 ≥ 4.5:1"这条纪律变成**可复算**的检查，
// 而不是靠肉眼看。颜色全部来自 css/design-tokens.css，不在这里硬编码色值。
//
// 口径：
//  · WCAG 2.1 相对亮度 + 对比度公式 ((L1+0.05)/(L2+0.05))。
//  · 半透明底（如 --color-accent-soft 是 rgba）先与父层做 alpha 合成再算，
//    并且**对每个可能的父层都算一遍取最差值**（保守），父层在结果里标出来。
//  · 只审计 670c 新增/深化组件用到的配对；不宣称覆盖全站。

export const AA_NORMAL = 4.5;   // 正文
export const AA_LARGE = 3.0;    // 大字（≥18.66px bold / ≥24px）

/** #rgb / #rrggbb / rgb() / rgba() → {r,g,b,a}；无法识别返回 null */
export function parseColor(str) {
  if (typeof str !== 'string') return null;
  const s = str.trim();
  let m = /^#([0-9a-f]{3})$/i.exec(s);
  if (m) {
    const [r, g, b] = m[1].split('').map((c) => parseInt(c + c, 16));
    return { r, g, b, a: 1 };
  }
  m = /^#([0-9a-f]{6})$/i.exec(s);
  if (m) {
    const n = parseInt(m[1], 16);
    return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255, a: 1 };
  }
  m = /^rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)$/i.exec(s);
  if (m) {
    const r = Number(m[1]), g = Number(m[2]), b = Number(m[3]);
    const a = m[4] === undefined ? 1 : Number(m[4]);
    if (![r, g, b, a].every(Number.isFinite)) return null;
    return { r, g, b, a };
  }
  return null;
}

/** 把半透明色 fg 合成到不透明底 bg 上 */
export function over(fg, bg) {
  if (!fg) return bg;
  if (fg.a >= 1) return { r: fg.r, g: fg.g, b: fg.b, a: 1 };
  const a = fg.a;
  return {
    r: fg.r * a + bg.r * (1 - a),
    g: fg.g * a + bg.g * (1 - a),
    b: fg.b * a + bg.b * (1 - a),
    a: 1,
  };
}

/** WCAG 相对亮度 */
export function relLuminance(c) {
  const f = (v) => {
    const x = v / 255;
    return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
}

/** 对比度（1..21）。两色都须可解析，否则返回 null */
export function contrastRatio(a, b) {
  const ca = typeof a === 'string' ? parseColor(a) : a;
  const cb = typeof b === 'string' ? parseColor(b) : b;
  if (!ca || !cb) return null;
  const l1 = relLuminance(ca), l2 = relLuminance(cb);
  const hi = Math.max(l1, l2), lo = Math.min(l1, l2);
  return (hi + 0.05) / (lo + 0.05);
}

/**
 * 解析 CSS 文本里的自定义属性，按主题归并。
 * 支持：:root（暗色默认）、@media prefers-color-scheme:light 内的 :root:not([data-theme="dark"])、
 *       html[data-theme="light"]、html[data-theme="dark"]。
 */
export function parseTokens(cssText) {
  const stack = [];
  const blocks = [];
  let buf = '';
  for (const c of String(cssText)) {
    if (c === '{') { stack.push(buf.trim()); buf = ''; }
    else if (c === '}') {
      const sel = stack.pop();
      // 记录非 at-rule 块的 body，同时保留它外面的 at-rule 上下文（如 prefers-color-scheme）
      if (sel && !sel.startsWith('@')) blocks.push({ sel, ctx: stack.join(' '), body: buf });
      buf = '';
    } else buf += c;
  }
  const base = {}, light = {}, dark = {};
  for (const { sel, ctx, body } of blocks) {
    const decls = {};
    const re = /(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);/g;
    let m;
    while ((m = re.exec(body))) decls[m[1]] = m[2].trim();

    // 主题判定必须看**上下文**：
    //   @media (prefers-color-scheme: light) { :root:not([data-theme="dark"]) { ... } }
    // 这条选择器里带 "dark" 字样，但它是**浅色**主题 —— 只看 sel 会判反（670c 踩过）。
    const lightCtx = /prefers-color-scheme:\s*light/i.test(ctx);
    const darkCtx = /prefers-color-scheme:\s*dark/i.test(ctx);
    const lightSel = /data-theme=["']light["']/.test(sel) || /prefers-color-scheme:\s*light/i.test(sel);
    const darkSel = /data-theme=["']dark["']/.test(sel);
    const excludesDark = /:not\(\[data-theme=["']dark["']\]\)/.test(sel);

    let theme = null;
    if (lightSel || (lightCtx && excludesDark)) theme = 'light';
    else if (darkSel || (darkCtx && /:not\(\[data-theme=["']light["']\]\)/.test(sel))) theme = 'dark';
    else if (/:root/.test(sel) && !lightCtx && !darkCtx) theme = 'base';

    if (theme === 'light') Object.assign(light, decls);
    else if (theme === 'dark') Object.assign(dark, decls);
    else if (theme === 'base') Object.assign(base, decls);
  }
  return {
    dark: { ...base, ...dark },
    light: { ...base, ...light },
  };
}

/** 把 token 名解析成可算的颜色；半透明则按 parents 逐个合成 */
export function resolveColor(tokens, name, parents = []) {
  const raw = tokens[name];
  if (raw === undefined) return null;
  const c = parseColor(raw);
  if (!c) return null;
  if (c.a >= 1) return { color: c, parent: null };
  let worst = null;
  for (const p of parents) {
    const pc = parseColor(tokens[p]);
    if (!pc) continue;
    const flat = over(c, over(pc, { r: 255, g: 255, b: 255, a: 1 }));
    const ratio = contrastRatio(flat, over(pc, { r: 255, g: 255, b: 255, a: 1 }));
    void ratio;
    if (!worst) worst = { color: flat, parent: p };
    else {
      // 保留"对前景最不利"的那个父层由调用方比较，这里只记录第一个可用的
    }
  }
  return worst ? { color: worst.color, parent: worst.parent } : { color: over(c, { r: 255, g: 255, b: 255, a: 1 }), parent: null };
}

/** 670c 新增组件实际用到的配对（fg 文字 / bg 底），bg 半透明时列出候选父层 */
export const PAIRS_670C = [
  { name: '页头 lede', fg: '--color-text-mute', bg: '--color-bg' },
  { name: '正文 / 底', fg: '--color-text', bg: '--color-bg' },
  { name: '正文 / 卡片', fg: '--color-text', bg: '--color-surface' },
  { name: '次级文字 / 卡片', fg: '--color-text-dim', bg: '--color-surface' },
  { name: '三级文字 / 卡片', fg: '--color-text-mute', bg: '--color-surface' },
  { name: '统计数值 / 次级面', fg: '--color-text', bg: '--color-surface-2' },
  { name: '统计标签 / 次级面', fg: '--color-text-mute', bg: '--color-surface-2' },
  { name: '薄弱数值 / 次级面', fg: '--color-fail', bg: '--color-surface-2' },
  { name: '良好数值 / 次级面', fg: '--color-pass', bg: '--color-surface-2' },
  { name: '证据链节点 / 次级面', fg: '--color-text', bg: '--color-surface-2' },
  { name: '证据链说明 / 次级面', fg: '--color-text-dim', bg: '--color-surface-2' },
  { name: '证据链输出 / 次级面', fg: '--color-pass', bg: '--color-surface-2' },
  { name: 'sanitizer 输出 / 次级面', fg: '--color-text-dim', bg: '--color-surface-2' },
  { name: 'kbd 键帽 / 次级面', fg: '--color-text-dim', bg: '--color-surface-2' },
  { name: '明细面板键 / 次级面', fg: '--color-text-mute', bg: '--color-surface-2' },
  { name: '明细面板值 / 次级面', fg: '--color-text-dim', bg: '--color-surface-2' },
  { name: '图表刻度 / 面板', fg: '--color-text-mute', bg: '--color-surface' },
  { name: '对比表单元格 / 面板', fg: '--color-text-dim', bg: '--color-surface' },
  { name: '漂移值 / 面板', fg: '--color-text-dim', bg: '--color-surface' },
  { name: '时间线时间 / 面板', fg: '--color-text-mute', bg: '--color-surface' },
  { name: '时间线内容 / 面板', fg: '--color-text-dim', bg: '--color-surface' },
  { name: '页脚链接 / 底', fg: '--color-accent', bg: '--color-bg' },
  { name: '聚类标签 / 底', fg: '--color-text-mute', bg: '--color-bg' },
  // 半透明底：列出候选父层
  { name: '热力图计数 / 选中底', fg: '--color-text', bg: '--color-accent-soft', parents: ['--color-surface', '--color-surface-2', '--color-bg'] },
  { name: '热力图标签 / 选中底', fg: '--color-text-dim', bg: '--color-accent-soft', parents: ['--color-surface', '--color-surface-2', '--color-bg'] },
  { name: '热力图标签 / 未学底', fg: '--color-text-mute', bg: '--color-surface-2' },
  { name: '差异高亮 / 面板', fg: '--color-fail', bg: '--color-surface' },
];

/**
 * 审计一批配对。半透明底会对每个候选父层算一次，取**最差**（最低）比值——
 * 保守口径：只要最差的那个也过线，才算过。
 */
export function auditPairs(tokens, pairs = PAIRS_670C, { min = AA_NORMAL } = {}) {
  const results = [];
  for (const p of pairs) {
    const fgC = parseColor(tokens[p.fg]);
    const bgRaw = parseColor(tokens[p.bg]);
    if (!fgC || !bgRaw) {
      results.push({ ...p, ratio: null, pass: false, error: 'token 缺失或无法解析' });
      continue;
    }
    const parents = bgRaw.a >= 1 ? [null] : (p.parents || ['--color-surface', '--color-bg']);
    let worst = Infinity, worstParent = null, fgUsed = fgC;
    for (const pn of parents) {
      const base = pn ? parseColor(tokens[pn]) : { r: 255, g: 255, b: 255, a: 1 };
      if (!base) continue;
      const flatBg = over(bgRaw, over(base, { r: 255, g: 255, b: 255, a: 1 }));
      const flatFg = over(fgC, flatBg);
      const r = contrastRatio(flatFg, flatBg);
      if (r !== null && r < worst) { worst = r; worstParent = pn; fgUsed = flatFg; }
    }
    if (!Number.isFinite(worst)) {
      results.push({ ...p, ratio: null, pass: false, error: '无法计算（父层 token 缺失）' });
      continue;
    }
    results.push({
      name: p.name, fg: p.fg, bg: p.bg, parent: worstParent,
      ratio: Math.round(worst * 100) / 100, pass: worst >= min, min,
    });
  }
  return results;
}

/** 一次审计两个主题 */
export function auditCss(cssText, opts = {}) {
  const themes = parseTokens(cssText);
  const out = {};
  for (const t of Object.keys(themes)) out[t] = auditPairs(themes[t], PAIRS_670C, opts);
  const failures = [];
  for (const [t, rs] of Object.entries(out)) {
    for (const r of rs) if (!r.pass) failures.push({ theme: t, ...r });
  }
  return { themes: out, failures, ok: failures.length === 0, pairs: PAIRS_670C.length };
}

// ── CLI ──
const _argv1 = (typeof process !== 'undefined' && process.argv) ? process.argv[1] : undefined;
if (_argv1 && String(_argv1).replace(/\\/g, '/').endsWith('/js/contrast_check.js')) {
  const { readFileSync } = await import('node:fs');
  const { fileURLToPath } = await import('node:url');
  const { dirname, join } = await import('node:path');
  const here = dirname(fileURLToPath(import.meta.url));
  const css = readFileSync(join(here, '..', 'css', 'design-tokens.css'), 'utf8');
  const rep = auditCss(css);
  for (const [theme, rs] of Object.entries(rep.themes)) {
    console.log('── ' + theme + ' ──');
    for (const r of rs) {
      const mark = r.pass ? 'PASS' : 'FAIL';
      console.log('  ' + mark + ' ' + String(r.ratio ?? 'n/a').padStart(6) + ':1  ' + r.name
        + '  (' + r.fg + ' on ' + r.bg + (r.parent ? ' over ' + r.parent : '') + ')');
    }
  }
  console.log('contrast_check: pairs=' + rep.pairs + ' failures=' + rep.failures.length);
  process.exit(rep.ok ? 0 : 1);
}
