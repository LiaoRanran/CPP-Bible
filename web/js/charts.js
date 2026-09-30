// web/js/charts.js
// 670c A2 · 实验结果页图表内核：**纯逻辑 + SVG 字符串**
//
// 为什么这么写：图表算法要能被 `node tests/charts.test.mjs` 真跑（本仓无 node_modules、无 jsdom），
// 所以主体只做「数据 → SVG 字符串」的纯函数变换；DOM 渲染与事件绑定全在 experiments.html。
//
// 纪律：
//  1) 颜色只引用 css/design-tokens.css 的变量（内联 SVG 的 presentation attribute 支持 var()），
//     不写死 hex；669c.css 已备好 .chart svg 下的 .axis-line/.grid-line/.tick-label/.bar/
//     .err-bar/.err-cap/.bar-val/.line-path/.line-dot/.pie-seg/.radar-* 等类，直接复用。
//  2) 所有进入 SVG 的文本必过 esc()：防注入（数据来自 JSON，不可信）+ 防标签串味。
//  3) 缺字段 ⇒ null（不抛异常）；缺数据 ⇒ emptyStateSvg()，文案必含「待670a生成」；不编造数字。
//  4) 每张图都是 role="img" + <title>；柱/扇区/点都带 data-* 供点击明细与键盘聚焦。
//  5) 例外（兼容 669c 基线冒烟 web/tests/smoke.mjs）：末尾的 barChart / pieChart 两个**旧版 DOM 适配器**
//     保留原名原签名，内部只做 el.innerHTML = <纯函数产出的 SVG 字符串>；它们不读全局 document，
//     传入假容器 {innerHTML:''} 也能在 Node 里跑。除这两个函数外，本文件不碰 DOM、不发 fetch。

export const CHARTS_VERSION = '670c-A2';

/** 缺数据时的统一文案（实验页所有空状态都必须含这五个字）。 */
export const PENDING = '待670a生成';

/** design-tokens.css 的语义色（写进 SVG 属性会被浏览器当 CSS 值求值 ⇒ 深浅主题自动跟随）。 */
export const TOKENS = {
  accent: 'var(--color-accent)',
  accentSoft: 'var(--color-accent-soft)',
  pass: 'var(--color-pass)',
  fail: 'var(--color-fail)',
  unknown: 'var(--color-unknown)',
  exception: 'var(--color-pass-exception)',
  line: 'var(--color-line)',
  lineStrong: 'var(--color-line-strong)',
  text: 'var(--color-text)',
  textDim: 'var(--color-text-dim)',
  textMute: 'var(--color-text-mute)',
  surface: 'var(--color-surface)',
  surface2: 'var(--color-surface-2)',
  bg: 'var(--color-bg)',
};

export const PALETTE = [
  TOKENS.accent, TOKENS.pass, TOKENS.exception, TOKENS.unknown, TOKENS.fail,
  'var(--color-accent)', 'var(--color-pass)',
];

/** 三个对照臂的固定配色（Static 灰 / Random 更淡 / Failure-driven 强调色）。 */
export const ARM_COLORS = {
  static: TOKENS.unknown,
  'static-rules': TOKENS.unknown,
  'b1-rule-only': TOKENS.unknown,
  random: TOKENS.textMute,
  'budget-matched-random': TOKENS.textMute,
  'failure-driven': TOKENS.accent,
  failure_driven: TOKENS.accent,
  queyi: TOKENS.accent,
  '阙疑': TOKENS.accent,
};

/** 约定顺序：三个语料数据集。 */
export const DATASET_KEYS = ['holdout', 'corpus', 'defect'];

export const DATASET_LABELS = {
  holdout: 'holdout（真错 · 双档 -O0/-O2）',
  corpus: 'corpus（external 可测口径）',
  defect: 'defect（缺陷注入 / 变异体）',
};

/** 检测器构成（饼图）固定口径顺序。 */
export const DETECTOR_KEYS = ['sanitizer', 'compiler-warn', 'cross-compile', 'perf', 'compile-time'];

export const DETECTOR_LABELS = {
  sanitizer: 'sanitizer（ASan/UBSan/TSan）',
  'compiler-warn': 'compiler-warn（-Wall/-Wextra）',
  'cross-compile': 'cross-compile（双编译器）',
  perf: 'perf（性能/回归探针）',
  'compile-time': 'compile-time（编译期断言）',
};

/** 口径消融三臂的短名（全样本 / 可测 / 排除 unknown）。 */
export const CALIBER_LABELS = {
  A_valid_only: '可测（unknown 剔除）',
  B_unknown_as_miss: '排除 unknown（未知记 miss）',
  C_all_samples: '全样本（unknown 进分母）',
};

/** 能力构成雷达的 6 个轴与目标值（目标值来自各产物自身的声明，不是拍脑袋的分母）。 */
export const ABILITY_TARGETS = [
  { key: 'rules', label: '门禁规则', unit: '', target: 67, source: 'status.rules.rules_total / metrics_666.metrics.rules_total' },
  { key: 'protectors', label: '保护器', unit: '', target: 9, source: 'status.protectors.protectors_total' },
  { key: 'ledger', label: '账本事件', unit: '', target: 452, source: 'metrics_666.metrics.ledger_events' },
  { key: 'cards', label: '知识卡（实）', unit: '', target: 42, source: 'metrics_666.metrics.cards_real / experiments.ability 知识卡（实）' },
  { key: 'nodes', label: '图节点', unit: '', target: 178, source: 'data/graph.json nodes.length（回退 status.w2.nodes）' },
  { key: 'mutation', label: '变异杀死率', unit: '%', target: 100, source: 'experiments.mutation[0].rate（core · on_scored）' },
];

/** baseline 三源：按此**顺序**尝试；全失败 ⇒ 「待670a生成」空状态。 */
export const BASELINE_PATHS = [
  'data/experiments/baseline_static.json',
  'data/experiments/baseline_random.json',
  'data/experiments/669_experiments.json',
];

/** 页面补充源（best-effort，单源失败不影响整页）。 */
export const SUPPLEMENT_PATHS = {
  experiments: 'data/experiments.json',
  metrics666: 'data/metrics_666.json',
  status: 'data/status.json',
  graph: 'data/graph.json',
};

/* ══════════════════════════════════════════════════════════════════════════
   0 · 基础工具（全部纯函数）
   ══════════════════════════════════════════════════════════════════════════ */

/** SVG/HTML 文本与属性统一转义（防注入）。null/undefined ⇒ ''。 */
export function esc(v) {
  if (v === null || v === undefined) return '';
  return String(v)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

export function isNum(v) { return typeof v === 'number' && Number.isFinite(v); }

/** 宽松数值解析：数字 / 数字串 ⇒ number，其余 ⇒ null（不抛异常）。 */
export function num(v) {
  if (isNum(v)) return v;
  if (typeof v === 'string' && v.trim() !== '') {
    const x = Number(v);
    if (Number.isFinite(x)) return x;
  }
  return null;
}

/** 0..100 的百分数 → '87.5%'；null ⇒ '—'（禁止无声变成 0）。 */
export function fmtPct(v, digits = 1) {
  const x = num(v);
  return x === null ? '—' : x.toFixed(digits) + '%';
}

/** 取整到 digits 位（写进 data-* 用）。 */
export function r1(v, digits = 1) {
  const x = num(v);
  if (x === null) return null;
  const m = Math.pow(10, digits);
  return Math.round(x * m) / m;
}

/** 轴上限取整：1/2/2.5/5/10 × 10^n 中第一个 ≥ v 的值。 */
export function niceCeil(v) {
  const x = num(v);
  if (x === null || x <= 0) return 10;
  const mag = Math.pow(10, Math.floor(Math.log10(x)));
  const steps = [1, 2, 2.5, 5, 10];
  for (const s of steps) {
    const c = s * mag;
    if (x <= c + 1e-9) return c;
  }
  return 10 * mag;
}

/** 建一个属性串（值为 null/undefined/false ⇒ 省略；true ⇒ 裸属性）。 */
function at(name, value) {
  if (value === null || value === undefined || value === false) return '';
  if (value === true) return ' ' + name;
  return ' ' + name + '="' + esc(value) + '"';
}

/** 按行折行（CJK 按字符数近似），最多 maxLines 行，超出补省略号。 */
export function wrapText(text, per = 46, maxLines = 3) {
  const src = String(text === null || text === undefined ? '' : text);
  const out = [];
  for (const raw of src.split(/\r?\n/)) {
    let s = raw;
    if (s === '') { out.push(''); continue; }
    while (s.length > per) { out.push(s.slice(0, per)); s = s.slice(per); }
    out.push(s);
  }
  if (out.length <= maxLines) return out;
  const cut = out.slice(0, maxLines);
  cut[maxLines - 1] = cut[maxLines - 1].slice(0, Math.max(0, per - 1)) + '…';
  return cut;
}

/** 按显示宽度折行：CJK/全角算 2 单位、ASCII 算 1 单位（SVG text 不会自动换行）。 */
export function wrapByWidth(text, maxUnits = 120, maxLines = 3) {
  const out = [];
  const src = String(text === null || text === undefined ? '' : text);
  for (const para of src.split(/\r?\n/)) {
    let cur = '';
    let w = 0;
    for (const ch of para) {
      const cw = /[\u1100-\u115F\u2E80-\uA4CF\uAC00-\uD7A3\uF900-\uFAFF\uFE30-\uFE4F\uFF00-\uFF60\uFFE0-\uFFE6]/.test(ch) ? 2 : 1;
      if (w + cw > maxUnits && cur !== '') { out.push(cur); cur = ''; w = 0; }
      cur += ch;
      w += cw;
    }
    out.push(cur);
  }
  if (out.length <= maxLines) return out;
  const cut = out.slice(0, maxLines);
  cut[maxLines - 1] = cut[maxLines - 1] + '…';
  return cut;
}

/* ══════════════════════════════════════════════════════════════════════════
   1 · 统计原语：Wilson score 区间
   ══════════════════════════════════════════════════════════════════════════ */

/**
 * Wilson score 置信区间（闭式，小样本比 Wald 稳；与 tools/stat_bounds.py::wilson 同式）。
 * @returns {{lo:number, hi:number, p:number}|null} 0..1 的 lo/hi 与点估计 p；n<=0 ⇒ null。
 * 边界：k=0 ⇒ lo 恒为 0；k=n ⇒ hi 恒为 1；k>n 会被夹到 n。
 */
export function wilsonCI(k, n, z = 1.96) {
  const nn = num(n);
  if (nn === null || nn <= 0) return null;
  const kRaw = num(k);
  const kk = Math.min(Math.max(kRaw === null ? 0 : kRaw, 0), nn);
  const zz = num(z) === null ? 1.96 : num(z);
  const p = kk / nn;
  const z2 = zz * zz;
  const d = 1 + z2 / nn;
  const c = p + z2 / (2 * nn);
  const m = zz * Math.sqrt((p * (1 - p)) / nn + z2 / (4 * nn * nn));
  let lo = (c - m) / d;
  let hi = (c + m) / d;
  if (kk === 0) lo = 0;
  if (kk === nn) hi = 1;
  if (lo < 0) lo = 0;
  if (hi > 1) hi = 1;
  return { lo, hi, p };
}

/**
 * 点击明细的单行文本：k/n = 百分比（Wilson 95% CI：lo – hi）。
 * ci 可选（0..1 的 {lo,hi}）；不给则用 wilsonCI 现算；n=0 ⇒ 显式「不可估」。
 */
export function describeSample(k, n, ci = null, opts = {}) {
  const o = opts || {};
  const digits = isNum(o.digits) ? o.digits : 1;
  const conf = o.conf || '95%';
  const nn = num(n);
  const kk = num(k);
  if (nn === null || nn <= 0) {
    return (kk === null ? 0 : kk) + '/0 = 不可估（n=0：无可用样本，区间无定义）';
  }
  if (kk === null) return '—/' + nn + '（只有分母，k 缺失）';
  const p = kk / nn;
  const c = (ci && isNum(ci.lo) && isNum(ci.hi)) ? ci : wilsonCI(kk, nn);
  const head = kk + '/' + nn + ' = ' + fmtPct(p * 100, digits);
  if (!c) return head;
  return head + '（Wilson ' + conf + ' CI：' + fmtPct(c.lo * 100, digits) + ' – ' + fmtPct(c.hi * 100, digits) + '）';
}

/* ══════════════════════════════════════════════════════════════════════════
   2 · 数据解析：baseline / 口径消融 / 检测器 / 演化
   ══════════════════════════════════════════════════════════════════════════ */

const DATASET_ALIASES = [
  { key: 'holdout', re: /hold|真错|盲态/i },
  { key: 'corpus', re: /corpus|external|语料|外部|层\s*[abc]/i },
  { key: 'defect', re: /defect|缺陷|注入|inject|mutant|变异体/i },
];

/** 把任意命名（'external 可测口径' / 'holdout 真错（双档）'）归一到 holdout|corpus|defect。 */
export function normalizeDatasetKey(raw) {
  if (raw === null || raw === undefined) return null;
  const s = String(raw).trim();
  if (!s) return null;
  const low = s.toLowerCase();
  if (DATASET_KEYS.indexOf(low) >= 0) return low;
  for (const a of DATASET_ALIASES) if (a.re.test(s)) return a.key;
  return null;
}

function normalizeSample(s) {
  if (s === null || s === undefined) return null;
  if (typeof s === 'string') return { id: s, verdict: null, note: null };
  if (typeof s !== 'object') return null;
  const id = s.id ?? s.sample ?? s.name ?? s.path ?? null;
  return {
    id: id === null ? null : String(id),
    verdict: s.verdict ?? s.state ?? s.result ?? s.status ?? null,
    note: s.note ?? s.detail ?? null,
  };
}

/** 宽松数据集归一：k/n/rate_pct/ci/cp/samples 全可缺，缺的填 null，永不抛。 */
export function normalizeDataset(node, key = null) {
  if (node === null || node === undefined) return null;
  if (isNum(node) || typeof node === 'string') node = { k: node };
  if (typeof node !== 'object') return null;
  const src = node;
  const k = num(src.k ?? src.catch ?? src.caught ?? src.hit ?? src.hits ?? src.numerator ?? src.num);
  let n = num(src.n ?? src.total ?? src.den);
  if (n === null && src.denominator && typeof src.denominator === 'object') n = num(src.denominator.value);
  if (n === null) n = num(src.denominator);
  if (n === null) n = num(src.samples_total);
  const pFromKn = (k !== null && n !== null && n > 0) ? k / n : null;
  let p = num(src.p ?? src.proportion);
  if (p === null) p = pFromKn;
  let ratePct = num(src.rate_pct ?? src.pct);
  if (ratePct === null && num(src.rate) !== null) {
    const raw = num(src.rate);
    ratePct = raw <= 1 ? raw * 100 : raw;
  }
  const notes = [];
  if (ratePct === null && pFromKn !== null) ratePct = pFromKn * 100;
  if (ratePct !== null && pFromKn !== null && Math.abs(ratePct - pFromKn * 100) > 0.05) {
    notes.push('rate_pct=' + r1(ratePct) + ' 与 k/n=' + r1(pFromKn * 100) + ' 不一致（口径冲突，已按原样呈现）');
  }
  // 区间：优先用产物自带的 Wilson 百分数；否则现算；再给可选的 C-P 区间
  const loPct = num(src.wilson_lo_pct ?? src.ci_lo_pct ?? src.wilson_low_pct);
  const hiPct = num(src.wilson_hi_pct ?? src.ci_hi_pct ?? src.wilson_high_pct);
  let ci = null;
  if (loPct !== null && hiPct !== null) ci = { lo: loPct / 100, hi: hiPct / 100, p: p, provided: true };
  else if (src.ci && num(src.ci.lo) !== null && num(src.ci.hi) !== null) ci = { lo: num(src.ci.lo), hi: num(src.ci.hi), p: p, provided: true };
  else if (k !== null && n !== null && n > 0) ci = wilsonCI(k, n);
  const cpLo = num(src.cp_lo_pct ?? (src.cp && src.cp.lo_pct));
  const cpHi = num(src.cp_hi_pct ?? (src.cp && src.cp.hi_pct));
  const cp = (cpLo !== null && cpHi !== null) ? { lo: cpLo / 100, hi: cpHi / 100, provided: true } : null;
  const samples = Array.isArray(src.samples) ? src.samples.map(normalizeSample).filter(Boolean) : [];
  const label = src.label ?? src.name ?? (key ? DATASET_LABELS[key] : null);
  return {
    present: true,
    key: key || normalizeDatasetKey(label) || null,
    label: label === null || label === undefined ? null : String(label),
    k: k, n: n, p: p, rate_pct: ratePct,
    ci: ci, cp: cp,
    samples: samples,
    exploratory: src.exploratory === true,
    note: src.note === null || src.note === undefined ? null : String(src.note),
    source: src.source === null || src.source === undefined ? null : String(src.source),
    cmd: src.cmd === null || src.cmd === undefined ? null : String(src.cmd),
    denominatorText: typeof src.denominator === 'string' ? src.denominator : null,
    conflicts: notes,
  };
}

/** 数据集点估计（0..100 的百分数）：rate_pct 优先，其次 k/n。 */
export function datasetRatePct(ds) {
  if (!ds) return null;
  const r = num(ds.rate_pct);
  if (r !== null) return r;
  if (num(ds.k) !== null && num(ds.n) !== null && num(ds.n) > 0) return (num(ds.k) / num(ds.n)) * 100;
  if (isNum(ds.p)) return ds.p * 100;
  return null;
}

function emptyDatasetBag() { return { holdout: null, corpus: null, defect: null }; }

/** 归一一「臂」：{key,label,color,datasets:{holdout,corpus,defect}}；支持 datasets 袋或扁平 k/n 行。 */
export function normalizeArm(node, fallbackKey = null) {
  if (node === null || node === undefined || typeof node !== 'object') return null;
  const rawKey = node.key ?? node.arm ?? node.id ?? fallbackKey;
  const key = String(rawKey === null || rawKey === undefined ? 'arm' : rawKey).trim() || 'arm';
  const label = String(node.label ?? node.name ?? key);
  const color = node.color || ARM_COLORS[key] || ARM_COLORS[key.toLowerCase()] || null;
  const datasets = emptyDatasetBag();
  const bag = (node.datasets && typeof node.datasets === 'object' && !Array.isArray(node.datasets)) ? node.datasets : null;
  if (bag) {
    for (const raw of Object.keys(bag)) {
      const dk = normalizeDatasetKey(raw);
      if (!dk) continue;
      const ds = normalizeDataset(bag[raw], dk);
      if (ds && !datasets[dk]) datasets[dk] = ds;
    }
  }
  // 顶层键直接带数据集（口径映射形态：{'A_valid_only（…）': {holdout:{…}, external:{…}}}）
  for (const raw of Object.keys(node)) {
    if (raw === 'datasets') continue;
    const dk = normalizeDatasetKey(raw);
    if (!dk || datasets[dk]) continue;
    const val = node[raw];
    if (val && typeof val === 'object' && !Array.isArray(val)) {
      const ds = normalizeDataset(val, dk);
      if (ds) datasets[dk] = ds;
    }
  }
  // 扁平 k/n 行：整行当作一个数据集（键从 dataset/key/name/label 推）
  const hasAny = DATASET_KEYS.some((dk) => datasets[dk]);
  if (!hasAny) {
    const dk = normalizeDatasetKey(node.dataset ?? node.key ?? node.name ?? node.label);
    if (dk) {
      const ds = normalizeDataset(node, dk);
      if (ds) datasets[dk] = ds;
    } else if (num(node.k) !== null || num(node.n) !== null || num(node.rate_pct) !== null) {
      const ds = normalizeDataset(node, 'holdout');
      if (ds) datasets.holdout = ds;
    }
  }
  return { key: key, label: label, color: color, datasets: datasets, exploratory: node.exploratory === true, note: node.note === undefined ? null : node.note };
}

/** 归一臂集合：接受数组，也接受 {"A_xxx（…）": {holdout:{…}}} 这种对象映射。 */
export function normalizeArms(input) {
  if (!input) return [];
  if (Array.isArray(input)) return input.map((a, i) => normalizeArm(a, 'arm' + (i + 1))).filter(Boolean);
  if (typeof input === 'object') {
    return Object.keys(input).map((k, i) => normalizeArm(Object.assign({ key: k }, input[k] || {}), 'arm' + (i + 1))).filter(Boolean);
  }
  return [];
}

/** 口径臂短名：'A_valid_only（本批主口径：unknown 剔除）' ⇒ '可测（unknown 剔除）'。 */
export function caliberLabel(rawKey) {
  const k = String(rawKey === null || rawKey === undefined ? '' : rawKey).trim();
  const base = k.split(/[（(:：,，]/)[0].trim();
  if (CALIBER_LABELS[base]) return CALIBER_LABELS[base] + ' · ' + base;
  if (CALIBER_LABELS[k]) return CALIBER_LABELS[k];
  return k || '口径';
}

/** 解析口径消融（caliber_ablation / calibers）。无则 null。 */
export function parseCalibers(raw) {
  if (!raw || typeof raw !== 'object') return null;
  const src = (raw.caliber_ablation && typeof raw.caliber_ablation === 'object') ? raw.caliber_ablation : raw;
  const armsInput = src.arms ?? null;
  if (!armsInput) return null;
  const arms = normalizeArms(armsInput).map((a) => Object.assign({}, a, {
    label: caliberLabel(a.key),
    color: ARM_COLORS[a.key] || null,
  }));
  if (!arms.length) return null;
  const seen = [];
  arms.forEach((a) => DATASET_KEYS.forEach((k) => { if (a.datasets[k] && seen.indexOf(k) < 0) seen.push(k); }));
  const delta = {};
  const dp = src.delta_pp || raw.delta_pp || null;
  if (dp && typeof dp === 'object') {
    for (const k of Object.keys(dp)) {
      const m = dp[k];
      if (m && typeof m === 'object') {
        delta[k] = Object.keys(m).map((kk) => kk + '=' + m[kk]).join(' / ');
      }
    }
  }
  return {
    arms: arms,
    datasets: seen.length ? seen : DATASET_KEYS.slice(),
    note: src.note ? String(src.note) : null,
    delta_pp: delta,
    source: 'caliber_ablation',
  };
}

/** 检测器构成归一：对象映射或数组 ⇒ [{key,label,value}]，固定口径顺序在前。 */
export function normalizeDetectors(raw) {
  if (!raw) return [];
  const out = [];
  const push = (key, label, value) => {
    const v = num(value);
    if (v === null || v < 0) return;
    out.push({ key: String(key), label: String(label || DETECTOR_LABELS[key] || key), value: v });
  };
  if (Array.isArray(raw)) {
    raw.forEach((d, i) => { if (d && typeof d === 'object') push(d.key ?? d.label ?? 'detector-' + (i + 1), d.label ?? d.key, d.value ?? d.n); });
  } else if (typeof raw === 'object') {
    for (const k of Object.keys(raw)) {
      const v = raw[k];
      if (v && typeof v === 'object') push(k, v.label ?? DETECTOR_LABELS[k] ?? k, v.value ?? v.n ?? v.count);
      else push(k, DETECTOR_LABELS[k] ?? k, v);
    }
  }
  // 固定口径顺序优先，未知键追加在后
  const rank = (k) => { const i = DETECTOR_KEYS.indexOf(k); return i < 0 ? 99 : i; };
  return out.sort((a, b) => rank(a.key) - rank(b.key));
}

/** 演化行归一：[{batch,mutation_pct,holdout_pct,note}]，缺字段填 null。 */
export function normalizeEvolution(raw) {
  if (!Array.isArray(raw)) return null;
  const rows = raw.map((r) => {
    if (!r || typeof r !== 'object') return null;
    const batch = r.batch ?? r.x ?? r.label ?? r.name ?? null;
    if (batch === null) return null;
    return {
      batch: String(batch),
      mutation_pct: num(r.mutation_pct ?? r.mutation ?? r.mutation_rate_pct),
      holdout_pct: num(r.holdout_pct ?? r.holdout ?? r.holdout_rate_pct ?? r.rate_pct),
      note: r.note === undefined ? null : String(r.note),
    };
  }).filter(Boolean);
  return rows.length ? rows : null;
}

/**
 * parseBaseline(json) ⇒ 规范化结构（**永不抛异常**）：
 *   { datasets:{holdout,corpus,defect}, arms:[...], calibers, detectors, evolution, notes, missing, ok }
 * 缺失字段一律 null；数据集缺失 ⇒ datasets[k] = null 并进 missing。
 */
export function parseBaseline(json) {
  const out = {
    ok: false, schema: null, source: null, generated_at: null, arm: null, label: null,
    planned: false, datasets: emptyDatasetBag(), arms: [], rowArms: [],
    calibers: null, detectors: [], evolution: null,
    notes: [], missing: DATASET_KEYS.slice(), raw: json === undefined ? null : json,
  };
  if (json === null || json === undefined) {
    out.notes.push('baseline JSON 缺失（null）：显示「' + PENDING + '」空状态');
    return out;
  }
  if (typeof json !== 'object') {
    out.notes.push('baseline JSON 不是对象（' + typeof json + '）：已忽略');
    return out;
  }
  const pushNote = (v) => {
    if (v === null || v === undefined || typeof v !== 'string') return;
    const s = v.trim();
    if (s && out.notes.indexOf(s) < 0) out.notes.push(s);
  };

  out.schema = json.schema ?? null;
  out.source = json.source ?? json.provenance ?? null;
  out.generated_at = json.generated_at ?? json.generatedAt ?? null;
  out.arm = json.arm ?? json.key ?? null;
  out.label = json.label ?? json.name ?? null;
  if (String(json.status || '').toLowerCase() === 'planned') out.planned = true;
  pushNote(json.note);
  pushNote(json.honest_note);
  if (json.registry && typeof json.registry === 'object') {
    pushNote(json.registry.honest_note);
    if (!out.label && json.registry.experiment) out.label = json.registry.experiment;
    if (!out.generated_at && json.registry.commit) out.generated_at = null;
  }
  if (json.baselines && !Array.isArray(json.baselines) && typeof json.baselines === 'object') {
    if (String(json.baselines.status || '').toLowerCase() === 'planned') out.planned = true;
    pushNote(json.baselines.note);
  }
  if (json.ablation && typeof json.ablation === 'object') pushNote(json.ablation.note);

  // 数据集来源 1：datasets 袋
  const bag = (json.datasets && typeof json.datasets === 'object' && !Array.isArray(json.datasets)) ? json.datasets : null;
  if (bag) {
    for (const raw of Object.keys(bag)) {
      const dk = normalizeDatasetKey(raw) || (DATASET_KEYS.indexOf(raw.toLowerCase()) >= 0 ? raw.toLowerCase() : null);
      if (!dk) continue;
      if (!out.datasets[dk]) out.datasets[dk] = normalizeDataset(bag[raw], dk);
    }
  }
  // 数据集来源 2：顶层直接给 holdout/corpus/defect
  for (const dk of DATASET_KEYS) {
    if (out.datasets[dk]) continue;
    const node = json[dk];
    if (node && typeof node === 'object') out.datasets[dk] = normalizeDataset(node, dk);
  }
  // 数据集来源 3：顶层扁平 k/n 行（单数据集 JSON）
  if (!bag && !out.datasets.holdout && (num(json.k) !== null || num(json.rate_pct) !== null)) {
    const dk = normalizeDatasetKey(json.dataset ?? json.arm ?? json.label ?? json.name) || 'holdout';
    out.datasets[dk] = normalizeDataset(json, dk);
  }

  // 臂来源 1：显式 arms（数组或映射）
  out.arms = normalizeArms(json.arms);

  // 臂来源 2：baselines 行数组（669_experiments.json 的形态）
  if (Array.isArray(json.baselines)) {
    out.rowArms = normalizeArms(json.baselines);
    // 逐行明细 ⇒ 每个数据集各取首个非空值，作为 datasets 的首选口径
    for (const a of out.rowArms) {
      for (const dk of DATASET_KEYS) {
        if (!out.datasets[dk] && a.datasets[dk]) out.datasets[dk] = a.datasets[dk];
      }
    }
    if (!out.arms.length && out.rowArms.length) {
      out.arms = [{
        key: 'failure-driven',
        label: out.label || '阙疑（failure-driven）',
        color: ARM_COLORS['failure-driven'],
        datasets: { holdout: out.datasets.holdout, corpus: out.datasets.corpus, defect: out.datasets.defect },
        exploratory: false,
        note: null,
      }];
      out.notes.push('baselines 为逐行明细（' + out.rowArms.length + ' 行）：按数据集各取首选值合成一臂，全部逐行值见 rowArms');
    }
  }

  // 臂来源 3：只有数据集 ⇒ 合成单臂
  if (!out.arms.length && (out.datasets.holdout || out.datasets.corpus || out.datasets.defect)) {
    out.arms = [{
      key: String(out.arm || 'default'),
      label: String(out.label || '默认臂'),
      color: ARM_COLORS[String(out.arm || '')] || TOKENS.accent,
      datasets: { holdout: out.datasets.holdout, corpus: out.datasets.corpus, defect: out.datasets.defect },
      exploratory: false,
      note: null,
    }];
  }

  out.calibers = parseCalibers(json.caliber_ablation || json.calibers || null);
  out.detectors = normalizeDetectors(json.detectors || json.detector_mix || json.detector_breakdown || null);
  out.evolution = normalizeEvolution(json.evolution || json.batches || null);
  out.missing = DATASET_KEYS.filter((k) => !out.datasets[k]);
  out.ok = out.arms.length > 0 || out.missing.length < DATASET_KEYS.length || !!out.calibers;
  if (!out.ok) {
    out.notes.push('JSON 中找不到 holdout/corpus/defect 任一数据集：显示「' + PENDING + '」空状态');
  }
  return out;
}

/** 从路径/标签推断臂身份：static / random / failure-driven。 */
export function inferArmKey(pathOrLabel, parsed = null) {
  const s = String(pathOrLabel || '').toLowerCase();
  if (/static|静态|regex|cppcheck|clang-tidy|rule-only|规则/.test(s)) return 'static';
  if (/random|随机|budget/.test(s)) return 'random';
  if (/failure|queyi|阙疑|669/.test(s)) return 'failure-driven';
  const arm = parsed && parsed.arm ? String(parsed.arm).toLowerCase() : '';
  if (arm && ARM_COLORS[arm]) return arm;
  return 'failure-driven';
}

/**
 * 把多个 baseline 源合成展示用臂列表（Static / Random / Failure-driven，按此顺序）。
 * 同 key 的源合并数据集（先到的非空值优先）。
 */
export function composeArms(sources = []) {
  const list = Array.isArray(sources) ? sources.filter(Boolean) : [];
  const byKey = new Map();
  const order = ['static', 'random', 'failure-driven'];
  for (const src of list) {
    const parsed = src.data || parseBaseline(src.raw || null);
    const key = src.armKey || inferArmKey(src.path || parsed.label || parsed.arm, parsed);
    const label = src.armLabel || (key === 'static' ? 'Static（静态规则）' : key === 'random' ? 'Random（budget-matched 随机）' : 'Failure-driven（阙疑 · 真实结果）');
    if (!byKey.has(key)) byKey.set(key, { key: key, label: label, color: ARM_COLORS[key] || null, datasets: emptyDatasetBag(), exploratory: false, note: null, paths: [] });
    const arm = byKey.get(key);
    if (src.path) arm.paths.push(src.path);
    if (parsed.arm && key === inferArmKey(parsed.arm, parsed) && !ARM_COLORS[key]) arm.color = arm.color || parsed.arms[0] && parsed.arms[0].color || null;
    const armsToMerge = parsed.arms.length ? parsed.arms : [];
    for (const a of armsToMerge) {
      for (const dk of DATASET_KEYS) {
        if (!arm.datasets[dk] && a.datasets[dk]) arm.datasets[dk] = a.datasets[dk];
      }
    }
    for (const dk of DATASET_KEYS) {
      if (!arm.datasets[dk] && parsed.datasets[dk]) arm.datasets[dk] = parsed.datasets[dk];
    }
    if (parsed.calibers && !arm.calibers) arm.calibers = parsed.calibers;
    if (Array.isArray(parsed.detectors) && parsed.detectors.length && !arm.detectors) arm.detectors = parsed.detectors;
    if (parsed.evolution && !arm.evolution) arm.evolution = parsed.evolution;
  }
  const out = [];
  for (const k of order) if (byKey.has(k)) out.push(byKey.get(k));
  for (const k of byKey.keys()) if (order.indexOf(k) < 0) out.push(byKey.get(k));
  // 颜色兜底
  out.forEach((a, i) => { if (!a.color) a.color = ARM_COLORS[a.key] || PALETTE[i % PALETTE.length]; });
  return out;
}

/** 按顺序尝试 BASELINE_PATHS；全部失败 ⇒ ok:false（页面显示「待670a生成」，不报错不崩溃）。 */
export async function loadBaselines(fetchJson, paths = BASELINE_PATHS) {
  const tried = [];
  const sources = [];
  if (typeof fetchJson !== 'function') {
    return { ok: false, sources: [], tried: [{ path: null, ok: false, error: 'fetchJson 不可用（非函数）' }], arms: [], error: 'fetchJson 不可用' };
  }
  for (const p of (paths || [])) {
    try {
      const raw = await fetchJson(p);
      sources.push({ path: p, raw: raw, data: parseBaseline(raw), ok: true });
      tried.push({ path: p, ok: true });
    } catch (e) {
      tried.push({ path: p, ok: false, error: (e && e.message) ? String(e.message) : String(e) });
    }
  }
  return {
    ok: sources.length > 0,
    sources: sources,
    tried: tried,
    arms: composeArms(sources),
    paths: (paths || []).slice(),
  };
}

/** 取第一个成功的源（保持老接口语义）。 */
export async function loadBaselineData(fetchJson, paths = BASELINE_PATHS) {
  const res = await loadBaselines(fetchJson, paths);
  const first = res.sources.length ? res.sources[0] : null;
  return {
    ok: res.ok,
    path: first ? first.path : null,
    raw: first ? first.raw : null,
    data: first ? first.data : parseBaseline(null),
    tried: res.tried,
  };
}

/** best-effort 拉补充源：任一失败只记 tried，不抛。 */
export async function loadSupplements(fetchJson, paths = SUPPLEMENT_PATHS) {
  const results = {};
  const tried = [];
  const keys = Object.keys(paths || {});
  for (const k of keys) {
    try {
      results[k] = await fetchJson(paths[k]);
      tried.push({ key: k, path: paths[k], ok: true });
    } catch (e) {
      results[k] = null;
      tried.push({ key: k, path: paths[k], ok: false, error: (e && e.message) ? String(e.message) : String(e) });
    }
  }
  return { results: results, tried: tried };
}

/* ══════════════════════════════════════════════════════════════════════════
   3 · SVG 骨架与空状态
   ══════════════════════════════════════════════════════════════════════════ */

function svgOpen(w, h, title, kind, extraClass) {
  return '<svg' + at('class', 'chart-svg' + (extraClass ? ' ' + extraClass : ''))
    + at('data-chart', kind) + at('viewBox', '0 0 ' + w + ' ' + h)
    + ' width="100%" preserveAspectRatio="xMidYMid meet" role="img"'
    + at('aria-label', title) + '>'
    + '<title>' + esc(title) + '</title>';
}

/**
 * 空状态：**必含「待670a生成」**。所有 builder 在无数据时都返回它（页面不会崩、不会空白）。
 * @param {string} msg 追加说明（可为空）
 */
export function emptyStateSvg(msg) {
  const text = (msg === null || msg === undefined || String(msg).trim() === '')
    ? '该图数据尚未产出：等 670a 把 baseline 写进 data/experiments/ 后自动出现（本页不编造数字）。'
    : String(msg);
  const lines = wrapByWidth(text, 84, 3);
  let out = '<svg class="chart-svg chart-pending" data-chart="empty" viewBox="0 0 640 172" width="100%" role="img"'
    + at('aria-label', PENDING + '：' + text) + '>';
  out += '<title>' + esc(PENDING) + '</title>';
  out += '<desc>' + esc(text) + '</desc>';
  out += '<rect class="ce-box" x="1" y="1" width="638" height="170" rx="10" fill="none"'
    + at('stroke', TOKENS.lineStrong) + ' stroke-width="1.5" stroke-dasharray="6 5"/>';
  out += '<text class="ce-t" x="320" y="64" text-anchor="middle"' + at('fill', TOKENS.textDim)
    + ' font-size="14" font-weight="600">' + esc(PENDING) + '</text>';
  lines.forEach((ln, i) => {
    out += '<text class="ce-m" x="320" y="' + (90 + i * 18) + '" text-anchor="middle"'
      + at('fill', TOKENS.textMute) + ' font-size="12">' + esc(ln) + '</text>';
  });
  out += '</svg>';
  return out;
}

const nf = (v) => String(Math.round(num(v) === null ? 0 : num(v) * 100) / 100);

/* ══════════════════════════════════════════════════════════════════════════
   4 · 分组柱：baseline 对比（A2 主图）与口径消融
   ══════════════════════════════════════════════════════════════════════════ */

export function datasetLabelOf(key, spec) {
  const map = (spec && spec.datasetLabels) || {};
  if (map[key]) return map[key];
  return DATASET_LABELS[key] || String(key);
}

/**
 * buildGroupedBars(spec) ⇒ SVG 字符串
 * spec = { arms:[{key,label,color,datasets:{holdout,corpus,defect}}], datasets:['holdout',...],
 *          unit:'%', max:100, width, height, title, selected:{arm,dataset}, kind, emptyMsg }
 * 每柱：<rect class="bar" data-arm data-dataset data-k data-n data-pct data-ci-lo data-ci-hi tabindex=0>
 *       + 误差线 .err-bar/.err-cap（有 CI 时）+ 数值标签 .bar-val；缺数据的柱画虚线幽灵柱并标 n/a。
 */
export function buildGroupedBars(spec) {
  const s = spec || {};
  const arms = normalizeArms(s.arms);
  // 显式给了 datasets ⇒ 一组一列全画（缺数据的画虚线幽灵柱）；没给 ⇒ 只画有数据的组
  const explicit = Array.isArray(s.datasets) && s.datasets.length > 0;
  const keys = (explicit ? s.datasets : DATASET_KEYS).filter((k) => typeof k === 'string');
  const visible = explicit ? keys : keys.filter((k) => arms.some((a) => a.datasets && a.datasets[k]));
  const anyData = arms.some((a) => DATASET_KEYS.some((k) => a.datasets && a.datasets[k]));
  if (!arms.length || !visible.length || !anyData) {
    return emptyStateSvg(s.emptyMsg || '分组柱需要 arms × datasets；当前没有可渲染的数据集（' + PENDING + '）');
  }
  const width = isNum(s.width) ? s.width : 760;
  const height = isNum(s.height) ? s.height : 340;
  const unit = s.unit === undefined ? '%' : s.unit;
  const kind = s.kind || 'grouped';
  const seen = [];
  arms.forEach((a) => visible.forEach((k) => {
    const ds = a.datasets[k];
    if (!ds) return;
    const v = datasetRatePct(ds);
    if (v !== null) seen.push(v);
    if (ds.ci && isNum(ds.ci.hi)) seen.push(ds.ci.hi * 100);
  }));
  const maxSeen = seen.length ? Math.max.apply(null, seen) : 0;
  const yMax = (isNum(s.max) && s.max > 0) ? s.max : (unit === '%' && maxSeen <= 100 ? 100 : niceCeil(maxSeen));
  const noteLines = s.note ? wrapByWidth(String(s.note), 120, 3) : [];
  const pad = { t: s.legend === false ? 18 : 36, r: 16, b: 64 + noteLines.length * 13, l: 48 };
  const plotW = width - pad.l - pad.r;
  const plotH = height - pad.t - pad.b;
  const baseY = height - pad.b;
  const groupW = plotW / visible.length;
  const barW = Math.max(10, Math.min(46, (groupW - 16) / arms.length));
  const ticks = 4;
  const yOf = (v) => baseY - plotH * (Math.max(0, Math.min(num(v) === null ? 0 : num(v), yMax)) / yMax);
  const title = s.title || '分组柱状图（检出率 %）';
  let out = svgOpen(width, height, title, kind);
  if (s.desc) out += '<desc>' + esc(Array.isArray(s.desc) ? s.desc.join('；') : s.desc) + '</desc>';
  // 网格 + y 刻度
  for (let i = 0; i <= ticks; i++) {
    const y = pad.t + plotH * (i / ticks);
    const v = yMax * (1 - i / ticks);
    out += '<line class="grid-line" x1="' + pad.l + '" y1="' + nf(y) + '" x2="' + nf(width - pad.r) + '" y2="' + nf(y) + '"/>';
    out += '<text class="tick-label" x="' + (pad.l - 6) + '" y="' + nf(y + 4) + '" text-anchor="end">'
      + esc(unit === '%' ? Math.round(v) + '%' : String(Math.round(v * 10) / 10)) + '</text>';
  }
  out += '<line class="axis-line" x1="' + pad.l + '" y1="' + pad.t + '" x2="' + pad.l + '" y2="' + baseY + '"/>';
  out += '<line class="axis-line" x1="' + pad.l + '" y1="' + baseY + '" x2="' + nf(width - pad.r) + '" y2="' + baseY + '"/>';
  const yTitle = s.yTitle || (unit === '%' ? '检出率 %' : '');
  if (yTitle) out += '<text class="axis-title" x="' + pad.l + '" y="' + (pad.t - 10) + '">' + esc(yTitle) + '</text>';
  // 柱
  visible.forEach((dk, gi) => {
    const gx = pad.l + groupW * gi;
    const rowW = barW * arms.length;
    const start = gx + (groupW - rowW) / 2;
    const ns = [];
    arms.forEach((arm, ai) => {
      const ds = arm.datasets[dk] || null;
      const color = arm.color || PALETTE[ai % PALETTE.length];
      const x = start + ai * barW;
      const cx = x + barW / 2;
      const v = ds ? datasetRatePct(ds) : null;
      const dlabel = datasetLabelOf(dk, s);
      const selected = !!(s.selected && s.selected.arm === arm.key && s.selected.dataset === dk);
      const baseLabel = arm.label + ' × ' + dlabel;
      const common = at('data-role', 'bar') + at('data-chart', kind) + at('data-arm', arm.key)
        + at('data-dataset', dk) + at('data-label', baseLabel)
        + (kind === 'caliber' ? at('data-caliber', arm.label) : '') + at('tabindex', 0);
      if (ds && ds.n !== null && ns.indexOf(ds.n) < 0) ns.push(ds.n);
      if (!ds || v === null || !isNum(v)) {
        const aria = baseLabel + '：无数据（' + PENDING + '）';
        out += '<rect' + at('class', 'bar is-missing') + common + at('data-missing', '1')
          + at('x', nf(x)) + at('y', nf(baseY - 8)) + at('width', nf(barW)) + at('height', 8) + at('rx', 3)
          + at('fill', 'none') + at('stroke', TOKENS.line) + at('stroke-dasharray', '3 3')
          + at('aria-label', aria) + '><title>' + esc(aria) + '</title></rect>';
        out += '<text class="bar-val" x="' + nf(cx) + '" y="' + nf(baseY - 14) + '" text-anchor="middle">n/a</text>';
        return;
      }
      const yTop = yOf(v);
      const aria = baseLabel + '：' + describeSample(ds.k, ds.n, ds.ci);
      out += '<rect' + at('class', selected ? 'bar is-selected' : 'bar') + common
        + at('data-k', ds.k) + at('data-n', ds.n) + at('data-pct', r1(v))
        + (ds.ci ? at('data-ci-lo', r1(ds.ci.lo * 100)) + at('data-ci-hi', r1(ds.ci.hi * 100)) : '')
        + at('x', nf(x)) + at('y', nf(yTop)) + at('width', nf(barW)) + at('height', nf(baseY - yTop))
        + at('rx', 4) + at('fill', color) + at('aria-label', aria)
        + '><title>' + esc(aria) + '</title></rect>';
      if (ds.ci && isNum(ds.ci.lo) && isNum(ds.ci.hi)) {
        const yHi = yOf(ds.ci.hi * 100);
        const yLo = yOf(ds.ci.lo * 100);
        const capW = Math.max(6, barW * 0.5);
        out += '<line class="err-bar" x1="' + nf(cx) + '" y1="' + nf(yHi) + '" x2="' + nf(cx) + '" y2="' + nf(yLo) + '"/>';
        out += '<line class="err-cap" x1="' + nf(cx - capW / 2) + '" y1="' + nf(yHi) + '" x2="' + nf(cx + capW / 2) + '" y2="' + nf(yHi) + '"/>';
        out += '<line class="err-cap" x1="' + nf(cx - capW / 2) + '" y1="' + nf(yLo) + '" x2="' + nf(cx + capW / 2) + '" y2="' + nf(yLo) + '"/>';
      }
      const topY = ds.ci && isNum(ds.ci.hi) ? Math.min(yTop, yOf(ds.ci.hi * 100)) : yTop;
      out += '<text class="bar-val" x="' + nf(cx) + '" y="' + nf(topY - 5) + '" text-anchor="middle">' + esc(valLabel(v, unit)) + '</text>';
    });
    out += '<text class="tick-label" x="' + nf(gx + groupW / 2) + '" y="' + (baseY + 20) + '" text-anchor="middle">'
      + esc(dlabel2(dk, s)) + '</text>';
    if (ns.length) {
      out += '<text class="tick-label" x="' + nf(gx + groupW / 2) + '" y="' + (baseY + 36) + '" text-anchor="middle">n='
        + esc(ns.join('/')) + '</text>';
    }
  });
  // 图例（SVG 内，字符串自包含）
  if (s.legend !== false) {
    let lx = pad.l;
    const ly = 14;
    arms.forEach((arm, ai) => {
      const color = arm.color || PALETTE[ai % PALETTE.length];
      out += '<rect x="' + nf(lx) + '" y="' + (ly - 9) + '" width="9" height="9" rx="2"' + at('fill', color) + '/>';
      out += '<text class="tick-label" x="' + nf(lx + 13) + '" y="' + ly + '">' + esc(arm.label) + '</text>';
      lx += 13 + Math.max(26, String(arm.label).length * 8) + 14;
    });
  }
  // 注记（口径 / Δpp / 来源）：贴在底部，颜色走 tokens
  noteLines.forEach((ln, i) => {
    const y = height - 6 - (noteLines.length - 1 - i) * 13;
    out += '<text class="tick-label" x="' + pad.l + '" y="' + nf(y) + '">' + esc(ln) + '</text>';
  });
  out += '</svg>';
  return out;
}

function dlabel2(dk, s) {
  const full = datasetLabelOf(dk, s);
  return full.length > 18 ? full.slice(0, 17) + '…' : full;
}

/**
 * buildCaliberBars(spec) ⇒ 口径消融分组柱（全样本 / 可测 / 排除 unknown）。
 * spec = { calibers|caliber|arms, datasets, title, ...同 buildGroupedBars }
 */
export function buildCaliberBars(spec) {
  const s = spec || {};
  let arms = [];
  let datasets = Array.isArray(s.datasets) && s.datasets.length ? s.datasets : null;
  let note = s.note || null;
  const cal = s.calibers || s.caliber || null;
  if (cal && Array.isArray(cal.arms) && cal.arms.length) {
    arms = cal.arms;
    datasets = datasets || cal.datasets;
    if (!note && cal.note) note = cal.note;
    if (cal.delta_pp && Object.keys(cal.delta_pp).length) {
      const parts = Object.keys(cal.delta_pp).map((k) => k + '：' + cal.delta_pp[k]);
      note = (note ? note + ' · ' : '') + 'Δpp ' + parts.join('；');
    }
  } else if (Array.isArray(s.arms) && s.arms.length) {
    arms = s.arms;
  } else if (s.arms && typeof s.arms === 'object') {
    const p = parseCalibers({ arms: s.arms });
    if (p) { arms = p.arms; datasets = datasets || p.datasets; note = note || p.note; }
  }
  return buildGroupedBars(Object.assign({}, s, {
    kind: 'caliber',
    title: s.title || '口径消融 · 分母效应（检出率 %）',
    arms: arms,
    datasets: datasets || DATASET_KEYS,
    note: note,
    emptyMsg: s.emptyMsg || '口径消融需要 caliber_ablation.arms（全样本 / 可测 / 排除 unknown）；当前无数据（' + PENDING + '）',
  }));
}

/* ══════════════════════════════════════════════════════════════════════════
   5 · 折线（系统演化：各批次变异率 / holdout 检出率）
   ══════════════════════════════════════════════════════════════════════════ */

function sortKeyOf(x) {
  const m = String(x === null || x === undefined ? '' : x).match(/(\d+)/);
  return m ? Number(m[1]) : Number.POSITIVE_INFINITY;
}

/** 按批次号排序（'645/646' ⇒ 645；无数字 ⇒ 排在最后并保持原序）。 */
export function sortPointsByBatch(points) {
  return (points || []).slice().sort((a, b) => {
    const ka = sortKeyOf(a.x);
    const kb = sortKeyOf(b.x);
    if (ka !== kb) return ka - kb;
    return String(a.x) < String(b.x) ? -1 : (String(a.x) > String(b.x) ? 1 : 0);
  });
}

function normalizeSeries(se, i) {
  if (!se || typeof se !== 'object') return null;
  const key = String(se.key ?? se.id ?? 'series-' + (i + 1));
  const label = String(se.label ?? se.name ?? key);
  const pts = Array.isArray(se.points) ? se.points : [];
  const points = pts.map((p, j) => {
    if (p === null || p === undefined || typeof p !== 'object') return null;
    const x = p.x ?? p.batch ?? p.label ?? j;
    const y = num(p.y ?? p.value ?? p.pct ?? p.rate);
    return {
      x: String(x),
      y: y,
      label: p.label === undefined || p.label === null ? null : String(p.label),
      note: p.note === undefined || p.note === null ? null : String(p.note),
      missing: y === null,
    };
  }).filter(Boolean);
  return { key: key, label: label, color: se.color || null, unit: se.unit || null, points: sortPointsByBatch(points) };
}

/**
 * buildLineChart(points|spec) ⇒ 折线 SVG：网格 + 双轴刻度 + 点（可点开明细）。
 * 支持：buildLineChart([{x:'656',y:74.8}, ...]) 或 { series:[{key,label,color,points}], xLabels, yMax, unit }
 * 缺值点（y=null）不插值，画成空心点并标「无数据」。
 */
export function buildLineChart(input) {
  const s = Array.isArray(input) ? { series: [{ key: 'series-1', label: '数值', points: input }] } : (input || {});
  let raw = s.series ?? s.points ?? [];
  if (!Array.isArray(raw)) raw = [];
  if (raw.length && !Array.isArray(raw[0].points) && (raw[0].y !== undefined || raw[0].value !== undefined)) {
    raw = [{ key: s.key || 'series-1', label: s.label || '数值', color: s.color || null, points: raw }];
  }
  const series = raw.map((se, i) => normalizeSeries(se, i)).filter((se) => se && se.points.length);
  if (!series.length) return emptyStateSvg(s.emptyMsg || '折线需要 series[].points；当前没有可渲染的数据（' + PENDING + '）');
  let xLabels = (Array.isArray(s.xLabels) && s.xLabels.length) ? s.xLabels.map(String) : null;
  if (!xLabels) {
    const seen = [];
    series.forEach((se) => se.points.forEach((p) => { if (seen.indexOf(p.x) < 0) seen.push(p.x); }));
    xLabels = seen.map((x) => ({ x: x })).sort((a, b) => sortKeyOf(a.x) - sortKeyOf(b.x)).map((o) => o.x);
  }
  const ys = [];
  series.forEach((se) => se.points.forEach((p) => { if (isNum(p.y)) ys.push(p.y); }));
  const yTop0 = ys.length ? Math.max.apply(null, ys) : 0;
  const yMax = (isNum(s.yMax) && s.yMax > 0) ? s.yMax : (s.unit === '%' && yTop0 <= 100 ? 100 : niceCeil(yTop0));
  const yMin = isNum(s.yMin) ? s.yMin : 0;
  const width = isNum(s.width) ? s.width : 760;
  const height = isNum(s.height) ? s.height : 300;
  const pad = { t: s.legend === false ? 18 : 36, r: 18, b: 46, l: 48 };
  const plotW = width - pad.l - pad.r;
  const plotH = height - pad.t - pad.b;
  const baseY = height - pad.b;
  const xOf = (x) => {
    const i = xLabels.indexOf(String(x));
    const idx = i < 0 ? 0 : i;
    return xLabels.length <= 1 ? pad.l + plotW / 2 : pad.l + (plotW * idx) / (xLabels.length - 1);
  };
  const yOf = (v) => baseY - plotH * ((Math.max(yMin, Math.min(v, yMax)) - yMin) / Math.max(1e-9, yMax - yMin));
  const ticks = 4;
  const unit = s.unit === undefined ? '%' : s.unit;
  const title = s.title || '演化折线（%）';
  let out = svgOpen(width, height, title, 'line');
  if (s.desc) out += '<desc>' + esc(Array.isArray(s.desc) ? s.desc.join('；') : s.desc) + '</desc>';
  for (let i = 0; i <= ticks; i++) {
    const y = pad.t + plotH * (i / ticks);
    const v = yMax - (yMax - yMin) * (i / ticks);
    out += '<line class="grid-line" x1="' + pad.l + '" y1="' + nf(y) + '" x2="' + nf(width - pad.r) + '" y2="' + nf(y) + '"/>';
    out += '<text class="tick-label" x="' + (pad.l - 6) + '" y="' + nf(y + 4) + '" text-anchor="end">'
      + esc(unit === '%' ? v.toFixed(0) + '%' : String(Math.round(v * 10) / 10)) + '</text>';
  }
  xLabels.forEach((x) => {
    const px = xOf(x);
    out += '<line class="grid-line" x1="' + nf(px) + '" y1="' + pad.t + '" x2="' + nf(px) + '" y2="' + baseY + '"/>';
    out += '<text class="tick-label" x="' + nf(px) + '" y="' + (baseY + 18) + '" text-anchor="middle">' + esc(x) + '</text>';
  });
  out += '<line class="axis-line" x1="' + pad.l + '" y1="' + pad.t + '" x2="' + pad.l + '" y2="' + baseY + '"/>';
  out += '<line class="axis-line" x1="' + pad.l + '" y1="' + baseY + '" x2="' + nf(width - pad.r) + '" y2="' + baseY + '"/>';
  const xTitle = s.xTitle || '批次';
  if (xTitle) out += '<text class="axis-title" x="' + nf(width - pad.r) + '" y="' + (baseY + 34) + '" text-anchor="end">' + esc(xTitle) + '</text>';
  // 折线 + 点
  series.forEach((se, si) => {
    const color = se.color || PALETTE[si % PALETTE.length];
    let d = '';
    let pen = false;
    se.points.forEach((p) => {
      if (!isNum(p.y)) { pen = false; return; }
      d += (pen ? ' L' : ' M') + nf(xOf(p.x)) + ',' + nf(yOf(p.y));
      pen = true;
    });
    if (d) out += '<path class="line-path"' + at('d', d.trim()) + at('stroke', color) + '/>';
    se.points.forEach((p) => {
      const px = xOf(p.x);
      const aria = se.label + ' ' + p.x + '：' + (isNum(p.y) ? valLabel(p.y, unit) : '无数据（' + PENDING + '）');
      if (!isNum(p.y)) {
        out += '<circle class="line-dot is-missing"' + at('data-role', 'line') + at('data-chart', 'line')
          + at('data-series', se.key) + at('data-series-label', se.label) + at('data-x', p.x)
          + at('data-missing', '1') + at('tabindex', 0) + at('cx', nf(px)) + at('cy', nf(baseY))
          + ' r="3.5"' + at('fill', 'none') + at('stroke', TOKENS.line) + at('stroke-dasharray', '2 2')
          + at('aria-label', aria) + '><title>' + esc(aria) + '</title></circle>';
        return;
      }
      const py = yOf(p.y);
      out += '<circle class="line-dot"' + at('data-role', 'line') + at('data-chart', 'line')
        + at('data-series', se.key) + at('data-series-label', se.label) + at('data-x', p.x)
        + at('data-y', r1(p.y)) + at('tabindex', 0) + at('cx', nf(px)) + at('cy', nf(py)) + ' r="4"'
        + at('fill', TOKENS.surface) + at('stroke', color) + ' stroke-width="2"'
        + at('aria-label', aria) + '><title>' + esc(aria) + '</title></circle>';
      out += '<text class="bar-val" x="' + nf(px) + '" y="' + nf(py - 9) + '" text-anchor="middle">' + esc(valLabel(p.y, unit)) + '</text>';
    });
  });
  if (s.legend !== false) {
    let lx = pad.l;
    const ly = 14;
    series.forEach((se, si) => {
      const color = se.color || PALETTE[si % PALETTE.length];
      out += '<line x1="' + nf(lx) + '" y1="' + ly + '" x2="' + nf(lx + 14) + '" y2="' + ly + '"' + at('stroke', color) + ' stroke-width="2"/>';
      out += '<text class="tick-label" x="' + nf(lx + 19) + '" y="' + (ly + 4) + '">' + esc(se.label) + '</text>';
      lx += 19 + Math.max(30, String(se.label).length * 8) + 16;
    });
  }
  out += '</svg>';
  return out;
}
/* ══════════════════════════════════════════════════════════════════════════
   6 · 饼图（检测器构成）与雷达（能力构成）
   ══════════════════════════════════════════════════════════════════════════ */

/** 数值标签：unit 为 '%' 时才带百分号，其余单位原样拼接。 */
export function valLabel(v, unit) {
  const x = num(v);
  if (x === null) return '—';
  const s = String(Math.round(x * 10) / 10);
  if (unit === '%') return s + '%';
  return s + (unit || '');
}

/**
 * buildPie(slices|spec) ⇒ 饼图 SVG。扇区带 data-key/data-label/data-value/data-pct/data-total。
 * 空（total<=0）⇒ emptyStateSvg。
 */
export function buildPie(input) {
  const s = Array.isArray(input) ? { slices: input } : (input || {});
  const raw = Array.isArray(s.slices) ? s.slices : (Array.isArray(s.data) ? s.data : []);
  const slices = raw.map((d, i) => {
    if (!d || typeof d !== 'object') return null;
    const value = num(d.value ?? d.n ?? d.count);
    if (value === null || value <= 0) return null;
    const label = String(d.label ?? d.key ?? 'slice-' + (i + 1));
    return { key: String(d.key ?? d.label ?? 'slice-' + (i + 1)), label: label, value: value, color: d.color || null, note: d.note === undefined ? null : String(d.note) };
  }).filter(Boolean);
  if (!slices.length) return emptyStateSvg(s.emptyMsg || '饼图需要 slices（value > 0）；当前没有可渲染的数据（' + PENDING + '）');
  const total = slices.reduce((a, d) => a + d.value, 0);
  const width = isNum(s.width) ? s.width : 620;
  const height = isNum(s.height) ? s.height : Math.max(240, 60 + slices.length * 26);
  const cx = isNum(s.cx) ? s.cx : 148;
  const cy = isNum(s.cy) ? s.cy : height / 2;
  const r = isNum(s.r) ? s.r : Math.min(104, height / 2 - 26);
  const title = s.title || '构成饼图';
  let out = svgOpen(width, height, title, 'pie');
  if (s.desc) out += '<desc>' + esc(Array.isArray(s.desc) ? s.desc.join('；') : s.desc) + '</desc>';
  let a0 = -Math.PI / 2;
  slices.forEach((d, i) => {
    const frac = d.value / total;
    const pct = frac * 100;
    const a1 = a0 + frac * Math.PI * 2;
    const color = d.color || PALETTE[i % PALETTE.length];
    const aria = d.label + '：' + d.value + ' / ' + total + '（' + fmtPct(pct) + '）';
    let dPath;
    if (frac >= 0.9999) {
      dPath = 'M' + nf(cx - r) + ',' + nf(cy)
        + ' a' + nf(r) + ',' + nf(r) + ' 0 1 0 ' + nf(2 * r) + ',0'
        + ' a' + nf(r) + ',' + nf(r) + ' 0 1 0 ' + nf(-2 * r) + ',0 Z';
    } else {
      const large = (a1 - a0) > Math.PI ? 1 : 0;
      const x0 = cx + r * Math.cos(a0);
      const y0 = cy + r * Math.sin(a0);
      const x1 = cx + r * Math.cos(a1);
      const y1 = cy + r * Math.sin(a1);
      dPath = 'M' + nf(cx) + ',' + nf(cy) + ' L' + nf(x0) + ',' + nf(y0)
        + ' A' + nf(r) + ',' + nf(r) + ' 0 ' + large + ' 1 ' + nf(x1) + ',' + nf(y1) + ' Z';
    }
    out += '<path' + at('class', 'pie-seg') + at('data-role', 'pie') + at('data-chart', 'pie')
      + at('data-key', d.key) + at('data-label', d.label) + at('data-value', d.value)
      + at('data-pct', r1(pct)) + at('data-total', total) + at('tabindex', 0)
      + at('d', dPath) + at('fill', color) + at('stroke', TOKENS.bg) + ' stroke-width="1.5"'
      + at('aria-label', aria) + '><title>' + esc(aria) + '</title></path>';
    if (pct >= 8) {
      const mid = (a0 + a1) / 2;
      const tx = cx + r * 0.62 * Math.cos(mid);
      const ty = cy + r * 0.62 * Math.sin(mid);
      out += '<text class="bar-val" x="' + nf(tx) + '" y="' + nf(ty + 4) + '" text-anchor="middle"'
        + at('fill', TOKENS.bg) + '>' + esc(Math.round(pct) + '%') + '</text>';
    }
    a0 = a1;
  });
  const lx = cx + r + 26;
  slices.forEach((d, i) => {
    const y = 34 + i * 26;
    const color = d.color || PALETTE[i % PALETTE.length];
    out += '<rect x="' + nf(lx) + '" y="' + (y - 9) + '" width="10" height="10" rx="2"' + at('fill', color) + '/>';
    out += '<text class="tick-label" x="' + nf(lx + 16) + '" y="' + y + '">' + esc(d.label) + '</text>';
    out += '<text class="tick-label" x="' + nf(width - 10) + '" y="' + y + '" text-anchor="end">'
      + esc(d.value + ' · ' + fmtPct((d.value / total) * 100)) + '</text>';
  });
  out += '</svg>';
  return out;
}

function normalizeAxis(a, i, spec) {
  if (!a || typeof a !== 'object') return null;
  const key = String(a.key ?? a.id ?? 'axis-' + (i + 1));
  const max = num(a.max ?? a.target ?? (spec && spec.max));
  const value = num(a.value);
  return {
    key: key,
    label: String(a.label ?? a.name ?? key),
    value: value,
    max: (max !== null && max > 0) ? max : 100,
    unit: a.unit === undefined || a.unit === null ? '' : String(a.unit),
    display: a.display === undefined || a.display === null ? null : String(a.display),
    source: a.source === undefined || a.source === null ? null : String(a.source),
    missing: value === null,
  };
}

/**
 * buildRadar(axes|spec) ⇒ 雷达 SVG（轴可配置：label/value/max/unit/display/source）。
 * 轴 < 3 ⇒ emptyStateSvg。缺值的轴按 0 画并标「缺」，不猜测。
 */
export function buildRadar(input) {
  const s = Array.isArray(input) ? { axes: input } : (input || {});
  const axes = (Array.isArray(s.axes) ? s.axes : []).map((a, i) => normalizeAxis(a, i, s)).filter(Boolean);
  if (axes.length < 3) return emptyStateSvg(s.emptyMsg || '雷达图至少需要 3 个可配置轴；当前没有可渲染的数据（' + PENDING + '）');
  const width = isNum(s.width) ? s.width : 560;
  const height = isNum(s.height) ? s.height : 380;
  const cx = isNum(s.cx) ? s.cx : width / 2;
  const cy = isNum(s.cy) ? s.cy : height / 2 + 8;
  const r = isNum(s.r) ? s.r : Math.max(60, Math.min(width, height) / 2 - 82);
  const rings = isNum(s.rings) ? Math.max(2, Math.round(s.rings)) : 4;
  const title = s.title || '能力构成雷达图';
  const n = axes.length;
  const pt = (i, rr) => {
    const ang = -Math.PI / 2 + (i * 2 * Math.PI) / n;
    return [cx + rr * Math.cos(ang), cy + rr * Math.sin(ang)];
  };
  const ratioOf = (a) => (a.missing ? 0 : Math.max(0, Math.min(1, a.value / a.max)));
  let out = svgOpen(width, height, title, 'radar');
  if (s.desc) out += '<desc>' + esc(Array.isArray(s.desc) ? s.desc.join('；') : s.desc) + '</desc>';
  for (let k = 1; k <= rings; k++) {
    const rr = (r * k) / rings;
    const pts = axes.map((a, i) => pt(i, rr).map(nf).join(',')).join(' ');
    out += '<polygon class="radar-grid"' + at('points', pts) + '/>';
  }
  axes.forEach((a, i) => {
    const p = pt(i, r);
    out += '<line class="radar-axis" x1="' + nf(cx) + '" y1="' + nf(cy) + '" x2="' + nf(p[0]) + '" y2="' + nf(p[1]) + '"/>';
  });
  const dataPts = axes.map((a, i) => pt(i, r * ratioOf(a)).map(nf).join(',')).join(' ');
  out += '<polygon class="radar-area"' + at('points', dataPts) + at('fill', TOKENS.accentSoft)
    + at('stroke', TOKENS.accent) + ' stroke-width="2"/>';
  axes.forEach((a, i) => {
    const p = pt(i, Math.max(2, r * ratioOf(a)));
    const aria = a.label + '：' + (a.missing ? '缺数据（' + PENDING + '）' : a.value + a.unit + ' / 目标 ' + a.max + a.unit)
      + (a.source ? '（来源：' + a.source + '）' : '');
    out += '<circle class="line-dot radar-dot"' + at('data-role', 'radar') + at('data-chart', 'radar')
      + at('data-axis', a.key) + at('data-label', a.label) + at('data-value', a.missing ? null : a.value)
      + at('data-max', a.max) + at('data-unit', a.unit) + at('data-source', a.source)
      + (a.missing ? at('data-missing', '1') : '') + at('tabindex', 0)
      + at('cx', nf(p[0])) + at('cy', nf(p[1])) + ' r="4"'
      + at('fill', a.missing ? TOKENS.surface : TOKENS.accent) + at('stroke', TOKENS.accent)
      + at('aria-label', aria) + '><title>' + esc(aria) + '</title></circle>';
    const lp = pt(i, r + 20);
    const ang = -Math.PI / 2 + (i * 2 * Math.PI) / n;
    const cosv = Math.cos(ang);
    const anchor = Math.abs(cosv) < 0.25 ? 'middle' : (cosv > 0 ? 'start' : 'end');
    const text = a.display || (a.label + ' ' + (a.missing ? '—' : a.value + a.unit));
    out += '<text class="radar-label" x="' + nf(lp[0]) + '" y="' + nf(lp[1] + 3) + '"'
      + at('text-anchor', anchor) + '>' + esc(text) + '</text>';
  });
  out += '</svg>';
  return out;
}

/** 按 kind 分发到具体 builder；未知 kind / 空数据 ⇒ 空状态（不抛）。 */
export function renderChart(kind, spec) {
  let k = kind;
  let s = spec;
  if (kind && typeof kind === 'object') { s = kind; k = kind.kind || kind.type || kind.chart || (kind.axes ? 'radar' : (kind.slices ? 'pie' : (kind.series ? 'line' : 'groupedBars'))); }
  const o = s || {};
  switch (String(k === null || k === undefined ? '' : k).trim().toLowerCase()) {
    case 'groupedbars': case 'grouped': case 'bars': case 'bar': return buildGroupedBars(o);
    case 'caliberbars': case 'caliber': case 'caliber_ablation': return buildCaliberBars(o);
    case 'line': case 'linechart': case 'evolution': return buildLineChart(o);
    case 'pie': case 'donut': return buildPie(o);
    case 'radar': case 'spider': return buildRadar(o);
    case 'empty': return emptyStateSvg(o.msg || o.emptyMsg);
    default: return emptyStateSvg(o.emptyMsg || ('未知图表类型「' + String(k === null || k === undefined ? '' : k) + '」'));
  }
}

/* ══════════════════════════════════════════════════════════════════════════
   7 · 交互逻辑（纯函数）：点击 → 选中 → 明细文本/HTML
   ══════════════════════════════════════════════════════════════════════════ */

/** 把点击目标的 data-* （element.dataset 或普通对象）归一成选中描述。 */
export function selectionFromDataset(ds) {
  const s = ds || {};
  const pick = function () {
    for (let i = 0; i < arguments.length; i++) {
      const v = s[arguments[i]];
      if (v !== undefined && v !== null && v !== '') return v;
    }
    return null;
  };
  const arm = pick('arm');
  const dataset = pick('dataset');
  const series = pick('series');
  const axis = pick('axis');
  const key = pick('key');
  let kind = pick('role', 'chart', 'kind');
  if (!kind) kind = axis !== null ? 'radar' : (series !== null ? 'line' : ((key !== null && arm === null && dataset === null) ? 'pie' : 'bar'));
  else kind = String(kind).toLowerCase();
  if (kind === 'grouped' || kind === 'groupedbars' || kind === 'bars' || kind === 'bar') kind = 'bar';
  const label = pick('label');
  return {
    kind: kind,
    arm: arm === null ? null : String(arm),
    dataset: dataset === null ? null : String(dataset),
    k: num(pick('k')),
    n: num(pick('n')),
    ciLo: num(pick('ciLo', 'ci-lo')),
    ciHi: num(pick('ciHi', 'ci-hi')),
    pct: num(pick('pct')),
    key: key === null ? null : String(key),
    label: label === null ? null : String(label),
    value: num(pick('value')),
    total: num(pick('total')),
    max: num(pick('max')),
    series: series === null ? null : String(series),
    seriesLabel: pick('seriesLabel') === null ? null : String(pick('seriesLabel')),
    x: pick('x') === null ? null : String(pick('x')),
    y: num(pick('y')),
    axis: axis === null ? null : String(axis),
    unit: pick('unit') === null ? '' : String(pick('unit')),
    source: pick('source') === null ? null : String(pick('source')),
    missing: pick('missing') !== null,
  };
}

/** 汇总样本清单文本（限 limit 条）。 */
export function samplesText(samples, limit) {
  const lim = isNum(limit) ? limit : 12;
  const list = Array.isArray(samples) ? samples.filter(Boolean) : [];
  if (!list.length) return '源数据未附逐样本清单（只有汇总 k/n）';
  const ids = list.slice(0, lim).map((x) => (x && x.id) ? String(x.id) : String(x));
  const more = list.length > lim ? '…（共 ' + list.length + ' 条）' : '';
  return ids.join('、') + more;
}

function collectArms(data) {
  if (!data) return [];
  if (Array.isArray(data)) return data;
  if (Array.isArray(data.arms) && data.arms.length) return data.arms;
  if (data.calibers && Array.isArray(data.calibers.arms)) return data.calibers.arms;
  return [];
}

/**
 * selectionDetail(data, sel, opts) ⇒ 明细对象
 *   { ok, kind, title, rows:[[label,value]], text, samples, samplesText, note }
 * 柱/口径：k/n/CI/百分比/样本列表；饼：计数/占比；线：批次/数值；雷达：轴/数值/目标/完成度/来源。
 */
export function selectionDetail(data, sel, opts) {
  const o = opts || {};
  const s = sel || {};
  const rows = [];
  const push = (k, v) => rows.push([String(k), (v === null || v === undefined || v === '') ? '—' : String(v)]);
  const note = (o.note === undefined || o.note === null) ? null : String(o.note);

  if (s.kind === 'pie') {
    const total = num(s.total);
    const value = num(s.value);
    const pct = (total && value !== null) ? (value / total) * 100 : null;
    const title = String(s.label || s.key || '扇区');
    push('扇区', title);
    push('计数', value);
    push('占比', fmtPct(pct));
    push('总数', total);
    const head = title + '：' + (value === null ? '—' : value) + ' / ' + (total === null ? '—' : total);
    return { ok: true, kind: 'pie', title: title, rows: rows, text: head + ' = ' + fmtPct(pct), samples: [], samplesText: null, note: note };
  }

  if (s.kind === 'line') {
    const y = num(s.y);
    const title = String(s.seriesLabel || s.series || '折线点') + ' @ ' + String(s.x === null ? '—' : s.x);
    push('批次', s.x);
    push('序列', s.seriesLabel || s.series);
    push('数值', y === null ? '无数据（' + PENDING + '）' : valLabel(y, s.unit));
    push('说明', y === null ? '该批次未产出真实值：不插值、不推测' : '真实值（产物现算）');
    return {
      ok: true, kind: 'line', title: title, rows: rows,
      text: title + '：' + (y === null ? '无数据（' + PENDING + '）' : valLabel(y, s.unit)),
      samples: [], samplesText: null, note: note,
    };
  }

  if (s.kind === 'radar') {
    const value = num(s.value);
    const max = num(s.max);
    const ratio = (value !== null && max) ? (value / max) * 100 : null;
    const title = String(s.label || s.axis || '能力轴');
    push('轴', title);
    push('实际值', value === null ? '缺数据（' + PENDING + '）' : valLabel(value, s.unit));
    push('目标值', max === null ? '—' : valLabel(max, s.unit));
    push('完成度', fmtPct(ratio));
    push('来源', s.source);
    return {
      ok: true, kind: 'radar', title: title, rows: rows,
      text: title + '：' + (value === null ? '缺数据' : valLabel(value, s.unit)) + ' / 目标 ' + (max === null ? '—' : valLabel(max, s.unit)) + '（' + fmtPct(ratio) + '）',
      samples: [], samplesText: null, note: note,
    };
  }

  // 柱 / 口径消融
  const arms = collectArms(data);
  let arm = null;
  let ds = null;
  if (arms.length) {
    for (const a of arms) if (a && String(a.key) === String(s.arm)) { arm = a; break; }
    if (arm && s.dataset && arm.datasets) ds = arm.datasets[s.dataset] || null;
  }
  const k = ds ? ds.k : num(s.k);
  const n = ds ? ds.n : num(s.n);
  let ci = ds ? ds.ci : null;
  if (!ci && num(s.ciLo) !== null && num(s.ciHi) !== null) ci = { lo: num(s.ciLo) / 100, hi: num(s.ciHi) / 100 };
  const rate = ds ? datasetRatePct(ds) : num(s.pct);
  const title = (arm ? arm.label : String(s.arm || '臂')) + ' × ' + datasetLabelOf(s.dataset, o);
  push('臂', arm ? arm.label : s.arm);
  push('数据集', datasetLabelOf(s.dataset, o));
  push('k / n', (k === null ? '—' : k) + ' / ' + (n === null ? '—' : n));
  push('检出率', fmtPct(rate));
  push('Wilson 95% CI', ci ? (fmtPct(ci.lo * 100) + ' – ' + fmtPct(ci.hi * 100)) : '不可估（n=0）');
  if (ds && ds.cp) push('C-P 95% CI', fmtPct(ds.cp.lo * 100) + ' – ' + fmtPct(ds.cp.hi * 100));
  push('口径 / 分母', ds ? (ds.denominatorText || ds.note || (ds.n !== null ? 'n=' + ds.n : '—')) : '—');
  push('来源', ds && ds.source ? ds.source : (ds && ds.cmd ? ds.cmd : '—'));
  const stext = samplesText(ds ? ds.samples : [], o.samplesLimit);
  push('样本列表', stext);
  return {
    ok: true, kind: (s.kind === 'caliber' ? 'caliber' : 'bar'), title: title, rows: rows,
    text: title + '：' + describeSample(k, n, ci),
    samples: ds ? ds.samples : [], samplesText: stext,
    note: note || (ds && ds.conflicts && ds.conflicts.length ? ds.conflicts.join('；') : null),
  };
}

/** 明细对象 → .detail-panel 内 HTML（全部转义）。 */
export function detailPanelHtml(detail) {
  const d = detail || {};
  if (!d.ok) {
    return '<p class="muted">' + esc(d.text || '点击柱子 / 扇区 / 点查看 k/n、置信区间与样本明细') + '</p>';
  }
  let html = '<h4 class="section-title">' + esc(d.title || '明细') + '</h4>';
  html += '<dl>' + (d.rows || []).map((r) => '<dt>' + esc(r[0]) + '</dt><dd>' + esc(r[1]) + '</dd>').join('') + '</dl>';
  if (d.note) html += '<p class="section-sub">' + esc(d.note) + '</p>';
  return html;
}

/* ══════════════════════════════════════════════════════════════════════════
   8 · 真实数据 → 图表输入（演化 / 检测器构成 / 能力构成）
   ══════════════════════════════════════════════════════════════════════════ */

/**
 * 演化折线数据：批次骨架取 timeline，率值只取**能追溯到批次**的真实产物。
 * 契约（670a）：baseline_*.json 可带 evolution:[{batch,mutation_pct,holdout_pct,note}]。
 */
export function buildEvolutionSeries(sources) {
  const s = sources || {};
  const rows = new Map();
  const notes = [];
  const touch = (batch) => {
    const b = String(batch === null || batch === undefined ? '' : batch).trim();
    if (!b) return null;
    if (!rows.has(b)) rows.set(b, { batch: b, mutation_pct: null, holdout_pct: null, note: null, origin: [] });
    return rows.get(b);
  };
  const mark = (row, tag) => { if (row && row.origin.indexOf(tag) < 0) row.origin.push(tag); };

  if (Array.isArray(s.evolution)) {
    s.evolution.forEach((r) => {
      if (!r || typeof r !== 'object') return;
      const row = touch(r.batch);
      if (!row) return;
      const m = num(r.mutation_pct);
      const h = num(r.holdout_pct);
      if (m !== null) row.mutation_pct = m;
      if (h !== null) row.holdout_pct = h;
      if (r.note) row.note = String(r.note);
      mark(row, 'evolution');
    });
  }
  const timelines = [];
  if (s.metrics666 && Array.isArray(s.metrics666.timeline)) timelines.push(s.metrics666.timeline);
  if (s.experiments && Array.isArray(s.experiments.timeline)) timelines.push(s.experiments.timeline);
  timelines.forEach((tl) => tl.forEach((t) => { if (t && t.batch !== undefined) mark(touch(t.batch), 'timeline'); }));

  const m666 = (s.metrics666 && s.metrics666.metrics) ? s.metrics666.metrics : null;
  if (m666 && m666.holdout && num(m666.holdout.rate_pct) !== null) {
    const row = touch('666');
    if (row && row.holdout_pct === null) row.holdout_pct = num(m666.holdout.rate_pct);
    mark(row, 'metrics_666');
  }
  if (s.experiments && Array.isArray(s.experiments.mutation) && s.experiments.mutation.length) {
    const core = s.experiments.mutation.filter((m) => /core/i.test(String(m && m.label)))[0] || s.experiments.mutation[0];
    const v = core ? num(core.rate) : null;
    if (v !== null) {
      const row = touch('666');
      if (row && row.mutation_pct === null) row.mutation_pct = v;
      mark(row, 'experiments');
    }
  }
  if (s.experiments669) {
    const p = parseBaseline(s.experiments669);
    if (p.datasets.holdout) {
      const row = touch('669');
      if (row && row.holdout_pct === null) row.holdout_pct = datasetRatePct(p.datasets.holdout);
      mark(row, '669_experiments');
    }
    if (p.datasets.corpus && num(s.corpusBatch) !== null) {
      const row = touch(s.corpusBatch);
      if (row && row.holdout_pct === null) row.holdout_pct = datasetRatePct(p.datasets.corpus);
      mark(row, '669_experiments');
    }
  }
  const batches = Array.from(rows.values()).sort((a, b) => (sortKeyOf(a.batch) - sortKeyOf(b.batch)) || (a.batch < b.batch ? -1 : 1));
  const known = batches.filter((r) => r.mutation_pct !== null || r.holdout_pct !== null).map((r) => r.batch);
  const series = [
    { key: 'mutation', label: '变异杀死率（内部自证 %）', color: TOKENS.pass, unit: '%', points: batches.map((r) => ({ x: r.batch, y: r.mutation_pct, label: r.batch + ' 变异杀死率', note: r.note })) },
    { key: 'holdout', label: 'holdout 检出率（%）', color: TOKENS.accent, unit: '%', points: batches.map((r) => ({ x: r.batch, y: r.holdout_pct, label: r.batch + ' holdout 检出率', note: r.note })) },
  ];
  notes.push('批次骨架取自 metrics_666.json / experiments.json 的 timeline；有真实率值的批次：' + (known.length ? known.join('、') : '无'));
  notes.push('无真实值的批次点显式留空（不插值、不推测）；逐批次变异率待 670a 写入 evolution 字段。');
  return { ok: known.length > 0, series: series, batches: batches.map((r) => r.batch), rows: batches, notes: notes };
}

/** 检测器构成（sanitizer / compiler-warn / cross-compile / perf / compile-time）；缺则回退 holdout 结果分布。 */
export function buildDetectorSlices(sources) {
  const s = sources || {};
  const dets = normalizeDetectors(s.detectors);
  if (dets.length) {
    return { slices: dets, pending: false, source: 'detectors', note: '检测器构成来自产物 detectors 字段（真实计数）' };
  }
  const exp = s.experiments;
  const outcomes = (exp && Array.isArray(exp.holdout_outcomes)) ? exp.holdout_outcomes : null;
  if (outcomes && outcomes.length) {
    const slices = outcomes.map((d, i) => ({
      key: String((d && d.label) ?? 'outcome-' + (i + 1)),
      label: String((d && d.label) ?? 'outcome-' + (i + 1)),
      value: num(d && d.value) === null ? 0 : num(d.value),
      color: null,
    })).filter((d) => d.value > 0);
    if (slices.length) {
      return {
        slices: slices, pending: true, source: 'holdout_outcomes',
        note: '检测器构成（sanitizer / compiler-warn / cross-compile / perf / compile-time）待 670a 生成 detectors 字段；此处回退显示 holdout 结果分布（真实值）',
      };
    }
  }
  return { slices: [], pending: true, source: null, note: '检测器构成与回退数据都不可用（' + PENDING + '）' };
}

/** 能力构成雷达轴：真实值 + 各轴目标（来自产物自身声明）。 */
export function buildAbilityAxes(sources) {
  const s = sources || {};
  const m = (s.metrics666 && s.metrics666.metrics) ? s.metrics666.metrics : null;
  const st = s.status || null;
  const exp = s.experiments || null;
  const ability = (exp && Array.isArray(exp.ability)) ? exp.ability : null;
  const fromAbility = (re) => {
    if (!ability) return null;
    const hit = ability.filter((a) => re.test(String(a && a.label)))[0];
    return hit ? num(hit.value) : null;
  };
  const pickNum = (cands, label) => {
    for (const c of cands) { const v = num(c); if (v !== null) return { value: v, source: label }; }
    return { value: null, source: label };
  };
  const mutationCore = (exp && Array.isArray(exp.mutation)) ? (exp.mutation.filter((x) => /core/i.test(String(x && x.label)))[0] || exp.mutation[0]) : null;
  const conf = {
    rules: pickNum([st && st.rules && st.rules.rules_total, m && m.rules_total, fromAbility(/门禁规则|规则/)], 'status.rules.rules_total'),
    protectors: pickNum([st && st.protectors && st.protectors.protectors_total, fromAbility(/保护器/)], 'status.protectors.protectors_total'),
    ledger: pickNum([m && m.ledger_events, fromAbility(/账本/)], 'metrics_666.metrics.ledger_events'),
    cards: pickNum([m && m.cards_real, st && st.cards && st.cards.cards_real, fromAbility(/知识卡/)], 'metrics_666.metrics.cards_real'),
    nodes: pickNum([s.graphNodes, st && st.w2 && st.w2.nodes, fromAbility(/节点/)], 'data/graph.json nodes.length'),
    mutation: { value: mutationCore ? num(mutationCore.rate) : null, source: mutationCore ? 'experiments.mutation[' + String(mutationCore.label) + '].rate' : 'experiments.mutation' },
  };
  const axes = ABILITY_TARGETS.map((t) => {
    const c = conf[t.key] || { value: null, source: t.source };
    return {
      key: t.key, label: t.label, unit: t.unit, value: c.value, max: t.target,
      source: c.source || t.source, missing: c.value === null,
      display: t.label + ' ' + (c.value === null ? '—' : c.value + t.unit),
    };
  });
  const missing = axes.filter((a) => a.missing).map((a) => a.key);
  const notes = ['各轴目标是产物自身声明的规模（67 / 9 / 452 / 42 / 178 / 100%），比值只表示「完工度」，不是能力分数'];
  if (missing.length) notes.push('缺真实值的轴：' + missing.join('、') + '（按 0 画并标注缺，不猜测）');
  return { axes: axes, missing: missing, notes: notes };
}

/* ══════════════════════════════════════════════════════════════════════════
   9 · 兼容层：669c 基线冒烟 web/tests/smoke.mjs 用到的两个旧接口
   —— 只有这两个函数会写 DOM，且容器由调用方传入（不读全局 document）。
   ══════════════════════════════════════════════════════════════════════════ */

/**
 * @deprecated 新代码用 buildGroupedBars(spec) 取 SVG 字符串。
 * 旧签名兼容：barChart(hostEl, [{label,value}], {max,unit,height,width}) ⇒ hostEl.innerHTML = <svg>
 */
export function barChart(host, data, opts) {
  const s = opts || {};
  const list = Array.isArray(data) ? data : [];
  const arms = list.map((d, i) => {
    const value = num(d && (d.value ?? d.rate_pct));
    const label = String((d && (d.label ?? d.key)) ?? 'bar-' + (i + 1));
    return {
      key: String((d && (d.key ?? d.label)) ?? 'bar-' + (i + 1)),
      label: label,
      color: (d && d.color) || null,
      datasets: { holdout: { label: label, rate_pct: value, k: (d && num(d.k)) === null ? null : num(d.k), n: (d && num(d.n)) === null ? null : num(d.n) } },
    };
  });
  const svg = buildGroupedBars({
    arms: arms, datasets: ['holdout'], kind: 'grouped',
    title: s.title || '柱状图',
    unit: s.unit === undefined ? '' : s.unit,
    max: s.max, width: s.width, height: s.height, legend: false,
    datasetLabels: { holdout: s.datasetLabel || '数值' },
  });
  if (host && typeof host === 'object') host.innerHTML = svg;
  return svg;
}

/**
 * @deprecated 新代码用 buildPie(spec) 取 SVG 字符串。
 * 旧签名兼容：pieChart(hostEl, [{label,value}]) ⇒ hostEl.innerHTML = <svg>
 */
export function pieChart(host, data) {
  const svg = buildPie({ slices: Array.isArray(data) ? data : [], title: '构成饼图' });
  if (host && typeof host === 'object') host.innerHTML = svg;
  return svg;
}

/** 旧接口：空状态提示（现在返回 SVG 字符串，host 可选）。 */
export function notice(host, text) {
  const svg = emptyStateSvg(text);
  if (host && typeof host === 'object') host.innerHTML = svg;
  return svg;
}


