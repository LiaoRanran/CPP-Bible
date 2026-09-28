// 656 C2 · 按钮（Web Component）：外观统一 / 键盘可达 / 可当链接用
// 用法：<qy-button href="starmap.html">打开星图</qy-button> 或 <qy-button id="x">导出</qy-button>
const CSS = `
:host { display: inline-block; }
button, a.btn {
  font: inherit; font-size: 13px; font-family: var(--font-sans);
  color: var(--color-text, #e6e8ea); background: var(--color-surface-2, #14181d);
  border: var(--border-width, 1px) solid var(--color-line-strong, #2a3138);
  border-radius: var(--radius-md, 7px); padding: 7px 13px; cursor: pointer;
  text-decoration: none; display: inline-block;
}
button:hover, a.btn:hover { border-color: var(--color-accent, #8ab4f8); }
button:focus-visible, a.btn:focus-visible { outline: 2px solid var(--color-accent, #8ab4f8); outline-offset: 2px; }
button:disabled { opacity: .45; cursor: not-allowed; }
:host([variant="primary"]) button, :host([variant="primary"]) a.btn {
  border-color: var(--color-accent, #8ab4f8); color: #fff;
}
`;

export class QyButton extends HTMLElement {
  static get observedAttributes() { return ['label', 'href', 'variant', 'disabled']; }
  connectedCallback() {
    if (this.shadowRoot) return;
    const root = this.attachShadow({ mode: 'open' });
    const href = this.getAttribute('href');
    const label = this.getAttribute('label') || '';
    root.innerHTML = `<style>${CSS}</style>
      ${href ? `<a class="btn" href="${href}"><span class="lbl">${label}</span><slot></slot></a>`
             : `<button type="button"><span class="lbl">${label}</span><slot></slot></button>`}`;
    if (!href) {
      root.querySelector('button').addEventListener('click', () => {
        this.dispatchEvent(new CustomEvent('qy-click', { bubbles: true }));
      });
    }
    const disabled = this.hasAttribute('disabled');
    const el = root.querySelector(href ? 'a.btn' : 'button');
    if (disabled && !href) el.disabled = true;
  }
  // 660 B4-3：label 属性变化后实时反映（修复 index.html 动态设 label 不生效）
  attributeChangedCallback(name, _old, val) {
    if (!this.shadowRoot) return;
    if (name === 'label') {
      const el = this.shadowRoot.querySelector('.lbl');
      if (el) el.textContent = val || '';
    }
  }
}

if (!customElements.get('qy-button')) customElements.define('qy-button', QyButton);
export default QyButton;
