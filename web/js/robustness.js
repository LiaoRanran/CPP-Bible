// 670c3 · 前端健壮性 DOM 胶水层
// 职责：全局运行时错误兜底 + 带重试的 fetchJSON + 错误卡/空状态渲染 + 骨架屏切换。
// 纯逻辑在 robustness_core.js；本文件只碰 DOM。所有页面统一 import 本模块。
import {
  RETRY_MAX, shouldRetry, retryDelayMs, classifyPayload, friendlyError,
  classifyFetchError, emptyModel, formatMetric, exhaustedHint,
} from './robustness_core.js';

export { formatMetric, emptyModel, classifyPayload, friendlyError };

const BANNER_ID = 'qy-error-banner';

/** 顶部错误横幅（全局兜底用）。 */
export function ensureBanner() {
  if (typeof document === 'undefined') return null;
  let el = document.getElementById(BANNER_ID);
  if (el) return el;
  el = document.createElement('div');
  el.id = BANNER_ID;
  el.className = 'qy-banner';
  el.setAttribute('role', 'alert');
  el.setAttribute('aria-live', 'assertive');
  el.hidden = true;
  el.innerHTML = '<span class="qy-banner-msg"></span>' +
    '<button type="button" class="qy-banner-close" aria-label="关闭">×</button>';
  el.querySelector('.qy-banner-close').addEventListener('click', () => hideBanner());
  (document.body || document.documentElement).prepend(el);
  return el;
}

export function showBanner(msg) {
  const el = ensureBanner();
  if (!el) return;
  el.querySelector('.qy-banner-msg').textContent = msg;
  el.hidden = false;
}

export function hideBanner() {
  const el = typeof document !== 'undefined' && document.getElementById(BANNER_ID);
  if (el) el.hidden = true;
}

/** 安装全局兜底：window.onerror + unhandledrejection。重复调用安全。 */
export function installGlobalErrorHandlers() {
  if (typeof window === 'undefined' || window.__qyRobustnessInstalled) return;
  window.__qyRobustnessInstalled = true;
  window.addEventListener('error', (e) => {
    console.error('[qy] window.onerror:', e.error || e.message);
    showBanner('页面初始化失败，请刷新重试');
  });
  window.addEventListener('unhandledrejection', (e) => {
    console.error('[qy] unhandledrejection:', e.reason);
    showBanner('页面初始化失败，请刷新重试');
  });
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/**
 * 带重试的 JSON 加载。失败 3 次后抛错（附 kind）。
 * @param {string} url
 * @param {{retries?:number, requiredKeys?:string[], onAttempt?:Function}} [opts]
 * @returns {Promise<{data:*, state:'ok'|'empty', attempts:number, kind?:string}>}
 */
export async function fetchJSON(url, opts = {}) {
  const max = opts.retries ?? RETRY_MAX;
  let lastErr = null;
  for (let attempt = 1; attempt <= max; attempt++) {
    try {
      if (opts.onAttempt) opts.onAttempt(attempt);
      const res = await fetch(url, { cache: 'no-cache' });
      if (!res.ok) { const e = new Error('HTTP ' + res.status); e.kind = 'http'; throw e; }
      const data = await res.json();
      const cls = classifyPayload(data, opts.requiredKeys || []);
      return { data, state: cls.state, attempts: attempt };
    } catch (err) {
      lastErr = err;
      const kind = err.kind || classifyFetchError(err);
      lastErr.kind = kind;
      console.error(`[qy] fetchJSON(${url}) 第 ${attempt}/${max} 次失败:`, err);
      if (shouldRetry(attempt, max)) { await sleep(retryDelayMs(attempt)); continue; }
      break;
    }
  }
  throw lastErr || new Error('unknown');
}

/** 渲染错误卡（含重试按钮）。 */
export function renderErrorCard(container, kind, onRetry) {
  if (!container) return;
  const m = friendlyError(kind);
  container.innerHTML = '';
  const card = document.createElement('div');
  card.className = 'qy-error-card';
  card.setAttribute('role', 'alert');
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'qy-btn';
  btn.textContent = m.action;
  if (m.retry && onRetry) btn.addEventListener('click', onRetry);
  else btn.addEventListener('click', () => location.reload());
  card.innerHTML = `<div class="qy-err-icon" aria-hidden="true">⚠</div>` +
    `<div class="qy-err-title">${m.title}</div>` +
    `<div class="qy-err-hint">${m.hint}</div>` +
    `<div class="qy-err-final">${exhaustedHint()}</div>`;
  card.appendChild(btn);
  container.appendChild(card);
}

/** 渲染空状态（可选"清除筛选"按钮）。 */
export function renderEmpty(container, kind = 'no-data', onAction) {
  if (!container) return;
  const m = emptyModel(kind);
  container.innerHTML = '';
  const box = document.createElement('div');
  box.className = 'qy-empty';
  box.setAttribute('role', 'status');
  box.innerHTML = `<div class="qy-empty-icon" aria-hidden="true">${m.icon}</div>` +
    `<div class="qy-empty-text">${m.text}</div>`;
  if (onAction) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'qy-btn';
    btn.textContent = m.action;
    btn.addEventListener('click', onAction);
    box.appendChild(btn);
  }
  container.appendChild(box);
}

/** 切换容器状态（骨架屏 ↔ 内容），带 200ms 过渡。 */
export function setState(el, state) {
  if (!el) return;
  el.dataset.qyState = state;
  el.classList.toggle('qy-loading', state === 'loading');
  el.classList.toggle('qy-ready', state === 'ready');
  el.classList.toggle('qy-empty-state', state === 'empty');
  el.classList.toggle('qy-error-state', state === 'error');
}

/** 初始化：装全局兜底（各页面入口调用一次）。 */
export function initRobustness() {
  installGlobalErrorHandlers();
}
