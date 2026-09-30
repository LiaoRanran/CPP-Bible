// 670c5 · 页面内键位接线（卡库等）：`/` 聚焦搜索、j/k 卡片间移动、Enter 打开
// 纯逻辑复用 a11y_core（normalizeKey / isTypingTarget / cycleIndex）；本文件只碰 DOM。
import { normalizeKey, isTypingTarget, cycleIndex } from './a11y_core.js';

export const CARD_SELECTOR = '#grid .card-item a[href], #grid .card-item button, #grid .card-item [tabindex]';

/** 收集可导航的卡片元素（纯函数：传入 root）。 */
export function collectItems(root) {
  if (!root || !root.querySelectorAll) return [];
  return Array.from(root.querySelectorAll(CARD_SELECTOR));
}

/** 计算下一个应聚焦的索引（包裹式）。 */
export function navIndex(current, len, dir) {
  if (len <= 0) return -1;
  if (current < 0) return dir > 0 ? 0 : len - 1;
  return cycleIndex(current, len, dir < 0);
}

export function installKeybinds() {
  if (typeof window === 'undefined' || window.__qyKeybindInstalled) return;
  window.__qyKeybindInstalled = true;
  window.addEventListener('keydown', (ev) => {
    const key = normalizeKey(ev);
    if (key === null) return;
    const t = ev.target;
    const typing = isTypingTarget(t && t.tagName, t && t.isContentEditable);

    // `/` → 聚焦搜索框（不在输入态时）
    if (key === '/' && !typing) {
      const q = document.getElementById('q');
      if (q) { ev.preventDefault(); q.focus(); if (q.select) q.select(); }
      return;
    }
    if (typing) return;

    // j / k → 卡片间移动焦点
    if (key === 'j' || key === 'k') {
      const items = collectItems(document);
      if (!items.length) return;
      ev.preventDefault();
      const idx = navIndex(items.indexOf(document.activeElement), items.length, key === 'j' ? 1 : -1);
      items[idx].focus();
      return;
    }

    // Enter → 打开当前聚焦卡片
    if (key === 'Enter') {
      const item = document.activeElement && document.activeElement.closest
        ? document.activeElement.closest('.card-item') : null;
      if (item) {
        const link = item.querySelector('a[href*="card.html"]');
        if (link && document.activeElement !== link) { ev.preventDefault(); link.click(); }
      }
    }
  });
}

export function initKeybinds() { installKeybinds(); }
