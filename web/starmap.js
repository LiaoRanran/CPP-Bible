// 653 B · 星图 hero：W2 接地图（178 节点 / 388 攻击边 / 194 击败边）三维编码
//   色 = 四态 · 大小 = 节点类型（卡 > 命题 > 误解）· 光（透明度）= credibility
// 655 D 深化：① 节点 hover 卡片化（标题 + 四态 + credibility + 攻防计数）
//            ② 点击 → 右侧**固定详情面板**（含攻击者/辩护者清单）
//            ③ **边 hover**（拾取最近边）显示攻击/击败关系并高亮该边
// 渲染：优先 cosmos.gl v3（本地 vendor）；不可达时**诚实降级**为 2D canvas（同编码，可交互）。
import { STATE_COLORS, STATE_LABELS, KIND_LABELS, LINK_STYLE, fetchJSON, fmtInt } from './app.js';
// 655 D：统计与几何（攻防计数 / 最近边）抽到 graph_core.js ⇒ 可被 Node 真跑验证
import { statsOf as coreStatsOf, pickEdgeIndex } from './graph_core.js';
// 656 C2：导航改为 `<qy-nav>` 组件（见 components/qy-nav.js），三个页面同一份实现

const canvas = document.getElementById('graph');
const stage = document.getElementById('stage');
const tip = document.getElementById('tip');
const detail = document.getElementById('detail');

let G = null;          // graph.json
let attackedSet = new Set();  // 受攻击节点 id（attack 边 target），B4-2 视觉标记用
let view = { x: 0, y: 0, k: 1 };
let pos = [];          // [{x,y}]
let idxById = new Map();
const filters = { pass: true, pass_with_exception: true, fail: true, unknown: true, defeatedOnly: false };

const RADIUS = { card: 7.5, prop: 4.2, misconception: 3.2 };
const alphaOf = (c) => (c >= 3 ? 1.0 : c === 2 ? 0.72 : 0.5);
const EDGE_PICK_PX = 7;      // 边拾取半径（屏幕像素）

// ── 布局：一次性力导向（O(n²) 可行，n=178）────────────────────────────────
function layout(nodes, links, iters = 320) {
  const n = nodes.length;
  const idx = new Map(nodes.map((d, i) => [d.id, i]));
  // 初始：以卡/命题的 domain 分簇，避免糊成一团
  const byDomain = new Map();
  nodes.forEach((d, i) => {
    const arr = byDomain.get(d.domain) || [];
    arr.push(i); byDomain.set(d.domain, arr);
  });
  let ring = 0;
  const R = 260;
  for (const [, arr] of byDomain) {
    const ang0 = (ring / byDomain.size) * Math.PI * 2;
    arr.forEach((i, j) => {
      const a = ang0 + (j / Math.max(1, arr.length)) * 0.9;
      pos[i] = { x: Math.cos(a) * R + (Math.random() - 0.5) * 40, y: Math.sin(a) * R + (Math.random() - 0.5) * 40 };
    });
    ring++;
  }
  const E = links.map((l) => [idx.get(l.source), idx.get(l.target)]).filter(([a, b]) => a != null && b != null);
  for (let it = 0; it < iters; it++) {
    const k = 3.2, rep = 5200, damp = 0.86;
    const fx = new Float64Array(n), fy = new Float64Array(n);
    for (const [a, b] of E) {
      const dx = pos[b].x - pos[a].x, dy = pos[b].y - pos[a].y;
      const d = Math.max(1e-3, Math.hypot(dx, dy));
      const f = (d - k * 26) * 0.0016;
      const ux = dx / d, uy = dy / d;
      fx[a] += ux * f; fy[a] += uy * f; fx[b] -= ux * f; fy[b] -= uy * f;
    }
    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        const dx = pos[j].x - pos[i].x, dy = pos[j].y - pos[i].y;
        const d2 = dx * dx + dy * dy + 25;
        const f = rep / (d2 * Math.sqrt(d2));
        fx[i] -= dx * f; fy[i] -= dy * f; fx[j] += dx * f; fy[j] += dy * f;
      }
    }
    for (let i = 0; i < n; i++) {
      pos[i].x += fx[i] * damp; pos[i].y += fy[i] * damp;
      pos[i].x = Math.max(-1200, Math.min(1200, pos[i].x));
      pos[i].y = Math.max(-900, Math.min(900, pos[i].y));
    }
  }
}

function passFilter(d) { return filters[d.state] !== false; }
function passLink(l) { return !filters.defeatedOnly || l.defeated; }
function nodeVisible(d) { return !!d && passFilter(d); }

// ── 2D 渲染 ──────────────────────────────────────────────────────────────
const ctx = canvas.getContext('2d');
let hovered = -1, selected = -1, hoverEdge = -1;

function resize() {
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  const r = canvas.getBoundingClientRect();
  canvas.width = Math.max(1, Math.floor(r.width * dpr));
  canvas.height = Math.max(1, Math.floor(r.height * dpr));
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  draw();
}

function toScreen(p) {
  const r = canvas.getBoundingClientRect();
  return { x: (p.x + view.x) * view.k + r.width / 2, y: (p.y + view.y) * view.k + r.height / 2 };
}
function toWorld(sx, sy) {
  const r = canvas.getBoundingClientRect();
  return { x: (sx - r.width / 2) / view.k - view.x, y: (sy - r.height / 2) / view.k - view.y };
}

function draw() {
  const r = canvas.getBoundingClientRect();
  ctx.clearRect(0, 0, r.width, r.height);
  if (!G) return;
  // 边（击败边加亮；攻击边按击败与否区分）
  for (let i = 0; i < G.links.length; i++) {
    const l = G.links[i];
    if (!passLink(l)) continue;
    const a = idxById.get(l.source), b = idxById.get(l.target);
    if (a == null || b == null || !nodeVisible(G.nodes[a]) || !nodeVisible(G.nodes[b])) continue;
    const st = LINK_STYLE[l.kind] || LINK_STYLE.attack;
    const defeated = l.defeated && l.kind === 'attack';
    const A = toScreen(pos[a]), B = toScreen(pos[b]);
    ctx.beginPath();
    ctx.moveTo(A.x, A.y); ctx.lineTo(B.x, B.y);
    const isHot = i === hoverEdge;
    ctx.strokeStyle = isHot
      ? (defeated ? 'rgba(217,107,107,.95)' : 'rgba(230,232,234,.85)')
      : `rgba(${defeated ? '217,107,107' : st.color},${defeated ? 0.42 : st.alpha})`;
    ctx.lineWidth = (isHot ? 2.2 : (defeated ? 1.15 : st.width)) * view.k;
    ctx.stroke();
  }
  // 节点
  const sel = selected >= 0 ? G.nodes[selected] : null;
  const neigh = sel ? neighbors(sel.id) : null;
  for (let i = 0; i < G.nodes.length; i++) {
    const d = G.nodes[i];
    if (!passFilter(d)) continue;
    const p = toScreen(pos[i]);
    const rad = (RADIUS[d.kind] || 4) * view.k;
    const dim = sel && !(neigh.has(d.id) || d.id === sel.id);
    ctx.globalAlpha = dim ? 0.18 : alphaOf(d.credibility);
    ctx.beginPath();
    // 形通道：卡=圆、命题=圆（小）、误解=方（一眼可分）
    if (d.kind === 'misconception') ctx.rect(p.x - rad, p.y - rad, rad * 2, rad * 2);
    else ctx.arc(p.x, p.y, rad, 0, Math.PI * 2);
    ctx.fillStyle = STATE_COLORS[d.state] || STATE_COLORS.unknown;
    ctx.fill();
    if (d.kind === 'card' || i === hovered) {
      ctx.lineWidth = i === hovered ? 1.6 : 1;
      ctx.strokeStyle = i === hovered ? '#e6e8ea' : 'rgba(230,232,234,.55)';
      ctx.stroke();
    }
    // B4-2：受攻击节点红色边框 + 光晕（不改位置/大小，仅加视觉标记）
    if (attackedSet.has(d.id)) {
      ctx.save();
      ctx.shadowColor = 'rgba(255,72,72,.9)';
      ctx.shadowBlur = 9 * view.k;
      ctx.lineWidth = 1.8 * view.k;
      ctx.strokeStyle = 'rgba(255,96,96,.95)';
      ctx.stroke();
      ctx.restore();
    }
    ctx.globalAlpha = 1;
  }
}

function neighbors(id) {
  const s = new Set([id]);
  for (const l of G.links) {
    if (l.source === id) s.add(l.target);
    if (l.target === id) s.add(l.source);
  }
  return s;
}

// ── 拾取：节点优先，其次**最近边**（点到线段距离）─────────────────────────
function pickNode(wx, wy) {
  let best = -1, bd = 18 / view.k;
  for (let i = 0; i < G.nodes.length; i++) {
    if (!passFilter(G.nodes[i])) continue;
    const d = Math.hypot(pos[i].x - wx, pos[i].y - wy);
    if (d < bd) { bd = d; best = i; }
  }
  return best;
}

function pickEdge(sx, sy) {
  return pickEdgeIndex({
    links: G.links, nodes: G.nodes, pos, toScreen,
    visible: nodeVisible, passLink, sx, sy, maxPx: EDGE_PICK_PX,
  });
}

// ── 交互 ─────────────────────────────────────────────────────────────────
let dragging = false, last = { x: 0, y: 0 }, moved = false;
canvas.addEventListener('mousedown', (e) => { dragging = true; moved = false; last = { x: e.clientX, y: e.clientY }; });
window.addEventListener('mouseup', () => { dragging = false; });
canvas.addEventListener('mousemove', (e) => {
  const r = canvas.getBoundingClientRect();
  if (dragging) {
    view.x += (e.clientX - last.x) / view.k;
    view.y += (e.clientY - last.y) / view.k;
    last = { x: e.clientX, y: e.clientY }; moved = true; draw(); return;
  }
  const sx = e.clientX - r.left, sy = e.clientY - r.top;
  const w = toWorld(sx, sy);
  hovered = pickNode(w.x, w.y);
  hoverEdge = hovered >= 0 ? -1 : pickEdge(sx, sy);
  if (hovered >= 0) {
    showTip(sx, sy, nodeTip(G.nodes[hovered]));
    canvas.style.cursor = 'pointer';
  } else if (hoverEdge >= 0) {
    showTip(sx, sy, edgeTip(G.links[hoverEdge]));
    canvas.style.cursor = 'crosshair';
  } else {
    tip.style.display = 'none'; canvas.style.cursor = 'grab';
  }
  if (hoverEdge >= 0 || hovered >= 0) draw();
});
canvas.addEventListener('mouseleave', () => {
  hovered = -1; hoverEdge = -1; tip.style.display = 'none'; draw();
});
canvas.addEventListener('click', () => {
  if (moved) return;
  selected = hovered;                 // -1 ⇒ 清空选中
  renderDetail(selected);
  draw();
});
canvas.addEventListener('wheel', (e) => {
  e.preventDefault();
  view.k = Math.max(0.25, Math.min(4, view.k * (e.deltaY < 0 ? 1.12 : 1 / 1.12)));
  draw();
}, { passive: false });

function showTip(x, y, html) {
  tip.style.display = 'block';
  tip.style.left = `${x + 14}px`;
  tip.style.top = `${y + 12}px`;
  tip.innerHTML = html;
}

function nodeTip(d) {
  const st = statsOf(d.id);
  return `<div class="t">${d.id}</div>
    <div class="m">${KIND_LABELS[d.kind] || d.kind} · <b>${STATE_LABELS[d.state] || d.state}</b></div>
    <div class="m">credibility=${d.credibility}${d.domain ? ` · domain=${d.domain}` : ''}${d.label ? ` · label=${d.label}` : ''}</div>
    ${d.title ? `<div class="m">${d.title}</div>` : ''}
    <div class="m">攻 ${st.attacks} · 被击败 ${st.defeated} · 防 ${st.defends}</div>
    <div class="m">点击固定详情</div>`;
}

function edgeTip(l) {
  const src = G.nodes[idxById.get(l.source)], dst = G.nodes[idxById.get(l.target)];
  const kind = l.kind === 'attack' ? (l.defeated ? '攻击边 · **被击败**' : '攻击边 · 未被击败')
    : l.kind === 'defend' ? '防御边' : '断言边（卡 → 命题）';
  return `<div class="t">${l.source} → ${l.target}</div>
    <div class="m">${kind}</div>
    <div class="m">${KIND_LABELS[src.kind] || src.kind} → ${KIND_LABELS[dst.kind] || dst.kind}</div>
    <div class="m">${STATE_LABELS[src.state] || src.state} → ${STATE_LABELS[dst.state] || dst.state}</div>`;
}

function statsOf(id) {
  return coreStatsOf(G.links, id);       // 实现在 graph_core.js（Node 可测）
}

// ── 详情面板（655 D：点击固定）────────────────────────────────────────────
function renderDetail(i) {
  if (!detail) return;
  if (i < 0 || !G) {
    detail.innerHTML = `<h3>详情</h3><p class="muted">点击节点固定详情 · 悬停边看攻击/击败关系</p>`;
    return;
  }
  const d = G.nodes[i];
  const st = statsOf(d.id);
  const inAttack = [], outAttack = [], defs = [];
  for (let k = 0; k < G.links.length; k++) {
    const l = G.links[k];
    if (l.kind === 'defend' && (l.source === d.id || l.target === d.id)) defs.push([l, k]);
    else if (l.kind === 'attack') {
      if (l.target === d.id) inAttack.push([l, k]);
      else if (l.source === d.id) outAttack.push([l, k]);
    }
  }
  const other = (l) => (l.source === d.id ? l.target : l.source);
  const row = ([l, k]) => {
    const o = G.nodes[idxById.get(other(l))];
    return `<li class="edge-row" data-edge="${k}">
      <span class="mono">${o ? o.id : other(l)}</span>
      <span class="muted">${o ? (KIND_LABELS[o.kind] || o.kind) : ''} · ${o ? (STATE_LABELS[o.state] || o.state) : ''}</span>
      ${l.kind === 'attack' ? `<qy-tag kind="${l.defeated ? 'bad' : 'warn'}">${l.defeated ? '被击败' : '未被击败'}</qy-tag>` : ''}
    </li>`;
  };
  detail.innerHTML = `<h3>详情（已固定）</h3>
    <div class="d-title mono">${d.id}</div>
    <div class="d-grid">
      <div><span class="stat-label">类型</span><div>${KIND_LABELS[d.kind] || d.kind}</div></div>
      <div><span class="stat-label">四态</span><div><qy-status state="${d.state}"></qy-status></div></div>
      <div><span class="stat-label">credibility</span><div class="mono">${d.credibility}</div></div>
      <div><span class="stat-label">domain</span><div class="mono">${d.domain || '—'}</div></div>
      ${d.status ? `<div><span class="stat-label">卡状态</span><div class="mono">${d.status}</div></div>` : ''}
      ${d.props != null ? `<div><span class="stat-label">命题数</span><div class="mono">${d.props}</div></div>` : ''}
      <div><span class="stat-label">攻击边</span><div class="mono">${st.attacks}（被击败 ${st.defeated}）</div></div>
      <div><span class="stat-label">防御边</span><div class="mono">${st.defends}</div></div>
    </div>
    ${d.title ? `<p class="d-note">${d.title}</p>` : ''}
    ${inAttack.length ? `<h3 style="margin-top:14px">受攻击（${inAttack.length}）</h3><ul class="edge-list">${inAttack.slice(0, 12).map(row).join('')}</ul>` : ''}
    ${outAttack.length ? `<h3 style="margin-top:14px">发出攻击（${outAttack.length}）</h3><ul class="edge-list">${outAttack.slice(0, 12).map(row).join('')}</ul>` : ''}
    ${defs.length ? `<h3 style="margin-top:14px">防御（${defs.length}）</h3><ul class="edge-list">${defs.slice(0, 12).map(row).join('')}</ul>` : ''}
    <p class="muted" style="margin-top:12px">再次点击空白处取消固定。</p>`;
}

// ── 统计/图例/筛选 ───────────────────────────────────────────────────────
function renderStats() {
  const m = G.meta, c = m.counts;
  const w2 = m.w2_summary || {};
  document.getElementById('stats').innerHTML = [
    [fmtInt(c.nodes), '节点'],
    [fmtInt(c.by_kind?.attack), '攻击边'],
    [fmtInt(c.defeated_links), '击败边'],
    [fmtInt(c.cards), '卡'],
    [fmtInt(c.props), '命题'],
    [`${w2.IN ?? '—'}/${w2.OUT ?? '—'}`, 'IN/OUT'],
  ].map(([v, l]) => `<div><div class="stat">${v}</div><div class="stat-label">${l}</div></div>`).join('');
}

/** 655 D：首屏描述文字也**现算**（不再写死 178/388/194，避免文档与数据漂移）。 */
function renderLead() {
  const c = G.meta.counts;
  const el = document.getElementById('lead-desc');
  if (!el) return;
  const w2 = G.meta.w2_summary || {};
  el.innerHTML = `真实台账渲染：<b>${fmtInt(c.nodes)}</b> 节点（${fmtInt(c.cards)} 卡 +
    ${fmtInt(c.props)} 命题 + ${fmtInt(c.nodes - c.cards - c.props)} 误解）·
    <b>${fmtInt(c.by_kind?.attack)}</b> 条攻击边（其中 <b>${fmtInt(c.defeated_links)}</b> 条被击败）·
    ${fmtInt(c.by_kind?.defend)} 条防御边 · W2 接地：IN ${w2.IN ?? '—'} / OUT ${w2.OUT ?? '—'}。
    数据由 <span class="kbd">tools/web_data_653.py</span> 从
    <span class="kbd">data/grounded_labels_w2.json</span> 与 <span class="kbd">atoms/**</span> 生成，<b>不造数据</b>。`;
}

function wireFilters() {
  for (const k of ['pass', 'pass_with_exception', 'fail', 'unknown']) {
    const cb = document.getElementById('f-' + k);
    cb.addEventListener('change', () => { filters[k] = cb.checked; draw(); });
  }
  const dd = document.getElementById('f-defeated');
  dd.addEventListener('change', () => { filters.defeatedOnly = dd.checked; draw(); });
  document.getElementById('reset').addEventListener('click', () => {
    view = { x: 0, y: 0, k: 1 }; selected = -1; renderDetail(-1); draw();
  });
}

// ── cosmos.gl v3（本地 vendor，654 修复）────────────────────────────────
// 653 用 CDN `+esm` 时，jsDelivr 把依赖写死为绝对 URL，且同时拉入
// `@luma.gl/core@9.3.5`（经 shadertools@9.3.5）与 `@9.3.6` ⇒ **luma.gl 双份**
// ⇒ 运行时报错、自动降级 2D。654 改为**本地 vendor**（web/vendor/，版本已统一 9.3.6、
// 导入已重写为相对路径，可离线）。CDN 不再使用；失败时仍降级 2D（要求 5）。
async function tryCosmos() {
  try {
    const mod = await import('./vendor/cosmos.js');
    const Graph = mod.Graph || mod.default?.Graph;
    if (!Graph) throw new Error('no Graph export');
    const cfg = {
      backgroundColor: '#090b0e',
      spaceSize: 4096,
      pointDefaultSize: 6,
      linkDefaultWidth: 0.6,
      linkDefaultColor: 'rgba(120,130,140,0.25)',
      enableDrag: true, enableZoom: true,
    };
    const graph = new Graph(canvas, cfg);
    const n = G.nodes;
    const P = new Float32Array(n.length * 2);
    pos.forEach((p, i) => { P[i * 2] = p.x * 3; P[i * 2 + 1] = p.y * 3; });
    const S = new Float32Array(n.length); const C = new Float32Array(n.length * 4);
    const rad = { card: 12, prop: 7, misconception: 5 };
    n.forEach((d, i) => {
      S[i] = rad[d.kind] || 6;
      const hex = (STATE_COLORS[d.state] || STATE_COLORS.unknown).replace('#', '');
      C[i * 4] = parseInt(hex.slice(0, 2), 16) / 255;
      C[i * 4 + 1] = parseInt(hex.slice(2, 4), 16) / 255;
      C[i * 4 + 2] = parseInt(hex.slice(4, 6), 16) / 255;
      C[i * 4 + 3] = alphaOf(d.credibility);
    });
    const L = new Float32Array(G.links.length * 2);
    G.links.forEach((l, i) => { L[i * 2] = idxById.get(l.source) ?? 0; L[i * 2 + 1] = idxById.get(l.target) ?? 0; });
    graph.setPointPositions(P); graph.setPointSizes(S); graph.setPointColors(C); graph.setLinks(L);
    graph.render();
    stage.classList.remove('fallback-note');
    document.getElementById('mode').textContent = 'GPU · cosmos.gl v3（本地 vendor 3.4.1 / luma.gl 9.3.6）';
    window.__cosmos_ok = true;   // 供自动化验证探测
    return true;
  } catch (e) {
    stage.classList.add('fallback-note');
    document.getElementById('mode').textContent = '2D canvas（降级）';
    window.__cosmos_err = String(e && e.message || e);
    return false;
  }
}

// ── 自动化验证钩子（655 D：给 tools/web_smoke_655.mjs 用；只读语义，不改渲染路径）──
window.__starmap_hooks = {
  /** 选中第 i 个节点并渲染详情面板（等价于"悬停后点击"）。 */
  select(i) { selected = i; renderDetail(i); draw(); return i >= 0 ? G.nodes[i].id : null; },
  /** 返回当前详情面板文本（供断言）。 */
  detailText() { return detail ? detail.textContent : ''; },
  /** 节点数（供断言）。 */
  nodeCount() { return G ? G.nodes.length : 0; },
  /** 边数（供断言）。 */
  linkCount() { return G ? G.links.length : 0; },
  /** 详细信息：`{id, state, credibility, attacks, defeated, defends}`。 */
  info(i) {
    const d = G.nodes[i];
    return { id: d.id, state: d.state, credibility: d.credibility, ...statsOf(d.id) };
  },
};

// ── 启动 ─────────────────────────────────────────────────────────────────
(async function main() {
  try {
    G = await fetchJSON('data/graph.json');
  } catch (e) {
    document.getElementById('stats').innerHTML = `<div class="muted">加载 data/graph.json 失败：${e.message}（请用本地静态服务器打开，file:// 下 fetch 会被浏览器拦截）</div>`;
    return;
  }
  idxById = new Map(G.nodes.map((d, i) => [d.id, i]));
  // 边预存两端下标（pickEdgeIndex 用；避免每次 hover 重建 Map）
  for (const l of G.links) { l._ai = idxById.get(l.source); l._bi = idxById.get(l.target); }
  // B4-2：受攻击节点 = 作为 attack 边 target 的节点
  attackedSet = new Set();
  for (const l of G.links) if (l.kind === 'attack') attackedSet.add(l.target);
  layout(G.nodes, G.links);
  renderLead(); renderStats(); renderDetail(-1); wireFilters(); resize();
  window.addEventListener('resize', resize);
  const gpu = await tryCosmos();
  if (!gpu) draw();
  // 首屏"会动"：轻度自转（仅 2D）
  if (!gpu) {
    let t = 0;
    setInterval(() => { t += 1; if (t % 3 === 0 && !dragging && selected < 0) { view.x += 0.35; draw(); } }, 60);
  }
})();
