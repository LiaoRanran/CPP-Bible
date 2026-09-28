// 653 B · 现场验哈希：浏览器 Web Crypto 现场重算 sha256，与台账哈希逐字节比对
// 655 D 深化：① 一次拖入/选择**多个**文件 ⇒ 批量验证结果表；② 结果**导出 CSV**。
//   全程离线（不联网、无后端、不上传文件）；file:// 打开也能用（仅 manifest 需经 fetch，已给内联兜底）
import { fetchJSON, shortHash } from './app.js';
// 655 D：纯逻辑（算哈希/匹配台账/判定/生成 CSV）抽到 verify_core.js ⇒ 可被 Node 真跑验证
import { sha256Hex, pickExpected, verdictOf, buildCsv, csvFileName } from './verify_core.js';
// 656 C2：导航改为 `<qy-nav>` 组件（见 components/qy-nav.js），三个页面同一份实现

const $ = (id) => document.getElementById(id);
let MANIFEST = { items: [], note: '' };
let RESULTS = [];          // [{name, bytes, actual, expected, ok, note}]

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

// ── 655 D：批量验证 ────────────────────────────────────────────────────────
function renderBatch() {
  if (!RESULTS.length) {
    $('batch-tbody').innerHTML = '<tr><td colspan="5" class="muted">未验证</td></tr>';
    $('batch-summary').textContent = '尚未验证';
    $('export').disabled = true; $('clear').disabled = true;
    return;
  }
  $('batch-tbody').innerHTML = RESULTS.map((r) => {
    const v = verdictOf(r);
    return `<tr class="${v.cls}">
      <td class="mono-cell">${r.name}</td>
      <td class="mono-cell">${r.bytes}</td>
      <td class="mono-cell">${shortHash(r.actual)}</td>
      <td class="mono-cell">${r.expected ? (r.matched_path || shortHash(r.expected)) : '—'}</td>
      <td>${v.text}${r.note ? ` <span class="muted">· ${r.note}</span>` : ''}</td>
    </tr>`;
  }).join('');
  const ok = RESULTS.filter((r) => r.ok).length;
  const bad = RESULTS.filter((r) => r.expected && !r.ok).length;
  const none = RESULTS.filter((r) => !r.expected).length;
  $('batch-summary').innerHTML =
    `${RESULTS.length} 个文件 · <b class="ok">一致 ${ok}</b> · <b class="bad">不一致 ${bad}</b>` +
    (none ? ` · <b class="skip">无台账 ${none}</b>` : '');
  $('export').disabled = false; $('clear').disabled = false;
}

/** 单个文件的验证（expected 为空 ⇒ 按文件名匹配台账；多文件批量时忽略手填 expected） */
async function verifyOne(file, manualExpected, multi) {
  const buf = await file.arrayBuffer();
  const actual = await sha256Hex(buf);
  let expected = multi ? '' : (manualExpected || '').trim().toLowerCase();
  let note = '', matched_path = '';
  if (!expected) {
    const hit = pickExpected(MANIFEST.items, file.name);
    if (hit) {
      expected = hit.sha256; matched_path = hit.path;
      note = '按文件名匹配台账';
    } else {
      note = MANIFEST.items.length ? '台账中无同名条目（仅实算值）' : '台账未加载（仅实算值）';
    }
  }
  return { name: file.name, bytes: file.size, actual, expected, matched_path,
           ok: !!expected && actual === expected, note };
}

async function verifyFiles(fileList) {
  const files = [...fileList];
  if (!files.length) return;
  const multi = files.length > 1;
  const manual = $('expected').value;
  const box = $('result');
  if (multi) { box.className = 'result'; box.innerHTML = ''; }
  $('batch-summary').textContent = `正在重算 ${files.length} 个文件的 sha256…`;
  const rows = [];
  for (const f of files) rows.push(await verifyOne(f, manual, multi));
  RESULTS = rows.concat(RESULTS).slice(0, 200);   // 新结果在前，最多保留 200 条
  renderBatch();
  if (!multi) setResult(rows[0]);
}

// ── 655 D：导出 CSV（逻辑在 verify_core.buildCsv，已被 Node 用例真跑覆盖）────
function exportCsv() {
  const csv = buildCsv(RESULTS.slice().reverse());      // 导出时按验证先后顺序
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = csvFileName();
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 2000);
}

// ── 事件接线 ─────────────────────────────────────────────────────────────
$('file').addEventListener('change', (e) => { if (e.target.files.length) verifyFiles(e.target.files); });
const dz = $('drop');
['dragenter', 'dragover'].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.style.borderColor = '#8ab4f8'; }));
['dragleave', 'drop'].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.style.borderColor = ''; }));
dz.addEventListener('drop', (e) => { if (e.dataTransfer.files.length) verifyFiles(e.dataTransfer.files); });
$('expected').addEventListener('input', () => setResult(null));
$('export').addEventListener('click', exportCsv);
$('clear').addEventListener('click', () => { RESULTS = []; renderBatch(); setResult(null); });

(async function main() {
  try {
    MANIFEST = await fetchJSON('data/manifest.json');
  } catch (e) {
    $('tbody').innerHTML = `<tr><td colspan="4" class="muted">加载 data/manifest.json 失败：${e.message}（file:// 下请用本地静态服务器；或直接拖文件做纯前台重算）</td></tr>`;
  }
  renderTable(); renderBatch();
  $('note').textContent = MANIFEST.note || '';
  // 能力自检：Web Crypto 是否可用（file:// 下 subtle 通常可用）
  $('crypto').textContent = (self.crypto && self.crypto.subtle) ? 'Web Crypto 可用' : 'Web Crypto 不可用（需 https 或 localhost）';
  window.__verify_ready = true;   // 供自动化验证探测
})();
