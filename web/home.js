// 666 B2 → 671d C1 · 首页逻辑（从 index.html 内联脚本抽出：可缓存、可审、可单测）
//
// 数据纪律：**只渲染，不写死**。所有数字来自
//   · web/data/metrics_666.json（tools/web_metrics_666.py 现算：卡数/规则数/检出率/账本/时间线/提交）
// 拿不到就显示"不可用"，绝不猜（见 docs/discipline/error_handling.md）。
//
// 671d 改动（去 AI 味 D1 / 动效 B5）：
//   · **删除数字滚动动画**（原来 0→目标 计 900ms）：数字是事实，不需要表演；
//   · **删除首屏 canvas 星图与自转动画**：无限循环动画被明令禁止，且它把首页变成装饰页；
//   · 时间线只取最近 8 个节点（原来全部铺开 → 信息堆砌）。
import { fetchJSON, fmtInt } from './app.js';
import {
  initRobustness, fetchJSON as robustFetch, renderErrorCard, renderEmpty,
  setState, formatMetric,
} from './js/robustness.js';

const $ = (id) => document.getElementById(id);

/** 直接写数字（671d：不再做 0→target 的滚动动画）。
 *  保留 countUp 这个名字并导出，是为了不打断任何既有 import —— 它现在就是"写一次"。 */
export function countUp(el, target, { fmt = fmtInt, suffix = '' } = {}) {
  if (!el) return;
  const txt = (target == null || !isFinite(target)) ? '—' : fmt(target) + suffix;
  if (typeof el.setNum === 'function') el.setNum(txt);
  else if (el && typeof el === 'object' && 'textContent' in el) el.textContent = txt;
}

/* ── ① 核心指标：盲集检出率 / 真机验证卡 / 门禁规则 / 演化记录 ────── */
function metricCard([num, unit, cap, sub]) {
  const d = document.createElement('div');
  d.className = 'metric';
  const n = document.createElement('div');
  n.className = 'num';
  const u = document.createElement('span');
  u.className = 'unit';
  u.textContent = unit || '';
  n.append(document.createTextNode('—'), u);
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
    [h.rate_pct ?? 0, '%', '盲集检出率', `catch ${h.catch ?? '—'} / miss ${h.miss ?? '—'} / unknown ${h.unknown ?? '—'}（unknown 不计分母）`],
    [M.cards_real ?? 0, '', '真机验证卡', `另有 ${M.cards_draft ?? '—'} 张 draft650 草稿，不计入实卡域`],
    [M.rules_total ?? 0, '', '门禁规则', '与 data/_gate_rules.json 同源（口径见 docs/caliber_convergence_658.md）'],
    [M.ledger_events ?? 0, '', '演化记录', `${M.ledger_path || ''}（红线：零改）`],
  ];
  box.innerHTML = '';
  const nodes = spec.map(metricCard);
  nodes.forEach((n) => box.appendChild(n));
  spec.forEach(([v, _u, _c, _s], i) => {
    const n = nodes[i]._num;
    const put = (txt) => { n.textContent = ''; n.append(document.createTextNode(txt), nodes[i]._unit); };
    put(v == null || v === 0 ? formatMetric(v) : fmtInt(v));
  });
  const note = $('metrics-note');
  if (note) {
    note.textContent = `检出率口径：${h.caliber || '—'}；复算 ${h.cmd || '—'}`
      + (M.external ? `　·　外部语料 ${M.external.rate_pct}%（${M.external.total} 条）` : '')
      + `　·　透明日志 ${M.transparency_log_entries ?? '—'} 条　·　Merkle ${M.merkle_dirs ? M.merkle_dirs.length : '—'} 目录 / ${M.merkle_files ?? '—'} 文件`;
  }
}

/* ── ② 演化时间线：只取最近 8 个节点 ────────────────────────── */
const TIMELINE_MAX = 8;

export async function renderTimeline() {
  const box = $('timeline');
  if (!box) return;
  try {
    const D = await fetchJSON('data/metrics_666.json');
    const all = D.timeline || [];
    // 账本按时间正序；取**最近** TIMELINE_MAX 条，再按时间倒序展示（新的在上）
    const rows = all.slice(-TIMELINE_MAX).reverse();
    if (!rows.length) { renderEmpty(box, 'no-data', renderTimeline); return; }
    box.innerHTML = rows.map((m) => `
      <li data-state="${m.state}">
        <div class="t-when">${m.batch} · ${m.date}</div>
        <div class="t-what">${m.what}</div>
        <div class="t-why">${m.why}</div>
      </li>`).join('');
  } catch (e) {
    box.innerHTML = `<li><div class="t-why">时间线不可用：${e.message}</div></li>`;
  }
}

/* ── ③ 最近提交 ──────────────────────────────────────────────── */
export async function renderCommits() {
  const box = $('commits');
  if (!box) return;
  try {
    const D = await fetchJSON('data/metrics_666.json');
    const rows = D.commits || [];
    if (!rows.length) { renderEmpty(box, 'no-commits', renderCommits); return; }
    box.innerHTML = `<ul class="commit-list">` +
      rows.map((c) => `<li><span class="c-when mono">${c.date}</span>
        <span class="kbd">${c.hash}</span> <span class="c-sub">${c.subject}</span></li>`).join('') + '</ul>';
  } catch (e) {
    renderErrorCard(box, e.kind || 'unknown', renderCommits);
  }
}

export function boot() {
  initRobustness();
  renderMetrics();
  renderTimeline();
  renderCommits();
}

if (document.readyState !== 'loading') boot();
else document.addEventListener('DOMContentLoaded', boot);
