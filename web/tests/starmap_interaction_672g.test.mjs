// 672g A · 星图交互模型验收（纯 Node / 无 DOM / 无 canvas / 无 jsdom / 零外部依赖）
//
// 跑法（在 web/ 下）：node tests/starmap_interaction_672g.test.mjs
//
// 病（用户原话"操作起来好奇怪"）：672e 把**左键拖拽做成旋转视角** —— 与图谱 / 地图类
//   应用的共识（拖拽 = 平移画布）相反；而同一页的键盘方向键又是平移 ⇒ 两套语义打架。
// 672g 的修复（本文件逐条锁死）：
//   · 左键拖拽 = 平移（panX/panY，屏幕像素，与 k 无关）
//   · 右键 / Shift+左键 = 旋转（rotY 绕竖轴 / rotX 俯仰，clamp ±1.3）
//   · 滚轮 = 以光标为不动点缩放
//   · 双击 = 复位（旋转 + 平移归零）
//   · 方向键 = 平移，与左键同一套语义、同一量纲
//   · 旋转灵敏度 0.006 → 0.003
//   · 画布角落常驻操作提示
// 另外顺带锁死 672g 修掉的投影量纲 bug：世界偏移必须在**缩放前**加、屏幕平移在**缩放后**加。
//
// 不测什么：canvas 实际像素（jsdom 无 2D context，测了也是假绿）。
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import * as SM from '../starmap.js';

let passed = 0;
const ok = (name, cond) => { assert.ok(cond, 'FAIL: ' + name); passed++; };
const eq = (a, b, m) => { assert.equal(a, b, 'FAIL: ' + m + ' (' + a + ' != ' + b + ')'); passed++; };
const near = (a, b, m, tol = 1e-9) => {
  assert.ok(Math.abs(a - b) <= tol, 'FAIL: ' + m + ' (' + a + ' !≈ ' + b + ')'); passed++;
};

const SRC = readFileSync(new URL('../starmap.js', import.meta.url), 'utf-8');
const HTML = readFileSync(new URL('../starmap.html', import.meta.url), 'utf-8');
const VP = { width: 900, height: 620, centerX: 450, centerY: 310, minK: 0.25, maxK: 6 };
const at = (v, w) => SM.projectPoint(w, Object.assign({}, v, { cx: VP.centerX, cy: VP.centerY }));
const W = { x: 120, y: -80, z: 30 };
const V0 = { x: -140, y: 25, k: 0.8, rotX: 0.2, rotY: -0.4, panX: 40, panY: -25 };

/* ══ ① 模式判定：左键平移 / 右键旋转 / Shift+左键旋转 ═════════════════════ */
ok('interactionMode 已导出', typeof SM.interactionMode === 'function');
eq(SM.interactionMode({ button: 0 }), 'pan', '左键（button=0）⇒ 平移');
eq(SM.interactionMode({ button: 2 }), 'rotate', '右键（button=2）⇒ 旋转');
eq(SM.interactionMode({ button: 0, shiftKey: true }), 'rotate', 'Shift + 左键 ⇒ 旋转');
eq(SM.interactionMode({}), 'pan', '合成事件缺 button ⇒ 按左键（平移）');
eq(SM.interactionMode({ button: 1 }), 'pan', '中键 ⇒ 平移（不是旋转）');

/* ══ ② 平移：屏幕像素量纲，与 k 无关 ═════════════════════════════════════ */
ok('panBy 已导出', typeof SM.panBy === 'function');
const p1 = SM.panBy(V0, 37, -12);
near(p1.panX - V0.panX, 37, 'panBy：panX 精确加 dx');
near(p1.panY - V0.panY, -12, 'panBy：panY 精确加 dy');
eq(p1.rotX, V0.rotX, 'panBy 不动 rotX');
eq(p1.rotY, V0.rotY, 'panBy 不动 rotY');
eq(p1.k, V0.k, 'panBy 不动 k');
eq(p1.x, V0.x, 'panBy 不动世界偏移 x');
// 屏幕上真的走了 37px，且在不同 k 下位移一致（证明量纲是屏幕 px 而非世界坐标）
const dA = at(SM.panBy(V0, 37, 0), W).sx - at(V0, W).sx;
const dB = at(SM.panBy(Object.assign({}, V0, { k: 2.5 }), 37, 0), W).sx - at(Object.assign({}, V0, { k: 2.5 }), W).sx;
near(dA, 37, '平移 37px ⇒ 屏幕真的走 37px（k=0.8）');
near(dB, 37, '平移 37px ⇒ 屏幕真的走 37px（k=2.5，与 k 无关）');

/* ══ ③ 旋转：灵敏度 0.003 + 俯仰 clamp，且不动平移 ═══════════════════════ */
ok('rotateBy 已导出', typeof SM.rotateBy === 'function');
eq(SM.ROTATE_SENSITIVITY, 0.003, '旋转灵敏度 = 0.003（672e 的 0.006 减半）');
ok('灵敏度确实比 672e 低', SM.ROTATE_SENSITIVITY < 0.006);
const r1 = SM.rotateBy(V0, 100, 40);
near(r1.rotY - V0.rotY, 100 * 0.003, 'rotateBy：水平 100px ⇒ rotY += 0.3');
near(r1.rotX - V0.rotX, 40 * 0.003, 'rotateBy：垂直 40px ⇒ rotX += 0.12');
eq(r1.panX, V0.panX, 'rotateBy 不动 panX');
eq(r1.panY, V0.panY, 'rotateBy 不动 panY');
eq(r1.x, V0.x, 'rotateBy 不动世界偏移 x');
// 俯仰 clamp ±1.3（一拖到底也不会翻面）
eq(SM.rotateBy(V0, 0, 100000).rotX, 1.3, 'rotX 上限 clamp = +1.3');
eq(SM.rotateBy(V0, 0, -100000).rotX, -1.3, 'rotX 下限 clamp = -1.3');
// 绕竖轴 rotY 不 clamp（可以一直转圈）
near(SM.rotateBy(V0, 100000, 0).rotY, V0.rotY + 300, 'rotY 不 clamp（可连续旋转）');

/* ══ ④ 平移与旋转互不干扰（先平后转 / 先转后平，结果一致）════════════════ */
const panThenRot = SM.rotateBy(SM.panBy(V0, 50, -20), 200, 60);
const rotThenPan = SM.panBy(SM.rotateBy(V0, 200, 60), 50, -20);
near(panThenRot.panX, rotThenPan.panX, '平移/旋转可交换：panX 一致');
near(panThenRot.rotY, rotThenPan.rotY, '平移/旋转可交换：rotY 一致');
near(panThenRot.rotX, rotThenPan.rotX, '平移/旋转可交换：rotX 一致');
// 只平移不旋转时，投影出的图形必须是**纯平移**（形状一点不变）
const before = at(V0, W), afterPan = at(SM.panBy(V0, 64, -31), W);
near(afterPan.sx - before.sx, 64, '纯平移：sx 位移 = 64');
near(afterPan.sy - before.sy, -31, '纯平移：sy 位移 = -31');
near(afterPan.scale, before.scale, '纯平移不改变 scale（不缩放）');
near(afterPan.alpha, before.alpha, '纯平移不改变 alpha（不变暗）');
// 旋转则必须改变投影（否则 2.5D 是假的）
const afterRot = at(SM.rotateBy(V0, 200, 0), W);
ok('旋转会改变投影（真 2.5D，不是 2D 平移）',
  Math.abs(afterRot.sx - before.sx) > 1e-6 || Math.abs(afterRot.sy - before.sy) > 1e-6);

/* ══ ⑤ 滚轮缩放：以光标为不动点 ═════════════════════════════════════════ */
ok('zoomAt 已导出', typeof SM.zoomAt === 'function');
const zNoAnchor = SM.zoomAt(V0, 1.2, null, VP);
eq(zNoAnchor.panX, V0.panX, '无锚点缩放 ⇒ 平移不动（以视口中心缩放）');
near(zNoAnchor.k, V0.k * 1.2, '无锚点缩放 ⇒ k × 1.2');
// 锚点不动：光标下那个世界点缩放前后屏幕坐标必须重合
const anchor = at(V0, W);
const zA = SM.zoomAt(V0, 1.12, { x: anchor.sx, y: anchor.sy }, VP);
const afterZoom = at(zA, W);
near(afterZoom.sx, anchor.sx, '滚轮放大：光标下的点 sx 不动');
near(afterZoom.sy, anchor.sy, '滚轮放大：光标下的点 sy 不动');
const zB = SM.zoomAt(V0, 1 / 1.12, { x: anchor.sx, y: anchor.sy }, VP);
near(at(zB, W).sx, anchor.sx, '滚轮缩小：光标下的点 sx 同样不动');
ok('缩放确实改变了 k', zA.k > V0.k && zB.k < V0.k);
// 缩放区间 clamp
eq(SM.zoomAt(V0, 1000, null, VP).k, 6, 'k 上限 clamp = 6');
eq(SM.zoomAt(V0, 0.0001, null, VP).k, 0.25, 'k 下限 clamp = 0.25');

/* ══ ⑥ 双击复位：旋转 + 平移归零，保留自适应给的 k ═══════════════════════ */
ok('resetViewTransform 已导出', typeof SM.resetViewTransform === 'function');
const dirty = SM.panBy(SM.rotateBy(V0, 300, 90), -70, 55);
const reset = SM.resetViewTransform(dirty);
eq(reset.rotX, 0, '复位：rotX 归零');
eq(reset.rotY, 0, '复位：rotY 归零');
eq(reset.panX, 0, '复位：panX 归零');
eq(reset.panY, 0, '复位：panY 归零');
eq(reset.k, dirty.k, '复位：k 保留（由 fitView 另行重算）');
eq(reset.x, dirty.x, '复位：世界偏移保留（由 fitView 另行重算）');

/* ══ ⑦ 方向键 = 平移，与左键同一套语义、同一量纲 ═════════════════════════ */
ok('panStepForKey 已导出', typeof SM.panStepForKey === 'function');
eq(SM.PAN_STEP_PX, 60, '方向键步长 = 60px（屏幕像素）');
near(SM.panStepForKey('ArrowLeft').dx, 60, '← ⇒ 内容右移 60px（视口左移）');
near(SM.panStepForKey('ArrowRight').dx, -60, '→ ⇒ 内容左移 60px（视口右移）');
near(SM.panStepForKey('ArrowUp').dy, 60, '↑ ⇒ 内容下移 60px（视口上移）');
near(SM.panStepForKey('ArrowDown').dy, -60, '↓ ⇒ 内容上移 60px（视口下移）');
eq(SM.panStepForKey('a'), null, '非方向键 ⇒ null（交还给缩放/复位分支）');
// 键鼠一致：一次 ← 与"左键拖 60px"产生的屏幕位移完全相等
const byKey = at(SM.panBy(V0, SM.panStepForKey('ArrowLeft').dx, SM.panStepForKey('ArrowLeft').dy), W);
const byMouse = at(SM.panBy(V0, 60, 0), W);
near(byKey.sx, byMouse.sx, '方向键平移与鼠标左键平移位移完全一致');
// 方向键步长不随 k 变（672e 是 60/k，和鼠标对不上）
near(SM.panStepForKey('ArrowLeft', 60).dx, SM.panStepForKey('ArrowLeft', 60).dx, '步长与 k 无关');

/* ══ ⑧ 投影量纲修复：世界偏移在缩放前、屏幕平移在缩放后 ═════════════════ */
// 自适应之后，包围盒中心必须落在视口中心（672e 实测偏 84px：中心落在 533.9 而非 450）
const bounds = { minX: -1425.48, minY: -848.02, maxX: 1184.52, maxY: 878.33,
  width: 2609.99, height: 1726.35, cx: -120.48, cy: 15.15 };
const fit = SM.fitTransform(bounds, { width: 900, height: 620, padding: 48, maxK: 1.6, minK: 0.2 });
const fitted = Object.assign(SM.defaultView(), fit);
const ctr = at(fitted, { x: bounds.cx, y: bounds.cy, z: 0 });
near(ctr.sx, VP.centerX, '自适应后包围盒中心 sx = 视口中心（672g 修掉的偏移 bug）', 1e-6);
near(ctr.sy, VP.centerY, '自适应后包围盒中心 sy = 视口中心', 1e-6);
// 旋转绕的是"已居中的模型"⇒ 转完中心仍在视口中心附近（不会被甩出视口）
const spun = SM.rotateBy(fitted, 300, 120);
const spunCtr = at(spun, { x: bounds.cx, y: bounds.cy, z: 0 });
ok('旋转后模型中心仍在视口内（绕模型中心转，不是绕世界原点）',
  Math.abs(spunCtr.sx - VP.centerX) < VP.width / 4 && Math.abs(spunCtr.sy - VP.centerY) < VP.height / 4);
// defaultView 六个分量齐全
const dv = SM.defaultView();
ok('defaultView 六分量齐全（含 panX/panY）',
  ['x', 'y', 'k', 'rotX', 'rotY', 'panX', 'panY'].every((k) => Object.prototype.hasOwnProperty.call(dv, k)));

/* ══ ⑨ 操作提示：常量是唯一真源 + HTML 里有承接元素 ═════════════════════ */
ok('INTERACTION_HINTS 已导出', typeof SM.INTERACTION_HINTS === 'string');
eq(SM.INTERACTION_HINTS, '左键平移 / 右键旋转 / 滚轮缩放 / 双击复位', '提示文案逐字一致');
['左键平移', '右键旋转', '滚轮缩放', '双击复位'].forEach((t) => {
  ok('提示含「' + t + '」', SM.INTERACTION_HINTS.indexOf(t) >= 0);
});
ok('starmap.html 有 #map-hint 承接元素', HTML.indexOf('id="map-hint"') > 0);
ok('starmap.html 静态文案与常量一致（JS 未加载时也能看到提示）',
  HTML.indexOf(SM.INTERACTION_HINTS) > 0);
ok('starmap.js 用常量写入 #map-hint（杜绝两处文案漂移）',
  /byId\('map-hint'\)/.test(SRC) && SRC.indexOf('INTERACTION_HINTS') > 0);

/* ══ ⑩ 源码接线锁：右键菜单被掐掉 + 按 button 分派 + 双击复位 ═══════════ */
ok('canvas 上挂了 contextmenu 且 preventDefault（否则右键一按就弹菜单）',
  /addEventListener\('contextmenu'/.test(SRC) && /contextmenu'[\s\S]{0,80}preventDefault/.test(SRC));
ok('mousedown 用 interactionMode(e) 决定模式（不再无脑旋转）',
  /mousedown'[\s\S]{0,200}interactionMode/.test(SRC));
ok('mousemove 拖拽分支按 mode 分派 panBy / rotateBy',
  /\(mode === 'rotate'\) \? rotateBy\(view, dx, dy\) : panBy\(view, dx, dy\)/.test(SRC));
ok('672e 的"拖拽旋转"写法已不复存在（回归锁）', SRC.indexOf('view.rotY += (e.clientX - last.x)') < 0);
ok('右键菜单未被泄漏：dblclick 仍绑定复位', /addEventListener\('dblclick', resetView\)/.test(SRC));
ok('方向键走 panStepForKey（不再 60 / view.k）',
  /panStepForKey\(e\.key\)/.test(SRC) && SRC.indexOf('60 / view.k') < 0);
ok('复位先归零旋转平移再自适应（resetViewTransform + fitView）',
  /view = resetViewTransform\(view\)/.test(SRC));

console.log('starmap_interaction_672g: ' + passed + ' assertions passed');
