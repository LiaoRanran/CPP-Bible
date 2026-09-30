// 670c4 · 可访问性 DOM 层：全局快捷键 + 帮助弹窗 + 焦点陷阱 + aria-live 播报
// 纯逻辑在 a11y_core.js；本文件只碰 DOM。
import {
  NAV_MAP, HELP_ITEMS, normalizeKey, isTypingTarget, resolveChord, cycleIndex,
  announceResults, announceRating, shouldCloseOnEsc,
} from './a11y_core.js';

export { announceResults, announceRating, normalizeKey, resolveChord, cycleIndex };

const LIVE_ID = 'qy-live';

/** 惰性创建 aria-live 播报区。 */
export function ensureLive() {
  if (typeof document === 'undefined') return null;
  let el = document.getElementById(LIVE_ID);
  if (el) return el;
  el = document.createElement('div');
  el.id = LIVE_ID;
  el.className = 'qy-sr-only';
  el.setAttribute('aria-live', 'polite');
  el.setAttribute('aria-atomic', 'true');
  (document.body || document.documentElement).appendChild(el);
  return el;
}

/** 向屏幕阅读器播报。 */
export function announce(msg) {
  const el = ensureLive();
  if (el) el.textContent = msg;
}

/* ── 帮助弹窗（role=dialog + 焦点陷阱）── */
let dialogEl = null, lastFocus = null;

export function buildHelpDialog() {
  const d = document.createElement('div');
  d.className = 'qy-dialog';
  d.setAttribute('role', 'dialog');
  d.setAttribute('aria-modal', 'true');
  d.setAttribute('aria-labelledby', 'qy-help-title');
  const rows = HELP_ITEMS.map((i) =>
    `<tr><th scope="row"><kbd>${i.keys.join('</kbd> <kbd>')}</kbd></th><td>${i.desc}</td></tr>`).join('');
  d.innerHTML = `<div class="qy-dialog-box">
    <h2 id="qy-help-title">键盘快捷键</h2>
    <table class="qy-help-table"><tbody>${rows}</tbody></table>
    <button type="button" class="qy-btn" data-close>关闭（Esc）</button></div>`;
  d.hidden = true;
  d.querySelector('[data-close]').addEventListener('click', closeDialog);
  d.addEventListener('keydown', trapTab);
  document.body.appendChild(d);
  return d;
}

function focusables(root) {
  return Array.from(root.querySelectorAll(
    'a[href],button:not([disabled]),input:not([disabled]),select,textarea,[tabindex]:not([tabindex="-1"])'
  )).filter((e) => e.offsetParent !== null || e === document.activeElement);
}

function trapTab(ev) {
  if (ev.key !== 'Tab' || !dialogEl) return;
  const f = focusables(dialogEl);
  if (!f.length) return;
  const idx = f.indexOf(document.activeElement);
  ev.preventDefault();
  const next = cycleIndex(idx < 0 ? -1 : idx, f.length, ev.shiftKey);
  f[next].focus();
}

export function openDialog() {
  if (!dialogEl) dialogEl = buildHelpDialog();
  lastFocus = document.activeElement;
  dialogEl.hidden = false;
  const f = focusables(dialogEl);
  (f[0] || dialogEl).focus();
  announce('已打开键盘快捷键帮助');
}

export function closeDialog() {
  if (dialogEl) dialogEl.hidden = true;
  if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();  // 焦点回到触发元素
}

export function isDialogOpen() {
  return Boolean(dialogEl && !dialogEl.hidden);
}

/* ── 全局快捷键 ── */
export function installShortcuts() {
  if (typeof window === 'undefined' || window.__qyA11yInstalled) return;
  window.__qyA11yInstalled = true;
  let pending = null;
  window.addEventListener('keydown', (ev) => {
    const key = normalizeKey(ev);
    if (key === null) return;
    if (shouldCloseOnEsc(isDialogOpen()) && key === 'Escape') { ev.preventDefault(); closeDialog(); return; }
    if (isTypingTarget(ev.target && ev.target.tagName, ev.target && ev.target.isContentEditable)) {
      if (key !== 'Escape') return;
    }
    if (key === '?') { ev.preventDefault(); openDialog(); return; }
    const r = resolveChord(pending, key);
    pending = r.pending;
    if (r.nav) { ev.preventDefault(); window.location.href = r.nav; }
  });
}

/** 页面入口调用一次。 */
export function initA11y() {
  ensureLive();
  installShortcuts();
}
