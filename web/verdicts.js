// 667 阶段2 · 判决页渲染层（DOM）。纯逻辑在 `verdicts_core.js`（可被 Node 真求值）。
//
// 纪律：① **只渲染，不写死** —— 数字全来自 web/data/verdicts_667.json；
//      ② 拿不到就显示"不可用"并说明生成命令，绝不猜（docs/discipline/error_handling.md）；
//      ③ 动效尊重 `prefers-reduced-motion`；④ 暴露 `window.__verdicts_hooks` 给 jsdom 冒烟。
//
// 670c A4 增量（本节以下全是**追加**，667 的老渲染路径一行没动）：
//   · 判决历史时间线        .timeline / .tl-item[data-state]（按 when 排，不是按落盘 seq）
//   · 四态分布变化图        内联 SVG 堆叠柱 + pass 占比折线（.chart svg .seg / .line-path）
//   · 漂移幅度条            .drift-bar / .drift-track / .drift-fill（中线为零，正右负左）
//   · 声明 vs 现算对比表    .diff-table，超容差行 .is-mismatch 高亮
//   纯逻辑全部在 ./js/verdicts_core.js，可用 `cd web && node tests/verdicts.test.mjs` 真跑。
import { fetchJSON } from './app.js';
import { sortRows, filterRows, dashCells, fmtNum, KIND_LABEL } from './verdicts_core.js';
// 670c A4 深化逻辑统一从 js/verdicts_core.js 进（它是 670c 新逻辑 + 对上面 667 老逻辑的
// export *）。老 import 保持原样 ⇒ 老渲染路径**一行没改**，行为零变更。
import {
  parseVerdicts, buildTimeline, fourStateSeries, parseDrift, driftBars, buildCompareModel,
  layoutStacked, linePath, stateAttr, FOUR_STATES, STATE_VAR, STATE_ZH, BUCKETS,
} from './js/verdicts_core.js';

const $ = (id) => document.getElementById(id);
const $$ = (sel, root) => [...((root || document).querySelectorAll(sel))];
const REDUCED = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

/** 数字滚动（只做视觉；尊重 reduced-motion；NaN 直接写 —）。 */
function countUp(el, target, digits = 0) {
  if (!el) return;
  const put = (v) => { el.firstChild ? (el.firstChild.nodeValue = v) : (el.textContent = v); };
  if (REDUCED || !isFinite(Number(target))) { put(fmtNum(target, digits)); return; }
  const t0 = performance.now(), dur = 900;
  const step = (now) => {
    const k = Math.min(1, (now - t0) / dur);
    const v = Number(target) * (1 - Math.pow(1 - k, 3));
    put(fmtNum(Number.isInteger(Number(target)) && !digits ? Math.round(v) : v, digits));
    if (k < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

let DATA = null;
const view = { q: '', state: 'all', source: 'all', key: 'when', dir: 'desc' };

/* ── 仪表盘 ─────────────────────────────────────────────────── */
function renderDash() {
  const box = $('dash');
  if (!box) return;
  const cells = dashCells(DATA.dashboard, DATA.verdicts_total);
  box.innerHTML = '';
  for (const c of cells) {
    const cell = document.createElement('div');
    cell.className = 'cell glass glass-tint';
    if (c.bad) cell.dataset.bad = '1';
    if (c.warn) cell.dataset.warn = '1';
    const num = document.createElement('div');
    num.className = 'd-num';
    num.appendChild(document.createTextNode('0'));
    if (c.unit) {
      const u = document.createElement('span');
      u.className = 'u'; u.textContent = c.unit; num.appendChild(u);
    }
    const cap = document.createElement('div');
    cap.className = 'd-cap'; cap.textContent = c.cap;
    const sub = document.createElement('div');
    sub.className = 'd-sub'; sub.textContent = c.sub || '';
    cell.append(num, cap, sub);
    if (c.warnLine) {
      const w = document.createElement('div');
      w.className = 'warn-line'; w.textContent = c.warnLine;
      cell.appendChild(w);
    }
    box.appendChild(cell);
    countUp(num, c.num, c.digits || 0);
  }
  const note = $('dash-note');
  if (note) {
    note.textContent = `生成于 ${DATA.generated_at || '—'} · 数据源：`
      + (DATA.dashboard?.holdout?.source || '—') + ' / ' + (DATA.dashboard?.external?.source || '—')
      + (DATA.unavailable?.length ? `　⚠ 不可用项：${DATA.unavailable.join('；')}` : '');
  }
}

function renderDrift() {
  const box = $('drift-box');
  if (!box) return;
  const rows = DATA.drift || [];
  box.innerHTML = rows.length
    ? `<div class="card glass" style="margin-top:var(--space-2)">
         <h3>漂移登记（${rows.length} 项 · 机器不自行裁决）</h3>
         <ul class="prose">${rows.map((d) => `<li><span class="kind-tag" data-kind="drift">漂移</span>
            <span class="mono">${d.field}</span>：落盘 <b>${d.stored}</b> → 现算 <b>${d.fresh}</b>
            <div class="note-faint">${d.note}</div></li>`).join('')}</ul>
       </div>`
    : '';
}

/* ── 判决历史表 ─────────────────────────────────────────────── */
function statePill(state, label) {
  return `<span class="state-pill" data-state="${state}"><i></i>${label || state}</span>`;
}

function renderTable() {
  const body = $('vt-body');
  const empty = $('vt-empty');
  const wrap = $('vt-wrap');
  if (!body) return;
  const rows = sortRows(filterRows(DATA.verdicts || [], view), view.key, view.dir);
  body.innerHTML = rows.map((r) => `
    <tr>
      <td class="w-when">${r.when || '—'}</td>
      <td>${r.source_label || r.source || '—'}</td>
      <td class="w-id">${r.id}</td>
      <td class="w-state">${statePill(r.state, r.state_label)}</td>
      <td><span class="mono">${r.detector || '—'}</span> <span class="note-faint">/ 期望 ${r.expect || '—'}</span></td>
      <td class="w-detail">${r.detail ? mdBold(esc(r.detail)) : '<span class="note-faint">（无说明）</span>'}</td>
    </tr>`).join('');
  const n = rows.length, total = (DATA.verdicts || []).length;
  const cnt = $('count');
  if (cnt) cnt.textContent = `显示 ${n} / ${total} 条（排序 ${view.key} ${view.dir === 'desc' ? '↓' : '↑'}）`;
  const isEmpty = n === 0;
  if (wrap) wrap.style.display = isEmpty ? 'none' : '';
  if (empty) {
    empty.innerHTML = isEmpty ? `<div class="empty">
      <b>没有匹配的判决记录</b>
      <p>当前筛选（搜索「${view.q}」/ 状态 ${view.state} / 来源 ${view.source}）下为空。
      这不是"没有数据"，而是<b>筛选把 ${total} 条都排除了</b>。</p>
      <p>下一步：点「重置筛选」，或把状态改成「全部」。
      <span class="kbd">python tools/web_verdicts_667.py --json</span> 可看全集。</p></div>` : '';
  }
  // 表头排序标记（无障碍：aria-sort）
  document.querySelectorAll('#vt thead .th-btn').forEach((b) => {
    if (b.dataset.key === view.key) {
      b.setAttribute('aria-sort', view.dir === 'asc' ? 'ascending' : 'descending');
      const a = b.querySelector('.arrow');
      if (a) a.textContent = view.dir === 'asc' ? '▲' : '▼';
    } else {
      b.removeAttribute('aria-sort');
      const a = b.querySelector('.arrow');
      if (a) a.textContent = '';
    }
  });
}

function renderCompare() {
  const body = $('ct-body');
  const empty = $('ct-empty');
  const wrap = $('ct-wrap');
  if (!body) return;
  const rows = DATA.compare || [];
  body.innerHTML = rows.map((r) => `
    <tr>
      <td class="w-id">${r.metric}</td>
      <td class="cmp-left">${r.left}</td>
      <td class="cmp-right">${r.right}</td>
      <td><span class="kind-tag" data-kind="${r.kind}">${KIND_LABEL[r.kind] || r.kind}</span></td>
      <td class="w-detail">${r.note}</td>
    </tr>`).join('');
  const isEmpty = rows.length === 0;
  if (wrap) wrap.style.display = isEmpty ? 'none' : '';
  if (empty) {
    empty.innerHTML = isEmpty ? `<div class="empty">
      <b>没有可对比的项</b>
      <p>对比表由 <span class="kbd">tools/web_verdicts_667.py</span> 现算生成。为空说明
      <span class="kbd">web/data/verdicts_667.json</span> 未生成或数据源缺失。</p>
      <p>下一步：<span class="kbd">python tools/web_verdicts_667.py --write</span></p></div>` : '';
  }
}

function renderExcluded() {
  const ul = $('excluded');
  if (!ul) return;
  ul.innerHTML = (DATA.excluded || []).map((t) => `<li>${t}</li>`).join('')
    || '<li>（无）</li>';
}

/* ══════════════════════════════════════════════════════════════════
   670c A4 · 时间线 / 四态分布 / 漂移幅度 / 声明-vs-现算对比表
   纪律：① 数字全来自 core 的返回值，这里只拼 DOM；
        ② 缺数据 ⇒ .chart-empty 占位 + 写明生成命令，不画假图；
        ③ 颜色只走 var(--color-*)，不写死 hex。
   ══════════════════════════════════════════════════════════════════ */

const A4 = { tlDir: 'asc', tlState: 'all', bucket: 'date', size: 5, diffOnly: false };

/** 数据源清单。baseline 在**仓库根** data/：静态站以 web/ 为根时 'data/baseline.json' 取不到，
 *  再从 '..' 试一次（把服务起在仓库根时这条会命中）。两个都失败 ⇒ 该节优雅降级。 */
const SOURCES = [
  { key: 'verdicts', urls: ['data/verdicts_667.json'], required: true },
  { key: 'status', urls: ['data/status.json'], required: false },
  { key: 'metrics', urls: ['data/metrics_666.json'], required: false },
  { key: 'baseline', urls: ['data/baseline.json', '../data/baseline.json'], required: false },
];

let PARSED = null;
let DRIFT = null;
let BASE_DRIFT = null;
let MODEL = null;
const LOADED = {};

function esc(v) {
  if (v === null || v === undefined) return '';
  return String(v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

/** 仓内 JSON 的 prose 约定是 **粗体**：**先 esc 再变 <b>**（顺序反了就是注入）。
 *  不用正则：避免生成器里的转义地狱，行为也更直观。 */
function mdBold(escaped) {
  const parts = String(escaped).split('**');
  if (parts.length < 3) return String(escaped);
  let out = '';
  for (let i = 0; i < parts.length; i++) out += (i % 2 === 1) ? '<b>' + parts[i] + '</b>' : parts[i];
  return out;
}

/** title="…" 这类属性里不能有标签 ⇒ 只把标记去掉。 */
function plainMd(s) { return String(s).split('**').join(''); }

/** 取第一个能拿到的 URL；全失败返回 errors 清单（不抛）。 */
async function fetchFirst(urls) {
  const errors = [];
  for (const u of urls) {
    try { return { url: u, json: await fetchJSON(u), errors: errors }; }
    catch (e) { errors.push(u + ' → ' + ((e && e.message) || e)); }
  }
  return { url: null, json: null, errors: errors };
}

/** 统一占位块（缺数据时用）：说清缺什么、怎么补。 */
function placeholder(title, lines) {
  return '<div class="chart-empty"><span class="ce-t">' + esc(title) + '</span>'
    + (lines || []).map(function (t) { return '<p class="section-sub">' + mdBold(esc(t)) + '</p>'; }).join('')
    + '</div>';
}

/* ── 1 · 判决历史时间线 ─────────────────────────────────────── */
function renderTimeline() {
  const ol = $('tl');
  const note = $('tl-note');
  const empty = $('tl-empty');
  if (!ol) return;
  if (!PARSED || !PARSED.total) {
    ol.innerHTML = '';
    if (empty) {
      empty.innerHTML = placeholder('时间线暂不可用', [
        '没有可解析的判决记录（verdicts 为空 / 数据源未生成）。',
        '生成命令：python tools/web_verdicts_667.py --write',
      ]);
    }
    if (note) note.textContent = '';
    return;
  }
  if (empty) empty.innerHTML = '';
  const tl = buildTimeline(PARSED, { dir: A4.tlDir });
  const rows = A4.tlState === 'all' ? tl.items : tl.items.filter(function (r) { return r.state === A4.tlState; });
  ol.innerHTML = rows.map(function (r) {
    return '<li class="tl-item" data-state="' + stateAttr(r.state) + '">'
      + '<div class="tl-when">' + esc(r.when || '无日期') + ' · 时序 #' + (r.chrono + 1) + ' · 批次 ' + esc(r.batch) + ' · seq ' + esc(r.seq) + '</div>'
      + '<div class="tl-what">'
      + '<span class="mono">' + esc(r.id) + '</span> '
      + '<span class="state-pill" data-state="' + stateAttr(r.state, 'pill') + '"><i></i>' + esc(r.state_label) + '</span> '
      + '<span class="dim">' + esc(r.source_label) + '</span> · ' + mdBold(esc(r.detail || '（无说明）'))
      + '</div></li>';
  }).join('');
  if (note) {
    const span = tl.items.length ? (tl.items[0].when + ' → ' + tl.items[tl.items.length - 1].when) : '—';
    note.textContent = '显示 ' + rows.length + ' / ' + tl.total + ' 条 · 跨度 ' + span
      + ' · 四态切换 ' + tl.transitions + ' 次'
      + (tl.reordered ? ' · 落盘顺序 ≠ 时间顺序（本视图已按 when 重排）' : '')
      + (tl.undated ? ' · ⚠ ' + tl.undated + ' 条无日期，排在最后' : '');
  }
}

/* ── 2 · 四态分布变化图（内联 SVG，纯几何来自 core）────────────── */
function renderSeries() {
  const box = $('fs-chart');
  const legend = $('fs-legend');
  const notes = $('fs-notes');
  const sub = $('fs-sub');
  if (!box) return;
  const meta = BUCKETS.filter(function (b) { return b.key === A4.bucket; })[0] || BUCKETS[0];
  const series = PARSED ? fourStateSeries(PARSED, { bucket: A4.bucket, size: A4.size }) : { buckets: [], total: 0, states: FOUR_STATES };
  if (!series.buckets.length) {
    box.innerHTML = placeholder('四态分布图暂不可用', [
      '没有可分桶的判决记录（verdicts 为空）。这不是"四态都是 0"，是**没有数据**。',
      '生成命令：python tools/web_verdicts_667.py --write',
    ]);
    if (legend) legend.innerHTML = '';
    if (notes) notes.innerHTML = '';
    if (sub) sub.textContent = '';
    return;
  }
  const w = Math.max(360, box.clientWidth || 720);
  const geo = layoutStacked(series, { width: w, height: 220 });
  const right = geo.width - geo.pad.r;
  const baseY = geo.pad.t + geo.plotH;
  const parts = [];
  parts.push('<svg viewBox="0 0 ' + geo.width + ' ' + geo.height + '" width="100%" height="' + geo.height
    + '" role="img" aria-label="四态随' + esc(meta.label) + '的分布变化">');
  parts.push('<title>四态分布变化（' + esc(meta.label) + ' · 共 ' + series.total + ' 条）</title>');
  geo.grid.forEach(function (g) {
    parts.push('<line class="grid-line" x1="' + geo.pad.l + '" y1="' + g.y.toFixed(1) + '" x2="' + right + '" y2="' + g.y.toFixed(1) + '"></line>');
    parts.push('<text class="tick-label" x="' + (geo.pad.l - 6) + '" y="' + (g.y + 4).toFixed(1) + '" text-anchor="end">' + esc(g.label) + '</text>');
  });
  parts.push('<line class="axis-line" x1="' + geo.pad.l + '" y1="' + baseY + '" x2="' + right + '" y2="' + baseY + '"></line>');
  parts.push('<text class="axis-title" x="' + geo.pad.l + '" y="' + (geo.pad.t - 2) + '">条数（峰值 ' + series.max + '）</text>');
  geo.bands.forEach(function (b) {
    b.segs.forEach(function (s) {
      if (s.h <= 0) return;
      parts.push('<rect class="seg" x="' + s.x.toFixed(1) + '" y="' + s.y.toFixed(1) + '" width="' + s.w.toFixed(1)
        + '" height="' + s.h.toFixed(1) + '" fill="' + STATE_VAR[s.state] + '" data-state="' + s.state + '" data-bucket="' + esc(b.key) + '">'
        + '<title>' + esc(b.label) + ' · ' + esc(s.state) + ' ' + s.value + ' 条（' + fmtNum(s.pct, 1) + '%）</title></rect>');
    });
  });
  const d = linePath(geo.line);
  if (d) parts.push('<path class="line-path" d="' + d + '" stroke="var(--color-accent)"></path>');
  geo.line.forEach(function (p) {
    if (p.y === null) return;
    parts.push('<circle class="line-dot" cx="' + p.x.toFixed(1) + '" cy="' + p.y.toFixed(1) + '" r="3.5" fill="var(--color-accent)">'
      + '<title>' + esc(p.key) + ' · pass 占比 ' + fmtNum(p.pct, 1) + '%</title></circle>');
  });
  geo.x_ticks.forEach(function (t) {
    parts.push('<text class="tick-label" x="' + t.x.toFixed(1) + '" y="' + (baseY + 14) + '" text-anchor="middle">' + esc(t.label) + '</text>');
  });
  parts.push('</svg>');
  box.innerHTML = parts.join('');

  if (legend) {
    legend.innerHTML = series.states.map(function (s) {
      return '<div class="lg-item"><span class="lg-dot" style="background:' + STATE_VAR[s] + '"></span>'
        + esc(s) + ' <span class="muted">' + esc(STATE_ZH[s]) + ' ' + series.totals[s] + ' 条</span></div>';
    }).join('') + '<div class="lg-item"><span class="lg-dot" style="background:var(--color-accent)"></span>折线 = 该桶 pass 占比</div>';
  }
  if (notes) {
    notes.innerHTML = series.buckets.map(function (b) {
      return '<li><span class="mono">' + esc(b.label) + '</span>'
        + '<span>' + b.total + ' 条 · ' + FOUR_STATES.map(function (s) {
          return esc(s) + ' ' + b.counts[s];
        }).join(' / ') + (b.from ? '（' + esc(b.from) + ' → ' + esc(b.to) + '）' : '') + '</span></li>';
    }).join('');
  }
  if (sub) {
    sub.textContent = meta.label + ' · ' + meta.sub + ' · 共 ' + series.buckets.length + ' 桶 / ' + series.total + ' 条 · 主导 ' + series.dominant;
  }
}

/* ── 3 · 漂移幅度条 ─────────────────────────────────────────── */
/** 把三张登记表 + 真不一致行合成一份「有数值的漂移」清单（按 field 去重，先到先得）。 */
function driftFeed() {
  const out = [];
  const seen = {};
  const add = function (d) {
    if (!d || !d.field || seen[d.field]) return;
    seen[d.field] = 1;
    out.push(d);
  };
  (DRIFT && DRIFT.items ? DRIFT.items : []).forEach(function (d) { if (d.numeric) add(d); });
  (BASE_DRIFT && BASE_DRIFT.items ? BASE_DRIFT.items : []).forEach(function (d) { if (d.numeric) add(d); });
  (MODEL && MODEL.rows ? MODEL.rows : []).forEach(function (r) {
    if (r.numeric && r.isMismatch) {
      add({
        field: r.label, label: r.label, kind: 'mismatch',
        stored: r.declared, fresh: r.computed, unit: r.unit,
        note: '声明 ' + r.declared_text + ' → 现算 ' + r.computed_text,
        source: r.declared_source + ' ↔ ' + r.computed_source,
        stored_raw: r.declared, fresh_raw: r.computed,
      });
    }
  });
  return out;
}

function renderDriftBars() {
  const box = $('drift-bars');
  const note = $('drift-note');
  if (!box) return;
  const feed = driftFeed();
  const res = driftBars(feed);
  if (!res.total) {
    box.innerHTML = placeholder('暂无可登记的漂移', [
      'verdicts_667.json 的 drift / compare 与 data/baseline.json 都没给出可比的数值。',
      '注意：这**不等于**"没有漂移"，只等于"没有登记"。',
    ]);
  } else {
    const head = '<div class="row-between">'
      + '<h3 class="section-title">漂移幅度（有数值 ' + res.numeric + ' 项 / 仅文字 ' + res.text_only + ' 项）</h3>'
      + '<span class="section-sub">量程 0 – ±' + fmtNum(res.scale, 2) + '　正向 ' + res.positive + ' · 负向 ' + res.negative + ' · 零漂移 ' + res.flat_count + '</span></div>';
    const rows = res.bars.map(function (b) {
      const fill = b.numeric
        ? '<i class="drift-fill ' + b.cls + '" style="' + b.style + '"></i>'
        : '';
      const val = b.numeric
        ? '<span class="drift-val">' + esc(b.val_text) + ' <span class="muted">(' + esc(b.rel_text) + ')</span></span>'
        : '<span class="drift-val dim">无数值（仅登记）</span>';
      const tip = b.numeric
        ? esc(plainMd(b.field)) + '：' + esc(b.stored_text) + ' → ' + esc(b.fresh_text) + '（Δ ' + esc(b.val_text) + '）'
        : esc(plainMd(b.field)) + '：' + esc(plainMd(b.note || b.text || '仅文字登记'));
      return '<div class="drift-bar" data-kind="' + esc(b.kind) + '" data-numeric="' + (b.numeric ? '1' : '0') + '">'
        + '<span class="mono" title="' + tip + '">' + esc(b.field) + '</span>'
        + '<div class="drift-track" title="' + tip + '">' + fill + '</div>'
        + val + '</div>';
    }).join('');
    box.innerHTML = head + rows;
  }
  if (note) {
    const bits = [];
    bits.push('登记来源：' + ((DRIFT && DRIFT.total ? 'verdicts_667.json 的 compare/drift（' + DRIFT.total + ' 项）' : '无') ));
    if (BASE_DRIFT && BASE_DRIFT.total) bits.push('data/baseline.json 的 tolerated_discrepancies（' + BASE_DRIFT.total + ' 项）');
    else bits.push('data/baseline.json **未加载**（它在仓库根；静态站以 web/ 为根时 HTTP 404）⇒ 图谱节点等登记项缺席');
    if (MODEL) bits.push('真不一致行 ' + MODEL.mismatches + ' 条');
    if (LOADED.baseline) bits.push('baseline 取自 ' + LOADED.baseline.url);
    note.innerHTML = mdBold(esc(bits.join(' · ')));
  }
}

/* ── 4 · 数据对比表：声明值 vs 现算值 ───────────────────────── */
function renderDiff() {
  const body = $('diff-body');
  const empty = $('diff-empty');
  const sub = $('diff-sub');
  const wrap = document.getElementById('diff') && document.getElementById('diff').parentNode;
  if (!body) return;
  if (!MODEL || !MODEL.total) {
    body.innerHTML = '';
    if (wrap) wrap.style.display = 'none';
    if (empty) {
      empty.innerHTML = placeholder('对比表暂不可用', [
        '没有任何一侧的数据源可用（verdicts / status / metrics / baseline 全缺）。',
        '生成命令：python tools/web_verdicts_667.py --write',
      ]);
    }
    if (sub) sub.textContent = '';
    return;
  }
  if (empty) empty.innerHTML = '';
  if (wrap) wrap.style.display = '';
  const rows = A4.diffOnly ? MODEL.rows.filter(function (r) { return r.isMismatch; }) : MODEL.rows;
  body.innerHTML = rows.map(function (r) {
    const tag = r.isMismatch ? 'drift' : (r.kind === 'exact' ? 'ok' : r.kind);
    const src = (r.declared_source || '—') + ' ↔ ' + (r.computed_source || '—');
    return '<tr class="' + r.rowClass + '" data-key="' + esc(r.key) + '">'
      + '<td><b>' + esc(r.label) + '</b>' + (r.note ? '<div class="dim">' + mdBold(esc(r.note)) + '</div>' : '') + '</td>'
      + '<td>' + esc(r.declared_text) + '</td>'
      + '<td>' + esc(r.computed_text) + '</td>'
      + '<td class="diff-delta">' + esc(r.diff_text) + (r.numeric ? ' <span class="muted">(' + esc(r.rel_text) + ')</span>' : '') + '</td>'
      + '<td>' + esc(r.limit_text) + '</td>'
      + '<td><span class="kind-tag" data-kind="' + esc(tag) + '">' + esc(r.verdict_text) + '</span></td>'
      + '<td class="dim">' + esc(src) + '</td></tr>';
  }).join('');
  if (sub) {
    sub.textContent = '显示 ' + rows.length + ' / ' + MODEL.total + ' 行 · 不一致 ' + MODEL.mismatches
      + ' · 一致 ' + MODEL.matches + ' · 口径差 ' + MODEL.caliber + ' · 冻结 ' + MODEL.frozen + ' · 缺口 ' + MODEL.partial
      + (MODEL.mismatches && !A4.diffOnly ? '　⚠ 有 ' + MODEL.mismatches + ' 行超容差，见高亮行' : '');
  }
}

function fillA4Controls() {
  const bs = $('fs-bucket');
  if (bs) {
    bs.innerHTML = BUCKETS.map(function (b) { return '<option value="' + b.key + '">' + esc(b.label) + '</option>'; }).join('');
    bs.value = A4.bucket;
  }
  const st = $('tl-state');
  if (st) {
    st.innerHTML = '<option value="all">全部</option>'
      + FOUR_STATES.map(function (s) { return '<option value="' + s + '">' + s + '（' + esc(STATE_ZH[s]) + '）</option>'; }).join('');
  }
}

function wireA4() {
  const dir = $('tl-dir');
  if (dir) dir.addEventListener('change', function () { A4.tlDir = dir.value; renderTimeline(); });
  const st = $('tl-state');
  if (st) st.addEventListener('change', function () { A4.tlState = st.value; renderTimeline(); });
  const bs = $('fs-bucket');
  if (bs) bs.addEventListener('change', function () { A4.bucket = bs.value; renderSeries(); });
  const sz = $('fs-size');
  if (sz) sz.addEventListener('change', function () { A4.size = Number(sz.value) || 5; renderSeries(); });
  const doOnly = $('diff-only');
  if (doOnly) doOnly.addEventListener('change', function () { A4.diffOnly = !!doOnly.checked; renderDiff(); });
  let t = null;
  window.addEventListener('resize', function () {
    if (t) clearTimeout(t);
    t = setTimeout(renderSeries, 150);
  });
}

function renderA4() {
  fillA4Controls();
  renderTimeline();
  renderSeries();
  renderDriftBars();
  renderDiff();
  wireA4();
}

/* ── 交互 ───────────────────────────────────────────────────── */
function wire() {
  const q = $('q');
  if (q) q.addEventListener('input', () => { view.q = q.value; renderTable(); });
  const st = $('f-state');
  if (st) st.addEventListener('change', () => { view.state = st.value; renderTable(); });
  const src = $('f-source');
  if (src) src.addEventListener('change', () => { view.source = src.value; renderTable(); });
  const so = $('f-sort');
  if (so) so.addEventListener('change', () => {
    const [k, d] = String(so.value).split(':');
    view.key = k; view.dir = d; renderTable();
  });
  document.querySelectorAll('#vt thead .th-btn').forEach((b) => {
    b.addEventListener('click', () => {
      const k = b.dataset.key;
      if (view.key === k) view.dir = view.dir === 'desc' ? 'asc' : 'desc';
      else { view.key = k; view.dir = k === 'when' ? 'desc' : 'asc'; }
      renderTable();
    });
  });
  const rs = $('reset');
  if (rs) rs.addEventListener('click', () => {
    view.q = ''; view.state = 'all'; view.source = 'all'; view.key = 'when'; view.dir = 'desc';
    if (q) q.value = '';
    if (st) st.value = 'all';
    if (src) src.value = 'all';
    if (so) so.value = 'when:desc';
    renderTable();
  });
}

function fillSourceOptions() {
  const sel = $('f-source');
  if (!sel) return;
  const set = [...new Set((DATA.verdicts || []).map((r) => r.source))];
  sel.innerHTML = '<option value="all">全部</option>'
    + set.map((s) => `<option value="${s}">${s}</option>`).join('');
}

async function boot() {
  // 四个源并行取：verdicts 必需，其余 best-effort（缺一个只影响对应章节）
  const results = await Promise.all(SOURCES.map((s) => fetchFirst(s.urls)));
  const failed = [];
  SOURCES.forEach((s, i) => {
    const r = results[i];
    if (r.json) { LOADED[s.key] = r; }
    else failed.push({ key: s.key, required: s.required, errors: r.errors });
  });

  if (!LOADED.verdicts) {
    const box = $('dash');
    const why = (failed.find((f) => f.key === 'verdicts') || { errors: [] }).errors.join('；');
    if (box) {
      box.innerHTML = '<div class="empty"><b>数据不可用</b>'
        + '<p>加载 <span class="kbd">data/verdicts_667.json</span> 失败：' + esc(why) + '</p>'
        + '<p>生成命令：<span class="kbd">python tools/web_verdicts_667.py --write</span>；'
        + '静态站需经 HTTP 打开（<span class="kbd">python -m http.server 8765 --directory web</span>）。</p></div>';
    }
    PARSED = null; MODEL = null;
    renderTimeline(); renderSeries(); renderDriftBars(); renderDiff();   // 全部走占位，不崩
    return;
  }

  DATA = LOADED.verdicts.json;
  PARSED = parseVerdicts(DATA);
  DRIFT = parseDrift(DATA, { source: 'web/data/verdicts_667.json' });
  BASE_DRIFT = LOADED.baseline
    ? parseDrift(LOADED.baseline.json, { source: LOADED.baseline.url })
    : { items: [], total: 0, numeric: 0, text_only: 0, tolerated: 0, sources: [], issues: [{ code: 'unavailable', msg: 'baseline.json 未加载' }] };
  MODEL = buildCompareModel({
    verdicts: DATA,
    status: LOADED.status ? LOADED.status.json : null,
    metrics: LOADED.metrics ? LOADED.metrics.json : null,
    baseline: LOADED.baseline ? LOADED.baseline.json : null,
    parsed: PARSED,
  });

  renderDash(); renderDrift(); fillSourceOptions();
  renderTable(); renderCompare(); renderExcluded(); wire();
  renderA4();
}

/* ── 自动化验证钩子（给 tools/web_smoke_667.mjs 用；只读语义，不改渲染路径）── */
window.__verdicts_hooks = {
  ready: () => !!DATA,
  total: () => (DATA?.verdicts || []).length,
  dashCells: () => dashCells(DATA?.dashboard || {}, DATA?.verdicts_total ?? 0)
    .map((c) => ({ key: c.key, num: c.num, bad: !!c.bad, warn: !!c.warn })),
  /** 按当前 view 返回行 id（等价于"筛选+排序"后的可见行）。 */
  visibleIds: () => sortRows(filterRows(DATA?.verdicts || [], view), view.key, view.dir).map((r) => r.id),
  setView: (patch) => { Object.assign(view, patch); renderTable(); return view; },
  compareRows: () => (DATA?.compare || []).map((r) => `${r.metric}|${r.kind}`),
  driftFields: () => (DATA?.drift || []).map((d) => d.field),
  bodyText: () => ($('vt-body')?.textContent || ''),
  emptyText: () => ($('vt-empty')?.textContent || ''),
  /* ── 670c A4 追加（只读语义，不改任何渲染路径）── */
  loadedSources: () => Object.keys(LOADED),
  parsedTotal: () => PARSED?.total ?? 0,
  parsedCounts: () => (PARSED ? { ...PARSED.counts } : null),
  timelineIds: () => (PARSED ? buildTimeline(PARSED, { dir: A4.tlDir }).items.map((r) => r.id) : []),
  timelineStates: () => (PARSED ? buildTimeline(PARSED, { dir: A4.tlDir }).order : []),
  timelineItems: () => $$('#tl .tl-item').length,
  seriesBuckets: () => (PARSED ? fourStateSeries(PARSED, { bucket: A4.bucket, size: A4.size }).buckets.map((b) => b.key + ':' + b.total) : []),
  driftBarCount: () => $$('#drift-bars .drift-bar').length,
  driftBarValues: () => $$('#drift-bars .drift-bar').map((el) => el.getAttribute('data-kind')),
  diffRedKeys: () => (MODEL ? MODEL.red_keys : []),
  diffRedRows: () => $$('#diff-body tr.is-mismatch').map((el) => el.getAttribute('data-key')),
  setA4: (patch) => { Object.assign(A4, patch); renderA4(); return { ...A4 }; },
};

if (document.readyState !== 'loading') boot();
else document.addEventListener('DOMContentLoaded', boot);
