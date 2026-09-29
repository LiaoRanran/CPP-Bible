// 666 B3/B6 · 卡库页：网格 + 筛选 + 搜索 + 展开（含机器卡独立区）
//
// 数据纪律：只渲染 `web/data/cards_index.json`（台账索引）与 `web/data/ig_cards_665.json`
//          （机器卡）；**不**在浏览器里推断状态 —— 状态字段由台账给，缺就是"未声明"。
// 性能（B6）：增量渲染（每批 24 张 + IntersectionObserver 哨兵）+ 列表项不做重排，
//            避免"47 张卡一次性建 DOM"（卡多时线性放大）。真正的虚拟滚动未做（见 666 报告登记）。
// 无障碍（B7）：原生 select/input/button；结果数用 `role="status" aria-live="polite"` 播报；
//              每张卡的"去学习"是 `<a>`（可 Tab、可复制链接）；网格是 `<ul>`（屏幕阅读器报条目数）。
import { fetchJSON, fmtInt } from './app.js';

const $ = (id) => document.getElementById(id);
const PAGE = 24;

let ALL = [];          // 台账卡（含草稿）
let VIEW = [];         // 过滤后的视图
let shown = 0;

const esc = (s) => String(s ?? '').replace(/[&<>"]/g,
  (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const uniq = (arr) => [...new Set(arr.filter((v) => v !== undefined && v !== null && v !== ''))].sort();

function cardItem(c) {
  const chip = (t, cls = '') => `<span class="chip ${cls}">${esc(t)}</span>`;
  const trainable = !c.draft;   // draft650 草稿不进学习页（台账未给 claim_structured）
  const learn = trainable
    ? `<a class="chip link" href="card.html?card=${encodeURIComponent(c.id)}">去学习 →</a>`
    : `<span class="chip">草稿 · 不提供学习视图</span>`;
  return `<li class="card-item">
    <div class="ci-head">
      <span class="ci-id">${esc(c.id)}</span>
      ${c.status ? chip(`status: ${c.status}`) : chip('status: 未声明')}
      ${c.draft ? chip('draft650') : ''}
    </div>
    <div class="ci-title">${esc(c.title || '（未声明标题）')}</div>
    <div class="ci-tags">
      ${c.domain ? chip(`域 ${c.domain}`) : ''}
      ${c.type ? chip(`型 ${c.type}`) : ''}
      ${c.dal ? chip(`DAL ${c.dal}`) : ''}
      ${c.verdict_state ? chip(`判决 ${c.verdict_state}`) : chip('判决 未声明')}
      ${c.downgraded ? chip('已降级') : ''}
      ${chip(`命题 ${fmtInt((c.props || []).length)}`)}
      ${chip(`证据 ${fmtInt((c.evidence || []).length)}`)}
      ${chip(`先修 ${fmtInt((c.prereqs || []).length)}`)}
    </div>
    <details>
      <summary>展开细节（台账字段；不推断）</summary>
      <div class="ci-body">
        <div>id：<span class="mono">${esc(c.id)}</span></div>
        <div>audience：${esc(c.audience ?? '未声明')} · cognitive_load：${esc(c.cognitive_load ?? '未声明')}</div>
        <div>命题 id：${(c.props || []).length ? esc((c.props || []).join(', ')) : '（无）'}</div>
        <div>证据 id：${(c.evidence || []).length ? esc((c.evidence || []).join(', ')) : '（无）'}</div>
        <div>先修：${(c.prereqs || []).length ? esc((c.prereqs || []).join(', ')) : '（本仓未声明）'}</div>
        <div style="margin-top:6px">${learn}</div>
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
  $('count').textContent = `匹配 ${fmtInt(VIEW.length)} / 共 ${fmtInt(ALL.length)} 张`
    + `（已显示 ${fmtInt(shown)}）· 状态口径见 docs/discipline/provenance.md`;
}

function applyFilters() {
  const q = ($('q').value || '').trim().toLowerCase();
  const st = $('f-status').value, dm = $('f-domain').value, tp = $('f-type').value;
  const scope = $('f-scope').value;
  VIEW = ALL.filter((c) => {
    if (scope === 'real' && c.draft) return false;
    if (scope === 'draft' && !c.draft) return false;
    if (st && (c.status || '') !== st) return false;
    if (dm && (c.domain || '') !== dm) return false;
    if (tp && (c.type || '') !== tp) return false;
    if (q && !(`${c.id} ${c.title || ''}`.toLowerCase().includes(q))) return false;
    return true;
  });
  $('grid').innerHTML = '';
  shown = 0;
  renderBatch();
}

function fillSelect(id, values, labeler = (v) => v) {
  const sel = $(id);
  sel.insertAdjacentHTML('beforeend',
    values.map((v) => `<option value="${esc(v)}">${esc(labeler(v))}</option>`).join(''));
}

async function renderIg() {
  const grid = $('ig-grid');
  try {
    const D = await fetchJSON('data/ig_cards_665.json');
    $('ig-note').textContent = `${D.total} 张 · ${D.status} · 与 664 记录一致 ${D.agree_with_664}`
      + `　·　复算：${D.recheck_cmd}　·　${D.note}`;
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
    $('ig-note').textContent = `机器卡不可用：${e.message}`;
  }
}

(async function main() {
  renderIg();   // 与卡库并行，互不阻塞
  try {
    const D = await fetchJSON('data/cards_index.json');
    ALL = D.cards || [];
  } catch (e) {
    $('count').textContent = `加载 data/cards_index.json 失败：${e.message}`
      + '（生成命令 python tools/web_data_653.py；请用本地静态服务器打开）';
    return;
  }
  fillSelect('f-status', uniq(ALL.map((c) => c.status)));
  fillSelect('f-domain', uniq(ALL.map((c) => c.domain)));
  fillSelect('f-type', uniq(ALL.map((c) => c.type)));
  applyFilters();

  $('q').addEventListener('input', applyFilters);
  for (const id of ['f-status', 'f-domain', 'f-type', 'f-scope']) {
    $(id).addEventListener('change', applyFilters);
  }
  $('reset').addEventListener('click', () => {
    $('q').value = ''; $('f-status').value = ''; $('f-domain').value = '';
    $('f-type').value = ''; $('f-scope').value = 'real';
    applyFilters();
  });
  $('more').addEventListener('click', renderBatch);

  // 增量渲染：滚到底自动续一批（B6）；没有 IntersectionObserver 时靠按钮
  if ('IntersectionObserver' in window) {
    new IntersectionObserver((ents) => {
      if (ents.some((e) => e.isIntersecting) && shown < VIEW.length) renderBatch();
    }, { rootMargin: '400px' }).observe($('more-wrap'));
  }
})();
