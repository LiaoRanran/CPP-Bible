// 670c A6 · 对比度审计（纯逻辑，无 DOM —— 可在 Node 真跑）
//
// 目的：把"新组件文字与背景对比度 ≥ 4.5:1"这条纪律变成**可复算**的检查，
// 而不是靠肉眼看。颜色全部来自 css/design-tokens.css，不在这里硬编码色值。
//
// 口径：
//  · WCAG 2.1 相对亮度 + 对比度公式 ((L1+0.05)/(L2+0.05))。
//  · 半透明底（如 --color-accent-soft 是 rgba）先与父层做 alpha 合成再算，
//    并且**对每个可能的父层都算一遍取最差值**（保守），父层在结果里标出来。
//
// 672a D · 口径修正：原来只有 PAIRS_670C 这 27 对写死的清单（文件头自己承认
//   "只审计 670c 组件用到的配对"）⇒ 新增组件、焦点环 vs 背景这类配对**永远进不了清单**，
//   审计数字精确到小数点、语义却是松的。现在改为两段式：
//     ① 基础清单 PAIRS_670C（27 对，已验证，不删不改 —— 回归口径）；
//     ② 自动抽取：扫 web/style.css + web/css/*.css，把 `color:` / `background:` /
//        `border-color:` 里的 var(--xxx) 解析成 design-tokens 的实际色值，
//        按"同一声明块 > 祖先选择器声明的底 > 页面底"的兜底链配成 fg/bg 对。
//   抽取出的配对去重后与①合并；焦点环配对显式加入（这是旧清单最大的盲区）。
//   注意：**不做全交叉**（fg 全集 × bg 全集）—— 那会把 accent 压 accent-strong
//   这种现实中不存在的组合也算进来（实测 1.60:1，纯噪音），任务书明令禁止。

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
    // 672a：自动抽取到的**字面量色**（横幅 / noscript 块，非令牌）没有 token 名，
    //       直接把 color 对象带进来；其余照旧按 token 名查表。
    const fgC = p.fgColor || parseColor(tokens[p.fg]);
    const bgRaw = p.bgColor || parseColor(tokens[p.bg]);
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
      source: p.source || 'base',
      file: p.file,                 // 自动抽取项的来源样式表（基础清单为 undefined）
      inferred: p.inferred,         // 背景是"声明的 / 祖先推断的 / 页面底兜底的"
    });
  }
  return results;
}

/** 一次审计两个主题（默认仍是 PAIRS_670C —— 回归口径不变，contrast.test 依赖它） */
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

/* ══════════════════════════════════════════════════════════════════════════
   672a D · 自动抽取（"新增组件自动进清单"）
   ══════════════════════════════════════════════════════════════════════════ */

/** 契约上的**非文字色**：design-tokens.css 明确"禁止用于正文"，故不进文字配对网格，
 *  改由 warns 报出（见 extractPairs）—— 这是纪律检查，不是对比度计算。 */
export const NON_TEXT_COLOR_TOKENS = ['--color-text-faint'];

/** 交互态 / 伪元素：hover/focus/active 等不进常规配对（那些是交互态，不需要 AA 级正文对比） */
const SKIP_SELECTOR_RE = /:(?:hover|focus|focus-visible|focus-within|active|disabled|checked|visited|link|target)\b|::(?:before|after|placeholder|selection|first-line|first-letter|marker|-webkit[\w-]*)\b|\[hidden\]/i;

/** 明确不是颜色的关键字（静默跳过，不算 warn —— 否则满屏噪音） */
const NON_COLOR_VALUES = new Set([
  'transparent', 'none', 'inherit', 'currentcolor', 'initial', 'unset', 'revert',
  '0', 'auto', 'clip-path',
]);

/** 注释 → 等量空白（**保行号**，warn 才能指到真实行） */
export function stripComments(text) {
  return String(text).replace(/\/\*[\s\S]*?\*\//g, (m) => m.replace(/[^\n]/g, ' '));
}

/** CSS 文本 → 声明块（含选择器 / at-rule 上下文 / 选择器所在行号） */
export function parseCssBlocks(cssText) {
  const stack = [];
  const blocks = [];
  let buf = '';
  let line = 1;
  let bufLine = 1;
  for (const ch of String(cssText)) {
    if (ch === '\n') { line++; buf += ch; continue; }
    if (buf.trim() === '' && ch !== ' ') bufLine = line;
    if (ch === '{') { stack.push({ sel: buf.trim(), line: bufLine }); buf = ''; }
    else if (ch === '}') {
      const top = stack.pop();
      if (top && top.sel && !top.sel.startsWith('@')) {
        blocks.push({
          sel: top.sel,
          ctx: stack.map((s) => s.sel).join(' '),
          body: buf,
          line: top.line,
        });
      }
      buf = '';
    } else buf += ch;
  }
  return blocks;
}

/** 声明块 body → { prop: value }（只取本块，不跨块） */
export function parseDecls(body) {
  const out = {};
  const re = /(^|[;{\s])([a-zA-Z-]+)\s*:\s*([^;{}]+)/g;
  let m;
  while ((m = re.exec(body))) {
    const prop = m[2].toLowerCase();
    if (!(prop in out)) out[prop] = m[3].trim();   // 同块重复声明取第一个
  }
  return out;
}

/** 沿 var() 链解析令牌，返回**最底层的规范名** + 色值；解析不出返回 null。
 *  例：--fg → var(--color-text) → #ededed ⇒ { name: '--color-text', color }。
 *  取规范名是必须的：auditPairs 用 parseColor(tokens[name]) 查表，别名层（var(...)）算不出色。 */
export function resolveTokenColor(tokens, name, depth = 0) {
  if (depth > 6) return null;                       // 防循环引用
  const raw = tokens[name];
  if (raw === undefined) return null;
  const direct = parseColor(raw);
  if (direct) return { name, color: direct };
  const m = /var\(\s*(--[A-Za-z0-9_-]+)/.exec(raw);
  if (m) return resolveTokenColor(tokens, m[1], depth + 1);
  return null;
}

/**
 * 解析一条声明值 → { kind, name, color }。
 * kind: 'token'（解析到令牌）/ 'literal'（字面量色或 var 的 fallback）/ 'skip'（不是颜色）/ 'unresolved'
 */
export function resolveDeclValue(raw, tokens) {
  let v = String(raw == null ? '' : raw).replace(/!important/gi, '').trim();
  if (!v) return { kind: 'skip' };
  if (/-gradient\(|url\(/i.test(v)) return { kind: 'unresolved', reason: `非纯色值：${v.slice(0, 40)}` };

  const varRe = /var\(\s*(--[A-Za-z0-9_-]+)\s*(?:,\s*(.+?)\s*)?\)/;
  const m = varRe.exec(v);
  if (m) {
    const token = m[1];
    const fallback = m[2];
    const hit = resolveTokenColor(tokens, token);
    if (hit) return { kind: 'token', name: hit.name, color: hit.color };
    // 令牌不存在 ⇒ 退到 fallback（672a 之前这些就是"僵尸变量"，正是靠 fallback 活下来的）
    if (fallback) {
      const fc = parseColor(fallback);
      if (fc) return { kind: 'literal', name: `${token}(fallback)`, color: fc };
    }
    return { kind: 'unresolved', name: token, reason: `令牌 ${token} 在 design-tokens.css 中不存在` };
  }
  if (NON_COLOR_VALUES.has(v.toLowerCase())) return { kind: 'skip' };
  const c = parseColor(v);
  if (c) return { kind: 'literal', name: v, color: c };
  return { kind: 'unresolved', reason: `无法解析的值：${v.slice(0, 40)}` };
}

/**
 * anc 与 sel 的"祖先强度"：0=无关，1=BEM 命名前缀（`.qy-banner` ⊃ `.qy-banner-close`），
 * 2=选择器前缀+组合器（`.detail` ⊃ `.detail .d-title`）。
 *
 * 说明（诚实登记）：DOM 嵌套关系靠 CSS 选择器是**推不出来**的 —— 这里用的是命名/选择器
 * 约定。等级 1 是启发式（BEM 前缀），可能误配；所以配对结果带 `inferred` 字段标出来，
 * 便于人工复核。`.card` 不认作 `.card-item` 的祖先（rest="-item" 不是组合器也不是 BEM 分隔）。
 */
function ancestorScore(anc, sel) {
  if (anc === sel || !sel.startsWith(anc)) return 0;
  const rest = sel.slice(anc.length);
  if (rest === '' || /^[\s>+~[]/.test(rest)) return 2;
  if (/^[-_]/.test(rest)) return 1;
  return 0;
}

/** 半透明底的候选父层（保守：逐个算取最差） */
const AUTO_PARENTS = ['--color-surface-2', '--color-surface', '--color-bg'];

/**
 * 从若干 CSS 源里抽取"文字/背景"配对。
 * @param {{file:string,text:string}[]} sources
 * @param {Record<string,string>} tokens 单主题的令牌表（用于解析 var 链）
 * @returns {{pairs:Array, warns:Array, stats:Object}}
 */
export function extractPairs(sources, tokens) {
  const pairs = [];
  const warns = [];
  const stats = { blocks: 0, skippedStates: 0, colors: 0, backgrounds: 0, borderColors: 0, unresolved: 0 };
  const byKey = new Map();

  // ── 1. 收集每个选择器的前景/背景 ──
  const items = [];
  for (const src of sources) {
    for (const b of parseCssBlocks(stripComments(src.text))) {
      if (/@keyframes|forced-colors/i.test(b.ctx)) continue;
      stats.blocks++;
      for (const sel of b.sel.split(',').map((s) => s.trim()).filter(Boolean)) {
        if (SKIP_SELECTOR_RE.test(sel)) { stats.skippedStates++; continue; }
        const d = parseDecls(b.body);
        const fgRaw = d.color;
        const bgRaw = d.background || d['background-color'];
        const bcRaw = d['border-color'];
        const fg = fgRaw === undefined ? null : resolveDeclValue(fgRaw, tokens);
        const bg = bgRaw === undefined ? null : resolveDeclValue(bgRaw, tokens);
        const bc = bcRaw === undefined ? null : resolveDeclValue(bcRaw, tokens);
        if (fg) stats.colors++;
        if (bg) stats.backgrounds++;
        if (bc) { stats.borderColors++; }
        items.push({ sel, file: src.file, line: b.line, fg, bg, bc });
      }
    }
  }

  // 去重口径：**同一文件内**按 (fg, bg) 去重；跨文件各留一条。
  // 理由：同一配色在 style.css / 669c.css / 组件里各写一遍，压成一条就丢掉了
  // "这条出现在哪个样式表"这层可定位性；而真正的冗余（同文件里 20 个选择器用同一配色）
  // 已经被压掉了。
  const push = (p) => {
    const key = `${p.file}|${p.fg}|${p.bg}`;
    const prev = byKey.get(key);
    // 同文件同配色只留一条；若已存的是"推断底"而新的是"声明底"，用后者替换（更可信）
    if (prev && !(prev.inferred && !p.inferred)) { prev.sources.push(p.sources[0]); return; }
    if (prev) pairs.splice(pairs.indexOf(prev), 1);
    byKey.set(key, p);
    pairs.push(p);
  };

  const pageBg = resolveTokenColor(tokens, '--color-bg');

  // ── 2. 配对：同块 → 祖先选择器 → 页面底 ──
  for (const it of items) {
    if (!it.fg) continue;
    if (it.fg.kind === 'unresolved') {
      warns.push({ file: it.file, line: it.line, selector: it.sel, token: it.fg.name || '-', reason: it.fg.reason });
      stats.unresolved++;
      continue;
    }
    if (!it.fg.color) continue;                                   // skip 类
    if (NON_TEXT_COLOR_TOKENS.includes(it.fg.name)) {
      warns.push({
        file: it.file, line: it.line, selector: it.sel, token: it.fg.name,
        reason: '契约上是非文字色（占位/分隔/图标），却被当作 color 用于文字 —— 属纪律问题，不进对比度网格',
      });
      continue;
    }
    let bg = null;
    let inferred = null;
    if (it.bg && it.bg.color) bg = it.bg;
    else if (it.bg && it.bg.kind === 'unresolved' && /遮罩|overlay/i.test(String(it.bg.reason))) { /* 忽略 */ }
    if (!bg) {
      let best = null;
      let bestScore = 0;
      for (const cand of items) {
        if (!cand.bg || !cand.bg.color) continue;
        const sc = ancestorScore(cand.sel, it.sel);
        if (!sc) continue;
        // 先比可信度（组合器 > BEM 前缀），同分取更长的（更近的祖先）
        if (sc > bestScore || (sc === bestScore && best && cand.sel.length > best.sel.length)) {
          best = cand; bestScore = sc;
        }
      }
      if (best) { bg = best.bg; inferred = `ancestor:${best.sel}`; }
    }
    if (!bg && pageBg) { bg = { kind: 'token', name: pageBg.name, color: pageBg.color }; inferred = 'page'; }
    if (!bg) {
      warns.push({ file: it.file, line: it.line, selector: it.sel, token: it.fg.name, reason: '找不到可配对的背景层' });
      continue;
    }
    const bgIsToken = bg.kind === 'token';
    push({
      name: `auto: ${it.sel}`,
      file: it.file,
      fg: it.fg.name,
      bg: bg.name,
      fgColor: it.fg.kind === 'literal' ? it.fg.color : undefined,
      bgColor: bg.kind === 'literal' ? bg.color : undefined,
      parents: bg.color.a < 1 ? AUTO_PARENTS : undefined,
      inferred: inferred || undefined,
      source: 'auto',
      sources: [{ file: it.file, line: it.line, selector: it.sel }],
    });
    void bgIsToken;
  }
  return { pairs, warns, stats };
}

/** 焦点环配对（旧清单最大的盲区：焦点环 vs 背景从来没进过清单）。
 *  --focus-ring = 2px solid var(--color-accent)；--bg/--panel/--panel-2 是
 *  --color-bg/--color-surface/--color-surface-2 的别名，这里写规范名（auditPairs 要能查到色）。 */
export const FOCUS_RING_PAIRS = [
  { name: '焦点环 / 底', fg: '--color-accent', bg: '--color-bg', source: 'focus-ring' },
  { name: '焦点环 / 卡片', fg: '--color-accent', bg: '--color-surface', source: 'focus-ring' },
  { name: '焦点环 / 次级面', fg: '--color-accent', bg: '--color-surface-2', source: 'focus-ring' },
];

/** 合并：基础 27 + 焦点环 + 自动抽取（抽取内部已去重，与基础清单并列保留：
 *  基础清单是"已验证的核心配对"，抽取项是"组件实际用法"，两者都留在结果里可交叉核对）。 */
export function buildPairList(tokens, sources = []) {
  const { pairs, warns, stats } = extractPairs(sources, tokens);
  const merged = [
    ...PAIRS_670C.map((p) => ({ ...p, source: 'base' })),
    ...FOCUS_RING_PAIRS,
    ...pairs,
  ];
  return { pairs: merged, warns, stats };
}

/** 一次审计两个主题（完整清单 = 基础 + 焦点环 + 自动抽取） */
export function auditCssFull(cssText, sources = [], opts = {}) {
  const themes = parseTokens(cssText);
  const out = {};
  let pairs = 0;
  const warns = [];
  let stats = {};
  for (const t of Object.keys(themes)) {
    const built = buildPairList(themes[t], sources);
    out[t] = auditPairs(themes[t], built.pairs, opts);
    pairs = built.pairs.length;
    stats = built.stats;
    for (const w of built.warns) warns.push({ theme: t, ...w });
  }
  // 主题无关的口径声明（错误色令牌缺失这类）
  if (resolveTokenColor(themes.dark || {}, '--color-error') === null) {
    warns.push({
      theme: 'both', file: 'design-tokens.css', line: 0, selector: ':root', token: '--color-error',
      reason: '无此令牌 ⇒ 错误色配对跳过；robustness.css 的横幅 #7f1d1d 仍为硬编码（待令牌化）',
    });
  }
  const failures = [];
  for (const [t, rs] of Object.entries(out)) {
    for (const r of rs) if (!r.pass) failures.push({ theme: t, ...r });
  }
  // warns 按主题去重（两个主题扫的是同一批文件）
  const seen = new Set();
  const uniqWarns = warns.filter((w) => {
    const k = `${w.file}|${w.line}|${w.selector}|${w.token}`;
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  });
  return { themes: out, failures, ok: failures.length === 0, pairs, warns: uniqWarns, stats };
}

// ── CLI ──
const _argv1 = (typeof process !== 'undefined' && process.argv) ? process.argv[1] : undefined;
if (_argv1 && String(_argv1).replace(/\\/g, '/').endsWith('/js/contrast_check.js')) {
  const { readFileSync, readdirSync, existsSync } = await import('node:fs');
  const { fileURLToPath } = await import('node:url');
  const { dirname, join } = await import('node:path');
  const here = dirname(fileURLToPath(import.meta.url));
  const asJson = (typeof process !== 'undefined' && process.argv.includes('--json'));

  // 令牌源（唯一真相）
  const css = readFileSync(join(here, '..', 'css', 'design-tokens.css'), 'utf8');
  // 被审计的样式表：主样式 + css/ 下的外围样式表（design-tokens 自己是令牌源，跳过）
  const sources = [];
  for (const rel of ['../style.css']) {
    const p = join(here, rel);
    if (existsSync(p)) sources.push({ file: rel, text: readFileSync(p, 'utf8') });
  }
  const cssDir = join(here, '..', 'css');
  if (existsSync(cssDir)) {
    for (const f of readdirSync(cssDir).sort()) {
      if (!f.endsWith('.css') || f === 'design-tokens.css') continue;
      sources.push({ file: 'css/' + f, text: readFileSync(join(cssDir, f), 'utf8') });
    }
  }

  const rep = auditCssFull(css, sources);

  if (asJson) {
    console.log(JSON.stringify(rep, null, 2));
  } else {
    for (const [theme, rs] of Object.entries(rep.themes)) {
      console.log('── ' + theme + ' ──');
      for (const r of rs) {
        const mark = r.pass ? 'PASS' : 'FAIL';
        console.log('  ' + mark + ' ' + String(r.ratio ?? 'n/a').padStart(6) + ':1  ' + r.name
          + '  (' + r.fg + ' on ' + r.bg + (r.parent ? ' over ' + r.parent : '') + ')');
      }
    }
    if (rep.warns.length) {
      console.log('── warn（跳过，不算失败）──');
      for (const w of rep.warns) {
        console.log('  [' + w.file + ':' + w.line + '] ' + w.selector + ' → ' + w.token + '：' + w.reason);
      }
    }
    console.log('contrast_check: pairs=' + rep.pairs + ' failures=' + rep.failures.length
      + ' warns=' + rep.warns.length
      + ' [base=' + PAIRS_670C.length + ' focus-ring=' + FOCUS_RING_PAIRS.length
      + ' auto=' + (rep.pairs - PAIRS_670C.length - FOCUS_RING_PAIRS.length) + ']'
      + ' sources=' + sources.map((s) => s.file).join(','));
  }
  process.exit(rep.ok ? 0 : 1);
}
