// 666 B1/B7 · 统一导航栏（Web Component）
// ① 五页共用同一实现（landing / cards / card / starmap / verify），避免"每页各写一份导航"；
// ② 无障碍：`<nav aria-label>` + `aria-current="page"` + 键盘可达 + 焦点环（token 提供）；
// ③ 主题切换：显式按钮（不强迫用户跟随系统），状态存 localStorage，键名 `qy-theme`。
// 用法：<qy-nav current="cards.html"></qy-nav>
const LINKS = [
  ['index.html', '总览'],
  ['cards.html', '卡库'],
  ['card.html', '学一张卡'],
  ['starmap.html', '星图'],
  ['verdicts.html', '判决与数字'],
  ['verify.html', '验哈希'],
];

const THEME_KEY = 'qy-theme';

/** 读取/应用主题（可被页脚按钮与顶栏按钮共用）。 */
export function applyTheme() {
  try {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === 'light' || saved === 'dark') {
      document.documentElement.dataset.theme = saved;
    }
  } catch { /* 隐私模式：忽略 */ }
}

export function toggleTheme() {
  const cur = document.documentElement.dataset.theme
    || (matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
  const next = cur === 'light' ? 'dark' : 'light';
  document.documentElement.dataset.theme = next;
  try { localStorage.setItem(THEME_KEY, next); } catch { /* 同上 */ }
  return next;
}

applyTheme();   // 尽早应用，减少首屏闪烁

const CSS = `
:host { display: block; }
nav {
  display: flex; align-items: center; gap: var(--space-3, 24px);
  padding: var(--space-2, 16px) var(--space-3, 24px);
  border-bottom: var(--border-width, 1px) solid var(--color-line, #2f2f2c);
  position: sticky; top: 0; background: var(--color-overlay, rgba(12,12,12,.72));
  backdrop-filter: blur(8px); z-index: var(--z-nav, 20); font-family: var(--font-sans);
}
.brand { font-weight: 600; font-size: 15px; color: var(--color-text, #e8e6e3); }
a {
  color: var(--color-text-dim, #b3aea7); text-decoration: none; font-size: 14px;
  padding: var(--space-1, 8px) 10px; border-radius: var(--radius-md, 8px);
}
a:hover { color: var(--color-text, #e8e6e3); background: var(--color-surface-2, #262625); }
a:focus-visible { outline: var(--focus-ring, 2px solid #d97757); outline-offset: 2px; }
a[aria-current="page"] {
  color: var(--color-text, #e8e6e3); background: var(--color-accent-soft, rgba(217,119,87,.16));
  box-shadow: inset 0 -2px 0 var(--color-accent, #d97757);
}
.spacer { flex: 1; }
.pill { font-family: var(--font-mono); font-size: 11px; color: var(--color-text-mute, #979089);
        border: 1px solid var(--color-line, #2f2f2c); padding: 2px 8px; border-radius: 999px; }
button { font: inherit; font-size: 12px; color: var(--color-text-dim, #b3aea7);
         background: transparent; border: 1px solid var(--color-line-strong, #3d3d3a);
         border-radius: var(--radius-md, 8px); padding: 5px 10px; cursor: pointer; }
button:hover { color: var(--color-text, #e8e6e3); border-color: var(--color-accent, #d97757); }
button:focus-visible { outline: var(--focus-ring, 2px solid #d97757); outline-offset: 2px; }
`;

export class QyNav extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const root = this.attachShadow({ mode: 'open' });
    root.innerHTML = `<style>${CSS}</style>
      <nav aria-label="主导航">
        <span class="brand">祈易 QueYi</span>
        ${LINKS.map(([href, text]) => `<a href="${href}" data-href="${href}">${text}</a>`).join('')}
        <span class="spacer"></span>
        <span class="pill" id="pill">静态站 · 无后端</span>
        <button id="theme" type="button" aria-label="切换深色/浅色主题">主题</button>
      </nav>`;
    const cur = this.getAttribute('current') || '';
    root.querySelectorAll('a[data-href]').forEach((a) => {
      if (a.dataset.href === cur) a.setAttribute('aria-current', 'page');
    });
    const badge = this.getAttribute('badge');
    if (badge) root.getElementById('pill').textContent = badge;
    root.getElementById('theme').addEventListener('click', () => {
      const next = toggleTheme();
      root.getElementById('theme').setAttribute(
        'aria-label', next === 'light' ? '切换到深色主题' : '切换到浅色主题');
    });
  }
}

if (!customElements.get('qy-nav')) customElements.define('qy-nav', QyNav);
export default QyNav;
