// 670c3 · 前端健壮性纯逻辑（可被 Node 直接测试，无 DOM 依赖）
// 与 verify_core / graph_core / learn_engine 同级：纯函数，浏览器与 Node 共用。
// 目标：任何异常都不白屏 —— 状态判定、重试策略、友好文案全部在此，UI 只做渲染。

export const RETRY_MAX = 3;
export const RETRY_DELAY_MS = 1000;

/** 是否还应重试（attempt 从 1 计）。 */
export function shouldRetry(attempt, max = RETRY_MAX) {
  return Number.isFinite(attempt) && attempt >= 1 && attempt < max;
}

/** 第 attempt 次失败后的等待毫秒（固定间隔，避免指数退避掩盖问题）。 */
export function retryDelayMs(_attempt) {
  return RETRY_DELAY_MS;
}

/**
 * 判定一份已解析的数据处于什么状态。
 * @param {*} data 已 JSON.parse 的结果（或 null/undefined）
 * @param {string[]} requiredKeys 必须存在的顶层字段
 * @returns {{state:'ok'|'empty', missing:string[]}}
 */
export function classifyPayload(data, requiredKeys = []) {
  if (data === null || data === undefined) return { state: 'empty', missing: requiredKeys.slice() };
  if (typeof data !== 'object') return { state: 'ok', missing: [] };
  const missing = requiredKeys.filter((k) => data[k] === undefined || data[k] === null);
  const isEmptyObj = !Array.isArray(data) && Object.keys(data).length === 0;
  if (isEmptyObj || missing.length > 0) return { state: 'empty', missing };
  return { state: 'ok', missing: [] };
}

/**
 * 把错误归类为面向用户的友好文案。
 * @param {string} kind network|missing|parse|http|unknown
 * @returns {{title:string, hint:string, action:string, retry:boolean}}
 */
export function friendlyError(kind) {
  switch (kind) {
    case 'network':
      return { title: '数据加载失败', hint: '可能是网络中断，或本地服务器未启动。', action: '重试', retry: true };
    case 'missing':
      return { title: '数据文件缺失', hint: '目标 JSON 不存在或尚未生成。', action: '重试', retry: true };
    case 'parse':
      return { title: '数据格式异常', hint: '返回内容不是合法 JSON，可能是文件损坏。', action: '重试', retry: true };
    case 'http':
      return { title: '服务器返回错误', hint: 'HTTP 状态非 2xx，请检查本地服务。', action: '重试', retry: true };
    default:
      return { title: '页面初始化失败', hint: '发生了未预期的错误。', action: '刷新页面', retry: false };
  }
}

/** 把 fetch 的失败原因归类为 kind。 */
export function classifyFetchError(err) {
  const msg = String((err && err.message) || err || '');
  if (/Failed to fetch|NetworkError|ERR_|net::/i.test(msg)) return 'network';
  if (/404|not found/i.test(msg)) return 'missing';
  if (/JSON|Unexpected token|parse/i.test(msg)) return 'parse';
  if (/HTTP \d/i.test(msg)) return 'http';
  return 'unknown';
}

/** 空状态模型（图标 + 文案 + 引导动作）。 */
export function emptyModel(kind = 'no-data') {
  const models = {
    'no-data': { icon: '∅', text: '暂无数据', action: '刷新' },
    'no-commits': { icon: '⌛', text: '暂无提交记录', action: '刷新' },
    'no-match': { icon: '🔍', text: '无匹配项', action: '清除筛选' },
    'need-js': { icon: '⚙', text: '此功能需要 JavaScript', action: '启用 JavaScript' },
  };
  return models[kind] || models['no-data'];
}

/**
 * 指标显示：0 或缺失显示 '--'（避免把"无数据"误读成"确实是 0"）。
 */
export function formatMetric(v) {
  if (v === null || v === undefined || v === '' ) return '--';
  if (typeof v === 'number' && v === 0) return '--';
  return String(v);
}

/** 三次失败后的最终提示（E2/B2 要求）。 */
export function exhaustedHint() {
  return '请检查本地服务器是否启动（python -m http.server）后刷新。';
}

/** 生成 noscript 纯 HTML（用于测试与生成一致性）。 */
export function noscriptHtml({ title, lines = [], note = '请启用 JavaScript 以获得完整体验。' }) {
  const body = lines.map((l) => `<p>${l}</p>`).join('');
  return `<noscript><div class="ns-fallback"><h1>${title}</h1>${body}<p class="ns-note">${note}</p></div></noscript>`;
}
