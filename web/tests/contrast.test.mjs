// 670c A6 · Node 真求值：对比度审计工具测试（无 DOM）
// 覆盖：颜色解析 · 相对亮度 · 对比度公式 · alpha 合成 · **主题块归属** · 真实 tokens 全绿
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  parseColor, over, relLuminance, contrastRatio,
  parseTokens, auditPairs, auditCss, PAIRS_670C, AA_NORMAL,
} from '../js/contrast_check.js';

let passed = 0;
const ok = (name, cond) => { assert.ok(cond, 'FAIL: ' + name); passed++; };
const close = (a, b, eps = 0.01) => Math.abs(a - b) <= eps;

// ── 颜色解析 ──
ok('#rgb 解析', JSON.stringify(parseColor('#f00')) === JSON.stringify({ r: 255, g: 0, b: 0, a: 1 }));
ok('#rrggbb 解析', JSON.stringify(parseColor('#1a1a1a')) === JSON.stringify({ r: 26, g: 26, b: 26, a: 1 }));
ok('rgb() 解析', parseColor('rgb(1, 2, 3)').b === 3);
ok('rgba() 解析保留 alpha', close(parseColor('rgba(217, 119, 87, .16)').a, 0.16));
ok('非法颜色返回 null', parseColor('not-a-color') === null && parseColor(null) === null);

// ── alpha 合成 ──
ok('不透明色合成后不变', JSON.stringify(over({ r: 1, g: 2, b: 3, a: 1 }, { r: 9, g: 9, b: 9, a: 1 })) === JSON.stringify({ r: 1, g: 2, b: 3, a: 1 }));
ok('全透明色等于底层', JSON.stringify(over({ r: 255, g: 255, b: 255, a: 0 }, { r: 10, g: 20, b: 30, a: 1 })) === JSON.stringify({ r: 10, g: 20, b: 30, a: 1 }));
ok('半透明色落在两层之间', (() => {
  const m = over({ r: 0, g: 0, b: 0, a: 0.5 }, { r: 100, g: 100, b: 100, a: 1 });
  return close(m.r, 50, 0.001);
})());

// ── 相对亮度 / 对比度 ──
ok('黑色亮度 = 0', close(relLuminance({ r: 0, g: 0, b: 0 }), 0, 1e-9));
ok('白色亮度 = 1', close(relLuminance({ r: 255, g: 255, b: 255 }), 1, 1e-9));
ok('黑白对比度 = 21', close(contrastRatio('#000000', '#ffffff'), 21, 0.01));
ok('同色对比度 = 1', close(contrastRatio('#123456', '#123456'), 1, 1e-9));
ok('对比度与顺序无关', close(contrastRatio('#000', '#fff'), contrastRatio('#fff', '#000')));
ok('非法输入返回 null', contrastRatio('zzz', '#fff') === null);
ok('AA 阈值为 4.5', AA_NORMAL === 4.5);

// ── 主题块归属（670c 真实踩过的坑）──
// @media (prefers-color-scheme: light) { :root:not([data-theme="dark"]) { ... } }
// 这条选择器里带 "dark" 字样，但它是**浅色**主题；只看 sel 会判反。
const CSS_FIXTURE = [
  ':root { --color-bg: #1a1a1a; --color-text: #e8e6e3; }',
  '@media (prefers-color-scheme: light) {',
  '  :root:not([data-theme="dark"]) { --color-bg: #faf9f7; --color-text: #1f1e1d; }',
  '}',
  'html[data-theme="light"] { --color-bg: #faf9f7; }',
  'html[data-theme="dark"] { color-scheme: dark; }',
].join('\n');
const tk = parseTokens(CSS_FIXTURE);
ok('dark 取 :root 的值', tk.dark['--color-bg'] === '#1a1a1a');
ok('dark 不被 light 覆盖（回归：not([data-theme=dark]) 必须归 light）', tk.dark['--color-text'] === '#e8e6e3');
ok('light 取 @media 里的值', tk.light['--color-bg'] === '#faf9f7');
ok('light 取 html[data-theme=light] 的值', tk.light['--color-text'] === '#1f1e1d');
ok('dark 主题里 color-scheme 不污染颜色 token', tk.dark['color-scheme'] === undefined);

// ── 审计逻辑 ──
const good = auditPairs({ '--fg': '#ffffff', '--bg': '#000000' }, [{ name: 'x', fg: '--fg', bg: '--bg' }]);
ok('审计：21:1 判过', good[0].pass === true && close(good[0].ratio, 21, 0.01));
const bad = auditPairs({ '--fg': '#666666', '--bg': '#000000' }, [{ name: 'x', fg: '--fg', bg: '--bg' }]);
ok('审计：低对比判不过（#666 on #000 = 3.66:1）', bad[0].pass === false && bad[0].ratio < 4.5);
// 阈值边界：#777 on #000 = 4.69:1 应当**通过**（防止把阈值写成 >=5 之类）
const edge = auditPairs({ '--fg': '#777777', '--bg': '#000000' }, [{ name: 'x', fg: '--fg', bg: '--bg' }]);
ok('审计：阈值边界 4.69:1 判过', edge[0].pass === true && edge[0].ratio > 4.5);
const miss = auditPairs({}, [{ name: 'x', fg: '--nope', bg: '--bg' }]);
ok('审计：缺 token 记 error 且判不过', miss[0].pass === false && !!miss[0].error);
ok('审计：半透明底会记录取到的最差父层', (() => {
  const r = auditPairs(
    { '--fg': '#ffffff', '--bg': 'rgba(0,0,0,0.5)', '--p1': '#ffffff', '--p2': '#000000' },
    [{ name: 'x', fg: '--fg', bg: '--bg', parents: ['--p1', '--p2'] }],
  );
  return r[0].parent === '--p1' && r[0].ratio <= 21;
})());

// ── 真实 design-tokens.css 全绿（这是本工具的交付口径）──
const realCss = readFileSync(new URL('../css/design-tokens.css', import.meta.url), 'utf8');
const real = auditCss(realCss);
ok('真实 tokens：暗色主题无失败', real.themes.dark.every((r) => r.pass === true));
ok('真实 tokens：亮色主题无失败', real.themes.light.every((r) => r.pass === true));
ok('真实 tokens：两主题都算到全部配对', real.themes.dark.length === PAIRS_670C.length
  && real.themes.light.length === PAIRS_670C.length);
ok('真实 tokens：overall ok 且 failures=0', real.ok === true && real.failures.length === 0);
// 671d：配色换了（暖中性+橙 → 中性灰阶+沉静蓝），锁定的数值随之更新。
// 仍锁"正文/底"这一对，是为了防止有人把正文色改淡 —— 断言的意义不变。
ok('真实 tokens：正文/底 暗色 = 16.91:1（与 tokens 注释一致）', (() => {
  const row = real.themes.dark.find((r) => r.name === '正文 / 底');
  return row && Math.abs(row.ratio - 16.91) < 0.05;
})());
ok('真实 tokens：正文/底 亮色 ≥ 15:1（浅底也要足够黑）', (() => {
  const row = real.themes.light.find((r) => r.name === '正文 / 底');
  return row && row.pass && row.ratio >= 15;
})());
ok('真实 tokens：热力图标签对比度已修复(≥4.5)', (() => {
  const d = real.themes.dark.find((r) => r.name === '热力图标签 / 选中底');
  const l = real.themes.light.find((r) => r.name === '热力图标签 / 选中底');
  return d.pass && l.pass && d.ratio >= 4.5 && l.ratio >= 4.5;
})());

console.log('contrast.test: ' + passed + ' assertions passed');
