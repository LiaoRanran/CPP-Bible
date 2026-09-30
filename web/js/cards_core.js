// ═══════════════════════════════════════════════════════════════════════════
// 670c A3 · 卡库页纯逻辑核心（无 DOM / 无 fetch ⇒ 可在 Node 里直接真跑）
//
// 本模块只"算"不"渲染"：cards.js 负责 DOM/SVG/交互，cards.test.mjs 拿真实算法结果对账。
// 数据由页面注入（本模块不自己取数）：
//   · web/data/cards_index.json —— 台账索引（id/标题/域/型/status/四态/证据 id/先修）
//   · web/data/cards.json       —— 全卡（claim/命题/边界/证据明细），供证据链与边界对比
//
// 【筛选语义 · 必须与 cards.test.mjs 一致】
//   · 维度内 OR：同一维度多选值之间取并集（四态选 pass+unknown ⇒ 命中任一即通过）
//   · 维度间 AND：不同维度取交集（全文 ∩ 四态 ∩ 域 ∩ 标准 ∩ 强度 ∩ 范围 ∩ 状态 ∩ 类型）
//   · 空数组 / 缺字段 = 该维度**不约束**（≠"匹配空值"）
//   · scope 特殊：'real' 只看非草稿 · 'draft' 只看草稿 · 'all' 全看
//   · cpp_standard：卡的任一标准 ∈ 所选集合即命中；NO_STANDARD('（未声明）') 命中"没声明标准"的卡
//   · strength：卡的证据强度 key ∈ 所选集合
//   · 全文：大小写不敏感；空白切词后 **多词 AND**（所有词都出现在搜索文本里才命中）
//
// 【方向约定 · 关系图】edges 一律 **前置 → 依赖它的卡**（箭头指向"用到它的人"）。
// 【证据链层级】card → evidence(证据 id) → file(证据文件) → sanitizer(工具输出)。
//   sanitizer 输出**只照抄台账字段**：台账没记 ⇒ 'unrecorded'，证据未入库 ⇒ 'unknown'，绝不编造。
// ═══════════════════════════════════════════════════════════════════════════

/** 四态展示顺序（与 cards.js 的既有口径一致；'' = 台账未声明） */
export const STATE_ORDER = ['pass', 'pass_with_exception', 'fail', 'unknown', ''];
/** 四态 → 中文标签 */
export const STATE_LABELS = {
  pass: 'pass · 通过',
  pass_with_exception: 'pass_with_exception · 带例外通过',
  fail: 'fail · 不通过',
  unknown: 'unknown · 未知',
  '': '未声明',
};
/** "没有声明 C++ 标准"在标准筛选里的占位值（前端也用它做选项） */
export const NO_STANDARD = '（未声明）';
/** 证据强度四档（level 越大越强） */
export const STRENGTH_LEVELS = [
  { level: 0, key: 'none', label: '无证据' },
  { level: 1, key: 'declared', label: '仅声明（索引里没有对应证据文件）' },
  { level: 2, key: 'present', label: '有证据文件（未全部 confirm）' },
  { level: 3, key: 'confirmed', label: '证据文件齐全且全 confirm' },
];
/** 排序模式（与 cards.html 的 #f-sort 选项一一对应） */
export const SORT_MODES = ['default', 'strength', 'state', 'evidence', 'domain', 'title'];

const isObj = (v) => v !== null && typeof v === 'object';
const str = (v) => (v === null || v === undefined ? '' : String(v));
const arr = (v) => (Array.isArray(v) ? v : v === null || v === undefined || v === '' ? [] : [v]);

/** 去重 + 稳定排序（默认字典序，保证输出确定性） */
export function uniqSorted(list = []) {
  return [...new Set(arr(list).map(str).filter((s) => s !== ''))].sort();
}

// ── 卡字段读取（索引卡 / 全卡两种形状都要认）────────────────────────────────
export const cardId = (c) => str(c?.id);
/**
 * 是否属于 **draft650 草稿批**（台账索引的 draft:true；本仓 10 张）。
 * 注意口径：台账 `status: 'draft'`（本仓 21 张）是**另一个维度**——
 * 它表示"卡自身还没 verified"，不等于 draft650 批；669c 既有 scope 只按 draft650 分域，
 * 本模块沿用同一口径（否则"实卡域"会从 37 张错缩到 26 张）。
 */
export const isDraft = (c) => c?.draft === true;
export function cardTitle(c) {
  return str(c?.title || c?.meta?.title || c?.claim);
}
export function cardClaim(c) {
  return str(c?.claim || c?.title || c?.meta?.title);
}
export function cardDomain(c) {
  return str(c?.domain || c?.meta?.domain);
}
export function cardType(c) {
  return str(c?.type || c?.meta?.type);
}
export function cardStatus(c) {
  return str(c?.status || c?.meta?.status);
}
/** 四态：'' = 台账未声明（**不**替它猜一个态） */
export function cardState(c) {
  const v = c?.verdict_state ?? c?.verdict?.state;
  return v === null || v === undefined ? '' : String(v);
}
export function stateLabel(state) {
  const s = str(state);
  return STATE_LABELS[s] || s || STATE_LABELS[''];
}
/** 卡声明的 C++/C 标准（全卡边界 → 索引兜底） */
export function cardStandards(c) {
  const cb = c?.boundary?.claim_boundary || c?.boundary || {};
  return uniqSorted([
    ...arr(c?.cpp_standard),
    ...arr(c?.standards),
    ...arr(cb?.standard),
    ...arr(c?.meta?.standard),
  ]);
}
/** 证据引用（索引卡是 id 数组；全卡是对象数组） */
export function evidenceRefs(c) {
  const raw = c?.evidence;
  if (Array.isArray(raw)) {
    return raw
      .map((it) => (isObj(it) ? { ...it, id: str(it.id) } : { id: str(it) }))
      .filter((r) => r.id !== '');
  }
  if (isObj(raw)) {
    return Object.entries(raw)
      .map(([id, v]) => ({ ...(isObj(v) ? v : {}), id }))
      .filter((r) => r.id !== '');
  }
  return [];
}
/** 证据 id 列表 */
export function cardEvidenceIds(c) {
  return evidenceRefs(c).map((r) => r.id);
}
/** 先修 id 列表（索引卡 prereqs: string[]；全卡 prerequisites: [{id}]） */
export function cardPrereqIds(c) {
  return uniqSorted([
    ...arr(c?.prereqs),
    ...arr(c?.prereq_ids),
    ...arr(c?.prerequisites).map((p) => (isObj(p) ? p.id : p)),
  ]);
}
/** 检索用标签：域 / 型 / DAL / status / 四态 / 标准 / 先修 / 草稿标记 */
export function cardTags(c) {
  return uniqSorted([
    cardDomain(c), cardType(c), c?.dal, cardStatus(c), cardState(c),
    isDraft(c) ? 'draft' : 'real',
    ...cardStandards(c),
    ...cardPrereqIds(c),
  ]);
}

/**
 * 合并「台账索引卡」与「全卡」：索引给筛选字段（status/四态/证据 id），
 * 全卡补索引没有的东西——claim、边界标准、命题数组、四态理由、相关卡、文件路径。
 * 冲突时**索引优先**（台账口径由索引给）；索引缺的才用全卡补。
 * 副作用说明：cards_index.json 的 props 是**数字**（条数），全卡是**数组**；
 * 合并后 props 恒为数组、props_count 恒为条数（修掉旧页面 "命题 0" 的显示假象）。
 */
export function mergeCardData(indexCards = [], fullCards = []) {
  const fullList = Array.isArray(fullCards) ? fullCards : Object.values(fullCards?.cards || fullCards || {});
  const byId = new Map();
  for (const f of arr(fullList)) { const id = cardId(f); if (id) byId.set(id, f); }
  return arr(indexCards).map((ic) => {
    const f = byId.get(cardId(ic)) || null;
    const std = cardStandards(ic).length ? cardStandards(ic) : (f ? cardStandards(f) : []);
    const pre = cardPrereqIds(ic).length ? cardPrereqIds(ic) : (f ? cardPrereqIds(f) : []);
    return {
      ...ic,
      claim: str(ic.claim || f?.claim),
      props: Array.isArray(f?.props) ? f.props : [],
      props_count: typeof ic?.props === 'number' ? ic.props : (Array.isArray(f?.props) ? f.props.length : 0),
      cpp_standard: std,
      prereq_ids: pre,
      prerequisites: arr(f?.prerequisites),
      boundary: f?.boundary || null,
      verdict_reasons: arr(f?.verdict?.reasons).map(str),
      related_verified_same_domain: uniqSorted(f?.related_verified_same_domain),
      path: str(ic.path || f?.path),
      full: !!f,
    };
  });
}

// ── 全文搜索 ───────────────────────────────────────────────────────────────
function buildEvidenceMap(index) {
  const m = new Map();
  const add = (id, rec) => {
    if (!id) return;
    const key = str(id);
    if (Array.isArray(rec)) m.set(key, { id: key, serves: rec.map(str) });
    else if (isObj(rec)) m.set(key, { ...rec, id: str(rec.id || key) });
    else if (!m.has(key)) m.set(key, { id: key });
  };
  if (!index) return m;
  if (index instanceof Map) { for (const [k, v] of index) add(k, v); return m; }
  if (Array.isArray(index)) { for (const rec of index) if (isObj(rec)) add(rec.id, rec); return m; }
  if (isObj(index.by_evidence)) return buildEvidenceMap(index.by_evidence);
  for (const [k, v] of Object.entries(index)) add(k, v);
  return m;
}
//: 归一化结果缓存：索引对象**视为不可变**（页面加载后不再改；要改就换新对象）。
//  没有这层缓存时，47 张卡 × 每条证据都会重建一次 Map（筛选输入时每敲一键就重算一遍）。
const EVID_MAP_CACHE = new WeakMap();
/** 索引归一化：Map / 数组 / {by_evidence} / 普通对象 都能吃（同对象只算一次） */
export function toEvidenceMap(index) {
  if (!index) return new Map();
  if (index instanceof Map) return index;
  const hit = EVID_MAP_CACHE.get(index);
  if (hit) return hit;
  const m = buildEvidenceMap(index);
  EVID_MAP_CACHE.set(index, m);
  return m;
}

/**
 * 卡的"可搜索文本"（小写）。覆盖：id / 标题 / 断言(claim) / 命题 /
 * 证据 id 与证据明细（含索引里的 hypothesis、artifact、输出）/ 标签 / 误解 / 文件路径。
 */
export function buildSearchText(c, index = null) {
  const map = toEvidenceMap(index);
  const parts = [];
  const put = (v) => { const s = str(v); if (s !== '') parts.push(s); };
  put(cardId(c)); put(cardTitle(c)); put(c?.claim); put(c?.note); put(c?.path);
  for (const p of arr(c?.props)) {
    if (isObj(p)) { put(p.id); put(p.statement); put(p.subject); put(p.predicate); put(p.object); put(p.external_basis); }
    else put(p);
  }
  for (const t of cardTags(c)) put(t);
  for (const ref of evidenceRefs(c)) {
    put(ref.id); put(ref.path); put(ref.hypothesis); put(ref.artifact); put(ref.verdict); put(ref.kind);
    const rec = map.get(ref.id);
    if (rec) { put(rec.path); put(rec.hypothesis); put(rec.artifact); put(rec.verdict); put(rec.kind); put(rec.sanitizer_output); }
  }
  for (const m of arr(c?.misconceptions)) {
    if (isObj(m)) { put(m.misconception); put(m.target); } else put(m);
  }
  return parts.join(' \n ').toLowerCase();
}

/** 查询切词：空白分隔、忽略大小写、丢掉空词 */
export function tokenize(q) {
  return str(q).toLowerCase().split(/\s+/).filter((t) => t !== '');
}

/** 多词 AND 命中判定（空查询 ⇒ 恒真） */
export function matchesQuery(c, q, index = null) {
  const tokens = tokenize(q);
  if (tokens.length === 0) return true;
  const text = buildSearchText(c, index);
  return tokens.every((t) => text.includes(t));
}

/** 全文搜索（保持入参顺序 ⇒ 排序交给 sortCards） */
export function searchCards(cards = [], q, index = null) {
  return arr(cards).filter((c) => matchesQuery(c, q, index));
}

// ── 高级筛选（维度内 OR · 维度间 AND）──────────────────────────────────────
function selList(v) {
  return arr(v).map(str).filter((s) => s !== '');
}
function normStrengthKey(v) {
  const s = str(v);
  if (/^\d+$/.test(s)) return STRENGTH_LEVELS[Number(s)]?.key || s;
  return s;
}

/**
 * 高级筛选。
 * @param {Array} cards
 * @param {object} f  {q, scope, verdict_state, domain, cpp_standard, strength, status, type, min_evidence}
 * @param {object} index 证据索引（供强度维度用；不给则强度按"卡自带字段"判定）
 */
export function filterCards(cards = [], f = {}, index = null) {
  const flt = f || {};
  const wantState = selList(flt.verdict_state ?? flt.state);
  const wantDomain = selList(flt.domain);
  const wantStd = selList(flt.cpp_standard ?? flt.standard);
  const wantStrength = selList(flt.strength).map(normStrengthKey);
  const wantStatus = selList(flt.status);
  const wantType = selList(flt.type);
  const scope = str(flt.scope || 'all');
  const q = str(flt.q ?? flt.query ?? '').trim();
  const minEvidence = flt.min_evidence === null || flt.min_evidence === undefined || flt.min_evidence === ''
    ? null : Number(flt.min_evidence);

  return arr(cards).filter((c) => {
    if (scope === 'real' && isDraft(c)) return false;
    if (scope === 'draft' && !isDraft(c)) return false;
    if (wantState.length && !wantState.includes(cardState(c))) return false;
    if (wantStatus.length && !wantStatus.includes(cardStatus(c))) return false;
    if (wantType.length && !wantType.includes(cardType(c))) return false;
    if (wantDomain.length && !wantDomain.includes(cardDomain(c))) return false;
    if (wantStd.length) {
      const stds = cardStandards(c);
      const hit = stds.length ? stds.some((s) => wantStd.includes(s)) : wantStd.includes(NO_STANDARD);
      if (!hit) return false;
    }
    if (wantStrength.length && !wantStrength.includes(evidenceStrength(c, index).key)) return false;
    if (minEvidence !== null && cardEvidenceIds(c).length < minEvidence) return false;
    if (q !== '' && !matchesQuery(c, q, index)) return false;
    return true;
  });
}

/** 把筛选条件需要出现的选项值收集出来（前端填 select 用） */
export function filterOptions(cards = [], index = null) {
  const list = arr(cards);
  return {
    verdict_state: uniqSorted(list.map(cardState)),
    domain: uniqSorted(list.map(cardDomain)),
    type: uniqSorted(list.map(cardType)),
    status: uniqSorted(list.map(cardStatus)),
    cpp_standard: [...uniqSorted(list.flatMap(cardStandards)), NO_STANDARD],
    strength: STRENGTH_LEVELS
      .filter((lv) => list.some((c) => evidenceStrength(c, index).key === lv.key))
      .map((lv) => lv.key),
  };
}

// ── 证据强度 ───────────────────────────────────────────────────────────────
function mergedEvidence(ref, map) {
  const rec = map.get(ref.id) || null;
  if (!rec) return { ref, rec: null, record: ref };
  return { ref, rec, record: { ...rec, ...ref } };
}
function refExists(ref, rec) {
  if (ref && ref.exists === false) return false;
  if (ref && ref.exists === true) return true;
  if (rec) {
    if (rec.exists === false) return false;
    if (rec.exists === true) return true;
    return str(rec.path || ref.path) !== '';
  }
  return false;
}
function refVerdict(ref, rec) {
  return str(ref?.verdict || rec?.verdict);
}
function sanitizerState(rec) {
  if (!rec) return { status: 'unknown', output: null };
  const out = rec.sanitizer_output ?? rec.sanitizer?.output;
  if (out === null || out === undefined) return { status: 'unrecorded', output: null };
  const s = String(out);
  return { status: s.trim() === '' ? 'clean' : 'hit', output: s };
}

/**
 * 证据强度（四档 · 只按台账字段判，不推断）。
 * 0 none 无证据 · 1 declared 仅声明（索引/卡里都找不到证据文件）·
 * 2 present 有证据文件但未全部 confirm · 3 confirmed 全部在库且 verdict=confirm
 */
export function evidenceStrength(c, index = null) {
  const map = toEvidenceMap(index);
  const refs = evidenceRefs(c);
  let found = 0, confirmed = 0, captured = 0;
  for (const ref of refs) {
    const { rec } = mergedEvidence(ref, map);
    const ok = refExists(ref, rec);
    if (ok) {
      found += 1;
      if (refVerdict(ref, rec) === 'confirm') confirmed += 1;
    }
    if (sanitizerState(rec).status === 'hit') captured += 1;
  }
  const total = refs.length;
  let level = 0;
  if (total > 0) level = found === 0 ? 1 : confirmed === found && found === total ? 3 : 2;
  const meta = STRENGTH_LEVELS[level];
  return {
    card_id: cardId(c), level, key: meta.key, label: meta.label,
    total, found, missing: total - found, confirmed, captured,
    pct: total === 0 ? 0 : Math.round((100 * found) / total),
  };
}

/** 证据强度排序分（越大越强）：档位 ×10 + confirm 数 ×2 + 在库数，verified 另加 3 */
export function strengthScore(c, index = null) {
  const s = evidenceStrength(c, index);
  let score = s.level * 10 + s.confirmed * 2 + s.found;
  const st = cardStatus(c);
  if (st === 'verified' || st === 'red-team-verified') score += 3;
  return score;
}

// ── 排序 / 统计 ────────────────────────────────────────────────────────────
/** 排序（不改入参；draft 在 strength 模式下永远沉底，与 669c 既有口径一致） */
export function sortCards(cards = [], mode = 'default', index = null) {
  const out = [...arr(cards)];
  const byId = (a, b) => cardId(a).localeCompare(cardId(b));
  const stateRank = (c) => { const i = STATE_ORDER.indexOf(cardState(c)); return i < 0 ? STATE_ORDER.length : i; };
  if (mode === 'strength') {
    out.sort((a, b) => (isDraft(a) ? 1 : 0) - (isDraft(b) ? 1 : 0)
      || strengthScore(b, index) - strengthScore(a, index) || byId(a, b));
  } else if (mode === 'state') {
    out.sort((a, b) => stateRank(a) - stateRank(b) || byId(a, b));
  } else if (mode === 'evidence') {
    out.sort((a, b) => evidenceRefs(b).length - evidenceRefs(a).length || byId(a, b));
  } else if (mode === 'domain') {
    out.sort((a, b) => cardDomain(a).localeCompare(cardDomain(b)) || byId(a, b));
  } else if (mode === 'title') {
    out.sort((a, b) => cardTitle(a).localeCompare(cardTitle(b), 'zh') || byId(a, b));
  } else {
    out.sort(byId);
  }
  return out;
}

/** 汇总统计（全部现算，数字直接来自入参卡集） */
export function cardStats(cards = [], index = null) {
  const list = arr(cards);
  const byState = {}, byDomain = {}, byType = {}, byStatus = {}, byStrength = {}, standards = {};
  let evidenceTotal = 0, cardsWith = 0, noStandard = 0, maxEvidence = 0;
  const distinct = new Set();
  for (const c of list) {
    const st = cardState(c) || '（未声明）';
    const dm = cardDomain(c) || '（未声明）';
    const tp = cardType(c) || '（未声明）';
    const ss = cardStatus(c) || '（未声明）';
    byState[st] = (byState[st] || 0) + 1;
    byDomain[dm] = (byDomain[dm] || 0) + 1;
    byType[tp] = (byType[tp] || 0) + 1;
    byStatus[ss] = (byStatus[ss] || 0) + 1;
    const s = evidenceStrength(c, index);
    byStrength[s.key] = (byStrength[s.key] || 0) + 1;
    const ids = cardEvidenceIds(c);
    evidenceTotal += ids.length;
    if (ids.length) cardsWith += 1;
    maxEvidence = Math.max(maxEvidence, ids.length);
    for (const id of ids) distinct.add(id);
    const stds = cardStandards(c);
    if (stds.length === 0) noStandard += 1;
    for (const v of stds) standards[v] = (standards[v] || 0) + 1;
  }
  return {
    total: list.length,
    drafts: list.filter(isDraft).length,
    real: list.filter((c) => !isDraft(c)).length,
    byState, byDomain, byType, byStatus, byStrength, standards,
    noStandard,
    evidence: {
      total: evidenceTotal,
      distinct: distinct.size,
      cardsWith,
      cardsWithout: list.length - cardsWith,
      max: maxEvidence,
      avg: list.length ? Number((evidenceTotal / list.length).toFixed(2)) : 0,
    },
  };
}

// ── 证据链（card → evidence → file → sanitizer）─────────────────────────────
/**
 * 构建一张卡的证据链树。
 * @returns {{card: object, root: object, stats: object}}
 *   root.children[i]  = 证据 id 节点（kind 'evidence'）
 *   …children[0]      = 证据文件节点（kind 'file'，带 exists/path）
 *   ……children[0/1]   = sanitizer 输出节点（kind 'sanitizer'）+ 复现命令节点（kind 'replay'）
 */
export function buildEvidenceChain(c, index = null) {
  const map = toEvidenceMap(index);
  const refs = evidenceRefs(c);
  const stats = { evidence: refs.length, found: 0, missing: 0, captured: 0, clean: 0, unrecorded: 0, unknown: 0 };
  const children = refs.map((ref) => {
    const rec = map.get(ref.id) || null;
    const record = rec ? { ...rec, ...ref } : ref;
    const exists = refExists(ref, rec);
    if (exists) stats.found += 1; else stats.missing += 1;
    const path = str(record.path || record.artifact) || '（索引未给证据文件路径）';
    const outSource = (rec && rec.sanitizer_output !== undefined) ? rec
      : (ref.sanitizer_output !== undefined ? ref : rec);
    const san = sanitizerState(outSource);
    if (san.status === 'hit') stats.captured += 1;
    else if (san.status === 'clean') stats.clean += 1;
    else stats[san.status] += 1;
    const tool = str(record.sanitizer_kind || record.sanitizer?.kind || record.detector || record.kind || 'sanitizer');
    const fileChildren = [{
      id: ref.id + '::sanitizer',
      kind: 'sanitizer',
      tool,
      status: san.status,
      output: san.output,
      note: san.status === 'hit' ? tool + ' 有输出（见原文，页面不裁剪）'
        : san.status === 'clean' ? tool + ' 无输出（空输出 = 无告警）'
          : san.status === 'unrecorded' ? '台账未记录 ' + tool + ' 输出（不推断）'
            : '证据未入库 ⇒ 无输出可查',
    }];
    const replay = str(record.replay_command);
    if (replay) {
      fileChildren.push({
        id: ref.id + '::replay', kind: 'replay', tool: 'replay', status: replay ? 'captured' : 'unknown',
        output: replay, note: '复现命令（照抄台账，页面不执行）',
      });
    }
    return {
      id: ref.id,
      kind: 'evidence',
      label: ref.id,
      exists,
      verdict: refVerdict(ref, record) || '（未声明）',
      evidence_kind: str(record.kind || record.type) || '（未声明）',
      serves: arr(record.serves).map(str),
      children: [{
        id: ref.id + '::file',
        kind: 'file',
        label: path,
        path,
        exists,
        artifact_sha256: str(record.artifact_sha256),
        note: exists ? '证据文件在库' : (rec ? '索引里标了 exists=false / 无路径' : '索引里没有这条证据 ⇒ 不能假装它在库'),
        children: fileChildren,
      }],
    };
  });

  return {
    card: {
      id: cardId(c), title: cardTitle(c), state: cardState(c),
      status: cardStatus(c), domain: cardDomain(c), strength: evidenceStrength(c, index),
    },
    root: {
      id: cardId(c),
      kind: 'card',
      label: cardId(c),
      title: cardTitle(c),
      state: cardState(c),
      note: refs.length ? '证据 ' + refs.length + ' 条' : '本卡未声明任何证据（不等于没有，只表示台账没记）',
      children,
    },
    stats,
  };
}

/** 由全卡数组建证据索引（web/data/cards.json ⇒ {by_evidence, by_card}） */
export function indexEvidenceFromCards(cards = []) {
  const by_evidence = {};
  const by_card = {};
  const users = new Map();
  for (const c of arr(cards)) {
    const id = cardId(c);
    if (!id) continue;
    const ids = [];
    for (const ref of evidenceRefs(c)) {
      ids.push(ref.id);
      if (!by_evidence[ref.id]) by_evidence[ref.id] = ref;
      if (!users.has(ref.id)) users.set(ref.id, []);
      if (!users.get(ref.id).includes(id)) users.get(ref.id).push(id);
    }
    by_card[id] = ids;
  }
  const shared = [...users.entries()].filter(([, v]) => v.length > 1).map(([k]) => k).sort();
  return { by_evidence, by_card, count: Object.keys(by_evidence).length, shared };
}

// ── 卡关系图 ───────────────────────────────────────────────────────────────
/** Tarjan 强连通分量（迭代版，避免深链爆栈）；输入 adj: Map<id, id[]> */
function tarjanSCC(ids, adj) {
  const index = new Map(), low = new Map(), onStack = new Set(), stack = [], out = [];
  let counter = 0;
  for (const root of ids) {
    if (index.has(root)) continue;
    const work = [{ v: root, i: 0 }];
    while (work.length) {
      const frame = work[work.length - 1];
      const v = frame.v;
      if (frame.i === 0) { index.set(v, counter); low.set(v, counter); counter += 1; stack.push(v); onStack.add(v); }
      const next = (adj.get(v) || [])[frame.i];
      if (next !== undefined) {
        frame.i += 1;
        if (!index.has(next)) work.push({ v: next, i: 0 });
        else if (onStack.has(next)) low.set(v, Math.min(low.get(v), index.get(next)));
      } else {
        work.pop();
        if (work.length) {
          const parent = work[work.length - 1].v;
          low.set(parent, Math.min(low.get(parent), low.get(v)));
        }
        if (low.get(v) === index.get(v)) {
          const comp = [];
          let w;
          do { w = stack.pop(); onStack.delete(w); comp.push(w); } while (w !== v);
          out.push(comp);
        }
      }
    }
  }
  return out;
}

/**
 * 由卡片构关系图。
 * @param {Array} cards 卡集
 * @param {object} opts {includeRelated?:boolean, known?:Iterable<string>}
 *   includeRelated=true 时并入 related_verified_same_domain 无向边（去重，按 id 小→大）
 *   known = 台账全量 id；给了它，则"不在本视图但在台账里"的先修记为 outside（≠ missing）
 * @returns {{nodes, edges, missing, outside, selfLoops, cycles, stats}}
 */
export function buildRelationGraph(cards = [], opts = {}) {
  const list = arr(cards);
  const includeRelated = opts.includeRelated === true;
  const known = opts.known ? new Set([...opts.known].map(str)) : null;
  const nodeMap = new Map();
  const extraIds = new Set();
  const ensure = (id) => {
    const key = str(id);
    let n = nodeMap.get(key);
    if (!n) {
      n = { id: key, label: key, domain: '', status: '', verdict_state: '', draft: false,
        missing: false, outside: false, inCycle: false, selfLoop: false,
        prereq_out: 0, prereq_in: 0, related: 0 };
      nodeMap.set(key, n);
    }
    return n;
  };
  for (const c of list) {
    const id = cardId(c);
    if (!id) continue;
    Object.assign(ensure(id), {
      label: cardTitle(c) || id, domain: cardDomain(c), status: cardStatus(c),
      verdict_state: cardState(c), draft: isDraft(c),
    });
  }
  const edges = [];
  const seen = new Set();
  const addEdge = (source, target, kind, extra = {}) => {
    const key = kind + '|' + source + '|' + target;
    if (seen.has(key) || source === '' || target === '') return null;
    seen.add(key);
    const e = { source, target, kind, missing: false, outside: false, selfLoop: source === target, ...extra };
    edges.push(e);
    return e;
  };
  const missingIds = new Set(), outsideIds = new Set(), selfLoops = new Set();

  for (const c of list) {
    const id = cardId(c);
    if (!id) continue;
    for (const p of cardPrereqIds(c)) {
      let target = nodeMap.get(p);
      if (!target) {
        target = ensure(p);
        if (known && known.has(p)) { target.outside = true; outsideIds.add(p); }
        else { target.missing = true; missingIds.add(p); extraIds.add(p); }
      }
      const e = addEdge(p, id, 'prereq', { missing: target.missing, outside: target.outside });
      if (!e) continue;
      if (e.selfLoop) { selfLoops.add(id); nodeMap.get(id).selfLoop = true; }
      nodeMap.get(p).prereq_out += 1;
      nodeMap.get(id).prereq_in += 1;
    }
  }
  if (includeRelated) {
    for (const c of list) {
      const id = cardId(c);
      if (!id) continue;
      for (const r of uniqSorted(c?.related_verified_same_domain)) {
        if (!nodeMap.has(r)) continue;             // 视图外的"相关"不建边（免得把图撑成台账全图）
        const a = id < r ? id : r, b = id < r ? r : id;
        if (a === b) continue;
        const e = addEdge(a, b, 'related');
        if (!e) continue;
        nodeMap.get(a).related += 1;
        nodeMap.get(b).related += 1;
      }
    }
  }

  // 环：只在 prereq 有向图上找（自环单列，不混进 cycles）
  const ids = [...nodeMap.keys()].sort();
  const adj = new Map(ids.map((id) => [id, []]));
  for (const e of edges) {
    if (e.kind !== 'prereq' || e.selfLoop) continue;
    adj.get(e.source).push(e.target);
  }
  for (const [, v] of adj) v.sort();
  const cycles = tarjanSCC(ids, adj)
    .filter((comp) => comp.length > 1)
    .map((comp) => comp.slice().sort())
    .sort((a, b) => a[0].localeCompare(b[0]) || a.length - b.length);
  const inCycle = new Set(cycles.flat());
  for (const id of inCycle) nodeMap.get(id).inCycle = true;

  const nodes = ids.map((id) => nodeMap.get(id));
  edges.sort((a, b) => a.kind.localeCompare(b.kind) || a.source.localeCompare(b.source) || a.target.localeCompare(b.target));
  const degree = new Map(nodes.map((n) => [n.id, 0]));
  for (const e of edges) { degree.set(e.source, degree.get(e.source) + 1); degree.set(e.target, degree.get(e.target) + 1); }
  return {
    nodes,
    edges,
    missing: [...missingIds].sort(),
    outside: [...outsideIds].sort(),
    selfLoops: [...selfLoops].sort(),
    cycles,
    stats: {
      nodes: nodes.length,
      edges: edges.length,
      prereq: edges.filter((e) => e.kind === 'prereq').length,
      related: edges.filter((e) => e.kind === 'related').length,
      missing: missingIds.size,
      outside: outsideIds.size,
      selfLoops: selfLoops.size,
      cycles: cycles.length,
      isolated: nodes.filter((n) => degree.get(n.id) === 0).length,
    },
  };
}

/** 关系图环形布局（纯几何，确定性；同输入 ⇒ 同输出） */
export function layoutRelationGraph(graph, opts = {}) {
  const nodes = arr(graph?.nodes);
  const width = Number(opts.width) || 720;
  const height = Number(opts.height) || 460;
  const pad = Number(opts.padding ?? 64);
  const cx = width / 2, cy = height / 2;
  const r = Math.max(24, Math.min(width, height) / 2 - pad);
  const order = nodes.map((n) => str(n.id)).sort();
  const positions = {};
  order.forEach((id, i) => {
    // 只有一个节点时放圆心（放在环上会看着像"图没画完"）
    const ang = order.length <= 1 ? -Math.PI / 2 : -Math.PI / 2 + (2 * Math.PI * i) / order.length;
    const rad = order.length <= 1 ? 0 : r;
    positions[id] = {
      x: Number((cx + rad * Math.cos(ang)).toFixed(2)),
      y: Number((cy + rad * Math.sin(ang)).toFixed(2)),
      angle: ang,
    };
  });
  return { width, height, cx, cy, radius: r, order, positions };
}

// ── 批量对比（2–3 张）──────────────────────────────────────────────────────
const CMP_MIN = 2, CMP_MAX = 3;
function cmpBoundary(c) {
  const cb = c?.boundary?.claim_boundary || c?.boundary || {};
  const seg = [];
  const put = (label, v) => { const s = arr(v).map(str).filter(Boolean).join(', '); if (s) seg.push(label + ' ' + s); };
  put('标准', cb.standard); put('编译器', cb.compilers); put('优化', cb.opt); put('平台', cb.platform);
  return seg.length ? seg.join(' · ') : '（本卡未声明边界）';
}
function cmpEvidenceText(c, index) {
  const ids = cardEvidenceIds(c);
  if (!ids.length) return '（无）';
  const s = evidenceStrength(c, index);
  return ids.join(', ') + '（' + s.total + ' 条 · ' + s.label + ' [' + s.key + ']）';
}

/**
 * 批量对比：只接受 2–3 张；其它数量**返回 ok:false**（宁缺勿假，不渲染半张表）。
 * @returns {{ok:boolean, error?:string, message?:string, count:number, ids:string[],
 *            cols:Array, rows:Array, summary:object}}
 */
export function buildComparison(cards = [], index = null) {
  const list = arr(cards).filter((c) => cardId(c) !== '');
  const count = list.length;
  if (count < CMP_MIN || count > CMP_MAX) {
    return {
      ok: false,
      error: 'need-2-to-3',
      message: '批量对比需要 2–3 张卡（收到 ' + count + ' 张）',
      count, ids: list.map(cardId), cols: [], rows: [], summary: null,
    };
  }
  const cols = list.map((c) => {
    const s = evidenceStrength(c, index);
    return {
      id: cardId(c), title: cardTitle(c) || '（未声明标题）', claim: cardClaim(c),
      domain: cardDomain(c), type: cardType(c), status: cardStatus(c),
      verdict_state: cardState(c), state_label: stateLabel(cardState(c)),
      standards: cardStandards(c), prereqs: cardPrereqIds(c),
      dal: str(c?.dal), audience: str(c?.audience || c?.meta?.audience),
      cognitive_load: str(c?.cognitive_load || c?.meta?.cognitive_load),
      draft: isDraft(c), strength: s,
    };
  });
  const valuesOf = (fn) => cols.map((col, i) => str(fn(list[i], col)));
  const row = (key, label, fn) => {
    const values = valuesOf(fn);
    return { key, label, values, differs: new Set(values).size > 1 };
  };
  const rows = [
    row('claim', '断言', (c, col) => col.claim || '（索引未含 claim，只有标题）'),
    row('verdict_state', '四态', (c, col) => col.state_label),
    row('evidence', '证据', (c) => cmpEvidenceText(c, index)),
    row('evidence_files', '证据文件', (c) => {
      const s = evidenceStrength(c, index);
      return s.total === 0 ? '（无）' : s.found + '/' + s.total + ' 在库 · ' + s.confirmed + ' 条 confirm';
    }),
    row('boundary', '边界', (c) => cmpBoundary(c)),
    row('standards', '标准', (c) => cardStandards(c).join(', ') || '（未声明）'),
    row('prereqs', '先修', (c) => cardPrereqIds(c).join(', ') || '（本仓未声明）'),
    row('domain_type', '域 / 型', (c) => (cardDomain(c) || '—') + ' / ' + (cardType(c) || '—')),
    row('status', 'status', (c) => cardStatus(c) || '（未声明）'),
  ];
  const evidenceSets = list.map((c) => new Set(cardEvidenceIds(c)));
  const shared = [...evidenceSets.reduce((acc, s) => new Set([...acc].filter((x) => s.has(x))), evidenceSets[0])].sort();
  const unique = {};
  list.forEach((c, i) => {
    const others = evidenceSets.filter((_, j) => j !== i);
    unique[cardId(c)] = [...evidenceSets[i]].filter((x) => !others.some((s) => s.has(x))).sort();
  });
  return {
    ok: true,
    count,
    ids: cols.map((c) => c.id),
    cols,
    rows,
    summary: {
      same_state: new Set(cols.map((c) => c.verdict_state)).size === 1,
      same_domain: new Set(cols.map((c) => c.domain)).size === 1,
      shared_evidence: shared,
      unique_evidence: unique,
      differ_rows: rows.filter((r) => r.differs).length,
      strongest: cols.slice().sort((a, b) => b.strength.level - a.strength.level || b.strength.confirmed - a.strength.confirmed || a.id.localeCompare(b.id))[0]?.id || '',
    },
  };
}
