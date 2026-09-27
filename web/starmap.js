// 653 B · 星图 hero：W2 接地图（178 节点 / 388 攻击边 / 194 击败边）三维编码
//   色 = 四态 · 大小 = 节点类型（卡 > 命题 > 误解）· 光（透明度）= credibility
// 渲染：优先 cosmos.gl v3（CDN, GPU）；不可达时**诚实降级**为 2D canvas（同编码，可交互）。
import { STATE_COLORS, STATE_LABELS, KIND_LABELS, LINK_STYLE, fetchJSON, fmtInt, mountNav } from './app.js';

mountNav('starmap.html');

const canvas = document.getElementById('graph');
const stage = document.getElementById('stage');
const tip = document.getElementById('tip');

let G = null;          // graph.json
let view = { x: 0, y: 0, k: 1 };
let pos = [];          // [{x,y}]
let visible = new Set();
const filters = { pass: true, pass_with_exception: true, fail: true, unknown: true, defeatedOnly: false };

const RADIUS = { card: 7.5, prop: 4.2, misconception: 3.2 };
const alphaOf = (c) => (c >= 3 ? 1.0 : c === 2 ? 0.72 : 0.5);

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

// ── 2D 渲染 ──────────────────────────────────────────────────────────────
const ctx = canvas.getContext('2d');
let hovered = -1, selected = -1;

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
  const idx = new Map(G.nodes.map((d, i) => [d.id, i]));
  // 边（击败边加亮；攻击边按击败与否区分）
  for (const l of G.links) {
    if (!passLink(l)) continue;
    const a = idx.get(l.source), b = idx.get(l.target);
    if (a == null || b == null || !passFilter(G.nodes[a]) || !passFilter(G.nodes[b])) continue;
    const st = LINK_STYLE[l.kind] || LINK_STYLE.attack;
    const defeated = l.defeated && l.kind === 'attack';
    ctx.beginPath();
    const A = toScreen(pos[a]), B = toScreen(pos[b]);
    ctx.moveTo(A.x, A.y); ctx.lineTo(B.x, B.y);
    ctx.strokeStyle = `rgba(${defeated ? '217,107,107' : st.color},${defeated ? 0.42 : st.alpha})`;
    ctx.lineWidth = (defeated ? 1.15 : st.width) * view.k;
    ctx.stroke();
  }
  // 节点
  const sel = selected >= 0 ? G.nodes[selected] : null;
  const neigh = sel ? neighbors(sel.id) : null;
  for (let i = 0; i < G.nodes.length; i++) {
    const d = G.nodes[i];
    if (!passFilter(d)) continue;
    const p = toScreen(pos[i]);
    const rad = (RADIUS[d.kind] || 4) * view.k * (d.kind === 'card' ? 1 : 1);
    const dim = sel && !(neigh.has(d.id) || d.id === sel.id);
    ctx.globalAlpha = dim ? 0.18 : alphaOf(d.credibility);
    ctx.beginPath();
    // 形通道：卡=圆、命题=圆（小）、误解=方（一眼可分）
    if (d.kind === 'misconception') ctx.rect(p.x - rad, p.y - rad, rad * 2, rad * 2);
    else ctx.arc(p.x, p.y, rad, 0, Math.PI * 2);
    ctx.fillStyle = STATE_COLORS[d.state] || STATE_COLORS.unknown;
    ctx.fill();
    if (d.kind === 'card') { ctx.lineWidth = 1; ctx.strokeStyle = 'rgba(230,232,234,.55)'; ctx.stroke(); }
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
  // hover 拾取
  const w = toWorld(e.clientX - r.left, e.clientY - r.top);
  let best = -1, bd = 18 / view.k;
  for (let i = 0; i < (G?.nodes.length || 0); i++) {
    if (!passFilter(G.nodes[i])) continue;
    const d = Math.hypot(pos[i].x - w.x, pos[i].y - w.y);
    if (d < bd) { bd = d; best = i; }
  }
  hovered = best;
  if (best >= 0) {
    const d = G.nodes[best];
    tip.style.display = 'block';
    tip.style.left = `${e.clientX - r.left + 14}px`;
    tip.style.top = `${e.clientY - r.top + 12}px`;
    tip.innerHTML = `<div class="t">${d.id}</div>
      <div class="m">${KIND_LABELS[d.kind] || d.kind} · ${STATE_LABELS[d.state] || d.state}</div>
      <div class="m">domain=${d.domain} · credibility=${d.credibility}${d.label ? ' · label=' + d.label : ''}</div>
      ${d.title ? `<div class="m">${d.title}</div>` : ''}`;
    canvas.style.cursor = 'pointer';
  } else { tip.style.display = 'none'; canvas.style.cursor = 'grab'; }
});
canvas.addEventListener('click', () => { if (!moved) { selected = hovered; draw(); } });
canvas.addEventListener('wheel', (e) => {
  e.preventDefault();
  view.k = Math.max(0.25, Math.min(4, view.k * (e.deltaY < 0 ? 1.12 : 1 / 1.12)));
  draw();
}, { passive: false });

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

function wireFilters() {
  for (const k of ['pass', 'pass_with_exception', 'fail', 'unknown']) {
    const cb = document.getElementById('f-' + k);
    cb.addEventListener('change', () => { filters[k] = cb.checked; draw(); });
  }
  const dd = document.getElementById('f-defeated');
  dd.addEventListener('change', () => { filters.defeatedOnly = dd.checked; draw(); });
  document.getElementById('reset').addEventListener('click', () => {
    view = { x: 0, y: 0, k: 1 }; selected = -1; draw();
  });
}

// ── cosmos.gl v3（可选增强）──────────────────────────────────────────────
async function tryCosmos() {
  try {
    const mod = await import('https://cdn.jsdelivr.net/npm/@cosmograph/cosmos@3/+esm');
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
    const n = G.nodes, idx = new Map(n.map((d, i) => [d.id, i]));
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
    G.links.forEach((l, i) => { L[i * 2] = idx.get(l.source) ?? 0; L[i * 2 + 1] = idx.get(l.target) ?? 0; });
    graph.setPointPositions(P); graph.setPointSizes(S); graph.setPointColors(C); graph.setLinks(L);
    graph.render();
    stage.classList.remove('fallback-note');
    document.getElementById('mode').textContent = 'GPU · cosmos.gl v3';
    return true;
  } catch (e) {
    stage.classList.add('fallback-note');
    document.getElementById('mode').textContent = '2D canvas（降级）';
    return false;
  }
}

// ── 启动 ─────────────────────────────────────────────────────────────────
(async function main() {
  try {
    G = await fetchJSON('data/graph.json');
  } catch (e) {
    document.getElementById('stats').innerHTML = `<div class="muted">加载 data/graph.json 失败：${e.message}（请用本地静态服务器打开，file:// 下 fetch 会被浏览器拦截）</div>`;
    return;
  }
  layout(G.nodes, G.links);
  renderStats(); wireFilters(); resize();
  window.addEventListener('resize', resize);
  const gpu = await tryCosmos();
  if (!gpu) draw();
  // 首屏"会动"：轻度自转（仅 2D）
  if (!gpu) {
    let t = 0;
    setInterval(() => { t += 1; if (t % 3 === 0 && !dragging && selected < 0) { view.x += 0.35; draw(); } }, 60);
  }
})();
