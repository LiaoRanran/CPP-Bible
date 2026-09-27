// web_logic_check_655.mjs — 655 D 前端**纯逻辑真求值**（Node 18 可跑，不依赖 jsdom）
//
// 与 web_smoke_655.mjs 的分工：
//   - 本脚本：把 `web/verify_core.js`（算哈希/匹配台账/判定/CSV 生成）与
//     `web/graph_core.js`（攻防计数/点到线段距离/最近边拾取）在 Node 里**真跑**并断言；
//   - web_smoke_655.mjs：用 jsdom 跑**整页 DOM 交互**（需 Node ≥20 的 jsdom；本机缺则 SKIP）。
// 两者互补：DOM 层可能因环境 SKIP，但**逻辑层在任何有 Node 的机器上都必须真过**。
//
// 运行：node tools/web_logic_check_655.mjs   退出码 0 = 全过，1 = 有断言失败。
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const WEB = path.join(ROOT, 'web');

if (!globalThis.crypto) {
  const { webcrypto } = await import('node:crypto');
  globalThis.crypto = webcrypto;               // Node 18 需要显式注入 WebCrypto
}

const vc = await import(pathToFileURL(path.join(WEB, 'verify_core.js')).href);
const gc = await import(pathToFileURL(path.join(WEB, 'graph_core.js')).href);

const failures = [];
function check(name, cond, extra = '') {
  console.log(`  [${cond ? 'ok' : 'FAIL'}] ${name}${extra ? ' · ' + extra : ''}`);
  if (!cond) failures.push(name);
}

const manifest = JSON.parse(fs.readFileSync(path.join(WEB, 'data', 'manifest.json'), 'utf-8'));
const graph = JSON.parse(fs.readFileSync(path.join(WEB, 'data', 'graph.json'), 'utf-8'));

// ── ① 真算：台账每一条都能被现算复现 ──────────────────────────────────────
console.log('\n[1/4] verify_core · 台账哈希真算复现');
let mismatch = [];
for (const it of manifest.items) {
  const buf = fs.readFileSync(path.join(ROOT, it.path));
  const got = await vc.sha256Hex(buf);
  if (got !== it.sha256) mismatch.push(it.path);
}
check(`台账 ${manifest.items.length} 条现算 sha256 全部一致`, mismatch.length === 0, mismatch.slice(0, 3).join(','));

// ── ② 匹配与判定 ─────────────────────────────────────────────────────────
console.log('\n[2/4] verify_core · 匹配 / 判定 / CSV');
const first = manifest.items[0];
check('按文件名匹配到台账条目', vc.pickExpected(manifest.items, vc.basename(first.path))?.path === first.path);
check('未知文件名 ⇒ null（不猜路径）', vc.pickExpected(manifest.items, 'no-such-file.bin') === null);
check('一致 ⇒ ok', vc.verdictOf({ expected: 'a', ok: true }).key === 'ok');
check('不一致 ⇒ bad', vc.verdictOf({ expected: 'a', ok: false }).key === 'bad');
check('无台账 ⇒ none（不判失败）', vc.verdictOf({ expected: '', ok: false }).key === 'none');

const rows = [
  { name: 'a.md', bytes: 3, actual: 'aa', expected: 'aa', matched_path: 'x/a.md', ok: true, note: '' },
  { name: 'weird,name"x.md', bytes: 5, actual: 'bb', expected: 'cc', matched_path: '', ok: false, note: '含,与"的字段' },
];
const csv = vc.buildCsv(rows);
const lines = csv.split('\r\n');
check('CSV 以 BOM 开头', csv.charCodeAt(0) === 0xfeff);
check('CSV 表头正确', lines[0] === '\ufeff' + vc.CSV_HEADER.join(','));
check('CSV 数据行数 = 2（含末尾空行）', lines.filter((l) => l).length === 3, `lines=${lines.filter((l) => l).length}`);
check('CSV 对含逗号/引号字段加引号并翻倍引号',
  csv.includes('"weird,name""x.md"') && csv.includes('"含,与""的字段"'), lines.find((l) => l.includes('weird')) || '');
check('CSV 判定列用中文三态', csv.includes(',一致,') && csv.includes(',不一致,'));
check('CSV 文件名带时间戳且为 .csv', /^queYi-hash-verify-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\.csv$/
  .test(vc.csvFileName(new Date('2026-09-27T12:34:56Z'))));

// ── ③ 星图统计：与暴力重算逐节点一致 ────────────────────────────────────
console.log('\n[3/4] graph_core · 攻防计数与 graph.json 对账');
let bad = 0;
for (const n of graph.nodes) {
  const got = gc.statsOf(graph.links, n.id);
  const want = { attacks: 0, defends: 0, defeated: 0 };
  for (const l of graph.links) {
    if (l.source !== n.id && l.target !== n.id) continue;
    if (l.kind === 'attack') { want.attacks++; if (l.defeated) want.defeated++; }
    else if (l.kind === 'defend') want.defends++;
  }
  if (got.attacks !== want.attacks || got.defends !== want.defends || got.defeated !== want.defeated) bad++;
}
check(`${graph.nodes.length} 个节点的攻/防/被击败计数与暴力重算一致`, bad === 0, `不一致 ${bad}`);
const sumAtt = graph.nodes.reduce((s, n) => s + gc.statsOf(graph.links, n.id).attacks, 0);
const attackLinks = graph.links.filter((l) => l.kind === 'attack').length;
check('攻击计数总和 = 2 × 攻击边数（每条边被两个端点各记一次）', sumAtt === 2 * attackLinks,
  `${sumAtt} vs ${2 * attackLinks}`);
check('击败边数与 meta 声明一致',
  graph.nodes.reduce((s, n) => s + gc.statsOf(graph.links, n.id).defeated, 0) === 2 * graph.meta.counts.defeated_links);

// ── ④ 几何：点到线段距离 + 最近边拾取 ───────────────────────────────────
console.log('\n[4/4] graph_core · 几何与最近边拾取');
check('线段上的点 ⇒ 距离 0', gc.pointSegDist(5, 0, 0, 0, 10, 0) === 0);
check('垂距 = 3', Math.abs(gc.pointSegDist(5, 3, 0, 0, 10, 0) - 3) < 1e-9);
check('超出端点 ⇒ 夹到端点距离（(20,0)→(10,0) = 10）', Math.abs(gc.pointSegDist(20, 0, 0, 0, 10, 0) - 10) < 1e-9);
check('退化线段（A=B）⇒ 点距', Math.abs(gc.pointSegDist(3, 4, 0, 0, 0, 0) - 5) < 1e-9);

const nodes = [{ id: 'A' }, { id: 'B' }, { id: 'C' }];
const pos = [{ x: 0, y: 0 }, { x: 100, y: 0 }, { x: 0, y: 100 }];
const toScreen = (p) => ({ x: p.x, y: p.y });
const links = [{ source: 'A', target: 'B', kind: 'attack', defeated: false, _ai: 0, _bi: 1 },
               { source: 'A', target: 'C', kind: 'defend', defeated: false, _ai: 0, _bi: 2 }];
const args = { links, nodes, pos, toScreen, visible: () => true, passLink: () => true, maxPx: 7 };
check('靠近 AB 中点 ⇒ 命中第 0 条边', gc.pickEdgeIndex({ ...args, sx: 50, sy: 3 }) === 0);
check('靠近 AC 中线 ⇒ 命中第 1 条边', gc.pickEdgeIndex({ ...args, sx: 3, sy: 50 }) === 1);
check('远离所有边 ⇒ -1', gc.pickEdgeIndex({ ...args, sx: 500, sy: 500 }) === -1);
check('被 passLink 过滤的边不参与拾取',
  gc.pickEdgeIndex({ ...args, sx: 3, sy: 50, passLink: (l) => l.kind !== 'defend' }) === -1);

console.log(`\n[web-logic-655] ${failures.length ? 'FAIL：' + failures.join(' / ') : '全部通过'}`);
process.exit(failures.length ? 1 : 0);
