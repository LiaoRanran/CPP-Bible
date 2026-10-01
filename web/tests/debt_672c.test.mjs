// 672c · 旧债修复 + 断点统一 + 键盘导航全站接线（纯 Node）
// 运行：node tests/debt_672c.test.mjs
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const dir = new URL('../', import.meta.url);
const read = (p) => readFileSync(new URL(p, dir), 'utf8');

const responsive = read('css/responsive.css');
const robustness = read('css/robustness.css');
const qyButton = read('components/qy-button.js');
const style = read('style.css');
const css669 = read('css/669c.css');

let n = 0;
const ok = (c, m) => { assert.ok(c, m); n++; };

/* ── B1：桌面端按钮不被强制 44px，仅在窄屏生效 ── */
ok(!/^\s*button,\s*\.qy-btn[^\n]*min-height:\s*44px/.test(responsive),
  'responsive.css：全局不再对按钮强制 min-height:44px');
ok(/@media \(max-width:\s*768px\)[\s\S]*?min-height:\s*44px/.test(responsive),
  'responsive.css：min-height:44px 收束在 @media (max-width:768px) 内');

/* ── B2：错误横幅 z-index 去魔法数字 ── */
ok(!robustness.includes('z-index: 9999'), 'robustness.css 无 z-index:9999');
ok(robustness.includes('z-index: calc(var(--z-modal) + 1)'), 'robustness.css 用令牌计算 z-index');

/* ── B3：qy-button primary 有 background（白字压沉静蓝底）── */
ok(qyButton.includes(':host([variant="primary"])') && qyButton.includes('background: var(--color-accent'),
  'qy-button primary 变体有 background: var(--color-accent)');

/* ── C：全站断点统一为 640/768/1024/1280（+480 超小屏）── */
const ALLOWED = new Set(['480', '640', '768', '1024', '1280']);
function checkBreakpoints(css, file) {
  const widths = [...css.matchAll(/@media\s*\((?:min|max)-width:\s*(\d+)px\)/g)].map((m) => m[1]);
  const bad = widths.filter((w) => !ALLOWED.has(w));
  ok(bad.length === 0, `${file} 断点仅 640/768/1024/1280/480（越界：${bad.join(',') || '无'}）`);
}
checkBreakpoints(style, 'style.css');
checkBreakpoints(css669, '669c.css');
checkBreakpoints(responsive, 'responsive.css');

/* ── D：8 页全部接线 initKeybinds ── */
const pages = ['index.html', 'cards.html', 'learn.html', 'experiments.html',
  'starmap.html', 'verdicts.html', 'verify.html', 'card.html'];
for (const p of pages) {
  const h = read(p);
  ok(h.includes('initKeybinds'), `${p} 注入 initKeybinds`);
  ok(h.includes('js/keybind.js'), `${p} 引用 js/keybind.js`);
}

console.log(`debt_672c: ${n} 断言全绿`);
