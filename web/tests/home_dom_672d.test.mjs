// 672d D · 首页 DOM 渲染校验（jsdom + mock fetch，**真执行 home.js**）
//
// 病（P3 批判）：没有任何测试校验首页 JS 渲染后的 DOM —— home.js 渲染了什么全靠人眼看。
// 本测试把 home.js 在 jsdom 里真跑一遍（mock fetch 提供可控数据），断言：
//   · 指标数字来自 mock 数据（只渲染，不写死）；
//   · `--`（取不到）与 `0`（真零）严格区分；
//   · 所有动态文本都过 esc（注入 <img onerror> / <b> 探针，断言不产生元素）；
//   · 时间线只取最近 5 条且新的在上；提交列表完整；
//   · 渲染全程无控制台错误；空数据 / 取数失败两个降级路径都渲染正确的兜底 UI。
//
// 结构依赖：绑定 672c 重制后的首页（#ab-* / #metrics / #timeline / #commits）。
// 672c 若再改结构，本测试会红 —— 这是**故意的**（结构变了就该同步更新测试），不是脆弱。
// 已知问题锁：#metrics 渲染完成后 aria-busy="true" 残留（672d-C 的发现，归 672e 修）。
// 若 robustness.js 修了 setState，请把该断言同步改为"aria-busy 已清"。
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

let JSDOM;
try {
  ({ JSDOM } = await import('jsdom'));
} catch {
  console.log('home_dom_672d: 跳过（jsdom 未安装，npm i -D jsdom 后重跑）');
  process.exit(0);
}

const dir = new URL('../', import.meta.url);
const HTML = readFileSync(new URL('index.html', dir), 'utf8');

let n = 0;
const ok = (c, m) => { assert.ok(c, m); n++; };
const eq = (a, b, m) => { assert.equal(a, b, m); n++; };

/** 构造可控的 metrics 数据（字段名与 tools/web_metrics_666.py 的产物对齐）。 */
function mockPayload() {
  return {
    generated_at: '2026-10-01T12:00:00+08:00',
    metrics: {
      holdout: {
        rate_pct: 42.9, catch: 3, den: 7, miss: 4, unknown: 2,
        opt_levels: ['L1', 'L2'], env: 'windows-test',
        cmd: 'python tools/holdout.py --tag "<b>bold</b>"',   // XSS 探针
      },
      external: {
        rate_pct: 33.3, rate_pct_all: 30, catch: 2, den: 6, total: 10,
        denominator: { excluded: { '无 ground_truth': 4 } },
        cmd: 'python tools/external.py',
      },
      counterfactual: { p: 0.5, r: 0.7, f1: 0.6, cases: 8, third_criterion_hits: 1, cmd: 'python tools/cf.py' },
      cards_real: 0,            // 真 0：必须显示 "0"，不许吞成 "--"
      cards_draft: null,        // 取不到：必须显示 "--"
      rules_total: 65,
      ledger_events: 1234,      // 千分位
      ledger_path: 'data/ledger.jsonl', ledger_redline: 'append-only',
      transparency_log_entries: 9, merkle_dirs: ['03', '15'], merkle_files: 7,
    },
    timeline: Array.from({ length: 9 }, (_, i) => ({
      state: i % 2 ? 'pass' : 'fail',
      batch: 'batch-' + i,
      date: '2026-09-' + String(10 + i),
      // XSS 探针放在第 9 条（最新，TIMELINE_MAX=5 必渲染）；older 条目不在截断窗口里
      what: i === 8 ? '<img src=x onerror=alert(1)>' : '正常描述 ' + i,
      why: '原因 ' + i,
    })),
    commits: [
      { date: '2026-10-01', hash: 'abc123def4567890', subject: 'subject one' },
      { date: '2026-09-30', hash: 'def456', subject: 'subject two' },
      { date: '2026-09-29', hash: '789abc', subject: 'subject three' },
    ],
  };
}

let caseId = 0;

/** 跑一次 home.js：新 JSDOM + mock fetch，返回渲染后的 document 与控制台错误。 */
async function runHome(payload, { status = 200, settleMs = 120 } = {}) {
  const dom = new JSDOM(HTML, { url: 'http://localhost/index.html' });
  const { window } = dom;
  const consoleErrors = [];
  const urls = [];
  const origErr = console.error;
  console.error = (...a) => consoleErrors.push(a.map((x) => String(x?.message ?? x)).join(' '));
  globalThis.window = window;
  globalThis.document = window.document;
  globalThis.fetch = async (u) => {
    urls.push(String(u));
    if (status !== 200) return { ok: false, status, json: async () => ({}) };
    return { ok: true, status: 200, json: async () => (typeof payload === 'function' ? payload() : payload) };
  };
  try {
    await import(new URL(`../home.js?case=${++caseId}`, import.meta.url).href);
    await new Promise((r) => setTimeout(r, settleMs));
  } finally {
    console.error = origErr;
  }
  return { document: window.document, consoleErrors, urls };
}

/* ── 场景 1：正常数据 ─────────────────────────────────────────── */
{
  const { document: d, consoleErrors, urls } = await runHome(mockPayload());
  const $ = (sel) => d.getElementById(String(sel).replace(/^#/, ''));   // getElementById 不吃 '#'
  const text = (id) => ($(id) ? $(id).textContent : '');

  // ① 摘要区：数字来自 mock，不写死
  eq(text('ab-holdout'), '42.9%', '摘要：盲集检出率来自数据');
  eq(text('ab-holdout-n'), '3/7', '摘要：分子/分母来自数据');
  eq(text('ab-corpus'), '33.3%', '摘要：外部语料检出率');
  eq(text('ab-cards'), '0', '摘要：真 0 显示 "0"（不许吞成 --）');
  eq(text('ab-ledger'), '1,234', '摘要：千分位格式化');
  eq(text('last-updated'), '2026-10-01T12:00:00+08:00', '页脚更新时间来自数据');

  // ② 现状表：结构 + 数值
  const table = d.querySelector('#metrics table.state-table');
  ok(table, '#metrics 渲染出 table.state-table');
  ok(table.querySelector('caption'), 'JS 渲染的表格带 caption（a11y）');
  eq(table.querySelectorAll('thead th').length, 4, '表头 4 列');
  eq(table.querySelectorAll('tbody tr').length, 7, '现状表 7 行');
  ok(table.textContent.includes('42.9%'), '表内出现 42.9%');
  ok(table.textContent.includes('3 / 7'), '表内出现分子/分母 3 / 7');
  ok(table.textContent.includes('0 张'), '真 0 → "0 张"');
  ok(table.textContent.includes('草稿 --'), '缺失 → "草稿 --"（-- 与 0 严格区分）');
  ok(table.textContent.includes('1,234 条'), '账本事件千分位');
  ok(table.textContent.includes('L1 / L2'), '双档口径来自数据');

  // ③ esc：探针字符串必须以**文本**出现，绝不能变成元素
  eq(d.querySelectorAll('#metrics b').length, 0, 'cmd 里的 <b> 未被解释成元素（过了 esc）');
  ok(table.textContent.includes('<b>bold</b>'), '探针字符串以原文出现');
  eq(d.querySelectorAll('img').length, 0, '时间线里的 <img onerror> 探针未变成元素');
  ok(d.querySelector('#timeline').textContent.includes('<img src=x onerror=alert(1)>'),
    'XSS 探针以原文出现（esc 生效）');

  // ④ 时间线：只取最近 5 条，新的在上
  const lis = d.querySelectorAll('#timeline li[data-state]');
  eq(lis.length, 5, '时间线只渲染最近 5 条（TIMELINE_MAX=5，数据有 9 条）');
  ok(lis[0].querySelector('.t-why').textContent.includes('原因 8'),
    '第一条是最新的一条（倒序）');
  eq(lis[0].getAttribute('data-state'), 'fail', 'data-state 来自数据（第 9 条是 fail）');

  // ⑤ 提交列表
  const commits = d.querySelectorAll('#commits .commit-list li');
  eq(commits.length, 3, '提交列表 3 条');
  ok(commits[0].textContent.includes('subject one'), '提交条目含 subject');
  ok(commits[0].querySelector('.kbd'), '提交条目含 hash（.kbd）');

  // ⑥ 状态与数据源
  eq($('#metrics').getAttribute('data-qy-state'), 'ready', '#metrics 状态机到 ready');
  ok(text('metrics-note').includes('windows-test'), '口径注记里的 env 来自数据');
  ok(urls.length >= 1 && urls.every((u) => u === 'data/metrics_666.json'),
    '全部取数都来自唯一数据源（不写死其它路径）');

  // ⑦ aria-busy 清理（672d-C 发现，672e 修：renderMetrics 渲染完成清掉初始 aria-busy="true"）
  eq($('#metrics').getAttribute('aria-busy'), 'false',
    '渲染完成后 aria-busy 已清（home.js 在 ready/empty/error 分支调 clearBusy，672e 修）');

  eq(consoleErrors.length, 0, '正常渲染全程无 console.error');
}

/* ── 场景 2：数据为空 ─────────────────────────────────────────── */
{
  const { document: d } = await runHome({ generated_at: '2026-10-01', metrics: {} });
  const $ = (sel) => d.getElementById(String(sel).replace(/^#/, ''));   // getElementById 不吃 '#'
  ok(d.querySelector('#metrics .qy-empty'), '空数据 → #metrics 渲染空状态');
  ok(d.querySelector('#metrics .qy-empty [role="status"]') ||
     d.querySelector('#metrics .qy-empty')?.getAttribute('role') === 'status', '空状态带 role="status"');
  eq($('#metrics').getAttribute('data-qy-state'), 'empty', '#metrics 状态机到 empty');
  eq(text0(d, 'ab-cards'), '--', '摘要区空数据 → "--"（不是 0）');
  ok(d.querySelector('#timeline .qy-empty'), '时间线空数据 → 空状态');
  ok(d.querySelector('#commits .qy-empty'), '提交空数据 → 空状态');
}

/* ── 场景 3：取数失败（HTTP 404）──────────────────────────────── */
{
  // robustness 的 fetchJSON 对 HTTP 错误也重试 3×1s ⇒ 等它走完再断言
  const { document: d } = await runHome(null, { status: 404, settleMs: 2600 });
  const $ = (sel) => d.getElementById(String(sel).replace(/^#/, ''));   // getElementById 不吃 '#'
  eq($('#metrics').getAttribute('data-qy-state'), 'error', '取数失败 → #metrics 状态机到 error');
  const card = d.querySelector('#metrics .qy-error-card');
  ok(card, '取数失败 → 渲染错误卡');
  eq(card.getAttribute('role'), 'alert', '错误卡 role="alert"');
  ok(card.querySelector('.qy-btn'), '错误卡带重试按钮');
  eq(text0(d, 'ab-cards'), '--', '摘要区失败 → "--"');
  ok(d.querySelector('#timeline').textContent.includes('时间线不可用'), '时间线失败有文字说明（不静默）');
}

function text0(d, id) {
  const el = d.getElementById(id);
  return el ? el.textContent : '';
}

console.log(`home_dom_672d: ${n} 断言全绿`);
