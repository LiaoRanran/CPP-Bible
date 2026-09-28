// 656 D · 学习 MVP：星图/列表选卡 → 三段式学习页（前置 / 学习 / 自测）+ 本机进度
//
// 设计原则（与全站一致）：
//   ① **只用真实数据**：页面渲染的每个字段都来自 `web/data/cards.json`（由 tools/teach_card_656.py 现算）；
//   ② **不假装有态**：本仓 47 张卡目前 0 张带边界三元组 ⇒ 四态必然显示 unknown，
//      页面把"为什么是 unknown"直接摊开（而不是挑一个好看的态）；
//   ③ **进度只存本机**：localStorage，不上传、无后端、无追踪；清缓存即清进度。
import { fetchJSON, fmtInt, shortHash } from './app.js';

const $ = (id) => document.getElementById(id);
const LS_KEY = 'queyi.progress.v1';

let ALL = null;                 // {count, cards: {id: card}}
let ORDER = [];                 // 稳定的卡顺序
let cur = null;                 // 当前卡对象
let progress = loadProgress();  // {id: {learned_at, correct, total, seen}}

// ── 进度（本机）────────────────────────────────────────────────────────────
function loadProgress() {
  try { return JSON.parse(localStorage.getItem(LS_KEY) || '{}') || {}; } catch { return {}; }
}
function saveProgress() {
  try { localStorage.setItem(LS_KEY, JSON.stringify(progress)); } catch { /* 隐私模式禁写：忽略 */ }
}
function renderProgress() {
  const learned = Object.values(progress).filter((p) => p && p.learned_at).length;
  const total = ALL ? ALL.count : 0;
  const pct = total ? Math.round((100 * learned) / total) : 0;
  $('progress').textContent = `本机已学 ${learned}/${total}（${pct}%）`;
}
function markLearned(id, on) {
  const p = progress[id] || {};
  p.learned_at = on ? new Date().toISOString().slice(0, 19) : null;
  progress[id] = p;
  saveProgress(); renderProgress(); renderLearnedButton();
}
function renderLearnedButton() {
  const on = !!(progress[cur?.id] || {}).learned_at;
  $('learned').setAttribute('label', on ? '已学 ✓（点击撤销）' : '标记已学');
}

// ── 渲染小工具 ─────────────────────────────────────────────────────────────
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const mono = (s) => `<span class="mono">${esc(s)}</span>`;
const panel = (title, body, cap = '') => `<qy-card title="${esc(title)}">${body}${cap ? `<p class="muted" style="margin-top:8px">${cap}</p>` : ''}</qy-card>`;

// ── 三段渲染 ───────────────────────────────────────────────────────────────
function renderPrereq(card) {
  const box = $('prereq');
  if (!card.prerequisites.length) {
    box.innerHTML = panel('本仓未声明前置', `<p>这张卡的 <span class="kbd">relations</span> 里没有
      <span class="kbd">prerequisite</span> 条目 ⇒ 台账层面**没有声明先修链**（不代表不需要基础）。</p>`);
  } else {
    box.innerHTML = card.prerequisites.map((p) => panel(
      p.title || p.id,
      `<p>${p.id} · ${esc(p.domain || '—')} · status ${esc(p.status || '—')}</p>
       <p class="muted" style="margin-top:6px">判决四态 ${esc(p.verdict_state || '—')} · 命题数 ${p.props ?? '—'}</p>
       <div class="btnrow"><qy-button data-goto="${esc(p.id)}" label="去学这张"></qy-button></div>`,
      '来源：卡 frontmatter.relations[].prerequisite（真实声明，非推测）')).join('');
  }
  const rel = card.related_verified_same_domain || [];
  $('related').innerHTML = rel.length
    ? `<p class="muted">同域已 verified（可供横向对照，**不是**先修声明）：${
        rel.map((r) => `<a href="#" data-goto="${esc(r)}">${esc(r)}</a>`).join('　·　')}</p>`
    : '';
}

function renderLearn(card) {
  const m = card.meta;
  $('card-head').innerHTML = panel(esc(m.title || card.id),
    `<p class="muted">${mono(card.id)} · ${esc(m.domain || '—')} / ${esc(m.type || '—')}
      · status ${esc(m.status || '—')} · DAL ${esc(m.dal || '—')}
      · 认知负荷 ${esc(m.cognitive_load || '—')} · 面向 ${esc(m.audience || '—')}</p>
     <p class="muted" style="margin-top:6px">文件 ${mono(card.path)}
      ${m.verified_by ? `· 人审 ${mono(m.verified_by)} @ ${esc(m.verified_at || '—')}` : ''}</p>`);

  $('claim').innerHTML = panel('核心断言（claim）', `<p style="color:var(--color-text)">${esc(card.claim)}</p>`);

  const cb = card.boundary.claim_boundary || {};
  const b3 = ['mutation_set_hash', 'mutation_count', 'generator_version'].map((k) => {
    const v = card.boundary[k];
    return `<div><span class="stat-label">${k}</span><div class="mono">${v ? esc(v) : '（缺）'}</div></div>`;
  }).join('');
  $('boundary').innerHTML = panel('边界（结论在什么范围内成立）',
    `<div class="detail" style="border:0;padding:0;background:none">
       <div><span class="stat-label">标准</span><div class="mono">${esc((cb.standard || []).join(', ') || '—')}</div></div>
       <div style="margin-top:8px"><span class="stat-label">编译器</span><div class="mono">${esc((cb.compilers || []).join(' / ') || '—')}</div></div>
       <div style="margin-top:8px"><span class="stat-label">优化</span><div class="mono">${esc((cb.opt || []).join(', ') || '—')}</div></div>
       <div style="margin-top:8px"><span class="stat-label">平台</span><div class="mono">${esc((cb.platform || []).join(', ') || '—')}</div></div>
       <div class="d-grid" style="margin-top:12px">${b3}</div>
     </div>`,
    '边界三元组（hash/count/version）是四态判决的**前提**：缺它 ⇒ 四态一律 unknown。');

  const v = card.verdict || {};
  $('verdict').innerHTML = panel('四态判决（现算）',
    `<p style="color:var(--color-text)"><qy-status state="${esc(v.state || 'unknown')}"></qy-status>
      <span class="muted">（boundary_ok=${esc(v.boundary_ok)} · downgraded=${esc(v.downgraded)}）</span></p>
     <ul style="margin:8px 0 0 18px;color:var(--color-text-dim);font-size:13px">
       ${(v.reasons || []).map((r) => `<li>${esc(r)}</li>`).join('')}
     </ul>`,
    '由 tools/four_state_verdict_638.classify_card 现场计算，页面不缓存、不美化。');

  $('props').innerHTML = `<h3>命题（${card.props.length} 条）</h3>` + (card.props.length ? card.props.map((p) => panel(
    `${p.id} · ${esc(p.claim_type || '—')}`,
    `<p style="color:var(--color-text)">${esc(p.statement)}</p>
     <p class="muted" style="margin-top:6px">${mono(p.subject)} ${mono(p.predicate)} ${mono(p.object)}</p>
     ${p.external_basis ? `<p class="muted" style="margin-top:6px">外部依据：${esc(p.external_basis)}</p>` : ''}
     <p class="muted" style="margin-top:6px">证据 ${(p.evidence || []).map((e) => mono(e)).join(' ')}
      ${p.liveness ? `· 活性 ${mono(JSON.stringify(p.liveness))}` : ''}
      ${p.signed_by ? `· 签 ${mono(p.signed_by)}` : ''}</p>`)).join('')
    : '<p class="muted">该卡没有 claim_structured（自测题会退化）</p>');

  $('evidence').innerHTML = `<h3>证据（${card.evidence.length} 张卡）</h3>` + card.evidence.map((e) => {
    if (!e.exists) return panel(`${e.id}（缺失）`, `<p style="color:var(--color-fail)">${esc(e.note || '')}</p>`);
    return panel(`${e.id} · verdict=${esc(e.verdict)}`,
      `<p class="muted">${esc(e.hypothesis || '')}</p>
       <p class="muted" style="margin-top:6px">fixture ${mono(e.fixture)}　artifact ${mono(e.artifact)}
         ${e.artifact_sha256 ? `· sha256 ${mono(shortHash(e.artifact_sha256))}` : ''}</p>
       ${e.replay_command ? `<pre class="mono" style="white-space:pre-wrap;background:var(--color-surface-2);
         border:1px solid var(--color-line);border-radius:var(--radius-md);padding:10px;margin-top:8px;
         font-size:12px;overflow:auto">${esc(e.replay_command)}</pre>` : ''}`);
  }).join('');

  const mis = card.misconceptions || [];
  $('misconceptions').innerHTML = `<h3>反例 / 被攻击（${mis.length}）</h3>` + (mis.length
    ? `<table><thead><tr><th>误解</th><th>指向</th><th>状态</th></tr></thead><tbody>${
        mis.map((x) => `<tr><td class="mono-cell">${esc(x.misconception)}</td>
          <td class="mono-cell">${esc(x.target)}</td>
          <td><qy-tag kind="${x.defeated ? 'ok' : 'warn'}">${x.defeated ? '已击败' : '未被击败'}</qy-tag></td></tr>`).join('')
      }</tbody></table>`
    : '<p class="muted">W2 接地图里没有指向本卡命题的攻击边（不等于没有反例，只表示台账没记）。</p>');
}

function renderSelfcheck(card) {
  const rows = card.selfcheck || [];
  $('selfcheck').innerHTML = rows.map((s, i) => `
    <qy-card title="Q${i + 1}　${esc(s.q)}">
      <div class="btnrow">
        <qy-button data-reveal="${i}" label="显示答案"></qy-button>
        <qy-button data-score="1" data-idx="${i}" label="我答对了"></qy-button>
        <qy-button data-score="0" data-idx="${i}" label="没答上"></qy-button>
        <span class="muted" id="sc-state-${i}"></span>
      </div>
      <div id="sc-a-${i}" style="display:none;margin-top:8px">
        <p style="color:var(--color-text);white-space:pre-wrap">${esc(s.a)}</p>
        <p class="muted" style="margin-top:6px">出处：${esc(s.source)}</p>
      </div>
    </qy-card>`).join('');
  const p = progress[card.id] || {};
  if (p.correct != null && p.total) {
    $('sc-state-0').textContent = '';   // 状态由按钮更新，保持简洁
  }
}

// ── 装载一张卡 ─────────────────────────────────────────────────────────────
function show(id) {
  if (!ALL || !ALL.cards[id]) return;
  cur = ALL.cards[id];
  $('pick').value = id;
  renderPrereq(cur); renderLearn(cur); renderSelfcheck(cur); renderLearnedButton();
  $('ledger-note').textContent = `台账现状：${fmtInt(ALL.count)} 张卡 · 当前卡来自 `
    + `${cur.path} · 数据生成于 ${ALL.generated_at || '—'}（${(cur.generated_from || []).length} 个来源，见 tools/teach_card_656.py）`;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function step(d) {
  const i = ORDER.indexOf(cur.id);
  const j = (i + d + ORDER.length) % ORDER.length;
  show(ORDER[j]);
}

// ── 事件 ───────────────────────────────────────────────────────────────────
document.addEventListener('click', (e) => {
  const t = e.target.closest('[data-goto]');
  if (t) { e.preventDefault(); show(t.dataset.goto); return; }
  const r = e.target.closest('[data-reveal]');
  if (r) {
    const el = $('sc-a-' + r.dataset.reveal);
    el.style.display = el.style.display === 'none' ? 'block' : 'none';
    r.setAttribute('label', el.style.display === 'none' ? '显示答案' : '收起答案');
    return;
  }
  const s = e.target.closest('[data-score]');
  if (s) {
    const p = progress[cur.id] || { correct: 0, total: 0 };
    p.correct = (p.correct || 0) + Number(s.dataset.score);
    p.total = (p.total || 0) + 1;
    progress[cur.id] = p; saveProgress();
    $('sc-state-' + s.dataset.idx).textContent =
      `本机记录：答对 ${p.correct}/${p.total}（第 ${s.dataset.idx * 1 + 1} 题）`;
  }
});
$('prev').addEventListener('qy-click', () => step(-1));
$('next').addEventListener('qy-click', () => step(1));
$('learned').addEventListener('qy-click', () => markLearned(cur.id, !(progress[cur.id] || {}).learned_at));
$('reveal-all').addEventListener('qy-click', () => {
  document.querySelectorAll('[id^="sc-a-"]').forEach((el) => { el.style.display = 'block'; });
});
$('hide-all').addEventListener('qy-click', () => {
  document.querySelectorAll('[id^="sc-a-"]').forEach((el) => { el.style.display = 'none'; });
});
$('pick').addEventListener('change', (e) => show(e.target.value));

// ── 启动 ───────────────────────────────────────────────────────────────────
(async function main() {
  let idx;
  try {
    idx = await fetchJSON('data/cards_index.json');
    ALL = await fetchJSON('data/cards.json');
  } catch (e) {
    $('prereq').innerHTML = panel('加载失败', `<p style="color:var(--color-fail)">${esc(e.message)}</p>`,
      '请用本地静态服务器打开（file:// 下 fetch 受限），并先跑 python tools/teach_card_656.py --all');
    return;
  }
  ALL.generated_at = ALL.generated_at || idx.generated_at;
  ORDER = idx.cards.map((c) => c.id);
  $('pick').innerHTML = idx.cards.map((c) =>
    `<option value="${esc(c.id)}">${esc(c.id)}　${esc((c.title || '').slice(0, 40))}${
      c.draft ? '（draft）' : ''}</option>`).join('');
  renderProgress();

  const params = new URLSearchParams(location.search);
  show(params.get('card') && ALL.cards[params.get('card')] ? params.get('card') : ORDER[0]);

  // 本仓现状（真实数字，不是文案）：0 张卡带边界三元组 ⇒ 四态全 unknown
  const unknown = idx.cards.filter((c) => c.verdict_state === 'unknown').length;
  const note = document.createElement('p');
  note.className = 'muted';
  note.style.marginTop = '8px';
  note.innerHTML = `台账现状（现算）：${idx.count} 张卡中 <b>${unknown}</b> 张的判决四态是 `
    + `<span class="mono">unknown</span> —— 因为 <span class="mono">mutation_set_hash/count/generator_version</span> `
    + `边界三元组尚未落到卡上（655 B 已登记）。页面**照实显示**，不挑好看的态。`;
  document.getElementById('ledger-note').after(note);
  window.__card_ready = true;   // 供自动化验证探测
})();
