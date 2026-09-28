// 656 C2 · 四态状态指示器（Web Component）：色点 + 中文态名，与判决四态一一对应
// 用法：<qy-status state="pass_with_exception"></qy-status>
const LABELS = {
  pass: 'pass',
  pass_with_exception: 'pass_with_exception',
  fail: 'fail',
  unknown: 'unknown',
};
const CSS = `
:host { display: inline-flex; align-items: center; gap: 6px; }
.dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
.text { font-family: var(--font-mono); font-size: 12px; color: var(--color-text, #e6e8ea); }
:host([state="pass"]) .dot { background: var(--color-pass, #58c6b2); }
:host([state="pass_with_exception"]) .dot { background: var(--color-pass-exception, #d8a657); }
:host([state="fail"]) .dot { background: var(--color-fail, #d96b6b); }
:host([state="unknown"]) .dot { background: var(--color-unknown, #7a838c); }
`;

export class QyStatus extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const root = this.attachShadow({ mode: 'open' });
    const st = this.getAttribute('state') || 'unknown';
    root.innerHTML = `<style>${CSS}</style>
      <span class="dot"></span><span class="text">${LABELS[st] || st}</span>`;
    this.setAttribute('title', `判决四态：${LABELS[st] || st}`);
  }
}

if (!customElements.get('qy-status')) customElements.define('qy-status', QyStatus);
export default QyStatus;
