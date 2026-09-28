// 656 C2 · 标签（Web Component）：仅三种语义（ok / warn / bad），不新增装饰性配色
// 用法：<qy-tag kind="ok">一致</qy-tag>
const CSS = `
:host { display: inline-block; }
.tag {
  font-family: var(--font-sans); font-size: 11px;
  border-radius: 999px; padding: 1px 7px;
  border: var(--border-width, 1px) solid var(--color-line-strong, #2a3138);
  color: var(--color-text-dim, #9aa3ab);
}
:host([kind="ok"]) .tag { color: var(--color-pass, #58c6b2); border-color: rgba(88,198,178,.4); }
:host([kind="warn"]) .tag { color: var(--color-pass-exception, #d8a657); border-color: rgba(216,166,87,.4); }
:host([kind="bad"]) .tag { color: var(--color-fail, #d96b6b); border-color: rgba(217,107,107,.45); }
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
