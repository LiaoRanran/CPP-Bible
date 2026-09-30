// 670c5 · 键位接线测试（纯 Node；DOM 部分用最小 mock）
// 运行：node tests/keybind_670c5.test.mjs
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import { CARD_SELECTOR, collectItems, navIndex } from '../js/keybind.js';
import { normalizeKey, isTypingTarget, cycleIndex } from '../js/a11y_core.js';

const dir = new URL('../', import.meta.url);
const read = (p) => readFileSync(new URL(p, dir), 'utf8');

let n = 0;
const ok = (c, m) => { assert.ok(c, m); n++; };
const eq = (a, b, m) => { assert.equal(a, b, m); n++; };

/* ── collectItems ── */
const mockRoot = (items) => ({ querySelectorAll: () => items });
eq(collectItems(null).length, 0, 'null root → 空数组');
eq(collectItems({}).length, 0, '无 querySelectorAll → 空数组');
eq(collectItems(mockRoot(['a', 'b', 'c'])).length, 3, '收集 3 个卡片项');
eq(collectItems(mockRoot([])).length, 0, '空列表 → 0');
ok(CARD_SELECTOR.includes('#grid'), 'CARD_SELECTOR 限定在 #grid');
ok(CARD_SELECTOR.includes('.card-item'), 'CARD_SELECTOR 限定 .card-item');

/* ── navIndex（j/k 导航）── */
eq(navIndex(-1, 5, 1), 0, '未聚焦时 j → 第一个');
eq(navIndex(-1, 5, -1), 4, '未聚焦时 k → 最后一个');
eq(navIndex(0, 5, 1), 1, 'j 前进一位');
eq(navIndex(4, 5, 1), 0, 'j 末尾回环到首个');
eq(navIndex(0, 5, -1), 4, 'k 首个回环到末尾');
eq(navIndex(2, 5, -1), 1, 'k 后退一位');
eq(navIndex(0, 0, 1), -1, '空列表 → -1');

/* ── 复用 a11y_core（接线一致性）── */
eq(normalizeKey({ key: '/' }), '/', '/ 归一');
eq(normalizeKey({ key: 'j' }), 'j', 'j 归一');
ok(isTypingTarget('INPUT'), '输入态识别（避免劫持输入）');
eq(cycleIndex(1, 3, false), 2, 'cycleIndex 复用一致');

/* ── 页面接线 ── */
for (const p of ['cards', 'learn']) {
  const h = read(`${p}.html`);
  ok(h.includes('initKeybinds'), `${p}.html 注入 initKeybinds`);
  ok(h.includes('js/keybind.js'), `${p}.html 引用 keybind.js`);
}
const kb = read('js/keybind.js');
ok(kb.includes("getElementById('q')"), 'keybind 处理 / → 聚焦 #q');
ok(kb.includes('initKeybinds'), 'keybind 导出 initKeybinds');
ok(kb.includes("from './a11y_core.js'"), 'keybind 复用 a11y_core（不重复实现）');

console.log(`keybind_670c5: ${n} 断言全绿`);
