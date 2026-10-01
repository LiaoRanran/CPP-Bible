// 670c A4 · 判决页深化 · Node 真求值测试（无 DOM / 无依赖 / 无 npm 包 ⇒ 直接 node 跑）
//
//   从 web/ 目录运行：  node tests/verdicts.test.mjs
//
// 纪律：断言**拿真实产物算出来的值**对比，不许写恒真断言。
// 覆盖：时间线排序 / 四态分桶 / 漂移正负 / 差异容差边界 / 缺字段降级。
import assert from 'node:assert/strict';
import { readFileSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';   // 第 12 节渲染冒烟用（把 fetch 接到本地文件）
import {
  parseVerdicts, buildTimeline, fourStateSeries, parseDrift, driftBars, buildDiffRows,
  buildCompareModel, layoutStacked, linePath, toEpoch, batchOf, stateAttr, toleranceLimit,
  pairNumbers, countStates, COMPARE_SPECS, FOUR_STATES,
} from '../js/verdicts_core.js';

let passed = 0;
const ok = (name, cond) => { assert.ok(cond, 'FAIL: ' + name); passed++; };
const near = (a, b, eps = 1e-9) => typeof a === 'number' && Math.abs(a - b) <= eps;
const load = (rel) => JSON.parse(readFileSync(new URL(rel, import.meta.url), 'utf8'));

const V = load('../data/verdicts_667.json');          // web/data/verdicts_667.json
const STATUS = load('../data/status.json');
const METRICS = load('../data/metrics_666.json');
const BASELINE = load('../../data/baseline.json');    // 仓库根 data/baseline.json（静态站取不到 ⇒ 见报告）

/* ── 1 · 真实条数 / 四态计数 ─────────────────────────────────────── */
const parsed = parseVerdicts(V);
ok('verdicts_667.json 真实判决条数 = 31', parsed.total === 31);
ok('declared total 与实测条数一致', parsed.declared_total === 31);
ok('真实数据无任何解析 issue', parsed.ok === true && parsed.issues.length === 0);
ok('四态计数：pass 12 / unknown 19', parsed.counts.pass === 12 && parsed.counts.unknown === 19);
ok('四态计数：fail 0 / pass_with_exception 0', parsed.counts.fail === 0 && parsed.counts.pass_with_exception === 0);
ok('四态计数合计 = 31', FOUR_STATES.reduce((s, k) => s + parsed.counts[k], 0) === 31);
ok('来源拆分：机器卡 16 + 缺陷夹具 15',
  parsed.by_source.ig_cards_665.total === 16 && parsed.by_source.defect_injection_661.total === 15);
ok('机器卡来源内四态：pass 12 / unknown 4',
  parsed.by_source.ig_cards_665.counts.pass === 12 && parsed.by_source.ig_cards_665.counts.unknown === 4);
ok('落盘只有两个日期', parsed.dates.length === 2 && parsed.dates[0] === '2026-09-28' && parsed.dates[1] === '2026-09-29');
ok('批次号从 source 抽出', batchOf('ig_cards_665') === '665' && batchOf('defect_injection_661') === '661');

/* ── 2 · 时间线排序 ─────────────────────────────────────────────── */
const tl = buildTimeline(parsed);
ok('时间线 = 31 条', tl.items.length === 31 && tl.total === 31);
ok('时间序首条 = 2026-09-28 的 ch85-historical（落盘顺序里它排第 17）', tl.items[0].id === 'ch85-historical');
ok('时间序末条 = 2026-09-29 的 IG01', tl.items[30].id === 'IG01');
ok('输入顺序 ≠ 时间顺序 ⇒ reordered', tl.reordered === true);
ok('四态序列首/末', tl.order[0] === 'unknown' && tl.order[30] === 'pass');
ok('时间单调不减（含 tie-break 后）', tl.items.every((r, i) => i === 0 || tl.items[i - 1].t <= r.t));
ok('同日期内按 seq 升序（IG16 在 IG01 之前）',
  tl.items.findIndex((r) => r.id === 'IG16') < tl.items.findIndex((r) => r.id === 'IG01'));
ok('四态切换次数 = 7（15 个连续 unknown 后开始交替）', tl.transitions === 7);
ok('反向时间线首条 = IG01', buildTimeline(parsed, { dir: 'desc' }).items[0].id === 'IG01');
ok('累计计数末条 = 总数', tl.items[30].cum.pass === 12 && tl.items[30].cum.unknown === 19 && tl.items[30].cum_total === 31);
ok('无日期条数 = 0（真实数据日期全合法）', tl.undated === 0);

/* ── 3 · 四态分桶（随时间分布变化）──────────────────────────────── */
const byDate = fourStateSeries(parsed, { bucket: 'date' });
ok('按日期分 2 桶', byDate.buckets.length === 2 && byDate.total === 31);
ok('桶 1 = 2026-09-28：15 条全 unknown',
  byDate.buckets[0].key === '2026-09-28' && byDate.buckets[0].total === 15 && byDate.buckets[0].counts.unknown === 15);
ok('桶 2 = 2026-09-29：16 条 pass 12 / unknown 4',
  byDate.buckets[1].key === '2026-09-29' && byDate.buckets[1].total === 16
  && byDate.buckets[1].counts.pass === 12 && byDate.buckets[1].counts.unknown === 4);
ok('桶内占比正确（12/16 = 75%）', near(byDate.buckets[1].pct.pass, 75));
ok('累计口径正确（最后累计 = 全量）', byDate.buckets[1].cum.pass === 12 && near(byDate.buckets[1].cum_pct.pass, 12 / 31 * 100));
ok('主导四态 = unknown；最大桶 = 2026-09-29 的 16 条', byDate.dominant === 'unknown' && byDate.max === 16);
ok('桶内 id 保留（可回溯到逐条）', byDate.buckets[0].ids[0] === 'ch85-historical' && byDate.buckets[0].ids.length === 15);

const bySource = fourStateSeries(parsed, { bucket: 'source' });
ok('按来源分 2 桶且按首条时间排（661 在前）',
  bySource.buckets.length === 2 && bySource.buckets[0].key === 'defect_injection_661' && bySource.buckets[1].key === 'ig_cards_665');

const byWin = fourStateSeries(parsed, { bucket: 'window', size: 5 });
ok('按 5 条窗口分 7 桶（31 = 5×6 + 1）', byWin.buckets.length === 7 && byWin.buckets[6].total === 1);
ok('窗口桶标签写明条号区间', byWin.buckets[0].label === '第 1–5 条' && byWin.buckets[6].label === '第 31–31 条');
ok('分桶计数合计 = 总数', byDate.buckets.reduce((s, b) => s + b.total, 0) === 31);

/* ── 4 · 堆叠柱几何 ─────────────────────────────────────────────── */
const geo = layoutStacked(byDate, { width: 600, height: 200 });
ok('几何：每桶 4 段（四态齐全）', geo.bands.every((b) => b.segs.length === 4));
const tall = geo.bands.reduce((a, b) => (b.total > a.total ? b : a), geo.bands[0]);
ok('最高桶段高之和 = 柱高（末段吸收误差）',
  near(tall.segs.reduce((s, g) => s + g.h, 0), tall.full, 1e-9) && near(tall.full, geo.plotH, 1e-9));
ok('柱 x 递增', geo.bands.every((b, i) => i === 0 || geo.bands[i - 1].x < b.x));
ok('折线点数 = 桶数', geo.line.length === byDate.buckets.length);
ok('折线：桶 1 pass 0% ⇒ 贴底；桶 2 pass 75% ⇒ y 在上半区',
  geo.line[0].pct === 0 && geo.line[0].y === geo.pad.t + geo.plotH
  && near(geo.line[1].pct, 75) && geo.line[1].y < geo.pad.t + geo.plotH / 2);
ok('网格线含 0 与 max', geo.grid[0].value === 0 && geo.grid[geo.grid.length - 1].value === geo.max);
const dpath = linePath(geo.line).split(' ');
ok('linePath：M 起点 + L 续点，坐标取两位小数',
  dpath.length === 4 && dpath[0] === 'M' + geo.line[0].x.toFixed(2) && dpath[1] === geo.line[0].y.toFixed(2)
  && dpath[2] === 'L' + geo.line[1].x.toFixed(2) && dpath[3] === geo.line[1].y.toFixed(2));
ok('linePath 跳过 y=null 的点、无点时返回空串',
  linePath([{ x: 1, y: null }, { x: 2, y: 3 }, { x: 3, y: 4 }]) === 'M2.00 3.00 L3.00 4.00'
  && linePath([]) === '' && linePath(null) === '');

/* ── 5 · 漂移登记规范化（真实 baseline.json）────────────────────── */
const drift = parseDrift(BASELINE, { source: 'data/baseline.json' });
ok('baseline tolerated_discrepancies = 2 条登记', drift.total === 2 && drift.sources.includes('tolerated_discrepancies[]'));
const gn = drift.items.find((d) => d.field === 'graph.nodes');
ok('graph.nodes 字段被抽出', !!gn && gn.kind === 'tolerated');
ok('graph.nodes：待权威源 121 / 以实测 178 为准', gn.pending === 121 && gn.authoritative === 178);
ok('graph.nodes：脱敏成 stored/fresh 且 delta = +57（正漂移）',
  gn.numeric === true && gn.stored === 121 && gn.fresh === 178 && gn.delta === 57 && gn.dir === 'up' && gn.neg === false);
ok('graph.nodes：相对误差 = 57/121', near(gn.rel_pct, 57 / 121 * 100));
const rulesDrift = drift.items.find((d) => d.field === 'rules');
ok('rules 条目：已归档无差异 ⇒ resolved', rulesDrift.resolved === true);
ok('rules 条目：无「待权威源/以…为准」配对 ⇒ 不硬造数值', rulesDrift.numeric === false && rulesDrift.delta === null);
ok('resolved 计数 = 1', drift.tolerated === 1);

/* ── 6 · 漂移登记：verdicts_667 的 compare 行（口径差）──────────── */
const cmpDrift = parseDrift(V, { source: 'web/data/verdicts_667.json' });
ok('compare 抽出 6 条口径差登记', cmpDrift.total === 6 && cmpDrift.sources.includes('compare[]'));
ok('其中 3 条两侧数值个数相同 ⇒ 可配对', cmpDrift.numeric === 3 && cmpDrift.text_only === 3);
const ext = cmpDrift.items.find((d) => d.field === '外部语料检出率');
// 672h 数字同步：corpus 扩样（可测 48→64）+ 口径行随之更新 ⇒ 62.5%（可测） vs 52.6%（全样本），
//   delta = −9.9。真值源 web/data/verdicts_667.json（由 tools/web_verdicts_667.py 重生成）。
ok('外部语料：62.5% → 52.6% ⇒ delta = −9.9（负漂移）',
  ext.numeric === true && near(ext.delta, -9.9) && ext.neg === true && ext.dir === 'down' && ext.kind === 'caliber');
const mut = cmpDrift.items.find((d) => d.field === '内部变异率');
// 672h 数字同步：变异 core 重跑后 97.3 → 96.5 ⇒ delta = 96.5 − 74.8 = −21.7（登记文本同步更新）
ok('内部变异率：96.5% → 74.8% ⇒ delta = −21.7（与登记文本的 21.7pp 一致）', near(mut.delta, -21.7));
const counter = cmpDrift.items.find((d) => d.field === '反事实算子 P/R/F1');
ok('反事实行两侧数值个数不同 ⇒ 拒绝硬配对（不造 +9 这种假漂移）',
  counter.numeric === false && counter.delta === null && /个数不同/.test(counter.skip_reason));
ok('pairNumbers：个数相同才配对', pairNumbers('a 1 b 2', 'c 3 d 4').numeric === true && pairNumbers('1 2 3', '9').numeric === false);

/* ── 7 · 漂移幅度条：正负几何 ───────────────────────────────────── */
const bars = driftBars(cmpDrift);
ok('幅度条条数 = 登记条数', bars.total === 6 && bars.bars.length === 6);
ok('负向 2 条（外部语料 / 内部变异率）、零漂移 1 条', bars.negative === 2 && bars.flat_count === 1 && bars.positive === 0);
ok('量程 = 最大 |delta| = 21.7', near(bars.max, 21.7) && near(bars.scale, 21.7));
const extBar = bars.bars.find((b) => b.field === '外部语料检出率');
ok('负向条：贴在中线左侧（left + width = 50%）',
  extBar.cls === 'is-neg' && extBar.left_pct < 50 && near(extBar.left_pct + extBar.width_pct, 50));
ok('负向条宽 = |−9.9| / 21.7 × 50', near(extBar.width_pct, 9.9 / 21.7 * 50));
ok('负向条文本带负号', extBar.val_text === '-9.90' && extBar.rel_text === '-15.8%');
ok('零漂移条：left=50、width=0、flat', bars.bars.find((b) => b.field === 'holdout 检出率').flat === true);
const posBars = driftBars([{ field: 'x', stored: 100, fresh: 150 }, { field: 'y', stored: 100, fresh: 75 }]);
ok('正向 +50（量程最大）⇒ 从中线向右占满半轨', posBars.bars[0].left_pct === 50 && near(posBars.bars[0].width_pct, 50));
ok('负向 −25 ⇒ 从中线向左半格（left + width = 50）',
  posBars.bars[1].left_pct === 25 && near(posBars.bars[1].width_pct, 25) && posBars.bars[1].left_pct + posBars.bars[1].width_pct === 50);
ok('同一量程下条宽与 |delta| 成正比（50 : 25 = 2 : 1）',
  near(posBars.bars[0].width_pct / posBars.bars[1].width_pct, 2) && posBars.positive === 1 && posBars.negative === 1);
ok('固定量程 opts.scale 生效（scale=100 ⇒ 半轨 = 50 单位）',
  near(driftBars([{ field: 'x', stored: 100, fresh: 150 }], { scale: 100 }).bars[0].width_pct, 25));
ok('无数值登记条：不画长度但仍在列表里', driftBars([{ field: 'z', note: '无数值' }]).bars[0].numeric === false
  && driftBars([{ field: 'z', note: '无数值' }]).bars[0].width_pct === 0);

/* ── 8 · 差异表：容差边界 ───────────────────────────────────────── */
const spec = [{ key: 'm', label: 'm', tol: { abs: 0.5 } }];
const atEdge = buildDiffRows({ m: 10 }, { m: 10.5 }, { specs: spec }).rows[0];
ok('恰好等于绝对容差 ⇒ 不算不一致（边界取严）', atEdge.diff === 0.5 && atEdge.within_tolerance === true && atEdge.isMismatch === false && atEdge.rowClass === 'is-match');
const overEdge = buildDiffRows({ m: 10 }, { m: 10.6 }, { specs: spec }).rows[0];
ok('超出绝对容差 0.1 ⇒ is-mismatch', overEdge.within_tolerance === false && overEdge.isMismatch === true && overEdge.rowClass === 'is-mismatch');
ok('差异文本带符号', overEdge.diff_text === '+0.60' && overEdge.rel_text === '+6.0%');
ok('相对容差：limit = rel × |声明值|', near(toleranceLimit(200, { rel: 0.01 }), 2));
const relEdge = buildDiffRows({ m: 200 }, { m: 202 }, { specs: [{ key: 'm', tol: { rel: 0.01 } }] }).rows[0];
ok('相对容差边界内 ⇒ 一致', relEdge.limit > 1.99 && relEdge.isMismatch === false);
ok('相对容差外 ⇒ 不一致', buildDiffRows({ m: 200 }, { m: 203 }, { specs: [{ key: 'm', tol: { rel: 0.01 } }] }).rows[0].isMismatch === true);
ok('容差 = 0（默认）时任何差异都不一致', buildDiffRows({ m: 1 }, { m: 1.000001 }).rows[0].isMismatch === true);
const calRow = buildDiffRows({ m: 10 }, { m: 20 }, { specs: [{ key: 'm', kind: 'caliber' }] }).rows[0];
ok('口径差行：数值差很大也**不判红绿**', calRow.isMismatch === false && calRow.rowClass === 'is-caliber' && /口径差/.test(calRow.verdict_text));
ok('负差异文本带负号', buildDiffRows({ m: 20 }, { m: 10 }).rows[0].diff_text === '-10');

/* ── 9 · 差异表：缺字段降级 ─────────────────────────────────────── */
const partial = buildDiffRows({ a: 1 }, { b: 2 });
ok('两侧各缺一条 ⇒ 2 行且都是 is-partial', partial.total === 2 && partial.partial === 2);
ok('缺一侧值时该侧显示 —、差异为 null（不冒充 0）',
  partial.rows[0].key === 'a' && partial.rows[0].declared === 1 && partial.rows[0].computed === null
  && partial.rows[0].computed_text === '—' && partial.rows[0].diff === null && partial.rows[0].isMismatch === false);
ok('缺值行写明缺口在哪一侧（且行标 is-partial）',
  partial.rows[0].missing === 'computed' && partial.rows[1].missing === 'declared'
  && partial.rows.every((r) => r.rowClass === 'is-partial'));
ok('未声明口径的指标走自动兜底 spec', partial.issues.some((i) => i.code === 'auto-spec'));
ok('空输入不抛异常', buildDiffRows(null, undefined).rows.length === 0 && buildDiffRows({}, {}).total === 0);

/* ── 10 · 比对模型：真实四源交叉核对 ───────────────────────────── */
const model = buildCompareModel({ verdicts: V, status: STATUS, metrics: METRICS, baseline: BASELINE, parsed });
ok('比对模型行数 = 口径表长度（' + COMPARE_SPECS.length + '）', model.total === COMPARE_SPECS.length && model.rows.length === COMPARE_SPECS.length);
ok('真实不一致只有 2 条：实卡数/卡总数（状态页口径 vs 判决页口径）',
  model.mismatches === 2 && model.red_keys.join(',') === 'cards_real_status,cards_total_status');
const redRow = model.rows.find((r) => r.key === 'cards_real_status');
ok('不一致行：37 → 42，差异 +5，相对 +13.5%',
  redRow.declared === 37 && redRow.computed === 42 && redRow.diff === 5 && redRow.rel_text === '+13.5%');
ok('缺口 4 条（反事实 / 图谱 / 总条数 / 夹具条数）', model.partial === 4);
// 672g 数字同步：672f「W1 实验抢救」把 holdout 从 16 样本扩到 22（已 reveal 并跑过）
//   ⇒ 判决页 samples 17 → 22，盲态池仍是 20 ⇒ 口径差由 −3 变 +2。
//   两侧真值：data/baseline.json::holdout.count = 20（声明侧）；
//            web/data/verdicts_667.json::dashboard.holdout.samples = 22（现算侧）。
//   仍是"口径差"（不判红绿）—— 两个数都对，只是量的不是同一件事。
// 672h 数字同步：holdout 已跑样本 22 → 42（第 5 轮扩样 h41-h60），盲态池仍是 20
//   ⇒ 口径差由 +2 变 +22（仍然是"口径差"，不判红绿：两个数都对，只是量的不是同一件事）。
ok('口径差 1 条（holdout 池 20 vs 已跑 42，diff = +22）',
  model.caliber === 1 && model.rows.find((r) => r.key === 'holdout_pool').diff === 22);
ok('冻结契约 3 条（逃逸率族）不借 is-match 的绿', model.frozen === 3
  && model.rows.filter((r) => r.kind === 'frozen').every((r) => r.rowClass === 'is-frozen' && r.isMismatch === false));
ok('一致 22 条（32 = 22 一致 + 2 不一致 + 4 缺口 + 1 口径差 + 3 冻结）',
  model.matches === 22 && model.total === 32
  && model.total === model.matches + model.mismatches + model.partial + model.caliber + model.frozen);
ok('全部四源都在 available 里', Object.values(model.available).every(Boolean));
ok('判决总条数现算 = 31（声明侧缺口）',
  model.rows.find((r) => r.key === 'verdict_page_total').computed === 31
  && model.rows.find((r) => r.key === 'verdict_page_total').missing === 'declared');
const noBaseline = buildCompareModel({ verdicts: V, status: STATUS, metrics: METRICS, parsed });
ok('缺 baseline.json 时**不崩**，只是图谱/变异等行变缺口', noBaseline.total === COMPARE_SPECS.length && noBaseline.partial > model.partial);
ok('缺 baseline 时仍能算出那 2 条真实不一致', noBaseline.red_keys.join(',') === 'cards_real_status,cards_total_status');
const empty = buildCompareModel();
ok('四源全缺时不崩、零不一致（全部是缺口）',
  empty.total === COMPARE_SPECS.length && empty.mismatches === 0 && empty.partial === COMPARE_SPECS.length);

/* ── 11 · 缺字段降级（解析层）───────────────────────────────────── */
const bad = parseVerdicts({});
ok('无 verdicts 数组 ⇒ 记 issue 且 0 条', bad.total === 0 && bad.issues.some((i) => i.code === 'no-verdicts-array'));
const badRow = parseVerdicts([{ id: 'X' }]);
ok('缺 state ⇒ 降级 unknown 并记 issue', badRow.rows[0].state === 'unknown' && badRow.rows[0].state_raw === '' && badRow.issues.some((i) => i.code === 'missing-state'));
ok('缺 when ⇒ t=null 且记 issue', badRow.rows[0].t === null && badRow.issues.some((i) => i.code === 'bad-when'));
ok('非法 state 降级而不是透传', parseVerdicts([{ id: 'Y', state: 'weird', when: '2026-01-01' }]).rows[0].state === 'unknown');
ok('非法日期（2026-02-31）判 null，不被 Date 偷偷滚成 3 月', toEpoch('2026-02-31') === null && toEpoch('2026-09-28') === Date.UTC(2026, 8, 28));
ok('总数声明与实测不符时记 issue',
  parseVerdicts({ verdicts: [{ id: 'a', state: 'pass', when: '2026-01-01' }], verdicts_total: 9 }).issues.some((i) => i.code === 'total-mismatch'));
ok('空/坏输入一律不抛', parseVerdicts(null).total === 0 && parseVerdicts('x').total === 0 && countStates(null).unknown === 0);
ok('空输入的时间线/分桶不崩', buildTimeline(null).items.length === 0 && fourStateSeries(null).buckets.length === 0
  && fourStateSeries(null).issues.some((i) => i.code === 'empty'));
ok('漂移：null / 空数组 / 无登记表对象都不崩',
  driftBars(null).total === 0 && driftBars([]).total === 0 && parseDrift({}).issues.some((i) => i.code === 'no-registry'));
ok('无日期条目永远排在时间线末尾（不分方向）',
  buildTimeline([{ id: 'no-date', state: 'fail' }, { id: 'dated', state: 'pass', when: '2026-01-01' }]).items[1].id === 'no-date'
  && buildTimeline([{ id: 'no-date', state: 'fail' }, { id: 'dated', state: 'pass', when: '2026-01-01' }], { dir: 'desc' }).items[1].id === 'no-date');
ok('data-state 两张表各归各（连字符 vs 下划线）',
  stateAttr('pass_with_exception') === 'pass-exception' && stateAttr('pass_with_exception', 'pill') === 'pass_with_exception'
  && stateAttr('nonsense') === 'unknown');


/* ── 12 · 渲染层冒烟（自建最小 DOM 垫片：本仓无 node_modules / 无 jsdom）──────
   为什么值得写：纯逻辑对了，DOM 里照样可能因为**拼错的 id / 类名**整段不渲染。
   这里把 web/verdicts.js 真的 import 进来跑一遍 boot()，再用字符串核对产出的 HTML。
   代价：垫片只实现本页用到的那几个 API，**不是**完整 DOM（见文件末尾的诚实边界）。 */

const HTML_SRC = readFileSync(new URL('../verdicts.html', import.meta.url), 'utf8');
const JS_SRC = readFileSync(new URL('../verdicts.js', import.meta.url), 'utf8');
const HTML_IDS = new Set([...HTML_SRC.matchAll(/id="([^"]+)"/g)].map((m) => m[1]));

/** 静态检查：verdicts.js 里 \$('x') / getElementById('x') 引用的 id 必须都在 HTML 里存在。 */
const referenced = new Set();
// 注意排除 $$\('…'\)（第二个 $ 前面还是 $）—— 那是 querySelectorAll，不是 id
for (const m of JS_SRC.matchAll(/(^|[^$])\$\(\s*'([^']+)'\s*\)/g)) referenced.add(m[2]);
for (const m of JS_SRC.matchAll(/getElementById\(\s*'([^']+)'\s*\)/g)) referenced.add(m[1]);
const dangling = [...referenced].filter((id) => !HTML_IDS.has(id));
ok('verdicts.js 引用的 ' + referenced.size + ' 个 id 全部存在于 verdicts.html（无拼写漂移）',
  referenced.size > 20 && dangling.length === 0);

function makeDom() {
  const map = new Map();
  const mk = (id) => ({
    id, _html: '', _text: '', style: {}, dataset: {}, children: [], firstChild: null,
    clientWidth: 900, checked: false, parentNode: { style: {} },
    set innerHTML(v) { this._html = String(v); }, get innerHTML() { return this._html; },
    set textContent(v) { this._text = String(v); },
    get textContent() { return this._text || this._html.replace(/<[^>]*>/g, ''); },
    appendChild(c) { if (this.firstChild === null) this.firstChild = c; this.children.push(c); return c; },
    append(...cs) { for (const c of cs) this.appendChild(c); },
    addEventListener() {}, setAttribute() {}, removeAttribute() {}, getAttribute() { return null; },
    querySelector() { return null; }, querySelectorAll() { return []; },
    classList: { add() {}, remove() {} },
  });
  for (const id of HTML_IDS) map.set(id, mk(id));
  globalThis.document = {
    readyState: 'complete',
    getElementById: (id) => map.get(id) || null,
    createElement: (tag) => { const e = mk(null); e.tagName = tag; return e; },
    createTextNode: (t) => ({ nodeValue: String(t) }),
    querySelectorAll: () => [], querySelector: () => null,
    addEventListener() {}, body: { prepend() {} },
  };
  return map;
}

/** 跑一次页面模块。mode='web-root' 时 baseline 取不到（静态站以 web/ 为根的实况）。 */
async function runPage(caseName, mode, opts = {}) {
  const map = makeDom();
  // 670c：'hide' 用来**显式**模拟某个源缺席。
  // 病（670c 实测）：(a) 原本靠"web/data/baseline.json 恰好不存在"来测降级，
  // 一旦真把 baseline 同步进 web/data/（670c 的修复），这条断言就会因为环境变了而红 ——
  // 断言不该依赖文件系统现状，所以改成显式隐藏。
  const hide = new Set(opts.hide || []);
  globalThis.window = { matchMedia: () => ({ matches: true }), addEventListener() {} };
  globalThis.performance = { now: () => Date.now() };
  globalThis.requestAnimationFrame = () => 0;
  globalThis.fetch = async (url) => {
    const p = mode === 'repo-root'
      ? path.resolve(WEB_DIR, url)
      : path.join(WEB_DIR, url.replace(/^\.\.\//, ''));
    if (mode === 'no-data' || hide.has(path.basename(p)) || !fileExists(p)) {
      return { ok: false, status: 404, json: async () => ({}) };
    }
    return { ok: true, status: 200, json: async () => JSON.parse(readFileSync(p, 'utf8')) };
  };
  await import(new URL('../verdicts.js', import.meta.url).href + '?smoke=' + caseName);
  await new Promise((r) => setTimeout(r, 80));
  return { map, hooks: globalThis.window.__verdicts_hooks };
}

const WEB_DIR = fileURLToPath(new URL('..', import.meta.url));
const fileExists = (p) => { try { return statSync(p).isFile(); } catch (e) { return false; } };
const cnt = (s, re) => (s.match(re) || []).length;

// (a) 降级：显式隐藏 baseline（模拟 670a 尚未落盘 / 未跑同步工具的检出），页面必须照样可用
const A = await runPage('a', 'web-root', { hide: ['baseline.json'] });
const elA = (id) => A.map.get(id) || { innerHTML: '', textContent: '' };
ok('页面模块挂上 window.__verdicts_hooks', !!A.hooks && A.hooks.ready() === true);
ok('降级后仍加载到 verdicts/status/metrics 三源（baseline 缺席）',
  A.hooks.loadedSources().join(',') === 'verdicts,status,metrics');
ok('时间线渲染 31 个 .tl-item，四态点 19 unknown / 12 pass',
  cnt(elA('tl').innerHTML, /class="tl-item"/g) === 31
  && cnt(elA('tl').innerHTML, /class="tl-item" data-state="unknown"/g) === 19
  && cnt(elA('tl').innerHTML, /class="tl-item" data-state="pass"/g) === 12);
ok('时间线小结写明重排与切换次数',
  /四态切换 7 次/.test(elA('tl-note').textContent) && /落盘顺序 ≠ 时间顺序/.test(elA('tl-note').textContent));
ok('四态图渲染出内联 SVG + 3 个非空堆叠段（2 桶：1×unknown、1×(pass+unknown)）',
  /<svg/.test(elA('fs-chart').innerHTML) && cnt(elA('fs-chart').innerHTML, /class="seg"/g) === 3);
ok('图例 5 项（四态 + 折线说明）且四态色走 var(--color-*)',
  cnt(elA('fs-legend').innerHTML, /class="lg-item"/g) === 5 && /var\(--color-pass\)/.test(elA('fs-legend').innerHTML));
ok('漂移条 5 条（compare 3 条有数值 + 2 条真不一致；baseline 缺席）',
  cnt(elA('drift-bars').innerHTML, /class="drift-bar"/g) === 5
  && cnt(elA('drift-bars').innerHTML, /drift-fill is-neg/g) === 2);
ok('漂移说明**显式登记** baseline 缺席，不假装没有漂移',
  /未加载/.test(elA('drift-note').textContent));
ok('差异表 32 行、其中 2 行 .is-mismatch',
  cnt(elA('diff-body').innerHTML, /<tr /g) === 32 && cnt(elA('diff-body').innerHTML, /class="is-mismatch"/g) === 2);
ok('渲染文本里没有未处理的 ** 标记（粗体已转 <b>）',
  cnt(elA('vt-body').innerHTML, /\*\*/g) === 0 && cnt(elA('diff-body').innerHTML, /\*\*/g) === 0
  && cnt(elA('tl').innerHTML, /\*\*/g) === 0 && cnt(elA('drift-bars').innerHTML, /\*\*/g) === 0);
ok('数据齐时**不出现**占位块', ['fs-chart', 'drift-bars', 'tl', 'diff-body'].every((i) => !/chart-empty/.test(elA(i).innerHTML)));

// (b) 交互：只看不一致 / 换分桶
A.hooks.setA4({ diffOnly: true });
ok('「只看不一致」过滤后剩 2 行', cnt(elA('diff-body').innerHTML, /<tr /g) === 2);
A.hooks.setA4({ diffOnly: false, bucket: 'window', size: 5 });
ok('切到 5 条窗口分桶 ⇒ 7 个桶', cnt(elA('fs-notes').innerHTML, /<li>/g) === 7);
A.hooks.setA4({ bucket: 'source' });
ok('切到按来源分桶 ⇒ 2 个桶', cnt(elA('fs-notes').innerHTML, /<li>/g) === 2);

// (a0) 670c 修复验证：web/data/baseline.json 已由 tools/web_experiments_sync_670c.py 同步，
// 静态站以 web/ 为根时 baseline **取得到** ⇒ 四源到齐、漂移条含 baseline 的 graph.nodes +57。
// 注意：本段必须在 (a)/(b) 之后 —— runPage 会换掉 globalThis.document，
// 放在前面会让 A 的 hooks 渲染到 A0 的 DOM 上。
const A0 = await runPage('a0', 'web-root');
const elA0 = (id) => A0.map.get(id) || { innerHTML: '', textContent: '' };
ok('修复后：web 根即可取到 baseline（四源到齐）', A0.hooks.loadedSources().length === 4);
ok('修复后：漂移条 6 条（含 baseline 的 graph.nodes +57）',
  cnt(elA0('drift-bars').innerHTML, /class="drift-bar"/g) === 6
  && /\+57/.test(elA0('drift-bars').innerHTML));

// (c) 服务起在**仓库根**时 ../data/baseline.json 命中 ⇒ 漂移条变 6 条（多出 graph.nodes +57）
const B = await runPage('b', 'repo-root');
const elB = (id) => B.map.get(id) || { innerHTML: '', textContent: '' };
ok('仓库根模式：四源全到齐', B.hooks.loadedSources().length === 4);
ok('仓库根模式：漂移条 6 条（补上 baseline 的 graph.nodes +57）',
  cnt(elB('drift-bars').innerHTML, /class="drift-bar"/g) === 6
  && /\+57/.test(elB('drift-bars').innerHTML));
ok('仓库根模式：差异表缺口从 9 降到 4（口径差 1 + 冻结 3）',
  /缺口 4/.test(elB('diff-sub').textContent) && /口径差 1/.test(elB('diff-sub').textContent));

// (d) 连 verdicts 都取不到 ⇒ 优雅降级，不抛异常
let threw = null;
let C = null;
try { C = await runPage('c', 'no-data'); } catch (e) { threw = e; }
ok('四个数据源全 404 时不抛异常', threw === null);
ok('全缺时显示「数据不可用」+ 抄得动的生成命令',
  /数据不可用/.test((C ? (C.map.get('dash') || {}).innerHTML : '') || '')
  && /web_verdicts_667\.py --write/.test((C ? (C.map.get('dash') || {}).innerHTML : '') || ''));
ok('全缺时时间线/图表/漂移/差异表四处都走占位（不是空白）',
  ['tl-empty', 'fs-chart', 'drift-bars', 'diff-empty'].every((i) => /chart-empty/.test(((C && C.map.get(i)) || {}).innerHTML || '')));

console.log('verdicts.test: ' + passed + ' assertions passed ✓');
// 诚实边界：第 12 节的 DOM 是**自建最小垫片**，只实现 getElementById / innerHTML /
// textContent / addEventListener / clientWidth 这几个本页用到的 API；它不能替代真浏览器的
// 布局与交互复核（jsdom 在本机不可用，见 tools/web_smoke_667.mjs 的 SKIP 说明）。

