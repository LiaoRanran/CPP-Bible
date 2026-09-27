// 653 B · 现场验哈希：浏览器 Web Crypto 现场重算 sha256，与台账哈希逐字节比对
//   全程离线（不联网、无后端、不上传文件）；file:// 打开也能用（仅 manifest 需经 fetch，已给内联兜底）
import { fetchJSON, shortHash, mountNav } from './app.js';

mountNav('verify.html');

const $ = (id) => document.getElementById(id);
let MANIFEST = { items: [], note: '' };

async function sha256Hex(buf) {
  const d = await crypto.subtle.digest('SHA-256', buf);
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

function basename(p) { return p.split('/').pop(); }

function renderTable() {
  const rows = MANIFEST.items.map((it, i) => `
    <tr id="row-${i}">
      <td class="mono-cell">${it.path}</td>
      <td class="mono-cell">${it.bytes}</td>
      <td class="mono-cell">${shortHash(it.sha256)}</td>
      <td><button data-i="${i}" class="pick">用这个比对</button></td>
    </tr>`).join('');
  $('tbody').innerHTML = rows || '<tr><td colspan="4" class="muted">manifest 为空</td></tr>';
  document.querySelectorAll('button.pick').forEach((b) => b.addEventListener('click', () => {
    const it = MANIFEST.items[Number(b.dataset.i)];
    $('expected').value = it.sha256;
    $('expect-name').textContent = it.path;
    setResult(null);
  }));
}

function setResult(res) {
  const box = $('result');
  if (!res) { box.className = 'result'; box.innerHTML = ''; return; }
  box.className = `result show ${res.ok ? 'ok' : 'bad'}`;
  box.innerHTML = `<div class="verdict">${res.ok ? '✓ 一致' : '✗ 不一致'}</div>
    <div class="hash">文件：${res.name}（${res.bytes} 字节）</div>
    <div class="hash">实算 sha256：${res.actual}</div>
    <div class="hash">台账 sha256：${res.expected || '（未指定）'}</div>
    ${res.note ? `<div class="hash">注：${res.note}</div>` : ''}`;
}

async function verifyFile(file) {
  const buf = await file.arrayBuffer();
  const actual = await sha256Hex(buf);
  let expected = $('expected').value.trim().toLowerCase();
  let note = '';
  if (!expected) {
    const hit = MANIFEST.items.find((it) => basename(it.path) === file.name);
    if (hit) { expected = hit.sha256; note = `按文件名在台账中匹配到 ${hit.path}`; }
    else { note = '台账中无同名条目（仅展示实算值）'; }
  }
  setResult({ ok: !!expected && actual === expected, name: file.name, bytes: file.size, actual, expected, note });
}

// ── 事件接线 ─────────────────────────────────────────────────────────────
$('file').addEventListener('change', (e) => { if (e.target.files[0]) verifyFile(e.target.files[0]); });
const dz = $('drop');
['dragenter', 'dragover'].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.style.borderColor = '#8ab4f8'; }));
['dragleave', 'drop'].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.style.borderColor = ''; }));
dz.addEventListener('drop', (e) => { const f = e.dataTransfer.files[0]; if (f) verifyFile(f); });
$('expected').addEventListener('input', () => setResult(null));

(async function main() {
  try {
    MANIFEST = await fetchJSON('data/manifest.json');
  } catch (e) {
    $('tbody').innerHTML = `<tr><td colspan="4" class="muted">加载 data/manifest.json 失败：${e.message}（file:// 下请用本地静态服务器；或直接拖文件做纯前台重算）</td></tr>`;
  }
  renderTable();
  $('note').textContent = MANIFEST.note || '';
  // 能力自检：Web Crypto 是否可用（file:// 下 subtle 通常可用）
  $('crypto').textContent = (self.crypto && self.crypto.subtle) ? 'Web Crypto 可用' : 'Web Crypto 不可用（需 https 或 localhost）';
})();
