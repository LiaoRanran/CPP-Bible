// 656 C2 · 卡片（Web Component）：标题 + 正文槽位
// 用法：<qy-card title="星图"><p>正文</p></qy-card>
const CSS = `
:host { display: block; }
.card {
  background: var(--color-surface, #101317);
  border: var(--border-width, 1px) solid var(--color-line, #1e242b);
  border-radius: var(--radius-lg, 10px);
  padding: var(--space-4, 18px);
  font-family: var(--font-sans);
}
h2 { font-size: 20px; font-weight: 600; margin: 0 0 6px; color: var(--color-text, #e6e8ea); }
p { margin: 0; font-size: 14px; color: var(--color-text-dim, #9aa3ab); }
:host([tight]) .card { padding: var(--space-3, 12px); }
`;

export class QyCard extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const root = this.attachShadow({ mode: 'open' });
    const title = this.getAttribute('title') || '';
    root.innerHTML = `<style>${CSS}</style>
      <div class="card">${title ? `<h2>${title}</h2>` : ''}<slot></slot></div>`;
  }
}

if (!customElements.get('qy-card')) customElements.define('qy-card', QyCard);
export default QyCard;
