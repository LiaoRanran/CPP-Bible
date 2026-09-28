// 655 D · 验哈希的**纯逻辑核心**（无 DOM 依赖 ⇒ 可在 Node 里真跑，见 tools/web_logic_check_655.mjs）
//   浏览器侧由 verify.js 调用；把"算哈希 / 匹配台账 / 判定 / 生成 CSV"从 DOM 里剥出来，
//   是为了让这几步能被自动化用例**真求值**，而不是只做语法检查。

/**
 * 取可用的 `WebCrypto.subtle`（657 E/F 加固）。
 *
 * 为什么不直接写裸 `crypto`：① 裸 `crypto` 依赖「全局恰好有 WebCrypto」，在
 * jsdom / 非 https 页面里可能是 undefined 或没有 `subtle` ⇒ 报错信息是
 * 「reading 'subtle' of undefined」，人看不懂是环境问题；② Node 里跑测试时
 * 全局可能被 harness 指到 jsdom 的 `window.crypto`（没有 `subtle`）。
 * 顺序：`self.crypto`（浏览器经典脚本里 self===window）→ `globalThis.crypto`
 * （Node 18+ 的 webcrypto）→ 都没有就**抛一句人能看懂的话**。
 */
function _subtle() {
  const c = (typeof self !== 'undefined' && self && self.crypto) || globalThis.crypto;
  if (c && c.subtle) return c.subtle;
  throw new Error('WebCrypto.subtle 不可用：需要 https 或 localhost（Node 18+ 也可）');
}

/** 现算 sha256（十六进制）。需要 `crypto.subtle`（浏览器或 Node 的 webcrypto）。 */
export async function sha256Hex(buf) {
  const d = await _subtle().digest('SHA-256', buf);
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export function basename(p) { return String(p).split('/').pop(); }

/** 按文件名在台账里找条目；找不到 ⇒ null（**不猜**路径）。 */
export function pickExpected(items, fileName) {
  return (items || []).find((it) => basename(it.path) === fileName) || null;
}

/** 结论三态：一致 / 不一致 / 无台账（expected 为空时**不判失败**）。 */
export function verdictOf(r) {
  if (!r || !r.expected) return { key: 'none', text: '无台账（仅实算）', cls: '' };
  return r.ok ? { key: 'ok', text: '一致', cls: 'ok' } : { key: 'bad', text: '不一致', cls: 'bad' };
}

/** RFC4180 字段转义（含逗号/引号/换行 ⇒ 加引号并把引号翻倍）。 */
export function csvCell(v) {
  const s = v == null ? '' : String(v);
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

export const CSV_HEADER = ['文件名', '字节', '实算 sha256', '台账 sha256', '台账路径', '结论', '备注'];

/** 结果表 → CSV 文本（Excel 友好：前置 BOM、CRLF 行尾）。 */
export function buildCsv(results) {
  const lines = [CSV_HEADER.join(',')];
  for (const r of results || []) {
    lines.push([r.name, r.bytes, r.actual, r.expected || '', r.matched_path || '',
                verdictOf(r).text, r.note || ''].map(csvCell).join(','));
  }
  return '\ufeff' + lines.join('\r\n') + '\r\n';
}

/** CSV 文件名：带时间戳，避免覆盖（本地时间，秒级）。 */
export function csvFileName(now = new Date()) {
  return `queYi-hash-verify-${now.toISOString().slice(0, 19).replace(/[:T]/g, '-')}.csv`;
}
