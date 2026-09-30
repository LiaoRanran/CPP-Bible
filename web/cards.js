// 670c A3 · 卡库页：全文搜索 + 高级筛选 + 批量对比 + 证据链 + 卡关系图
//   —— 在 669c A2（四态筛选 / 证据强度排序 / 详情弹窗 / 增量渲染 / 机器卡独立区）之上**增量深化**，
//      既有能力一个不删：筛选、排序、分页、弹窗、机器卡区都还在，只是换了更强的引擎。
//
// 分层（670c「纯逻辑分离」约定）：
//   · web/js/cards_core.js —— 搜索 / 筛选 / 强度 / 证据链 / 关系图 / 对比 / 统计（纯逻辑，无 DOM，Node 里真跑测试）
//   · 本文件               —— 取数、DOM、SVG、事件；**不在这里写算法**
//
// 数据纪律（与全站一致）：
//   · 只渲染台账给的字段：web/data/cards_index.json（索引）+ web/data/cards.json（全卡）+ ig_cards_665.json（机器卡）
//   · 缺字段显示「未声明」；证据没入库就说「未入库」；sanitizer 输出没记就说「未记录」——不推断、不美化。
import { fetchJSON, fmtInt } from './app.js';
import {
  NO_STANDARD, STRENGTH_LEVELS,
  cardTitle, cardClaim, cardDomain, cardType, cardStatus, cardState,
  cardStandards, cardPrereqIds, cardEvidenceIds, isDraft, stateLabel,
  mergeCardData, indexEvidenceFromCards, evidenceStrength, cardStats, filterOptions,
  filterCards, sortCards, buildEvidenceChain, buildRelationGraph, layoutRelationGraph, buildComparison,
} from './js/cards_core.js';

const $ = (id) => document.getElementById(id);
const PAGE = 24;      // 增量渲染批大小（B6 既有口径）
const CMP_MAX = 3;    // 批量对比最多 3 张

let RAW = [];         // cards_index.json 原样（关系图 known 集合用）
let ALL = [];         // 索引 + 全卡 合并后的卡
let EVID = null;      // 证据索引（{by_evidence, by_card}）
let VIEW = [];        // 当前筛选视图
let shown = 0;
let SELECTED = [];    // 参与对比的卡 id（保序，≤ CMP_MAX）
let CHAIN_ID = '';    // 证据链当前卡
let REL_FOCUS = '';   // 关系图焦点节点

const esc = (s) => String(s ?? '').replace(/[&<>"]/g,
  (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const chip = (t, cls = '') => `<span class="chip ${cls}">${esc(t)}</span>`;
const statePill = (st) => `<span class="state-pill" data-state="${esc(st)}"><i></i>${esc(st)}</span>`;
const propsCount = (c) => (typeof c.props_count === 'number' ? c.props_count
  : (Array.isArray(c.props) ? c.props.length : 0));
const strengthOf = (c) => evidenceStrength(c, EVID);
const findCard = (id) => ALL.find((c) => c.id === id) || null;
const selValues = (id) => Array.from($(id).selectedOptions || []).map((o) => o.value);

// ── 卡片渲染（主列表）──────────────────────────────────────────────────────
function cardItem(c) {
  const s = strengthOf(c);
  const trainable = !isDraft(c);
  const checked = SELECTED.includes(c.id) ? ' checked' : '';
  const learn = trainable
    ? `<a class="chip link" href="card.html?card=${encodeURIComponent(c.id)}">去学习 →</a>`
    : '<span class="chip">draft650 · 不提供学习视图</span>';
  const claim = cardClaim(c);
  const propIds = Array.isArray(c.props) && c.props.length
    ? c.props.map((p) => (p && p.id) || String(p)).join(', ') : '（无）';
  const preIds = cardPrereqIds(c);
  return `<li class="card-item" data-id="${esc(c.id)}">
    <div class="ci-head">
      <span class="ci-id">${esc(c.id)}</span>
      ${c.status ? chip('status: ' + c.status) : chip('status: 未声明')}
      ${cardState(c) ? statePill(cardState(c)) : ''}
      ${isDraft(c) ? chip('draft650') : ''}
      <span class="spacer"></span>
      <label class="mono" style="font-size:11px;color:var(--color-text-mute)">
        <input type="checkbox" data-cmp="${esc(c.id)}"${checked}>对比</label>
    </div>
    <div class="ci-title">${esc(cardTitle(c) || '（未声明标题）')}</div>
    ${claim ? '<p class="ci-claim">' + esc(claim.length > 200 ? claim.slice(0, 200) + '…' : claim) + '</p>' : ''}
    <div class="ci-tags">
      ${c.domain ? chip('域 ' + c.domain) : ''}
      ${c.type ? chip('型 ' + c.type) : ''}
      ${c.dal ? chip('DAL ' + c.dal) : ''}
      ${cardState(c) ? chip('判决 ' + cardState(c)) : chip('判决 未声明')}
      ${c.downgraded ? chip('已降级') : ''}
      ${chip('命题 ' + fmtInt(propsCount(c)))}
      ${chip('证据 ' + fmtInt(cardEvidenceIds(c).length) + ' · ' + s.key)}
      ${chip('先修 ' + fmtInt(preIds.length))}
      ${cardStandards(c).length ? chip('标准 ' + cardStandards(c).join('/')) : chip('标准 未声明')}
    </div>
    <details>
      <summary>展开细节（台账字段；不推断）</summary>
      <div class="ci-body">
        <div>id：<span class="mono">${esc(c.id)}</span>${c.path ? ' · 文件 <span class="mono">' + esc(c.path) + '</span>' : ''}</div>
        <div>audience：${esc(c.audience ?? '未声明')} · cognitive_load：${esc(c.cognitive_load ?? '未声明')}</div>
        <div>命题 id：${esc(propIds)}</div>
        <div>证据 id：${cardEvidenceIds(c).length ? esc(cardEvidenceIds(c).join(', ')) : '（无）'}</div>
        <div>先修：${preIds.length ? preIds.map((p) => '<a href="card.html?card=' + encodeURIComponent(p) + '" class="mono">' + esc(p) + '</a>').join(' ') : '（本仓未声明）'}</div>
        <div>证据强度：<span class="mono">${esc(s.key)}</span>（在库 ${s.found}/${s.total} · confirm ${s.confirmed} · 有输出 ${s.captured} · 缺失 ${s.missing}）</div>
        <div class="btnrow">${learn}
          <button type="button" class="detail-btn" data-detail="${esc(c.id)}">详情</button>
          <button type="button" class="detail-btn" data-chain="${esc(c.id)}">证据链</button></div>
      </div>
    </details>
  </li>`;
}

function renderBatch() {
  const grid = $('grid');
  const next = VIEW.slice(shown, shown + PAGE);
  grid.insertAdjacentHTML('beforeend', next.map(cardItem).join(''));
  shown += next.length;
  $('more').hidden = shown >= VIEW.length;
  const st = cardStats(ALL, EVID);
  $('count').textContent = '匹配 ' + fmtInt(VIEW.length) + ' / 共 ' + fmtInt(ALL.length)
    + ' 张（已显示 ' + fmtInt(shown) + '）'
    + ' · 实卡 ' + fmtInt(st.real) + ' · draft650 ' + fmtInt(st.drafts)
    + ' · 证据引用 ' + fmtInt(st.evidence.total) + ' 条 / 去重 ' + fmtInt(st.evidence.distinct)
    + ' · 强度 confirmed ' + fmtInt(st.byStrength.confirmed || 0) + ' / none ' + fmtInt(st.byStrength.none || 0)
    + ' · 状态口径见 docs/discipline/provenance.md';
  syncCompareUI();
}

// ── 筛选（维度内 OR · 维度间 AND，语义在 cards_core.js 里写死并测试）──────────
function readFilter() {
  return {
    q: $('q').value,
    scope: $('f-scope').value,
    verdict_state: selValues('f-verdict'),
    strength: selValues('f-strength'),
    domain: selValues('f-domain'),
    cpp_standard: selValues('f-std'),
    status: $('f-status').value ? [$('f-status').value] : [],
    type: $('f-type').value ? [$('f-type').value] : [],
  };
}
function applyFilters() {
  VIEW = sortCards(filterCards(ALL, readFilter(), EVID), $('f-sort').value, EVID);
  $('grid').innerHTML = '';
  shown = 0;
  renderBatch();
  renderRelation();
  const q = $('q').value.trim();
  $('q-hint').textContent = q === ''
    ? '空查询 = 不约束'
    : q.split(/\s+/).filter(Boolean).length + ' 个词全部命中才显示（AND）';
}

function fillSelect(id, values, labeler = (v) => v) {
  $(id).insertAdjacentHTML('beforeend',
    values.map((v) => '<option value="' + esc(v) + '">' + esc(labeler(v)) + '</option>').join(''));
}
function fillMulti(id, values, labeler = (v) => v) {
  $(id).innerHTML = values.map((v) => '<option value="' + esc(v) + '">' + esc(labeler(v)) + '</option>').join('');
}

// ── 批量对比（2–3 张；少于 2 张或多余 3 张都不出表）─────────────────────────
function syncCompareUI() {
  const cards = SELECTED.map(findCard).filter(Boolean);
  const full = cards.length >= CMP_MAX;
  document.querySelectorAll('input[data-cmp]').forEach((box) => {
    box.checked = SELECTED.includes(box.dataset.cmp);
    box.disabled = full && !box.checked;
  });
  $('cmp-count').textContent = '已选 ' + cards.length + ' / ' + CMP_MAX;
  renderCompare(cards);
}
function renderCompare(cards) {
  const out = $('compare-out');
  const empty = $('compare-empty');
  const cmp = buildComparison(cards, EVID);
  if (!cmp.ok) {
    out.innerHTML = '';
    empty.hidden = false;
    empty.querySelector('.ce-t').textContent = cards.length === 0
      ? '还没有对比对象' : '只选了 ' + cards.length + ' 张：对比需要 2–3 张';
    $('cmp-msg').textContent = cmp.message;
    return;
  }
  empty.hidden = true;
  $('cmp-msg').textContent = '差异行 ' + cmp.summary.differ_rows + '/' + cmp.rows.length
    + ' · 四态' + (cmp.summary.same_state ? '一致' : '不同')
    + ' · 共有证据 ' + cmp.summary.shared_evidence.length + ' 条 · 最强 ' + cmp.summary.strongest;
  out.innerHTML = cmp.cols.map((col, i) => `<article class="compare-col">
      <h4>${esc(col.id)}</h4>
      <p class="section-sub">${esc(col.title)}</p>
      <dl>${cmp.rows.map((r) => '<dt>' + esc(r.label)
        + (r.differs ? ' <b title="本行取值不同">≠</b>' : '') + '</dt><dd>' + esc(r.values[i]) + '</dd>').join('')}</dl>
      <div class="btnrow">
        <button type="button" class="detail-btn" data-detail="${esc(col.id)}">详情</button>
        <button type="button" class="detail-btn" data-chain="${esc(col.id)}">证据链</button>
        <button type="button" class="detail-btn" data-cmp-drop="${esc(col.id)}">移出</button>
      </div>
    </article>`).join('');
}

// ── 证据链（.ev-tree）──────────────────────────────────────────────────────
function chainHeadHTML(n) {
  if (n.kind === 'card') {
    return '<span class="ev-node">' + esc(n.id) + '</span> <span class="ev-kind">卡 · 四态 '
      + esc(stateLabel(n.state)) + '</span> <span class="ev-kind">' + esc(n.note) + '</span>';
  }
  if (n.kind === 'evidence') {
    return '<span class="ev-node">' + esc(n.id) + '</span> <span class="ev-kind">证据 · verdict=' + esc(n.verdict)
      + ' · ' + (n.exists ? '在库' : '未入库') + ' · kind=' + esc(n.evidence_kind) + '</span>';
  }
  if (n.kind === 'file') {
    return '<span class="ev-node">' + esc(n.label) + '</span> <span class="ev-kind">证据文件'
      + (n.exists ? '' : '（缺失）') + '</span>'
      + (n.artifact_sha256 ? ' <span class="ev-kind mono">sha256 ' + esc(n.artifact_sha256.slice(0, 16)) + '…</span>' : '');
  }
  if (n.kind === 'replay') {
    return '<span class="ev-kind">复现命令（页面不执行）：</span><div class="sanitizer-out">' + esc(n.output) + '</div>';
  }
  const body = (n.output === null || n.output === undefined)
    ? '<span class="ev-kind">' + esc(n.note) + '</span>'
    : '<div class="sanitizer-out">' + esc(n.output === '' ? '（空输出 = 无告警）' : n.output) + '</div>';
  return '<span class="ev-kind">' + esc(n.tool) + ' 输出 · ' + esc(n.status) + '：</span> ' + body;
}
function chainTreeHTML(node) {
  const kids = node.children || [];
  const head = chainHeadHTML(node);
  if (!kids.length) return '<li>' + head + '</li>';
  return '<li>' + head + '<ul>' + kids.map(chainTreeHTML).join('') + '</ul></li>';
}
function fillChainSelect() {
  const sel = $('chain-card');
  sel.innerHTML = ALL.slice().sort((a, b) => a.id.localeCompare(b.id)).map((c) => {
    const n = cardEvidenceIds(c).length;
    return '<option value="' + esc(c.id) + '">' + esc(c.id) + ' · 证据 ' + n + '（' + esc(strengthOf(c).key) + '）</option>';
  }).join('');
  if (!findCard(CHAIN_ID)) {
    const preferred = VIEW.find((c) => cardEvidenceIds(c).length) || VIEW[0] || ALL[0];
    CHAIN_ID = preferred ? preferred.id : '';
  }
  sel.value = CHAIN_ID;
}
function renderChain() {
  const c = findCard(CHAIN_ID);
  const out = $('chain-out');
  if (!c) {
    out.innerHTML = '<p class="muted">没有可显示的卡。</p>';
    $('chain-sum').textContent = '';
    return;
  }
  const t = buildEvidenceChain(c, EVID);
  out.innerHTML = '<ul class="ev-tree">' + chainTreeHTML(t.root) + '</ul>';
  $('chain-sum').textContent = '本卡证据 ' + t.stats.evidence + ' 条 · 在库 ' + t.stats.found
    + ' · 缺失 ' + t.stats.missing + ' · 有输出 ' + t.stats.captured + ' · 空输出(clean) ' + t.stats.clean
    + ' · 台账未记录 ' + t.stats.unrecorded + ' · 未入库 ' + t.stats.unknown
    + (t.stats.unrecorded ? '　（「未记录」= 台账没有该字段，不等于「没有输出」）' : '');
  $('chain-card').value = CHAIN_ID;
}

// ── 卡关系图（SVG）─────────────────────────────────────────────────────────
function renderRelation() {
  const host = $('rel-graph');
  const includeRelated = $('rel-related').checked;
  const g = buildRelationGraph(VIEW, { includeRelated, known: RAW.map((c) => c.id) });
  const w = Math.max(680, Math.min(1080, g.nodes.length * 26 + 260));
  const h = Math.max(420, Math.min(700, g.nodes.length * 13 + 220));
  const lay = layoutRelationGraph(g, { width: w, height: h, padding: 76 });
  const pos = (id) => lay.positions[id] || { x: lay.cx, y: lay.cy };
  const R = 7;
  const edges = g.edges.map((e) => {
    const a = pos(e.source), b = pos(e.target);
    if (e.selfLoop) {
      const d = 'M ' + (a.x - 6) + ' ' + (a.y - 6) + ' A 11 11 0 1 1 ' + (a.x + 6) + ' ' + (a.y - 6);
      return '<path class="rel-edge" style="marker-end:none;stroke:var(--color-pass-exception)" d="' + d + '" data-kind="self"></path>';
    }
    const dx = b.x - a.x, dy = b.y - a.y, len = Math.hypot(dx, dy) || 1;
    const x1 = a.x + (dx / len) * (R + 2), y1 = a.y + (dy / len) * (R + 2);
    const x2 = b.x - (dx / len) * (R + 7), y2 = b.y - (dy / len) * (R + 7);
    const style = e.missing ? 'stroke:var(--color-fail);stroke-dasharray:4 3'
      : e.kind === 'related' ? 'marker-end:none;stroke-dasharray:2 4;opacity:.5'
        : e.outside ? 'stroke-dasharray:6 4' : '';
    return '<line class="rel-edge" x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '"'
      + (style ? ' style="' + style + '"' : '') + ' data-kind="' + esc(e.kind) + '"></line>';
  }).join('');
  const degree = new Map(g.nodes.map((n) => [n.id, 0]));
  for (const e of g.edges) {
    if (e.selfLoop) continue;
    degree.set(e.source, (degree.get(e.source) || 0) + 1);
    degree.set(e.target, (degree.get(e.target) || 0) + 1);
  }
  const showAllLabels = g.nodes.length <= 26;
  const ringOf = (n, r) => {
    if (n.missing) return '<circle cx="0" cy="0" r="' + (r + 4) + '" style="fill:none;stroke:var(--color-fail);stroke-dasharray:3 2"></circle>';
    if (n.inCycle) return '<circle cx="0" cy="0" r="' + (r + 4) + '" style="fill:none;stroke:var(--color-fail)"></circle>';
    if (n.outside) return '<circle cx="0" cy="0" r="' + (r + 4) + '" style="fill:none;stroke:var(--color-unknown);stroke-dasharray:2 3"></circle>';
    return '';
  };
  const nodes = g.nodes.map((n) => {
    const p = pos(n.id);
    const focus = n.id === REL_FOCUS;
    const r = focus ? 10 : (n.missing ? 6 : R);
    const showLabel = showAllLabels || focus || (degree.get(n.id) || 0) > 0;
    const tip = n.id + ' · ' + n.label + ' · 域 ' + (n.domain || '—') + ' · 先修出 ' + n.prereq_out + ' / 入 ' + n.prereq_in
      + (n.missing ? ' · 缺失前置' : '') + (n.outside ? ' · 视图外' : '') + (n.inCycle ? ' · 在环里' : '');
    return '<g class="rel-node' + (focus ? ' is-focus' : '') + '" data-node="' + esc(n.id) + '" role="button" tabindex="0"'
      + ' aria-label="' + esc(n.id + '（域 ' + (n.domain || '—') + '，先修入 ' + n.prereq_in + '）') + '">'
      + '<title>' + esc(tip) + '</title>'
      + '<circle cx="' + p.x + '" cy="' + p.y + '" r="' + r + '"></circle>'
      + '<g transform="translate(' + p.x + ' ' + p.y + ')">' + ringOf(n, r) + '</g>'
      + (showLabel ? '<text x="' + p.x + '" y="' + (p.y - r - 6) + '" text-anchor="middle">' + esc(n.id.replace(/^ATOM-/, '')) + '</text>' : '')
      + '</g>';
  }).join('');
  host.innerHTML = '<svg viewBox="0 0 ' + w + ' ' + h + '" width="' + w + '" height="' + h + '" role="img"'
    + ' aria-label="卡关系图：' + g.stats.nodes + ' 个节点、' + g.stats.edges + ' 条边">'
    + '<defs><marker id="rel-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6"'
    + ' orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--color-line-strong)"></path></marker></defs>'
    + '<g class="rel-edges">' + edges + '</g><g class="rel-nodes">' + nodes + '</g></svg>';
  $('rel-stats').textContent = '节点 ' + g.stats.nodes + ' · 边 ' + g.stats.edges
    + '（先修 ' + g.stats.prereq + ' / 同域相关 ' + g.stats.related + '）'
    + ' · 缺失前置 ' + g.stats.missing + (g.missing.length ? '：' + g.missing.join(', ') : '')
    + ' · 视图外 ' + g.stats.outside + ' · 自环 ' + g.stats.selfLoops + ' · 环 ' + g.stats.cycles
    + ' · 孤立 ' + g.stats.isolated + ' · 焦点 ' + (REL_FOCUS || '（无）') + '　（图随筛选实时重建）';
}

function focusNode(id) {
  REL_FOCUS = id;
  if (findCard(id)) {
    CHAIN_ID = id;
    fillChainSelect();
    renderChain();
  }
  renderRelation();
}

// ── 详情弹窗（669c A2，670c A3 起内嵌证据链）────────────────────────────────
function openModal(id) {
  const c = findCard(id);
  if (!c) return;
  const s = strengthOf(c);
  const ev = cardEvidenceIds(c).length
    ? cardEvidenceIds(c).map((e) => chip(e)).join(' ') : '<span class="muted">无</span>';
  const propIds = Array.isArray(c.props) && c.props.length
    ? c.props.map((p) => (p && p.id) || String(p)).join(', ') : '（无）';
  const preIds = cardPrereqIds(c);
  const pre = preIds.length
    ? preIds.map((p) => '<a class="chip link" href="card.html?card=' + encodeURIComponent(p) + '">' + esc(p) + '</a>').join(' ')
    : '（本仓未声明）';
  const t = buildEvidenceChain(c, EVID);
  $('modal-body').innerHTML = `
    <h2 id="modal-title">${esc(c.id)}</h2>
    <p style="font-size:15px;color:var(--color-text)">${esc(cardTitle(c) || '')}</p>
    ${c.claim ? '<p class="ci-claim">' + esc(c.claim) + '</p>' : ''}
    <dl class="modal-kv">
      <dt>状态 / 四态</dt><dd>${esc(cardStatus(c) || '未声明')} ${cardState(c) ? statePill(cardState(c)) : '<span class="muted">未声明</span>'}</dd>
      <dt>域 / 类型</dt><dd>${esc(cardDomain(c) || '—')} / ${esc(cardType(c) || '—')}</dd>
      <dt>DAL / 受众</dt><dd>${esc(c.dal || '—')} / ${esc(c.audience || '未声明')}（认知负荷 ${esc(c.cognitive_load || '未声明')}）</dd>
      <dt>标准</dt><dd>${esc(cardStandards(c).join(', ') || '未声明')}</dd>
      <dt>命题 id</dt><dd>${esc(propIds)}</dd>
      <dt>证据强度</dt><dd>${esc(s.key)}（在库 ${s.found}/${s.total} · confirm ${s.confirmed} · 有输出 ${s.captured}）</dd>
    </dl>
    <div class="ci-tags">证据：${ev}</div>
    <div class="ci-tags">先修：${pre}</div>
    <h3 class="section-title" style="margin-top:var(--space-3)">证据链（${fmtInt(t.stats.evidence)} 条）</h3>
    <ul class="ev-tree">${chainTreeHTML(t.root)}</ul>
    ${c.verdict_reasons && c.verdict_reasons.length
      ? '<p class="modal-note">四态理由：' + esc(c.verdict_reasons.join('；')) + '</p>' : ''}
    <p class="modal-note">四态判决理由见 <a href="verdicts.html">判决与数字</a>；
      每条证据（EV-…）带版本串 + 命令 + 输入哈希 + 期望输出，可在 <a href="verify.html">验哈希</a> 复现 ——
      前端只渲染，不替它背书。</p>
    <div class="btnrow"><a class="chip link" href="card.html?card=${encodeURIComponent(c.id)}">打开卡详情页 →</a>
      <button type="button" class="detail-btn" data-chain="${esc(c.id)}">看完整证据链</button></div>`;
  $('modal').hidden = false;
  $('modal-close').focus();
}
function closeModal() { $('modal').hidden = true; }

// ── 机器卡（独立区，不与教学台账混）────────────────────────────────────────
async function renderIg() {
  const grid = $('ig-grid');
  try {
    const D = await fetchJSON('data/ig_cards_665.json');
    // 只拼台账真给了的字段（缺的字段不显示 "undefined" —— 页面不替数据补话）
    const head = [D.total + ' 张', D.status].filter(Boolean).join(' · ');
    const bits = [head];
    if (D.agree_with_664 !== undefined) bits.push('与 664 记录一致 ' + D.agree_with_664);
    if (D.recheck_cmd) bits.push('复算：' + D.recheck_cmd);
    if (D.source) bits.push('来源：' + D.source);
    if (D.note) bits.push(D.note);
    $('ig-note').textContent = bits.join('　·　');
    grid.innerHTML = (D.cards || []).map((c) => `<li class="card-item">
      <div class="ci-head"><span class="ci-id">${esc(c.id)}</span>
        <span class="chip">${esc(c.verdict)}</span><span class="chip">四态 ${esc(c.four_state)}</span></div>
      <div class="ci-title">${esc(c.assertion || '')}</div>
      <div class="ci-body"><div>detector：<span class="mono">${esc(c.detector)}</span></div>
        <div>签名：<span class="mono">${esc((c.signature || '').slice(0, 32))}…</span></div>
        <div>反例：${esc((c.counterexample || '').slice(0, 160))}</div></div>
      <div class="ci-tags"><span class="chip">needs_review: ${esc(String(c.needs_review))}</span>
        <span class="chip">无人签 · 不进教学台账</span></div>
    </li>`).join('');
  } catch (e) {
    $('ig-note').textContent = '机器卡不可用：' + e.message;
  }
}

// ── 事件 ───────────────────────────────────────────────────────────────────
function bindEvents() {
  $('q').addEventListener('input', applyFilters);
  for (const id of ['f-status', 'f-type', 'f-scope', 'f-sort']) $(id).addEventListener('change', applyFilters);
  for (const id of ['f-verdict', 'f-strength', 'f-domain', 'f-std']) $(id).addEventListener('change', applyFilters);
  $('rel-related').addEventListener('change', renderRelation);
  $('more').addEventListener('click', renderBatch);
  $('reset').addEventListener('click', () => {
    $('q').value = '';
    for (const id of ['f-verdict', 'f-strength', 'f-domain', 'f-std']) {
      Array.from($(id).options).forEach((o) => { o.selected = false; });
    }
    $('f-status').value = ''; $('f-type').value = '';
    $('f-scope').value = 'real'; $('f-sort').value = 'default';
    applyFilters();
  });

  // 主列表：对比勾选 + 详情 / 证据链按钮
  $('grid').addEventListener('change', (e) => {
    const box = e.target.closest('input[data-cmp]');
    if (!box) return;
    const id = box.dataset.cmp;
    if (box.checked) {
      if (SELECTED.length >= CMP_MAX) {
        box.checked = false;
        $('cmp-msg').textContent = '最多对比 ' + CMP_MAX + ' 张：先移出一张再勾。';
        return;
      }
      if (!SELECTED.includes(id)) SELECTED.push(id);
    } else {
      SELECTED = SELECTED.filter((x) => x !== id);
    }
    syncCompareUI();
  });
  $('grid').addEventListener('click', (e) => {
    const d = e.target.closest('[data-detail]');
    if (d) { openModal(d.dataset.detail); return; }
    const ch = e.target.closest('[data-chain]');
    if (ch) { CHAIN_ID = ch.dataset.chain; fillChainSelect(); renderChain(); $('chain-out').scrollIntoView({ block: 'center' }); }
  });

  // 对比区
  $('cmp-run').addEventListener('click', () => renderCompare(SELECTED.map(findCard).filter(Boolean)));
  $('cmp-clear').addEventListener('click', () => { SELECTED = []; syncCompareUI(); });
  $('compare-out').addEventListener('click', (e) => {
    const d = e.target.closest('[data-detail]');
    if (d) { openModal(d.dataset.detail); return; }
    const ch = e.target.closest('[data-chain]');
    if (ch) { CHAIN_ID = ch.dataset.chain; fillChainSelect(); renderChain(); return; }
    const dr = e.target.closest('[data-cmp-drop]');
    if (dr) { SELECTED = SELECTED.filter((x) => x !== dr.dataset.cmpDrop); syncCompareUI(); }
  });
  $('chain-card').addEventListener('change', (e) => { CHAIN_ID = e.target.value; renderChain(); });

  // 关系图：点/回车节点 ⇒ 高亮 + 跳到它的证据链
  $('rel-graph').addEventListener('click', (e) => {
    const g = e.target.closest('[data-node]');
    if (g) focusNode(g.dataset.node);
  });
  $('rel-graph').addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const g = e.target.closest('[data-node]');
    if (g) { e.preventDefault(); focusNode(g.dataset.node); }
  });

  // 弹窗
  $('modal-close').addEventListener('click', closeModal);
  $('modal').querySelector('[data-close]').addEventListener('click', closeModal);
  $('modal-body').addEventListener('click', (e) => {
    const ch = e.target.closest('[data-chain]');
    if (ch) { closeModal(); CHAIN_ID = ch.dataset.chain; fillChainSelect(); renderChain(); $('chain-out').scrollIntoView({ block: 'center' }); }
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
    if (e.key === '/' && !/^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement && document.activeElement.tagName || '')) {
      e.preventDefault(); $('q').focus();
    }
  });

  // 增量渲染：滚到底自动续一批（B6）；没有 IntersectionObserver 时靠按钮
  if ('IntersectionObserver' in window) {
    new IntersectionObserver((ents) => {
      if (ents.some((x) => x.isIntersecting) && shown < VIEW.length) renderBatch();
    }, { rootMargin: '400px' }).observe($('more-wrap'));
  }
}

// ── 启动 ───────────────────────────────────────────────────────────────────
(async function main() {
  renderIg();   // 与卡库并行，互不阻塞
  try {
    const D = await fetchJSON('data/cards_index.json');
    RAW = D.cards || [];
    $('data-stamp').textContent = '索引 ' + fmtInt(RAW.length) + ' 张 · 生成 ' + (D.generated_at || '—');
  } catch (e) {
    $('count').textContent = '加载 data/cards_index.json 失败：' + e.message
      + '（生成命令 python tools/web_data_653.py；请用本地静态服务器打开）';
    return;
  }
  let note = '';
  try {
    const F = await fetchJSON('data/cards.json');
    EVID = indexEvidenceFromCards(Object.values(F.cards || {}));
    ALL = mergeCardData(RAW, F.cards);
    note = '全卡已接入：claim / 边界标准 / 命题数组 / 证据明细（' + fmtInt(EVID.count) + ' 条证据索引）';
  } catch (e) {
    EVID = null;
    ALL = RAW.map((c) => ({ ...c, props: [], props_count: typeof c.props === 'number' ? c.props : 0, cpp_standard: [] }));
    note = '全卡 data/cards.json 不可用（' + e.message + '）：标准筛选 / 证据链 / 边界对比退化，其余照常';
  }
  const opts = filterOptions(ALL, EVID);
  fillSelect('f-status', opts.status, (v) => 'status: ' + v);
  fillSelect('f-type', opts.type, (v) => '型: ' + v);
  fillMulti('f-verdict', opts.verdict_state, (v) => stateLabel(v));
  fillMulti('f-strength', opts.strength, (v) => {
    const lv = STRENGTH_LEVELS.find((x) => x.key === v);
    return lv ? v + ' · ' + lv.label : v;
  });
  fillMulti('f-domain', opts.domain, (v) => '域 ' + v);
  fillMulti('f-std', opts.cpp_standard, (v) => (v === NO_STANDARD ? v : '标准 ' + v));
  applyFilters();
  fillChainSelect();
  renderChain();
  bindEvents();
  $('filter-note').insertAdjacentHTML('beforeend', '　<b>' + esc(note) + '</b>');

  // 自动化探针（tools/web_smoke_* 用；浏览器里没有副作用）
  window.__cards_ready = true;
  window.__cards_hooks = {
    viewIds: () => VIEW.map((c) => c.id),
    stats: () => cardStats(ALL, EVID),
    graph: () => buildRelationGraph(VIEW, {
      includeRelated: $('rel-related').checked, known: RAW.map((c) => c.id),
    }).stats,
    cmp: () => SELECTED.slice(),
    compare: () => buildComparison(SELECTED.map(findCard).filter(Boolean), EVID),
    chain: () => buildEvidenceChain(findCard(CHAIN_ID) || ALL[0], EVID).stats,
    focus: (id) => focusNode(id),
  };
})();
