// 666 B1/B7 · 统一导航栏（Web Component）
// ① 五页共用同一实现（landing / cards / card / starmap / verify），避免"每页各写一份导航"；
// ② 无障碍：`<nav aria-label>` + `aria-current="page"` + 键盘可达 + 焦点环（token 提供）；
// ③ 主题切换：显式按钮（不强迫用户跟随系统），状态存 localStorage，键名 `qy-theme`。
// 用法：<qy-nav current="cards.html"></qy-nav>
const LINKS = [
  ['index.html', '总览'],
  ['cards.html', '卡库'],
  ['card.html', '学一张卡'],
  ['learn.html', '学习'],
  ['starmap.html', '星图'],
  ['experiments.html', '实验'],
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

/* 671d：① 删掉 backdrop-filter（毛玻璃）——对比度不可算，且是模板感的主要来源；
 *       ② 当前页不再给"背景块 + 内阴影"，改为**强调色文字 + 2px 下划线**（更像文档站）；
 *       ③ 兜底色改为中性灰阶（原来是暖中性 #2f2f2c / #e8e6e3）。 */
const CSS = `
:host { display: block; }
nav {
  display: flex; align-items: center; gap: var(--space-3, 24px);
  padding: 12px var(--space-3, 24px);
  border-bottom: var(--border-width, 1px) solid var(--color-line, #262626);
  position: sticky; top: 0; background: var(--color-bg, #0a0a0a);
  z-index: var(--z-nav, 20); font-family: var(--font-sans);
}
.brand { font-weight: 600; font-size: 15px; color: var(--color-text, #ededed);
         letter-spacing: -.015em; white-space: nowrap; }
a {
  color: var(--color-text-dim, #a1a1a1); text-decoration: none; font-size: 13px;
  padding: var(--space-1, 8px) 2px; border-radius: 0;
  border-bottom: 2px solid transparent; white-space: nowrap;
}
a:hover { color: var(--color-text, #ededed); text-decoration: none; background: none; }
a:focus-visible { outline: var(--focus-ring, 2px solid #5b8def); outline-offset: 2px; }
a[aria-current="page"] {
  color: var(--color-accent, #5b8def); background: none;
  border-bottom-color: var(--color-accent, #5b8def); box-shadow: none;
}
.spacer { flex: 1; }
/* 671d：状态胶囊 → 一行淡色说明文字（去掉边框/底，减少一个装饰层） */
.pill { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-faint, #666666);
        white-space: nowrap; }
button { font: inherit; font-size: 12px; color: var(--color-text-dim, #a1a1a1);
         background: transparent; border: 1px solid var(--color-line, #262626);
         border-radius: var(--radius-md, 6px); padding: 5px 10px; cursor: pointer; }
button:hover { color: var(--color-text, #ededed); border-color: var(--color-accent, #5b8def); }
button:focus-visible { outline: var(--focus-ring, 2px solid #5b8def); outline-offset: 2px; }
/* 673b B2：断点统一 —— 原 900px 是全站唯一非标值（672c 定的档位是 480/640/768/1024/1280），
   导航折叠与 669c.css / responsive.css / style.css 的 768px 对齐。 */
@media (max-width: 768px) {
  nav { gap: 12px; flex-wrap: wrap; padding-inline: 16px; }
  a { min-height: var(--touch-min, 44px); display: inline-flex; align-items: center; }
}
`;

export class QyNav extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const root = this.attachShadow({ mode: 'open' });
    root.innerHTML = `<style>${CSS}</style>
      <nav aria-label="主导航">
        <span class="brand">阙疑 QueYi</span>
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
