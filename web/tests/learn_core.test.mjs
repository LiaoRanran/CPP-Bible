// 672g C · 学习页纯逻辑验收（无 DOM / 无 jsdom / 无 localStorage / 零外部依赖）
//
// 跑法（在 web/ 下）：node tests/learn_core.test.mjs
//
// 由来：learn.html 里 139–495 行的内联 module 脚本（约 350 行）**无法被 Node 测试** ——
//   筛选、评分、SVG 拼串和 getElementById 焊在一起。672g 抽成两层后，纯逻辑层可直测：
//     · 牌组过滤（域 / 全文 / 范围四态）
//     · 统计面板与掌握度百分比
//     · 学习路径 SVG、掌握度曲线、薄弱热力图、今日队列
//     · 知识卡三阶段 / 错例四段式的 HTML（主动回忆：未揭晓不给答案）
//
// 不测什么：localStorage / Blob / FileReader（DOM 层，由 jsdom 冒烟覆盖）。
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import * as CORE from '../js/learn_core.js';
import * as ENG from '../js/learn_engine.js';

let passed = 0;
const ok = (name, cond) => { assert.ok(cond, 'FAIL: ' + name); passed++; };
const eq = (a, b, m) => { assert.equal(a, b, 'FAIL: ' + m + ' (' + a + ' != ' + b + ')'); passed++; };
const has = (s, t, m) => { assert.ok(String(s).indexOf(t) >= 0, 'FAIL: ' + m + '（未含「' + t + '」）'); passed++; };
const lacks = (s, t, m) => { assert.ok(String(s).indexOf(t) < 0, 'FAIL: ' + m + '（不该含「' + t + '」）'); passed++; };

const HTML = readFileSync(new URL('../learn.html', import.meta.url), 'utf-8');

/* ── 夹具：两张知识卡 + 两张错例卡 ── */
const ATOMS = [
  { id: 'ATOM-MEM-001', kind: 'atom', domain: 'mem', title: '内存序', assertion: 'seq_cst 有全局序',
    evidence: ['E1', 'E2'], prereqs: ['ATOM-CONC-001'], verdict_state: 'pass', credibility: 3 },
  { id: 'ATOM-CONC-002', kind: 'atom', domain: 'conc', title: '竞态检测', assertion: 'TSan 能报数据竞争',
    evidence: [], prereqs: [], verdict_state: 'fail', credibility: 2 },
];
const ERRORS = [
  { id: 'ERR-001', kind: 'error', wrong_assertion: 'volatile 能保证线程安全',
    fixture_code: 'int x; std::thread t([&]{x=1;});', fixture_path: 't/err001.cpp',
    sanitizer_output: 'WARNING: ThreadSanitizer: data race', correct_assertion: 'volatile 不做同步',
    correct_source: '反例派生', detector: 'tsan', four_state: 'fail', needs_review: true, verdict: 'fail' },
  { id: 'ERR-002', kind: 'error', wrong_assertion: '未定义行为不会优化', correct_assertion: 'UB 会被优化掉',
    detector: 'ubsan', four_state: 'pass', needs_review: false },
];
const DAY = ENG.DAY || 86400000;
const now = Date.now();
const dueProgress = { 'ATOM-MEM-001': { ...ENG.freshState(), due: now - DAY, reps: 1, last: now - 2 * DAY } };

/* ══ ① 内联脚本已外抽（本批次的存在前提）════════════════════════════════ */
ok('learn.html 不再有内联 module 逻辑脚本', !/<script type="module">\s*\nimport/.test(HTML));
ok('learn.html 改为外链 js/learn.js', HTML.indexOf('<script type="module" src="js/learn.js">') > 0);
ok('learn.html 里不再出现 buildCardDeck（逻辑已搬走）', HTML.indexOf('buildCardDeck') < 0);
ok('js/learn.js 存在且引用 core',
  readFileSync(new URL('../js/learn.js', import.meta.url), 'utf-8').indexOf("from './learn_core.js'") > 0);
ok('键盘导航仍在（handleKey 未被搬丢）',
  readFileSync(new URL('../js/learn.js', import.meta.url), 'utf-8').indexOf('handleKey') > 0);

/* ══ ② 牌组过滤 ═════════════════════════════════════════════════════════ */
eq(CORE.filterDeck(ATOMS, { scope: 'all' }).length, 2, 'scope=all ⇒ 全部');
eq(CORE.filterDeck(ATOMS, { scope: 'all', domain: 'mem' }).length, 1, '域筛选：mem ⇒ 1 张');
eq(CORE.filterDeck(ATOMS, { scope: 'all', domain: 'mem' })[0].id, 'ATOM-MEM-001', '域筛选命中对的那张');
eq(CORE.filterDeck(ERRORS, { scope: 'all', domain: 'mem', isAtom: false }).length, 2,
  '错例牌组不套用域筛选（与线上一致：错例无 domain 维度）');
eq(CORE.filterDeck(ATOMS, { scope: 'all', q: '竞态' }).length, 1, '全文：命中标题');
eq(CORE.filterDeck(ATOMS, { scope: 'all', q: 'TSAN' }).length, 1, '全文：大小写不敏感');
eq(CORE.filterDeck(ATOMS, { scope: 'all', q: 'seq_cst' }).length, 1, '全文：命中 assertion');
eq(CORE.filterDeck(ATOMS, { scope: 'all', q: '不存在这个词' }).length, 0, '全文：无命中 ⇒ 0');
eq(CORE.filterDeck([], { scope: 'all' }).length, 0, '空牌组不抛异常');
const weakProgress = { 'ATOM-CONC-002': { ...ENG.freshState(), reps: 4, lapses: 3, ease: 1.6 } };
eq(CORE.filterDeck(ATOMS, { scope: 'untouched', progress: {} }).length, 2, '未学过：空进度 ⇒ 全部');
eq(CORE.filterDeck(ATOMS, { scope: 'untouched', progress: dueProgress }).length, 1, '未学过：学过的不算');
eq(CORE.filterDeck(ATOMS, { scope: 'weak', progress: weakProgress }).length, 1, '薄弱：只留薄弱那张');
eq(CORE.filterDeck(ATOMS, { scope: 'due', progress: dueProgress }).length >= 1, true, '今日该复习：到期卡在列');
ok('过滤不修改原数组', ATOMS.length === 2 && CORE.filterDeck(ATOMS, { scope: 'all', domain: 'mem' }).length === 1);

/* ══ ③ 统计面板 ═════════════════════════════════════════════════════════ */
const stats = ENG.deckStatsEx({}, ATOMS);
const dash = CORE.dashHtml(stats);
eq((dash.match(/stat-tile/g) || []).length, 6, '六宫格：6 个 stat-tile');
has(dash, '已学', '有"已学"');
has(dash, '掌握', '有"掌握"');
has(dash, '薄弱', '有"薄弱"');
has(dash, '连续天数', '有"连续天数"');
eq(CORE.masteryPct({ total: 10, mastered: 3 }), 30, '掌握度 = 30%');
eq(CORE.masteryPct({ total: 0, mastered: 0 }), 0, 'total=0 ⇒ 0%（不除零、不 NaN）');
eq(CORE.masteryPct(null), 0, 'null ⇒ 0');
const dashWeak = CORE.dashHtml({ ...stats, weak: 4 });
has(dashWeak, 'is-weak', '有薄弱 ⇒ 打 is-weak 标');
has(CORE.dashHtml({ ...stats, streak: { current: 5 } }), 'is-good', '连续 ≥3 天 ⇒ 打 is-good');

/* ══ ④ 学习路径 SVG ═════════════════════════════════════════════════════ */
const path = ENG.pathProgress({}, ATOMS);
const svg = CORE.pathFlowSvg(path);
has(svg, '<svg', '路径是 SVG');
has(svg, 'role="list"', '路径有 role=list（可访问性）');
has(svg, 'aria-label="学习路径三阶段进度"', '路径有 aria-label');
eq((svg.match(/pf-node/g) || []).length, path.stages.length, '阶段节点数 = stages 长度');
has(svg, 'pf-edge', '阶段之间有连线');
has(svg, '已完成', '状态文字：已完成');
ok('每个节点都带 aria-label（阶段名 + done/total）',
  (svg.match(/aria-label="/g) || []).length >= path.stages.length);
eq(CORE.pathFlowSvg({ stages: [], currentStage: -1 }), '<svg viewBox="0 0 600 104" role="list" aria-label="学习路径三阶段进度"></svg>',
  '空阶段不抛异常');

/* ══ ⑤ 掌握度曲线 ═══════════════════════════════════════════════════════ */
const curve0 = ENG.masteryCurve({}, ATOMS);
eq(CORE.curveNoteText(curve0), '暂无记录', '无记录 ⇒ 「暂无记录」');
has(CORE.masteryCurveSvg(curve0), 'chart-empty', '快照 < 2 ⇒ 空状态（不画假线）');
eq(CORE.curveNoteText({ points: [], events: 0 }), '暂无记录', '空曲线不抛异常');
const curve2 = { points: [{ t: 1000, studied: 4, mastered: 1 }, { t: 2000, studied: 4, mastered: 3 }], events: 5 };
eq(CORE.curveNoteText(curve2), '2 个快照 · 5 次复习', '有记录 ⇒ 报快照数与复习次数');
const curveSvg = CORE.masteryCurveSvg(curve2);
has(curveSvg, 'sp-line', '曲线有折线');
has(curveSvg, 'sp-dot', '曲线有快照点');
has(curveSvg, 'sp-grid', '曲线有网格');
has(curveSvg, 'role="img"', '曲线有 role=img');
eq((curveSvg.match(/sp-dot/g) || []).length, 2, '2 个快照 ⇒ 2 个点（不插值多画）');

/* ══ ⑥ 薄弱热力图 ═══════════════════════════════════════════════════════ */
const cells = ENG.weakHeatmap({}, ATOMS);
has(CORE.heatmapHtml(cells), 'heat-cell', '有域 ⇒ 画格子');
has(CORE.heatmapHtml(cells), 'mem', '格子标域名');
has(CORE.heatmapHtml([{ ...cells[0], isWeak: true }]), 'is-weak', '薄弱域打 is-weak（红框）');
has(CORE.heatmapHtml([]), 'chart-empty', '无域 ⇒ 空状态（不是空白）');

/* ══ ⑦ 今日队列 ═════════════════════════════════════════════════════════ */
const byId = Object.fromEntries(ATOMS.map((c) => [c.id, c]));
const qids = ENG.dueQueue(dueProgress, ATOMS, CORE.QUEUE_LIMIT);
has(CORE.queueListHtml(qids, byId, dueProgress), 'queue-item', '有到期卡 ⇒ 列出条目');
has(CORE.queueListHtml(qids, byId, dueProgress), 'data-id=', '条目带 data-id（点击可跳转）');
has(CORE.queueListHtml([], byId, {}), 'muted', '空队列 ⇒ 提示换筛选（不是空白）');
has(CORE.queueListHtml(['ATOM-MEM-001'], byId, {}), '新', '未学过的卡标"新"');
eq(CORE.QUEUE_LIMIT, 12, '队列上限 12（与线上一致）');

/* ══ ⑧ 知识卡三阶段（主动回忆：未揭晓不给答案）══════════════════════════ */
const fresh = ENG.freshState();
const atomHidden = CORE.cardViewHtml(ATOMS[0], fresh, false, null);
has(atomHidden, 'id="flip"', '未揭晓 ⇒ 只有"揭晓"按钮');
lacks(atomHidden, 'grade-row', '未揭晓 ⇒ 不给评分（先回想再揭晓）');
lacks(atomHidden, 'class="answer"', '未揭晓 ⇒ 不给答案');
has(atomHidden, 'ATOM-CONC-001', '前置关系要列出来（未揭晓也可见）');
lacks(atomHidden, 'E1', '证据属于答案，未揭晓不得泄漏');
const atomShown = CORE.cardViewHtml(ATOMS[0], fresh, true, null);
has(atomShown, 'class="answer"', '揭晓 ⇒ 给答案');
has(atomShown, 'E1', '揭晓后证据要列出来');
has(atomShown, 'grade-row', '揭晓 ⇒ 才出现评分');
eq((atomShown.match(/class="grade"/g) || []).length, 4, '评分四档：1/2/3/4');
has(CORE.cardViewHtml(ATOMS[1], fresh, false, null), '无先修声明', '无先修 ⇒ 明说未声明（不假装没有）');

/* ══ ⑨ 错例四段式 ═══════════════════════════════════════════════════════ */
const errShown = CORE.errorViewHtml(ERRORS[0], fresh, true, false);
has(errShown, '错误断言', '第 1 段：错误断言');
has(errShown, '反例代码', '第 2 段：反例代码');
has(errShown, 'sanitizer 输出', '第 3 段：sanitizer 输出');
has(errShown, '正确断言', '第 4 段：正确断言');
has(errShown, 'ThreadSanitizer', 'sanitizer 原文照抄');
has(errShown, '机器生成 · 未签', '无人签 ⇒ 打"未签"标（不冒充已核准知识）');
has(errShown, '无人签', '并说明不进台账');
const errNoSan = CORE.errorViewHtml(ERRORS[1], fresh, true, null);
has(errNoSan, '本卡无 sanitizer 输出', '缺 sanitizer 输出 ⇒ 明说缺失（不编造）');
has(errNoSan, '本卡无反例源码', '缺反例源码 ⇒ 明说缺失');
const errHidden = CORE.errorViewHtml(ERRORS[1], fresh, false, null);
lacks(errHidden, 'UB 会被优化掉', '未揭晓 ⇒ 不泄漏正确断言原文（先回想再揭晓）');
has(errHidden, 'id="flip"', '未揭晓 ⇒ 只给"揭晓正确断言"按钮');
has(CORE.errorViewHtml(ERRORS[0], fresh, true, null), '正确断言来源', '正确断言必须标来源');

/* ══ ⑩ 文案与逃逸 ═══════════════════════════════════════════════════════ */
has(CORE.posNoteText(0, 12, fresh), '第 1 / 12 张', '位置说明');
has(CORE.posNoteText(0, 12, fresh), '易学因子', '位置说明带易学因子');
has(CORE.emptyStudyHtml(), 'data/cards_index.json', '空态说明知识卡来源');
has(CORE.emptyStudyHtml(), 'data/err_deck_670c.json', '空态说明错例来源');
has(CORE.loadErrorHtml(new Error('网络断了')), 'python -m http.server', '加载失败 ⇒ 提示用静态服务器');
lacks(CORE.loadErrorHtml(new Error('<img onerror=1>')), '<img', '错误信息必须转义（防注入）');
eq(CORE.exportNoteText(7), '已导出 7 张卡进度。', '导出提示');
eq(CORE.importNoteText(7, 0), '已合并导入 7 张卡进度。', '导入提示（无跳过）');
has(CORE.importNoteText(7, 2), '跳过 2 条坏数据', '导入提示要写出跳过数');
eq(CORE.STORE_KEY, 'qy-learn-progress-v1', '进度键名与页面说明一致');
eq(CORE.GRADES.length, 4, '评分四档');
eq(CORE.GRADES.map((g) => g[0]).join(','), '1,3,4,5', 'SM-2 的 q = 1/3/4/5');
const st2 = CORE.stateOfCard({}, 'NOPE');
ok('stateOfCard 兜底 freshState（绝不返回 undefined）', st2 && typeof st2.ease === 'number');
has(CORE.gradeRowHtml(fresh), 'id="skip"', '评分行有"跳过"');

console.log('learn_core: ' + passed + ' assertions passed');
