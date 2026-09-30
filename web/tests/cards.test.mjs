// 670c A3 · cards_core 纯逻辑测试（无 DOM / 无 fetch / 无 npm 依赖 ⇒ 直接 node 跑）
//   运行：cd web && node tests/cards.test.mjs
// 断言口径：全部拿**真实算法结果**对账 —— 一半用合成夹具覆盖边界（自环/缺失/环/少于 2 张），
//          一半用 web/data 里的**真实台账**（47 张卡 / 63 条证据）验证数字。
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  STATE_ORDER, NO_STANDARD, STRENGTH_LEVELS, SORT_MODES,
  uniqSorted, cardTitle, cardState, cardStandards, cardPrereqIds, cardTags, isDraft,
  toEvidenceMap, buildSearchText, tokenize, matchesQuery, searchCards,
  filterCards, filterOptions, evidenceStrength, strengthScore, sortCards, cardStats,
  buildEvidenceChain, indexEvidenceFromCards, buildRelationGraph, layoutRelationGraph,
  buildComparison, mergeCardData,
} from '../js/cards_core.js';

let passed = 0;
const ok = (name, cond) => { assert.ok(cond, 'FAIL: ' + name); passed++; };
const eq = (name, actual, expected) => {
  assert.deepEqual(actual, expected, 'FAIL: ' + name + ' ⇒ ' + JSON.stringify(actual) + ' ≠ ' + JSON.stringify(expected));
  passed++;
};

// ═══════════════════════════════════════════════ 合成夹具（边界：强度 / 缺失 / 证据链）
const CARDS = [
  { id: 'ATOM-A-001', title: 'Fence 与 atomic 的顺序约束', domain: 'conc', type: 'mechanism',
    status: 'verified', verdict_state: 'pass', draft: false, cpp_standard: ['C++11', 'C++17'],
    evidence: ['EV-A-001', 'EV-A-002'], prereqs: [] },
  { id: 'ATOM-B-001', title: '仅 fence 的旧写法（反例）', domain: 'MEM', type: 'pitfall',
    status: 'draft', verdict_state: 'unknown', draft: false, cpp_standard: ['C++98'],
    evidence: ['EV-B-001'], prereqs: ['ATOM-A-001'] },
  { id: 'ATOM-C-001', title: 'Draft650 草稿：中断里改全局变量', domain: 'emb', type: 'rule',
    status: 'draft', verdict_state: 'unknown', draft: true, evidence: [], prereqs: [] },
  { id: 'ATOM-D-001', title: '证据未入库的卡', domain: 'UB', type: 'fact',
    status: 'verified', verdict_state: 'fail', draft: false, cpp_standard: ['C++20'],
    evidence: ['EV-Z-001'], prereqs: [] },
];
const EV_INDEX = {
  'EV-A-001': { id: 'EV-A-001', path: 'evidence/conc/EV-A-001.md', exists: true, verdict: 'confirm',
    kind: 'asm', replay_command: 'g++ -std=c++23 -O2 -S x.cpp', sanitizer_output: '' },
  'EV-A-002': { id: 'EV-A-002', path: 'evidence/conc/EV-A-002.md', exists: true, verdict: 'confirm',
    kind: 'run', sanitizer_output: 'runtime error: signed integer overflow' },
  'EV-B-001': { id: 'EV-B-001', path: 'evidence/mem/EV-B-001.md', exists: true, verdict: 'refute', kind: 'run' },
  // EV-Z-001 故意不在索引里 ⇒ "仅声明"
};
const ids = (list) => list.map((c) => c.id);

// ── 搜索 ─────────────────────────────────────────────────────────────────────
eq('空查询 = 不约束（全返回）', ids(searchCards(CARDS, '')), ids(CARDS));
eq('纯空白查询 = 不约束', ids(searchCards(CARDS, '   ')), ids(CARDS));
eq('切词：去空白 + 小写', tokenize('  Fence   Atomic '), ['fence', 'atomic']);
ok('大小写不敏感（ATOMIC 命中标题含 atomic 的卡）', ids(searchCards(CARDS, 'ATOMIC')).join() === 'ATOM-A-001');
eq('未命中 ⇒ 空数组', ids(searchCards(CARDS, 'zzz-not-here')), []);
eq('多词 AND：fence AND atomic ⇒ 只有 A（B 只有 fence）', ids(searchCards(CARDS, 'fence atomic')), ['ATOM-A-001']);
eq('多词 AND：任一词未命中 ⇒ 空（不是 OR）', ids(searchCards(CARDS, 'fence zzz')), []);
eq('搜证据 id', ids(searchCards(CARDS, 'EV-B-001')), ['ATOM-B-001']);
eq('搜标签（域 conc）', ids(searchCards(CARDS, 'conc')), ['ATOM-A-001']);
eq('搜索引里的证据输出（全文穿透到证据库）', ids(searchCards(CARDS, 'signed integer overflow', EV_INDEX)), ['ATOM-A-001']);
ok('搜索文本已小写化（原文 Fence 不再出现）',
  buildSearchText(CARDS[0], EV_INDEX).includes('fence') && !buildSearchText(CARDS[0], EV_INDEX).includes('Fence'));
ok('matchesQuery 空查询恒真', matchesQuery(CARDS[1], '', EV_INDEX) === true);
eq('toEvidenceMap 认 {by_evidence:{id:[卡]}} 形状', toEvidenceMap({ by_evidence: { 'EV-X': ['CARD-1'] } }).get('EV-X').serves, ['CARD-1']);

// ── 高级筛选：维度内 OR · 维度间 AND ────────────────────────────────────────
eq('四态多选 OR：pass ∪ unknown ⇒ 3 张（fail 的 D 落选）', ids(filterCards(CARDS, { verdict_state: ['pass', 'unknown'] }, EV_INDEX)), ['ATOM-A-001', 'ATOM-B-001', 'ATOM-C-001']);
eq('维度间 AND：四态 unknown ∩ 域 MEM ⇒ 只有 B', ids(filterCards(CARDS, { verdict_state: ['unknown'], domain: ['MEM'] }, EV_INDEX)), ['ATOM-B-001']);
eq('域多选 OR：MEM ∪ emb ⇒ B、C', ids(filterCards(CARDS, { domain: ['MEM', 'emb'] }, EV_INDEX)), ['ATOM-B-001', 'ATOM-C-001']);
eq('标准多选 OR：C++11 ∪ C++20 ⇒ A、D', ids(filterCards(CARDS, { cpp_standard: ['C++11', 'C++20'] }, EV_INDEX)), ['ATOM-A-001', 'ATOM-D-001']);
eq('标准筛选：C++98 ⇒ 只有 B', ids(filterCards(CARDS, { cpp_standard: ['C++98'] }, EV_INDEX)), ['ATOM-B-001']);
eq('标准筛选：NO_STANDARD 命中"没声明标准"的卡（C）', ids(filterCards(CARDS, { cpp_standard: [NO_STANDARD] }, EV_INDEX)), ['ATOM-C-001']);
eq('强度筛选：confirmed ⇒ A', ids(filterCards(CARDS, { strength: ['confirmed'] }, EV_INDEX)), ['ATOM-A-001']);
eq('强度筛选：present（有文件但非 confirm）⇒ B', ids(filterCards(CARDS, { strength: ['present'] }, EV_INDEX)), ['ATOM-B-001']);
eq('强度筛选：declared（证据未入库）⇒ D', ids(filterCards(CARDS, { strength: ['declared'] }, EV_INDEX)), ['ATOM-D-001']);
eq('强度筛选：none（无证据）⇒ C', ids(filterCards(CARDS, { strength: ['none'] }, EV_INDEX)), ['ATOM-C-001']);
eq('强度筛选也认数字档位（0 ⇒ none）', ids(filterCards(CARDS, { strength: [0] }, EV_INDEX)), ['ATOM-C-001']);
eq('scope=draft 只看 draft650 批 ⇒ C', ids(filterCards(CARDS, { scope: 'draft' }, EV_INDEX)), ['ATOM-C-001']);
ok('scope=real 排除 draft650 批 ⇒ 3 张（status:draft 的 B 仍在，口径与 669c 一致）',
  filterCards(CARDS, { scope: 'real' }, EV_INDEX).length === 3 && isDraft(CARDS[1]) === false);
eq('空选择 = 该维度不约束', ids(filterCards(CARDS, { verdict_state: [], domain: [], strength: [] }, EV_INDEX)), ids(CARDS));
eq('全文 ∩ 筛选：fence ∩ 域 MEM ⇒ B', ids(filterCards(CARDS, { q: 'fence', domain: ['MEM'] }, EV_INDEX)), ['ATOM-B-001']);
eq('全文 ∩ 筛选：fence ∩ 域 emb ⇒ 空', ids(filterCards(CARDS, { q: 'fence', domain: ['emb'] }, EV_INDEX)), []);
eq('min_evidence ≥2 ⇒ 只有 A', ids(filterCards(CARDS, { min_evidence: 2 }, EV_INDEX)), ['ATOM-A-001']);
ok('filterOptions 标准维度含 NO_STANDARD', filterOptions(CARDS, EV_INDEX).cpp_standard.includes(NO_STANDARD));
ok('filterOptions 强度维度只列出现过的档', filterOptions(CARDS, EV_INDEX).strength.join() === 'none,declared,present,confirmed');

// ── 证据强度 / 排序 / 统计 ──────────────────────────────────────────────────
const sA = evidenceStrength(CARDS[0], EV_INDEX);
ok('A：2 条证据全在库 + verdict=confirm ⇒ level 3 confirmed',
  sA.key === 'confirmed' && sA.level === 3 && sA.found === 2 && sA.confirmed === 2 && sA.pct === 100);
ok('A：sanitizer 输出一条 hit、一条 clean ⇒ captured=1', sA.captured === 1);
ok('B：有文件但 verdict=refute ⇒ level 2 present', evidenceStrength(CARDS[1], EV_INDEX).key === 'present');
ok('D：证据 id 在、索引里没有 ⇒ level 1 declared', evidenceStrength(CARDS[3], EV_INDEX).key === 'declared');
ok('C：没有证据 id ⇒ level 0 none', evidenceStrength(CARDS[2], EV_INDEX).level === 0);
ok('强度分：confirmed > present > declared', strengthScore(CARDS[0], EV_INDEX) > strengthScore(CARDS[1], EV_INDEX)
  && strengthScore(CARDS[1], EV_INDEX) > strengthScore(CARDS[3], EV_INDEX));
const beforeSort = ids(CARDS);
eq('sortCards default = 按 id', ids(sortCards(CARDS, 'default', EV_INDEX)), ['ATOM-A-001', 'ATOM-B-001', 'ATOM-C-001', 'ATOM-D-001']);
ok('sortCards strength：最强在前、草稿沉底',
  sortCards(CARDS, 'strength', EV_INDEX)[0].id === 'ATOM-A-001' && sortCards(CARDS, 'strength', EV_INDEX).at(-1).id === 'ATOM-C-001');
eq('sortCards 不改入参', ids(CARDS), beforeSort);
eq('sortCards state：按 STATE_ORDER 分组（pass → fail → unknown）',
  ids(sortCards(CARDS, 'state', EV_INDEX)), ['ATOM-A-001', 'ATOM-D-001', 'ATOM-B-001', 'ATOM-C-001']);
ok('SORT_MODES 覆盖页面下拉的全部取值', SORT_MODES.length === 6 && SORT_MODES.includes('strength') && SORT_MODES.includes('state'));
const st = cardStats(CARDS, EV_INDEX);
ok('统计：总 4 / 草稿 1 / 实卡 3', st.total === 4 && st.drafts === 1 && st.real === 3);
ok('统计：四态分布 + 证据条数 + 无证据卡数',
  st.byState.pass === 1 && st.byState.fail === 1 && st.evidence.total === 4 && st.evidence.distinct === 4 && st.evidence.cardsWithout === 1);
ok('统计：强度分布（none/declared/present/confirmed 各 1）',
  st.byStrength.none === 1 && st.byStrength.declared === 1 && st.byStrength.present === 1 && st.byStrength.confirmed === 1);
eq('uniqSorted：去重 + 排序 + 丢空值', uniqSorted(['b', 'a', 'b', '', null, undefined, 'c']), ['a', 'b', 'c']);

// ── 证据链（card → evidence → file → sanitizer）─────────────────────────────
const chainA = buildEvidenceChain(CARDS[0], EV_INDEX);
ok('链：根是卡，一级子节点 = 每条证据 id', chainA.root.kind === 'card' && ids(chainA.root.children) .join() === 'EV-A-001,EV-A-002');
ok('链：三级层级 card→evidence→file→sanitizer',
  chainA.root.children[0].kind === 'evidence'
  && chainA.root.children[0].children[0].kind === 'file'
  && chainA.root.children[0].children[0].children[0].kind === 'sanitizer');
ok('链：证据文件路径照抄台账且标在库',
  chainA.root.children[0].children[0].label === 'evidence/conc/EV-A-001.md' && chainA.root.children[0].children[0].exists === true);
ok('链：sanitizer 空输出 ⇒ clean（跑过、无告警）',
  chainA.root.children[0].children[0].children[0].status === 'clean');
ok('链：sanitizer 有输出 ⇒ hit，且原文透传',
  chainA.root.children[0].children[0].children[0].id === 'EV-A-001::sanitizer'
  && chainA.root.children[1].children[0].children[0].status === 'hit'
  && chainA.root.children[1].children[0].children[0].output === 'runtime error: signed integer overflow');
ok('链：复现命令作为 file 的第二个子节点',
  chainA.root.children[0].children[0].children[1].kind === 'replay'
  && chainA.root.children[0].children[0].children[1].output.startsWith('g++ -std=c++23'));
ok('链统计：2 条证据全在库、0 缺失、1 条有 sanitizer 输出',
  chainA.stats.found === 2 && chainA.stats.missing === 0 && chainA.stats.captured === 1);
const chainD = buildEvidenceChain(CARDS[3], EV_INDEX);
ok('链：证据未入库 ⇒ exists=false + sanitizer unknown（不编造输出）',
  chainD.root.children[0].exists === false
  && chainD.root.children[0].children[0].children[0].status === 'unknown'
  && chainD.stats.missing === 1);
const chainC = buildEvidenceChain(CARDS[2], EV_INDEX);
ok('链：无证据的卡 ⇒ 空子节点 + 统计全 0（不假装有链）',
  chainC.root.children.length === 0 && chainC.stats.evidence === 0 && chainC.stats.found === 0);

// ── 关系图（自环 / 缺失前置 / 环）───────────────────────────────────────────
const REL = [
  { id: 'R-A', prereqs: [] },
  { id: 'R-B', prereqs: ['R-A'] },
  { id: 'R-C', prereqs: ['R-B'] },
  { id: 'R-SELF', prereqs: ['R-SELF'] },
  { id: 'R-MISS', prereqs: ['R-NOPE'] },
];
const g1 = buildRelationGraph(REL);
eq('图：前置边方向 = 前置 → 依赖它的卡', g1.edges.find((e) => e.kind === 'prereq' && e.source === 'R-A').target, 'R-B');
ok('图：边数 4（A→B、B→C、SELF 自环、NOPE→MISS）', g1.stats.prereq === 4 && g1.stats.edges === 4);
eq('图：自环单列，且不混进 cycles', [g1.selfLoops, g1.cycles.length], [['R-SELF'], 0]);
ok('图：自环边的 selfLoop 标记为真', g1.edges.some((e) => e.selfLoop && e.source === 'R-SELF' && e.target === 'R-SELF'));
eq('图：缺失前置计进 missing', g1.missing, ['R-NOPE']);
ok('图：缺失前置仍有节点且标 missing=true',
  g1.nodes.find((n) => n.id === 'R-NOPE').missing === true && g1.nodes.find((n) => n.id === 'R-A').missing === false);
const gOut = buildRelationGraph([{ id: 'X', prereqs: ['R-A'] }], { known: ['X', 'R-A'] });
eq('图：给了 known ⇒ 视图外的先修算 outside 不算 missing', [gOut.missing, gOut.outside], [[], ['R-A']]);
const gCycle = buildRelationGraph([
  { id: 'P', prereqs: ['R'] }, { id: 'Q', prereqs: ['P'] }, { id: 'R', prereqs: ['Q'] },
]);
eq('图：P→Q→R→P 检出 1 个环（成员排序后返回）', gCycle.cycles, [['P', 'Q', 'R']]);
ok('图：环内节点标 inCycle', gCycle.nodes.filter((n) => n.inCycle).length === 3 && gCycle.stats.cycles === 1);
const gRel = buildRelationGraph([
  { id: 'RA', related_verified_same_domain: ['RB'] },
  { id: 'RB', related_verified_same_domain: ['RA'] },
], { includeRelated: true });
ok('图：同域相关边去重（双向声明 ⇒ 1 条无向边），默认不启用',
  gRel.stats.related === 1 && gRel.edges[0].kind === 'related' && buildRelationGraph([{ id: 'RA', related_verified_same_domain: ['RB'] }, { id: 'RB' }]).stats.related === 0);
const lay1 = layoutRelationGraph(g1, { width: 720, height: 460 });
const lay2 = layoutRelationGraph(g1, { width: 720, height: 460 });
ok('布局：每个节点都有坐标且确定性（两次调用相同）',
  Object.keys(lay1.positions).length === g1.nodes.length && JSON.stringify(lay1) === JSON.stringify(lay2));
ok('布局：坐标落在画布内、半径为正',
  Object.values(lay1.positions).every((p) => p.x >= 0 && p.x <= 720 && p.y >= 0 && p.y <= 460) && lay1.radius > 0);
const laySingle = layoutRelationGraph({ nodes: [{ id: 'ONLY' }] }, { width: 400, height: 400 });
eq('布局：单节点落在圆心', [laySingle.positions.ONLY.x, laySingle.positions.ONLY.y], [200, 200]);

// ── 批量对比（2–3 张；少于 2 张拒绝）────────────────────────────────────────
const cmp2 = buildComparison([CARDS[0], CARDS[1]], EV_INDEX);
ok('对比：2 张 ⇒ ok，两列 + 行含断言/证据/四态/边界',
  cmp2.ok === true && cmp2.count === 2 && cmp2.cols.length === 2
  && ['claim', 'verdict_state', 'evidence', 'boundary'].every((k) => cmp2.rows.some((r) => r.key === k)));
ok('对比：四态不同 ⇒ 该行 differs=true', cmp2.rows.find((r) => r.key === 'verdict_state').differs === true);
eq('对比：四态取值是人类可读标签', cmp2.rows.find((r) => r.key === 'verdict_state').values, ['pass · 通过', 'unknown · 未知']);
ok('对比：证据行带条数与强度', cmp2.rows.find((r) => r.key === 'evidence').values[0].includes('2 条') && cmp2.rows.find((r) => r.key === 'evidence').values[0].includes('confirmed'));
const cmpSame = buildComparison([{ ...CARDS[0] }, { ...CARDS[0], id: 'ATOM-A-002' }], EV_INDEX);
ok('对比：两列完全相同 ⇒ 所有行 differs=false', cmpSame.rows.every((r) => r.differs === false));
const cmp3 = buildComparison([CARDS[0], CARDS[1], CARDS[3]], EV_INDEX);
ok('对比：3 张 ⇒ ok 且三列', cmp3.ok === true && cmp3.count === 3 && cmp3.cols.length === 3);
const cmp1 = buildComparison([CARDS[0]], EV_INDEX);
ok('对比：1 张 ⇒ 拒绝（ok=false / need-2-to-3 / 不出一行）',
  cmp1.ok === false && cmp1.error === 'need-2-to-3' && cmp1.rows.length === 0 && cmp1.count === 1);
ok('对比：0 张 ⇒ 拒绝', buildComparison([], EV_INDEX).ok === false && buildComparison([], EV_INDEX).message.includes('0 张'));
ok('对比：4 张 ⇒ 拒绝（宁缺勿假，不渲染半张表）', buildComparison([...CARDS], EV_INDEX).ok === false);
const shared = buildComparison([{ ...CARDS[0], evidence: ['EV-SHARED'] }, { ...CARDS[1], evidence: ['EV-SHARED', 'EV-ONLY-B'] }], EV_INDEX);
eq('对比：共有证据 / 独有证据现算', [shared.summary.shared_evidence, shared.summary.unique_evidence['ATOM-B-001']], [['EV-SHARED'], ['EV-ONLY-B']]);
ok('对比：证据都未入库 ⇒ 强度仍照实报 declared',
  buildComparison([{ id: 'N1', evidence: ['EV-N1'] }, { id: 'N2', evidence: ['EV-N2'] }], EV_INDEX).cols.every((c) => c.strength.key === 'declared'));

// ═══════════════════════════════════════════════ 真实台账（web/data，只读）
const IDX = JSON.parse(readFileSync(new URL('../data/cards_index.json', import.meta.url), 'utf8'));
const FULL = JSON.parse(readFileSync(new URL('../data/cards.json', import.meta.url), 'utf8'));
const realIndex = indexEvidenceFromCards(Object.values(FULL.cards));
const merged = mergeCardData(IDX.cards, FULL.cards);
const realIds = (l) => l.map((c) => c.id);

ok('真台账：索引 47 张 / 10 张 draft650', IDX.count === 47 && IDX.cards.length === 47 && IDX.drafts === 10);
ok('真台账：合并后 47 张全部匹配到全卡', merged.length === 47 && merged.every((c) => c.full === true));
ok('真台账：证据索引 63 条 + 1 条被多卡共用（EV-MEM-001）',
  realIndex.count === 63 && realIndex.shared.length === 1 && realIndex.shared[0] === 'EV-MEM-001');
ok('真台账：props 修形（索引给条数、全卡给数组）',
  merged.every((c) => Array.isArray(c.props) && typeof c.props_count === 'number')
  && merged.find((c) => c.id === 'ATOM-HIST-AUTOPTR-001').props_count === 4);
eq('真台账：C++98 标准只命中 auto_ptr 那张卡', realIds(filterCards(merged, { cpp_standard: ['C++98'] }, realIndex)), ['ATOM-HIST-AUTOPTR-001']);
eq('真台账：未声明标准的正好是 10 张 draft650', filterCards(merged, { cpp_standard: [NO_STANDARD] }, realIndex).length, 10);
eq('真台账：scope=real / draft 的口径 = 37 / 10（与 cards.js 旧口径一致）',
  [filterCards(merged, { scope: 'real' }, realIndex).length, filterCards(merged, { scope: 'draft' }, realIndex).length], [37, 10]);
ok('真台账：status=draft（21 张）与 draft650 批（10 张）是两个维度',
  filterCards(merged, { status: ['draft'] }, realIndex).length === 21
  && filterCards(merged, { scope: 'real', status: ['draft'] }, realIndex).length === 11);
eq('真台账：搜证据 id EV-CONC-001 只命中 fence 卡', realIds(searchCards(merged, 'EV-CONC-001', realIndex)), ['ATOM-CONC-FENCE-001']);
eq('真台账：多词 AND（ASAN + 泄漏）命中两张 LEAK 卡', realIds(searchCards(merged, 'ASAN 泄漏', realIndex)), ['ATOM-MEM-LEAK-001', 'ATOM-MEM-LEAK-002']);
eq('真台账：全文穿透证据库（fence + atomic 三张内存序卡）', searchCards(merged, 'fence atomic', realIndex).length, 3);
ok('真台账：fence 卡证据链 2 条全在库、sanitizer 未记录（照实说）',
  (() => { const ch = buildEvidenceChain(merged.find((c) => c.id === 'ATOM-CONC-FENCE-001'), realIndex);
    return ch.root.children.length === 2 && ch.stats.found === 2 && ch.stats.missing === 0
      && ch.stats.unrecorded === 2 && ch.root.children[0].children[0].label === 'evidence/conc/EV-CONC-001.md'; })());
ok('真台账：draft650 卡强度 = none（无证据，不编造）',
  evidenceStrength(merged.find((c) => c.draft === true), realIndex).key === 'none');
ok('真台账：强度排序第一名是 3 条证据的 ALLOC-001（42 分）',
  sortCards(merged, 'strength', realIndex)[0].id === 'ATOM-MEM-ALLOC-001'
  && strengthScore(sortCards(merged, 'strength', realIndex)[0], realIndex) === 42);
const gReal = buildRelationGraph(merged, { known: IDX.cards.map((c) => c.id) });
ok('真台账：先修边 2 条（都指向 FENCE）、无缺失/无自环/无环',
  gReal.stats.prereq === 2 && gReal.stats.missing === 0 && gReal.stats.selfLoops === 0 && gReal.stats.cycles === 0
  && gReal.edges.every((e) => e.source === 'ATOM-CONC-FENCE-001'));
eq('真台账：并入同域相关边 ⇒ 158 条（原始 197 条去重后）', buildRelationGraph(merged, { includeRelated: true, known: IDX.cards.map((c) => c.id) }).stats.related, 158);
const gReal2 = buildRelationGraph(merged, { known: IDX.cards.map((c) => c.id) });
eq('真台账：环形布局节点数 = 图节点数（47）', Object.keys(layoutRelationGraph(gReal2).positions).length, gReal2.nodes.length);
const stReal = cardStats(merged, realIndex);
ok('真台账：统计自洽（域分布求和 = 总数、pass 26 / unknown 21）',
  Object.values(stReal.byDomain).reduce((a, b) => a + b, 0) === 47 && stReal.byState.pass === 26 && stReal.byState.unknown === 21);
ok('真台账：证据 64 条引用 / 63 条不重复 / 37 张卡带证据',
  stReal.evidence.total === 64 && stReal.evidence.distinct === 63 && stReal.evidence.cardsWith === 37 && stReal.evidence.max === 3);
const cmpReal = buildComparison([merged.find((c) => c.id === 'ATOM-CONC-FENCE-001'), merged.find((c) => c.id === 'ATOM-CONC-LOCK-001')], realIndex);
ok('真台账：两张内存序卡对比 = 四态同行、断言不同行、边界文本一致',
  cmpReal.ok && cmpReal.rows.find((r) => r.key === 'verdict_state').differs === false
  && cmpReal.rows.find((r) => r.key === 'claim').differs === true
  && cmpReal.rows.find((r) => r.key === 'boundary').differs === false);

console.log('cards.test: ' + passed + ' assertions passed ✓');
