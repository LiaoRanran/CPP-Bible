// 672b · 数据层单点测试（纯 Node，无 jsdom 依赖 ⇒ 始终可跑）
// 覆盖 web/js/data.js：formatMetric / pct / esc / fetchJSON（重试 / 超时 / 缓存）。
// 运行：node tests/data_672b.test.mjs
import assert from 'node:assert/strict';

import { fetchJSON, esc, formatMetric, pct } from '../js/data.js';

const origFetch = globalThis.fetch;
let n = 0;
const ok = (c, m) => { assert.ok(c, m); n++; };
const eq = (a, b, m) => { assert.equal(a, b, m); n++; };

const fakeRes = (body, { ok = true, status = 200 } = {}) => ({
  ok, status,
  json: async () => (typeof body === 'string' ? JSON.parse(body) : body),
});

/* ── A. formatMetric：缺失 ≠ 0 ── */
eq(formatMetric(null), '--', 'null → --');
eq(formatMetric(undefined), '--', 'undefined → --');
eq(formatMetric(''), '--', "'' → --（空串视为取不到）");
eq(formatMetric(0), '0', '0 → 0（不再把真 0 撒谎成 --）');
eq(formatMetric(87.5), '87.5', '正常值原样');
eq(formatMetric(42), '42', '整数原样');

/* ── B. pct ── */
eq(pct(null), '--', 'pct(null) → --');
eq(pct(0), '0%', 'pct(0) → 0%');
eq(pct(87.5), '87.5%', 'pct(87.5) → 87.5%');

/* ── C. esc：HTML 卫生 ── */
eq(esc('a&b<c>d"e'), 'a&amp;b&lt;c&gt;d&quot;e', 'esc 转义 & < > "');
eq(esc(null), '', 'esc(null) → 空串');
eq(esc(0), '0', 'esc(0) → "0"');

/* ── D. fetchJSON：成功 + JSON 解析 ── */
globalThis.fetch = async () => fakeRes({ hello: 1 });
const d1 = await fetchJSON('d1.json');
eq(d1.hello, 1, 'fetchJSON 解析 JSON');

/* ── E. fetchJSON：页内 Map 缓存（同 URL 只取一次）── */
let calls = 0;
globalThis.fetch = async () => { calls++; return fakeRes({ a: 2 }); };
const c1 = await fetchJSON('cache.json');
const c2 = await fetchJSON('cache.json');
eq(c1.a, 2, 'cached 第一次');
eq(c2.a, 2, 'cached 第二次');
eq(calls, 1, '页内缓存：同 URL 只取一次');

/* ── F. fetchJSON：失败重试，第 3 次成功 ── */
let attempts = 0;
globalThis.fetch = async () => { attempts++; if (attempts < 3) throw new Error('net down'); return fakeRes({ ok: 1 }); };
const r = await fetchJSON('retry.json', { retries: 3, retryDelay: 1, timeout: 1000 });
eq(r.ok, 1, '重试后成功');
eq(attempts, 3, '重试 3 次后第 3 次成功（2 次重试）');

/* ── G. fetchJSON：HTTP 非 2xx 抛错带状态码 ── */
globalThis.fetch = async () => fakeRes({}, { ok: false, status: 404 });
let httpThrew = false;
try { await fetchJSON('missing.json'); } catch (e) { httpThrew = true; ok(/404/.test(e.message), 'HTTP 404 抛错带状态码'); }
ok(httpThrew, 'HTTP 非 2xx 抛错');

/* ── H. fetchJSON：超时触发 AbortController ── */
let aborted = false;
globalThis.fetch = async (url, opts) => new Promise((resolve, reject) => {
  opts.signal.addEventListener('abort', () => { aborted = true; reject(new Error('aborted')); });
});
let toThrew = false;
try { await fetchJSON('timeout.json', { retries: 0, timeout: 50 }); }
catch { toThrew = true; }
ok(toThrew, '超时后抛错');
ok(aborted, '超时触发 AbortController.abort');

/* 还原全局 fetch，避免影响其它测试进程 */
globalThis.fetch = origFetch;

console.log(`data_672b: ${n} 断言全绿`);
