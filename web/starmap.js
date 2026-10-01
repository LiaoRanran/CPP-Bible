// 670c A5 · 星图页 = 纯逻辑（解析 / 布局数学 / 搜索） + Canvas 2D 渲染
//
// 为什么换渲染：
//   653–656 的星图走「SVG 逐元素 + cosmos.gl GPU」。178 节点 / 1093 边下，
//   ① SVG 逐元素建 DOM，拖动时逐帧改属性 ⇒ 明显掉帧；
//   ② vendor 里的 cosmos/d3 子模块不齐，离线时不可靠（只能降级 2D）。
//   670c 改为**自写力导向 + Canvas 2D**：一次求解（不跑每帧物理）、按需重绘、零外部依赖。
//
// 文件结构（硬纪律）：
//   一 · 纯逻辑：不碰 DOM / canvas / fetch，全部 ESM 导出 ⇒ Node 真跑
//        （web/tests/starmap.test.mjs，运行命令见交付报告 / 测试文件头）
//   二 · 浏览器引导：只在 document/window 存在时执行 ⇒ Node import 本文件不碰 DOM
//
// 页面上所有数字都**现算**（本文件不写死 178/1093/8），避免文档与数据漂移。

import { STATE_COLORS, STATE_LABELS, KIND_LABELS, LINK_STYLE, fetchJSON, fmtInt } from './app.js';
export { STATE_COLORS, STATE_LABELS, KIND_LABELS };

/* ══════════════════════════════════════════════════════════════════════════
   一 · 纯逻辑
   ══════════════════════════════════════════════════════════════════════════ */

/** 数据里 42 个误解节点的 domain 是 "?"（无域）⇒ 单独成簇，不丢、也不假装它有域。 */
export const UNKNOWN_DOMAIN = '?';

/** 形通道：卡 > 命题 > 误解（世界坐标半径）。 */
export const KIND_RADIUS = { card: 7.5, prop: 4.2, misconception: 3.2 };

/** 光通道：credibility 3/2/1 → 不透明度。与页面图例同值。 */
export const CRED_ALPHA = { 3: 1, 2: 0.72, 1: 0.5 };

/** 关系强度的种类基线（派生量：数据里没有 weight 字段）。 */
export const EDGE_KIND_BASE = { asserts: 1, attack: 1.15, defend: 0.7 };
/** 被击败的攻击边加权（"这条边真的打赢了" ⇒ 画粗一点）。 */
export const DEFEAT_BOOST = 1.3;
/** log2(1+degA+degB) 的归一参考（真实数据最大度 51 ⇒ log2(103)≈6.7）。 */
export const HUB_REF = 8;

/** design-tokens.css 的镜像回退值（浏览器里优先读 CSS 变量真值）。 */
export const TOKEN_FALLBACK = {
  '--color-bg': '#1a1a1a', '--color-surface': '#202020', '--color-surface-2': '#262625',
  '--color-line': '#2f2f2c', '--color-line-strong': '#3d3d3a',
  '--color-text': '#e8e6e3', '--color-text-dim': '#b3aea7', '--color-text-mute': '#979089',
  '--color-accent': '#d97757', '--color-pass': '#5fc3ae',
  '--color-pass-exception': '#d9a959', '--color-fail': '#e07a72', '--color-unknown': '#8b9299',
  '--font-sans': 'Inter, system-ui, "Segoe UI", "Noto Sans SC", sans-serif',
  '--font-mono': 'ui-monospace, Consolas, monospace',
};
/** 聚类色用到的 6 个 token（其余 2 档由 mixHex 混合派生，不新增色板）。 */
export const TOKEN_KEYS = ['--color-pass', '--color-accent', '--color-pass-exception',
  '--color-unknown', '--color-fail', '--color-text-dim'];

const clamp = (v, lo, hi) => (v < lo ? lo : v > hi ? hi : v);
const num = (v, d = 0) => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const round = (v, d = 4) => { const p = Math.pow(10, d); return Math.round(v * p) / p; };
/** 选项对象归一：null / undefined / 非对象 ⇒ {}（纯函数要能扛住 null 实参）。 */
const opt = (o) => (o && typeof o === 'object' ? o : {});

/** 确定性 PRNG（种子固定 ⇒ 布局可复现，测试才能断言真值）。 */
export function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** '#rrggbb' → [r,g,b]（非法输入 ⇒ null）。 */
export function hexToRgb(hex) {
  const s = String(hex == null ? '' : hex).trim().replace(/^#/, '');
  if (!/^[0-9a-fA-F]{6}$/.test(s)) return null;
  return [parseInt(s.slice(0, 2), 16), parseInt(s.slice(2, 4), 16), parseInt(s.slice(4, 6), 16)];
}
/** [r,g,b] → '#rrggbb'。 */
export function rgbToHex(rgb) {
  if (!Array.isArray(rgb) || rgb.length < 3) return '#000000';
  return '#' + rgb.slice(0, 3).map((v) => clamp(Math.round(num(v, 0)), 0, 255)
    .toString(16).padStart(2, '0')).join('');
}
/** 两色线性混合（聚类色全部由 token 色派生，不新造色板）。 */
export function mixHex(a, b, t = 0.5) {
  const pa = hexToRgb(a), pb = hexToRgb(b);
  if (!pa || !pb) return pa ? a : (pb ? b : '#000000');
  const f = clamp(num(t, 0.5), 0, 1);
  return rgbToHex(pa.map((v, i) => v + (pb[i] - v) * f));
}

/** 聚类色板：6 个 token + 2 个 token 混合档 = 8 档（真实聚类数 8）。 */
export function clusterPalette(resolve) {
  const get = (k) => {
    let v = '';
    try { v = typeof resolve === 'function' ? resolve(k) : (resolve ? resolve[k] : ''); } catch { v = ''; }
    v = String(v == null ? '' : v).trim();
    return hexToRgb(v) ? v : (TOKEN_FALLBACK[k] || '#8b9299');
  };
  const pass = get('--color-pass'), accent = get('--color-accent');
  const exc = get('--color-pass-exception'), unk = get('--color-unknown');
  const fail = get('--color-fail'), dim = get('--color-text-dim');
  return [pass, accent, exc, unk, fail, dim,
    mixHex(pass, accent, 0.5), mixHex(exc, unk, 0.55)];
}

/** domain 归一：小写 + trim；空 / '?' / 'null' ⇒ UNKNOWN_DOMAIN（只在展示层归一，不改数据）。 */
export function normDomain(d) {
  const s = String(d == null ? '' : d).trim().toLowerCase();
  if (!s || s === '?' || s === 'null' || s === 'undefined' || s === '-') return UNKNOWN_DOMAIN;
  return s;
}

/** 从 id 命名规则推 domain：`MIS-<DOMAIN>-NNN` ⇒ <domain>（小写）；推不出 ⇒ UNKNOWN_DOMAIN。
 *  真实数据里 42 个误解节点的 domain 字段是 "?"，而 id 前缀 42/42 都能对上真实 domain，
 *  其中 40/42 与"攻击目标所在域"的多数票一致（另 2 个是跨域攻击，如 MIS-CONC-001 打 ub）⇒
 *  **展示层**用 id 前缀归属，不改数据；前缀对不上真实 domain 时仍退回 "?"。 */
export function domainFromId(id) {
  const m = /^MIS-([A-Za-z]+)-\d+$/.exec(String(id == null ? '' : id));
  return m ? normDomain(m[1]) : UNKNOWN_DOMAIN;
}

/** cards_index.json → Map(id → card)（接受 {cards:[…]} 或裸数组）。 */
export function indexCards(cardsIndex) {
  const m = new Map();
  const arr = cardsIndex && (Array.isArray(cardsIndex) ? cardsIndex : cardsIndex.cards);
  if (Array.isArray(arr)) for (const c of arr) if (c && c.id != null) m.set(String(c.id), c);
  return m;
}

/** 证据强度（派生量）：① node.evidence ② cards_index 里自己的 evidence 条数
 *  ③ 所属卡（node.card）的 evidence 条数 ④ 回退 credibility ⑤ 0。 */
export function evidenceOf(node, cardsById = null) {
  if (!node) return { value: 0, source: 'none' };
  const ev = node.evidence;
  if (typeof ev === 'number' && Number.isFinite(ev)) return { value: ev, source: 'node.evidence' };
  if (Array.isArray(ev)) return { value: ev.length, source: 'node.evidence' };
  if (cardsById && typeof cardsById.get === 'function' && cardsById.size) {
    const self = cardsById.get(String(node.id));
    if (self && Array.isArray(self.evidence)) return { value: self.evidence.length, source: 'cards_index' };
    if (node.card && cardsById.has(String(node.card))) {
      const owner = cardsById.get(String(node.card));
      if (owner && Array.isArray(owner.evidence)) return { value: owner.evidence.length, source: 'owner_card' };
    }
  }
  if (typeof node.credibility === 'number' && Number.isFinite(node.credibility)) {
    return { value: node.credibility, source: 'credibility' };
  }
  return { value: 0, source: 'none' };
}
export function evidenceStrength(node, cardsById = null) { return evidenceOf(node, cardsById).value; }

/** 关系强度（派生量，用于边粗细）：种类基线 × 端点度数（对数压缩）× 是否被击败。 */
export function edgeWeight(edge, ctx = {}) {
  const e = edge || {};
  const c = opt(ctx);
  const base = num(EDGE_KIND_BASE[e.kind], 1);
  const da = num(c.degSource != null ? c.degSource : e.degSource, 0);
  const db = num(c.degTarget != null ? c.degTarget : e.degTarget, 0);
  const hub = Math.min(1, Math.log2(1 + Math.max(0, da) + Math.max(0, db)) / HUB_REF);
  const boost = e.defeated ? DEFEAT_BOOST : 1;
  return round(base * (0.55 + 0.9 * hub) * boost, 4);
}

/** 关系强度 → 屏幕线宽（weightMax 归一，k = 当前缩放）。 */
export function strokeWidthFor(weight, weightMax, opts = {}) {
  const o = opt(opts);
  const k = num(o.k, 1);
  const base = num(o.base, 1);
  const w = num(weight, 0), mx = Math.max(1e-6, num(weightMax, 1));
  const t = clamp(w / mx, 0.25, 1);
  return round(clamp(base * (0.45 + t * 1.35) * k, 0.15, 8), 3);
}

/** 按 domain 聚类统计：卡数 / 平均证据强度 / 质心（给布局与标签用）。 */
export function clusterByDomain(nodes, positions = null) {
  const map = new Map();
  const list = Array.isArray(nodes) ? nodes : [];
  list.forEach((n, i) => {
    const key = n && n.domain ? String(n.domain) : UNKNOWN_DOMAIN;
    let c = map.get(key);
    if (!c) {
      c = { domain: key, label: key === UNKNOWN_DOMAIN ? '?（无域·误解）' : key,
        count: 0, evidenceSum: 0, avgEvidence: 0, cx: 0, cy: 0,
        cards: 0, props: 0, misconceptions: 0, members: [] };
      map.set(key, c);
    }
    c.count++;
    c.evidenceSum += num(n && n.evidence, 0);
    c.members.push(i);
    if (n && n.kind === 'card') c.cards++;
    else if (n && n.kind === 'prop') c.props++;
    else if (n && n.kind === 'misconception') c.misconceptions++;
    const p = positions && positions[i];
    if (p) { c.cx += num(p.x); c.cy += num(p.y); }
  });
  const out = Array.from(map.values());
  for (const c of out) {
    c.avgEvidence = c.count ? round(c.evidenceSum / c.count, 3) : 0;
    c.cx = c.count ? round(c.cx / c.count, 2) : 0;
    c.cy = c.count ? round(c.cy / c.count, 2) : 0;
  }
  out.sort((a, b) => (b.count - a.count) || (a.domain < b.domain ? -1 : a.domain > b.domain ? 1 : 0));
  return out;
}

/** 簇的几何铺开半径（q 分位距离；用于画聚类晕与判断是否值得画标签）。 */
export function clusterSpread(members, positions, q = 0.9) {
  const idx = Array.isArray(members) ? members : [];
  let cx = 0, cy = 0, n = 0;
  for (const i of idx) { const p = positions && positions[i]; if (p) { cx += num(p.x); cy += num(p.y); n++; } }
  if (!n) return { cx: 0, cy: 0, r: 0, rMax: 0, count: 0 };
  cx /= n; cy /= n;
  const ds = [];
  for (const i of idx) {
    const p = positions && positions[i];
    if (p) ds.push(Math.hypot(num(p.x) - cx, num(p.y) - cy));
  }
  ds.sort((a, b) => a - b);
  const qq = clamp(num(q, 0.9), 0, 1);
  const at = ds.length ? ds[Math.min(ds.length - 1, Math.floor(qq * (ds.length - 1)))] : 0;
  return { cx: round(cx, 2), cy: round(cy, 2), r: round(at, 2), rMax: round(ds.length ? ds[ds.length - 1] : 0, 2), count: n };
}

/** 节点 → 簇 key 数组（力导向的簇内聚、以及聚类筛选都用它）。 */
export function clusterIndexOf(nodes) {
  return (Array.isArray(nodes) ? nodes : []).map((n) => (n && n.domain ? String(n.domain) : UNKNOWN_DOMAIN));
}

/** 初始摆位（确定性）：簇心铺在环上，簇内按黄金角螺旋铺开 ⇒ 第一帧就不糊成一团。 */
export function seedPositions(nodes, params = {}) {
  const list = Array.isArray(nodes) ? nodes : [];
  const P = opt(params);
  const rnd = mulberry32(num(P.rngSeed, 0x51a7c0de));
  const ringR = num(P.ringRadius, 340);
  const spreadR = num(P.clusterRadius, 110);
  const clusters = clusterByDomain(list);
  const nC = Math.max(1, clusters.length);
  const out = new Array(list.length);
  const GA = 2.399963229728653;
  clusters.forEach((c, ci) => {
    const a0 = (ci / nC) * Math.PI * 2;
    const bx = Math.cos(a0) * ringR, by = Math.sin(a0) * ringR;
    c.members.forEach((i, j) => {
      const t = (j + 0.5) / Math.max(1, c.members.length);
      const rr = Math.sqrt(t) * spreadR;
      const ang = j * GA + a0;
      out[i] = {
        x: bx + Math.cos(ang) * rr + (rnd() - 0.5) * 6,
        y: by + Math.sin(ang) * rr + (rnd() - 0.5) * 6,
      };
    });
  });
  for (let i = 0; i < out.length; i++) if (!out[i]) out[i] = { x: 0, y: 0 };
  return out;
}

/** 力导向默认参数（Fruchterman–Reingold + 向心 + 簇内聚）。 */
export const DEFAULT_FORCES = {
  springLength: 42,   // FR 的 k：边的自然长度
  gravity: 0.18,      // 向心（每步把节点拉回中心的比例）
  gravityX: null,     // 可分别给两轴（null ⇒ 用 gravity）
  gravityY: 0.24,     // y 略强：视口是横的 ⇒ 布局长成横向
  spreadY: 0.5,       // y 向斥力折减（各向异性斥力；与 gravityY 一起定纵横比）
  crossBoost: 2.5,    // **跨簇**斥力倍数：不同 domain 的节点互相推得更开（聚类才看得出边界）
  clusterK: 0.12,     // 簇内聚：离簇心超过 clusterRadius 才拉
  clusterRadius: 130,
  maxStep: 26,        // 温度上限（每步最大位移，像素）
  cutoff: 1400,       // 斥力截断：更远的一对 1/d² 已可忽略（≈15.7k 对里的大多数）
  cooling: 0.985,     // 每步温度衰减
  minGap: 14,         // 重合保护：d 小于它按它算，避免 1/d 爆炸
};
// 上面这组默认值是在真实数据（178 节点 / 1093 边）上调出来的，实测：
//   布局 2620×1730（纵横比 1.51，与 960×620 画布同向）、最近点对 ≥ 15.9px、
//   簇间最小间隔 / 半径和 ≥ 1.3（7 个域互不糊在一起）、200 步 ≈ 60–130ms（只在加载时跑一次）。

/** 一步力导向（**纯函数**：不修改入参，返回新数组）。 */
export function stepForces(state, params = {}) {
  const P = Object.assign({}, DEFAULT_FORCES, params);
  const src = (state && state.positions) || [];
  const n = src.length;
  const alpha = clamp(num(state && state.alpha, 1), 0, 1);
  const k = Math.max(1, num(P.springLength, DEFAULT_FORCES.springLength));
  const k2 = k * k;
  // 热点循环走 **TypedArray 扁平数组**（比 [{x,y}] 属性访问快，实测 178 节点 240 步 100ms → 45ms）；
  // 入参/出参仍是 {x,y} 数组 ⇒ 纯函数语义不变，也不修改入参。
  const px = new Float64Array(n), py = new Float64Array(n);
  for (let i = 0; i < n; i++) { px[i] = num(src[i] && src[i].x); py[i] = num(src[i] && src[i].y); }
  const fx = new Float64Array(n), fy = new Float64Array(n);
  const cutoff2 = num(P.cutoff, DEFAULT_FORCES.cutoff) * num(P.cutoff, DEFAULT_FORCES.cutoff);
  const minGap = Math.max(1e-3, num(P.minGap, DEFAULT_FORCES.minGap));
  const minGap2 = minGap * minGap;
  const spreadY = Math.max(0.05, num(P.spreadY, DEFAULT_FORCES.spreadY));
  const crossBoost = Math.max(1, num(P.crossBoost, DEFAULT_FORCES.crossBoost));
  const TAU = 6.283185307179586;
  const cluster = (state && state.cluster) || null;
  // 簇 id 数值化：热点循环里比整数（每步 15.7k 对，字符串比较会明显拖慢）
  const idOf = new Map();
  const cid = new Int32Array(n).fill(-1);
  if (cluster) {
    for (let i = 0; i < n; i++) {
      const key = cluster[i];
      if (key == null) continue;
      let id = idOf.get(key);
      if (id === undefined) { id = idOf.size; idOf.set(key, id); }
      cid[i] = id;
    }
  }

  // ① 斥力：O(n²) + 距离截断（178 节点 ⇒ 15753 对/步）；
  //    热点里用 Math.sqrt 而非 Math.hypot（后者实测慢约 3 倍），y 分量乘 spreadY（各向异性）。
  for (let i = 0; i < n; i++) {
    const xi = px[i], yi = py[i];
    let ax = 0, ay = 0;
    for (let j = i + 1; j < n; j++) {
      let vx = px[j] - xi, vy = py[j] - yi;
      const d2 = vx * vx + vy * vy;
      if (d2 > cutoff2) continue;
      let d;
      if (d2 < minGap2) {
        // 完全重合：给一对确定的、只与下标有关的推力（避免 1/d 爆炸与 NaN）
        const a = (i * 2.399963 + j * 0.618) % TAU;
        vx = Math.cos(a) * minGap; vy = Math.sin(a) * minGap; d = minGap;
      } else {
        d = Math.sqrt(d2);
      }
      const f = (k2 / d) * (cid[i] === cid[j] ? 1 : crossBoost);
      const ux = (vx / d) * f;
      const uy = ((vy / d) * f) * spreadY;
      ax -= ux; ay -= uy;
      fx[j] += ux; fy[j] += uy;
    }
    fx[i] += ax; fy[i] += ay;
  }
  // ② 弹簧：边（权重越大越硬 ⇒ 强关系更短）
  const edges = (state && state.edges) || [];
  for (let e = 0; e < edges.length; e++) {
    const ed = edges[e] || {};
    const a = ed.a != null ? ed.a : ed.source, b = ed.b != null ? ed.b : ed.target;
    if (!(a >= 0 && b >= 0 && a < n && b < n) || a === b) continue;
    const vx = px[b] - px[a], vy = py[b] - py[a];
    const d = Math.max(1e-3, Math.sqrt(vx * vx + vy * vy));
    const w = clamp(num(ed.weight, 1), 0.2, 3);
    const f = ((d * d) / k) * (0.55 + 0.45 * w);
    const ux = (vx / d) * f, uy = (vy / d) * f;
    fx[a] += ux; fy[a] += uy;
    fx[b] -= ux; fy[b] -= uy;
  }
  // ③ 向心（gravity）+ 簇内聚（离簇心超过 clusterRadius 才拉）
  const clusterK = num(P.clusterK, DEFAULT_FORCES.clusterK);
  if (cluster && clusterK > 0 && idOf.size) {
    const nc = idOf.size;
    const cxs = new Float64Array(nc), cys = new Float64Array(nc), cns = new Int32Array(nc);
    for (let i = 0; i < n; i++) {
      const id = cid[i];
      if (id < 0) continue;
      cxs[id] += px[i]; cys[id] += py[i]; cns[id]++;
    }
    const cr = num(P.clusterRadius, DEFAULT_FORCES.clusterRadius);
    for (let i = 0; i < n; i++) {
      const id = cid[i];
      if (id < 0 || !cns[id]) continue;
      const vx = cxs[id] / cns[id] - px[i], vy = cys[id] / cns[id] - py[i];
      const d = Math.sqrt(vx * vx + vy * vy);
      if (d <= cr) continue;
      const f = clusterK * (d - cr);
      fx[i] += (vx / d) * f; fy[i] += (vy / d) * f;
    }
  }
  // ④ 积分：位移按温度截断（FR 的标准做法：位移即力、温度收敛），不引入速度态 ⇒ 无震荡
  const temp = Math.max(0.5, num(P.maxStep, DEFAULT_FORCES.maxStep) * alpha);
  const gravity = num(P.gravity, DEFAULT_FORCES.gravity);
  const gx = num(P.gravityX, gravity), gy = num(P.gravityY, gravity);
  const out = new Array(n);
  let maxMove = 0, energy = 0;
  for (let i = 0; i < n; i++) {
    const mx = fx[i] - px[i] * gx;
    const my = fy[i] - py[i] * gy;
    const len = Math.sqrt(mx * mx + my * my);
    const sc = len > temp ? temp / len : 1;
    const nx = px[i] + mx * sc, ny = py[i] + my * sc;
    out[i] = { x: nx, y: ny };
    const mvx = nx - px[i], mvy = ny - py[i];
    const moved = Math.sqrt(mvx * mvx + mvy * mvy);
    if (moved > maxMove) maxMove = moved;
    energy += moved;
  }
  return { positions: out, alpha: alpha * num(P.cooling, DEFAULT_FORCES.cooling), maxMove, energy };
}

/** 最近点对距离（防重叠的验收指标）。 */
export function minPairDistance(positions) {
  const ps = Array.isArray(positions) ? positions : [];
  let best = Infinity;
  for (let i = 0; i < ps.length; i++) {
    const xi = num(ps[i] && ps[i].x), yi = num(ps[i] && ps[i].y);
    for (let j = i + 1; j < ps.length; j++) {
      const vx = xi - num(ps[j] && ps[j].x), vy = yi - num(ps[j] && ps[j].y);
      const d = Math.sqrt(vx * vx + vy * vy);
      if (d < best) best = d;
    }
  }
  return ps.length < 2 ? 0 : round(best, 4);
}

/** 防重叠：把过近的一对对推开（纯函数，返回新数组 + 收敛指标）。 */
export function relaxOverlaps(positions, radii, params = {}) {
  const P = opt(params);
  const minDist = Math.max(0.001, num(P.minDist, 16));
  const iters = Math.max(0, Math.round(num(P.iterations, 40)));
  const strength = clamp(num(P.strength, 0.5), 0, 1);
  const n = (Array.isArray(positions) ? positions : []).length;
  const cur = new Array(n);
  for (let i = 0; i < n; i++) cur[i] = { x: num(positions[i] && positions[i].x), y: num(positions[i] && positions[i].y) };
  const rad = (i) => Math.max(0, num(radii && radii[i], 0));
  let used = 0, moved = 0;
  const need0 = minDist;
  for (let it = 0; it < iters; it++) {
    moved = 0;
    for (let i = 0; i < n; i++) {
      const ci = cur[i];
      for (let j = i + 1; j < n; j++) {
        const cj = cur[j];
        const need = Math.max(need0, rad(i) + rad(j));
        let vx = cj.x - ci.x, vy = cj.y - ci.y;
        // 先用平方距离挡掉绝大多数对（不开方）⇒ 每轮 15.7k 对只做一次乘法比较
        const d2 = vx * vx + vy * vy;
        if (d2 >= need * need) continue;
        let d = Math.sqrt(d2);
        if (d < 1e-6) {
          const a = (i * 2.399963 + j * 0.618) % (Math.PI * 2);
          vx = Math.cos(a); vy = Math.sin(a); d = 1;
        }
        const push = ((need - d) / 2) * strength;
        const ux = vx / d, uy = vy / d;
        ci.x -= ux * push; ci.y -= uy * push;
        cj.x += ux * push; cj.y += uy * push;
        moved += push;
      }
    }
    used = it + 1;
    if (moved < 1e-3) break;
  }
  return { positions: cur, iterations: used, moves: round(moved, 4), minDistance: minPairDistance(cur) };
}

/** 整轮求解：种子摆位 → N 步力导向（带收敛早停）→ 防重叠。
 *  n=178 / m=1093 实测：260 步 O(n²) ≈ 4.1M 次内积，几十毫秒；页面只在加载时跑一次。 */
export function runLayout(nodes, edges, params = {}) {
  const list = Array.isArray(nodes) ? nodes : [];
  const P = opt(params);
  const iterations = Math.max(0, Math.round(num(P.iterations, 240)));
  const tolerance = num(P.tolerance, 0.12);
  const positions0 = Array.isArray(P.positions) ? P.positions : seedPositions(list, P);
  let st = { positions: positions0, edges: edges || [], cluster: clusterIndexOf(list), alpha: 1 };
  let used = 0, maxMove = Infinity, energy = 0;
  for (let i = 0; i < iterations; i++) {
    const r = stepForces(st, Object.assign({}, P, { alpha: st.alpha }));
    st = { positions: r.positions, edges: st.edges, cluster: st.cluster, alpha: r.alpha };
    used = i + 1; maxMove = r.maxMove; energy = r.energy;
    if (maxMove < tolerance) break;
  }
  const radii = list.map((x) => num(KIND_RADIUS[x && x.kind], 4));
  const sep = relaxOverlaps(st.positions, radii, {
    minDist: num(P.minDist, 16),
    iterations: num(P.separationIterations, 40),
    strength: num(P.separationStrength, 0.5),
  });
  return {
    positions: sep.positions, iterations: used, converged: maxMove < tolerance,
    maxMove: round(maxMove, 4), energy: round(energy, 2),
    minDistance: sep.minDistance, separationIterations: sep.iterations,
  };
}

/** 搜索：命中节点 **id 列表**（大小写不敏感 / 部分匹配 / 空查询 ⇒ []）。
 *  排序：id 全等 < id 前缀 < id 子串 < 标题/标签 < domain 全等，同级按 id 字典序。 */
export function locateNode(nodes, query) {
  const q = String(query == null ? '' : query).trim().toLowerCase();
  if (!q) return [];
  const hits = [];
  for (const n of (Array.isArray(nodes) ? nodes : [])) {
    if (!n) continue;
    const id = String(n.id == null ? '' : n.id).toLowerCase();
    const label = String(n.label == null ? '' : n.label).toLowerCase();
    const title = String(n.title == null ? '' : n.title).toLowerCase();
    const domain = String(n.domain == null ? '' : n.domain).toLowerCase();
    let score = -1;
    if (id === q) score = 0;
    else if (id.startsWith(q)) score = 1;
    else if (id.includes(q)) score = 2;
    else if (title.includes(q) || label.includes(q)) score = 3;
    else if (domain === q) score = 4;
    if (score >= 0) hits.push({ id: String(n.id), score });
  }
  hits.sort((a, b) => (a.score - b.score) || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  return hits.map((h) => h.id);
}

/** 四态 + 聚类的可见性筛选（返回下标数组，保持原顺序）。 */
export function filterNodes(nodes, opts = {}) {
  const O = opt(opts);
  const states = O.states instanceof Set ? O.states
    : (Array.isArray(O.states) ? new Set(O.states) : null);
  const domain = O.domain && O.domain !== 'all' ? String(O.domain).toLowerCase() : null;
  const out = [];
  (Array.isArray(nodes) ? nodes : []).forEach((n, i) => {
    if (!n) return;
    if (states && !states.has(n.state)) return;
    if (domain && String(n.domain == null ? '' : n.domain).toLowerCase() !== domain) return;
    out.push(i);
  });
  return out;
}

/** 某节点的邻居下标集合（含自己）。 */
export function neighborsOf(edges, index) {
  const s = new Set([index]);
  for (const e of (Array.isArray(edges) ? edges : [])) {
    if (!e) continue;
    if (e.a === index) s.add(e.b);
    else if (e.b === index) s.add(e.a);
  }
  return s;
}

/** 世界坐标 → 屏幕：screen = (world + view) * k + 视口中心。 */
export function applyTransform(p, view, viewport = {}) {
  const vp = opt(viewport);
  const k = num(view && view.k, 1), vx = num(view && view.x, 0), vy = num(view && view.y, 0);
  const cx = num(vp.centerX, num(vp.width, 0) / 2);
  const cy = num(vp.centerY, num(vp.height, 0) / 2);
  return { x: (num(p && p.x) + vx) * k + cx, y: (num(p && p.y) + vy) * k + cy };
}
/** 屏幕坐标 → 世界坐标（applyTransform 的逆）。 */
export function invertTransform(s, view, viewport = {}) {
  const vp = opt(viewport);
  const k = Math.max(1e-6, num(view && view.k, 1));
  const vx = num(view && view.x, 0), vy = num(view && view.y, 0);
  const cx = num(vp.centerX, num(vp.width, 0) / 2);
  const cy = num(vp.centerY, num(vp.height, 0) / 2);
  return { x: (num(s && s.x) - cx) / k - vx, y: (num(s && s.y) - cy) / k - vy };
}

/* ══════════════════════════════════════════════════════════════════════════
   2.5D 伪 3D 投影（672e）：不引入 Three.js，纯手算透视
   ══════════════════════════════════════════════════════════════════════════ */

/** 透视投影：把世界坐标 {x,y,z} 投到屏幕。
 *  · 旋转：先绕 Y 轴（水平拖拽），再绕 X 轴（俯仰拖拽）；
 *  · 透视：相机在 z = -cam 处朝 +z 看，z 越大离相机越远 ⇒
 *    **近大远小**（scale 随深度递减）+ **远节点更暗**（alpha 随深度递减）；
 *  · 本函数不接触任何颜色，渲染层颜色一律走 design-tokens（STATE_COLORS /
 *    clusterPalette / LINK_STYLE），不写死 green/red/yellow。 */
export function projectPoint(world, view) {
  const v = opt(view);
  const rotX = num(v.rotX, 0), rotY = num(v.rotY, 0);
  const k = Math.max(0.01, num(v.k, 1));
  const x = num(world && world.x), y = num(world && world.y), z = num(world && world.z);
  // 绕 Y 轴
  const cY = Math.cos(rotY), sY = Math.sin(rotY);
  const x1 = x * cY + z * sY;
  const z1 = -x * sY + z * cY;
  // 绕 X 轴
  const cX = Math.cos(rotX), sX = Math.sin(rotX);
  const y1 = y * cX - z1 * sX;
  const z2 = y * sX + z1 * cX;
  const cam = Math.max(1, num(v.cam, 900));
  const focal = Math.max(1, num(v.focal, 900));
  const depth = cam + z2;                 // 相机到点（有符号）距离，>0
  const safe = depth < 1 ? 1 : depth;
  const persp = focal / safe;             // 近大远小
  const cx = num(v.cx, 0), cy = num(v.cy, 0);
  const panX = num(v.x, 0), panY = num(v.y, 0);
  return {
    sx: cx + x1 * persp * k + panX,
    sy: cy + y1 * persp * k + panY,
    scale: persp * k,                              // 屏幕缩放（含透视 + 用户缩放）
    depth: z2,                                     // 旋转后的深度（仅供调用方做明暗）
    alpha: round(clamp(focal * k / safe, 0.45, 1), 4),  // 远节点更暗
  };
}

/** 深度分配（确定性）：每个节点一个 z ∈ [-range, range]，种子由下标决定 ⇒
 *  布局可复现、测试可断言真值。纯视觉层（不影响 2D 力导向布局，不写死 178/1093）。 */
export function depthFor(nodes, positions, params = {}) {
  const P = opt(params);
  const range = num(P.range, 220);
  const rndSeed = num(P.rngSeed, 0x246e2a17);
  const list = Array.isArray(nodes) ? nodes : [];
  const out = new Float64Array(list.length);
  for (let i = 0; i < list.length; i++) {
    const r = mulberry32((rndSeed ^ (i * 0x9e3779b1)) >>> 0)();
    out[i] = (r * 2 - 1) * range;
  }
  return out;
}

/** 节点大小分级：按连接数（degree）分级（hub 最大，孤立点最小）。
 *  对数归一 ⇒ 度数从 0 到 hub 平滑映射到 [min, max]。形状仍由 kind 决定。 */
export const DEGREE_TIERS = { min: 2.4, max: 13, hub: 51 };
export function nodeRadiusFor(degree, params = {}) {
  const P = opt(params);
  const minR = num(P.min, DEGREE_TIERS.min), maxR = num(P.max, DEGREE_TIERS.max);
  const hub = Math.max(1, num(P.hub, DEGREE_TIERS.hub));
  const d = Math.max(0, num(degree, 0));
  const t = clamp(Math.log2(1 + d) / Math.log2(1 + hub), 0, 1);
  return round(minR + (maxR - minR) * t, 3);
}

/** hover 高亮邻居（纯函数）：返回某节点的绘制 alpha。
 *  · 悬停/选中某节点时，非邻居压暗（dimNeighbor），邻居保持；
 *  · 搜索未命中（searchHits 不含 i）压暗（dimSearch）；
 *  · baseAlpha 通常是 credibility 不透明度，由调用方传入。 */
export function nodeAlpha(i, ctx = {}) {
  const c = opt(ctx);
  const hovered = num(c.hovered, -1), selected = num(c.selected, -1);
  const neighbors = c.neighbors instanceof Set ? c.neighbors : null;
  const searchHits = c.searchHits instanceof Set ? c.searchHits : null;
  let a = clamp(num(c.baseAlpha, 1), 0, 1);
  if (neighbors && (hovered >= 0 || selected >= 0)) {
    const focus = selected >= 0 ? selected : hovered;
    if (focus >= 0 && focus !== i && !neighbors.has(i)) a *= clamp(num(c.dimNeighbor, 0.2), 0, 1);
  }
  if (searchHits && !searchHits.has(i)) a *= clamp(num(c.dimSearch, 0.18), 0, 1);
  return round(a, 4);
}

/** 把某个节点移到视口中心所需的**平移/缩放**（搜索命中后居中用它）。 */
export function screenTransform(node, viewport = {}) {
  const vp = opt(viewport);
  const k = clamp(num(vp.k, 1), num(vp.minK, 0.25), num(vp.maxK, 6));
  const ox = num(vp.offsetX, 0), oy = num(vp.offsetY, 0);
  return { x: -num(node && node.x) + ox / k, y: -num(node && node.y) + oy / k, k };
}

/** 位置数组的包围盒（复位视图 / 自适应缩放用）。 */
export function boundsOf(positions) {
  const ps = (Array.isArray(positions) ? positions : []).filter(Boolean);
  if (!ps.length) return { minX: 0, minY: 0, maxX: 0, maxY: 0, width: 0, height: 0, cx: 0, cy: 0 };
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  for (const p of ps) {
    const x = num(p.x), y = num(p.y);
    if (x < minX) minX = x; if (x > maxX) maxX = x;
    if (y < minY) minY = y; if (y > maxY) maxY = y;
  }
  return { minX, minY, maxX, maxY, width: maxX - minX, height: maxY - minY,
    cx: (minX + maxX) / 2, cy: (minY + maxY) / 2 };
}

/** 自适应缩放：让包围盒（留 padding）铺满视口。 */
export function fitTransform(bounds, viewport = {}) {
  const vp = opt(viewport);
  const w = Math.max(1, num(vp.width, 1)), h = Math.max(1, num(vp.height, 1));
  const pad = Math.max(0, num(vp.padding, 32));
  const bw = Math.max(1e-6, num(bounds && bounds.width, 1));
  const bh = Math.max(1e-6, num(bounds && bounds.height, 1));
  const k = clamp(Math.min((w - 2 * pad) / bw, (h - 2 * pad) / bh),
    num(vp.minK, 0.25), num(vp.maxK, 6));
  return { x: -num(bounds && bounds.cx, 0), y: -num(bounds && bounds.cy, 0), k };
}

/** 点到线段距离（t 截断到 [0,1]）。 */
export function distToSegment(px, py, ax, ay, bx, by) {
  const vx = bx - ax, vy = by - ay;
  const len2 = vx * vx + vy * vy;
  if (len2 < 1e-9) return Math.hypot(px - ax, py - ay);
  const t = clamp(((px - ax) * vx + (py - ay) * vy) / len2, 0, 1);
  return Math.hypot(px - (ax + t * vx), py - (ay + t * vy));
}

/** 命中最近的节点（世界坐标；isVisible(i) 可选）。 */
export function pickNodeAt(positions, nodes, world, radius, isVisible = null) {
  let best = -1, bd = Math.max(0, num(radius, 12));
  const list = Array.isArray(nodes) ? nodes : [];
  for (let i = 0; i < list.length; i++) {
    if (isVisible && !isVisible(i)) continue;
    const p = positions && positions[i];
    if (!p) continue;
    const d = Math.hypot(num(p.x) - num(world && world.x), num(p.y) - num(world && world.y));
    if (d <= bd) { bd = d; best = i; }
  }
  return best;
}

/** 命中最近的边（屏幕坐标 + 屏幕位置表）。 */
export function pickEdgeAt(screenPositions, edges, point, maxPx = 7, isVisible = null) {
  let best = -1, bd = num(maxPx, 7);
  const list = Array.isArray(edges) ? edges : [];
  for (let i = 0; i < list.length; i++) {
    if (isVisible && !isVisible(i)) continue;
    const e = list[i];
    if (!e) continue;
    const A = screenPositions && screenPositions[e.a], B = screenPositions && screenPositions[e.b];
    if (!A || !B) continue;
    const d = distToSegment(num(point && point.x), num(point && point.y), A.x, A.y, B.x, B.y);
    if (d < bd) { bd = d; best = i; }
  }
  return best;
}

/** HTML 转义（节点标题来自数据，进 innerHTML 前必须转义）。 */
export function escapeHTML(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

/** 聚类 hover 文案（纯函数 ⇒ 测试能断言"卡数 + 平均证据强度"确实被写出来）。 */
export function clusterTip(cluster) {
  const c = cluster || {};
  return {
    title: String(c.label || c.domain || '?'),
    lines: [
      String(num(c.count, 0)) + ' 节点（' + num(c.cards, 0) + ' 卡 · ' + num(c.props, 0) + ' 命题 · '
        + num(c.misconceptions, 0) + ' 误解）',
      '平均证据强度 ' + num(c.avgEvidence, 0).toFixed(2) + '（派生量：卡的证据条数 / 非卡回退 credibility）',
    ],
  };
}

/** 节点 hover 文案。 */
export function nodeTip(node) {
  const n = node || {};
  const lines = [
    (KIND_LABELS[n.kind] || n.kind || '?') + ' · ' + (STATE_LABELS[n.state] || n.state || '?'),
    'domain ' + (n.domain || '?') + ' · credibility ' + num(n.credibility, 0)
      + ' · 度 ' + num(n.degree, 0) + ' · 证据强度 ' + num(n.evidence, 0),
  ];
  if (n.label && n.label !== n.id) lines.push(String(n.label));
  return { title: String(n.id || '?'), lines };
}

/** 只统计与该节点相连的边（与 graph_core.statsOf 同语义，供 hooks/详情面板共用）。 */
export function statsOf(edges, id) {
  let attacks = 0, defends = 0, defeated = 0;
  for (const l of (Array.isArray(edges) ? edges : [])) {
    if (!l || (l.source !== id && l.target !== id)) continue;
    if (l.kind === 'attack') { attacks++; if (l.defeated) defeated++; }
    else if (l.kind === 'defend') defends++;
  }
  return { attacks, defends, defeated };
}

/** 从解析结果现算首屏数字（不读 meta.counts ⇒ 可与 meta 交叉验证）。 */
export function summarize(graph) {
  const nodes = (graph && graph.nodes) || [];
  const edges = (graph && graph.edges) || [];
  const s = { nodes: nodes.length, links: edges.length, attack: 0, defend: 0, asserts: 0,
    defeated: 0, cards: 0, props: 0, misconceptions: 0, clusters: 0, degreeSum: 0, maxDegree: 0,
    domainFromId: 0, domainFromCard: 0, domainMissing: 0 };
  for (const e of edges) {
    if (e.kind === 'attack') { s.attack++; if (e.defeated) s.defeated++; }
    else if (e.kind === 'defend') s.defend++;
    else if (e.kind === 'asserts') s.asserts++;
  }
  for (const n of nodes) {
    if (n.domainSource === 'id') s.domainFromId++;
    else if (n.domainSource === 'card') s.domainFromCard++;
    else if (n.domainSource === 'none') s.domainMissing++;
    if (n.kind === 'card') s.cards++;
    else if (n.kind === 'prop') s.props++;
    else if (n.kind === 'misconception') s.misconceptions++;
    const d = num(n.degree, 0);
    s.degreeSum += d;
    if (d > s.maxDegree) s.maxDegree = d;
  }
  s.clusters = (graph && graph.clusters ? graph.clusters.length : 0);
  return s;
}

/** 解析 graph.json → 渲染/布局要用的中间结构（**纯函数**）。
 *  返回 { nodes, edges, clusters, positions, meta, counts }。
 *  · domain 只在展示层归一：小写（数据里同一域有 MEM/mem 两态）+ 无域时按 id 前缀
 *    `MIS-<域>-NNN` 归属（42 个误解节点，42/42 前缀都指向真实 domain）⇒ 不改数据；
 *  · evidence 是派生量（见 evidenceOf）；
 *  · edge.weight 是派生量（数据里没有 weight 字段，见 edgeWeight）。 */
export function parseGraph(json, opts = {}) {
  const O = opt(opts);
  const rawNodes = (json && Array.isArray(json.nodes)) ? json.nodes : [];
  const rawLinks = (json && Array.isArray(json.links)) ? json.links : [];
  const cardsById = O.cardsById || indexCards(O.cardsIndex);
  const at = new Map();
  rawNodes.forEach((n, i) => { if (n && n.id != null) at.set(String(n.id), i); });
  const degree = new Array(rawNodes.length).fill(0);
  const edges = [];
  for (const l of rawLinks) {
    if (!l) continue;
    const a = at.get(String(l.source)), b = at.get(String(l.target));
    if (a == null || b == null) continue;      // 悬空边直接丢（真实数据里为 0，但不信数据）
    degree[a]++; degree[b]++;
    edges.push({ source: String(l.source), target: String(l.target), a, b,
      kind: l.kind || 'attack', defeated: !!l.defeated, weight: 0 });
  }
  const knownDomains = new Set();
  for (const n of rawNodes) {
    const d = normDomain(n && n.domain);
    if (d !== UNKNOWN_DOMAIN) knownDomains.add(d);
  }
  const nodes = rawNodes.map((n, i) => {
    const id = String(n.id);
    const domainRaw = n.domain == null ? '' : String(n.domain);
    let domain = normDomain(domainRaw);
    let domainSource = domain === UNKNOWN_DOMAIN ? 'none' : 'field';
    if (domain === UNKNOWN_DOMAIN) {
      const byId = domainFromId(id);
      if (byId !== UNKNOWN_DOMAIN && knownDomains.has(byId)) { domain = byId; domainSource = 'id'; }  // MIS-MEM-031 ⇒ mem
      else if (n.card != null) {
        const owner = at.get(String(n.card));
        if (owner != null) { domain = normDomain(rawNodes[owner].domain); domainSource = 'card'; }
      }
    }
    const ev = evidenceOf(n, cardsById);
    return { id, label: n.title || n.label || id, title: n.title || '', kind: n.kind || 'prop',
      state: n.state || 'unknown', credibility: num(n.credibility, 0), domain, domainRaw, domainSource,
      card: n.card == null ? null : String(n.card), props: n.props,
      evidence: ev.value, evidenceSource: ev.source, degree: degree[i] };
  });
  for (const e of edges) e.weight = edgeWeight(e, { degSource: degree[e.a], degTarget: degree[e.b] });
  const positions = Array.isArray(O.positions) ? O.positions
    : (O.seed === false ? null : seedPositions(nodes, {
      rngSeed: O.rngSeed, ringRadius: O.ringRadius, clusterRadius: O.clusterRadius }));
  const clusters = clusterByDomain(nodes, positions);
  const parsed = { nodes, edges, clusters, positions, meta: (json && json.meta) || {} };
  parsed.counts = summarize(parsed);
  return parsed;
}

/* ══════════════════════════════════════════════════════════════════════════
   二 · 浏览器引导（Node import 本文件时整段跳过）
   ══════════════════════════════════════════════════════════════════════════ */
const IS_BROWSER = typeof document !== 'undefined' && typeof window !== 'undefined';
const byId = (id) => document.getElementById(id);

if (IS_BROWSER) {
  boot().catch((e) => {
    const box = byId('stats');
    if (box) box.innerHTML = '<div class="muted">星图初始化失败：' + escapeHTML(e && e.message || e)
      + '（请用本地静态服务器打开：file:// 下 fetch 会被浏览器拦截）</div>';
  });
}

async function boot() {
  const canvas = byId('graph');
  const wrap = byId('stage');
  const tip = byId('tip');
  const detail = byId('detail');
  const labelsSvg = byId('cluster-labels');
  const ctx = canvas && canvas.getContext ? canvas.getContext('2d') : null;   // jsdom 下为 null/桩
  /* 671d：`raf` 与 `REDUCED_MOTION` 只服务于已删除的入场动画，一并移除
   *   （保留 `now`：力导向求解耗时统计仍在用）。 */
  const now = () => (window.performance && window.performance.now ? window.performance.now() : Date.now());
  const SVG_NS = 'http://www.w3.org/2000/svg';

  const cssVar = (name) => {
    try {
      const v = window.getComputedStyle(document.documentElement).getPropertyValue(name);
      return String(v == null ? '' : v).trim();
    } catch { return ''; }
  };
  const tok = (name) => { const v = cssVar(name); return hexToRgb(v) ? v : (TOKEN_FALLBACK[name] || '#8b9299'); };
  const PALETTE = clusterPalette(cssVar);
  // 画布上用到的少数 token 色（聚类标签走 SVG 覆盖层 ⇒ 字体/颜色由 .cluster-label 提供）
  const C = {
    text: tok('--color-text'), dim: tok('--color-text-dim'), accent: tok('--color-accent'),
  };
  // 边的四种描边（颜色取自 app.js 的 LINK_STYLE = design-tokens 的镜像）
  const EDGE_STROKE = [
    'rgba(' + LINK_STYLE.asserts.color + ',' + LINK_STYLE.asserts.alpha + ')',
    'rgba(' + LINK_STYLE.defend.color + ',' + LINK_STYLE.defend.alpha + ')',
    'rgba(' + LINK_STYLE.attack.color + ',' + LINK_STYLE.attack.alpha + ')',
    'rgba(' + LINK_STYLE.attack.color + ',0.82)',      // 被击败的攻击边：同色更亮更粗
  ];

  let G = null;                       // parseGraph 结果
  let state = null;                   // { positions, edges, cluster }
  let idxById = new Map();
  let view = { x: 0, y: 0, k: 1, rotX: 0, rotY: 0 };
  let viewInit = false;
  let hovered = -1, selected = -1, hoverEdge = -1, hoverCluster = -1;
  let SP = [];                 // 投影后的屏幕坐标缓存（每帧重算）
  let rafPending = false;      // scheduleDraw 的 rAF 去重
  let hits = [], hitAt = -1, searchHits = null;
  let layoutInfo = { iterations: 0, ms: 0, minDistance: 0, converged: false, separationIterations: 0 };
  const reveal = 1;   // 671d：固定 1（入场动画已删，节点首帧即最终尺寸）
  const filters = { states: new Set(['pass', 'pass_with_exception', 'fail', 'unknown']),
    domain: 'all', defeatedOnly: false, weight: true };
  const labelEls = new Map();        // domain → <text class="cluster-label">
  const labelBoxes = [];             // [{domain, x, y, w, h}] 供聚类 hover 命中
  let labelGroup = null;
  let weightMax = 1;

  // ── 视口 / 坐标 ──────────────────────────────────────────────────────────
  function viewport() {
    const w = (wrap && wrap.clientWidth) || (canvas && canvas.clientWidth) || 960;
    const h = (canvas && canvas.clientHeight) || (wrap && wrap.clientHeight) || 620;
    return { width: Math.max(1, Math.round(w)), height: Math.max(1, Math.round(h)) };
  }
  const toScreen = (p) => applyTransform(p, view, viewport());
  const toWorld = (sx, sy) => invertTransform({ x: sx, y: sy }, view, viewport());

  function resize() {
    if (!canvas) return;
    const vp = viewport();
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    canvas.width = Math.max(1, Math.round(vp.width * dpr));
    canvas.height = Math.max(1, Math.round(vp.height * dpr));
    if (ctx && typeof ctx.setTransform === 'function') ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (!viewInit) { fitView(false); viewInit = true; }
    draw();
  }

  // ── 可见性 ───────────────────────────────────────────────────────────────
  const passFilter = (n) => !!(n && filters.states.has(n.state));
  const inDomain = (n) => filters.domain === 'all' || (n && n.domain) === filters.domain;
  const nodeVisible = (i) => !!(G && passFilter(G.nodes[i]) && inDomain(G.nodes[i]));
  const edgeVisible = (i) => {
    const e = G.edges[i];
    if (filters.defeatedOnly && !(e.kind === 'attack' && e.defeated)) return false;
    return nodeVisible(e.a) && nodeVisible(e.b);
  };
  /** 可见节点下标：直接用纯函数 filterNodes（页面里不另写一套筛选逻辑）。 */
  const visibleIndices = () => filterNodes(G.nodes, { states: filters.states, domain: filters.domain });
  const dimBySearch = (i) => !!(searchHits && !searchHits.has(i));
  const isHit = (i) => hitAt >= 0 && hits[hitAt] != null && idxById.get(hits[hitAt]) === i;
  function neighborSet() {
    if (selected < 0) return null;
    return neighborsOf(G.edges, selected);
  }

  // ── 布局 / 视图 ──────────────────────────────────────────────────────────
  function fitView(redraw = true) {
    if (!state) return;
    const vp = viewport();
    view = fitTransform(boundsOf(state.positions), { width: vp.width, height: vp.height, padding: 48, maxK: 1.6, minK: 0.2 });
    if (redraw) draw();
  }
  /** 复位视图：清空选中/悬停 + 旋转归零 + 自适应。拖拽旋转后双击画布即回到正视角。 */
  function resetView() {
    selected = -1; hovered = -1; hoverEdge = -1; hoverCluster = -1;
    hitAt = hits.length ? 0 : -1;
    renderDetail(-1); view.rotX = 0; view.rotY = 0; fitView();
  }
  function zoomBy(f, around = null) {
    const vp = viewport();
    const before = around ? toWorld(around.x, around.y) : null;
    view.k = clamp(view.k * f, 0.25, 6);
    if (before) {
      const after = toWorld(around.x, around.y);
      view.x += after.x - before.x;
      view.y += after.y - before.y;
    }
    draw();
    return view.k;
  }
  function centerOnIndex(i, minK = 1.4) {
    if (!(i >= 0) || !state || !state.positions[i]) return null;
    const vp = viewport();
    view = screenTransform(state.positions[i], {
      width: vp.width, height: vp.height, k: Math.max(view.k, minK), minK: 0.25, maxK: 6,
    });
    draw();
    return { x: view.x, y: view.y, k: view.k };
  }

  // ── Canvas 绘制（2.5D 伪3D：透视投影 + 按需重绘；无每帧物理循环）─────────
  /** 投影一个世界点（带当前视口中心）。 */
  function proj(p, vp) { return projectPoint(p, Object.assign({}, view, { cx: vp.width / 2, cy: vp.height / 2 })); }
  /** 聚类成员的平均深度（光晕/标签跟着 2.5D 走）。 */
  function avgZ(members) {
    let s = 0, n = 0;
    const z = state && state.z;
    for (const i of (members || [])) { if (z && z[i] != null) { s += z[i]; n++; } }
    return n ? s / n : 0;
  }
  /** rAF 去重：连续交互只排一帧（≈60fps），避免 mousemove 风暴掉帧。 */
  function scheduleDraw() {
    if (rafPending) return;
    rafPending = true;
    const run = () => { rafPending = false; draw(); };
    if (typeof requestAnimationFrame === 'function') requestAnimationFrame(run);
    else setTimeout(run, 16);
  }

  function draw() {
    if (!ctx || !G || !state) return;
    const vp = viewport();
    SP = new Array(state.positions.length);
    for (let i = 0; i < state.positions.length; i++) {
      SP[i] = proj({ x: state.positions[i].x, y: state.positions[i].y, z: state.z[i] }, vp);
    }
    if (typeof ctx.clearRect === 'function') ctx.clearRect(0, 0, vp.width, vp.height);
    drawClusterHalo(SP, vp);
    drawEdges(SP, vp);
    drawNodes(SP, vp);
    drawFocus(SP, vp);
    drawLabels(SP, vp);
  }

  function cull(A, B, vp) {
    const m = 40;
    if (A.sx < -m && B.sx < -m) return true;
    if (A.sx > vp.width + m && B.sx > vp.width + m) return true;
    if (A.sy < -m && B.sy < -m) return true;
    if (A.sy > vp.height + m && B.sy > vp.height + m) return true;
    return false;
  }

  function drawEdges(SP, vp) {
    const buckets = new Map();
    const nc = 4;                                    // 权重档数（量化后分桶，减少状态切换）
    for (let i = 0; i < G.edges.length; i++) {
      if (!edgeVisible(i)) continue;
      const e = G.edges[i];
      const A = SP[e.a], B = SP[e.b];
      if (!A || !B || cull(A, B, vp)) continue;
      const cls = e.kind === 'attack' ? (e.defeated ? 3 : 2) : (e.kind === 'defend' ? 1 : 0);
      const t = filters.weight ? Math.min(1, e.weight / weightMax) : 0.5;
      const wc = Math.min(3, Math.floor(t * 4));
      const key = cls * nc + wc;
      let arr = buckets.get(key);
      if (!arr) { arr = []; buckets.set(key, arr); }
      arr.push(A.sx, A.sy, B.sx, B.sy);
    }
    for (const [key, pts] of buckets) {
      const cls = Math.floor(key / nc), wc = key % nc;
      const w = filters.weight
        ? strokeWidthFor((wc + 0.5) / 4 * weightMax, weightMax, { k: view.k, base: 1 })
        : 0.5 * view.k;
      if (typeof ctx.beginPath !== 'function') break;
      ctx.beginPath();
      for (let k = 0; k < pts.length; k += 4) { ctx.moveTo(pts[k], pts[k + 1]); ctx.lineTo(pts[k + 2], pts[k + 3]); }
      ctx.lineWidth = Math.max(0.2, w);
      ctx.strokeStyle = EDGE_STROKE[cls];
      ctx.stroke();
    }
    if (hoverEdge >= 0 && G.edges[hoverEdge]) {
      const e = G.edges[hoverEdge];
      const A = SP[e.a], B = SP[e.b];
      if (A && B) {
        ctx.beginPath(); ctx.moveTo(A.sx, A.sy); ctx.lineTo(B.sx, B.sy);
        ctx.lineWidth = Math.max(1.4, 2.2 * view.k);
        // 高亮色走 design-token（accent / text），不写死 red/green
        ctx.strokeStyle = (e.kind === 'attack' && e.defeated) ? C.accent : C.text;
        ctx.stroke();
      }
    }
  }

  function drawNodes(SP, vp) {
    const neigh = neighborSet();
    const search = searchHits;
    for (let i = 0; i < G.nodes.length; i++) {
      if (!nodeVisible(i)) continue;
      const n = G.nodes[i], p = SP[i];
      if (!p || p.sx < -80 || p.sy < -80 || p.sx > vp.width + 80 || p.sy > vp.height + 80) continue;
      const r = Math.max(1.2, nodeRadiusFor(n.degree) * p.scale);   // 大小按 degree；近大远小来自 p.scale
      const a = nodeAlpha(i, { hovered, selected, neighbors: neigh, searchHits: search,
        baseAlpha: num(CRED_ALPHA[n.credibility], 0.6) }) * num(p.alpha, 1);
      ctx.globalAlpha = clamp(a, 0, 1);
      ctx.beginPath();
      if (n.kind === 'misconception') ctx.rect(p.sx - r, p.sy - r, r * 2, r * 2);   // 形通道：误解=方
      else ctx.arc(p.sx, p.sy, r, 0, Math.PI * 2);
      ctx.fillStyle = STATE_COLORS[n.state] || STATE_COLORS.unknown;              // 色通道：四态（design-token 镜像）
      ctx.fill();
      if (n.kind === 'card' || i === hovered || i === selected || isHit(i)) {
        ctx.lineWidth = (i === hovered || isHit(i)) ? 1.6 : 1;
        ctx.strokeStyle = (i === hovered || isHit(i)) ? C.text : 'rgba(232,230,227,.55)';
        ctx.stroke();
      }
      ctx.globalAlpha = 1;
    }
  }

  function drawClusterHalo(SP, vp) {
    if (!G.clusters) return;
    G.clusters.forEach((c, ci) => {
      if (filters.domain !== 'all' && c.domain !== filters.domain) return;
      const sp = clusterSpread(c.members, state.positions, 0.9);
      const ctr = proj({ x: c.cx, y: c.cy, z: avgZ(c.members) }, vp);
      const r = Math.max(12, sp.r * ctr.scale);
      if (ctr.sx < -r || ctr.sy < -r || ctr.sx > vp.width + r || ctr.sy > vp.height + r) return;
      const col = hexToRgb(PALETTE[ci % PALETTE.length]) || [139, 146, 153];
      // 渐变光晕（替代实心大圆）：中心 token 色 0.20 → 边缘透明
      if (typeof ctx.createRadialGradient !== 'function') {
        ctx.globalAlpha = 0.06; ctx.beginPath(); ctx.arc(ctr.sx, ctr.sy, r, 0, Math.PI * 2);
        ctx.fillStyle = PALETTE[ci % PALETTE.length]; ctx.fill(); ctx.globalAlpha = 1; return;
      }
      const g = ctx.createRadialGradient(ctr.sx, ctr.sy, r * 0.1, ctr.sx, ctr.sy, r);
      g.addColorStop(0, 'rgba(' + col[0] + ',' + col[1] + ',' + col[2] + ',0.20)');
      g.addColorStop(1, 'rgba(' + col[0] + ',' + col[1] + ',' + col[2] + ',0)');
      ctx.globalAlpha = 1;
      ctx.beginPath(); ctx.arc(ctr.sx, ctr.sy, r, 0, Math.PI * 2);
      ctx.fillStyle = g; ctx.fill();
    });
  }

  function drawFocus(SP, vp) {
    const idx = [hovered, selected].filter((i) => i >= 0);
    if (hitAt >= 0 && hits[hitAt] != null) idx.push(idxById.get(hits[hitAt]));
    const shown = new Set();
    for (const i of idx) {
      if (i == null || shown.has(i) || !G.nodes[i] || !SP[i]) continue;
      shown.add(i);
      const p = SP[i], r = Math.max(4, nodeRadiusFor(G.nodes[i].degree) * p.scale);
      ctx.beginPath();
      ctx.arc(p.sx, p.sy, r + 5, 0, Math.PI * 2);
      ctx.lineWidth = isHit(i) ? 2 : 1.5;
      ctx.strokeStyle = isHit(i) ? C.accent : C.dim;
      ctx.stroke();
    }
  }

  function drawLabels(SP, vp) {
    if (!labelGroup) return;
    labelBoxes.length = 0;
    G.clusters.forEach((c, ci) => {
      const el = labelEls.get(c.domain);
      if (!el) return;
      const visible = c.members.some((i) => nodeVisible(i));
      const ctr = proj({ x: c.cx, y: c.cy, z: avgZ(c.members) }, vp);
      const onScreen = ctr.sx > 20 && ctr.sy > 20 && ctr.sx < vp.width - 20 && ctr.sy < vp.height - 20;
      if (!visible || !onScreen) { el.setAttribute('opacity', '0'); return; }
      const r = Math.max(10, clusterSpread(c.members, state.positions, 0.9).r * ctr.scale);
      const w = String(c.label || c.domain).length * 6.6 + 14;
      el.setAttribute('opacity', filters.domain === 'all' || filters.domain === c.domain ? '0.95' : '0.15');
      el.setAttribute('x', ctr.sx.toFixed(1));
      el.setAttribute('y', (ctr.sy - 6).toFixed(1));
      labelBoxes.push({ domain: c.domain, x: ctr.sx, y: ctr.sy - 6, w, h: 16, index: ci, r });
    });
  }

  // ── 拾取 ─────────────────────────────────────────────────────────────────
  function pickNode(sx, sy) {
    let best = -1, bd = Infinity;
    for (let i = 0; i < G.nodes.length; i++) {
      if (!nodeVisible(i)) continue;
      const p = SP[i]; if (!p) continue;
      const r = Math.max(6, nodeRadiusFor(G.nodes[i].degree) * p.scale) + 6 / view.k;
      const d = Math.hypot(p.sx - sx, p.sy - sy);
      if (d <= r && d < bd) { bd = d; best = i; }
    }
    return best;
  }
  function pickEdge(sx, sy) {
    let best = -1, bd = 7;
    for (let i = 0; i < G.edges.length; i++) {
      if (!edgeVisible(i)) continue;
      const e = G.edges[i];
      const A = SP[e.a], B = SP[e.b];
      if (!A || !B) continue;
      const d = distToSegment(sx, sy, A.sx, A.sy, B.sx, B.sy);
      if (d < bd) { bd = d; best = i; }
    }
    return best;
  }
  function pickCluster(sx, sy) {
    for (const b of labelBoxes) {
      if (Math.abs(sx - b.x) <= b.w / 2 + 6 && Math.abs(sy - b.y) <= b.h + 6) return b.index;
    }
    return -1;
  }

  // ── 提示气泡（.canvas-tip）───────────────────────────────────────────────
  function showTip(x, y, title, lines) {
    if (!tip) return;
    tip.innerHTML = '<div class="mono">' + escapeHTML(title) + '</div>'
      + (lines || []).map((l) => '<div class="muted">' + escapeHTML(l) + '</div>').join('');
    tip.hidden = false;
    const vp = viewport();
    const w = tip.offsetWidth || 240, h = tip.offsetHeight || 56;
    tip.style.left = Math.max(6, Math.min(vp.width - w - 6, x + 14)) + 'px';
    tip.style.top = Math.max(6, Math.min(vp.height - h - 6, y + 12)) + 'px';
  }
  function hideTip() { if (tip) tip.hidden = true; }

  // ── 搜索 ─────────────────────────────────────────────────────────────────
  function applySearch(text, opts = {}) {
    const q = String(text == null ? '' : text);
    hits = q.trim() ? locateNode(G.nodes, q) : [];
    searchHits = hits.length ? new Set(hits.map((id) => idxById.get(id))) : null;
    hitAt = hits.length ? 0 : -1;
    const cnt = byId('q-count');
    if (cnt) {
      cnt.textContent = !q.trim() ? ''
        : hits.length
          ? '匹配 ' + hits.length + ' 个节点（未命中的压暗，不隐藏）· 回车依次居中'
          : '没有节点匹配「' + q + '」—— 这不是加载失败，是数据集里没有这个词';
    }
    if (opts.center !== false && hits.length) centerOnIndex(idxById.get(hits[0]));
    else draw();
    return hits;
  }
  function cycleHit() {
    if (!hits.length) return null;
    hitAt = (hitAt + 1) % hits.length;
    const i = idxById.get(hits[hitAt]);
    centerOnIndex(i);
    const t = nodeTip(G.nodes[i]);
    const c = vpCenter();
    showTip(c.x, c.y, '命中 ' + (hitAt + 1) + '/' + hits.length + ' · ' + t.title, t.lines);
    draw();
    return hits[hitAt];
  }
  function vpCenter() { const vp = viewport(); return { x: vp.width / 2 - 60, y: vp.height / 2 }; }

  // ── 渲染 UI 文本 / 图例 / 详情 ───────────────────────────────────────────
  function renderLead() {
    const s = G.counts, m = G.meta || {}, w2 = m.w2_summary || {};
    const el = byId('lead-desc');
    if (!el) return;
    el.innerHTML = '真实台账渲染：<b>' + fmtInt(s.nodes) + '</b> 节点（' + fmtInt(s.cards) + ' 卡 + '
      + fmtInt(s.props) + ' 命题 + ' + fmtInt(s.misconceptions) + ' 误解）· <b>' + fmtInt(s.links)
      + '</b> 条边（攻击 ' + fmtInt(s.attack) + '／其中被击败 ' + fmtInt(s.defeated) + ' · 防御 '
      + fmtInt(s.defend) + ' · 卡→命题 ' + fmtInt(s.asserts) + '）· <b>' + fmtInt(s.clusters)
      + '</b> 个 domain 聚类（展示层小写归一；其中 ' + fmtInt(s.domainFromId)
      + ' 个误解节点的 domain 数据里是 "?"，按 id 前缀 MIS-<域>-NNN 归属）· W2 接地：IN ' + (w2.IN == null ? '—' : w2.IN)
      + ' / OUT ' + (w2.OUT == null ? '—' : w2.OUT) + '。渲染 = 自写力导向 + Canvas 2D，数字全部现算。';
  }

  function renderStats() {
    const s = G.counts;
    const box = byId('stats');
    if (!box) return;
    box.innerHTML = [
      [fmtInt(s.nodes), '节点'], [fmtInt(s.links), '边'],
      [fmtInt(s.attack), '攻击边（被击败 ' + fmtInt(s.defeated) + '）'],
      [fmtInt(s.cards), '卡'], [fmtInt(s.props), '命题'], [fmtInt(s.clusters), '聚类（domain）'],
    ].map(([v, l]) => '<div class="stat-tile"><div class="st-n">' + v + '</div><div class="st-l">'
      + escapeHTML(l) + '</div></div>').join('');
  }

  function renderDetail(i) {
    if (!detail) return;
    if (!G || !(i >= 0)) {
      detail.innerHTML = '<h3>详情</h3><p class="muted">点击节点固定详情 · <b>悬停</b>看摘要 · '
        + '<b>悬停边</b>看攻击/击败关系 · 搜索命中会自动居中。</p>';
      return;
    }
    const n = G.nodes[i];
    const st = statsOf(G.edges, n.id);
    const inA = [], outA = [], def = [];
    for (let k = 0; k < G.edges.length; k++) {
      const e = G.edges[k];
      if (e.source !== n.id && e.target !== n.id) continue;
      if (e.kind === 'defend') def.push(k);
      else if (e.kind === 'attack') { if (e.target === n.id) inA.push(k); else outA.push(k); }
    }
    const other = (e) => (e.source === n.id ? e.target : e.source);
    const row = (k) => {
      const e = G.edges[k];
      const o = G.nodes[idxById.get(other(e))];
      return '<li class="edge-row" data-edge="' + k + '"><span class="mono">'
        + escapeHTML(o ? o.id : other(e)) + '</span> <span class="muted">'
        + escapeHTML(o ? (KIND_LABELS[o.kind] || o.kind) + ' · ' + (STATE_LABELS[o.state] || o.state) : '')
        + (e.kind === 'attack' ? ' · ' + (e.defeated ? '被击败' : '未被击败') : '')
        + '</span></li>';
    };
    detail.innerHTML = '<h3>详情（已固定）</h3>'
      + '<div class="d-title mono">' + escapeHTML(n.id) + '</div>'
      + '<div class="d-grid">'
      + '<div><span class="stat-label">类型</span><div>' + escapeHTML(KIND_LABELS[n.kind] || n.kind) + '</div></div>'
      + '<div><span class="stat-label">四态</span><div><span class="dot st-' + escapeHTML(n.state) + '"></span>'
      + '<span class="mono">' + escapeHTML(STATE_LABELS[n.state] || n.state) + '</span></div></div>'
      + '<div><span class="stat-label">credibility</span><div class="mono">' + num(n.credibility, 0) + '</div></div>'
      + '<div><span class="stat-label">domain</span><div class="mono">' + escapeHTML(n.domain) + '</div></div>'
      + '<div><span class="stat-label">证据强度</span><div class="mono">' + num(n.evidence, 0)
      + '（' + escapeHTML(n.evidenceSource) + '）</div></div>'
      + '<div><span class="stat-label">度</span><div class="mono">' + num(n.degree, 0) + '</div></div>'
      + '<div><span class="stat-label">受攻击</span><div class="mono">' + inA.length + '</div></div>'
      + '<div><span class="stat-label">发出攻击</span><div class="mono">' + outA.length + '</div></div>'
      + '<div><span class="stat-label">攻击边合计</span><div class="mono">' + st.attacks
      + '（被击败 ' + st.defeated + '）</div></div>'
      + '<div><span class="stat-label">防御边</span><div class="mono">' + st.defends + '</div></div>'
      + '</div>'
      + (n.label && n.label !== n.id ? '<p class="d-note">' + escapeHTML(n.label) + '</p>' : '')
      + (inA.length ? '<h3 style="margin-top:var(--space-2)">受攻击（' + inA.length + '）</h3><ul class="edge-list">'
        + inA.slice(0, 12).map(row).join('') + '</ul>' : '')
      + (outA.length ? '<h3 style="margin-top:var(--space-2)">发出攻击（' + outA.length + '）</h3><ul class="edge-list">'
        + outA.slice(0, 12).map(row).join('') + '</ul>' : '')
      + (def.length ? '<h3 style="margin-top:var(--space-2)">防御（' + def.length + '）</h3><ul class="edge-list">'
        + def.slice(0, 12).map(row).join('') + '</ul>' : '')
      + '<p class="muted" style="margin-top:var(--space-2)">再次点击空白处取消固定。</p>';
  }

  function renderClusters() {
    const box = byId('clusters');
    if (box) {
      box.innerHTML = '<div class="chan"><b>聚类（domain · 展示层小写归一）</b></div>'
        + G.clusters.map((c, ci) => '<button class="chip" type="button" data-cluster="' + escapeHTML(c.domain)
          + '" title="展开 ' + escapeHTML(c.domain) + '（' + c.count + ' 节点 · 平均证据 '
          + c.avgEvidence.toFixed(2) + '）"><span class="sq" style="background:'
          + PALETTE[ci % PALETTE.length] + '"></span>' + escapeHTML(c.label) + ' · ' + c.count + '</button>').join('')
        + '<span class="chan muted">' + (G.counts.domainFromId
          ? G.counts.domainFromId + ' 个误解节点的 domain 在数据里是 "?"，展示层按 id 前缀 MIS-&lt;域&gt;-NNN 归属（与攻击目标多数域一致 40/42）· '
          : '')
        + '点聚类 ⇒ 展开成员与平均证据强度；下拉框 ⇒ 只显示该聚类</span>';
      box.querySelectorAll('button[data-cluster]').forEach((b) => {
        b.addEventListener('click', () => expandCluster(b.dataset.cluster));
      });
    }
    const sel = byId('f-cluster');
    if (sel) {
      sel.innerHTML = '<option value="all">全部</option>'
        + G.clusters.map((c) => '<option value="' + escapeHTML(c.domain) + '">' + escapeHTML(c.label)
          + '（' + c.count + '）</option>').join('');
    }
  }

  function expandCluster(key) {
    const c = G.clusters.find((x) => x.domain === key);
    const box = byId('cluster-panel');
    if (!c || !box) return 0;
    const tipInfo = clusterTip(c);
    box.innerHTML = '<div class="card glass glass-tint" style="padding:var(--space-2)">'
      + '<div class="row-between"><h3 class="section-title">聚类 ' + escapeHTML(c.label) + '</h3>'
      + '<span class="muted">' + tipInfo.lines[0] + ' · ' + tipInfo.lines[1] + '</span>'
      + '<span class="spacer"></span>'
      + '<button type="button" id="cluster-filter">只看这个聚类</button>'
      + '<button type="button" id="cluster-close">收起</button></div>'
      + '<ul class="cluster-list">' + c.members.slice(0, 60).map((i) => {
        const n = G.nodes[i];
        return '<li><span class="mono">' + escapeHTML(n.id) + '</span>'
          + '<span class="note-faint">' + escapeHTML(KIND_LABELS[n.kind] || n.kind) + ' · '
          + escapeHTML(STATE_LABELS[n.state] || n.state) + ' · 证据 ' + num(n.evidence, 0) + '</span>'
          + '<span class="grow"></span><button class="chip" type="button" data-focus="' + i + '">定位</button></li>';
      }).join('') + '</ul>'
      + (c.count > 60 ? '<p class="note-faint">（只列前 60 个，共 ' + c.count + ' 个）</p>' : '')
      + '</div>';
    const close = box.querySelector('#cluster-close');
    if (close) close.addEventListener('click', () => { box.innerHTML = ''; });
    const only = box.querySelector('#cluster-filter');
    if (only) only.addEventListener('click', () => {
      filters.domain = c.domain;
      const sel = byId('f-cluster');
      if (sel) sel.value = c.domain;
      selected = -1; renderDetail(-1); draw();
    });
    box.querySelectorAll('button[data-focus]').forEach((b) => {
      b.addEventListener('click', () => {
        const i = Number(b.dataset.focus);
        selected = i; hovered = i; centerOnIndex(i, 1.6); renderDetail(i);
      });
    });
    return c.members.length;
  }

  function setModeText() {
    const el = byId('mode');
    if (!el) return;
    el.textContent = 'Canvas 2D（自写力导向）· ' + G.counts.nodes + ' 节点 / ' + G.counts.links
      + ' 边 / ' + G.counts.clusters + ' 聚类 · 布局 ' + layoutInfo.iterations + ' 迭代 ' + layoutInfo.ms + 'ms · 防重叠 '
      + layoutInfo.separationIterations + ' 迭代（最近点对 ' + layoutInfo.minDistance.toFixed(1) + 'px）'
      + ' · 无每帧物理 · 无入场动画 · 收敛 ' + (layoutInfo.converged ? '是' : 'maxMove ' + layoutInfo.maxMove.toFixed(2) + 'px（视觉已稳定）');
  }

  // ── 交互 ─────────────────────────────────────────────────────────────────
  function wire() {
    let dragging = false, moved = false, last = { x: 0, y: 0 };
    const localPos = (e) => {
      const r = canvas && canvas.getBoundingClientRect ? canvas.getBoundingClientRect() : { left: 0, top: 0 };
      return { x: (e.clientX || 0) - r.left, y: (e.clientY || 0) - r.top };
    };
    if (canvas) {
      canvas.addEventListener('mousedown', (e) => { dragging = true; moved = false; last = { x: e.clientX, y: e.clientY }; });
      window.addEventListener('mouseup', () => { dragging = false; });
      canvas.addEventListener('mousemove', (e) => {
        if (!G || !state) return;
        if (dragging) {
          // 2.5D：拖拽旋转模型（水平→绕 Y，垂直→绕 X 俯仰），不再平移
          view.rotY += (e.clientX - last.x) * 0.006;
          view.rotX = clamp(view.rotX + (e.clientY - last.y) * 0.006, -1.3, 1.3);
          last = { x: e.clientX, y: e.clientY };
          moved = true; hideTip(); scheduleDraw(); return;
        }
        const s = localPos(e);
        hovered = pickNode(s.x, s.y);
        hoverEdge = hovered >= 0 ? -1 : pickEdge(s.x, s.y);
        hoverCluster = (hovered >= 0 || hoverEdge >= 0) ? -1 : pickCluster(s.x, s.y);
        if (hovered >= 0) {
          const t = nodeTip(G.nodes[hovered]);
          showTip(s.x, s.y, t.title, t.lines);
          canvas.style.cursor = 'pointer';
        } else if (hoverEdge >= 0) {
          const e2 = G.edges[hoverEdge];
          showTip(s.x, s.y, e2.source + ' → ' + e2.target, [
            e2.kind === 'attack' ? (e2.defeated ? '攻击边 · 被击败' : '攻击边 · 未被击败')
              : e2.kind === 'defend' ? '防御边' : '断言边（卡 → 命题）',
            '关系强度（派生）' + e2.weight.toFixed(2) + ' · 端度数 ' + G.nodes[e2.a].degree + '/' + G.nodes[e2.b].degree,
          ]);
          canvas.style.cursor = 'crosshair';
        } else if (hoverCluster >= 0) {
          const c = G.clusters[hoverCluster];
          const t = clusterTip(c);
          showTip(s.x, s.y, t.title, t.lines);
          canvas.style.cursor = 'help';
        } else {
          hideTip(); canvas.style.cursor = 'grab';
        }
        scheduleDraw();
      });
      canvas.addEventListener('mouseleave', () => {
        hovered = -1; hoverEdge = -1; hoverCluster = -1; hideTip(); draw();
      });
      canvas.addEventListener('click', () => {
        if (moved) return;
        selected = hovered;
        renderDetail(selected);
        scheduleDraw();
      });
      canvas.addEventListener('wheel', (e) => {
        e.preventDefault();
        zoomBy(e.deltaY < 0 ? 1.12 : 1 / 1.12, localPos(e));
      }, { passive: false });
      canvas.addEventListener('keydown', (e) => {
        const step = 60 / view.k;
        if (e.key === 'ArrowLeft') view.x += step;
        else if (e.key === 'ArrowRight') view.x -= step;
        else if (e.key === 'ArrowUp') view.y += step;
        else if (e.key === 'ArrowDown') view.y -= step;
        else if (e.key === '+' || e.key === '=') { zoomBy(1.25); return; }
        else if (e.key === '-' || e.key === '_') { zoomBy(1 / 1.25); return; }
        else if (e.key === '0') { fitView(); return; }
        else if (e.key === 'Escape') { selected = -1; renderDetail(-1); draw(); return; }
        else return;
        e.preventDefault(); draw();
      });
      if (typeof ResizeObserver === 'function' && wrap) {
        try { new ResizeObserver(() => resize()).observe(wrap); } catch { /* 忽略 */ }
      }
    }
    window.addEventListener('resize', resize);

    for (const k of ['pass', 'pass_with_exception', 'fail', 'unknown']) {
      const cb = byId('f-' + k);
      if (cb) cb.addEventListener('change', () => {
        if (cb.checked) filters.states.add(k); else filters.states.delete(k);
        draw();
      });
    }
    const dd = byId('f-defeated');
    if (dd) dd.addEventListener('change', () => { filters.defeatedOnly = dd.checked; draw(); });
    const w = byId('f-weight');
    if (w) w.addEventListener('change', () => { filters.weight = w.checked; draw(); });
    const sel = byId('f-cluster');
    if (sel) sel.addEventListener('change', () => {
      filters.domain = sel.value; selected = -1; renderDetail(-1); draw();
    });
    const q = byId('q');
    if (q) {
      q.addEventListener('input', () => applySearch(q.value, { center: false }));
      q.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); cycleHit(); } });
    }
    const qn = byId('q-next');
    if (qn) qn.addEventListener('click', () => cycleHit());
    const zin = byId('zin');
    if (zin) zin.addEventListener('click', () => zoomBy(1.25));
    const zout = byId('zout');
    if (zout) zout.addEventListener('click', () => zoomBy(1 / 1.25));
    const reset = byId('reset');
    if (reset) reset.addEventListener('click', resetView);
    // 2.5D：双击画布复位（旋转归零 + 自适应），与右上角"复位视图"按钮同效
    canvas.addEventListener('dblclick', resetView);
  }

  // ── 启动 ─────────────────────────────────────────────────────────────────
  /* 671d：删掉 420ms 的"节点尺寸入场动画"（easeOutCubic）。
   *   理由：① 420ms > 本批次规定的 200ms 上限；② 首次渲染时节点从小变大，
   *   在数据图上属于装饰而非信息；③ 力导向图本身已经是"一次性求解后按需重绘"，
   *   多这一层动画只会让首屏看起来更"模板"。改为直接绘制最终尺寸。 */
  function startReveal() {
    reveal = 1;
    draw();
  }

  const raw = await fetchJSON('data/graph.json');
  let cardsIndex = null;
  try { cardsIndex = await fetchJSON('data/cards_index.json'); } catch { cardsIndex = null; }
  G = parseGraph(raw, { cardsIndex });
  idxById = new Map(G.nodes.map((n, i) => [n.id, i]));
  weightMax = G.edges.reduce((m, e) => Math.max(m, e.weight), 1);

  // —— 自动化验证钩子（tools/web_smoke_655.mjs 等按 id 探测；语义只读）——
  window.__starmap_hooks = {
    select(i) { selected = i; renderDetail(i); scheduleDraw(); return i >= 0 && G.nodes[i] ? G.nodes[i].id : null; },
    detailText() { return detail ? detail.textContent : ''; },
    nodeCount() { return G ? G.nodes.length : 0; },
    linkCount() { return G ? G.edges.length : 0; },
    info(i) {
      const n = G.nodes[i];
      if (!n) return null;
      return { id: n.id, state: n.state, credibility: n.credibility, ...statsOf(G.edges, n.id) };
    },
    clusters: () => G.clusters.map((c) => c.domain + ':' + c.count),
    visibleCount() { return G ? visibleIndices().length : 0; },
    search(text) { applySearch(text); return hits.length ? hits.length : -1; },
    zoom(f) { return zoomBy(f); },
    setWeight(on) { filters.weight = !!on; draw(); return filters.weight; },
    expand(key) { return expandCluster(key); },
    layout() { return { ...layoutInfo }; },
    transform() { return { ...view }; },
    locate(query) { return locateNode(G.nodes, query); },
    centerOn(i) { return centerOnIndex(i); },
    counts() { return { ...G.counts }; },
  };

  // 布局：**只在加载时算一次**（实测毫秒数写进 #mode，不假装很快）
  const t0 = now();
  // 迭代预算：实测 160 步后布局指标就饱和了（纵横比 1.50 / 簇间隔 ≥1.2 / 最近点对 16px），
  // 240 步没有可见收益 ⇒ 取 200 步 + 40 步防重叠；只在加载时跑一次，之后按需重绘。
  const solved = runLayout(G.nodes, G.edges, { iterations: 200, tolerance: 0.12, minDist: 16, separationIterations: 40 });
  layoutInfo = { iterations: solved.iterations, ms: Math.round(now() - t0),
    minDistance: solved.minDistance, converged: solved.converged, maxMove: solved.maxMove,
    separationIterations: solved.separationIterations };
  state = { positions: solved.positions, z: depthFor(G.nodes, solved.positions, {}),
    edges: G.edges.map((e) => ({ a: e.a, b: e.b, weight: e.weight })),
    cluster: clusterIndexOf(G.nodes) };
  G.clusters = clusterByDomain(G.nodes, state.positions);

  if (labelsSvg) {
    labelGroup = document.createElementNS(SVG_NS, 'g');
    labelsSvg.appendChild(labelGroup);
    G.clusters.forEach((c, ci) => {
      const t = document.createElementNS(SVG_NS, 'text');
      t.setAttribute('class', 'cluster-label');
      t.setAttribute('text-anchor', 'middle');
      // 注意：SVG 的 **表现属性** fill 会被 .cluster-label 的 CSS fill 压过 ⇒ 用内联 style
      t.style.fill = PALETTE[ci % PALETTE.length];
      t.setAttribute('opacity', '0.95');
      t.textContent = c.label + ' · ' + c.count;
      labelGroup.appendChild(t);
      labelEls.set(c.domain, t);
    });
  }

  renderLead(); renderStats(); renderDetail(-1); renderClusters(); setModeText();
  wire();
  resize();
  startReveal();
  window.__starmap_ready = true;
}
