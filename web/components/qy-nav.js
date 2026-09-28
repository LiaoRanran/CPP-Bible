// 656 C2 · 统一导航栏（Web Component）
// 三个页面（landing / starmap / verify）共用同一个实现，避免"每页各写一份导航"导致的漂移。
// 用法：<qy-nav current="starmap.html"></qy-nav>
const LINKS = [
  ['index.html', '总览'],
  ['starmap.html', '星图'],
  ['verify.html', '验哈希'],
  ['card.html', '学一张卡'],
];

const CSS = `
:host { display: block; }
nav {
  display: flex; align-items: center; gap: var(--space-5, 22px);
  padding: 14px var(--space-6, 26px); border-bottom: var(--border-width, 1px) solid var(--color-line, #1e242b);
  position: sticky; top: 0; background: rgba(11,13,16,.92); backdrop-filter: blur(6px);
  z-index: var(--z-nav, 20); font-family: var(--font-sans);
}
.brand { font-weight: 600; letter-spacing: .14em; text-transform: uppercase; font-size: 12px; color: var(--color-text-dim, #9aa3ab); }
a { color: var(--color-text-dim, #9aa3ab); text-decoration: none; font-size: 13px; border: 0; }
a:hover { color: #fff; }
a[aria-current="page"] { color: var(--color-text, #e6e8ea); border-bottom: 1px solid var(--color-accent, #8ab4f8); padding-bottom: 2px; }
.spacer { flex: 1; }
.pill { font-family: var(--font-mono); font-size: 11px; color: var(--color-text-mute, #6b747c);
        border: 1px solid var(--color-line, #1e242b); padding: 2px 8px; border-radius: 999px; }
`;

export class QyNav extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const root = this.attachShadow({ mode: 'open' });
    root.innerHTML = `<style>${CSS}</style>
      <nav>
        <span class="brand">QueYi</span>
        ${LINKS.map(([href, text]) => `<a href="${href}" data-href="${href}">${text}</a>`).join('')}
        <span class="spacer"></span>
        <span class="pill" id="pill">静态站 · 无后端</span>
      </nav>`;
    const cur = this.getAttribute('current') || '';
    root.querySelectorAll('a[data-href]').forEach((a) => {
      if (a.dataset.href === cur) a.setAttribute('aria-current', 'page');
    });
    const badge = this.getAttribute('badge');
    if (badge) root.getElementById('pill').textContent = badge;
  }
}

if (!customElements.get('qy-nav')) customElements.define('qy-nav', QyNav);
export default QyNav;
