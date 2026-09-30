// 667 阶段2 · 判决页**纯逻辑层**（无 DOM、无 fetch ⇒ 可被 Node 真求值）
//
// 为什么单独抽一层：666 的教训是"改了代码没重跑落盘"，而前端最容易出这类事的
// 地方正是"渲染时才算的逻辑"（DOM 里算 → 没人测 → 静默错）。照 655 的
// `graph_core.js` / `verify_core.js` 先例，把**筛选 / 排序 / 取值**抽成纯函数，
// `tools/web_logic_check_667.mjs` 可以直接 import 并断言。
//
// 纪律：这里**不写死任何数字**。所有数字来自 web/data/verdicts_667.json。

/** 四态排序权重：**越"确定地坏"越靠后**；筛选与排序共用同一张表，避免两处口径不一致。 */
export const STATE_ORDER = { pass: 0, pass_with_exception: 1, unknown: 2, fail: 3 };

export const SORTABLE = ['when', 'state', 'id', 'source'];

/** 排序：只认 SORTABLE 里的键；未知键原样返回（不静默假装排过）。 */
export function sortRows(rows, key = 'when', dir = 'desc') {
  if (!Array.isArray(rows)) return [];
  if (!SORTABLE.includes(key)) return rows.slice();
  const sign = dir === 'asc' ? 1 : -1;
  const val = (r) => {
    if (key === 'state') return STATE_ORDER[r.state] ?? 9;
    return String(r[key] ?? '');
  };
  return rows.slice().sort((a, b) => {
    const va = val(a), vb = val(b);
    // 数值键（state）用大小比较；字符串键用 `localeCompare`
    // （**不用 `<`/`>`**：那会让 'IG01' 排在 'ch110' 前面——大写字母的码位更小，
    //  对用户是"看起来乱序"。排序口径必须和"人眼看到的一致"）
    const c = (typeof va === 'number' && typeof vb === 'number')
      ? (va < vb ? -1 : va > vb ? 1 : 0)
      : String(va).localeCompare(String(vb), 'zh-Hans-CN');
    if (c !== 0) return c * sign;
    return String(a.id).localeCompare(String(b.id));   // 稳定：同值按 id
  });
}

/** 筛选：q 匹配 id / detail / detector；state / source 精确匹配（'all' = 不限）。 */
export function filterRows(rows, { q = '', state = 'all', source = 'all' } = {}) {
  if (!Array.isArray(rows)) return [];
  const needle = String(q).trim().toLowerCase();
  return rows.filter((r) => {
    if (state !== 'all' && r.state !== state) return false;
    if (source !== 'all' && r.source !== source) return false;
    if (!needle) return true;
    return [r.id, r.detail, r.detector, r.verdict, r.source_label]
      .some((v) => String(v ?? '').toLowerCase().includes(needle));
  });
}

/** 数字格式：整数千分位；小数按位；**null/undefined 一律 '—'（不用 0 冒充）**。 */
export function fmtNum(v, digits = 0) {
  if (v === null || v === undefined || Number.isNaN(Number(v))) return '—';
  return Number(v).toLocaleString('en-US', {
    minimumFractionDigits: digits, maximumFractionDigits: digits,
  });
}

/**
 * 仪表盘单元格：**全部从 dashboard 现算字段取值**。
 * `warn` = 口径需提醒；`bad` = 漂移（数字不可直接引用）。
 */
export function dashCells(d, verdictsTotal) {
  const h = (d && d.holdout) || {};
  const e = (d && d.external) || {};
  const esc = (d && d.escape) || {};
  return [
    { key: 'cards', num: d?.cards_real, digits: 0, cap: '知识卡',
      sub: `另 ${fmtNum(d?.cards_draft)} 张草稿 · 命题 ${fmtNum(d?.propositions)}（counts_659 现算）` },
    { key: 'rules', num: d?.rules_total, digits: 0, cap: '判决规则',
      sub: '与 data/_gate_rules.json 同源' },
    { key: 'verdicts', num: verdictsTotal, digits: 0, cap: '判决历史（逐条）',
      sub: '只含**有逐条结果**的产物；聚合型样本不进表' },
    { key: 'holdout', num: h.rate_pct, unit: '%', digits: 1, cap: 'holdout 检出率',
      sub: `现算 ${fmtNum(h.catch)}/${fmtNum(h.den)}（${h.denominator || '—'}）`,
      bad: h.drift ? 1 : 0,
      warnLine: h.drift
        ? `⚠ 漂移：落盘 ${fmtNum(h.stored_rate_pct, 1)}% 无现算来源，现算 ${fmtNum(h.rate_pct, 1)}%。需人裁决前不得引用。`
        : '' },
    { key: 'external', num: e.rate_pct, unit: '%', digits: 1, cap: '外部语料检出率',
      sub: `分母 ${fmtNum(e.den)}（catch+miss）；按全部 ${fmtNum(e.total)} 条算则是 ${fmtNum(e.rate_pct_all, 1)}%`,
      warn: 1 },
    { key: 'escape', num: esc.rate_pct, unit: '%', digits: 4, cap: '逃逸率（冻结契约）',
      sub: `${fmtNum(esc.escaped)}/${fmtNum(esc.denominator)} · 616 冻结；**非**真实错误率`, warn: 1 },
    { key: 'ledger', num: d?.ledger_events, digits: 0, cap: '账本事件',
      sub: 'data/646_authority_rule_annotation.jsonl（红线：零改）' },
    { key: 'protectors', num: d?.protectors, digits: 0, cap: '保护器',
      sub: (d?.protectors_missing?.length)
        ? `⚠ 缺 ${d.protectors_missing.length} 个`
        : '全部就位（镜像自拆仓 queyi-core）' },
  ];
}

/** 对比表行的"种类 → 中文"，与 CSS 的 `.kind-tag[data-kind]` 一一对应。 */
export const KIND_LABEL = { drift: '漂移', caliber: '口径差', frozen: '冻结契约', ok: '一致' };
