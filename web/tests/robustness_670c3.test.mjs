// 670c3 · 前端健壮性测试（纯 Node，无 jsdom 依赖 ⇒ 始终可跑）
// 覆盖：noscript 覆盖/体积、robustness.css 链接、全局兜底注入、robustness_core 纯逻辑。
// 运行：node tests/robustness_670c3.test.mjs
import assert from 'node:assert/strict';
import { readFileSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

import {
  RETRY_MAX, RETRY_DELAY_MS, shouldRetry, retryDelayMs, classifyPayload,
  friendlyError, classifyFetchError, emptyModel, formatMetric, exhaustedHint, noscriptHtml,
} from '../js/robustness_core.js';

const dir = new URL('../', import.meta.url);
const PAGES = ['index', 'cards', 'learn', 'experiments', 'verdicts', 'starmap', 'verify', 'card'];
const read = (p) => readFileSync(new URL(p, dir), 'utf8');

let n = 0;
const ok = (cond, msg) => { assert.ok(cond, msg); n++; };
const eq = (a, b, msg) => { assert.equal(a, b, msg); n++; };

/* ── A. noscript 覆盖 8/8 ── */
for (const p of PAGES) {
  const html = read(`${p}.html`);
  ok(/<noscript>[\s\S]*?<\/noscript>/.test(html), `${p}.html 含 <noscript> 块`);
}

/* ── B. noscript 体积 ≤ 500 字节/页（E2） ── */
for (const p of PAGES) {
  const html = read(`${p}.html`);
  const m = html.match(/<noscript>[\s\S]*?<\/noscript>/);
  ok(m && Buffer.byteLength(m[0], 'utf8') <= 500, `${p}.html noscript ≤500B（实 ${m ? Buffer.byteLength(m[0], 'utf8') : 'N/A'}）`);
}

/* ── C. robustness.css 已链接 + 关键类存在 ── */
for (const p of PAGES) {
  ok(read(`${p}.html`).includes('css/robustness.css'), `${p}.html 链接 robustness.css`);
}
const css = read('css/robustness.css');
for (const cls of ['.qy-skeleton', '.qy-error-card', '.qy-empty', '.qy-banner', '.ns-fallback', 'prefers-reduced-motion']) {
  ok(css.includes(cls), `robustness.css 含 ${cls}`);
}
ok(Buffer.byteLength(css, 'utf8') <= 4096, 'robustness.css ≤4KB（E2 skeleton≤2KB）');

/* ── D. 全局兜底注入 8/8 ── */
for (const p of PAGES) {
  ok(read(`${p}.html`).includes('initRobustness'), `${p}.html 注入 initRobustness`);
}

/* ── E. index 骨架屏 ── */
const idx = read('index.html');
ok(idx.includes('qy-skeleton'), 'index 含 skeleton 类');
ok(/id="metrics"[^>]*data-qy-state="loading"/.test(idx), 'index #metrics 初始 loading 态');

/* ── F. robustness_core 纯逻辑 ── */
eq(RETRY_MAX, 3, 'RETRY_MAX = 3');
eq(RETRY_DELAY_MS, 1000, 'RETRY_DELAY_MS = 1000');
ok(shouldRetry(1), 'shouldRetry(1) = true');
ok(shouldRetry(2), 'shouldRetry(2) = true');
ok(!shouldRetry(3), 'shouldRetry(3) = false（已到上限）');
ok(!shouldRetry(0), 'shouldRetry(0) = false');
eq(retryDelayMs(1), 1000, 'retryDelayMs(1) = 1000');

eq(classifyPayload(null, []).state, 'empty', 'null → empty');
eq(classifyPayload({}, []).state, 'empty', '空对象 → empty');
eq(classifyPayload({ a: 1 }, ['a']).state, 'ok', '字段齐 → ok');
eq(classifyPayload({}, ['metrics']).state, 'empty', '缺必需字段 → empty');
ok(classifyPayload({ b: 1 }, ['a']).missing.includes('a'), 'missing 列出缺失字段');

eq(friendlyError('network').retry, true, 'network 可重试');
eq(friendlyError('missing').title, '数据文件缺失', 'missing 文案');
eq(friendlyError('parse').title, '数据格式异常', 'parse 文案');
eq(friendlyError('unknown').retry, false, 'unknown 不重试');
ok(friendlyError('http').title.length > 0, 'http 有文案');

eq(classifyFetchError(new Error('Failed to fetch')), 'network', 'Failed to fetch → network');
eq(classifyFetchError(new Error('HTTP 404')), 'missing', 'HTTP 404 → missing');
eq(classifyFetchError(new Error('Unexpected token < in JSON')), 'parse', 'JSON 解析错 → parse');

eq(emptyModel('no-commits').text, '暂无提交记录', 'no-commits 文案');
eq(emptyModel('no-match').text, '无匹配项', 'no-match 文案');
ok(emptyModel('whatever').text.length > 0, '未知 kind 有默认模型');

eq(formatMetric(0), '--', '0 → --（不误导）');
eq(formatMetric(null), '--', 'null → --');
eq(formatMetric(87.5), '87.5', '正常值原样');
eq(formatMetric(42), '42', '整数原样');

ok(exhaustedHint().includes('http.server'), '三次失败提示含启动本地服务器命令');

const ns = noscriptHtml({ title: 'T', lines: ['a', 'b'] });
ok(ns.startsWith('<noscript>') && ns.includes('<h1>T</h1>'), 'noscriptHtml 结构正确');

console.log(`robustness_670c3: ${n} 断言全绿`);
