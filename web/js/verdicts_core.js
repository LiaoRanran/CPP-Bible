// 670c A4 · 判决页深化 · **纯逻辑层**（无 DOM、无 fetch ⇒ Node 里 node tests/verdicts.test.mjs 可真求值）
//
// 为什么新开 web/js/ 而不是直接改 web/verdicts_core.js：
//   667 把 core 放在 web/ 根（web/verdicts_core.js），670c 的约定是**新纯逻辑进 web/js/**。
//   本文件 = 670c 新增逻辑 + 对 667 既有逻辑的 export *，于是上层只需要认识一个模块：
//     web/verdicts.js        → import './js/verdicts_core.js'
//     web/tests/verdicts.test.mjs → import '../js/verdicts_core.js'
//   667 的原文件**零改动**（670c A4 的允许清单里没有它，红线：只动清单内文件）。
//
// 纪律：
//   ① **不写死任何数字** —— 全部来自 web/data/verdicts_667.json / status.json / metrics_666.json
//      与 data/baseline.json；
//   ② **缺字段不猜** —— 拿不到就记进 issues 并保留 null，由渲染层显示占位（不许用 0 冒充）；
//   ③ **口径差（caliber / frozen）不做红绿判定** —— 两个分母都合法，一律标红会变成狼来了；
//   ④ 纯函数：同样输入永远同样输出，排序稳定（同值按 seq 再按 id）。

import { fmtNum } from '../verdicts_core.js';
export * from '../verdicts_core.js';

/* ══════════════════════════════════════════════════════════════════
   0 · 常量与四态口径
   ══════════════════════════════════════════════════════════════════ */

/** 四态固定顺序：**显示顺序与计数顺序共用这一张表**，避免两处口径漂移。 */
export const FOUR_STATES = ['pass', 'pass_with_exception', 'fail', 'unknown'];

export const STATE_ZH = {
  pass: '通过',
  pass_with_exception: '带例外通过',
  fail: '未通过',
  unknown: '未知',
};

/** 四态 → 设计令牌变量（**不写死颜色**，改主题只改 design-tokens.css）。 */
export const STATE_VAR = {
  pass: 'var(--color-pass)',
  pass_with_exception: 'var(--color-pass-exception)',
  fail: 'var(--color-fail)',
  unknown: 'var(--color-unknown)',
};

/**
 * data-state 属性有两张互不相同的表，**别混**：
 *   时间线 .tl-item[data-state]  → 669c.css 用连字符 pass-exception
 *   徽章   .state-pill[data-state] → style.css 用下划线 pass_with_exception
 */
export const TL_STATE_ATTR = {
  pass: 'pass', pass_with_exception: 'pass-exception', fail: 'fail', unknown: 'unknown',
};
export const PILL_STATE_ATTR = {
  pass: 'pass', pass_with_exception: 'pass_with_exception', fail: 'fail', unknown: 'unknown',
};

/** 取 data-state 值；未知四态一律降级成 unknown（不是抛异常、也不是原样透传）。 */
export function stateAttr(state, kind = 'timeline') {
  const table = kind === 'pill' ? PILL_STATE_ATTR : TL_STATE_ATTR;
  return table[state] || table.unknown;
}

/* ── 取值小工具：**null 就是 null**，不用 0/'' 冒充 ── */
const isObj = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);
const str = (v) => (v === null || v === undefined ? '' : String(v));
const pick = (...vs) => vs.find((v) => v !== undefined && v !== null) ?? null;

/** 宽松数值：'87.5' → 87.5；''/null/true/NaN → null。 */
export function num(v) {
  if (v === null || v === undefined || v === '' || typeof v === 'boolean') return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

/** 四态归一：不是四态之一（含缺失）→ unknown，并保留原值供渲染层显示。 */
export function normalizeState(v) {
  return FOUR_STATES.includes(v) ? v : 'unknown';
}

export function zeroCounts() {
  return { pass: 0, pass_with_exception: 0, fail: 0, unknown: 0 };
}

/** 四态计数：非数组/坏行都不抛，只当 unknown 计（降级而非崩溃）。 */
export function countStates(rows) {
  const c = zeroCounts();
  for (const r of (Array.isArray(rows) ? rows : [])) c[normalizeState(r && r.state)] += 1;
  return c;
}

export function pct(part, whole) {
  const p = num(part), w = num(whole);
  if (p === null || w === null || w === 0) return null;
  return (p / w) * 100;
}

/** 'YYYY-MM-DD[...]' → UTC 毫秒；非法日期（含 2026-02-31 这类被 Date 归一化的）→ null。 */
const DATE_RE = /^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2}))?)?/;
export function toEpoch(when) {
  const s = str(when).trim();
  const m = DATE_RE.exec(s);
  if (!m) return null;
  const y = Number(m[1]), mo = Number(m[2]), d = Number(m[3]);
  const hh = Number(m[4] ?? 0), mi = Number(m[5] ?? 0), ss = Number(m[6] ?? 0);
  const t = Date.UTC(y, mo - 1, d, hh, mi, ss);
  if (!Number.isFinite(t)) return null;
  const back = new Date(t);
  // Date.UTC 会把 2026-02-31 悄悄滚成 3 月 3 日 —— 那不是"合法日期"，必须判 null
  if (back.getUTCFullYear() !== y || back.getUTCMonth() !== mo - 1 || back.getUTCDate() !== d) return null;
  return t;
}

/** 批次号：'ig_cards_665' → '665'；取不到三位数就退回来源串本身。 */
export function batchOf(source) {
  const s = str(source);
  if (!s) return '未标注';
  const m = /(\d{3})/.exec(s);
  return m ? m[1] : s;
}

/** 入参兼容：数组 / parseVerdicts 结果 / buildTimeline 结果 / verdicts_667.json 原样。 */
function asRows(x) {
  if (Array.isArray(x)) return x.filter(isObj);
  if (isObj(x)) {
    for (const k of ['rows', 'items', 'verdicts']) {
      if (Array.isArray(x[k])) return x[k].filter(isObj);
    }
  }
  return [];
}

/* ══════════════════════════════════════════════════════════════════
   1 · parseVerdicts —— 判决 JSON → 时间线数据
   ══════════════════════════════════════════════════════════════════ */

/**
 * 规范化判决集合。**不做排序**（排序是 buildTimeline 的事），保持输入顺序并记下 index。
 * 返回 { rows, total, declared_total, counts, by_source, dates, batches, issues, ok }。
 * 任何缺字段/坏字段都进 issues，**绝不静默补齐**。
 */
export function parseVerdicts(json) {
  const issues = [];
  let raw = [];
  let declaredTotal = null;

  if (Array.isArray(json)) {
    raw = json;
  } else if (isObj(json)) {
    declaredTotal = num(json.verdicts_total);
    if (Array.isArray(json.verdicts)) raw = json.verdicts;
    else issues.push({ code: 'no-verdicts-array', msg: '输入对象里没有 verdicts 数组（数据源未生成？）' });
    if (declaredTotal !== null && declaredTotal !== raw.length) {
      issues.push({
        code: 'total-mismatch',
        msg: 'verdicts_total=' + declaredTotal + ' 与实测条数 ' + raw.length + ' 不一致（落盘与现读不同步）',
      });
    }
  } else {
    issues.push({ code: 'bad-input', msg: '输入既不是数组也不是对象（undefined/null/标量）' });
  }

  const rows = raw.map((r, i) => {
    const o = isObj(r) ? r : {};
    if (!isObj(r)) issues.push({ code: 'bad-row', index: i, msg: '第 ' + (i + 1) + ' 条不是对象，已按空记录降级' });
    const id = str(o.id);
    if (!id) issues.push({ code: 'missing-id', index: i, msg: '第 ' + (i + 1) + ' 条缺 id' });
    const stateRaw = str(o.state);
    if (!stateRaw) issues.push({ code: 'missing-state', index: i, msg: (id || '第 ' + (i + 1) + ' 条') + ' 缺 state，已降级为 unknown' });
    else if (!FOUR_STATES.includes(stateRaw)) issues.push({ code: 'bad-state', index: i, msg: (id || '第 ' + (i + 1) + ' 条') + ' 的 state=' + stateRaw + ' 不是四态，已降级为 unknown' });
    const when = str(o.when);
    const t = toEpoch(when);
    if (t === null) issues.push({ code: 'bad-when', index: i, msg: (id || '第 ' + (i + 1) + ' 条') + ' 的 when=' + (when || '(空)') + ' 不是可用日期，时间线里排到最后' });
    const seq = num(o.seq);

    return {
      id: id || ('(无 id #' + (i + 1) + ')'),
      index: i,
      source: str(o.source),
      source_label: str(o.source_label) || str(o.source) || '未标注来源',
      batch: batchOf(o.source),
      detector: str(o.detector),
      expect: str(o.expect),
      verdict: str(o.verdict),
      detail: str(o.detail),
      repro: str(o.repro),
      when,
      date: t === null ? '' : when.slice(0, 10),
      t,
      seq: seq === null ? i : seq,
      seq_missing: seq === null,
      state: normalizeState(stateRaw),
      state_raw: stateRaw,
      state_label: str(o.state_label) || STATE_ZH[normalizeState(stateRaw)],
    };
  });

  const bySource = {};
  for (const r of rows) {
    const k = r.source || '(未标注)';
    if (!bySource[k]) {
      bySource[k] = { source: k, label: r.source_label, batch: r.batch, total: 0, counts: zeroCounts(), first: null, last: null };
    }
    const b = bySource[k];
    b.total += 1;
    b.counts[r.state] += 1;
    if (r.t !== null) {
      if (b.first === null || r.t < b.first) b.first = r.t;
      if (b.last === null || r.t > b.last) b.last = r.t;
    }
  }

  const dates = [...new Set(rows.map((r) => r.date).filter(Boolean))].sort();
  const sourceList = Object.values(bySource).sort((a, b) => (a.first ?? Infinity) - (b.first ?? Infinity) || a.source.localeCompare(b.source));

  return {
    rows,
    total: rows.length,
    declared_total: declaredTotal,
    counts: countStates(rows),
    by_source: bySource,
    sources: sourceList,
    dates,
    batches: [...new Set(rows.map((r) => r.batch))],
    issues,
    ok: issues.length === 0,
  };
}

/* ══════════════════════════════════════════════════════════════════
   2 · buildTimeline —— 按时间排序 + 四态序列
   ══════════════════════════════════════════════════════════════════ */

/**
 * 时间线。排序键：t ↑（无日期的**永远垫底**，不管 asc/desc）→ seq → id。
 * 输入顺序 ≠ 时间顺序时置 reordered=true（667 的落盘就是这种：夹具 2026-09-28 排在
 * 机器卡 2026-09-29 之后，因为落盘按 seq 而非 when）。
 * 返回 { items, order, counts, transitions, reordered, undated, total, ascending }。
 */
export function buildTimeline(verdicts, opts = {}) {
  const rows = asRows(verdicts);
  const dir = opts.dir === 'desc' ? 'desc' : 'asc';
  const sorted = rows.slice().sort((a, b) => {
    const ta = a.t === null || a.t === undefined ? Infinity : a.t;
    const tb = b.t === null || b.t === undefined ? Infinity : b.t;
    if (ta !== tb) {
      if (ta === Infinity) return 1;      // 无日期垫底（与方向无关：不知道时间的东西不该冒充最新/最旧）
      if (tb === Infinity) return -1;
      return dir === 'asc' ? ta - tb : tb - ta;
    }
    const sa = num(a.seq) ?? 0, sb = num(b.seq) ?? 0;
    if (sa !== sb) return dir === 'asc' ? sa - sb : sb - sa;
    return str(a.id).localeCompare(str(b.id));
  });

  const cum = zeroCounts();
  const items = sorted.map((r, i) => {
    cum[r.state] += 1;
    return {
      ...r,
      i,
      chrono: dir === 'asc' ? i : sorted.length - 1 - i,
      cum: { ...cum },
      cum_total: i + 1,
      cum_pct: pct(cum[r.state], i + 1),
    };
  });

  const asc = rows.slice().sort((a, b) => {
    const ta = a.t ?? Infinity, tb = b.t ?? Infinity;
    if (ta !== tb) return ta - tb;
    return (num(a.seq) ?? 0) - (num(b.seq) ?? 0) || str(a.id).localeCompare(str(b.id));
  });

  let transitions = 0;
  for (let i = 1; i < asc.length; i++) if (asc[i].state !== asc[i - 1].state) transitions += 1;

  return {
    items,
    order: items.map((r) => r.state),
    counts: countStates(items),
    transitions,
    reordered: rows.some((r, i) => sorted[i] && r.id !== sorted[i].id),
    undated: items.filter((r) => r.t === null).length,
    total: items.length,
    ascending: dir === 'asc',
    dir,
  };
}

/* ══════════════════════════════════════════════════════════════════
   3 · fourStateSeries —— 四态随时间的分布变化（分桶）
   ══════════════════════════════════════════════════════════════════ */

export const BUCKETS = [
  { key: 'date', label: '按日期', sub: '每个落盘日期一桶（时间序）' },
  { key: 'source', label: '按来源', sub: '每个产物一桶（按首条时间排）' },
  { key: 'window', label: '按条数窗口', sub: '按时间序每 size 条一桶（等量分箱）' },
];

/**
 * 分桶统计。opts.bucket ∈ {date, source, window}；opts.size 仅 window 用（默认 5）。
 * 返回 { bucket, size, states, buckets[], totals, total, max, dominant, issues }。
 * buckets[i] = { key, label, from, to, total, counts, pct, cum, cum_pct, batches, ids, dominant }
 */
export function fourStateSeries(verdicts, opts = {}) {
  const rows = asRows(verdicts);
  const bucket = BUCKETS.some((b) => b.key === opts.bucket) ? opts.bucket : 'date';
  const size = Math.max(1, Math.trunc(num(opts.size) ?? 5));
  const issues = [];

  // 分桶必须走**时间序**：不然"随时间变化"会变成"随落盘顺序变化"
  const ordered = buildTimeline(rows, { dir: 'asc' }).items;

  let raw = [];
  if (bucket === 'window') {
    for (let i = 0; i < ordered.length; i += size) {
      const slice = ordered.slice(i, i + size);
      raw.push({ key: 'w' + (i / size + 1), label: '第 ' + (i + 1) + '–' + (i + slice.length) + ' 条', items: slice });
    }
  } else {
    const keyOf = bucket === 'date' ? (r) => r.date || '无日期' : (r) => r.source || '未标注';
    const map = new Map();
    for (const r of ordered) {
      const k = keyOf(r);
      if (!map.has(k)) map.set(k, []);
      map.get(k).push(r);
    }
    raw = [...map.entries()].map(([k, items]) => ({ key: k, label: k, items }));
  }

  const cum = zeroCounts();
  const buckets = raw.map((b) => {
    const counts = countStates(b.items);
    for (const s of FOUR_STATES) cum[s] += counts[s];
    const total = b.items.length;
    const p = {};
    for (const s of FOUR_STATES) p[s] = pct(counts[s], total);
    const cumPct = {};
    for (const s of FOUR_STATES) cumPct[s] = pct(cum[s], cum.pass + cum.pass_with_exception + cum.fail + cum.unknown);
    let dominant = FOUR_STATES[0];
    for (const s of FOUR_STATES) if (counts[s] > counts[dominant]) dominant = s;
    return {
      key: b.key,
      label: b.label,
      from: b.items[0] ? b.items[0].date || '' : '',
      to: b.items[b.items.length - 1] ? b.items[b.items.length - 1].date || '' : '',
      total,
      counts,
      pct: p,
      cum: { ...cum },
      cum_pct: cumPct,
      batches: [...new Set(b.items.map((r) => r.batch))],
      ids: b.items.map((r) => r.id),
      dominant,
    };
  });

  if (!rows.length) issues.push({ code: 'empty', msg: '没有判决记录 ⇒ 四态序列为空（不是"四态都是 0"）' });

  const totals = countStates(rows);
  const max = buckets.reduce((m, b) => Math.max(m, b.total), 0);
  let dominant = null;
  for (const s of FOUR_STATES) if (dominant === null || totals[s] > totals[dominant]) dominant = s;

  return { bucket, size, states: FOUR_STATES.slice(), buckets, totals, total: rows.length, max, dominant, issues };
}

/* ══════════════════════════════════════════════════════════════════
   4 · 漂移登记规范化
   ══════════════════════════════════════════════════════════════════ */

const NUM_RE_SRC = '-?\\d+(?:\\.\\d+)?';

/** 文本里的全部数值（**仅用于展示/兜底**；配对另有更严的规则，见 pairNumbers）。 */
export function numbersIn(text) {
  const re = new RegExp(NUM_RE_SRC, 'g');
  const out = [];
  let m;
  const s = str(text);
  while ((m = re.exec(s)) !== null) out.push(Number(m[0]));
  return out;
}

/** 文本里第一个数值（'87.5%（落盘 14/16）' → 87.5）；没有就 null。 */
export function firstNumber(text) {
  const n = numbersIn(text);
  return n.length ? n[0] : null;
}

const AUTHORITATIVE_RE = /以[^，。；;]*?(-?\d+(?:\.\d+)?)\s*为准/;
const PENDING_RE = /(-?\d+(?:\.\d+)?)\s*待权威源/;
// 注意：必须排除「不一致」—— 否则 graph.nodes 那条"…不一致 — 以实测 178 为准，121 待权威源"
// 会被误判成"已裁定"。用负向后行断言卡住「不」字。
const RESOLVED_RE = /无差异|已归档|已裁定|已收敛|统一为|(?<!不)一致/;

/**
 * 「声明值 vs 现算值」的配对规则：**两侧数值个数必须相同**才认为在比同一个量。
 * 这条保守规则是必须的 —— 'P=1.0 R=1.0 F1=1.0' 与 '分母 10 条' 硬配对会得到 +9 这种
 * 纯属虚构的漂移。个数不同就**不猜**：numeric=false 并写明 skip 原因。
 */
export function pairNumbers(left, right) {
  const a = numbersIn(left), b = numbersIn(right);
  if (!a.length || !b.length) return { numeric: false, reason: '两侧至少一侧没有数值' };
  if (a.length !== b.length) {
    return { numeric: false, reason: '两侧数值个数不同（' + a.length + ' vs ' + b.length + '）⇒ 口径不同，不猜测配对' };
  }
  return { numeric: true, stored: a[0], fresh: b[0], all: { left: a, right: b } };
}

/** 缺什么就补什么：把任意形态的条目补成规范化漂移项。 */
function makeDriftItem(o, i) {
  const stored = num(o.stored);
  const fresh = num(o.fresh);
  const numeric = o.numeric === false ? false : (stored !== null && fresh !== null);
  const delta = numeric ? fresh - stored : null;
  const rel = (numeric && stored !== 0) ? (delta / Math.abs(stored)) * 100 : null;
  return {
    id: str(o.id) || ('drift-' + (i + 1)),
    field: str(o.field) || ('#' + (i + 1)),
    label: str(o.label) || str(o.field) || ('#' + (i + 1)),
    kind: str(o.kind) || 'drift',
    note: str(o.note),
    text: str(o.text),
    source: str(o.source),
    stored,
    fresh,
    stored_raw: pick(o.stored_raw, o.stored),
    fresh_raw: pick(o.fresh_raw, o.fresh),
    numeric,
    skip_reason: str(o.skip_reason),
    delta,
    rel_pct: rel,
    dir: delta === null ? null : (delta > 0 ? 'up' : delta < 0 ? 'down' : 'flat'),
    neg: delta !== null && delta < 0,
    pending: num(o.pending),
    authoritative: num(o.authoritative),
    resolved: !!o.resolved,
    numbers: Array.isArray(o.numbers) ? o.numbers.slice() : numbersIn(o.text),
  };
}

/** 数组里的原始条目 → 规范化漂移项（已经是规范化的就原样通过）。 */
export function normalizeDrift(list) {
  if (!Array.isArray(list)) return [];
  return list.map((raw, i) => {
    if (isObj(raw) && typeof raw.numeric === 'boolean' && 'delta' in raw) return raw;   // 已规范化
    if (!isObj(raw)) {
      // ③ 纯文本：'field: 文本'
      const s = str(raw);
      const m = /^([^:：]{1,48})[:：]\s*(.+)$/.exec(s);
      const field = m ? m[1] : ('#' + (i + 1));
      const text = m ? m[2] : s;
      const pending = num((PENDING_RE.exec(text) || [])[1]);
      const authoritative = num((AUTHORITATIVE_RE.exec(text) || [])[1]);
      return makeDriftItem({
        field, text, note: text, kind: 'tolerated', source: '文本登记',
        stored: pending, fresh: authoritative,
        pending, authoritative, resolved: RESOLVED_RE.test(text), numbers: numbersIn(text),
      }, i);
    }
    // ① 结构化：{ field, stored, fresh, note } / { declared, computed }
    if ('stored' in raw || 'fresh' in raw || 'declared' in raw || 'computed' in raw) {
      return makeDriftItem({
        ...raw,
        stored: pick(raw.stored, raw.declared, raw.from),
        fresh: pick(raw.fresh, raw.computed, raw.to),
        text: str(raw.text) || str(raw.note),
      }, i);
    }
    // ② compare 行：{ metric, left, right, kind, note }
    const paired = pairNumbers(raw.left, raw.right);
    return makeDriftItem({
      id: 'cmp-' + (i + 1),
      field: str(raw.metric) || ('#' + (i + 1)),
      label: str(raw.metric) || ('#' + (i + 1)),
      kind: str(raw.kind) || 'caliber',
      note: str(raw.note),
      text: str(raw.left) + '  ⟷  ' + str(raw.right),
      source: 'compare 行',
      stored_raw: pick(raw.left), fresh_raw: pick(raw.right),
      stored: paired.numeric ? paired.stored : null,
      fresh: paired.numeric ? paired.fresh : null,
      numeric: paired.numeric,
      skip_reason: paired.reason || '',
      numbers: numbersIn(str(raw.left) + ' ' + str(raw.right)),
    }, i);
  });
}

/**
 * 漂移登记规范化。认得：
 *   ① { drift: [{ field, stored, fresh, note }] }   —— web/data/verdicts_667.json
 *   ② { compare: [{ metric, left, right, kind, note }] }
 *   ③ { tolerated_discrepancies: ['field: 文本', ...] } —— data/baseline.json（**仓库根**，
 *      静态站以 web/ 为根时取不到 ⇒ 渲染层优雅降级，见 verdicts.js）
 *   ④ 裸数组 / 单条 { field, stored, fresh }
 * 返回 { items, total, numeric, text_only, tolerated, issues, sources }。
 */
export function parseDrift(input, opts = {}) {
  const items = [];
  const issues = [];
  const sources = [];

  if (Array.isArray(input)) {
    if (!input.length) issues.push({ code: 'empty-registry', msg: '漂移登记是空数组 ⇒ 本批无可登记的漂移' });
    items.push(...normalizeDrift(input));
    sources.push('数组入参');
  } else if (isObj(input)) {
    if (Array.isArray(input.drift)) {
      sources.push('drift[]');
      items.push(...normalizeDrift(input.drift.map((d) => ({ ...d, kind: str(d.kind) || 'drift', source: 'drift 登记' }))));
    }
    if (Array.isArray(input.compare)) {
      sources.push('compare[]');
      items.push(...normalizeDrift(input.compare));
    }
    if (Array.isArray(input.tolerated_discrepancies)) {
      sources.push('tolerated_discrepancies[]');
      items.push(...normalizeDrift(input.tolerated_discrepancies.map((t) => String(t))));
    }
    for (const k of ['drifts', 'deltas', 'discrepancies', 'baseline_drift']) {
      if (Array.isArray(input[k])) {
        sources.push(k + '[]');
        items.push(...normalizeDrift(input[k].map((d) => ({ ...d, kind: str(d.kind) || 'drift' }))));
      }
    }
    if ('field' in input || 'key' in input) {
      sources.push('单条');
      items.push(...normalizeDrift([input]));
    }
    if (!sources.length) {
      issues.push({ code: 'no-registry', msg: '输入对象里没有 drift / compare / tolerated_discrepancies 任何一张登记表' });
    }
  } else {
    issues.push({ code: 'bad-input', msg: '漂移登记入参既不是数组也不是对象（未加载？）' });
  }

  // 去重：同一 field 只留一条（先到先得），避免 drift[] 与 compare[] 重复登记同一量
  const seen = new Set();
  const uniq = [];
  for (const it of items) {
    const k = it.field;
    if (seen.has(k)) { issues.push({ code: 'duplicate-field', msg: '重复登记的漂移项：' + k + '（已保留首条）' }); continue; }
    seen.add(k);
    uniq.push(it);
  }

  return {
    items: uniq,
    total: uniq.length,
    numeric: uniq.filter((d) => d.numeric).length,
    text_only: uniq.filter((d) => !d.numeric).length,
    tolerated: uniq.filter((d) => d.resolved).length,
    sources: [...new Set(sources)],
    issues: [...issues, ...(opts.issues || [])],
    source_url: str(opts.source),
  };
}

/* ══════════════════════════════════════════════════════════════════
   5 · driftBars —— 漂移幅度条（含正负）
   ══════════════════════════════════════════════════════════════════ */

function inferDigits(...vs) {
  const ns = vs.filter((v) => typeof v === 'number' && Number.isFinite(v));
  if (!ns.length) return 0;
  return ns.some((n) => !Number.isInteger(n)) ? 2 : 0;
}

/**
 * 幅度条几何：轨道宽 100%，**中点 50% 为零**，正向右、负向左（对齐 669c.css
 * 的 .drift-fill{left:50%} + .is-neg）。opts.scale 可固定量程，默认取最大 |delta|。
 * 返回 { bars, max, scale, total, numeric, text_only }。
 */
export function driftBars(drift, opts = {}) {
  let items;
  if (Array.isArray(drift)) items = normalizeDrift(drift);
  else if (isObj(drift) && Array.isArray(drift.items)) items = drift.items;
  else if (isObj(drift)) items = parseDrift(drift).items;
  else items = [];

  const numericItems = items.filter((d) => d.numeric && typeof d.delta === 'number');
  const max = numericItems.reduce((m, d) => Math.max(m, Math.abs(d.delta)), 0);
  const scale = num(opts.scale) ?? max;

  const bars = items.map((d) => {
    const digits = num(opts.digits) ?? inferDigits(d.stored, d.fresh, d.delta);
    const widthPct = (d.numeric && scale > 0) ? Math.min(50, (Math.abs(d.delta) / scale) * 50) : 0;
    const neg = !!d.neg;
    const leftPct = neg ? 50 - widthPct : 50;
    const sign = d.delta > 0 ? '+' : '';
    return {
      ...d,
      digits,
      width_pct: widthPct,
      left_pct: leftPct,
      right_pct: leftPct + widthPct,
      flat: d.numeric && d.delta === 0,
      cls: neg ? 'is-neg' : '',
      val_text: d.numeric ? sign + fmtNum(d.delta, digits) : '—',
      rel_text: d.rel_pct === null || d.rel_pct === undefined ? '—' : (d.rel_pct > 0 ? '+' : '') + fmtNum(d.rel_pct, 1) + '%',
      stored_text: d.stored === null ? '—' : fmtNum(d.stored, digits),
      fresh_text: d.fresh === null ? '—' : fmtNum(d.fresh, digits),
      style: 'left:' + leftPct.toFixed(4) + '%;width:' + widthPct.toFixed(4) + '%',
    };
  });

  return {
    bars,
    total: bars.length,
    numeric: bars.filter((b) => b.numeric).length,
    text_only: bars.filter((b) => !b.numeric).length,
    positive: bars.filter((b) => b.numeric && b.delta > 0).length,
    negative: bars.filter((b) => b.numeric && b.delta < 0).length,
    flat_count: bars.filter((b) => b.flat).length,
    max,
    scale,
  };
}

/* ══════════════════════════════════════════════════════════════════
   6 · buildDiffRows —— 声明值 vs 现算值 vs 差异
   ══════════════════════════════════════════════════════════════════ */

export const DEFAULT_TOLERANCE = { abs: 0, rel: 0 };

/** 容差上限：max(abs, rel × |声明值|)。**声明值缺失时只用 abs**（没有基准就谈不上相对误差）。 */
export function toleranceLimit(declared, tol) {
  const t = { ...DEFAULT_TOLERANCE, ...(tol || {}) };
  const abs = num(t.abs) ?? 0;
  const rel = num(t.rel) ?? 0;
  const base = typeof declared === 'number' && Number.isFinite(declared) ? Math.abs(declared) : 0;
  return Math.max(abs, rel * base);
}

function toMetricMap(x) {
  const out = {};
  if (!isObj(x)) return out;
  for (const [k, v] of Object.entries(x)) {
    if (isObj(v) && 'value' in v) out[k] = { value: num(v.value), source: str(v.source), raw: v.value };
    else out[k] = { value: num(v), source: '', raw: v };
  }
  return out;
}

/**
 * 差异行。判定式：**|差异| > max(absTol, relTol×|声明值|)** ⇒ is-mismatch。
 * 恰好等于容差**不算**不一致（边界取严：容差是"允许的上界"）。
 * kind !== 'exact' 的行（caliber/frozen/drift）**永不算 mismatch**，只标 is-caliber。
 */
export function buildDiffRows(declared, computed, opts = {}) {
  const dMap = toMetricMap(declared);
  const cMap = toMetricMap(computed);
  const specs = Array.isArray(opts.specs) ? opts.specs.slice() : [];
  const known = new Set(specs.map((s) => s.key));
  const issues = [];
  for (const k of [...new Set([...Object.keys(dMap), ...Object.keys(cMap)])].sort()) {
    if (!known.has(k)) { specs.push({ key: k, label: k }); issues.push({ code: 'auto-spec', msg: '指标 ' + k + ' 没有声明口径，按精确比对（容差 0）兜底' }); }
  }

  const rows = specs.map((sp) => {
    const d = dMap[sp.key] || null;
    const c = cMap[sp.key] || null;
    const dv = d ? d.value : null;
    const cv = c ? c.value : null;
    const missing = dv === null && cv === null ? 'both' : dv === null ? 'declared' : cv === null ? 'computed' : null;
    const numeric = missing === null;
    const diff = numeric ? cv - dv : null;
    const rel = (numeric && dv !== 0) ? (diff / Math.abs(dv)) * 100 : null;
    const tol = { ...DEFAULT_TOLERANCE, ...(sp.tol || sp.tolerance || {}) };
    const limit = numeric ? toleranceLimit(dv, tol) : null;
    const within = numeric ? Math.abs(diff) <= limit : null;
    const kind = sp.kind || 'exact';
    const isMismatch = numeric && kind === 'exact' && within === false;
    const digits = num(sp.digits) ?? inferDigits(dv, cv, diff);

    return {
      key: sp.key,
      label: sp.label || sp.key,
      unit: sp.unit || '',
      digits,
      kind,
      note: sp.note || '',
      declared: dv, computed: cv,
      declared_text: dv === null ? '—' : fmtNum(dv, digits) + (sp.unit || ''),
      computed_text: cv === null ? '—' : fmtNum(cv, digits) + (sp.unit || ''),
      declared_source: d ? d.source : '',
      computed_source: c ? c.source : '',
      missing,
      numeric,
      diff,
      rel_pct: rel,
      tolerance: tol,
      limit,
      within_tolerance: within,
      isMismatch,
      mismatch: isMismatch,
      // 非 exact 的口径（caliber/frozen）单独给类名，**不借 is-match 的绿** —— 绿会读成"已核对无误"
      rowClass: missing ? 'is-partial' : isMismatch ? 'is-mismatch' : (kind === 'exact' ? 'is-match' : 'is-' + kind),
      diff_text: diff === null ? '—' : (diff > 0 ? '+' : '') + fmtNum(diff, digits) + (sp.unit || ''),
      rel_text: rel === null ? '—' : (rel > 0 ? '+' : '') + fmtNum(rel, 1) + '%',
      limit_text: limit === null ? '—' : '≤ ' + fmtNum(limit, Math.max(digits, 4)),
      verdict_text: missing
        ? (missing === 'both' ? '两侧都没有值' : (missing === 'declared' ? '无声明值可比（缺口）' : '无现算值可比（缺口）'))
        : isMismatch ? '不一致（超容差）' : (kind === 'exact' ? '一致（在容差内）' : '口径差（不判红绿）'),
    };
  });

  return {
    rows,
    specs,
    total: rows.length,
    mismatches: rows.filter((r) => r.isMismatch).length,
    matches: rows.filter((r) => r.rowClass === 'is-match').length,
    partial: rows.filter((r) => r.missing).length,
    caliber: rows.filter((r) => r.rowClass === 'is-caliber').length,
    frozen: rows.filter((r) => r.rowClass === 'is-frozen').length,
    red_keys: rows.filter((r) => r.isMismatch).map((r) => r.key),
    issues,
  };
}

/* ══════════════════════════════════════════════════════════════════
   7 · buildCompareModel —— 真实数据源的比对模型（声明 vs 现算）
   ══════════════════════════════════════════════════════════════════ */

export const SOURCE_URLS = {
  verdicts: 'data/verdicts_667.json',
  status: 'data/status.json',
  metrics: 'data/metrics_666.json',
  baseline: 'data/baseline.json',
  parsed: 'data/verdicts_667.json',
};

/**
 * 指标口径表。d/c 是 '来源.路径' —— 第一个点前是数据源名，其余交给 dig。
 * tol 只写**有依据**的容差：整数计数 0；率值按落盘小数位（1 位 → 0.05，4 位 → 0.00005）。
 * kind='caliber' 表示两个口径都合法，**不判红绿**。
 */
export const COMPARE_SPECS = [
  { key: 'holdout_rate_pct', label: 'holdout 检出率', unit: '%', digits: 1, tol: { abs: 0.05 }, note: 'catch+miss 口径；unknown 不计入分母', d: 'metrics.metrics.holdout.rate_pct', c: 'verdicts.dashboard.holdout.rate_pct' },
  { key: 'holdout_catch', label: 'holdout 检出数', digits: 0, note: '现算 catch', d: 'metrics.metrics.holdout.catch', c: 'verdicts.dashboard.holdout.catch' },
  { key: 'holdout_miss', label: 'holdout 漏检数', digits: 0, note: '现算 miss', d: 'metrics.metrics.holdout.miss', c: 'verdicts.dashboard.holdout.miss' },
  { key: 'holdout_unknown', label: 'holdout 未知数', digits: 0, note: '检测器不可用 ⇒ 不进分母', d: 'metrics.metrics.holdout.unknown', c: 'verdicts.dashboard.holdout.unknown' },
  { key: 'holdout_den', label: 'holdout 分母', digits: 0, note: 'catch+miss', d: 'metrics.metrics.holdout.den', c: 'verdicts.dashboard.holdout.den' },
  // 672g：说明文字**不再写死数字** —— 672f 扩样后"已跑 17"变成 22，而这行 note 是给用户看的
  //   静态串，写死就会静默过期（左边一列显示新值、说明还念旧值）。数字以左右两列为准。
  { key: 'holdout_pool', label: 'holdout 池规模', digits: 0, kind: 'caliber', note: 'baseline 记的是**盲态池规模**；判决页的 samples 是**已 reveal 并跑过的条数**。两个都对，不是漂移 —— 具体数字见左右两列。', d: 'baseline.holdout.count', c: 'verdicts.dashboard.holdout.samples' },
  { key: 'external_rate_pct', label: '外部语料检出率', unit: '%', digits: 1, tol: { abs: 0.05 }, note: 'catch+miss 口径', d: 'metrics.metrics.external.rate_pct', c: 'verdicts.dashboard.external.rate_pct' },
  { key: 'external_rate_all_pct', label: '外部语料检出率（全样本）', unit: '%', digits: 1, tol: { abs: 0.05 }, note: '分母 = 全部 40 条；与上一行**必须一起看**', d: 'metrics.metrics.external.rate_pct_all', c: 'verdicts.dashboard.external.rate_pct_all' },
  { key: 'external_den', label: '外部语料分母', digits: 0, note: 'catch+miss', d: 'metrics.metrics.external.den', c: 'verdicts.dashboard.external.den' },
  { key: 'external_total', label: '外部语料样本数', digits: 0, note: '含 unknown 与 not_error', d: 'metrics.metrics.external.total', c: 'verdicts.dashboard.external.total' },
  { key: 'cards_real', label: '实卡数（666 落盘口径）', digits: 0, note: 'web/data/metrics_666.json 的 cards_real', d: 'metrics.metrics.cards_real', c: 'verdicts.dashboard.cards_real' },
  { key: 'cards_real_status', label: '实卡数（状态页口径）', digits: 0, note: '**两个现算工具对同一个量给出不同值** ⇒ 需人裁决哪个是当前真值', d: 'status.cards.cards_real', c: 'verdicts.dashboard.cards_real' },
  { key: 'cards_total_status', label: '卡总数（状态页口径）', digits: 0, note: 'status 的 47 = 实卡 37 + 草稿 10；判决页的 52 = 42 + 10', d: 'status.cards.cards_total', c: 'verdicts.dashboard.cards_total' },
  { key: 'cards_draft', label: '草稿卡数', digits: 0, note: '两侧一致', d: 'metrics.metrics.cards_draft', c: 'verdicts.dashboard.cards_draft' },
  { key: 'rules_total', label: '判决规则数', digits: 0, note: 'gate_engine 执行权威', d: 'metrics.metrics.rules_total', c: 'verdicts.dashboard.rules_total' },
  { key: 'rules_total_status', label: '判决规则数（状态页口径）', digits: 0, note: 'status.json 独立现算的交叉校验', d: 'status.rules.rules_total', c: 'verdicts.dashboard.rules_total' },
  { key: 'rules_documented', label: '规则清单条目数', digits: 0, note: 'baseline 的 documented_brief', d: 'baseline.rules.documented_brief', c: 'verdicts.dashboard.rules_total' },
  { key: 'ledger_events', label: '账本事件数', digits: 0, note: '452 冻结（红线：零改）', d: 'metrics.metrics.ledger_events', c: 'verdicts.dashboard.ledger_events' },
  { key: 'escape_rate_pct', label: '逃逸率（冻结契约）', unit: '%', digits: 4, tol: { abs: 0.00005 }, kind: 'frozen', note: '616 冻结；**不是**真实错误率，不可与检出率并列', d: 'status.escape.rate_pct', c: 'verdicts.dashboard.escape.rate_pct' },
  { key: 'escape_den', label: '逃逸率分母', digits: 0, kind: 'frozen', note: 'variants − n_a − equivalent', d: 'status.escape.denominator', c: 'verdicts.dashboard.escape.denominator' },
  { key: 'escape_variants', label: '变异体总数', digits: 0, kind: 'frozen', note: '两侧一致', d: 'status.escape.variants', c: 'verdicts.dashboard.escape.variants' },
  { key: 'protectors', label: '保护器数', digits: 0, note: '镜像自拆仓 queyi-core', d: 'status.protectors.protectors_total', c: 'verdicts.dashboard.protectors' },
  { key: 'mutation_core', label: '变异杀伤率 core（on_scored）', unit: '%', digits: 1, tol: { abs: 0.05 }, note: '内部自证指标，**不作缺陷检测率**', d: 'baseline.mutation.core_kill_rate_pct', c: 'verdicts.dashboard.mutation.core' },
  { key: 'mutation_all', label: '变异杀伤率 all（on_scored）', unit: '%', digits: 1, tol: { abs: 0.05 }, note: '内部自证指标，**不作缺陷检测率**', d: 'baseline.mutation.all_kill_rate_pct', c: 'verdicts.dashboard.mutation.all' },
  { key: 'atoms_md_files', label: 'atoms md 文件数', digits: 0, note: '含 README ⇒ 比卡数多 1', d: 'baseline.cards.atoms_total', c: 'verdicts.dashboard.atoms_md_files' },
  { key: 'counterfactual_cases', label: '反事实案例数（带真值标签）', digits: 0, note: '判决页产物里**没有**逐条反事实 ⇒ 现算侧缺口', d: 'metrics.metrics.counterfactual.cases', c: null },
  { key: 'graph_nodes', label: '图谱节点数', digits: 0, note: '判决页产物不含图谱 ⇒ 现算侧缺口；baseline 记 178（README 的 121 已被裁定作废）', d: 'baseline.graph.nodes', c: null },
  { key: 'verdict_page_total', label: '判决历史总条数', digits: 0, note: '现算 = 解析后的条数；**没有任何落盘文件声明过这个量** ⇒ 声明侧缺口（诚实登记）', d: null, c: 'parsed.total' },
  { key: 'defects_total', label: '缺陷夹具判决数', digits: 0, note: '现算 = defect_injection_661 的逐条数；声明侧无对应产物', d: null, c: 'parsed.by_source.defect_injection_661.total' },
  { key: 'ig_pass', label: '机器卡 pass 数', digits: 0, note: 'status 的 four_state_dist 与逐条解析交叉校验', d: 'status.ig_cards_665.four_state_dist.pass', c: 'parsed.by_source.ig_cards_665.counts.pass' },
  { key: 'ig_unknown', label: '机器卡 unknown 数', digits: 0, note: 'cross-compile 探针未呈现 ⇒ unknown', d: 'status.ig_cards_665.four_state_dist.unknown', c: 'parsed.by_source.ig_cards_665.counts.unknown' },
  { key: 'ig_total', label: '机器卡条数', digits: 0, note: '16 条逐条结果', d: 'status.ig_cards_665.total', c: 'parsed.by_source.ig_cards_665.total' },
];

function dig(o, path) {
  let cur = o;
  for (const k of str(path).split('.')) {
    if (cur === null || cur === undefined) return undefined;
    cur = cur[k];
  }
  return cur;
}

/** 'metrics.metrics.cards_real' → sources.metrics 里 dig('metrics.cards_real') */
function resolvePath(sources, path) {
  if (!path) return { value: undefined, bag: null };
  const i = path.indexOf('.');
  const head = i < 0 ? path : path.slice(0, i);
  const rest = i < 0 ? '' : path.slice(i + 1);
  const bag = sources ? sources[head] : null;
  if (!bag) return { value: undefined, bag: head };
  return { value: rest ? dig(bag, rest) : bag, bag: head };
}

/**
 * 真实数据 → 比对模型。sources = { verdicts, status, metrics, baseline, parsed }；
 * 任何一项缺失都只是"这一侧没值"，**不抛异常**，并记进 issues。
 */
export function buildCompareModel(sources = {}) {
  const src = sources || {};
  const available = {
    verdicts: !!src.verdicts,
    status: !!src.status,
    metrics: !!src.metrics,
    baseline: !!src.baseline,
    parsed: !!src.parsed,
  };
  const issues = [];
  const declared = {};
  const computed = {};

  for (const sp of COMPARE_SPECS) {
    const d = resolvePath(src, sp.d);
    const c = resolvePath(src, sp.c);
    const dv = num(d.value);
    const cv = num(c.value);
    if (sp.d && dv === null) issues.push({ code: 'declared-missing', key: sp.key, msg: sp.key + ' 的声明值取不到（' + sp.d + '）' + (d.bag && !available[d.bag] ? '：数据源 ' + d.bag + ' 未加载' : '') });
    if (sp.c && cv === null) issues.push({ code: 'computed-missing', key: sp.key, msg: sp.key + ' 的现算值取不到（' + sp.c + '）' + (c.bag && !available[c.bag] ? '：数据源 ' + c.bag + ' 未加载' : '') });
    if (dv !== null) declared[sp.key] = { value: dv, source: SOURCE_URLS[d.bag] || d.bag || '—' };
    if (cv !== null) computed[sp.key] = { value: cv, source: SOURCE_URLS[c.bag] || c.bag || '—' };
  }

  const model = buildDiffRows(declared, computed, { specs: COMPARE_SPECS });

  return {
    ...model,
    declared,
    computed,
    available,
    issues: [...issues, ...model.issues],
    sources: Object.entries(SOURCE_URLS).filter(([k]) => available[k]).map(([, v]) => v).filter((v, i, a) => a.indexOf(v) === i),
  };
}

/* ══════════════════════════════════════════════════════════════════
   8 · layoutStacked —— 堆叠柱 + 折线的纯几何（渲染层只拼 SVG）
   ══════════════════════════════════════════════════════════════════ */

/**
 * 四态堆叠柱几何。每个桶一根柱，段高 = 桶高 × 该态占比；
 * **最后一段吸收浮点误差** ⇒ Σ段高 == 柱高（可断言）。
 * 折线 = 每桶 pass 占比（趋势），点 x 取柱中心。
 */
export function layoutStacked(series, opts = {}) {
  const w = num(opts.width) ?? 720;
  const h = num(opts.height) ?? 200;
  const pad = { l: 36, r: 14, t: 12, b: 36, ...(opts.pad || {}) };
  const buckets = (series && Array.isArray(series.buckets)) ? series.buckets : [];
  const states = (series && Array.isArray(series.states) && series.states.length) ? series.states : FOUR_STATES.slice();
  const plotW = Math.max(0, w - pad.l - pad.r);
  const plotH = Math.max(0, h - pad.t - pad.b);
  const max = Math.max(1, ...buckets.map((b) => num(b.total) ?? 0));
  const n = buckets.length;
  const step = n ? plotW / n : plotW;
  const barW = Math.max(2, Math.min(48, step * 0.62));

  const bands = buckets.map((b, i) => {
    const x = pad.l + step * i + (step - barW) / 2;
    const total = num(b.total) ?? 0;
    const full = plotH * (total / max);
    let used = 0;
    const segs = states.map((s, k) => {
      const v = num(b.counts && b.counts[s]) ?? 0;
      const raw = total > 0 ? full * (v / total) : 0;
      const hh = k === states.length - 1 ? Math.max(0, full - used) : raw;
      const y = pad.t + plotH - used - hh;
      used += hh;
      const seg = { state: s, value: v, x, y, w: barW, h: hh, total, pct: pct(v, total) };
      return seg;
    });
    return { key: b.key, label: b.label, x, w: barW, total, full, y: pad.t + plotH - full, segs, dominant: b.dominant };
  });

  const line = buckets.map((b, i) => {
    const p = pct((b.counts && b.counts.pass) ?? 0, b.total);
    return {
      x: pad.l + step * i + step / 2,
      pct: p,
      y: p === null ? null : pad.t + plotH - plotH * (p / 100),
      key: b.key,
    };
  });

  const ticks = Math.min(4, max);
  const grid = Array.from({ length: ticks + 1 }, (_, i) => {
    const v = (max / ticks) * i;
    return { value: v, y: pad.t + plotH - plotH * (i / ticks), label: String(Math.round(v)) };
  });

  return {
    width: w, height: h, pad, plotW, plotH, max, step, bar_width: barW,
    bands, line, grid,
    x_ticks: buckets.map((b, i) => ({ x: pad.l + step * i + step / 2, label: String(b.label), key: b.key })),
    states,
    total: buckets.reduce((s, b) => s + (num(b.total) ?? 0), 0),
  };
}

/** 折线 path（跳过 y=null 的点）；给渲染层直接用，纯字符串。 */
export function linePath(points) {
  const pts = (Array.isArray(points) ? points : []).filter((p) => p && typeof p.y === 'number');
  if (pts.length < 2) return pts.length === 1 ? ('M' + pts[0].x.toFixed(2) + ' ' + pts[0].y.toFixed(2)) : '';
  return pts.map((p, i) => (i ? 'L' : 'M') + p.x.toFixed(2) + ' ' + p.y.toFixed(2)).join(' ');
}
