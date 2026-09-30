// 670c5 · 性能 + dist 构建测试（纯 Node）
// 运行：node tests/perf_670c5.test.mjs
import assert from 'node:assert/strict';
import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = new URL('../', import.meta.url);
const webDir = fileURLToPath(dir);
const PAGES = ['index', 'cards', 'learn', 'experiments', 'verdicts', 'starmap', 'verify', 'card'];
const read = (p) => readFileSync(new URL(p, dir), 'utf8');

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
  ok(!/(src|href)="https?:\/\//.test(h), `${p}: 无外部 http(s) 依赖`);
  ok(!/\bdebugger\b/.test(h), `${p}: 无 debugger 残留`);
  ok(h.split('</head>')[0].includes('rel="stylesheet"'), `${p}: CSS 在 head`);
  // 脚本均为 module（延迟执行）
  const scripts = [...h.matchAll(/<script([^>]*)>/g)].map((m) => m[1]);
  ok(scripts.every((s) => s.includes('type="module"')), `${p}: 所有 <script> 为 module`);
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
