// 656 C2 · 标签（Web Component）：仅三种语义（ok / warn / bad），不新增装饰性配色
// 用法：<qy-tag kind="ok">一致</qy-tag>
const CSS = `
:host { display: inline-block; }
.tag {
  font-family: var(--font-sans); font-size: 11px;
  /* 671d：全圆角胶囊 → 6px（--radius-pill 已由 999px 收敛为 6px） */
  border-radius: var(--radius-pill, 6px); padding: 1px 7px;
  border: var(--border-width, 1px) solid var(--color-line-strong, #262626);
  color: var(--color-text-dim, #a1a1a1);
}
:host([kind="ok"]) .tag { color: var(--color-pass, #4ade80); border-color: var(--color-pass, #4ade80); }
:host([kind="warn"]) .tag { color: var(--color-pass-exception, #fbbf24); border-color: var(--color-pass-exception, #fbbf24); }
:host([kind="bad"]) .tag { color: var(--color-fail, #f87171); border-color: var(--color-fail, #f87171); }
`;

export class QyTag extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const root = this.attachShadow({ mode: 'open' });
    root.innerHTML = `<style>${CSS}</style><span class="tag"><slot></slot></span>`;
  }
}

if (!customElements.get('qy-tag')) customElements.define('qy-tag', QyTag);
export default QyTag;
