// 670c A5 · 星图纯逻辑测试（无 DOM / 无 canvas / 无依赖 ⇒ 直接 node 跑）
//
// 运行（在 web/ 下）：
//   node tests/starmap.test.mjs
//
// 测什么：只测 web/starmap.js **导出的纯函数**（数据解析 / 聚类统计 / 关系强度 /
//   力导向迭代 / 防重叠 / 搜索 / 屏幕变换 / 拾取 / 文案），并对 web/data/graph.json
//   的真实数据做**独立复算**（测试里自己再数一遍，不用被测代码的结论）。
// 不测什么：canvas 绘制与 DOM 渲染 —— jsdom 没有 2D context，测了也是假绿；
//   这部分由 tools/web_smoke_655.mjs（jsdom 真跑页面 + __starmap_hooks）覆盖。
import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as SM from '../starmap.js';

let passed = 0;
const ok = (name, cond) => { assert.ok(cond, 'FAIL: ' + name); passed++; };

// ── 真实台账（只读；测试自己解析，避免用被测函数的结论当真值）──────────────
const readJSON = (rel) => JSON.parse(fs.readFileSync(new URL(rel, import.meta.url), 'utf-8'));
const rawGraph = readJSON('../data/graph.json');
const cardsIndex = readJSON('../data/cards_index.json');
const G = SM.parseGraph(rawGraph, { cardsIndex });
const SRC = fs.readFileSync(new URL('../starmap.js', import.meta.url), 'utf-8');
const HTML = fs.readFileSync(new URL('../starmap.html', import.meta.url), 'utf-8');

// 独立统计（不调用被测函数）
const deg = new Map();
for (const l of rawGraph.links) {
  deg.set(l.source, (deg.get(l.source) || 0) + 1);
  deg.set(l.target, (deg.get(l.target) || 0) + 1);
}
const cardEv = new Map(cardsIndex.cards.map((c) => [c.id, c.evidence.length]));
// 独立实现一遍 domain 归属（测试自己的代码，不用被测函数）：
//   数据字段 → （无域时）id 前缀 MIS-<DOMAIN>-NNN（前缀必须是真实 domain）→ 否则 "?"
const realDomains = new Set(rawGraph.nodes
  .map((n) => String(n.domain == null ? '' : n.domain).trim().toLowerCase())
  .filter((d) => d && d !== '?'));
const domKey = (n) => {
  const own = String(n.domain == null ? '' : n.domain).trim().toLowerCase();
  if (own && own !== '?') return own;
  const parts = String(n.id).split('-');
  const pre = parts.length > 1 ? parts[1].toLowerCase() : '';
  return realDomains.has(pre) ? pre : '?';
};
const byDomain = new Map();
for (const n of rawGraph.nodes) {
  const k = domKey(n);
  if (!byDomain.has(k)) byDomain.set(k, []);
  byDomain.get(k).push(n);
}
// 独立实现一遍证据强度：卡 = cards_index 证据条数；命题 = 所属卡的条数；其余回退 credibility
const evOf = (n) => (n.kind === 'card' ? cardEv.get(n.id)
  : (n.kind === 'prop' && n.card ? cardEv.get(n.card) : n.credibility));

/* ══ ① 真实数据解析 ══════════════════════════════════════════════════════ */
ok('graph.json 节点数 = 178，与 meta.counts 一致',
  rawGraph.nodes.length === 178 && rawGraph.meta.counts.nodes === 178);
ok('graph.json 边数 = 1093，与 meta.counts 一致',
  rawGraph.links.length === 1093 && rawGraph.meta.counts.links === 1093);
ok('parseGraph 不丢节点/边', G.nodes.length === 178 && G.edges.length === 1093);
ok('每条边的下标可回指原 id（a/b 索引正确）',
  G.edges.every((e) => G.nodes[e.a].id === e.source && G.nodes[e.b].id === e.target));
ok('度数总和 = 2 × 边数（无悬空边）', G.counts.degreeSum === 2 * 1093);
ok('每个节点度数 = 独立统计', G.nodes.every((n) => n.degree === (deg.get(n.id) || 0)));
ok('最大度 = 51（hub 命题），0 度节点 10 个',
  G.counts.maxDegree === 51
  && G.nodes.reduce((a, n) => (n.degree > a.degree ? n : a)).id === 'ATOM-MEM-SHARED-001::prop-1'
  && G.nodes.filter((n) => n.degree === 0).length === 10);
ok('summarize 现算聚类数 = 7', G.counts.clusters === 7);
ok('summarize 与 meta.counts 交叉一致（不读 meta 现算）',
  G.counts.attack === rawGraph.meta.counts.by_kind.attack
  && G.counts.defend === rawGraph.meta.counts.by_kind.defend
  && G.counts.asserts === rawGraph.meta.counts.by_kind.asserts
  && G.counts.defeated === rawGraph.meta.counts.defeated_links
  && G.counts.cards === rawGraph.meta.counts.cards
  && G.counts.props === rawGraph.meta.counts.props);
ok('三类节点：卡 47 / 命题 89 / 误解 42',
  G.counts.cards === 47 && G.counts.props === 89 && G.counts.misconceptions === 42);
ok('domain 只在展示层小写归一（MEM/mem、LANG/lang 合成一簇；原数据不动）',
  rawGraph.nodes.some((n) => n.domain === 'MEM') && rawGraph.nodes.some((n) => n.domain === 'mem')
  && rawGraph.nodes.some((n) => n.domain === 'LANG')
  && G.nodes.every((n) => n.domain === n.domain.toLowerCase())
  && G.clusters.every((c) => c.domain === c.domain.toLowerCase())
  && G.clusters.find((c) => c.domain === 'mem').count
     === rawGraph.nodes.filter((n) => String(n.domain).toLowerCase() === 'mem').length
        + rawGraph.nodes.filter((n) => n.kind === 'misconception' && String(n.id).startsWith('MIS-MEM-')).length);

/* ══ ② 聚类统计 clusterByDomain ═════════════════════════════════════════ */
ok('聚类数 = 7、成员总数 = 178、不再有 "?" 簇（误解的域由 id 前缀推出）',
  G.clusters.length === 7 && G.clusters.every((c) => c.domain !== '?')
  && G.clusters.reduce((s, c) => s + c.count, 0) === 178);
ok('每个聚类的 count/卡/命题/误解 = 独立统计',
  G.clusters.every((c) => {
    const arr = byDomain.get(c.domain) || [];
    return arr.length === c.count
      && arr.filter((n) => n.kind === 'card').length === c.cards
      && arr.filter((n) => n.kind === 'prop').length === c.props
      && arr.filter((n) => n.kind === 'misconception').length === c.misconceptions;
  }));
ok('mem 聚类 = 115 节点（23 卡 · 65 命题 · 27 误解）', (() => {
  const c = G.clusters.find((x) => x.domain === 'mem');
  return c && c.count === 115 && c.cards === 23 && c.props === 65 && c.misconceptions === 27;
})());
ok('误解的域全部推得出来：42/42 的 id 前缀都指向真实 domain', (() => {
  const misc = rawGraph.nodes.filter((n) => n.kind === 'misconception');
  return misc.length === 42 && misc.every((n) => realDomains.has(String(n.id).split('-')[1].toLowerCase()));
})());
ok('id 前缀与"攻击目标所在域"的多数票一致 40/42（另 2 个是跨域攻击）', (() => {
  const at = new Map(rawGraph.nodes.map((n) => [n.id, n]));
  let agree = 0;
  for (const m of rawGraph.nodes.filter((n) => n.kind === 'misconception')) {
    const tally = {};
    for (const l of rawGraph.links) {
      if (l.source !== m.id && l.target !== m.id) continue;
      const other = at.get(l.source === m.id ? l.target : l.source);
      const d = String((other && other.domain) || '').trim().toLowerCase();
      if (d && d !== '?') tally[d] = (tally[d] || 0) + 1;
    }
    const best = Object.entries(tally).sort((a, b) => b[1] - a[1])[0];
    if (best && best[0] === String(m.id).split('-')[1].toLowerCase()) agree++;
  }
  return agree === 40;
})());
ok('avgEvidence = 成员证据强度的独立均值（7 簇全部）',
  G.clusters.every((c) => {
    const arr = byDomain.get(c.domain) || [];
    const avg = arr.reduce((s, n) => s + evOf(n), 0) / arr.length;
    return arr.length === c.count && Math.abs(avg - c.avgEvidence) < 5e-4;
  }));
ok('clusterSpread：大簇铺得更开（mem > cpp）',
  SM.clusterSpread(G.clusters.find((c) => c.domain === 'mem').members, G.positions).r
  > SM.clusterSpread(G.clusters.find((c) => c.domain === 'cpp').members, G.positions).r);

/* ══ ③ 证据强度 evidenceOf ══════════════════════════════════════════════ */
const srcCount = G.nodes.reduce((a, n) => { a[n.evidenceSource] = (a[n.evidenceSource] || 0) + 1; return a; }, {});
ok('证据来源分布：47 卡走 cards_index / 89 命题继承所属卡 / 42 误解回退 credibility',
  srcCount.cards_index === 47 && srcCount.owner_card === 89 && srcCount.credibility === 42);
ok('命题的证据条数 = 其所属卡的 evidence 条数（真值对照）', (() => {
  const p = G.nodes.find((n) => n.kind === 'prop');
  return p.evidence === cardEv.get(p.card) && p.evidenceSource === 'owner_card';
})());
ok('domain 来源：136 个来自数据字段 / 42 个来自误解 id 前缀 / 0 个推不出',
  G.counts.domainFromId === 42 && G.counts.domainFromCard === 0 && G.counts.domainMissing === 0
  && G.nodes.filter((n) => n.domainSource === 'field').length === 136);
ok('domainFromId：MIS-MEM-031→mem、MIS-UB-002→ub、其余一律 "?"',
  SM.domainFromId('MIS-MEM-031') === 'mem' && SM.domainFromId('MIS-UB-002') === 'ub'
  && SM.domainFromId('ATOM-MEM-001') === '?' && SM.domainFromId('') === '?' && SM.domainFromId(null) === '?');
ok('卡的证据条数 = cards_index 里的数组长度（抽样 5 张）',
  G.nodes.filter((n) => n.kind === 'card').slice(0, 5)
    .every((n) => n.evidence === cardEv.get(n.id) && n.evidenceSource === 'cards_index'));
ok('node.evidence 数字/数组优先于 cards_index',
  SM.evidenceStrength({ id: 'X', evidence: 7, credibility: 1 }) === 7
  && SM.evidenceStrength({ id: 'X', evidence: ['a', 'b'], credibility: 1 }) === 2
  && SM.evidenceOf({ id: 'X', credibility: 2 }).source === 'credibility');

/* ══ ④ 关系强度 edgeWeight / strokeWidthFor ════════════════════════════ */
const eBase = { kind: 'attack', defeated: false };
ok('edgeWeight 确定性 + 不修改入参', (() => {
  const inp = Object.assign({}, eBase);
  const a = SM.edgeWeight(inp, { degSource: 3, degTarget: 4 });
  const b = SM.edgeWeight(inp, { degSource: 3, degTarget: 4 });
  return a === b && Object.keys(inp).length === 2 && a > 0;
})());
ok('edgeWeight 随端度数单调递增（hub 项）',
  SM.edgeWeight(eBase, { degSource: 1, degTarget: 1 })
  < SM.edgeWeight(eBase, { degSource: 10, degTarget: 10 })
  && SM.edgeWeight(eBase, { degSource: 10, degTarget: 10 })
  < SM.edgeWeight(eBase, { degSource: 25, degTarget: 26 }));
ok('被击败的攻击边 = 未击败 × 1.3（权重保留 4 位小数 ⇒ 容差 1e-3）', (() => {
  const off = SM.edgeWeight(eBase, { degSource: 1, degTarget: 1 });
  const on = SM.edgeWeight({ kind: 'attack', defeated: true }, { degSource: 1, degTarget: 1 });
  // 权重保留 4 位小数 ⇒ 比值有 1e-4 量级的取整误差
  return Math.abs(on / off - 1.3) < 1e-3 && Math.abs(on - off * 1.3) < 1e-4;
})());
ok('未知 kind 回退基线 1，缺参不抛',
  SM.edgeWeight({ kind: 'zzz' }) === 0.55 && SM.edgeWeight() === 0.55 && SM.edgeWeight(null, null) === 0.55);
ok('真实 1093 条边的 weight ∈ [0.69, 1.88]',
  Math.abs(Math.min.apply(null, G.edges.map((e) => e.weight)) - 0.6927) < 1e-3
  && Math.abs(Math.max.apply(null, G.edges.map((e) => e.weight)) - 1.8731) < 1e-3);
ok('strokeWidthFor：权重越大越粗、随缩放 k 线性',
  SM.strokeWidthFor(1.87, 1.87, { k: 1 }) > SM.strokeWidthFor(0.69, 1.87, { k: 1 })
  && Math.abs(SM.strokeWidthFor(1.87, 1.87, { k: 2 }) - 2 * SM.strokeWidthFor(1.87, 1.87, { k: 1 })) < 1e-9);

/* ══ ⑤ 力导向 stepForces / runLayout / 防重叠 ═════════════════════════ */
const st0 = { positions: [{ x: -100, y: 0 }, { x: 100, y: 0 }, { x: 0, y: 60 }],
  edges: [{ a: 0, b: 1, weight: 1 }, { a: 1, b: 2, weight: 1 }], cluster: ['a', 'a', 'a'], alpha: 1 };
const snapBefore = JSON.stringify(st0.positions);
const r1 = SM.stepForces(st0, {});
ok('stepForces 纯函数：入参位置不被修改，返回新数组',
  JSON.stringify(st0.positions) === snapBefore && r1.positions !== st0.positions
  && r1.positions.length === 3 && r1.positions.every((p) => Number.isFinite(p.x) && Number.isFinite(p.y)));
ok('温度冷却：返回的 alpha < 入参 alpha', r1.alpha < 1 && r1.maxMove >= 0 && r1.energy >= r1.maxMove);
ok('完全重合的节点不产生 NaN/Infinity', (() => {
  const s = SM.stepForces({ positions: [{ x: 0, y: 0 }, { x: 0, y: 0 }, { x: 0, y: 0 }],
    edges: [{ a: 0, b: 1 }], cluster: ['z', 'z', 'z'], alpha: 1 }, {});
  return s.positions.every((p) => Number.isFinite(p.x) && Number.isFinite(p.y));
})());
ok('两节点一弹簧：200 步后边长收敛到 springLength 附近（±20%）', (() => {
  const L = SM.runLayout([{ id: 'a', kind: 'prop', domain: 'x' }, { id: 'b', kind: 'prop', domain: 'x' }],
    [{ a: 0, b: 1, weight: 1 }],
    { iterations: 200, springLength: 60, separationIterations: 0, positions: [{ x: -300, y: 0 }, { x: 300, y: 0 }] });
  const d = Math.hypot(L.positions[0].x - L.positions[1].x, L.positions[0].y - L.positions[1].y);
  return d > 48 && d < 72;
})());

const solved = SM.runLayout(G.nodes, G.edges, { iterations: 240, tolerance: 0.12, minDist: 16, separationIterations: 40 });
ok('runLayout：178 个有限坐标，迭代不超上限，给出收敛指标',
  solved.positions.length === 178
  && solved.positions.every((p) => Number.isFinite(p.x) && Number.isFinite(p.y))
  && solved.iterations > 0 && solved.iterations <= 240 && typeof solved.converged === 'boolean');
ok('布局形状与画布同向：纵横比 ∈ [1.2, 2.0]', (() => {
  const bb = SM.boundsOf(solved.positions);
  const asp = bb.width / bb.height;
  return asp >= 1.2 && asp <= 2.0;
})());
ok('7 个域互不糊在一起：簇间最小间隔 / 半径和 ≥ 1.0', (() => {
  const cl = SM.clusterByDomain(G.nodes, solved.positions);
  const sp = new Map(cl.map((c) => [c.domain, SM.clusterSpread(c.members, solved.positions, 0.9)]));
  let worst = Infinity;
  for (let i = 0; i < cl.length; i++) {
    for (let j = i + 1; j < cl.length; j++) {
      const a = sp.get(cl[i].domain), b = sp.get(cl[j].domain);
      const r = Math.hypot(a.cx - b.cx, a.cy - b.cy) / (a.r + b.r + 1e-9);
      if (r < worst) worst = r;
    }
  }
  return worst >= 1.0;
})());
ok('runLayout 确定性：同参数两次结果逐位一致（种子固定）',
  JSON.stringify(solved.positions) === JSON.stringify(
    SM.runLayout(G.nodes, G.edges, { iterations: 240, tolerance: 0.12, minDist: 16, separationIterations: 40 }).positions));
const noSep = SM.runLayout(G.nodes, G.edges, { iterations: 240, tolerance: 0.12, separationIterations: 0 });
ok('防重叠真起作用：最近点对 16.0（不防重叠时 3.3）',
  solved.minDistance >= 16 * 0.99 && noSep.minDistance < 5 && solved.minDistance > noSep.minDistance * 3);
ok('relaxOverlaps：3 个重合点被推开到 ≥ 0.98 × minDist', (() => {
  const r = SM.relaxOverlaps([{ x: 5, y: 5 }, { x: 5, y: 5 }, { x: 5, y: 5 }], [4, 4, 4], { minDist: 16, iterations: 40 });
  return r.minDistance >= 16 * 0.98 && r.iterations > 0 && r.positions.length === 3;
})());
ok('minPairDistance 已知值', SM.minPairDistance([{ x: 0, y: 0 }, { x: 3, y: 4 }]) === 5
  && SM.minPairDistance([{ x: 0, y: 0 }]) === 0);

/* ══ ⑥ 搜索 locateNode ═════════════════════════════════════════════════ */
ok('空查询 / 空白查询 / null → []（不是"匹配全部"）',
  SM.locateNode(G.nodes, '').length === 0 && SM.locateNode(G.nodes, '   ').length === 0
  && SM.locateNode(G.nodes, null).length === 0);
ok('大小写不敏感：小写查询仍命中大写 id 且排第一',
  SM.locateNode(G.nodes, 'atom-conc-fence-001')[0] === 'ATOM-CONC-FENCE-001');
ok('部分匹配：FENCE → 3 个，race → 4 个且全部含 race',
  SM.locateNode(G.nodes, 'FENCE').length === 3
  && SM.locateNode(G.nodes, 'race').length === 4
  && SM.locateNode(G.nodes, 'race').every((id) => id.toLowerCase().includes('race')));
ok('排序：id 全等优先于前缀/子串', (() => {
  const hits = SM.locateNode(G.nodes, 'ATOM-CONC-RACE-001');
  return hits[0] === 'ATOM-CONC-RACE-001' && hits[1] === 'ATOM-CONC-RACE-001::prop-1';
})());
ok('数据集里没有的词 → []（页面据此显示"真的没有"，不是加载失败）',
  SM.locateNode(G.nodes, 'memory').length === 0 && SM.locateNode(G.nodes, 'zzzz-不存在').length === 0);

/* ══ ⑦ 屏幕变换 screenTransform / fitTransform ═════════════════════════ */
const vp = { width: 800, height: 600, k: 2 };
ok('screenTransform 把节点放到视口正中（用 applyTransform 反算）', (() => {
  const tr = SM.screenTransform({ x: 5, y: -7 }, vp);
  const s = SM.applyTransform({ x: 5, y: -7 }, tr, vp);
  return tr.x === -5 && tr.y === 7 && tr.k === 2 && s.x === 400 && s.y === 300;
})());
ok('screenTransform 夹取缩放（k=99 → maxK，k=0.01 → minK）',
  SM.screenTransform({ x: 0, y: 0 }, { width: 800, height: 600, k: 99 }).k === 6
  && SM.screenTransform({ x: 0, y: 0 }, { width: 800, height: 600, k: 0.01 }).k === 0.25);
ok('screenTransform 支持屏幕偏移（标签避让用）', (() => {
  const tr = SM.screenTransform({ x: 0, y: 0 }, { width: 800, height: 600, k: 2, offsetX: 40 });
  return SM.applyTransform({ x: 0, y: 0 }, tr, { width: 800, height: 600 }).x === 400 + 40;
})());
ok('invertTransform ∘ applyTransform = 恒等', (() => {
  const tr = { x: -12, y: 30, k: 1.7 };
  const back = SM.invertTransform(SM.applyTransform({ x: 33, y: -44 }, tr, vp), tr, vp);
  return Math.abs(back.x - 33) < 1e-9 && Math.abs(back.y + 44) < 1e-9;
})());
ok('boundsOf 已知值（宽高/中心）', (() => {
  const b = SM.boundsOf([{ x: -10, y: -20 }, { x: 30, y: 40 }]);
  return b.width === 40 && b.height === 60 && b.cx === 10 && b.cy === 10;
})());
ok('fitTransform：包围盒中心映到视口中心，且缩放被 maxK 夹住', (() => {
  const b = SM.boundsOf([{ x: -10, y: -20 }, { x: 30, y: 40 }]);
  const tr = SM.fitTransform(b, { width: 800, height: 600, padding: 20, maxK: 6, minK: 0.25 });
  const s = SM.applyTransform({ x: b.cx, y: b.cy }, tr, { width: 800, height: 600 });
  return tr.k === 6 && s.x === 400 && s.y === 300;
})());
ok('真实布局自适应缩放 k ∈ (0.2, 1.6]（178 节点不会缩成一点）', (() => {
  const tr = SM.fitTransform(SM.boundsOf(solved.positions), { width: 960, height: 620, padding: 48, maxK: 1.6, minK: 0.2 });
  return tr.k > 0.2 && tr.k <= 1.6;
})());

/* ══ ⑧ 拾取 / 文案 / 颜色 / 其它工具 ═══════════════════════════════════ */
ok('distToSegment：垂足 / 端点外 / 退化线段', (() => {
  return SM.distToSegment(0, 5, 0, 0, 10, 0) === 5
    && SM.distToSegment(20, 0, 0, 0, 10, 0) === 10
    && Math.abs(SM.distToSegment(3, 3, 5, 5, 5, 5) - Math.SQRT2 * 2) < 1e-9;
})());
ok('pickNodeAt：最近优先 + 半径外 -1 + isVisible 过滤', (() => {
  const pos = [{ x: 0, y: 0 }, { x: 100, y: 0 }, { x: 10, y: 0 }];
  const nodes = [{ id: 'a' }, { id: 'b' }, { id: 'c' }];
  return SM.pickNodeAt(pos, nodes, { x: 9, y: 2 }, 15) === 2
    && SM.pickNodeAt(pos, nodes, { x: 500, y: 500 }, 15) === -1
    && SM.pickNodeAt(pos, nodes, { x: 9, y: 2 }, 15, (i) => i !== 2) === 0;
})());
ok('pickEdgeAt：命中最近边，超出阈值 -1', (() => {
  const scr = [{ x: 0, y: 0 }, { x: 100, y: 0 }];
  const edges = [{ a: 0, b: 1 }];
  return SM.pickEdgeAt(scr, edges, { x: 50, y: 5 }, 7) === 0
    && SM.pickEdgeAt(scr, edges, { x: 50, y: 50 }, 7) === -1;
})());
ok('clusterTip 写明节点数/卡数/命题数与平均证据强度（两位小数）', (() => {
  const mem = G.clusters.find((c) => c.domain === 'mem');
  const t = SM.clusterTip(mem);
  return t.title === 'mem' && t.lines[0] === '115 节点（23 卡 · 65 命题 · 27 误解）'
    && t.lines[1].indexOf('平均证据强度 ' + mem.avgEvidence.toFixed(2)) === 0;
})());
ok('nodeTip 写明四态 / domain / credibility / 度 / 证据强度', (() => {
  const t = SM.nodeTip(G.nodes[0]);
  return t.title === 'ATOM-CONC-FENCE-001' && t.lines[0].indexOf('pass') >= 0
    && t.lines[1].indexOf('度 2') > 0 && t.lines[1].indexOf('证据强度 2') > 0;
})());
ok('escapeHTML 转义 & < > " \'', SM.escapeHTML('<b>"x"&\'y\'') === '&lt;b&gt;&quot;x&quot;&amp;&#39;y&#39;');
ok('mixHex / hexToRgb / rgbToHex 已知值',
  SM.mixHex('#000000', '#ffffff', 0.5) === '#808080'
  && SM.mixHex('#5fc3ae', '#d97757', 0.5) === '#9c9d83'
  && SM.mixHex('#000000', '#ffffff', 0) === '#000000'
  && SM.rgbToHex([255, 128, 0]) === '#ff8000'
  && JSON.stringify(SM.hexToRgb('#5FC3AE')) === '[95,195,174]'
  && SM.hexToRgb('zzz') === null);
ok('clusterPalette：8 档、全部合法 hex、CSS 变量覆盖生效、读不到时回退 token 值', (() => {
  const fallback = SM.clusterPalette(() => '');
  const overridden = SM.clusterPalette((k) => (k === '--color-pass' ? '#00ff00' : ''));
  return fallback.length === 8 && fallback.every((c) => SM.hexToRgb(c))
    && fallback[0] === '#5fc3ae' && fallback[1] === '#d97757'
    && overridden[0] === '#00ff00' && overridden[6] !== fallback[6];
})());
ok('normDomain：MEM→mem、"?/空/null"→?（展示层归一，不改数据）',
  SM.normDomain('MEM') === 'mem' && SM.normDomain(' ? ') === '?'
  && SM.normDomain('') === '?' && SM.normDomain(null) === '?' && SM.normDomain('Lang') === 'lang');
ok('mulberry32 同种子同序列（布局可复现）',
  SM.mulberry32(42)() === SM.mulberry32(42)() && SM.mulberry32(42)() !== SM.mulberry32(43)());
ok('filterNodes：四态 + 聚类筛选（全部 178 / pass 116 / mem 115 / mem+pass 86）',
  SM.filterNodes(G.nodes, {}).length === 178
  && SM.filterNodes(G.nodes, { states: ['pass'] }).length === 116
  && SM.filterNodes(G.nodes, { domain: 'mem' }).length === 115
  && SM.filterNodes(G.nodes, { domain: 'mem', states: ['pass'] }).length === 86);
ok('neighborsOf 含自身（MIS-MEM-031 有 12 个邻居）', (() => {
  const i = G.nodes.findIndex((n) => n.id === 'MIS-MEM-031');
  return SM.neighborsOf(G.edges, i).size === 13 && SM.neighborsOf(G.edges, i).has(i);
})());
ok('statsOf 与独立统计一致（MIS-MEM-031：24 攻 / 12 被击败 / 0 防）', (() => {
  const st = SM.statsOf(G.edges, 'MIS-MEM-031');
  let attacks = 0, defeated = 0, defends = 0;
  for (const l of rawGraph.links) {
    if (l.source !== 'MIS-MEM-031' && l.target !== 'MIS-MEM-031') continue;
    if (l.kind === 'attack') { attacks++; if (l.defeated) defeated++; } else if (l.kind === 'defend') defends++;
  }
  return st.attacks === 24 && st.defeated === 12 && st.defends === 0
    && st.attacks === attacks && st.defeated === defeated && st.defends === defends;
})());

/* ══ ⑨ 静态接线：纯逻辑 / 页面的分工没有漂移 ═══════════════════════════ */
ok('六个必需纯函数 + 依赖它们的工具函数都已导出',
  ['parseGraph', 'clusterByDomain', 'edgeWeight', 'stepForces', 'locateNode', 'screenTransform',
    'domainFromId', 'evidenceOf', 'runLayout', 'relaxOverlaps', 'fitTransform', 'clusterTip', 'nodeTip']
    .every((k) => typeof SM[k] === 'function'));
ok('本文件在无 DOM 的 Node 里 import 成功（纯逻辑区不碰 document）',
  typeof document === 'undefined' && typeof SM.parseGraph === 'function');
ok('starmap.js 的浏览器引导有 document/window 守卫',
  SRC.indexOf("typeof document !== 'undefined' && typeof window !== 'undefined'") > 0);
ok('starmap.html 复用 669c 共享类（canvas-wrap / canvas-tip / cluster-label / stat-grid / search-input）',
  ['canvas-wrap', 'canvas-tip', 'cluster-label', 'stat-grid', 'search-input', 'kbd-hints']
    .every((c) => HTML.indexOf(c) > 0) && SRC.indexOf("'cluster-label'") > 0);
ok('starmap.html 仍接设计令牌 + 组件出口 + <qy-nav>（656 接线门禁）',
  HTML.indexOf('css/design-tokens.css') > 0 && HTML.indexOf('css/669c.css') > 0
  && HTML.indexOf('components/index.js') > 0 && HTML.indexOf('<qy-nav') > 0);
ok('starmap.html 无重复 id（旧版有两个 id="reset"）', (() => {
  const ids = (HTML.match(/id="[^"]+"/g) || []).map((s) => s.slice(4, -1));
  return ids.length > 0 && new Set(ids).size === ids.length;
})());
ok('starmap.js 里 byId(...) 用到的静态 id 全部存在于 HTML', (() => {
  const used = Array.from(new Set((SRC.match(/byId\('([^']+)'\)/g) || []).map((s) => s.slice(6, -2))));
  const have = new Set((HTML.match(/id="[^"]+"/g) || []).map((s) => s.slice(4, -1)));
  return used.length >= 15 && used.every((id) => have.has(id));
})());
ok('数字不写死：逻辑代码区（已去注释）不出现 178 / 1093', (() => {
  const CODE = SRC.replace(/\/\*[\s\S]*?\*\//g, '')
    .split('\n').map((l) => l.replace(/\/\/.*$/, '')).join('\n');
  return CODE.indexOf('178') < 0 && CODE.indexOf('1093') < 0;
})());

console.log('starmap.test: ' + passed + ' assertions passed');
