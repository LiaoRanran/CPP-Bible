// 666 B2 → 671d C1 → 671d2 D → 672c · 首页逻辑（从 index.html 内联脚本抽出：可缓存、可审、可单测）
//
// 数据纪律：**只渲染，不写死**。所有数字来自
//   · web/data/metrics_666.json（tools/web_metrics_666.py 现算：卡数/规则数/检出率/账本/时间线/提交）
// 拿不到就写 `--`（formatMetric / 占位），绝不猜、绝不填 0 充当真实值（见 docs/discipline/error_handling.md）。
//
// 672b：数据层单点（fetchJSON / esc / formatMetric / pct）统一收口到 ./js/data.js
// 672c：首页彻底重制（学术克制版式）—— 摘要/核心指标/架构/演化/复现/提交全部现算，无硬编码数字、
//       无数字滚动、无骨架屏、无渐变/毛玻璃/辉光。
import { fmtInt } from './app.js';
import {
  initRobustness, fetchJSON as robustFetch, renderErrorCard, renderEmpty,
  setState,
} from './js/robustness.js';
import { fetchJSON, esc, formatMetric, pct } from './js/data.js';

const $ = (id) => document.getElementById(id);

/* ── 空值保护：`--` 表示"取不到"，与 0 严格区分 ─────────────────── */
const nz = (v, suffix = '') => (v == null ? '--' : fmtInt(v) + suffix);
/** P / R / F1 这类 [0,1] 值固定一位小数：`1` 与 `1.0` 在读数语境里不是一回事。 */
const dec1 = (v) => (v == null ? '--' : Number(v).toFixed(1));

function setText(id, v) {
  const el = $(id);
  if (el) el.textContent = (v == null || v === '') ? '--' : String(v);
}

/* ── ① 现状表：行定义（字段全部来自 metrics_666.json，不在这里写死数字） ── */
function metricRows(M) {
  const h = M.holdout || {};
  const ext = M.external || {};
  const cf = M.counterfactual || {};
  const opt = (h.opt_levels || []).join(' / ') || '--';
  const excluded = Object.entries((ext.denominator && ext.denominator.excluded) || {})
    .map(([k, v]) => `${k} ${v}`).join('、');
  return [
    {
      name: '盲集检出率（holdout）',
      value: pct(h.rate_pct),
      n: `${nz(h.catch)} / ${nz(h.den)}`,
      caliber: `catch ${nz(h.catch)}、miss ${nz(h.miss)}；unknown ${nz(h.unknown)} 不计入分母；`
        + `双档 ${opt} 任一档报出即 catch`,
      cmd: h.cmd || '--',
    },
    {
      name: '外部语料（可测口径）',
      value: pct(ext.rate_pct),
      n: `${nz(ext.catch)} / ${nz(ext.den)}`,
      caliber: `全样本 ${pct(ext.rate_pct_all)}（${nz(ext.catch)}/${nz(ext.total)}）`
        + (excluded ? `；剔除 ${excluded}` : ''),
      cmd: ext.cmd || '--',
    },
    {
      name: '反事实 P / R / F1',
      value: `${dec1(cf.p)} / ${dec1(cf.r)} / ${dec1(cf.f1)}`,
      n: `${nz(cf.cases)} 案`,
      caliber: `分母 = 带 ground_truth 标签的案例数；第三次判据命中 ${nz(cf.third_criterion_hits)}`,
      cmd: cf.cmd || '--',
    },
    {
      name: '真机验证卡',
      value: nz(M.cards_real, ' 张'),
      n: `草稿 ${nz(M.cards_draft)}`,
      caliber: '草稿（draft650）不计入实卡域；卡即断言，逐张带边界与证据',
      cmd: 'python tools/web_metrics_666.py',
    },
    {
      name: '门禁规则',
      value: nz(M.rules_total, ' 条'),
      n: '',
      caliber: '与 data/_gate_rules.json 同源（口径见 docs/caliber_convergence_658.md）',
      cmd: 'python tools/web_metrics_666.py',
    },
    {
      name: '账本事件',
      value: nz(M.ledger_events, ' 条'),
      n: '',
      caliber: `${M.ledger_path || '--'}（红线：${M.ledger_redline || '--'}）`,
      cmd: 'python tools/web_metrics_666.py',
    },
    {
      name: '透明日志 / Merkle',
      value: `${nz(M.transparency_log_entries, ' 条')} / ${nz((M.merkle_dirs || []).length, ' 目录')}`,
      n: `${nz(M.merkle_files)} 文件`,
      caliber: `Merkle 覆盖目录：${(M.merkle_dirs || []).join('、') || '--'}`,
      cmd: 'python tools/web_metrics_666.py',
    },
  ];
}

/* ── ② 摘要 + 页脚更新时间：数字现算，取不到留占位 ── */
export async function renderAbstract() {
  if (!$('ab-holdout')) return;
  try {
    const D = await fetchJSON('data/metrics_666.json');
    const M = (D && D.metrics) || {};
    const h = M.holdout || {};
    const ext = M.external || {};
    setText('ab-holdout', pct(h.rate_pct));
    setText('ab-holdout-n', `${nz(h.catch)}/${nz(h.den)}`);
    setText('ab-corpus', pct(ext.rate_pct));
    setText('ab-corpus-n', `${nz(ext.catch)}/${nz(ext.den)}`);
    setText('ab-cards', nz(M.cards_real));
    setText('ab-rules', nz(M.rules_total));
    setText('ab-ledger', nz(M.ledger_events));
    setText('last-updated', (D && D.generated_at) || '--');
  } catch (e) {
    /* 留 -- 占位，不抛、不影响其余区块 */
  }
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
  const rows = metricRows(M);
  box.innerHTML = `<table class="state-table">
  <caption>表 1　核心指标。数据源 web/data/metrics_666.json（tools/web_metrics_666.py 现算）；<span class="mono">--</span> 表示该字段取不到值。</caption>
  <thead><tr><th>指标</th><th>值</th><th>口径</th><th>复算命令</th></tr></thead>
  <tbody>${rows.map((r) => `<tr>
    <td>${esc(r.name)}</td>
    <td class="mono nowrap">${esc(r.value)} <span class="muted">${esc(r.n)}</span></td>
    <td>${esc(r.caliber)}</td>
    <td class="mono">${esc(r.cmd)}</td>
  </tr>`).join('')}</tbody>
</table>`;
  const note = $('metrics-note');
  if (note) {
    note.textContent = `环境：${M.holdout && M.holdout.env ? M.holdout.env : '--'}`
      + `　·　数据源 web/data/metrics_666.json，本页只渲染、不写死数字。`;
  }
}

/* ── ③ 演化：只取最近 5 个节点 ──────────────────────────────── */
const TIMELINE_MAX = 5;

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
      <li data-state="${esc(m.state)}">
        <div class="t-when">${esc(m.batch)} · ${esc(m.date)}</div>
        <div class="t-what">${esc(m.what)}</div>
        <div class="t-why">${esc(m.why)}</div>
      </li>`).join('');
  } catch (e) {
    box.innerHTML = `<li><div class="t-why">时间线不可用：${esc(e.message)}</div></li>`;
  }
}

/* ── ④ 最近提交 ──────────────────────────────────────────────── */
export async function renderCommits() {
  const box = $('commits');
  if (!box) return;
  try {
    const D = await fetchJSON('data/metrics_666.json');
    const rows = D.commits || [];
    if (!rows.length) { renderEmpty(box, 'no-commits', renderCommits); return; }
    box.innerHTML = `<ul class="commit-list">` +
      rows.map((c) => `<li><span class="c-when mono">${esc(c.date)}</span>
        <span class="kbd">${esc(c.hash)}</span> <span class="c-sub">${esc(c.subject)}</span></li>`).join('') + '</ul>';
  } catch (e) {
    renderErrorCard(box, e.kind || 'unknown', renderCommits);
  }
}

export function boot() {
  initRobustness();
  renderAbstract();
  renderMetrics();
  renderTimeline();
  renderCommits();
}

if (document.readyState !== 'loading') boot();
else document.addEventListener('DOMContentLoaded', boot);
