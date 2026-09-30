// 666 B2 · 首页逻辑（从 index.html 内联脚本抽出：可缓存、可审、可单测）
//
// 数据纪律：**只渲染，不写死**。所有数字来自
//   · web/data/metrics_666.json（tools/web_metrics_666.py 现算：卡数/规则数/检出率/账本/时间线/提交）
//   · web/data/status.json（tools/web_status_655.py 现算：保护器/逃逸率/W2）
//   · web/data/graph.json（星图真数据）
// 拿不到就显示"不可用"，绝不猜（见 docs/discipline/error_handling.md）。
import { STATE_COLORS, fetchJSON, fmtInt } from './app.js';
import {
  initRobustness, fetchJSON as robustFetch, renderErrorCard, renderEmpty,
  setState, formatMetric,
} from './js/robustness.js';

const $ = (id) => document.getElementById(id);
const REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/** 数字滚动（真实数值 → 0 计到目标；尊重 reduced-motion）。 */
export function countUp(el, target, { fmt = fmtInt, suffix = '', dur = 900 } = {}) {
  if (!el) return;
  const put = (v) => { if (typeof el.setNum === 'function') el.setNum(v); else el.textContent = v; };
  if (REDUCED || !isFinite(target)) { put(fmt(target) + suffix); return; }
  const t0 = performance.now();
  const step = (now) => {
    const k = Math.min(1, (now - t0) / dur);
    const eased = 1 - Math.pow(1 - k, 3);
    const v = target * eased;
    put(fmt(Number.isInteger(target) ? Math.round(v) : v) + suffix);
    if (k < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

/* ── ① 核心指标（B2：卡数 / 规则数 / 检出率 / 账本）─────────────── */
function metricCard([num, unit, cap, sub]) {
  const d = document.createElement('div');
  d.className = 'metric';
  const n = document.createElement('div');
  n.className = 'num';
  n.textContent = '0';
  const u = document.createElement('span');
  u.className = 'unit';
  u.textContent = unit || '';
  n.appendChild(u);
  const c = document.createElement('div'); c.className = 'cap'; c.textContent = cap;
  const s = document.createElement('div'); s.className = 'sub'; s.textContent = sub || '';
  d.append(n, c, s);
  d._num = n; d._unit = u;
  return d;
}

export async function renderMetrics() {
  const box = $('metrics');
  if (!box) return;
  setState(box, 'loading');
  let M;
  try {
    const r = await robustFetch('data/metrics_666.json', { requiredKeys: ['metrics'] });
    M = r.data.metrics;
    if (!M || Object.keys(M).length === 0) {
      setState(box, 'empty');
      renderEmpty(box, 'no-data', renderMetrics);
      return;
    }
  } catch (e) {
    setState(box, 'error');
    renderErrorCard(box, e.kind || 'unknown', renderMetrics);
    return;
  }
  setState(box, 'ready');
  const h = M.holdout || {};
  const spec = [
    [M.cards_real ?? 0, '', '知识卡（实卡域）',
      `另有 ${M.cards_draft ?? '—'} 张 draft650 草稿，不计入实卡域`],
    [M.rules_total ?? 0, '', '判决规则', '与 data/_gate_rules.json 同源（口径见 docs/caliber_convergence_658.md）'],
    [h.rate_pct ?? 0, '%', 'holdout 检出率', `catch ${h.catch} / miss ${h.miss} / unknown ${h.unknown}（unknown 不计分母）`],
    [M.ledger_events ?? 0, '', '账本事件', `${M.ledger_path || ''}（红线：零改）`],
  ];
  box.innerHTML = '';
  const nodes = spec.map(metricCard);
  nodes.forEach((n) => box.appendChild(n));
  spec.forEach(([v, _u, _c, _s], i) => {
    const n = nodes[i]._num;
    const put = (txt) => { n.textContent = ''; n.appendChild(document.createTextNode(txt)); n.appendChild(nodes[i]._unit); };
    if (v == null || v === 0) { put(formatMetric(v)); return; }  // B3：0/缺失显示 '--'，不误导
    countUp({ setNum: put }, v, { suffix: '' });
  });
  const note = $('metrics-note');
  if (note) {
    note.textContent = `检出率口径：${h.caliber || '—'}；复算 ${h.cmd || '—'}`
      + (M.external ? `　·　外部语料 ${M.external.rate_pct}%（${M.external.total} 条）` : '')
      + `　·　透明日志 ${M.transparency_log_entries ?? '—'} 条　·　Merkle ${M.merkle_dirs ? M.merkle_dirs.length : '—'} 目录 / ${M.merkle_files ?? '—'} 文件`;
  }
}

/* ── ② 系统状态时间线 ─────────────────────────────────────────── */
export async function renderTimeline() {
  const box = $('timeline');
  if (!box) return;
  try {
    const D = await fetchJSON('data/metrics_666.json');
    box.innerHTML = (D.timeline || []).map((m) => `
      <li data-state="${m.state}">
        <div class="t-when">${m.batch} · ${m.date}</div>
        <div class="t-what">${m.what}</div>
        <div class="t-why">${m.why}</div>
      </li>`).join('');
  } catch (e) {
    box.innerHTML = `<li><div class="t-why">时间线不可用：${e.message}</div></li>`;
  }
}

/* ── ③ 最新提交 ──────────────────────────────────────────────── */
export async function renderCommits() {
  const box = $('commits');
  if (!box) return;
  try {
    const D = await fetchJSON('data/metrics_666.json');
    const rows = D.commits || [];
    if (!rows.length) { renderEmpty(box, 'no-commits', renderCommits); return; }
    box.innerHTML = `<ul class="mono" style="list-style:none;margin:0;padding:0;font-size:12px">` +
      rows.map((c) => `<li style="padding:3px 0"><span class="muted">${c.date}</span>
        <span class="kbd">${c.hash}</span> ${c.subject}</li>`).join('') + '</ul>';
  } catch (e) {
    renderErrorCard(box, e.kind || 'unknown', renderCommits);
  }
}

/* ── ④ 系统现状面板（655 D 既有：保护器 / 逃逸率）────────────── */
export async function renderStatus() {
  const grid = $('status-grid');
  if (!grid) return;
  setState(grid, 'loading');
  try {
    const S = (await robustFetch('data/status.json', { requiredKeys: ['cards'] })).data;
    const cards = S.cards || {}, prot = S.protectors || {}, esc = S.escape || {};
    const sub = (id, text) => $(id).setAttribute('sub', text);
    countUp($('s-cards'), cards.cards_real ?? 0);
    sub('s-cards', `另有 ${cards.cards_draft ?? '—'} 张 draft650 草稿 · verified ${(cards.card_statuses || {}).verified ?? '—'}`);
    countUp($('s-prot'), prot.protectors_total ?? 0);
    const miss = (prot.protectors_missing || []).length;
    sub('s-prot', miss ? `⚠ 缺 ${miss} 个：${prot.protectors_missing.join(', ')}`
                       : '全部就位 · 源：queyi-core/tools/');
    if (esc.available && esc.rate_pct != null) {
      countUp($('s-escape'), esc.rate_pct, { fmt: (v) => Number(v).toFixed(4), suffix: '%' });
      sub('s-escape', `${esc.escaped}/${esc.denominator}（v7 基线漏检率，**非**本书真实错误率；交叉核对 616：${esc.frozen_matches ? '一致' : '不一致'}）`);
    } else {
      $('s-escape').setNum('不可用');
    }
    const un = S.unavailable || [];
    $('status-note').textContent =
      `数据来源：${(S.generated_from || []).join('　·　')}　生成于 ${S.generated_at || '—'}`
      + (un.length ? `　⚠ 缺项：${un.join('；')}` : '');
  } catch (e) {
    setState(grid, 'error');
    renderErrorCard(grid, e.kind || 'unknown', renderStatus);
  }
}

/* ── ⑤ hero 小图（真数据、会动；非装饰）───────────────────────── */
export async function renderHero() {
  const canvas = $('mini');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const stage = $('stage');
  const RAD = { card: 6.4, prop: 3.4, misconception: 2.6 };
  const ALPHA = (c) => (c >= 3 ? 1 : c === 2 ? .72 : .5);
  let G, pos = [], t = 0, hover = -1;

  const resize = () => {
    const dpr = Math.min(2, devicePixelRatio || 1), r = canvas.getBoundingClientRect();
    canvas.width = Math.floor(r.width * dpr); canvas.height = Math.floor(r.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  const initLayout = () => {
    const n = G.nodes.length;
    pos = G.nodes.map((_d, i) => {
      const a = (i / n) * Math.PI * 2 * 3.2, r = 120 + (i % 7) * 26;
      return { x: Math.cos(a) * r, y: Math.sin(a) * r * .62 };
    });
  };
  const draw = () => {
    const r = canvas.getBoundingClientRect();
    ctx.clearRect(0, 0, r.width, r.height);
    const idx = new Map(G.nodes.map((d, i) => [d.id, i]));
    ctx.save(); ctx.translate(r.width / 2, r.height / 2);
    const k = Math.min(1.5, r.width / 900) * 1.15;
    ctx.scale(k, k); ctx.rotate(t * 0.00035);
    for (const l of G.links) {
      if (l.kind === 'defend') continue;
      const a = idx.get(l.source), b = idx.get(l.target);
      if (a == null || b == null) continue;
      ctx.beginPath(); ctx.moveTo(pos[a].x, pos[a].y); ctx.lineTo(pos[b].x, pos[b].y);
      ctx.strokeStyle = l.defeated ? 'rgba(224,122,114,.42)' : 'rgba(150,150,150,.14)';
      ctx.lineWidth = l.defeated ? 1.1 : .5; ctx.stroke();
    }
    for (let i = 0; i < G.nodes.length; i++) {
      const d = G.nodes[i], p = pos[i];
      ctx.globalAlpha = hover >= 0 && hover !== i ? .28 : ALPHA(d.credibility);
      const rad = RAD[d.kind] || 3;
      ctx.beginPath();
      if (d.kind === 'misconception') ctx.rect(p.x - rad, p.y - rad, rad * 2, rad * 2);
      else ctx.arc(p.x, p.y, rad, 0, Math.PI * 2);
      ctx.fillStyle = STATE_COLORS[d.state] || STATE_COLORS.unknown; ctx.fill();
      if (d.kind === 'card') { ctx.lineWidth = .9; ctx.strokeStyle = 'rgba(232,230,227,.5)'; ctx.stroke(); }
      ctx.globalAlpha = 1;
    }
    ctx.restore();
  };
  const tick = () => {
    t += 1;
    for (let i = 0; i < pos.length; i++) {
      pos[i].x += Math.sin((t + i * 37) * 0.004) * 0.10;
      pos[i].y += Math.cos((t + i * 53) * 0.004) * 0.10;
    }
    draw(); requestAnimationFrame(tick);
  };
  canvas.addEventListener('mousemove', (e) => {
    const r = canvas.getBoundingClientRect();
    ctx.save(); ctx.translate(r.width / 2, r.height / 2);
    const k = Math.min(1.5, r.width / 900) * 1.15;
    const x = (e.clientX - r.left - r.width / 2) / k, y = (e.clientY - r.top - r.height / 2) / k;
    let best = -1, bd = 14;
    for (let i = 0; i < pos.length; i++) {
      const d = Math.hypot(pos[i].x - x, pos[i].y - y);
      if (d < bd) { bd = d; best = i; }
    }
    ctx.restore(); hover = best;
    canvas.style.cursor = best >= 0 ? 'pointer' : 'default';
  });
  canvas.addEventListener('mouseleave', () => { hover = -1; });

  try {
    G = await fetchJSON('data/graph.json');
  } catch (e) {
    stage?.classList.add('fallback-note');
    const chip = $('mode-chip');
    if (chip) chip.textContent = '需经本地静态服务器打开（file:// 下 fetch 受限）';
    return;
  }
  const c = G.meta.counts, w2 = G.meta.w2_summary || {};
  const stats = [[c.nodes, '节点'], [c.by_kind?.attack, '攻击边'], [c.defeated_links, '击败边'],
                 [c.cards, '知识卡'], [c.props, '命题'], [null, 'IN / OUT']];
  const box = $('stats');
  if (box) {
    box.innerHTML = stats.map(([_v, l], i) => `
      <div class="card"><div class="stat" id="stat-${i}">0</div><div class="stat-label">${l}</div></div>`).join('');
    stats.forEach(([v, _l], i) => {
      const el = $('stat-' + i);
      if (v == null) el.textContent = `${w2.IN ?? '—'} / ${w2.OUT ?? '—'}`;
      else countUp(el, v);
    });
  }
  const btn = $('starmap-btn');
  if (btn) btn.setAttribute('label', `打开星图（${fmtInt(c.nodes)} 节点）`);
  const sn = $('src-note');
  if (sn) sn.textContent = '数据来源：' + (G.meta.generated_from || []).join('　·　');
  const chip = $('mode-chip');
  if (chip) chip.textContent = `${fmtInt(c.links)} 条边真实渲染 · 计数为滚动动画`;
  initLayout(); resize();
  window.addEventListener('resize', () => { resize(); draw(); });
  requestAnimationFrame(tick);
}

export function boot() {
  initRobustness();
  renderMetrics();
  renderTimeline();
  renderCommits();
  renderStatus();
  renderHero();
}

if (document.readyState !== 'loading') boot();
else document.addEventListener('DOMContentLoaded', boot);
