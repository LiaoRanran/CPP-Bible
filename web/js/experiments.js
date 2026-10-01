// ═══════════════════════════════════════════════════════════════════════════
// 672g B · 实验结果页 **DOM 层**（取数 / 渲染 / 事件）
//
// 由来：experiments.html 的 180–386 行内联 module 脚本（约 200 行）无法被 Node 测试。
//   672g 把它外抽成两层，行为逐字保持：
//     · js/experiments_core.js —— 合并 / 口径挑选 / 文案（纯函数，可 Node 直测）
//     · 本文件                 —— fetch + innerHTML + addEventListener（**不写算法**）
//
// 兜底纪律（照搬内联版）：任何一张图出错都降级成空状态，绝不让整页崩。
// ═══════════════════════════════════════════════════════════════════════════

import { fetchJSON } from '../app.js';
import {
  BASELINE_PATHS, PENDING,
  loadBaselines, loadSupplements,
  buildGroupedBars, buildCaliberBars, buildLineChart, buildPie, buildRadar,
  emptyStateSvg, selectionFromDataset, selectionDetail, detailPanelHtml,
  buildEvolutionSeries, buildDetectorSlices, buildAbilityAxes,
} from './charts.js';
import {
  ALL_DATASETS, initialState, pickDatasets,
  mergedField, mergedCalibers, mergedDetectors,
  baselineNoteText, caliberArms, caliberNoteText,
  evolutionNoteText, batchesText, detectorNoteText, abilityNoteText,
  triedItems, sourceListHtml, sourceNoteText, errorText,
} from './experiments_core.js';

const $ = (id) => document.getElementById(id);
const state = initialState();

/* ── 渲染兜底：任何一张图出错都降级成空状态，绝不让整页崩 ── */
function safe(hostId, fn) {
  try { fn(); }
  catch (e) {
    const h = $(hostId);
    if (h) h.innerHTML = emptyStateSvg(errorText(e));
  }
}

/* ── 选中明细：点柱 / 扇区 / 点 ⇒ .detail-panel ── */
function wire(hostId, panelId, dataFn, opts) {
  const host = $(hostId);
  const panel = $(panelId);
  if (!host || !panel) return;
  const show = (ev) => {
    const t = ev.target;
    const el = (t && t.closest) ? t.closest('[data-role]') : null;
    if (!el) return;
    let detail = null;
    try { detail = selectionDetail(dataFn(), selectionFromDataset(el.dataset || {}), opts || {}); }
    catch (e) { detail = { ok: false, text: '明细渲染异常（已降级）：' + String((e && e.message) || e) }; }
    panel.innerHTML = detailPanelHtml(detail);
    panel.hidden = false;
    const prev = host.querySelector('.is-selected');
    if (prev && prev !== el) prev.classList.remove('is-selected');
    if (el.classList && (el.classList.contains('bar') || el.classList.contains('pie-seg') || el.classList.contains('line-dot'))) {
      el.classList.add('is-selected');
    }
  };
  host.addEventListener('click', show);
  host.addEventListener('keydown', (ev) => {
    if (ev.key === 'Enter' || ev.key === ' ' || ev.key === 'Spacebar') { ev.preventDefault(); show(ev); }
  });
}

/* ── ① baseline 分组柱 ── */
function renderBaseline() {
  const arms = state.arms || [];
  const note = baselineNoteText(state.base.sources);
  $('base-note').textContent = note;
  const svg = buildGroupedBars({
    title: 'baseline 对比 · 检出率（%）', unit: '%', datasets: state.datasets, arms: arms, width: 880, height: 380,
    emptyMsg: 'baseline 数据未就绪：按顺序尝试 ' + BASELINE_PATHS.join(' / ') + ' 全部失败 ⇒ 「' + PENDING + '」。'
      + '670a 写入后此处自动出现 Static / Random / Failure-driven 三臂 × holdout / corpus / defect 三语料。',
    note: note,
  });
  $('c-baseline').innerHTML = svg;
}
/* ── ② 口径消融 ── */
function renderCaliber() {
  const cal = state.calibers;
  if (!cal) {
    $('cal-note').textContent = '待 670a';
    $('c-caliber').innerHTML = emptyStateSvg('口径消融需要 caliber_ablation.arms（全样本 / 可测 / 排除 unknown）：当前未取到（' + PENDING + '）');
    return;
  }
  const arms = caliberArms(cal, state.caliber);
  $('cal-note').textContent = caliberNoteText(state.caliber, (cal.arms || []).length);
  $('c-caliber').innerHTML = buildCaliberBars({
    calibers: { arms: arms.length ? arms : (cal.arms || []), datasets: cal.datasets, note: cal.note, delta_pp: cal.delta_pp },
    title: '口径消融 · 分母效应（%）', unit: '%', width: 880, height: 380,
  });
}
/* ── ③ 演化折线 ── */
function renderEvolution() {
  const evo = state.evolution || buildEvolutionSeries({});
  $('evo-batches').textContent = batchesText(evo.batches);
  $('evo-note').textContent = evolutionNoteText(evo);
  $('c-evolution').innerHTML = buildLineChart({
    title: '系统演化 · 变异杀死率 / holdout 检出率（%）', unit: '%', yMax: 100, width: 880, height: 320,
    xLabels: evo.batches, series: evo.series, desc: evo.notes,
    emptyMsg: '演化折线需要批次骨架（timeline）与可追溯的真实率值：当前未取到（' + PENDING + '）',
  });
}
/* ── ④ 检测器构成 ── */
function renderDetectors() {
  const d = buildDetectorSlices({ detectors: mergedDetectors(state.base.sources), experiments: state.exp });
  $('det-note').textContent = detectorNoteText(d);
  $('c-detectors').innerHTML = buildPie({
    title: '检测器构成', slices: d.slices, width: 660, height: 320,
    emptyMsg: '检测器构成（sanitizer / compiler-warn / cross-compile / perf / compile-time）与回退分布都不可用（' + PENDING + '）',
  });
  $('d-detectors').innerHTML = detailPanelHtml({ ok: false, text: d.note });
  $('d-detectors').hidden = false;
}
/* ── ⑤ 能力构成雷达 ── */
function renderAbility() {
  const ab = buildAbilityAxes({
    metrics666: state.metrics, status: state.status, experiments: state.exp,
    graphNodes: (state.graph && Array.isArray(state.graph.nodes)) ? state.graph.nodes.length : null,
  });
  $('abi-note').textContent = abilityNoteText(ab);
  $('c-ability').innerHTML = buildRadar({ title: '能力构成（实际 / 目标）', axes: ab.axes, desc: ab.notes, width: 620, height: 400 });
}

function renderAll() {
  safe('c-baseline', renderBaseline);
  safe('c-caliber', renderCaliber);
  safe('c-evolution', renderEvolution);
  safe('c-detectors', renderDetectors);
  safe('c-ability', renderAbility);
}

/* ── 数据源状态（诚实登记 200 / 404） ── */
function renderSources() {
  $('src-list').innerHTML = sourceListHtml(triedItems(state.base, state.sup));
  $('src-note').textContent = sourceNoteText((state.base && state.base.sources) ? state.base.sources.length : 0);
}

/* ── 控件 ── */
function bindTabs(attr, onPick) {
  const btns = Array.prototype.slice.call(document.querySelectorAll('[' + attr + ']'));
  btns.forEach((b) => b.addEventListener('click', () => {
    btns.forEach((x) => x.setAttribute('aria-selected', String(x === b)));
    onPick(b.getAttribute(attr));
  }));
}

/* ── 启动 ── */
(async function main() {
  try {
    state.base = await loadBaselines(fetchJSON, BASELINE_PATHS);
  } catch (e) {
    state.base = { ok: false, sources: [], arms: [], tried: [{ path: '(loadBaselines 异常)', ok: false, error: String((e && e.message) || e) }] };
  }
  try {
    state.sup = await loadSupplements(fetchJSON);
  } catch (e) {
    state.sup = { results: {}, tried: [{ key: '(loadSupplements 异常)', path: '(补充源)', ok: false, error: String((e && e.message) || e) }] };
  }
  state.exp = state.sup.results.experiments || null;
  state.metrics = state.sup.results.metrics666 || null;
  state.status = state.sup.results.status || null;
  state.graph = state.sup.results.graph || null;
  const e669 = (state.base.sources || []).filter((s) => /669_experiments/.test(s.path))[0];
  state.e669 = e669 ? e669.raw : null;

  state.arms = state.base.arms || [];
  state.calibers = mergedCalibers(state.base.sources);
  state.evolution = buildEvolutionSeries({
    metrics666: state.metrics, experiments: state.exp, experiments669: state.e669,
    evolution: mergedField(state.base.sources, 'evolution'),
  });

  renderSources();
  renderAll();

  bindTabs('data-ds', (v) => {
    state.datasets = pickDatasets(v, ALL_DATASETS);
    safe('c-baseline', renderBaseline);
  });
  bindTabs('data-cal', (v) => {
    state.caliber = v || 'all';
    safe('c-caliber', renderCaliber);
  });

  wire('c-baseline', 'd-baseline', () => ({ arms: state.arms }), { note: '口径与分母见「口径消融」图；缺数据的柱标 n/a，不填 0' });
  wire('c-caliber', 'd-caliber', () => (state.calibers ? { arms: state.calibers.arms } : { arms: [] }));
  wire('c-evolution', 'd-evolution', () => ({ arms: [] }));
  wire('c-detectors', 'd-detectors', () => ({ arms: [] }));
  wire('c-ability', 'd-ability', () => ({ arms: [] }));
})();
