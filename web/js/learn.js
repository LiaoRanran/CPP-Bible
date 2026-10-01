// ═══════════════════════════════════════════════════════════════════════════
// 672g C · 学习页 **DOM 层**（取数 / 事件 / localStorage / 导入导出）
//
// 由来：learn.html 的 139–495 行内联 module 脚本（约 350 行）无法被 Node 测试。
//   672g 外抽成两层，行为逐字保持（含键盘导航 handleKey）：
//     · js/learn_core.js —— 过滤 + 全部 HTML/SVG 字符串生成（纯函数，可 Node 直测）
//     · 本文件           —— document / localStorage / Blob / FileReader / addEventListener
//
// 进度纪律（照搬内联版）：进度**只在 localStorage 本机保存**，可导出/导入，不出本机。
// ═══════════════════════════════════════════════════════════════════════════

import { fetchJSON } from '../app.js';
import {
  sm2, buildCardDeck, buildErrorDeck,
  deckStatsEx, dueQueue, pathProgress, masteryCurve, weakHeatmap,
  handleKey, exportPayload, importPayload,
} from './learn_engine.js';
import {
  STORE_KEY, QUEUE_LIMIT, esc,
  filterDeck, dashHtml, masteryPct, pathFlowSvg,
  curveNoteText, masteryCurveSvg, heatmapHtml, queueListHtml,
  cardViewHtml, posNoteText, emptyStudyHtml, loadErrorHtml,
  exportNoteText, importNoteText, stateOfCard,
} from './learn_core.js';

const $ = (id) => document.getElementById(id);

let ATOMS = [];          // 知识卡牌组
let ERRORS = [];         // 错例牌组
let progress = load();   // { [id]: state }
let deck = 'atom';       // 当前牌组
let list = [];           // 过滤后队列（card 对象）
let pos = 0;             // 当前在 list 中的下标
let revealed = false;
let deckSigned = null;   // 错例牌组是否已签（来自数据文件 signed 字段）

function load() {
  try { return JSON.parse(localStorage.getItem(STORE_KEY)) || {}; }
  catch { return {}; }
}
function save() {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(progress)); } catch { /* 隐私模式下忽略 */ }
}

// ── 数据加载（两路并行，互不阻塞）──
(async function init() {
  try {
    const [idx, errDeck] = await Promise.all([
      fetchJSON('data/cards_index.json'),
      // 670c 优先用带反例代码的错例牌组；取不到再退回 665 旧格式
      fetchJSON('data/err_deck_670c.json')
        .catch(() => fetchJSON('data/ig_cards_665.json').catch(() => ({ cards: [] }))),
    ]);
    ATOMS = buildCardDeck(idx.cards || []);
    ERRORS = buildErrorDeck(errDeck);
    deckSigned = typeof errDeck.signed === 'boolean' ? errDeck.signed : null;
    fillDomains();
    bindControls();
    render();
  } catch (e) {
    $('study').innerHTML = loadErrorHtml(e);
  }
})();

function fillDomains() {
  const wrap = $('f-domain-wrap');
  if (deck !== 'atom') { wrap.hidden = true; return; }
  wrap.hidden = false;
  const doms = [...new Set(ATOMS.map((c) => c.domain).filter(Boolean))].sort();
  $('f-domain').innerHTML = '<option value="">全部</option>'
    + doms.map((d) => '<option value="' + esc(d) + '">' + esc(d) + '</option>').join('');
}

function bindControls() {
  document.querySelectorAll('.deck-tab').forEach((b) => b.addEventListener('click', () => {
    document.querySelectorAll('.deck-tab').forEach((x) => x.setAttribute('aria-selected', 'false'));
    b.setAttribute('aria-selected', 'true');
    deck = b.dataset.deck; pos = 0; revealed = false;
    fillDomains(); render();
  }));
  $('q').addEventListener('input', () => { pos = 0; render(); });
  $('f-domain').addEventListener('change', () => { pos = 0; render(); });
  $('f-scope').addEventListener('change', () => { pos = 0; render(); });
  $('export').addEventListener('click', exportProgress);
  $('import').addEventListener('click', () => $('import-file').click());
  $('import-file').addEventListener('change', importProgress);
  $('reset-progress').addEventListener('click', () => {
    if (confirm('清空本机全部学习进度？此操作不可撤销。')) { progress = {}; save(); render(); }
  });
  document.addEventListener('keydown', onKey);
}

// ── 键盘快捷键（判定逻辑在 learn_engine.handleKey，纯函数可测）──
function onKey(e) {
  const tag = e.target && e.target.tagName;
  if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') return;  // 不抢输入框的键
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  const r = handleKey(e.key, { hasCard: list.length > 0, revealed, index: pos, length: list.length });
  if (r.action === 'none') return;
  e.preventDefault();
  if (r.action === 'reveal') { revealed = true; renderStudy(); }
  else if (r.action === 'prev') { pos = (pos - 1 + list.length) % list.length; revealed = false; renderStudy(); }
  else if (r.action === 'next') { pos = (pos + 1) % list.length; revealed = false; renderStudy(); }
  else if (r.action === 'grade') grade(list[pos], r.q);
}

// ── 过滤 + 队列生成 ──
function currentDeck() { return deck === 'atom' ? ATOMS : ERRORS; }
function filterList() {
  return filterDeck(currentDeck(), {
    q: ($('q').value || ''),
    domain: $('f-domain').value,
    scope: $('f-scope').value,
    progress, isAtom: deck === 'atom',
  });
}

// ── 渲染：路径 + 统计 + 可视化 + 队列 + 当前卡 ──
function render() {
  const d = currentDeck();
  const stats = deckStatsEx(progress, d);
  $('dash').innerHTML = dashHtml(stats);
  const pct = masteryPct(stats);
  $('mastery-bar').style.width = pct + '%';
  $('mastery-pct').textContent = pct + '%';

  $('path-flow').innerHTML = pathFlowSvg(pathProgress(progress, d));
  const curve = masteryCurve(progress, d);
  $('curve-note').textContent = curveNoteText(curve);
  $('spark').innerHTML = masteryCurveSvg(curve);
  $('heat').innerHTML = heatmapHtml(weakHeatmap(progress, d));

  list = filterList();
  renderQueue();
  renderStudy();
}

function renderQueue() {
  const ids = dueQueue(progress, list, QUEUE_LIMIT);
  const map = Object.fromEntries(list.map((c) => [c.id, c]));
  $('queue').innerHTML = queueListHtml(ids, map, progress);
  $('queue').querySelectorAll('.queue-item').forEach((li) => li.addEventListener('click', () => {
    const i = list.findIndex((c) => c.id === li.dataset.id);
    if (i >= 0) { pos = i; revealed = false; renderStudy(); }
  }));
}

function renderStudy() {
  const box = $('study');
  if (!list.length) {
    box.innerHTML = emptyStudyHtml();
    $('pos-note').textContent = '';
    return;
  }
  if (pos >= list.length) pos = 0;
  const c = list[pos];
  const st = stateOfCard(progress, c.id);
  box.innerHTML = cardViewHtml(c, st, revealed, deckSigned);
  revealed = false;
  box.querySelector('#flip')?.addEventListener('click', () => { revealed = true; renderStudy(); });
  box.querySelectorAll('.grade').forEach((b) => b.addEventListener('click', () => grade(c, Number(b.dataset.q))));
  box.querySelector('#skip')?.addEventListener('click', () => { pos = (pos + 1) % list.length; revealed = false; renderStudy(); });
  $('pos-note').textContent = posNoteText(pos, list.length, st);
}

function grade(c, q) {
  progress[c.id] = sm2(stateOfCard(progress, c.id), q);
  save();
  pos = (pos + 1) % list.length;
  revealed = false;
  render();
}

// ── 导入导出（纯本机）──
function exportProgress() {
  const blob = new Blob([exportPayload(progress, { source: 'learn.html', cards: currentDeck().length })],
    { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'queyi-learn-progress.json';
  a.click();
  URL.revokeObjectURL(a.href);
  $('io-note').textContent = exportNoteText(Object.keys(progress).length);
}
function importProgress(e) {
  const file = e.target.files?.[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    const r = importPayload(String(reader.result), progress);
    if (!r.ok) { $('io-note').textContent = '导入失败：' + r.error; return; }
    progress = r.progress;
    save(); render();
    $('io-note').textContent = importNoteText(r.imported, r.skipped);
  };
  reader.readAsText(file);
}
