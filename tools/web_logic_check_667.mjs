// 667 阶段2 · 前端纯逻辑**真求值**（Node 直接 import web/verdicts_core.js，不用浏览器）。
//
// 为什么存在：666 的教训是"改了代码没重跑落盘"。前端最容易出现同类事故的地方是
// "渲染时才算的筛选/排序/取值逻辑"——没人测就静默错。这里把纯逻辑拉到 Node 里断言，
// 并把 **真实数据文件** 也一起验（不是只测玩具输入）。
//
// 用法：node tools/web_logic_check_667.mjs
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

import {
  sortRows, filterRows, fmtNum, dashCells, STATE_ORDER, KIND_LABEL, SORTABLE,
} from '../web/verdicts_core.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');

let pass = 0, fail = 0;
function ok(name, cond, extra = '') {
  if (cond) { pass++; console.log(`  [ok]   ${name}${extra ? ' · ' + extra : ''}`); }
  else { fail++; console.log(`  [FAIL] ${name}${extra ? ' · ' + extra : ''}`); }
}

// ── 1. 纯逻辑（合成输入）──────────────────────────────────────────────────
const ROWS = [
  { id: 'b', when: '2026-09-28', state: 'fail', source: 's1', detail: 'beta', detector: 'asan', verdict: 'miss' },
  { id: 'a', when: '2026-09-29', state: 'pass', source: 's2', detail: 'alpha', detector: 'ubsan', verdict: 'catch' },
  { id: 'c', when: '2026-09-29', state: 'unknown', source: 's1', detail: 'gamma', detector: 'gate', verdict: 'unknown' },
];

ok('时间倒序：最新在第一个', sortRows(ROWS, 'when', 'desc')[0].id === 'a',
  sortRows(ROWS, 'when', 'desc').map((r) => r.id).join('>'));
ok('时间升序：最旧在第一个', sortRows(ROWS, 'when', 'asc')[0].id === 'b');
ok('状态排序按 STATE_ORDER（fail 最坏）',
  sortRows(ROWS, 'state', 'desc')[0].state === 'fail');
ok('同值稳定：按 id 兜底',
  sortRows(ROWS, 'when', 'desc').map((r) => r.id).join('>') === 'a>c>b');
ok('未知排序键 ⇒ 原样返回（不静默假装排过）',
  sortRows(ROWS, 'nope', 'desc').map((r) => r.id).join('>') === 'b>a>c');
ok('SORTABLE 不含未知键', SORTABLE.includes('when') && !SORTABLE.includes('nope'));

ok('筛选：状态精确匹配', filterRows(ROWS, { state: 'fail' }).length === 1);
ok('筛选：来源精确匹配', filterRows(ROWS, { source: 's1' }).length === 2);
ok('筛选：搜索命中 detail 小写', filterRows(ROWS, { q: 'ALPHA' }).length === 1);
ok('筛选：搜索命中 detector', filterRows(ROWS, { q: 'ubsan' }).length === 1);
ok('筛选：空条件 = 全量', filterRows(ROWS).length === 3);
ok('筛选 + 排序可组合',
  filterRows(ROWS, { source: 's1' }).length === 2
  && sortRows(filterRows(ROWS, { source: 's1' }), 'id', 'asc')[0].id === 'b');

ok('fmtNum：整数千分位', fmtNum(1234567) === '1,234,567', fmtNum(1234567));
ok('fmtNum：小数位保留', fmtNum(0.0711, 4) === '0.0711', fmtNum(0.0711, 4));
ok('fmtNum：null ⇒ —（不用 0 冒充）', fmtNum(null) === '—');
ok('fmtNum：undefined ⇒ —', fmtNum(undefined) === '—');

// ── 2. 真实数据（web/data/verdicts_667.json）──────────────────────────────
let D = null;
try {
  D = JSON.parse(readFileSync(join(ROOT, 'web/data/verdicts_667.json'), 'utf8'));
} catch (e) {
  ok('读取 web/data/verdicts_667.json', false, String(e && e.message));
}

if (D) {
  const rows = D.verdicts || [];
  ok('判决历史非空', rows.length > 0, `${rows.length} 条`);
  ok('工具已按时间倒序落盘',
    rows.every((r, i) => i === 0 || rows[i - 1].when >= r.when));
  ok('每条都有四态且在 STATE_ORDER 里',
    rows.every((r) => Object.prototype.hasOwnProperty.call(STATE_ORDER, r.state)),
    `${new Set(rows.map((r) => r.state)).size} 种`);
  ok('每条都有复算命令', rows.every((r) => typeof r.repro === 'string' && r.repro.length > 0));

  const cells = dashCells(D.dashboard, D.verdicts_total);
  ok('仪表盘单元格 ≥ 8', cells.length >= 8, `${cells.length} 个`);
  ok('仪表盘无 undefined 数字（缺失必须走 fmtNum 的 —）',
    cells.every((c) => c.num !== undefined),
    cells.filter((c) => c.num === undefined).map((c) => c.key).join(',') || '无');
  // 668：不变量 —— **有漂移就必须标 bad；没漂移就不许标 bad**（不是"必须永远有漂移"）
  ok('仪表盘的 bad 标记与漂移状态一致（不变量）',
    cells.find((c) => c.key === 'holdout')?.bad === (D.dashboard?.holdout?.drift ? 1 : 0),
    `drift=${D.dashboard?.holdout?.drift}`);
  ok('外部语料两个分母都给了',
    D.dashboard?.external?.rate_pct != null && D.dashboard?.external?.rate_pct_all != null,
    `${D.dashboard?.external?.rate_pct} / ${D.dashboard?.external?.rate_pct_all}`);
  ok('对比表非空', (D.compare || []).length > 0, `${(D.compare || []).length} 行`);
  ok('对比表每行都有性质与说明',
    (D.compare || []).every((r) => KIND_LABEL[r.kind] && r.note));
  ok('excluded 已登记（不假装全量）', (D.excluded || []).length > 0, `${(D.excluded || []).length} 条`);
  // 668：漂移是**关系**不是常量 —— 修好之后漂移可以（也应该）为空。
  // 断言改成不变量：落盘率与现算率不一致 ⇒ 必须有一条 drift 说明它。
  const h = D.dashboard?.holdout || {};
  ok('漂移是关系：不一致就必须登记',
    h.stored_rate_pct === undefined || (h.drift === (h.stored_rate_pct !== h.rate_pct)),
    `stored=${h.stored_rate_pct} fresh=${h.rate_pct} drift=${h.drift}`);
  ok('漂移项都带 field/stored/fresh/note',
    (D.drift || []).every((d) => d.field && d.stored !== undefined && d.fresh !== undefined && d.note));
}

console.log(`[667 web-logic] ${fail === 0 ? 'PASS' : 'FAIL'} · ${pass} passed / ${fail} failed`);
process.exit(fail === 0 ? 0 : 1);
