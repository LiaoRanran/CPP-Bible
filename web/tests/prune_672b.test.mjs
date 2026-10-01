// 672b · 减法批次验收测试（纯 Node，读文件系统 + 动态 import 校验）
// 覆盖：vendor 与 4 死组件已删、components/index.js 收敛、app.js 收敛（删 mountNav + re-export）、
//        build.mjs 白名单去 vendor、CSS 死类移除且 LIVE 类保留、data.js 存在且导出齐全。
// 运行：node tests/prune_672b.test.mjs
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = fileURLToPath(new URL('../', import.meta.url));
const P = (p) => `${ROOT}${p}`;
const read = (p) => readFileSync(P(p), 'utf8');

let n = 0;
const ok = (c, m) => { assert.ok(c, m); n++; };
const no = (c, m) => { assert.ok(!c, m); n++; };
const eq = (a, b, m) => { assert.equal(a, b, m); n++; };

/* ── A. vendor 目录已删除 ── */
no(existsSync(P('vendor')), 'web/vendor 目录已删');

/* ── B. 4 个死组件已删 ── */
for (const f of ['qy-card.js', 'qy-panel.js', 'qy-status.js', 'qy-tag.js']) {
  no(existsSync(P(`components/${f}`)), `components/${f} 已删`);
}
/* ── B'. 留存组件仍在 ── */
for (const f of ['qy-nav.js', 'qy-button.js', 'index.js']) {
  ok(existsSync(P(`components/${f}`)), `components/${f} 留存`);
}

/* ── C. components/index.js 收敛 ── */
const idx = read('components/index.js');
ok(idx.includes("export { QyNav } from './qy-nav.js';"), 'index 仍导出 QyNav');
ok(idx.includes("export { QyButton } from './qy-button.js';"), 'index 仍导出 QyButton');
no(idx.includes("./qy-card.js"), 'index 不再 re-export qy-card');
no(idx.includes("./qy-panel.js"), 'index 不再 re-export qy-panel');
no(idx.includes("./qy-status.js"), 'index 不再 re-export qy-status');
no(idx.includes("./qy-tag.js"), 'index 不再 re-export qy-tag');
eq(idx.match(/export const COMPONENTS = \[([^\]]*)\]/)[1].replace(/\s|'/g, ''), 'qy-nav,qy-button',
  'COMPONENTS 收敛为 [qy-nav, qy-button]');

/* ── D. app.js 收敛：删 mountNav + re-export data.js ── */
const app = read('app.js');
no(/export function mountNav\s*\(/.test(app), 'app.js 已删 mountNav');
ok(/export \{\s*fetchJSON\s*\} from '\.\/js\/data\.js';/.test(app), 'app.js re-export data.js 的 fetchJSON');
// 动态 import 验证：fetchJSON 确实可从 app.js 取到（旧调用方零改动）
const appMod = await import(pathToFileURL(P('app.js')).href);
ok(typeof appMod.fetchJSON === 'function', 'app.js 仍可导出 fetchJSON（re-export）');

/* ── E. build.mjs 白名单去 vendor ── */
const build = read('build.mjs');
const dirsLine = build.match(/const DIRS = \[([^\]]*)\]/)[1];
no(dirsLine.includes('vendor'), 'build.mjs DIRS 不再含 vendor');
for (const d of ['css', 'js', 'components', 'data']) {
  ok(dirsLine.includes(`'${d}'`), `build.mjs DIRS 含 '${d}'`);
}

/* ── F. style.css：死类移除 ── */
const css = read('style.css');
no(/\.nav\s*\{/.test(css), 'style.css 删 .nav 块');
no(/\.status-grid/.test(css), 'style.css 删 .status-grid');
no(/\.glass-hover/.test(css), 'style.css 删 .glass-hover');
no(/\.glow-pass/.test(css), 'style.css 删 .glow-*');
no(/@media \(max-width: 360px\) \{\s*\}/.test(css), 'style.css 不残留空 360px 媒体查询');

/* ── F'. style.css：LIVE 类保留 ── */
for (const cls of ['.glass {', '.glass-tint {', '.kind-tag {', '.dash {', '.warn-line {', '.cluster-list {']) {
  ok(css.includes(cls), `style.css 保留 LIVE 类 ${cls}`);
}

/* ── G. 669c.css：err-step 移除，LIVE 类保留 ── */
const c669 = read('css/669c.css');
no(/\.err-step/.test(c669), '669c.css 删 .err-step');
for (const cls of ['.detail-btn', '.modal-kv', '.compare-col', '.ev-tree']) {
  ok(c669.includes(cls), `669c.css 保留 LIVE 类 ${cls}`);
}

/* ── H. data.js 存在且导出齐全 ── */
const dataMod = await import(pathToFileURL(P('js/data.js')).href);
for (const name of ['fetchJSON', 'esc', 'formatMetric', 'pct']) {
  ok(typeof dataMod[name] === 'function', `data.js 导出 ${name}`);
}

/* ── I. home.js 已迁到 data.js（无本地 esc/pct 重复）── */
const home = read('home.js');
ok(home.includes("from './js/data.js'"), 'home.js 从 data.js 导入');
ok(/import \{[^}]*\bformatMetric\b[^}]*\} from '\.\/js\/data\.js'/.test(home), 'home.js 从 data.js 取 formatMetric');
no(/import \{[^}]*\bformatMetric\b[^}]*\} from '\.\/js\/robustness\.js'/.test(home), 'home.js 不从 robustness 取 formatMetric');
no(/const esc = \(s\)/.test(home), 'home.js 不再本地定义 esc');
no(/const pct = \(v\)/.test(home), 'home.js 不再本地定义 pct');

/* ── J. metrics_666.json 已补 generated_at ── */
const m666 = JSON.parse(read('data/metrics_666.json'));
ok(typeof m666.generated_at === 'string' && m666.generated_at.length >= 10, 'metrics_666.json 含 generated_at');

console.log(`prune_672b: ${n} 断言全绿`);
