// 667 阶段2 · 判决页渲染层（DOM）。纯逻辑在 `verdicts_core.js`（可被 Node 真求值）。
//
// 纪律：① **只渲染，不写死** —— 数字全来自 web/data/verdicts_667.json；
//      ② 拿不到就显示"不可用"并说明生成命令，绝不猜（docs/discipline/error_handling.md）；
//      ③ 动效尊重 `prefers-reduced-motion`；④ 暴露 `window.__verdicts_hooks` 给 jsdom 冒烟。
import { fetchJSON } from './app.js';
import { sortRows, filterRows, dashCells, fmtNum, KIND_LABEL } from './verdicts_core.js';

const $ = (id) => document.getElementById(id);
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
      <td class="w-detail">${r.detail || '<span class="note-faint">（无说明）</span>'}</td>
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
  try {
    DATA = await fetchJSON('data/verdicts_667.json');
  } catch (e) {
    const box = $('dash');
    if (box) {
      box.innerHTML = `<div class="empty"><b>数据不可用</b>
        <p>加载 <span class="kbd">data/verdicts_667.json</span> 失败：${e.message}</p>
        <p>生成命令：<span class="kbd">python tools/web_verdicts_667.py --write</span>；
        静态站需经 HTTP 打开（<span class="kbd">python -m http.server 8765 --directory web</span>）。</p></div>`;
    }
    return;
  }
  renderDash(); renderDrift(); fillSourceOptions();
  renderTable(); renderCompare(); renderExcluded(); wire();
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
};

if (document.readyState !== 'loading') boot();
else document.addEventListener('DOMContentLoaded', boot);
