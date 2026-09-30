// 670c A1 · 学习引擎（纯逻辑，无 DOM / 无 fetch —— 可在 Node 直接真跑测试）
//
// 学习科学依据（_arch_v38）：
//   · 间隔重复（SM-2）：基于每次回忆质量的调度，比固定间隔留存更高；
//   · 主动回忆（retrieval practice）：先隐藏答案再回忆，比重读有效；
//   · 错例驱动（error-driven）：先看反例（错误代码）再看正例（正确断言）。
//
// 本模块只做"算"，不做"渲染"：状态结构、SM-2 调度、牌组构建、路径进度、
// 掌握度曲线、薄弱热力图、连续天数、键位映射、导入导出校验。
// 真实数据由 learn.html 注入（cards_index.json + err_deck_670c.json）。

export const DAY = 86400000;

/** 单卡学习状态的初始值（SM-2） */
export function freshState() {
  return { ease: 2.5, interval: 0, reps: 0, lapses: 0, due: 0, lastQ: null, history: [] };
}

/**
 * SM-2 调度（SuperMemo 2，经典实现）。
 * @param {object} st  当前状态（含 ease/interval/reps/lapses/history）
 * @param {number} q   回忆质量 0–5（0=完全忘；5=完美流畅）
 * @param {number} now 时间戳（默认 Date.now()，便于测试注入）
 * @returns {object}   新状态（不修改入参）
 */
export function sm2(st, q, now = Date.now()) {
  const ease = st.ease ?? 2.5;
  let interval = st.interval ?? 0;
  let reps = st.reps ?? 0;
  let lapses = st.lapses ?? 0;
  const quality = Math.max(0, Math.min(5, Math.round(q)));

  if (quality < 3) {
    // 回忆失败：重置重复计次，明天重学
    reps = 0;
    interval = 1;
    lapses += 1;
  } else {
    if (reps === 0) interval = 1;
    else if (reps === 1) interval = 6;
    else interval = Math.round(interval * ease);
    reps += 1;
  }

  // 更新易学因子（下限 1.3，避免塌缩）
  let newEase = ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
  newEase = Math.max(1.3, newEase);

  const due = now + interval * DAY;
  return {
    ...st,
    ease: newEase,
    interval,
    reps,
    lapses,
    due,
    lastQ: quality,
    history: [...(st.history || []), { q: quality, t: now }],
  };
}

/** 是否到期（可被复习）：due <= now */
export function isDue(st, now = Date.now()) {
  return (st.due ?? 0) <= now;
}

/** 是否"已掌握"：间隔 ≥ 21 天且至少成功重复 2 次 */
export function isMastered(st) {
  return (st.interval ?? 0) >= 21 && (st.reps ?? 0) >= 2 && (st.lastQ ?? 0) >= 3;
}

/** 是否"薄弱"：有过失败（lapses）或最近一次回忆质量偏低 */
export function isWeak(st) {
  return (st.lapses ?? 0) >= 1 || (st.lastQ ?? 0) < 3;
}

/**
 * 是否"动过"：有任何学习痕迹。
 *
 * 670c 修正（669c 遗留 bug）：SM-2 在回忆失败时把 reps 重置为 0，只增加 lapses。
 * 669c 用 reps>0 判定"已学"，于是**昨天刚答错**的卡会被算成"未学/未触碰"，
 * 既不计入薄弱、也不进"待复习"，正好把最该复习的卡藏了起来。
 * 这里改用"有痕迹"判定（成功重复 / 失败 / 有历史事件任一）。
 */
export function isTouched(st) {
  if (!st) return false;
  if ((st.reps ?? 0) > 0) return true;
  if ((st.lapses ?? 0) > 0) return true;
  return Array.isArray(st.history) && st.history.length > 0;
}

/**
 * 由 cards_index.json 的 cards 数组构建"知识卡牌组"。
 * 排除草稿（draft=true，台账未给 claim_structured，不进教学台账）。
 * 每张牌只携带**台账里真实存在的字段**，不编造断言/边界文本。
 */
export function buildCardDeck(cards = []) {
  return cards
    .filter((c) => !c.draft)
    .map((c) => ({
      id: c.id,
      kind: 'atom',
      title: c.title || c.id,
      domain: c.domain || '',
      verdict_state: c.verdict_state || 'unknown',
      dal: c.dal || '',
      audience: c.audience || '',
      evidence: Array.isArray(c.evidence) ? c.evidence : [],
      prereqs: Array.isArray(c.prereqs) ? c.prereqs : [],
    }));
}

/**
 * 构建"反例牌组"（错误驱动）。
 *
 * 兼容两种输入：
 *   1) web/data/err_deck_670c.json（670c 新增，推荐）
 *      { cards: [{ wrong_assertion, counterexample, fixture_code, sanitizer_output,
 *                  correct_assertion, correct_source, ... }] }
 *   2) web/data/ig_cards_665.json（665/669c 旧格式）
 *      { cards: [{ assertion, counterexample, measured_out, fixture, ... }] }
 *
 * 四段式（错误断言 → 反例代码 → sanitizer 输出 → 正确断言）两种格式都能填满；
 * 缺哪段就是空串，**不编造**。correct_source 记录"正确断言"的来源。
 */
export function buildErrorDeck(ig = {}) {
  const cards = Array.isArray(ig.cards) ? ig.cards : [];
  return cards
    .filter((c) => c && (c.counterexample || c.wrong_assertion || c.assertion))
    .map((c) => {
      const isNew = Object.prototype.hasOwnProperty.call(c, 'wrong_assertion');
      const wrong = isNew ? (c.wrong_assertion || '') : (c.assertion || '');
      const correct = isNew ? (c.correct_assertion || '') : '';
      return {
        id: c.id || wrong || 'ig',
        kind: 'error',
        detector: c.detector || '',
        verdict: c.verdict || '',
        four_state: c.four_state || '',
        signature: c.signature || '',
        wrong_assertion: wrong,
        counterexample: c.counterexample || '',
        fixture_path: isNew ? (c.fixture_path || '') : (c.fixture || ''),
        fixture_code: c.fixture_code || '',
        sanitizer_output: isNew ? (c.sanitizer_output || '') : (c.measured_out || '').trim(),
        correct_assertion: correct,
        // 旧格式没有"正确断言"字段 ⇒ 来源标 unknown，前端不得假装有
        correct_source: isNew ? (c.correct_source || 'counterexample-text/machine-unsigned') : 'unavailable/legacy-ig-format',
        refuted: isNew ? !!c.refuted : (c.verdict === 'catch'),
        needs_review: isNew ? !!c.needs_review : true,
      };
    });
}

/** 反例牌的"四段式"是否完整（用于统计与前端提示） */
export function errorCardCompleteness(card) {
  return {
    wrong_assertion: !!card.wrong_assertion,
    counterexample: !!card.counterexample,
    fixture_code: !!card.fixture_code,
    sanitizer_output: !!card.sanitizer_output,
    correct_assertion: !!card.correct_assertion,
    complete: !!(card.wrong_assertion && card.counterexample
      && card.fixture_code && card.sanitizer_output && card.correct_assertion),
  };
}

/* ══════════════════════════════════════════════════════════════
   A1 · 学习路径可视化（三阶段）
   ══════════════════════════════════════════════════════════════ */

export const STAGES = [
  { id: 'prereq', name: '前置关系', desc: '先修卡掌握后才算走通' },
  { id: 'assert', name: '断言 / 四态 / 证据', desc: '主动回忆：先回想再揭晓（学过一次即算走通）' },
  { id: 'quiz', name: '自测', desc: '按回忆质量评分（SM-2 调度）' },
];

/**
 * 三阶段进度。每阶段给出 done/total/ratio/status。
 *  · prereq：先修（限定在牌组内、可学的那些）全部掌握；
 *  · assert：卡被学过（有任何学习痕迹，见 isTouched）；
 *  · quiz  ：卡被判定为"已掌握"。
 * status: 'done' | 'current' | 'todo'；currentStage 取第一个未完成阶段（全完成取末阶段）。
 */
export function pathProgress(progress = {}, deck = []) {
  const ids = new Set(deck.map((c) => c.id));
  const total = deck.length;
  let ready = 0, studied = 0, mastered = 0;

  for (const c of deck) {
    // 只把"牌组内"的先修算作可判定条件；牌组外先修无法在此学习，忽略
    const known = (c.prereqs || []).filter((p) => ids.has(p));
    const ok = known.every((p) => isMastered(progress[p] || {}));
    if (ok) ready += 1;

    const st = progress[c.id];
    if (isTouched(st)) {
      studied += 1;
      if (isMastered(st)) mastered += 1;
    }
  }

  const raw = [
    { done: ready, total },
    { done: studied, total },
    { done: mastered, total },
  ];

  const stages = STAGES.map((s, i) => {
    const { done } = raw[i];
    const ratio = total > 0 ? done / total : 0;
    return { ...s, index: i, done, total, ratio, status: 'todo' };
  });

  let currentStage = stages.findIndex((s) => s.ratio < 1);
  if (currentStage < 0) currentStage = stages.length - 1;

  for (let i = 0; i < stages.length; i++) {
    if (i < currentStage) stages[i].status = 'done';
    else if (i === currentStage) stages[i].status = stages[i].ratio >= 1 ? 'done' : 'current';
  }
  // 全完成时末阶段也标 done
  if (stages.every((s) => s.ratio >= 1)) stages.forEach((s) => { s.status = 'done'; });

  const overall = stages.length ? stages.reduce((a, s) => a + s.ratio, 0) / stages.length : 0;
  return { stages, currentStage, overall, total };
}

/* ══════════════════════════════════════════════════════════════
   A1 · SM-2 可视化：下次复习 / 掌握度曲线 / 薄弱热力图
   ══════════════════════════════════════════════════════════════ */

/** 下次复习时间戳；从未学过返回 null */
export function nextReviewAt(st) {
  if (!st || (st.reps ?? 0) === 0) return null;
  return st.due ?? null;
}

/** 下次复习的人话（用注入的 now，便于测试） */
export function formatNextReview(st, now = Date.now()) {
  const due = nextReviewAt(st);
  if (due === null) return '未开始';
  const days = (due - now) / DAY;
  if (days <= 0) return '该复习了';
  if (days < 1) return '今天';
  if (days < 2) return '明天';
  return Math.round(days) + ' 天后';
}

/**
 * 掌握度曲线：按时间重放每张卡的 history（用 sm2 重算），
 * 在每个事件时刻快照 studied / mastered / 平均回忆质量。
 * 返回 { points: [{t, studied, mastered, avgQ}], events: n }
 */
export function masteryCurve(progress = {}, deck = []) {
  const events = [];
  for (const c of deck) {
    const st = progress[c.id];
    if (!st || !Array.isArray(st.history)) continue;
    for (const h of st.history) {
      if (h && Number.isFinite(h.t) && Number.isFinite(h.q)) events.push({ id: c.id, t: h.t, q: h.q });
    }
  }
  events.sort((a, b) => a.t - b.t || String(a.id).localeCompare(String(b.id)));

  const states = {};
  const points = [];
  let i = 0;
  while (i < events.length) {
    const t = events[i].t;
    // 同一时刻的事件一起应用后再快照，避免同刻出现多个点
    while (i < events.length && events[i].t === t) {
      const e = events[i];
      states[e.id] = sm2(states[e.id] || freshState(), e.q, e.t);
      i += 1;
    }
    const all = Object.values(states);
    const studied = all.length;
    const mastered = all.filter(isMastered).length;
    const avgQ = studied ? all.reduce((a, s) => a + (s.lastQ ?? 0), 0) / studied : 0;
    points.push({ t, studied, mastered, avgQ });
  }
  return { points, events: events.length };
}

/**
 * 薄弱知识点热力图：按 keyOf(card)（默认 domain）分桶，
 * 给出 total/studied/mastered/weak 与 level(0–3)。
 * level 以"掌握占比"分档：0 未学；≥1/3 掌握 → 2；≥2/3 掌握 → 3。
 * 返回按"越薄弱越靠前"排序的数组。
 */
export function weakHeatmap(progress = {}, deck = [], keyOf = (c) => c.domain || '未标注') {
  const buckets = new Map();
  for (const c of deck) {
    const k = keyOf(c);
    if (!buckets.has(k)) buckets.set(k, { key: k, total: 0, studied: 0, mastered: 0, weak: 0 });
    const b = buckets.get(k);
    b.total += 1;
    const st = progress[c.id];
    if (isTouched(st)) {
      b.studied += 1;
      if (isMastered(st)) b.mastered += 1;
      if (isWeak(st)) b.weak += 1;
    }
  }
  const out = [...buckets.values()].map((b) => {
    const m = b.total ? b.mastered / b.total : 0;
    const level = b.studied === 0 ? 0 : m >= 2 / 3 ? 3 : m >= 1 / 3 ? 2 : 1;
    return { ...b, level, isWeak: b.weak > 0, ratio: m };
  });
  out.sort((a, b) => (b.weak - a.weak) || (a.ratio - b.ratio) || a.key.localeCompare(b.key));
  return out;
}

/**
 * 连续学习天数：从所有 history 时间戳里取"天"（floor(t/DAY)）。
 * current：从今天（或昨天）往前连续计数；longest：历史最长连续。
 */
export function streakDays(progress = {}, now = Date.now()) {
  const days = new Set();
  for (const st of Object.values(progress)) {
    if (!st || !Array.isArray(st.history)) continue;
    for (const h of st.history) {
      if (h && Number.isFinite(h.t)) days.add(Math.floor(h.t / DAY));
    }
  }
  const sorted = [...days].sort((a, b) => a - b);
  let longest = 0, run = 0, prev = null;
  for (const d of sorted) {
    run = (prev !== null && d === prev + 1) ? run + 1 : 1;
    if (run > longest) longest = run;
    prev = d;
  }
  const today = Math.floor(now / DAY);
  let current = 0;
  let cursor = days.has(today) ? today : (days.has(today - 1) ? today - 1 : null);
  while (cursor !== null && days.has(cursor)) { current += 1; cursor -= 1; }
  return { current, longest, days: sorted };
}

/**
 * 统计（基于 progress 与牌组 id 列表）。
 * @param {object} progress  { [cardId]: state }，来自 localStorage
 * @param {Array}  deck      牌组（含 id）
 */
export function deckStats(progress = {}, deck = []) {
  let studied = 0, mastered = 0, weak = 0, due = 0, untouched = 0;
  const now = Date.now();
  for (const card of deck) {
    const st = progress[card.id];
    if (!isTouched(st)) { untouched += 1; continue; }
    studied += 1;
    if (isMastered(st)) mastered += 1;
    if (isWeak(st)) weak += 1;
    if (isDue(st, now)) due += 1;
  }
  return { total: deck.length, studied, mastered, weak, due, untouched };
}

/** deckStats 的增强版：额外带连续天数与路径进度 */
export function deckStatsEx(progress = {}, deck = [], now = Date.now()) {
  const base = deckStats(progress, deck);
  return { ...base, streak: streakDays(progress, now), path: pathProgress(progress, deck) };
}

/**
 * 生成今日复习队列（按"最该先复习"排序：已到期 > 临期 > 未学）。
 * 返回牌组中需要出现在"今日"里的 id 列表（已到期的优先，其次未学的补位）。
 * @param {number} limit 队列上限（避免一次刷太多）
 */
export function dueQueue(progress = {}, deck = [], limit = 20, now = Date.now()) {
  const due = [], fresh = [];
  for (const card of deck) {
    const st = progress[card.id];
    if (isTouched(st) && isDue(st, now)) due.push(card.id);
    else if (!isTouched(st)) fresh.push(card.id);
  }
  due.sort((a, b) => (progress[a].due ?? 0) - (progress[b].due ?? 0));
  return [...due, ...fresh].slice(0, limit);
}

/* ══════════════════════════════════════════════════════════════
   A1 · 键盘快捷键（纯映射，便于测试）
   ══════════════════════════════════════════════════════════════ */

/** 1–4 → SM-2 质量分（忘记/困难/良好/完美） */
export const GRADE_KEYS = { '1': 1, '2': 3, '3': 4, '4': 5 };
export const GRADE_LABELS = { 1: '忘记', 3: '困难', 4: '良好', 5: '完美' };

/**
 * 把按键映射成动作。ctx: { hasCard, revealed, index, length }
 * 返回 { action, q? }，action ∈ reveal|prev|next|grade|none
 *  · 空格：没揭晓 → 揭晓；已揭晓 → none（避免误触重复揭晓）
 *  · ←/→ ：上一张/下一张（只有一张时 none）
 *  · 1–4 ：仅"已揭晓"时评分（防止没看答案就评分）
 */
export function handleKey(key, ctx = {}) {
  const none = { action: 'none' };
  if (!ctx || !ctx.hasCard || !(ctx.length > 0)) return none;

  if (key === ' ' || key === 'Spacebar' || key === 'Space') {
    return ctx.revealed ? none : { action: 'reveal' };
  }
  if (key === 'ArrowLeft') return ctx.length > 1 ? { action: 'prev' } : none;
  if (key === 'ArrowRight') return ctx.length > 1 ? { action: 'next' } : none;
  if (Object.prototype.hasOwnProperty.call(GRADE_KEYS, key)) {
    return ctx.revealed ? { action: 'grade', q: GRADE_KEYS[key] } : none;
  }
  return none;
}

/* ══════════════════════════════════════════════════════════════
   A1 · 进度导出 / 导入（本机，带校验）
   ══════════════════════════════════════════════════════════════ */

export const EXPORT_SCHEMA = 'queyi-learn-progress/v1';

/** 一条学习状态是否可信（导入时过滤脏数据，避免坏档案毁掉整个进度） */
export function isValidState(s) {
  if (!s || typeof s !== 'object' || Array.isArray(s)) return false;
  for (const k of ['ease', 'interval', 'reps', 'lapses', 'due']) {
    const v = s[k];
    if (v !== undefined && v !== null && !Number.isFinite(v)) return false;
  }
  if (s.history !== undefined && !Array.isArray(s.history)) return false;
  return true;
}

/** 导出载荷（字符串），带 schema/时间/条数，便于复现与排查 */
export function exportPayload(progress = {}, meta = {}, now = Date.now()) {
  return JSON.stringify({
    schema: EXPORT_SCHEMA,
    exported_at: new Date(now).toISOString(),
    count: Object.keys(progress).length,
    meta,
    cards: progress,
  }, null, 2);
}

/**
 * 导入并合并。默认保留"更靠前"的那条（reps 大者胜，平局比 interval），
 * 避免把已复习进度覆盖回旧档案。逐条校验，坏条目跳过并计数。
 * @returns {{ok:boolean, progress:object, imported:number, skipped:number, error:string|null}}
 */
export function importPayload(text, existing = {}, opts = {}) {
  const prefer = opts.prefer || 'advanced';
  let data;
  try {
    data = JSON.parse(text);
  } catch (e) {
    return { ok: false, progress: existing, imported: 0, skipped: 0, error: 'JSON 解析失败：' + e.message };
  }
  const cards = (data && typeof data === 'object' && !Array.isArray(data)) ? (data.cards || data) : null;
  if (!cards || typeof cards !== 'object' || Array.isArray(cards)) {
    return { ok: false, progress: existing, imported: 0, skipped: 0, error: '结构不符：缺少 cards 对象' };
  }

  const merged = { ...existing };
  let imported = 0, skipped = 0;
  for (const [id, st] of Object.entries(cards)) {
    if (!isValidState(st)) { skipped += 1; continue; }
    const cur = merged[id];
    if (prefer === 'imported' || !cur) {
      merged[id] = st;
    } else {
      const a = cur.reps ?? 0, b = st.reps ?? 0;
      merged[id] = (b > a || (b === a && (st.interval ?? 0) > (cur.interval ?? 0))) ? st : cur;
    }
    imported += 1;
  }
  return { ok: true, progress: merged, imported, skipped, error: null };
}
