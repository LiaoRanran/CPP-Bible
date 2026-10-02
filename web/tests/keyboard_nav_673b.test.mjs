// 673b B3 · 键盘导航**验收项锁定**测试（纯 Node，无 DOM / 无依赖）。
//
//   从 web/ 目录运行：  node tests/keyboard_nav_673b.test.mjs
//
// 为什么单开一个文件：672c/672d 把键位铺到 8 页，但**没有一条断言锁住"就这 6 个目的地"
// 与"8 页都注入了"**——键位表被误改（多加/少加一个键）或新加页面忘了注入，现有测试都不会红。
// 本文件把这两条验收项写成回归锁；焦点/弹窗行为仍由 a11y_670c4.test.mjs 覆盖。
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';

const dir = new URL('../', import.meta.url);
const read = (p) => readFileSync(new URL(p, dir), 'utf8');

let n = 0;
const ok = (c, m) => { assert.ok(c, m); n++; };
const eq = (a, b, m) => { assert.equal(a, b, m); n++; };

const { NAV_MAP, HELP_ITEMS, resolveChord, normalizeKey, shouldCloseOnEsc } =
  await import('../js/a11y_core.js');

/* ── 1 · 目的地集合：就是这 6 个（多一个少一个都要红）────────────── */
eq(Object.keys(NAV_MAP).sort().join(','), 'c,e,h,l,s,v', 'NAV_MAP 恰好 6 个目的地 h/c/l/e/v/s');
eq(NAV_MAP.h, 'index.html', 'h → 首页');
eq(NAV_MAP.c, 'cards.html', 'c → 卡片');
eq(NAV_MAP.l, 'learn.html', 'l → 学习');
eq(NAV_MAP.e, 'experiments.html', 'e → 实验');
eq(NAV_MAP.v, 'verdicts.html', 'v → 判决');
eq(NAV_MAP.s, 'starmap.html', 's → 星图');

/* ── 2 · g 前缀和弦：每个字母都能解析到对应页 ────────────────────── */
for (const [k, page] of Object.entries(NAV_MAP)) {
  const r = resolveChord('g', k);
  eq(r.nav, page, `g+${k} → ${page}`);
  eq(r.pending, null, `g+${k} 解析后不残留 pending`);
}
eq(resolveChord(null, 'g').pending, 'g', '单独按 g ⇒ 进入 pending 态');
eq(resolveChord('g', 'z').nav, null, 'g+未映射键 ⇒ 不跳转（不瞎猜）');
eq(resolveChord(null, 'h').nav, null, '不带 g 前缀的 h 不跳转（避免误触）');
eq(normalizeKey({ key: 'G' }), 'G', 'normalizeKey 保留原大小写（小写归一在 resolveChord 内做）');
eq(normalizeKey({ key: 'Escape' }), 'Escape', 'Escape 保留原样（供弹窗判据用）');
eq(resolveChord('g', 'H').nav, 'index.html', '第二键大小写不敏感（resolveChord toLowerCase）');
eq(resolveChord(null, 'G').pending, null, '大写 G 不进 pending（契约：前缀必须小写 g）');
eq(normalizeKey({ key: 'g', ctrlKey: true }), null, 'Ctrl+g 是浏览器快捷键 ⇒ 忽略');

/* ── 3 · ? 帮助与 Esc 关闭 ───────────────────────────────────────── */
const helpKeys = HELP_ITEMS.map((i) => (Array.isArray(i.keys) ? i.keys.join('+') : String(i.keys)));
ok(helpKeys.includes('?'), 'HELP_ITEMS 含 ? 帮助条目');
ok(helpKeys.includes('g+h') || helpKeys.includes('g') , 'HELP_ITEMS 解释了 g 前缀');
ok(HELP_ITEMS.length >= 6, `HELP_ITEMS 至少 6 条（实际 ${HELP_ITEMS.length}）`);
eq(shouldCloseOnEsc(true), true, '有弹窗时 Esc 应关闭');
eq(shouldCloseOnEsc(false), false, '无弹窗时 Esc 不应声称可关闭');

/* ── 4 · 八页注入：全站页面都必须接线，且不得漏页 ─────────────────── */
const pages = readdirSync(new URL('.', dir)).filter((f) => f.endsWith('.html')).sort();
eq(pages.length, 8, 'web/ 下恰好 8 个页面（新增页面必须同步本测试与注入）');
for (const p of pages) {
  const html = read(p);
  ok(/initKeybinds/.test(html), `${p} 注入 initKeybinds`);
  ok(/js\/a11y\.js/.test(html), `${p} 引入 a11y.js（? 帮助 / Esc 关闭 / g 和弦的接线层）`);
  ok(/js\/keybind\.js/.test(html), `${p} 引入 keybind.js（j/k 导航与 Enter 激活）`);
  ok(/skip-to|class="skip|skip-link|跳到主内容/.test(html), `${p} 有跳转链接（键盘可绕过导航）`);
}

/* ── 5 · 帮助弹窗的无障碍契约（不靠 DOM，靠源码契约）──────────────── */
const a11y = read('js/a11y.js');
ok(/setAttribute\(['"]role['"],\s*['"]dialog['"]\)/.test(a11y), '帮助弹窗声明 role=dialog');
ok(/aria-modal/.test(a11y), '帮助弹窗声明 aria-modal');
ok(/aria-labelledby/.test(a11y), '帮助弹窗有 aria-labelledby');
ok(/trapTab/.test(a11y), '帮助弹窗做焦点陷阱');
ok(/shouldCloseOnEsc/.test(a11y), 'Esc 关闭走统一判据（shouldCloseOnEsc）');

console.log(`keyboard_nav_673b.test: ${n} assertions passed ✓`);
