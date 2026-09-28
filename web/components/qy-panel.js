// 656 C2 · 数据面板（Web Component）：大数字 + 说明，用于"系统现状 / 学习进度"这类指标
// 用法：<qy-panel caption="知识卡" num="37" sub="另有 10 张草稿"></qy-panel>
const CSS = `
:host { display: block; }
.cell {
  background: var(--color-surface, #101317);
  border: var(--border-width, 1px) solid var(--color-line, #1e242b);
  border-radius: var(--radius-lg, 10px);
  padding: var(--space-4, 16px);
  font-family: var(--font-sans);
}
.num { font-family: var(--font-mono); font-size: 30px; line-height: 1.1; color: var(--color-text, #e6e8ea); }
.num .unit { font-size: 14px; color: var(--color-text-mute, #6b747c); margin-left: var(--space-1, 4px); }
.cap { font-size: 12px; color: var(--color-text-mute, #6b747c); text-transform: uppercase;
       letter-spacing: .08em; margin-top: var(--space-2, 6px); }
.sub { font-size: 12px; color: var(--color-text-dim, #9aa3ab); margin-top: var(--space-2, 6px); }
:host([warn]) .cell { border-color: rgba(216,166,87,.45); }
:host([bad]) .cell { border-color: rgba(217,107,107,.45); }
`;

export class QyPanel extends HTMLElement {
  static get observedAttributes() { return ['num', 'unit', 'caption', 'sub']; }

  connectedCallback() {
    if (!this.shadowRoot) {
      const root = this.attachShadow({ mode: 'open' });
      root.innerHTML = `<style>${CSS}</style>
        <div class="cell">
          <div class="num" id="num"><span class="unit" id="unit"></span></div>
          <div class="cap" id="cap"></div>
          <div class="sub" id="sub"></div>
          <slot></slot>
        </div>`;
    }
    this.render();
  }

  attributeChangedCallback() { this.render(); }

  render() {
    const root = this.shadowRoot;
    if (!root) return;
    const set = (id, attr) => {
      const v = this.getAttribute(attr) || '';
      root.getElementById(id).textContent = v;
    };
    set('unit', 'unit'); set('cap', 'caption'); set('sub', 'sub');
    this.setNum(this.getAttribute('num') || '');
  }

  /** 供 JS 更新数字（如滚动动画）。 */
  setNum(text) {
    const root = this.shadowRoot;
    if (!root) return;
    const unit = root.getElementById('unit');
    root.getElementById('num').textContent = '';
    root.getElementById('num').appendChild(document.createTextNode(text));
    if (unit) root.getElementById('num').appendChild(unit);
  }
}

if (!customElements.get('qy-panel')) customElements.define('qy-panel', QyPanel);
export default QyPanel;
