// 670c5 · 性能 + dist 构建测试（纯 Node）
// 运行：node tests/perf_670c5.test.mjs
import assert from 'node:assert/strict';
import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { gzipSync } from 'node:zlib';
import { fileURLToPath } from 'node:url';

const dir = new URL('../', import.meta.url);
const webDir = fileURLToPath(dir);
const PAGES = ['index', 'cards', 'learn', 'experiments', 'verdicts', 'starmap', 'verify', 'card'];
const read = (p) => readFileSync(new URL(p, dir), 'utf8');

/* ── 672d B · 加载时资源 vs 导航链接（与 tools/perf_audit_670c5.py 同一口径）──
 * <a href> 是点一下才下载的导航链接，不属于首屏；只有 link/script/img 才是加载时资源。 */
const LOAD_TAGS_RE = /<(link|script|img)\b([^>]*)>/gi;
const NAV_A_RE = /<a\b([^>]*)>/gi;
const ATTR_RE = /(?:src|href)\s*=\s*"([^"]+)"/;
const REL_RE = /rel\s*=\s*"([^"]+)"/;
const LOADABLE_REL = new Set(['stylesheet', 'icon', 'shortcut', 'apple-touch-icon',
  'manifest', 'preload', 'modulepreload', 'mask-icon']);
const EXTERNAL = /^(https?:|\/\/|data:|#|mailto:)/;

function loadRefs(html, includeExternal = false) {
  const out = [];
  for (const m of html.matchAll(LOAD_TAGS_RE)) {
    const tag = m[1].toLowerCase();
    const attrs = m[2];
    if (tag === 'link') {
      const rel = REL_RE.exec(attrs);
      const rels = (rel ? rel[1].toLowerCase().split(/\s+/) : []);
      if (!rels.some((r) => LOADABLE_REL.has(r))) continue;
    }
    const a = ATTR_RE.exec(attrs);
    if (!a) continue;
    const r = a[1];
    if (EXTERNAL.test(r) && !(includeExternal && /^https?:/.test(r))) continue;
    out.push(r);
  }
  return out;
}
const navRefs = (html) => [...html.matchAll(NAV_A_RE)]
  .map((m) => (ATTR_RE.exec(m[1]) || [])[1])
  .filter((r) => r && !EXTERNAL.test(r));

let n = 0;
const ok = (c, m) => { assert.ok(c, m); n++; };
const eq = (a, b, m) => { assert.equal(a, b, m); n++; };

/* ── B3 · 性能（≥20）── */
const BUDGET_HTML_KB = 60, BUDGET_DOM = 1500;
for (const p of PAGES) {
  const h = read(`${p}.html`);
  const kb = Buffer.byteLength(h, 'utf8') / 1024;
  ok(kb <= BUDGET_HTML_KB, `${p}: HTML ${kb.toFixed(1)}KB ≤ ${BUDGET_HTML_KB}KB`);
  const dom = (h.match(/<[a-zA-Z][a-zA-Z0-9-]*/g) || []).length;
  ok(dom <= BUDGET_DOM, `${p}: DOM 标签 ${dom} ≤ ${BUDGET_DOM}`);
  // 672d：只判**加载时**外部资源；`<a href="https://github.com/…">` 引用链接不算依赖
  ok(loadRefs(h, true).filter((r) => /^https?:/.test(r)).length === 0,
    `${p}: 无外部 http(s) 加载资源（导航/引用链接不算）`);
  ok(!/\bdebugger\b/.test(h), `${p}: 无 debugger 残留`);
  ok(h.split('</head>')[0].includes('rel="stylesheet"'), `${p}: CSS 在 head`);
  // 脚本均为 module（延迟执行）
  const scripts = [...h.matchAll(/<script([^>]*)>/g)].map((m) => m[1]);
  ok(scripts.every((s) => s.includes('type="module"')), `${p}: 所有 <script> 为 module`);
}

/* ── 672d B · 首屏 gzip 口径：只算加载时资源，预算不放松 ── */
const HOME_GZIP_BUDGET_KB = 120;   // 与 tools/perf_audit_670c5.py 的 BUDGET_HOME_GZIP_KB 保持一致
{
  const h = read('index.html');
  const load = loadRefs(h);
  const nav = navRefs(h);
  ok(nav.length > 0, '首页确有导航链接（口径修正才有意义）');
  ok(nav.some((r) => /\.json$/.test(r)), '首页导航链指向 .json 数据文件（旧口径会误计入）');
  ok(!load.some((r) => /\.json$/.test(r)), '首屏加载资源不含 .json（导航链接已剔除）');
  ok(!load.some((r) => nav.includes(r)), '加载时资源与导航链接互不重叠');
  const gzOf = (rel) => {
    const p = join(webDir, rel.split('?')[0]);
    return existsSync(p) ? gzipSync(readFileSync(p)).length : 0;
  };
  const htmlGz = gzipSync(Buffer.from(h, 'utf8')).length;
  const gzKb = (htmlGz + load.reduce((s, r) => s + gzOf(r), 0)) / 1024;
  const legacyKb = (htmlGz + [...load, ...nav].reduce((s, r) => s + gzOf(r), 0)) / 1024;
  ok(gzKb <= HOME_GZIP_BUDGET_KB, `首页首屏 gzip ${gzKb.toFixed(1)}KB ≤ ${HOME_GZIP_BUDGET_KB}KB`);
  ok(gzKb < legacyKb, `新口径 ${gzKb.toFixed(1)}KB < 旧口径 ${legacyKb.toFixed(1)}KB（剔除了导航链接）`);
  eq(HOME_GZIP_BUDGET_KB, 120, '预算仍是 120KB（口径修正不得顺手放松标准）');
}

// 关键资源：我的 JS 无 console.log / debugger
for (const f of ['js/a11y.js', 'js/a11y_core.js', 'js/keybind.js', 'js/robustness.js', 'js/robustness_core.js']) {
  const t = read(f);
  ok(!/\bdebugger\b/.test(t), `${f}: 无 debugger`);
  ok(!/console\.log\(/.test(t), `${f}: 无 console.log`);
}

/* ── D3 · dist 构建（≥5）── */
const distDir = join(webDir, 'dist');
if (existsSync(distDir)) {
  for (const p of PAGES) ok(existsSync(join(distDir, `${p}.html`)), `dist 含 ${p}.html`);
  ok(existsSync(join(distDir, 'home.js')), 'dist 含 home.js（670c2 修过的坑）');
  ok(existsSync(join(distDir, 'css', 'a11y.css')), 'dist 含 css/a11y.css');
  ok(existsSync(join(distDir, 'css', 'responsive.css')), 'dist 含 css/responsive.css');
  ok(existsSync(join(distDir, 'js', 'a11y.js')), 'dist 含 js/a11y.js');
  ok(existsSync(join(distDir, 'js', 'keybind.js')), 'dist 含 js/keybind.js');
  // 引用 0 缺失
  let missing = 0;
  for (const p of PAGES) {
    const h = readFileSync(join(distDir, `${p}.html`), 'utf8');
    for (const m of h.matchAll(/(?:src|href)="([^"]+)"/g)) {
      const r = m[1];
      if (/^(https?:|\/\/|data:|#|mailto:)/.test(r)) continue;
      if (!existsSync(join(distDir, r.split('?')[0].split('#')[0]))) missing++;
    }
  }
  eq(missing, 0, 'dist 引用资源 0 缺失');
  const idxKb = statSync(join(distDir, 'index.html')).size / 1024;
  ok(idxKb <= 60, `dist/index.html ${idxKb.toFixed(1)}KB ≤ 60KB`);
} else {
  console.log('perf_670c5: 跳过 dist 断言（先跑 node web/build.mjs）');
}

console.log(`perf_670c5: ${n} 断言全绿`);
