// 672c · 首页重制验收（纯 Node，无 jsdom 依赖）
// 运行：node tests/home_672c.test.mjs
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const dir = new URL('../', import.meta.url);
const read = (p) => readFileSync(new URL(p, dir), 'utf8');

const html = read('index.html');
const home = read('home.js');
const style = read('style.css');
const tokens = read('css/design-tokens.css');

let n = 0;
const ok = (c, m) => { assert.ok(c, m); n++; };
const eq = (a, b, m) => { assert.equal(a, b, m); n++; };

/* ── 1. 无 AI 禁词 ── */
const BANNED = ['赋能', '打造', '一站式', '高效', '革命性', '颠覆', '革新', '重塑', '卓越', '智能化', '瀑布流', '闭环生态'];
for (const w of BANNED) {
  ok(!html.includes(w), `首页 HTML 无禁词「${w}」`);
  ok(!home.includes(w), `home.js 无禁词「${w}」`);
}

/* ── 2. 无硬编码指标数字（全部现算自 metrics_666.json）── */
// 这些值来自上一版 metrics_666.json；首页与 home.js 都不得写死，必须由 JS 注入。
const HARD = ['87.5', '43.8', '81.0', '54.2', '17/21', '26/48',
  '42 张', '67 条', '452 条', '14 / 16', '14/16', '14 / 32', '14/32'];
for (const v of HARD) {
  ok(!html.includes(v), `首页 HTML 未硬编码「${v}」`);
  ok(!home.includes(v), `home.js 未硬编码「${v}」`);
}

/* ── 3. 引用 home.js 与 data.js ── */
ok(html.includes('home.js'), '首页 HTML 引用 home.js');
ok(home.includes("from './js/data.js'"), 'home.js 从 data.js 取数据层（fetchJSON/esc/formatMetric/pct）');

/* ── 4. 最大栏宽 ≤ 720px（学术栏宽）── */
ok(/main\.home,\s*main\.home\s*>\s*\.wrap\s*\{\s*max-width:\s*var\(--wrap-prose\)/.test(style),
  'style.css 把首页栏宽约束为 var(--wrap-prose)');
const m = tokens.match(/--wrap-prose:\s*(\d+)px/);
ok(m && Number(m[1]) <= 720, `令牌 --wrap-prose ≤ 720px（实际 ${m && m[1]}）`);

/* ── 5. 无渐变 / 毛玻璃 / 辉光 / count-up（只查 HTML + home.js）── */
for (const k of ['gradient', 'backdrop-filter', 'blur(', 'box-shadow', 'countUp', 'count-up', 'glow']) {
  ok(!html.includes(k), `首页 HTML 无「${k}」`);
  ok(!home.includes(k), `home.js 无「${k}」`);
}

/* ── 6. 结构要素齐全 ── */
ok(html.includes('id="ab-holdout"'), '首页含摘要占位 ab-holdout（数字现算）');
ok(html.includes('id="ab-ledger"'), '首页含摘要占位 ab-ledger（数字现算）');
ok(html.includes('id="last-updated"'), '页脚含最后更新时间占位（来自 generated_at）');
ok(html.includes('class="flow"') && html.includes('断言') && html.includes('演化'), '首页含纯 SVG 架构图（断言→证据→判决→账本→演化）');
ok(home.includes('state-table'), '首页含三线表（核心指标，由 home.js 注入）');
ok(html.includes('initKeybinds'), '首页接线 initKeybinds');

console.log(`home_672c: ${n} 断言全绿`);
