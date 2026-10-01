// 670c A2 · Node 真求值：web/js/charts.js 纯逻辑测试
// 跑法（在 web/ 目录）：node tests/charts.test.mjs
// 无 DOM / 无 jsdom / 无第三方依赖；DOM 只出现在 barChart/pieChart 两个旧适配器，用假容器验证。
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import {
  wilsonCI, describeSample, esc, niceCeil, valLabel,
  parseBaseline, normalizeDatasetKey, datasetRatePct, normalizeArm, parseCalibers, caliberLabel,
  buildGroupedBars, buildCaliberBars, buildLineChart, buildPie, buildRadar,
  emptyStateSvg, renderChart, selectionFromDataset, selectionDetail, detailPanelHtml,
  composeArms, loadBaselines, loadBaselineData, loadSupplements,
  buildEvolutionSeries, buildDetectorSlices, buildAbilityAxes, sortPointsByBatch,
  barChart, pieChart, BASELINE_PATHS, PENDING, DATASET_KEYS,
} from '../js/charts.js';

let passed = 0;
const ok = (name, cond) => { assert.ok(cond, 'FAIL: ' + name); passed++; };
const near = (name, a, b, eps) => {
  const e = eps === undefined ? 5e-5 : eps;
  assert.ok(typeof a === 'number' && Math.abs(a - b) <= e, 'FAIL: ' + name + ' → ' + a + ' != ' + b);
  passed++;
};

/* ════════════ 1 · Wilson 区间（真值对照 tools/stat_bounds.py）════════════ */
// 期望值由仓库自带的 python 现算：python tools/stat_bounds.py wilson --k K --n N
const w1416 = wilsonCI(14, 16);
near('wilson(14,16).lo = 0.6398', w1416.lo, 0.6398);
near('wilson(14,16).hi = 0.9650', w1416.hi, 0.9650);
near('wilson(14,16).p = 0.875', w1416.p, 0.875);
const w1432 = wilsonCI(14, 32);
near('wilson(14,32).lo = 0.2817', w1432.lo, 0.2817);
near('wilson(14,32).hi = 0.6067', w1432.hi, 0.6067);
const w1440 = wilsonCI(14, 40);
near('wilson(14,40).lo = 0.2213', w1440.lo, 0.2213);
near('wilson(14,40).hi = 0.5049', w1440.hi, 0.5049);
const w19 = wilsonCI(1, 9);
near('wilson(1,9).lo = 0.0199', w19.lo, 0.0199);
near('wilson(1,9).hi = 0.4350', w19.hi, 0.4350);

// 边界：k=0 / k=n / n=0
const w0 = wilsonCI(0, 16);
ok('wilson(0,16).lo 恰为 0（不是 1e-17）', w0.lo === 0);
near('wilson(0,16).hi = 0.1936', w0.hi, 0.1936);
near('wilson(0,10).hi < 0.4（与 stat_bounds selftest 同界）', wilsonCI(0, 10).hi, 0.27756);
const wn = wilsonCI(16, 16);
ok('wilson(16,16).hi 恰为 1', wn.hi === 1);
near('wilson(16,16).lo = 0.8064', wn.lo, 0.8064);
ok('wilson(k,0) = null', wilsonCI(0, 0) === null);
ok('wilson(3,0) = null（n<=0 不编造 0/1）', wilsonCI(3, 0) === null);
const clamp = wilsonCI(20, 16);
ok('k>n 被夹到 n（p=1, hi=1）', clamp.p === 1 && clamp.hi === 1);
const sym = wilsonCI(3, 20);
near('对称性 hi(k,n) = 1 - lo(n-k,n)', sym.hi, 1 - wilsonCI(17, 20).lo);

// 区间性质：lo <= p <= hi，且不越界
for (const kn of [[0, 1], [1, 1], [2, 7], [13, 17], [99, 100]]) {
  const c = wilsonCI(kn[0], kn[1]);
  ok('区间包含点估计 ' + kn[0] + '/' + kn[1], c.lo <= c.p + 1e-12 && c.p <= c.hi + 1e-12 && c.lo >= 0 && c.hi <= 1);
}

/* ════════════ 2 · 明细文本 describeSample ════════════ */
ok('describeSample(14,16) 全文', describeSample(14, 16) === '14/16 = 87.5%（Wilson 95% CI：64.0% – 96.5%）');
ok('describeSample 用传入的 ci', describeSample(7, 10, { lo: 0.4, hi: 0.9 }).indexOf('40.0% – 90.0%') > 0);
ok('describeSample(0,0) 明说不可估', describeSample(0, 0).indexOf('n=0') > 0);
ok('describeSample(k=null,n=5) 不编 k', describeSample(null, 5).indexOf('k 缺失') > 0);
ok('valLabel 非百分号单位不加 %', valLabel(452, '') === '452' && valLabel(97.34, '%') === '97.3%');
ok('niceCeil 87.5 ⇒ 100 / 43.8 ⇒ 50', niceCeil(87.5) === 100 && niceCeil(43.8) === 50);

/* ════════════ 3 · 解析（缺失填 null、永不抛）════════════ */
const FIX_STATIC = {
  schema: 'queyi-baseline/v1', arm: 'static', label: 'Static（静态规则）', generated_at: '2026-10-01T00:00:00',
  datasets: {
    holdout: { k: 9, n: 16, samples: [{ id: 'H-001', verdict: 'catch' }, { id: 'H-002', verdict: 'miss', note: 'x' }] },
    corpus: { k: 4, n: 32, note: '全样本 40' },
  },
  detectors: { 'perf': 1, sanitizer: 8, 'compile-time': 1, 'cross-compile': 2, 'compiler-warn': 5 },
  evolution: [{ batch: '656', mutation_pct: 61.2, holdout_pct: 50 }],
};
const p = parseBaseline(FIX_STATIC);
ok('三个数据集键恒存在', DATASET_KEYS.every((k) => k in p.datasets));
ok('缺 defect ⇒ null 且进 missing', p.datasets.defect === null && p.missing.length === 1 && p.missing[0] === 'defect');
ok('k/n ⇒ rate_pct 现算 56.25', p.datasets.holdout.k === 9 && p.datasets.holdout.n === 16 && Math.abs(p.datasets.holdout.rate_pct - 56.25) < 1e-9);
ok('无 CI ⇒ 现算 Wilson(9,16)', Math.abs(p.datasets.holdout.ci.lo - wilsonCI(9, 16).lo) < 1e-12);
ok('samples 归一（id/verdict/note）', p.datasets.holdout.samples.length === 2 && p.datasets.holdout.samples[1].note === 'x');
ok('单臂合成（arm=static）', p.arms.length === 1 && p.arms[0].key === 'static');
ok('corpus 注记保留', p.datasets.corpus.note === '全样本 40');
ok('detectors 归一并按固定口径排序', p.detectors.length === 5 && p.detectors.map((d) => d.key).join(',') === 'sanitizer,compiler-warn,cross-compile,perf,compile-time');
ok('evolution 归一', p.evolution.length === 1 && p.evolution[0].batch === '656' && p.evolution[0].mutation_pct === 61.2);
ok('parseBaseline(null) 不抛且 ok=false', parseBaseline(null).ok === false && parseBaseline(null).datasets.holdout === null);
ok('parseBaseline(字符串) 不抛', parseBaseline('nope').missing.length === 3);
ok('parseBaseline({}) 不抛', parseBaseline({}).datasets.corpus === null);
ok('缺字段填 null（不填 0）', parseBaseline({ datasets: { holdout: {} } }).datasets.holdout.k === null);
ok('nil 数据集 ⇒ null', normalizeDatasetSafe());
function normalizeDatasetSafe() {
  const q = parseBaseline({ datasets: { holdout: null } });
  return q.datasets.holdout === null;
}
ok('别名归一 external⇒corpus / 真错⇒holdout / 缺陷注入⇒defect',
  normalizeDatasetKey('external 可测口径') === 'corpus' && normalizeDatasetKey('holdout 真错（双档）') === 'holdout' && normalizeDatasetKey('defect（缺陷注入）') === 'defect');
ok('rate_pct 与 k/n 冲突被显式记下', parseBaseline({ datasets: { holdout: { k: 1, n: 4, rate_pct: 50 } } }).datasets.holdout.conflicts.length === 1);

// 669_experiments.json 的形态（baselines 逐行 + caliber_ablation）
const FIX_669 = {
  schema: 'queyi-experiments/v1',
  registry: { experiment: '669 P3 实验启动', honest_note: '只做全量复算' },
  baselines: [
    { name: 'holdout 真错（双档，可测口径）', k: 14, n: 16, rate_pct: 87.5, wilson_lo_pct: 64.0, wilson_hi_pct: 96.5, cp_lo_pct: 61.7, cp_hi_pct: 98.4, exploratory: true },
    { name: 'external 可测口径', k: 14, n: 32, rate_pct: 43.8, wilson_lo_pct: 28.2, wilson_hi_pct: 60.7 },
    { name: 'external 全样本口径', k: 14, n: 40, rate_pct: 35.0, wilson_lo_pct: 22.1, wilson_hi_pct: 50.5 },
    { name: 'external 层 C（无可用检测器）', k: 0, n: 0, rate_pct: null },
  ],
  caliber_ablation: {
    arms: {
      'A_valid_only（本批主口径：unknown 剔除）': { holdout: { k: 14, n: 16, rate_pct: 87.5 }, external: { k: 14, n: 32, rate_pct: 43.8 } },
      'B_unknown_as_miss（保守：unknown 记 miss）': { holdout: { k: 14, n: 17, rate_pct: 82.4 }, external: { k: 14, n: 37, rate_pct: 37.8 } },
      'C_all_samples（最保守：unknown + not_error 都进分母）': { holdout: { k: 14, n: 17, rate_pct: 82.4 }, external: { k: 14, n: 40, rate_pct: 35.0 } },
    },
    delta_pp: { holdout: { A_minus_C_pp: 5.1 }, external: { A_minus_C_pp: 8.8 } },
    note: '三臂共用同一份原始计数',
  },
};
const p669 = parseBaseline(FIX_669);
ok('669 形态：逐行 baselines ⇒ 单臂 + rowArms 保留 4 行', p669.arms.length === 1 && p669.rowArms.length === 4);
ok('669 形态：臂 key = failure-driven', p669.arms[0].key === 'failure-driven');
ok('669 形态：holdout 取首行 14/16', p669.datasets.holdout.k === 14 && p669.datasets.holdout.n === 16);
ok('669 形态：产物自带 wilson 被采信（64.0/96.5）', Math.abs(p669.datasets.holdout.ci.lo * 100 - 64.0) < 1e-9 && p669.datasets.holdout.ci.provided === true);
ok('669 形态：C-P 区间也解析', Math.abs(p669.datasets.holdout.cp.hi * 100 - 98.4) < 1e-9);
ok('669 形态：corpus 取 external 可测 14/32', p669.datasets.corpus.k === 14 && p669.datasets.corpus.n === 32);
ok('669 形态：0/0 行不编造率值', p669.rowArms[3].datasets.corpus.rate_pct === null || p669.rowArms[3].datasets.corpus.rate_pct === undefined);
ok('669 形态：n=0 ⇒ ci=null', p669.rowArms[3].datasets.corpus.ci === null);
ok('口径解析：三臂', p669.calibers.arms.length === 3);
ok('口径中文短名（可测 / 排除 unknown / 全样本）',
  caliberLabel('A_valid_only（本批主口径：unknown 剔除）').indexOf('可测') === 0
  && caliberLabel('B_unknown_as_miss（保守）').indexOf('排除 unknown') === 0
  && caliberLabel('C_all_samples（最保守）').indexOf('全样本') === 0);
ok('口径臂数据集键归一 external⇒corpus', p669.calibers.datasets.join(',') === 'holdout,corpus');
ok('口径 Δpp 转文本', p669.calibers.delta_pp.external.indexOf('8.8') > 0);
ok('parseCalibers(null) = null', parseCalibers(null) === null);

/* ════════════ 4 · 组合臂 / 加载（含全失败降级）════════════ */
const fixedArms = composeArms([
  { path: 'data/experiments/baseline_static.json', data: parseBaseline(FIX_STATIC) },
  { path: 'data/experiments/669_experiments.json', data: parseBaseline(FIX_669) },
]);
ok('composeArms：Static 优先、Failure-driven 在后', fixedArms.map((a) => a.key).join(',') === 'static,failure-driven');
ok('composeArms：标签与配色齐备', fixedArms[0].label.indexOf('Static') === 0 && !!fixedArms[0].color && !!fixedArms[1].color);
ok('composeArms：数据集来自各自源', fixedArms[0].datasets.holdout.k === 9 && fixedArms[1].datasets.holdout.k === 14);

const fetched = [];
const fakeFetch = async (url) => {
  fetched.push(url);
  if (url.indexOf('baseline_static') >= 0) return FIX_STATIC;
  if (url.indexOf('baseline_random') >= 0) throw new Error(url + ' → HTTP 404');
  if (url.indexOf('669_experiments') >= 0) return FIX_669;
  throw new Error(url + ' → HTTP 404');
};
const loaded = await loadBaselines(fakeFetch);
ok('loadBaselines：按 BASELINE_PATHS 顺序尝试', fetched.join('|') === BASELINE_PATHS.join('|'));
ok('loadBaselines：成功/失败逐条记录', loaded.tried[0].ok === true && loaded.tried[1].ok === false && loaded.tried[2].ok === true);
ok('loadBaselines：失败原因带 HTTP 404', loaded.tried[1].error.indexOf('404') > 0);
ok('loadBaselines：合成两臂（random 缺 ⇒ 不虚构）', loaded.arms.map((a) => a.key).join(',') === 'static,failure-driven');

const allFail = await loadBaselines(async (u) => { throw new Error(u + ' → HTTP 404'); });
ok('全部 404 ⇒ ok=false、arms 空、不抛', allFail.ok === false && allFail.arms.length === 0 && allFail.sources.length === 0);
const noFetch = await loadBaselines(null);
ok('fetchJson 不可用也不抛', noFetch.ok === false && noFetch.tried[0].error.indexOf('fetchJson') === 0);
const first = await loadBaselineData(fakeFetch);
ok('loadBaselineData：取第一个成功源', first.ok === true && first.path === BASELINE_PATHS[0] && first.data.datasets.holdout.k === 9);
const sup = await loadSupplements(async (u) => { if (u.indexOf('graph') >= 0) throw new Error('404'); return { ok: 1 }; });
ok('loadSupplements：单源失败不影响其它', sup.results.graph === null && sup.results.metrics666.ok === 1 && sup.tried.filter((t) => t.ok).length === 3);

/* ════════════ 5 · SVG 渲染（关键元素 / data-* / 误差线）════════════ */
const barSpec = {
  title: 'baseline 对比 · 检出率（%）', unit: '%', max: 100,
  arms: fixedArms, datasets: ['holdout', 'corpus', 'defect'],
};
const bars = buildGroupedBars(barSpec);
ok('柱状图：role="img" + <title>', bars.indexOf('role="img"') > 0 && bars.indexOf('<title>') > 0);
ok('柱状图：svg 根 + viewBox', bars.indexOf('<svg') === 0 && bars.indexOf('viewBox="0 0 760 340"') > 0);
ok('柱状图：4 根真实柱（2 臂 × holdout/corpus）', (bars.match(/class="bar"/g) || []).length === 4);
ok('柱状图：defect 缺 ⇒ 2 根幽灵柱 is-missing', (bars.match(/bar is-missing/g) || []).length === 2);
ok('柱状图：每柱误差线 err-bar（4 根）', (bars.match(/class="err-bar"/g) || []).length === 4);
ok('柱状图：每柱两个误差帽 err-cap（8 个）', (bars.match(/class="err-cap"/g) || []).length === 8);
ok('柱状图：数值标签 87.5%', bars.indexOf('>87.5%<') > 0 && bars.indexOf('class="bar-val"') > 0);
ok('柱状图：data-arm/data-dataset/data-k/data-n', bars.indexOf('data-arm="static"') > 0 && bars.indexOf('data-dataset="holdout"') > 0 && bars.indexOf('data-k="9"') > 0 && bars.indexOf('data-n="16"') > 0);
ok('柱状图：data-ci-lo/data-ci-hi（误差线可被点击读到）', bars.indexOf('data-ci-lo="') > 0 && bars.indexOf('data-ci-hi="') > 0);
ok('柱状图：键盘可聚焦 tabindex="0"', bars.indexOf('tabindex="0"') > 0);
ok('柱状图：网格/轴/刻度类齐备', bars.indexOf('class="grid-line"') > 0 && bars.indexOf('class="axis-line"') > 0 && bars.indexOf('class="tick-label"') > 0);
const barsSel = buildGroupedBars(Object.assign({}, barSpec, { selected: { arm: 'static', dataset: 'holdout' } }));
ok('柱状图：选中态加 is-selected', barsSel.indexOf('class="bar is-selected"') > 0);
ok('柱状图：无臂 ⇒ 空状态（不抛）', buildGroupedBars({ arms: [] }).indexOf(PENDING) > 0);

const calSvg = buildCaliberBars({ calibers: p669.calibers, title: '口径消融' });
ok('口径图：3 臂 × 2 数据集 = 6 柱', (calSvg.match(/class="bar"/g) || []).length === 6);
ok('口径图：data-caliber 标注 + 中文口径名', calSvg.indexOf('data-caliber="') > 0 && calSvg.indexOf('可测（unknown 剔除）') > 0);
ok('口径图：Δpp 注记进入 svg', calSvg.indexOf('A_minus_C_pp=8.8') > 0);
const calFromRaw = buildCaliberBars({ arms: FIX_669.caliber_ablation.arms });
ok('口径图：直接喂原始 arms 映射也能画', (calFromRaw.match(/class="bar"/g) || []).length === 6);
ok('口径图：无数据 ⇒ 空状态', buildCaliberBars({}).indexOf(PENDING) > 0);

const lineSvg = buildLineChart({
  title: '演化', unit: '%', yMax: 100, xLabels: ['656', '666', '669'],
  series: [{ key: 'holdout', label: 'holdout 检出率', color: 'var(--color-accent)', points: [{ x: '656', y: 74.8 }, { x: '666', y: 87.5 }, { x: '669', y: null }] }],
});
ok('折线：line-path 存在且为单条系列', lineSvg.indexOf('class="line-path"') > 0 && (lineSvg.match(/class="line-path"/g) || []).length === 1);
ok('折线：3 个点（2 实心 + 1 空心缺值）', (lineSvg.match(/class="line-dot"/g) || []).length === 2 && (lineSvg.match(/class="line-dot is-missing"/g) || []).length === 1);
ok('折线：缺值点不连线（path 只含 2 个坐标）', (lineSvg.match(/class="line-path" d="([^"]*)"/) || ['', ''])[1].split(' L').length === 2);
ok('折线：网格 + 双轴刻度 + 点 data-*', lineSvg.indexOf('class="grid-line"') > 0 && lineSvg.indexOf('class="tick-label"') > 0 && lineSvg.indexOf('data-x="666"') > 0 && lineSvg.indexOf('data-y="87.5"') > 0);
ok('折线：空输入 ⇒ 空状态', buildLineChart([]).indexOf(PENDING) > 0);
ok('折线：批次排序（645/646 在 656 前）', sortPointsByBatch([{ x: '656' }, { x: '645/646' }, { x: '669' }]).map((q) => q.x).join(',') === '645/646,656,669');

const pieSvg = buildPie({
  title: '检测器构成',
  slices: [{ key: 'sanitizer', label: 'sanitizer', value: 8 }, { key: 'compiler-warn', label: 'compiler-warn', value: 5 }, { key: 'perf', label: 'perf', value: 1 }],
});
ok('饼图：3 个扇区 data-key', (pieSvg.match(/class="pie-seg"/g) || []).length === 3 && pieSvg.indexOf('data-key="sanitizer"') > 0);
ok('饼图：data-value/data-pct/data-total', pieSvg.indexOf('data-value="8"') > 0 && pieSvg.indexOf('data-pct="57.1"') > 0 && pieSvg.indexOf('data-total="14"') > 0);
ok('饼图：图例含计数与百分比', pieSvg.indexOf('8 · 57.1%') > 0);
const dOnly = (buildPie({ slices: [{ label: 'only', value: 3 }] }).match(/ d="([^"]*)"/) || ['', ''])[1];
ok('饼图：单扇区退化画整圆（两条弧命令、无半径线）', (dOnly.match(/ a/g) || []).length === 2 && dOnly.indexOf(' L') < 0);
ok('饼图：全零 ⇒ 空状态', buildPie({ slices: [{ label: 'x', value: 0 }] }).indexOf(PENDING) > 0);

/* ════════════ 6 · 真实产物 → 图表输入（拿仓库现算值对照）════════════ */
const dir = (f) => new URL(f, import.meta.url);
const metrics666 = JSON.parse(readFileSync(dir('../data/metrics_666.json'), 'utf8'));
const status = JSON.parse(readFileSync(dir('../data/status.json'), 'utf8'));
const experiments = JSON.parse(readFileSync(dir('../data/experiments.json'), 'utf8'));
const graph = JSON.parse(readFileSync(dir('../data/graph.json'), 'utf8'));

const ab = buildAbilityAxes({ metrics666, status, experiments, graphNodes: graph.nodes.length });
const byKey = {};
ab.axes.forEach((a) => { byKey[a.key] = a; });
ok('能力雷达：6 个轴', ab.axes.length === 6);
ok('能力雷达：规则 67（status.json）', byKey.rules.value === 67);
ok('能力雷达：保护器 9（status.json）', byKey.protectors.value === 9);
ok('能力雷达：账本 452（metrics_666.json）', byKey.ledger.value === 452);
ok('能力雷达：知识卡 42（metrics_666.json）', byKey.cards.value === 42);
ok('能力雷达：节点数取自 graph.json 现算', byKey.nodes.value === graph.nodes.length && graph.nodes.length > 0);
ok('能力雷达：目标 = 67/9/452/42/178/100', ab.axes.map((a) => a.max).join(',') === '67,9,452,42,178,100');
// 672g 数字同步：真值源 data/656_mutation_report_core.json 的 kill_rate_on_scored
//   在 672f「W1 实验抢救（固定种子 + baseline 新分母重跑）」后由 97.3 → 96.5
//   （killed 110 / on_scored 114 = 147 − import_error 29 − timeout 4）。
//   本断言原来锁死 97.3 ⇒ 前端一直红在一条**已经过期的快照**上，不是页面错。
ok('能力雷达：变异 96.5（experiments.json core·on_scored）', byKey.mutation.value === 96.5);
ok('能力雷达：真实源全部命中 ⇒ 无缺失', ab.missing.length === 0);
const radarSvg = buildRadar({ title: '能力构成', axes: ab.axes });
ok('雷达：网格/轴/数据面类齐备', radarSvg.indexOf('class="radar-grid"') > 0 && radarSvg.indexOf('class="radar-axis"') > 0 && radarSvg.indexOf('class="radar-area"') > 0);
ok('雷达：6 个轴点带 data-axis/data-max', (radarSvg.match(/data-axis=/g) || []).length === 6 && radarSvg.indexOf('data-max="178"') > 0);
ok('雷达：轴标签含真实值（门禁规则 67）', radarSvg.indexOf('门禁规则 67') > 0);
const radarMiss = buildRadar({ axes: [{ key: 'a', label: 'A', value: 1, max: 1 }, { key: 'b', label: 'B', value: null, max: 2 }, { key: 'c', label: 'C', value: 1, max: 1 }] });
ok('雷达：缺值轴画 0 并标 data-missing', radarMiss.indexOf('data-missing="1"') > 0 && radarMiss.indexOf('data-axis="b"') > 0);
ok('雷达：轴 <3 ⇒ 空状态', buildRadar({ axes: [{ label: 'A', value: 1 }, { label: 'B', value: 2 }] }).indexOf(PENDING) > 0);

const evo = buildEvolutionSeries({ metrics666, experiments, experiments669: FIX_669, evolution: FIX_STATIC.evolution });
ok('演化：批次骨架来自 timeline 且按号排序', evo.batches[0] === '641' && evo.batches[evo.batches.length - 1] === '669'
  && evo.batches.join(',') === '641,645/646,647,656,661/664/665,666,669');
ok('演化：没有 669 源就不虚构 669 批次', buildEvolutionSeries({ metrics666 }).batches.indexOf('669') < 0);
ok('演化：656 用 evolution 契约值 61.2', evo.rows.filter((r) => r.batch === '656')[0].mutation_pct === 61.2);
// 672g 数字同步：同上一处，672f 新分母重跑后 97.3 → 96.5（真值源 656_mutation_report_core.json）
ok('演化：666 变异率 96.5（experiments.json 真实值）', evo.rows.filter((r) => r.batch === '666')[0].mutation_pct === 96.5);
// 672g 数字同步：holdout 在 672f「W1 实验抢救」后由 16 样本扩到 22（catch 14→17、miss 2→4、
//   den 16→21）⇒ 检出率 87.5 → 81.0；672h「W3 扩样」再扩到 41（catch 34、miss 7）⇒ 81.0 → 82.9。
//   真值源 web/data/metrics_666.json::metrics.holdout.rate_pct（工具重生成，非手改）。
ok('演化：666 holdout 82.9（metrics_666.json 真实值）', evo.rows.filter((r) => r.batch === '666')[0].holdout_pct === 82.9);
ok('演化：641 无真实值 ⇒ 显式 null 不插值', evo.rows.filter((r) => r.batch === '641')[0].mutation_pct === null);
ok('演化：两条序列（变异 / holdout）', evo.series.length === 2 && evo.series[0].key === 'mutation' && evo.series[1].key === 'holdout');
ok('演化：折线可渲染', buildLineChart({ series: evo.series, xLabels: evo.batches, unit: '%', yMax: 100 }).indexOf('class="line-path"') > 0);

const dets = buildDetectorSlices({ detectors: { 'perf': 1, sanitizer: 8, 'compile-time': 1, 'cross-compile': 2, 'compiler-warn': 5 } });
ok('检测器构成：固定口径顺序', dets.slices.map((d) => d.key).join(',') === 'sanitizer,compiler-warn,cross-compile,perf,compile-time');
ok('检测器构成：pending=false（有真 detectors 字段）', dets.pending === false);
const detsFb = buildDetectorSlices({ experiments });
// 672h：holdout 扩样到 41 后回退分布 = catch 34 / miss 7 / unknown 1（真值源 experiments.json::holdout_outcomes）
ok('检测器构成：缺字段回退 holdout 结果分布并标 pending', detsFb.pending === true && detsFb.slices.length === 3 && detsFb.slices[0].value === 34);
ok('检测器构成：两处都缺 ⇒ 空 slices', buildDetectorSlices({}).slices.length === 0);

/* ════════════ 7 · 空状态 / 分派 ════════════ */
const emp = emptyStateSvg('baseline_static.json 404：待 670a 写入 data/experiments/');
ok('空状态：必含「待670a生成」', emp.indexOf(PENDING) > 0);
ok('空状态：role="img" + <title>', emp.indexOf('role="img"') > 0 && emp.indexOf('<title>' + PENDING + '</title>') > 0);
ok('空状态：透传说明文本', emp.indexOf('baseline_static.json 404') > 0);
ok('空状态：不给 msg 也含「待670a生成」', emptyStateSvg().indexOf(PENDING) > 0);
ok('renderChart("bars", 空) ⇒ 空状态不抛', renderChart('bars', {}).indexOf(PENDING) > 0);
ok('renderChart 未知 kind ⇒ 空状态', renderChart('nope', { emptyMsg: 'x' }).indexOf(PENDING) > 0);
ok('renderChart 对象分派 pie', renderChart({ slices: [{ label: 'a', value: 1 }] }).indexOf('class="pie-seg"') > 0);
ok('renderChart("caliber") 分派', renderChart('caliber', { calibers: p669.calibers }).indexOf('data-caliber="') > 0);

/* ════════════ 8 · 交互：选中 → 明细 ════════════ */
const sel = selectionFromDataset({ role: 'bar', chart: 'grouped', arm: 'static', dataset: 'holdout', k: '14', n: '16', 'ci-lo': '64', 'ci-hi': '96.5', pct: '87.5' });
ok('selectionFromDataset：字符串属性归一成数字', sel.kind === 'bar' && sel.k === 14 && sel.n === 16 && sel.ciLo === 64 && sel.ciHi === 96.5);
ok('selectionFromDataset：DOM dataset 驼峰也认', selectionFromDataset({ role: 'pie', key: 'sanitizer', value: '8', total: '14' }).kind === 'pie');
ok('selectionFromDataset：line/radar 分派', selectionFromDataset({ role: 'line', series: 'holdout', x: '666', y: '87.5' }).kind === 'line' && selectionFromDataset({ role: 'radar', axis: 'rules', value: '67' }).kind === 'radar');

const det = selectionDetail({ arms: fixedArms }, { kind: 'bar', arm: 'static', dataset: 'holdout' });
const rowOf = (d, k) => (d.rows.filter((r) => r[0] === k)[0] || [])[1];
ok('明细：k / n 行 = 9 / 16', rowOf(det, 'k / n') === '9 / 16');
ok('明细：检出率 56.3%', rowOf(det, '检出率') === '56.3%');
const ci916 = wilsonCI(9, 16);
ok('明细：CI 行 = wilsonCI(9,16)（python 对照 33.2% / 76.9%）',
  rowOf(det, 'Wilson 95% CI') === (ci916.lo * 100).toFixed(1) + '% – ' + (ci916.hi * 100).toFixed(1) + '%'
  && rowOf(det, 'Wilson 95% CI') === '33.2% – 76.9%');
ok('明细：文本含 k/n/百分比/CI', det.text.indexOf('9/16 = 56.3%') > 0 && det.text.indexOf('Wilson 95% CI') > 0);
ok('明细：样本列表逐条列出', rowOf(det, '样本列表') === 'H-001、H-002');
const detNoSample = selectionDetail({ arms: [{ key: 'x', label: 'X', datasets: { holdout: { k: 1, n: 2 } } }] }, { kind: 'bar', arm: 'x', dataset: 'holdout' });
ok('明细：无样本清单时明说（不伪造）', rowOf(detNoSample, '样本列表').indexOf('未附逐样本清单') > 0);
ok('明细：n=0 ⇒ 不可估', selectionDetail(null, { kind: 'bar', arm: 'x', dataset: 'holdout', k: '0', n: '0' }).text.indexOf('不可估') > 0);
ok('明细：饼图占比行', rowOf(selectionDetail(null, { kind: 'pie', key: 'sanitizer', label: 'sanitizer', value: 8, total: 14 }), '占比') === '57.1%');
ok('明细：雷达完成度行', rowOf(selectionDetail(null, { kind: 'radar', axis: 'rules', label: '门禁规则', value: 67, max: 67, unit: '' }), '完成度') === '100.0%');
const html = detailPanelHtml(det);
ok('明细 HTML：dl/dt/dd 结构', html.indexOf('<dl>') > 0 && html.indexOf('<dt>k / n</dt><dd>9 / 16</dd>') > 0);
ok('明细 HTML：空选中给提示', detailPanelHtml(null).indexOf('点击柱子') > 0);

/* ════════════ 9 · 转义安全（防注入）════════════ */
ok('esc 转义 &<>"\'', esc('<b a="1">&\'x</b>') === '&lt;b a=&quot;1&quot;&gt;&amp;&#39;x&lt;/b&gt;');
const evilSvg = buildGroupedBars({
  arms: [{ key: 'a" onmouseover="alert(1)', label: '</title><script>alert(1)</script>', datasets: { holdout: { k: 1, n: 2 } } }],
  datasets: ['holdout'],
});
ok('柱状图：标签中的 <script> 被转义', evilSvg.indexOf('<script>') < 0 && evilSvg.indexOf('&lt;script&gt;') > 0);
ok('柱状图：属性里的引号被转义（无法逃出 data-arm）', evilSvg.indexOf('a&quot; onmouseover=&quot;alert(1)') > 0);
ok('柱状图：</title> 未提前闭合标题', evilSvg.indexOf('</title><script') < 0);
ok('饼图：标签转义', buildPie({ slices: [{ label: '<b>x</b>', value: 2 }] }).indexOf('<b>x</b>') < 0);
ok('雷达：标签转义', buildRadar({ axes: [{ label: '<i>a</i>', value: 1, max: 1 }, { label: 'b', value: 1, max: 1 }, { label: 'c', value: 1, max: 1 }] }).indexOf('<i>a</i>') < 0);
ok('空状态：msg 转义', emptyStateSvg('<img src=x onerror=1>').indexOf('<img') < 0);
ok('明细 HTML：值转义', detailPanelHtml(selectionDetail({ arms: [{ key: 'a', label: '<script>x</script>', datasets: { holdout: { k: 1, n: 2 } } }] }, { kind: 'bar', arm: 'a', dataset: 'holdout' })).indexOf('<script>') < 0);

/* ════════════ 10 · 旧接口兼容（web/tests/smoke.mjs 用）════════════ */
const host = { innerHTML: '' };
barChart(host, [{ label: 'a', value: 5 }, { label: 'b', value: 3 }], {});
ok('barChart(旧)：写入容器且为 <svg>', host.innerHTML.indexOf('<svg') === 0 && host.innerHTML.indexOf('role="img"') > 0);
ok('barChart(旧)：两根柱 + 数值标签', (host.innerHTML.match(/class="bar"/g) || []).length === 2 && host.innerHTML.indexOf('>5<') > 0);
pieChart(host, [{ label: 'x', value: 1 }, { label: 'y', value: 2 }]);
ok('pieChart(旧)：两扇区', (host.innerHTML.match(/class="pie-seg"/g) || []).length === 2);

/* ════════════ 11 · 真实 669 产物对照（文件缺失则跳过，不影响上述断言）════════════ */
const frozen669 = new URL('../../data/experiments/669_experiments.json', import.meta.url);
if (existsSync(frozen669)) {
  const real669 = JSON.parse(readFileSync(frozen669, 'utf8'));
  const real = parseBaseline(real669);
  ok('真产物 669：holdout 14/16 = 87.5（与 JSON rate_pct 一致）', real.datasets.holdout.k === 14 && real.datasets.holdout.n === 16 && real.datasets.holdout.rate_pct === 87.5);
  ok('真产物 669：现算 Wilson 命中产物自带的 64.0 / 96.5', Math.abs(wilsonCI(14, 16).lo * 100 - 64.0) < 0.05 && Math.abs(wilsonCI(14, 16).hi * 100 - 96.5) < 0.05);
  ok('真产物 669：外部可测 14/32 命中 28.2 / 60.7', Math.abs(wilsonCI(14, 32).lo * 100 - real.datasets.corpus.ci.lo * 100) < 0.05);
  ok('真产物 669：口径三臂 + 中文短名', real.calibers.arms.length === 3 && real.calibers.arms[0].label.indexOf('可测') === 0);
  ok('真产物 669：三臂同源不同分母（A/B/C holdout n = 16/17/17）', real.calibers.arms.map((a) => a.datasets.holdout.n).join(',') === '16,17,17');
} else {
  console.log('SKIP: data/experiments/669_experiments.json 不存在（670a 可能已改路径）— 已用内联 669 形态夹具覆盖同款断言');
}

console.log('charts.test: ' + passed + ' assertions passed ✓');
