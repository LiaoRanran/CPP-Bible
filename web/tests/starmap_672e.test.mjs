// 672e A · 星图 2.5D 伪3D 重制验收（无 DOM / 无 canvas / 无 jsdom / 零外部依赖）
//
// 跑法（在 web/ 下）：node tests/starmap_672e.test.mjs
//
// 测什么：只测 672e 新增的**纯函数投影/绘制逻辑**（projectPoint / depthFor /
//   nodeRadiusFor / nodeAlpha），并扫描 web/starmap.js 源码确认：
//   · 有 z 轴透视（近大远小 + 远节点更暗，且旋转会带动 z 轴）；
//   · hover 高亮邻居（非邻居压暗、邻居保持）；
//   · 颜色全部走 design-tokens（不写死 green/red/yellow，不引 Three.js）；
//   · 2D 平面变换数学未被动（applyTransform/invertTransform 仍导出）。
// 不测什么：canvas 实际像素（jsdom 无 2D context，测了也是假绿）。
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import * as SM from '../starmap.js';

let passed = 0;
const ok = (name, cond) => { assert.ok(cond, 'FAIL: ' + name); passed++; };
const gt = (a, b, m) => { assert.ok(a > b, m + ' (' + a + ' !> ' + b + ')'); passed++; };
const lt = (a, b, m) => { assert.ok(a < b, m + ' (' + a + ' !< ' + b + ')'); passed++; };

const SRC = readFileSync(new URL('../starmap.js', import.meta.url), 'utf-8');

/* ══ ① 透视投影：近大远小 + 远节点更暗（z 轴存在）════════════════════════ */
ok('projectPoint 已导出', typeof SM.projectPoint === 'function');

const near = SM.projectPoint({ x: 0, y: 0, z: -150 }, { rotX: 0, rotY: 0, k: 1 });
const far = SM.projectPoint({ x: 0, y: 0, z: 150 }, { rotX: 0, rotY: 0, k: 1 });
gt(near.scale, far.scale, 'z 轴透视：近节点 scale > 远节点 scale（近大远小）');
gt(near.alpha, far.alpha, 'z 轴透视：近节点 alpha > 远节点 alpha（远节点更暗）');
ok('projectPoint.alpha 被夹在 [0.45, 1]',
  near.alpha >= 0.45 && near.alpha <= 1 && far.alpha >= 0.45 && far.alpha <= 1);

// 旋转必须带动 z 轴：同样一个点，绕 Y 轴转一下，屏幕 x 必须变（否则 z 轴没参与投影）
const p0 = SM.projectPoint({ x: 0, y: 0, z: 100 }, { rotX: 0, rotY: 0, k: 1 });
const pR = SM.projectPoint({ x: 0, y: 0, z: 100 }, { rotX: 0, rotY: 0.6, k: 1 });
ok('旋转带动 z 轴：rotY 改变后同一点屏幕坐标变化（真 2.5D，不是 2D 平移）',
  Math.abs(p0.sx - pR.sx) > 1e-6 || Math.abs(p0.sy - pR.sy) > 1e-6);
// 俯仰（绕 X）也必须有可见效果
const pX = SM.projectPoint({ x: 0, y: 0, z: 100 }, { rotX: 0.5, rotY: 0, k: 1 });
ok('俯仰旋转 rotX 也改变投影', Math.abs(p0.sy - pX.sy) > 1e-6 || Math.abs(p0.sx - pX.sx) > 1e-6);
// 缩放 k 线性作用到 scale
const pk = SM.projectPoint({ x: 0, y: 0, z: 0 }, { rotX: 0, rotY: 0, k: 2 });
ok('缩放 k 线性作用到投影 scale（k=2 ⇒ scale 翻倍）',
  Math.abs(pk.scale - 2 * SM.projectPoint({ x: 0, y: 0, z: 0 }, { rotX: 0, rotY: 0, k: 1 }).scale) < 1e-9);

/* ══ ② 深度分配：确定性 + 2.5D 铺开（不写死 178/1093）═══════════════════ */
ok('depthFor 已导出', typeof SM.depthFor === 'function');
const nodes = Array.from({ length: 20 }, (_, i) => ({ id: 'n' + i, kind: 'prop', domain: 'x' }));
const z1 = SM.depthFor(nodes, null, {});
const z2 = SM.depthFor(nodes, null, {});
ok('depthFor 长度 = 节点数', z1.length === 20);
ok('depthFor 确定性（同输入逐位一致）',
  Array.from(z1).every((v, i) => v === z2[i]));
ok('depthFor 非全平（真 3D 深度，不是 0）',
  new Set(Array.from(z1)).size > 3);
ok('depthFor 同时含近（负）与远（正）',
  Array.from(z1).some((v) => v < 0) && Array.from(z1).some((v) => v > 0));
ok('depthFor 不越界（|z| <= range=220）',
  Array.from(z1).every((v) => Math.abs(v) <= 220 + 1e-9));

/* ══ ③ 节点大小按 degree 分级（hub 最大，孤立点最小）════════════════════ */
ok('nodeRadiusFor 已导出', typeof SM.nodeRadiusFor === 'function');
const r0 = SM.nodeRadiusFor(0), rHub = SM.nodeRadiusFor(51), rMid = SM.nodeRadiusFor(10);
ok('degree=0 ⇒ 最小半径', r0 === SM.DEGREE_TIERS.min);
ok('degree=hub(51) ⇒ 最大半径', Math.abs(rHub - SM.DEGREE_TIERS.max) < 1e-9);
lt(r0, rMid, '半径随 degree 单调增（0 < 10）');
lt(rMid, rHub, '半径随 degree 单调增（10 < 51）');

/* ══ ④ hover 高亮邻居（纯函数 nodeAlpha）═════════════════════════════════ */
ok('nodeAlpha 已导出', typeof SM.nodeAlpha === 'function');
const neigh = new Set([3, 5, 8]);
// 悬停 3：邻居 5 保持满亮，非邻居 7 压暗
ok('hover 邻居 ⇒ 满亮', SM.nodeAlpha(5, { hovered: 3, neighbors: neigh, baseAlpha: 1 }) === 1);
lt(SM.nodeAlpha(7, { hovered: 3, neighbors: neigh, baseAlpha: 1 }),
  SM.nodeAlpha(5, { hovered: 3, neighbors: neigh, baseAlpha: 1 }),
  'hover 非邻居 ⇒ 压暗（dimNeighbor）');
// 悬停节点本身不被当非邻居压暗
ok('hover 节点自身 ⇒ 满亮（不是非邻居）',
  SM.nodeAlpha(3, { hovered: 3, neighbors: neigh, baseAlpha: 1 }) === 1);
// 搜索未命中压暗，命中保持
const hits = new Set([5]);
ok('搜索命中 ⇒ 满亮', SM.nodeAlpha(5, { searchHits: hits, baseAlpha: 1 }) === 1);
lt(SM.nodeAlpha(7, { searchHits: hits, baseAlpha: 1 }),
  1, '搜索未命中 ⇒ 压暗（dimSearch）');
// 无 hover/搜索 ⇒ 不被压暗
ok('无 hover/搜索 ⇒ 不被压暗', SM.nodeAlpha(7, { baseAlpha: 0.6 }) === 0.6);

/* ══ ⑤ 颜色全部走 design-tokens（不写死 green/red/yellow，不引 Three.js）══ */
// 当前 design-tokens 的四态色（深/浅两主题）。若 starmap.js 写死它们，等于绕过令牌系统。
const FORBIDDEN = ['#4ade80', '#f87171', '#fbbf24', '#15803d', '#b91c1c', '#a16207'];
ok('starmap.js 不写死当前 design-token 四态色（green/red/yellow）',
  FORBIDDEN.every((h) => SRC.indexOf(h) < 0));
ok('starmap.js 不引 Three.js（零外部依赖）',
  !/from\s+['"]three['"]/.test(SRC) && SRC.indexOf('THREE') < 0);
ok('starmap.js 节点色走导入的 STATE_COLORS（design-token 镜像）',
  SRC.indexOf('STATE_COLORS') > 0);
ok('starmap.js 聚类色走 clusterPalette（从 CSS 变量派生）',
  SRC.indexOf('clusterPalette') > 0);
ok('starmap.js 连线色走 LINK_STYLE（design-token 镜像）',
  SRC.indexOf('EDGE_STROKE') > 0);

/* ══ ⑥ 2D 平面变换数学未被动（回归锁）══════════════════════════════════ */
ok('applyTransform / invertTransform 仍导出（2D 数学未删）',
  typeof SM.applyTransform === 'function' && typeof SM.invertTransform === 'function');
const inv = SM.invertTransform(SM.applyTransform({ x: 31, y: -44 }, { x: -12, y: 30, k: 1.7 }, { width: 800, height: 600 }),
  { x: -12, y: 30, k: 1.7 }, { width: 800, height: 600 });
ok('2D 变换仍可逆（invert∘apply = 恒等）',
  Math.abs(inv.x - 31) < 1e-9 && Math.abs(inv.y + 44) < 1e-9);

console.log('starmap_672e: ' + passed + ' assertions passed');
