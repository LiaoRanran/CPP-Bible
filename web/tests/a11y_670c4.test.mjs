// 670c4 · 可访问性测试（纯 Node；DOM 部分依赖 jsdom，缺失则跳过并标注）
// 覆盖：a11y_core 纯逻辑 + 8 页面静态结构 + a11y_audit 审计产物。
// 运行：node tests/a11y_670c4.test.mjs
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';

import {
  NAV_MAP, HELP_ITEMS, normalizeKey, isTypingTarget, resolveChord, cycleIndex,
  announceResults, announceRating, shouldCloseOnEsc,
} from '../js/a11y_core.js';

const dir = new URL('../', import.meta.url);
const root = new URL('../../', import.meta.url);
const PAGES = ['index', 'cards', 'learn', 'experiments', 'verdicts', 'starmap', 'verify', 'card'];
const read = (p) => readFileSync(new URL(p, dir), 'utf8');

let n = 0;
const ok = (c, m) => { assert.ok(c, m); n++; };
const eq = (a, b, m) => { assert.equal(a, b, m); n++; };

/* ── 1. 快捷键映射与帮助 ── */
eq(Object.keys(NAV_MAP).length, 6, 'NAV_MAP 有 6 个 g+ 目标');
eq(NAV_MAP.h, 'index.html', 'g+h → 首页');
eq(NAV_MAP.c, 'cards.html', 'g+c → 卡库');
eq(NAV_MAP.l, 'learn.html', 'g+l → 学习台');
eq(NAV_MAP.e, 'experiments.html', 'g+e → 实验');
eq(NAV_MAP.v, 'verdicts.html', 'g+v → 判决');
eq(NAV_MAP.s, 'starmap.html', 'g+s → 星图');
ok(HELP_ITEMS.length >= 10, '帮助清单 ≥10 条');
ok(HELP_ITEMS.some((i) => i.desc.includes('帮助')), '帮助清单含"打开帮助"');

/* ── 2. normalizeKey ── */
eq(normalizeKey({ key: 'g' }), 'g', 'g → g');
eq(normalizeKey({ key: 'Escape' }), 'Escape', 'Escape 归一');
eq(normalizeKey({ key: '?' }), '?', '? 归一');
eq(normalizeKey({ key: '/' }), '/', '/ 归一');
eq(normalizeKey({ key: 'ArrowLeft' }), 'ArrowLeft', 'ArrowLeft 归一');
eq(normalizeKey({ key: ' ' }), ' ', '空格归一');
eq(normalizeKey({ key: 'g', ctrlKey: true }), null, 'Ctrl+g 忽略');
eq(normalizeKey({ key: 'F5' }), null, 'F5 忽略');

/* ── 3. isTypingTarget ── */
ok(isTypingTarget('INPUT'), 'INPUT 是输入目标');
ok(isTypingTarget('textarea'), 'textarea 是输入目标');
ok(isTypingTarget('SELECT'), 'SELECT 是输入目标');
ok(!isTypingTarget('DIV'), 'DIV 不是输入目标');
ok(isTypingTarget('DIV', true), 'contenteditable 是输入目标');

/* ── 4. resolveChord（g 前缀）── */
eq(resolveChord(null, 'g').pending, 'g', 'g 进入待定');
eq(resolveChord('g', 'c').nav, 'cards.html', 'g→c 解析为卡库');
eq(resolveChord('g', 'z').nav, null, 'g→z 无导航');
eq(resolveChord('g', 'z').pending, null, 'g→z 清空待定');
eq(resolveChord(null, 'j').pending, null, 'j 不进入待定');

/* ── 5. cycleIndex（焦点陷阱）── */
eq(cycleIndex(0, 3, false), 1, '正向 0→1');
eq(cycleIndex(2, 3, false), 0, '正向末尾回环');
eq(cycleIndex(0, 3, true), 2, '反向 0→2 回环');
eq(cycleIndex(-1, 3, false), 0, '未聚焦时进入第一个');
eq(cycleIndex(0, 0, false), -1, '空列表返回 -1');

/* ── 6. 播报文案 ── */
eq(announceResults(0, 0), '没有匹配项', '无结果播报');
eq(announceResults(5, 5), '显示 5 条结果，共 5 条', '全量播报');
ok(announceResults(2, 9).includes('筛选后'), '筛选播报含"筛选后"');
eq(announceRating(4), '已标记为已掌握', '评分 4 播报');
eq(announceRating(1), '已标记为薄弱', '评分 1 播报');
ok(shouldCloseOnEsc(true), '弹窗开 → Esc 应关闭');
ok(!shouldCloseOnEsc(false), '无弹窗 → Esc 不处理');

/* ── 7. 8 页面静态结构 ── */
for (const p of PAGES) {
  const h = read(`${p}.html`);
  ok(/skip-link|href="#main"/.test(h), `${p}: 有跳过链接`);
  ok(h.includes('<main'), `${p}: 有 <main>`);
  ok(/qy-nav|<nav/.test(h), `${p}: 有导航`);
  eq((h.match(/<h1[\s>]/g) || []).length, 1, `${p}: 恰好 1 个 <h1>`);
  ok(/<html[^>]*lang=/.test(h), `${p}: html 有 lang`);
  ok(h.includes('name="viewport"'), `${p}: 有 viewport`);
  ok(h.includes('css/a11y.css'), `${p}: 链接 a11y.css`);
  ok(h.includes('initA11y'), `${p}: 注入 initA11y`);
  ok(h.includes('<noscript>'), `${p}: 保留 noscript（不破坏 670c3）`);
  ok(h.includes('initRobustness'), `${p}: 保留 initRobustness（不破坏 670c3）`);
}

/* ── 8. 审计产物（若已运行 tools/a11y_audit_670c4.py --write）── */
const auditPath = new URL('data/a11y_audit_670c4.json', root);
if (existsSync(auditPath)) {
  const audit = JSON.parse(readFileSync(auditPath, 'utf8'));
  eq(audit.critical_total, 0, 'a11y 审计 critical = 0');
  eq(audit.pages.length, 8, '审计覆盖 8 页');
  ok(!audit.pages.some((p) => (p.counts.critical || 0) > 0), '无任何页有 critical');
} else {
  console.log('a11y_670c4: 跳过审计产物断言（先跑 tools/a11y_audit_670c4.py --write）');
}

console.log(`a11y_670c4: ${n} 断言全绿`);
