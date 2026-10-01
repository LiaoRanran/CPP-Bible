// ═══════════════════════════════════════════════════════════════════════════
// 672g C · 学习页**纯逻辑 + 字符串渲染**（无 DOM / 无 fetch / 无 localStorage
//   ⇒ Node 里直接真跑，见 tests/learn_core.test.mjs）
//
// 由来：learn.html 的 139–495 行内联 module 脚本（约 350 行）无法被 Node 测试 ——
//   筛选、评分、SVG 拼串和 getElementById 焊在一起。672g 劈成两层：
//     · 本文件   —— 过滤 / 统计接线 / 全部 HTML·SVG **字符串**生成（纯函数）
//     · js/learn.js —— document / localStorage / Blob / FileReader / 事件
//
// 学习科学口径（照搬 _arch_v38，一个字不改）：
//   · 间隔重复：SM-2 调度（learn_engine.sm2）
//   · 主动回忆：先回想再揭晓（revealed=false 时不给答案）
//   · 错例驱动：错误断言 → 反例代码 → sanitizer 输出 → 正确断言（四段式）
//   · 机器生成的错例**无人签** ⇒ 打"机器生成 · 未签"标，不进 cards.json 台账
// ═══════════════════════════════════════════════════════════════════════════

import {
  sm2, isMastered, isWeak, isTouched, freshState,
  dueQueue, formatNextReview, errorCardCompleteness,
} from './learn_engine.js';

/** 进度在 localStorage 里的键名（页面说明里也写了这个名，两处必须一致）。 */
export const STORE_KEY = 'qy-learn-progress-v1';

/** 自测四档（SM-2 的 q）：键 1/2/3/4 对应 q = 1 / 3 / 4 / 5。 */
export const GRADES = [[1, '忘了'], [3, '困难'], [4, '还行'], [5, '流畅']];

/** 今日队列最多展示条数（照搬内联版 renderQueue 的 12）。 */
export const QUEUE_LIMIT = 12;

const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const fmt = (n) => (n ?? 0).toLocaleString('en-US');
/** 易学因子显示（stateOf 可能给 freshState ⇒ 恒有 ease，仍兜底 2.50）。 */
const easeText = (st) => (st && typeof st.ease === 'number' ? st.ease.toFixed(2) : '2.50');
const stateOf = (progress, id) => (progress && progress[id]) || freshState();

export { esc, fmt };

/* ══ ① 牌组过滤（原本 inline 的 filterList，只把 DOM 取值换成入参）══════════ */

/** 牌组过滤（纯函数）。
 *  · domain 只在知识卡牌组生效（错例牌组没有 domain 维度 —— 与线上一致）
 *  · 全文：id / 标题 / 断言 / 错误断言 / 正确断言 / 反例 / 检测器 / domain 拼成一串后包含匹配
 *  · scope：untouched=未学过 · weak=薄弱 · due=今日该复习的优先（走 dueQueue）· 其余=全部 */
export function filterDeck(cards, opts = {}) {
  const o = opts || {};
  const q = String(o.q == null ? '' : o.q).trim().toLowerCase();
  const dom = o.domain || '';
  const scope = o.scope || 'due';
  const progress = o.progress || {};
  const isAtom = o.isAtom !== false;
  let arr = Array.isArray(cards) ? cards.slice() : [];
  if (isAtom && dom) arr = arr.filter((c) => c && c.domain === dom);
  if (q) {
    arr = arr.filter((c) => (c ? [
      c.id, c.title, c.assertion, c.wrong_assertion, c.correct_assertion,
      c.counterexample, c.detector, c.domain,
    ].filter(Boolean).join(' ').toLowerCase().includes(q) : false));
  }
  if (scope === 'untouched') arr = arr.filter((c) => !isTouched(progress[c.id]));
  // 672g 顺带修的隐患：内联版直接写 isWeak(progress[c.id])，而 isWeak 内部读 st.lapses
  //   ⇒ 牌组里只要有一张**从没学过**的卡（progress 里没有这个 key），切到"薄弱"范围就
  //   TypeError 整页白屏。这里补一个"没学过 ⇒ 不算薄弱"的短路：语义更对（薄弱 = 学过且答错），
  //   也保证任何 progress 形状下都不抛。有进度记录的卡行为与原来完全一致。
  else if (scope === 'weak') arr = arr.filter((c) => !!(progress[c.id] && isWeak(progress[c.id])));
  else if (scope === 'due') {
    const set = new Set(dueQueue(progress, arr, 9999));
    arr = arr.filter((c) => set.has(c.id));
  }
  return arr;
}

/* ══ ② 统计面板 ═══════════════════════════════════════════════════════════ */

/** 学习统计六宫格（已学 / 掌握 / 薄弱 / 待复习 / 未学 / 连续天数）。 */
export function dashHtml(stats) {
  const s = stats || {};
  const streak = s.streak || {};
  return [
    ['已学', fmt(s.studied), ''],
    ['掌握', fmt(s.mastered), 'is-good'],
    ['薄弱', fmt(s.weak), s.weak ? 'is-weak' : ''],
    ['待复习', fmt(s.due), ''],
    ['未学', fmt(s.untouched), ''],
    ['连续天数', fmt(streak.current), streak.current >= 3 ? 'is-good' : ''],
  ].map(([cap, n, cls]) => '<div class="stat-tile ' + cls + '"><div class="st-n">' + n
    + '</div><div class="st-l">' + cap + '</div></div>').join('');
}

/** 掌握进度百分比（整数 0–100；total=0 ⇒ 0）。 */
export function masteryPct(stats) {
  const s = stats || {};
  return s.total ? Math.round(100 * (s.mastered || 0) / s.total) : 0;
}

/* ══ ③ 学习路径三阶段 SVG ═════════════════════════════════════════════════ */

/** 学习路径：三阶段流程图（当前阶段高亮，已达成的显示完成色）。 */
export function pathFlowSvg(p) {
  const W = 600, H = 104, NW = 168, NH = 68, GAP = 40, Y = 18;
  const stages = (p && Array.isArray(p.stages)) ? p.stages : [];
  const current = (p && p.currentStage) != null ? p.currentStage : -1;
  const parts = [];
  stages.forEach((s, i) => {
    const x = 12 + i * (NW + GAP);
    const label = s.name + '：' + s.done + '/' + s.total;
    parts.push('<g class="pf-node is-' + s.status + '" transform="translate(' + x + ',' + Y + ')" role="listitem" aria-label="' + esc(label) + '">');
    parts.push('<rect width="' + NW + '" height="' + NH + '" rx="6"></rect>');
    parts.push('<text class="pf-name" x="12" y="26">' + esc(s.name) + '</text>');
    parts.push('<text class="pf-count" x="12" y="46">' + s.done + '/' + s.total + ' · ' + Math.round(s.ratio * 100) + '%</text>');
    parts.push('<text x="12" y="60" style="font-size:10px">' + esc(s.status === 'done' ? '已完成' : s.status === 'current' ? '进行中' : '待开始') + '</text>');
    parts.push('</g>');
    if (i < stages.length - 1) {
      const x1 = x + NW, x2 = x + NW + GAP;
      const cls = s.status === 'done' ? 'pf-edge is-done' : (i === current ? 'pf-edge is-current' : 'pf-edge');
      const cy = Y + NH / 2;
      parts.push('<line class="' + cls + '" x1="' + x1 + '" y1="' + cy + '" x2="' + (x2 - 10) + '" y2="' + cy + '"></line>');
      parts.push('<polygon class="pf-badge" points="' + (x2 - 12) + ',' + (cy - 4) + ' ' + x2 + ',' + cy + ' ' + (x2 - 12) + ',' + (cy + 4) + '"></polygon>');
    }
  });
  return '<svg viewBox="0 0 ' + W + ' ' + H + '" role="list" aria-label="学习路径三阶段进度">'
    + parts.join('') + '</svg>';
}

/* ══ ④ 掌握度曲线（内联 SVG，零依赖）══════════════════════════════════════ */

/** 曲线右上角说明。 */
export function curveNoteText(curve) {
  const pts = (curve && Array.isArray(curve.points)) ? curve.points : [];
  return pts.length ? (pts.length + ' 个快照 · ' + (curve.events || 0) + ' 次复习') : '暂无记录';
}
/** 掌握度曲线：快照 < 2 ⇒ 空状态；否则画网格 + 面积 + 折线 + 快照点。 */
export function masteryCurveSvg(curve) {
  const pts = (curve && Array.isArray(curve.points)) ? curve.points : [];
  if (pts.length < 2) {
    return '<div class="chart-empty"><span class="ce-t">还没有复习记录</span>复习几张卡后，这里会画出掌握度随时间的变化。</div>';
  }
  const W = 340, H = 96, P = 8;
  const minT = pts[0].t, maxT = pts[pts.length - 1].t;
  const span = Math.max(1, maxT - minT);
  const maxY = Math.max(1, ...pts.map((p) => p.studied));
  const X = (t) => P + (W - 2 * P) * ((t - minT) / span);
  const Y = (v) => H - P - (H - 2 * P) * (v / maxY);
  const line = pts.map((p, i) => (i ? 'L' : 'M') + X(p.t).toFixed(1) + ',' + Y(p.mastered).toFixed(1)).join(' ');
  const area = line + ' L' + X(maxT).toFixed(1) + ',' + (H - P) + ' L' + X(minT).toFixed(1) + ',' + (H - P) + ' Z';
  const dots = pts.map((p) => '<circle class="sp-dot" cx="' + X(p.t).toFixed(1) + '" cy="' + Y(p.mastered).toFixed(1) + '" r="2.5"><title>'
    + new Date(p.t).toISOString().slice(0, 10) + '：已掌握 ' + p.mastered + '/' + p.studied + '</title></circle>').join('');
  const grid = [0, 0.5, 1].map((f) => '<line class="sp-grid" x1="' + P + '" y1="' + Y(maxY * f).toFixed(1) + '" x2="' + (W - P) + '" y2="' + Y(maxY * f).toFixed(1) + '"></line>').join('');
  return '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="掌握度曲线">'
    + '<title>已掌握张数随时间变化（峰值 ' + maxY + '）</title>' + grid
    + '<path class="sp-area" d="' + area + '" opacity=".35"></path>'
    + '<path class="sp-line" d="' + line + '"></path>' + dots + '</svg>';
}

/* ══ ⑤ 薄弱热力图 ═════════════════════════════════════════════════════════ */

/** 按域聚合的薄弱热力图（颜色越浅＝掌握越少；isWeak 打红框）。 */
export function heatmapHtml(cells) {
  const list = Array.isArray(cells) ? cells : [];
  if (!list.length) return '<div class="chart-empty"><span class="ce-t">这个牌组没有可聚合的域</span></div>';
  return list.map((c) => '<div class="heat-cell' + (c.isWeak ? ' is-weak' : '')
    + '" data-level="' + c.level + '" title="' + esc(c.key) + '：掌握 ' + c.mastered + '/' + c.total
    + '，已学 ' + c.studied + '，薄弱 ' + c.weak + '">'
    + '<div class="hc-n">' + c.mastered + '/' + c.total + '</div>'
    + '<div class="hc-l">' + esc(c.key) + '</div></div>').join('');
}

/* ══ ⑥ 今日队列 ═══════════════════════════════════════════════════════════ */

/** 今日队列：空 ⇒ 提示换筛选；否则按 dueQueue 顺序给"已掌握 / 薄弱 / 复习中 / 新"标签。 */
export function queueListHtml(ids, byId, progress) {
  const list = Array.isArray(ids) ? ids : [];
  if (!list.length) {
    return '<li class="muted">今天这个范围内没有要复习的 —— 切换"范围"或"牌组"试试。</li>';
  }
  return list.map((id) => {
    const c = (byId && byId[id]) || {}; const st = progress && progress[id];
    const tag = st && isMastered(st) ? '已掌握' : st && isWeak(st) ? '薄弱' : (isTouched(st) ? '复习中' : '新');
    return '<li class="queue-item" data-id="' + esc(id) + '">'
      + '<span class="chip">' + esc(tag) + '</span>'
      + '<span class="qi-title">' + esc(c.title || c.wrong_assertion || c.assertion || id) + '</span></li>';
  }).join('');
}

/* ══ ⑦ 卡片视图（知识卡三阶段 / 错例四段式）═══════════════════════════════ */

/** 评分行（揭晓后才出现）：四档 + 跳过，并预告"若评还行"的下次复习时间。 */
export function gradeRowHtml(st) {
  const next = formatNextReview(sm2(st || freshState(), 4));
  return '<div class="grade-row"><span class="muted">你回想得怎么样？</span>'
    + GRADES.map(([q, label], i) => '<button class="grade" data-q="' + q + '" type="button">'
      + (i + 1) + ' ' + label + '</button>').join('')
    + '<button id="skip" class="ghost" type="button">跳过</button></div>'
    + '<p class="section-sub">若评"还行"，下次复习约在 ' + esc(next) + '　·　当前易学因子 '
    + easeText(st) + '</p>';
}

/** 知识卡：三阶段（前置 → 断言/边界/四态/证据 → 自测）。 */
export function atomViewHtml(c, st, revealed) {
  const pill = '<span class="state-pill" data-state="' + esc(c.verdict_state) + '"><i></i>' + esc(c.verdict_state) + '</span>';
  const prereqs = (c.prereqs && c.prereqs.length)
    ? c.prereqs.map((p) => '<a class="chip link" href="card.html?card=' + encodeURIComponent(p) + '">' + esc(p) + '</a>').join(' ')
    : '<span class="muted">无先修声明（或本仓未声明）</span>';
  const evidence = (c.evidence && c.evidence.length)
    ? c.evidence.map((e) => '<span class="chip">' + esc(e) + '</span>').join(' ')
    : '<span class="muted">无</span>';
  const answer = '<div class="answer">'
    + '<div class="claim-line">' + esc(c.title) + '</div>'
    + '<div class="ci-tags" style="margin-top:8px">' + pill
    + (c.domain ? ' <span class="chip">域 ' + esc(c.domain) + '</span>' : '')
    + (c.dal ? ' <span class="chip">DAL ' + esc(c.dal) + '</span>' : '')
    + (c.audience ? ' <span class="chip">受众 ' + esc(c.audience) + '</span>' : '') + '</div>'
    + '<div class="ci-tags" style="margin-top:6px">证据：' + evidence + '</div>'
    + '<p class="muted" style="margin-top:8px">边界三元组（input_domain / precondition / failure_mode）见 '
    + '<a class="chip link" href="card.html?card=' + encodeURIComponent(c.id) + '">卡详情 →</a></p></div>';
  return '<div class="stages">'
    + '<div class="ls-stage"><span class="st-num">1</span><div><b>前置关系</b><div class="ci-tags" style="margin-top:6px">' + prereqs + '</div></div></div>'
    + '<div class="ls-stage"><span class="st-num">2</span><div><b>断言 / 四态 / 证据</b>'
    + '<p class="muted" style="margin:6px 0 0">先盖住答案，在脑子里回想这条卡讲什么，再按"揭晓"（或空格）。</p>'
    + (revealed ? answer : '<button id="flip" class="primary" type="button">揭晓断言</button>') + '</div></div>'
    + '<div class="ls-stage"><span class="st-num">3</span><div><b>自测</b>'
    + (revealed ? gradeRowHtml(st) : '<p class="muted">揭晓后在此评分（或按 1–4）。</p>') + '</div></div>'
    + '</div>';
}

/** 错例卡：四段式（错误断言 → 反例代码 → sanitizer 输出 → 正确断言）+ 自测。
 *  机器生成且无人签 ⇒ 打"机器生成 · 未签"标（不冒充已核准知识）。 */
export function errorViewHtml(c, st, revealed, deckSigned) {
  const complete = errorCardCompleteness(c);
  const badge = c.needs_review
    ? '<span class="chip" title="机器生成、无人签，不作为已核准知识">机器生成 · 未签</span>' : '';
  const step1 = '<div class="claim-line bad">' + esc(c.wrong_assertion || '（无错误断言文本）') + '</div>'
    + (c.refuted ? '<p class="section-sub">该主张已被反例证伪（b_refuted=true）。</p>' : '');
  const step2 = c.fixture_code
    ? '<pre class="code">' + esc(c.fixture_code) + '</pre>'
      + (c.fixture_path ? '<p class="section-sub mono">' + esc(c.fixture_path) + '</p>' : '')
    : '<p class="muted">本卡无反例源码。</p>';
  const step3 = c.sanitizer_output
    ? '<pre class="sanitizer-out">' + esc(c.sanitizer_output) + '</pre>'
    : '<p class="muted">本卡无 sanitizer 输出（' + esc(c.verdict || 'verdict 未知') + '：检测器未命中）。</p>';
  const step4 = revealed
    ? '<div class="answer"><div class="claim-line ok">' + esc(c.correct_assertion || '（无正确断言文本）') + '</div>'
      + '<div class="ci-tags" style="margin-top:8px">' + badge
      + (c.detector ? ' <span class="chip">检测器 ' + esc(c.detector) + '</span>' : '')
      + (c.four_state ? ' <span class="state-pill" data-state="' + esc(c.four_state) + '"><i></i>' + esc(c.four_state) + '</span>' : '')
      + (!complete.correct_assertion ? ' <span class="chip">正确断言缺失</span>' : '') + '</div>'
      + '<p class="section-sub">正确断言来源：<span class="mono">' + esc(c.correct_source) + '</span></p></div>'
    : '<button id="flip" class="primary" type="button">揭晓正确断言</button>';
  const note = (deckSigned === false || c.needs_review)
    ? '<p class="section-sub">这批错例来自机器卡（' + esc(c.source_id || c.id) + '），'
      + '<b>无人签</b>，不进 cards.json 台账；"正确断言"由反例文字派生，见上来源标注。</p>' : '';
  return '<div class="stages err-card">'
    + '<div class="ls-stage"><span class="st-num">1</span><div><b>错误断言</b>' + step1 + '</div></div>'
    + '<div class="ls-stage"><span class="st-num">2</span><div><b>反例代码</b>' + step2 + '</div></div>'
    + '<div class="ls-stage"><span class="st-num">3</span><div><b>sanitizer 输出</b>' + step3 + '</div></div>'
    + '<div class="ls-stage"><span class="st-num">4</span><div><b>正确断言</b>' + step4 + note + '</div></div>'
    + '<div class="ls-stage"><span class="st-num">5</span><div><b>自测</b>'
    + (revealed ? gradeRowHtml(st) : '<p class="muted">揭晓后在此评分（或按 1–4）。</p>') + '</div></div>'
    + '</div>';
}

/** 当前卡的视图（按 kind 分派：atom ⇒ 三阶段，其余 ⇒ 错例四段式）。 */
export function cardViewHtml(c, st, revealed, deckSigned) {
  return (c && c.kind === 'atom') ? atomViewHtml(c, st, revealed) : errorViewHtml(c, st, revealed, deckSigned);
}

/** 学习区下方的位置说明（第几张 / 下次复习 / 易学因子）。 */
export function posNoteText(pos, length, st) {
  return '第 ' + (pos + 1) + ' / ' + length + ' 张　·　'
    + '下次复习：' + formatNextReview(st) + '　·　易学因子 ' + easeText(st);
}

/** 牌组为空时的占位（说明两张牌组各自的数据来源，不编造卡）。 */
export function emptyStudyHtml() {
  return '<div class="empty"><b>没有匹配的卡</b><p>调整上方筛选，或切换牌组。知识卡来自 '
    + '<span class="mono">data/cards_index.json</span>（已排除草稿）；错例来自 '
    + '<span class="mono">data/err_deck_670c.json</span>（机器卡的反例四段式）。</p></div>';
}

/** 数据加载失败时的占位（提示用静态服务器打开）。 */
export function loadErrorHtml(err) {
  return '<div class="empty"><b>数据加载失败</b><p>' + esc(err && err.message)
    + '。请用本地静态服务器打开（如 <span class="mono">python -m http.server</span>），且 data/ 目录可访问。</p></div>';
}

/* ══ ⑧ 导入导出（纯数据部分；Blob / FileReader 仍在 learn.js）══════════════ */

/** 导出进度后的提示文案。 */
export function exportNoteText(count) {
  return '已导出 ' + count + ' 张卡进度。';
}
/** 导入进度后的提示文案（坏条目跳过了要写出来）。 */
export function importNoteText(imported, skipped) {
  return '已合并导入 ' + imported + ' 张卡进度' + (skipped ? '，跳过 ' + skipped + ' 条坏数据' : '') + '。';
}

/** 取某张卡的进度（没有 ⇒ freshState，绝不返回 undefined 让渲染层自己猜）。 */
export function stateOfCard(progress, id) { return stateOf(progress, id); }
