// 667 阶段2 · 前端 **jsdom 真跑 DOM** 冒烟（不是静态 grep，是真的把页面跑起来）。
//
// 诚实边界（先写在最前面）：
//   · 本机 Node 若 < 20 或 jsdom 不可用 ⇒ 本脚本**打印 SKIP 并 exit 0**，
//     **不把 SKIP 当 PASS**。谁跑出来是 SKIP，验收报告里就得写 SKIP。
//   · 星图页依赖 canvas/WebGL，jsdom 里 `getContext` 返回 null ⇒ **不在这里验星图**；
//     星图的纯逻辑走 `tools/web_logic_check_667.mjs`，交互走人工 30 秒复核（见 docs/667_frontend.md）。
//   · 这里只跑**判决页**的真实渲染路径：取数据 → 渲染仪表盘/表格/对比表 → 筛选 → 排序 → 空状态。
//
// 用法：node tools/web_smoke_667.mjs
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');

let pass = 0, fail = 0;
function ok(name, cond, extra = '') {
  if (cond) { pass++; console.log(`  [ok]   ${name}${extra ? ' · ' + extra : ''}`); }
  else { fail++; console.log(`  [FAIL] ${name}${extra ? ' · ' + extra : ''}`); }
}

// ── 0. 环境探测（不可用就诚实 SKIP，不伪造绿）────────────────────────────
const major = Number(process.versions.node.split('.')[0]);
let JSDOM = null;
try {
  JSDOM = (await import('jsdom')).JSDOM;
} catch (e) {
  console.log(`[667 web-smoke] SKIP · jsdom 不可用（${String(e && e.message).slice(0, 120)}）`);
  console.log(`                Node ${process.versions.node}；655 已记录：本机 Node18 与 jsdom 的 ESM 依赖不兼容。`);
  console.log('                ⇒ 本项**不算通过**，请以人工浏览器复核替代（见 docs/667_frontend.md §5）。');
  process.exit(0);
}
if (major < 20) {
  console.log(`[667 web-smoke] 提示：Node ${process.versions.node} < 20，jsdom 可能加载失败；若失败按 SKIP 处理。`);
}

// ── 1. 起 DOM ─────────────────────────────────────────────────────────────
const html = readFileSync(join(ROOT, 'web/verdicts.html'), 'utf8');
const data = JSON.parse(readFileSync(join(ROOT, 'web/data/verdicts_667.json'), 'utf8'));

const dom = new JSDOM(html, { url: 'http://localhost:8765/verdicts.html', pretendToBeVisual: false });
const { window } = dom;
globalThis.window = window;
globalThis.document = window.document;
globalThis.performance = window.performance ?? globalThis.performance;
// 走 reduced-motion 分支：顺带验证"关动效时数字也要正确落地"
window.matchMedia = () => ({ matches: true, addEventListener() {}, removeEventListener() {} });
globalThis.matchMedia = window.matchMedia;
// 静态站靠 fetch 取 JSON：这里把它接到本地文件（**不联网**）
const fetched = [];
globalThis.fetch = async (url) => {
  fetched.push(String(url));
  const rel = String(url).replace(/^https?:\/\/[^/]+\//, '');
  if (rel.includes('verdicts_667.json')) {
    return { ok: true, json: async () => data };
  }
  return { ok: false, status: 404, json: async () => ({}) };
};
window.fetch = globalThis.fetch;

// ── 2. 真跑页面模块 ───────────────────────────────────────────────────────
await import('../web/verdicts.js');
await new Promise((r) => setTimeout(r, 60));   // 等一次 microtask/渲染

const hooks = window.__verdicts_hooks;
ok('页面模块已挂载钩子', !!hooks);
if (!hooks) {
  console.log(`[667 web-smoke] FAIL · 未拿到 window.__verdicts_hooks`);
  process.exit(1);
}
ok('数据已就绪', hooks.ready() === true);
ok('确实发起了 data/verdicts_667.json 请求',
  fetched.some((u) => u.includes('verdicts_667.json')), fetched.join(','));
ok('判决历史条数 = 数据文件里的条数', hooks.total() === (data.verdicts || []).length,
  `${hooks.total()} vs ${(data.verdicts || []).length}`);

// ── 3. 渲染结果（DOM 里真的有东西）────────────────────────────────────────
const doc = window.document;
const rowsRendered = doc.querySelectorAll('#vt-body tr').length;
ok('表格渲染出行', rowsRendered === data.verdicts.length, `${rowsRendered} 行`);
ok('仪表盘渲染出单元格', doc.querySelectorAll('#dash .cell').length >= 8,
  `${doc.querySelectorAll('#dash .cell').length} 个`);
ok('reduced-motion 下数字**立即写终值**（不是停在 0）',
  (doc.querySelector('#dash .d-num')?.textContent || '').trim() !== '0');
// 668：漂移是**关系**不是常量 —— 修好后可以为空。有则必须渲染，无则必须不渲染（不许挂空卡片）。
const driftN = (data.drift || []).length;
ok(`漂移登记与渲染一致（当前 ${driftN} 项）`,
  driftN === 0
    ? (doc.getElementById('drift-box')?.textContent || '').trim() === ''
    : (doc.getElementById('drift-box')?.textContent || '').includes('漂移'));
ok('对比表渲染出行', doc.querySelectorAll('#ct-body tr').length === (data.compare || []).length,
  `${doc.querySelectorAll('#ct-body tr').length} 行`);
ok('excluded 已渲染（诚实登记）', doc.querySelectorAll('#excluded li').length > 0,
  `${doc.querySelectorAll('#excluded li').length} 条`);
ok('状态色标带 data-state（不是只靠颜色）',
  doc.querySelectorAll('#vt-body .state-pill[data-state]').length > 0,
  `${doc.querySelectorAll('#vt-body .state-pill[data-state]').length} 个`);
ok('来源下拉已按数据填充',
  doc.querySelectorAll('#f-source option').length >= 2,
  `${doc.querySelectorAll('#f-source option').length} 项`);

// ── 4. 交互：筛选 / 排序 / 空状态 ─────────────────────────────────────────
const before = hooks.visibleIds().length;
hooks.setView({ state: 'fail' });
const afterFail = hooks.visibleIds();
ok('按状态筛选生效', afterFail.length <= before, `${before} → ${afterFail.length}`);
ok('筛选后 DOM 行数跟着变',
  doc.querySelectorAll('#vt-body tr').length === afterFail.length);

hooks.setView({ state: 'all', q: 'ubsan' });
const byQ = hooks.visibleIds();
ok('搜索筛选生效', byQ.length > 0 && byQ.length < before, `${byQ.length} 条命中 ubsan`);

hooks.setView({ q: '__绝不可能存在的关键词__' });
ok('空结果时**显示空状态**（不是空白表格）',
  doc.querySelectorAll('#vt-body tr').length === 0
  && (doc.getElementById('vt-empty')?.textContent || '').includes('没有匹配的判决记录'));
ok('空状态里给了下一步（重置 / 命令）',
  (doc.getElementById('vt-empty')?.textContent || '').includes('重置筛选'));

hooks.setView({ q: '', state: 'all', key: 'id', dir: 'asc' });
const asc = hooks.visibleIds();
ok('排序切到 id 升序生效',
  asc.length === before && asc.join(',') === [...asc].sort((a, b) => String(a).localeCompare(String(b))).join(','),
  asc.slice(0, 3).join(','));

// ── 5. 无障碍静态项（能自动验的部分）──────────────────────────────────────
ok('有跳转链接', !!doc.querySelector('a.skip-link'));
ok('表格有 <caption> 供屏幕阅读器', doc.querySelectorAll('table caption').length >= 2);
ok('结果计数用 role=status + aria-live',
  doc.getElementById('count')?.getAttribute('role') === 'status');
ok('所有表头排序按钮是 <button>（键盘可达）',
  [...doc.querySelectorAll('#vt thead .th-btn')].every((b) => b.tagName === 'BUTTON'));
ok('搜索框有 <label for>', !!doc.querySelector('label[for="q"]'));

console.log(`[667 web-smoke] ${fail === 0 ? 'PASS' : 'FAIL'} · ${pass} passed / ${fail} failed`);
process.exit(fail === 0 ? 0 : 1);
