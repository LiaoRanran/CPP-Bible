// ═══════════════════════════════════════════════════════════════════════════
// 672g B · 实验结果页**纯逻辑**（无 DOM / 无 fetch ⇒ Node 里直接真跑）
//
// 由来：experiments.html 里 180–386 行的内联 module 脚本无法被 Node 测试 ——
//   它一边取数合并，一边写 innerHTML，逻辑和 DOM 焊死在一起。672g 把它劈成两层：
//     · 本文件 —— 取数合并 / 口径挑选 / 提示文案（纯函数，tests/experiments_core.test.mjs）
//     · js/experiments.js —— DOM 渲染与事件接线，**不在这里写算法**
//
// 口径纪律（与页面一致，一个字都不改）：
//   · baseline 三源按顺序尝试，**缺的臂不补、不插值、不推测** ⇒ 只标「待670a生成」
//   · 口径消融：同一份分子、三种分母 ⇒ 数字差十几个百分点不是检测能力变化
//   · 演化折线：只有能追溯到批次的真实值才落点，无值批次画空心点
// ═══════════════════════════════════════════════════════════════════════════

import { esc, PENDING, BASELINE_PATHS } from './charts.js';

/** baseline 对比图的三个语料（"全部"tab 的展开结果）。 */
export const ALL_DATASETS = ['holdout', 'corpus', 'defect'];

/** 页面状态初值（纯数据 ⇒ 测试能直接构造，不需要 DOM）。 */
export function initialState() {
  return {
    base: { ok: false, sources: [], tried: [], arms: [] },
    sup: { results: {}, tried: [] },
    exp: null, metrics: null, status: null, graph: null, e669: null,
    arms: [], calibers: null, detectors: [], evolution: null,
    datasets: ALL_DATASETS.slice(), caliber: 'all',
  };
}

/** 数据集 tab → datasets 数组（'all' 展开成三个语料；其余单值；非法值 ⇒ 全部）。 */
export function pickDatasets(v, all = ALL_DATASETS) {
  const list = Array.isArray(all) && all.length ? all : ALL_DATASETS;
  if (v === 'all' || v == null || v === '') return list.slice();
  return [v];
}

/* ── 670a 契约字段合并：多源按 **sources 顺序** 取第一个有值的 ───────────── */

/** 合并某个契约字段（含则用，无则 null；数组要求非空）。 */
export function mergedField(sources, name) {
  for (const s of (Array.isArray(sources) ? sources : [])) {
    const v = s && s.data ? s.data[name] : null;
    if (v && (Array.isArray(v) ? v.length : true)) return v;
  }
  return null;
}
/** 合并 caliber_ablation 口径块。 */
export function mergedCalibers(sources) {
  for (const s of (Array.isArray(sources) ? sources : [])) {
    if (s && s.data && s.data.calibers) return s.data.calibers;
  }
  return null;
}
/** 合并 detectors（要求非空数组）。 */
export function mergedDetectors(sources) {
  for (const s of (Array.isArray(sources) ? sources : [])) {
    if (s && s.data && s.data.detectors && s.data.detectors.length) return s.data.detectors;
  }
  return null;
}

/* ── 提示文案（原本写在 render* 里的字符串拼接，逐字照搬） ───────────────── */

/** ① baseline 图右上角的数据源说明。 */
export function baselineNoteText(sources) {
  const list = Array.isArray(sources) ? sources : [];
  return list.length
    ? ('数据源：' + list.map((s) => (s && s.path) || '(未知路径)').join(' + '))
    : ('三个 baseline 源全部未就绪（' + BASELINE_PATHS.join(' / ') + '）');
}

/** ② 口径消融：按当前口径挑臂（'all' 全看；其余按 key 前缀匹配）+ 兜底（空则回退全臂）。 */
export function caliberArms(calibers, caliber) {
  const cal = calibers || {};
  const arms = Array.isArray(cal.arms) ? cal.arms : [];
  if (caliber === 'all' || caliber == null || caliber === '') return arms.slice();
  const picked = arms.filter((a) => String(a && a.key).indexOf(caliber) === 0);
  return picked.length ? picked : arms.slice();   // 一条都没匹配上 ⇒ 退回全臂（与线上一致）
}
/** ② 口径消融右上角的说明（口径不是 'all' 时恒为 "1 臂" —— 与线上文案一致）。 */
export function caliberNoteText(caliber, totalArms) {
  return ((caliber === 'all' ? Number(totalArms) || 0 : 1) + ' 臂 · 分母不同、分子同源');
}

/** ③ 演化折线：有真实值的批次数（mutation_pct / holdout_pct 任一非 null）。 */
export function realValueBatches(rows) {
  return (Array.isArray(rows) ? rows : [])
    .filter((r) => r && (r.mutation_pct !== null || r.holdout_pct !== null)).length;
}
/** ③ 演化折线右上角的说明。 */
export function evolutionNoteText(evolution) {
  const evo = evolution || {};
  return evo.ok ? ('有真实值的批次 ' + realValueBatches(evo.rows) + ' 个') : '待 670a';
}
/** ③ 批次骨架（"a → b → c"，空 ⇒ '—'）。 */
export function batchesText(batches) {
  return (Array.isArray(batches) && batches.length) ? batches.join(' → ') : '—';
}

/** ④ 检测器构成右上角的说明（pending ⇒ 说明用的是回退口径）。 */
export function detectorNoteText(d) {
  const o = d || {};
  return o.pending ? ('回退口径：' + (o.source || '无') + '（真 detectors 字段待 670a）')
    : '口径：detectors（真实计数）';
}

/** ⑤ 能力构成雷达右上角的说明（缺真实值的轴要写出来，不假装六轴全绿）。 */
export function abilityNoteText(ab) {
  const missing = (ab && Array.isArray(ab.missing)) ? ab.missing : [];
  return missing.length ? ('缺真实值的轴：' + missing.join('、')) : '六轴全部命中真实产物';
}

/* ── 数据源状态（诚实登记 200 / 404，不把 404 说成 200） ──────────────────── */

/** 把 base.tried + sup.tried 合成一条列表（保序）。 */
export function triedItems(base, sup) {
  const out = [];
  const push = (t) => out.push({ path: t && t.path, ok: !!(t && t.ok), error: (t && t.error) || '' });
  (Array.isArray(base && base.tried) ? base.tried : []).forEach(push);
  (Array.isArray(sup && sup.tried) ? sup.tried : []).forEach(push);
  return out;
}
/** 数据源列表的 <li> 串（命中 / 未命中 + 路径 + 失败原因）。 */
export function sourceListHtml(items) {
  return (Array.isArray(items) ? items : []).map((t) => '<li>'
    + (t.ok ? '<span class="dim">命中</span>' : '<span class="dim">未命中</span>')
    + ' <span class="mono">' + esc(t.path) + '</span>'
    + (t.ok ? '' : ' <span class="dim">' + esc(t.error || '失败') + '</span>')
    + '</li>').join('');
}
/** 数据源区块右上角的说明。 */
export function sourceNoteText(hitCount) {
  const hit = Number(hitCount) || 0;
  return hit
    ? ('baseline 命中 ' + hit + '/' + BASELINE_PATHS.length + ' 源 —— 缺的臂不虚构，图里标 n/a')
    : ('baseline 三源全部未就绪 ⇒ baseline / 口径两图显示「' + PENDING + '」（页面其余图仍按真实产物渲染）');
}

/** 异常降级文案（DOM 层的 safe() 捕获异常后写进图表容器，绝不让整页崩）。 */
export function errorText(err) {
  return '渲染异常（已降级，页面其余部分不受影响）：' + String((err && err.message) || err);
}
