// 672g B · 实验结果页纯逻辑验收（无 DOM / 无 jsdom / 零外部依赖）
//
// 跑法（在 web/ 下）：node tests/experiments_core.test.mjs
//
// 由来：experiments.html 里 180–386 行的内联 module 脚本（约 200 行）**无法被 Node 测试**
//   —— 取数合并与 innerHTML 焊在一起。672g 抽成两层后，这层纯逻辑终于能直测：
//     · 多源合并（缺的臂不补、不插值、不推测）
//     · 口径挑选（同一份分子换分母）
//     · 提示文案（200 / 404 诚实登记，不把未命中说成命中）
//
// 不测什么：SVG 像素、fetch 真实网络（由 charts.test.mjs 与 perf 测试覆盖）。
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import * as CORE from '../js/experiments_core.js';
import { BASELINE_PATHS, PENDING } from '../js/charts.js';

let passed = 0;
const ok = (name, cond) => { assert.ok(cond, 'FAIL: ' + name); passed++; };
const eq = (a, b, m) => { assert.equal(a, b, 'FAIL: ' + m + ' (' + a + ' != ' + b + ')'); passed++; };
const has = (s, t, m) => { assert.ok(String(s).indexOf(t) >= 0, 'FAIL: ' + m + '（未含「' + t + '」）'); passed++; };
const lacks = (s, t, m) => { assert.ok(String(s).indexOf(t) < 0, 'FAIL: ' + m + '（不该含「' + t + '」）'); passed++; };

const HTML = readFileSync(new URL('../experiments.html', import.meta.url), 'utf-8');

/* ══ ① 内联脚本已外抽（本批次的存在前提）════════════════════════════════ */
ok('experiments.html 不再有内联 module 逻辑脚本',
  !/<script type="module">\s*\nimport/.test(HTML));
ok('experiments.html 改为外链 js/experiments.js',
  HTML.indexOf('<script type="module" src="js/experiments.js">') > 0);
ok('experiments.html 里不再出现 loadBaselines（逻辑已搬走）',
  HTML.indexOf('loadBaselines') < 0);
ok('js/experiments.js 存在且引用 core',
  readFileSync(new URL('../js/experiments.js', import.meta.url), 'utf-8').indexOf("from './experiments_core.js'") > 0);

/* ══ ② 数据集 tab → datasets ═════════════════════════════════════════════ */
eq(CORE.ALL_DATASETS.length, 3, '三个语料：holdout / corpus / defect');
eq(CORE.ALL_DATASETS.join(','), 'holdout,corpus,defect', '语料顺序与页面一致');
eq(CORE.pickDatasets('all').length, 3, '「全部」⇒ 三个语料全展开');
eq(CORE.pickDatasets('holdout').join(','), 'holdout', '单语料 ⇒ 只留一个');
eq(CORE.pickDatasets('').length, 3, '空值 ⇒ 回退全部（不报错）');
eq(CORE.pickDatasets(null).length, 3, 'null ⇒ 回退全部');
ok('pickDatasets 返回新数组（改它不污染 ALL_DATASETS）',
  (() => { const a = CORE.pickDatasets('all'); a.push('x'); return CORE.ALL_DATASETS.length === 3; })());
const st = CORE.initialState();
eq(st.datasets.join(','), 'holdout,corpus,defect', 'initialState.datasets 默认全展开');
eq(st.caliber, 'all', 'initialState.caliber 默认 all');
eq(st.exp, null, 'initialState.exp 默认 null（未取数不许有假值）');

/* ══ ③ 多源合并：按顺序取第一个有值的，缺的臂不补 ═══════════════════════ */
const noCal = { path: 'a.json', data: { arms: [] } };
const withCal = { path: 'b.json', data: { calibers: { arms: [{ key: 'A_valid_only' }, { key: 'B_unknown_as_miss' }] } } };
const withDet = { path: 'c.json', data: { detectors: [{ k: 'sanitizer', n: 3 }], evolution: [{ b: '670c' }] } };
eq(CORE.mergedField([noCal, withDet], 'evolution').length, 1, 'mergedField：跳过没有该字段的源');
eq(CORE.mergedField([noCal], 'evolution'), null, 'mergedField：全都缺 ⇒ null（不编造）');
eq(CORE.mergedField([{ data: { evolution: [] } }], 'evolution'), null, 'mergedField：空数组视为缺失');
ok('mergedCalibers 命中带 calibers 的源', CORE.mergedCalibers([noCal, withCal]) === withCal.data.calibers);
eq(CORE.mergedCalibers([noCal]), null, 'mergedCalibers：无 ⇒ null');
eq(CORE.mergedDetectors([withDet, withCal]).length, 1, 'mergedDetectors 命中');
eq(CORE.mergedDetectors([{ data: { detectors: [] } }]), null, 'mergedDetectors：空数组不算命中');
eq(CORE.mergedDetectors([]), null, 'mergedDetectors：无源 ⇒ null');
ok('空 sources / null 都不抛异常',
  CORE.mergedField(null, 'x') === null && CORE.mergedCalibers(undefined) === null);

/* ══ ④ 口径消融：同一份分子换分母 ═══════════════════════════════════════ */
const cal = withCal.data.calibers;
eq(CORE.caliberArms(cal, 'all').length, 2, "口径 all ⇒ 两臂全看");
eq(CORE.caliberArms(cal, 'A_valid_only').length, 1, "口径 A ⇒ 按 key 前缀挑出 1 臂");
eq(CORE.caliberArms(cal, 'A_valid_only')[0].key, 'A_valid_only', '挑出来的是对的那条');
eq(CORE.caliberArms(cal, 'ZZZ').length, 2, '匹配不到 ⇒ 回退全臂（与线上一致，不显示空图）');
eq(CORE.caliberArms(null, 'all').length, 0, 'calibers 为 null ⇒ 空数组（由调用方走空状态）');
eq(CORE.caliberNoteText('all', 2), '2 臂 · 分母不同、分子同源', 'all ⇒ 显示总臂数');
eq(CORE.caliberNoteText('A_valid_only', 2), '1 臂 · 分母不同、分子同源', '单口径 ⇒ 恒显示 1 臂');
has(CORE.caliberNoteText('all', 2), '分母不同、分子同源', '口径提示必须提醒"差异来自分母"');

/* ══ ⑤ 演化折线：只有真实值才落点 ═══════════════════════════════════════ */
const rows = [{ mutation_pct: 97.3, holdout_pct: null }, { mutation_pct: null, holdout_pct: 87.5 },
  { mutation_pct: null, holdout_pct: null }];
eq(CORE.realValueBatches(rows), 2, '有真实值的批次 = 2（两列任一非 null）');
eq(CORE.realValueBatches([]), 0, '空 ⇒ 0');
eq(CORE.evolutionNoteText({ ok: true, rows }), '有真实值的批次 2 个', 'ok ⇒ 报真实批次数');
eq(CORE.evolutionNoteText({ ok: false, rows }), '待 670a', '未就绪 ⇒ 「待 670a」（不是 0）');
eq(CORE.evolutionNoteText(null), '待 670a', 'null ⇒ 「待 670a」');
eq(CORE.batchesText(['669c', '670a', '670c']), '669c → 670a → 670c', '批次骨架用 → 连接');
eq(CORE.batchesText([]), '—', '无批次 ⇒ —（不编造批次名）');

/* ══ ⑥ 检测器 / 能力构成的诚实标注 ══════════════════════════════════════ */
eq(CORE.detectorNoteText({ pending: false }), '口径：detectors（真实计数）', '真 detectors 字段 ⇒ 标真实口径');
has(CORE.detectorNoteText({ pending: true, source: '回退分布' }), '回退口径', '回退 ⇒ 必须标明是回退');
has(CORE.detectorNoteText({ pending: true }), '待 670a', '回退 ⇒ 注明真字段待生成');
eq(CORE.abilityNoteText({ missing: [] }), '六轴全部命中真实产物', '无缺失 ⇒ 六轴全绿');
has(CORE.abilityNoteText({ missing: ['mutation', 'nodes'] }), 'mutation、nodes', '缺轴 ⇒ 点名缺哪几轴');

/* ══ ⑦ 数据源状态：200 / 404 诚实登记 ═══════════════════════════════════ */
const items = CORE.triedItems(
  { tried: [{ path: 'x.json', ok: true }, { path: 'y.json', ok: false, error: '404' }] },
  { tried: [{ path: 'z.json', ok: false, error: 'timeout' }] },
);
eq(items.length, 3, 'base.tried + sup.tried 合成 3 条');
eq(items[0].path, 'x.json', '顺序：base 在前');
eq(items[2].error, 'timeout', '失败原因带出来');
const list = CORE.sourceListHtml(items);
has(list, '命中', '命中要有标记');
has(list, '未命中', '未命中要有标记');
has(list, '404', '失败原因要写出来');
eq((list.match(/<li>/g) || []).length, 3, '3 条 ⇒ 3 个 <li>');
// XSS：路径来自配置/异常信息，必须转义
has(CORE.sourceListHtml([{ path: '<img onerror=1>', ok: false, error: '<b>' }]), '&lt;img', '路径转义（防注入）');
lacks(CORE.sourceListHtml([{ path: '<img onerror=1>', ok: false, error: '' }]), '<img', '原文不得留未转义标签');

has(CORE.sourceNoteText(0), PENDING, '0 源命中 ⇒ 明说两图显示「待670a生成」');
has(CORE.sourceNoteText(1), 'baseline 命中 1/' + BASELINE_PATHS.length, '1 源命中 ⇒ 报 x/3');
has(CORE.sourceNoteText(1), '缺的臂不虚构', '必须声明缺的臂不补');
lacks(CORE.sourceNoteText(1), PENDING, '有命中时不再说"全部未就绪"');

/* ══ ⑧ baseline 数据源说明 + 异常降级 ════════════════════════════════════ */
has(CORE.baselineNoteText([]), BASELINE_PATHS[0], '未就绪 ⇒ 三个源路径全列出来');
eq(CORE.baselineNoteText([{ path: 'a.json' }, { path: 'b.json' }]), '数据源：a.json + b.json', '命中 ⇒ 列实际路径');
has(CORE.errorText(new Error('炸了')), '渲染异常（已降级', '异常文案标明已降级');
has(CORE.errorText(new Error('炸了')), '炸了', '异常原因带出来');

console.log('experiments_core: ' + passed + ' assertions passed');
