// web_smoke_655.mjs — 655 D **真实求值**前端冒烟（jsdom 里跑真页面代码，不是静态 grep）
//
// 为什么需要它：653 交付静态站时，只能用 `node --check`（语法）+ 静态服务 200 冒烟；
//   654 想做真浏览器检查被 Node 版本与执行授权挡住。本脚本用 jsdom **在 Node 里真跑**
//   `web/*.js` 与 `index.html` 的内联模块，断言"渲染出来的是**真实数据**、交互**真能工作**"：
//     ① verify：拖入 2 个文件（1 个与台账一致 + 1 个被篡改）⇒ 批量表判定正确 + CSV 导出内容正确；
//     ② starmap：节点/边数与台账一致；`__starmap_hooks.select(i)` ⇒ 详情面板出现 id/四态/credibility/攻防计数；
//     ③ index：系统现状面板 37 卡 / 67 规则 / 9 保护器 / 0.0711% 与 `web/data/status.json` 一致。
//
// 运行：
//   node tools/web_smoke_655.mjs            # 缺 jsdom ⇒ 打印 SKIP 并 exit 0（诚实降级，不假绿）
//   WEB_SMOKE_NODE_MODULES=<dir> node tools/web_smoke_655.mjs
// 退出码：0 = 通过或 SKIP；1 = 断言失败。
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';
import { createRequire } from 'module';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const WEB = path.join(ROOT, 'web');

// jsdom 装在受管 node workspace（与 tools/mermaid_parse_check.mjs 同源）
const MODULES = process.env.WEB_SMOKE_NODE_MODULES
  || process.env.MERMAID_NODE_MODULES
  || 'C:/Users/ASUS/.workbuddy/binaries/node/workspace/node_modules';

let JSDOM;
try {
  const req = createRequire(pathToFileURL(path.join(MODULES, 'anchor.js')));
  ({ JSDOM } = await import(pathToFileURL(req.resolve('jsdom'))));
} catch (e) {
  console.log(`[web-smoke-655] SKIP：找不到 jsdom（${MODULES}）——${String(e).slice(0, 120)}`);
  process.exit(0);
}

const failures = [];
function check(name, cond, extra = '') {
  console.log(`  [${cond ? 'ok' : 'FAIL'}] ${name}${extra ? ' · ' + extra : ''}`);
  if (!cond) failures.push(name);
}

function fakeCtx() {
  return new Proxy({}, {
    get: (t, k) => (k in t ? t[k] : (t[k] = () => undefined)),
    set: (t, k, v) => { t[k] = v; return true; },
  });
}

async function mkDom(htmlFile) {
  const html = fs.readFileSync(path.join(WEB, htmlFile), 'utf-8');
  const dom = new JSDOM(html, { url: 'http://localhost/', pretendToBeVisual: true });
  const w = dom.window;
  w.HTMLCanvasElement.prototype.getContext = () => fakeCtx();
  w.matchMedia = () => ({ matches: true, addEventListener() {}, removeEventListener() {} });  // 关动画 ⇒ 数字立即落位
  if (!w.crypto) w.crypto = globalThis.crypto;
  w.fetch = async (url) => {
    const p = path.join(WEB, String(url));
    if (!fs.existsSync(p)) throw new Error(`stub 404: ${url}`);
    return { ok: true, status: 200, json: async () => JSON.parse(fs.readFileSync(p, 'utf-8')) };
  };
  global.window = w; global.document = w.document; global.navigator = w.navigator;
  global.fetch = w.fetch; global.crypto = w.crypto;
  return dom;
}

async function waitFor(fn, ms = 5000, step = 50) {
  const t0 = Date.now();
  for (;;) {
    try { if (fn()) return true; } catch { /* 继续等 */ }
    if (Date.now() - t0 > ms) return false;
    await new Promise((r) => setTimeout(r, step));
  }
}

const $$ = (d, sel) => Array.from(d.querySelectorAll(sel));
const manifest = JSON.parse(fs.readFileSync(path.join(WEB, 'data', 'manifest.json'), 'utf-8'));
const status = JSON.parse(fs.readFileSync(path.join(WEB, 'data', 'status.json'), 'utf-8'));

// ── ① verify.html：批量验证 + CSV 导出 ─────────────────────────────────────
{
  console.log('\n[1/3] web/verify.html —— 批量验哈希 + CSV 导出');
  const dom = await mkDom('verify.html');
  const { window: w } = dom;
  const item = manifest.items[0];
  const goodBytes = fs.readFileSync(path.join(ROOT, item.path));
  const badBytes = Buffer.from('tampered-on-purpose');
  const mk = (name, buf) => ({ name, size: buf.length, arrayBuffer: async () => buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.length) });
  const drop = w.document.getElementById('drop');
  await import(pathToFileURL(path.join(WEB, 'verify.js')).href);
  await waitFor(() => w.document.getElementById('tbody').textContent.includes(item.path));

  const ev = new w.Event('drop', { bubbles: true });
  ev.dataTransfer = { files: [mk(path.basename(item.path), goodBytes), mk('tampered.bin', badBytes)] };
  drop.dispatchEvent(ev);
  await waitFor(() => w.document.getElementById('batch-summary').textContent.includes('不一致'));

  const rows = $$(w.document, '#batch-tbody tr');
  const summary = w.document.getElementById('batch-summary').textContent;
  check('批量表出现 2 行', rows.length === 2, `rows=${rows.length}`);
  check('主结论：1 一致 / 1 不一致', /一致 1/.test(summary) && /不一致 1/.test(summary), summary.trim());
  check('一致行命中台账路径', rows.some((r) => r.textContent.includes(item.path.split('/').pop())));
  check('导出按钮已启用', w.document.getElementById('export').disabled === false);

  let blob = null;
  w.URL.createObjectURL = (b) => { blob = b; return 'blob:stub'; };
  w.URL.revokeObjectURL = () => {};
  w.document.getElementById('export').click();
  const csv = blob ? await blob.text() : '';
  check('CSV 有表头', csv.startsWith('\ufeff文件名,字节,实算 sha256'), csv.slice(0, 40));
  check('CSV 含两条数据行', csv.trim().split('\r\n').length === 3, `lines=${csv.trim().split('\r\n').length}`);
  check('CSV 判定列正确', csv.includes('一致') && csv.includes('不一致'));
  check('CSV 实算哈希 = 台账哈希（真算）', csv.includes(item.sha256), item.sha256.slice(0, 16));
  dom.window.close();
}

// ── ② starmap.html：节点/边数 + 详情面板 ──────────────────────────────────
{
  console.log('\n[2/3] web/starmap.html —— 星图详情面板（655 D 新增）');
  const dom = await mkDom('starmap.html');
  const { window: w } = dom;
  await import(pathToFileURL(path.join(WEB, 'starmap.js')).href);
  const ok = await waitFor(() => w.__starmap_hooks && w.__starmap_hooks.nodeCount() > 0);
  check('星图数据加载（hooks 就绪）', ok);
  if (ok) {
    const graph = JSON.parse(fs.readFileSync(path.join(WEB, 'data', 'graph.json'), 'utf-8'));
    check('节点数与 graph.json 一致',
      w.__starmap_hooks.nodeCount() === graph.nodes.length,
      `${w.__starmap_hooks.nodeCount()} vs ${graph.nodes.length}`);
    check('边数与 graph.json 一致', w.__starmap_hooks.linkCount() === graph.links.length);
    check('首屏描述已现算（含真实节点数）',
      w.document.getElementById('lead-desc').textContent.includes(String(graph.meta.counts.nodes)));
    check('统计卡渲染 6 格', $$(w.document, '#stats > div').length === 6);

    const cards = graph.nodes.map((n, i) => [n, i]).filter(([n]) => n.kind === 'card');
    let best = null;
    for (const [, i] of cards) {
      const info = w.__starmap_hooks.info(i);
      if (info.attacks > 0) { best = [i, info]; break; }
    }
    check('存在受攻击的卡节点', !!best);
    if (best) {
      const [i, info] = best;
      w.__starmap_hooks.select(i);
      const txt = w.__starmap_hooks.detailText();
      check('详情面板含节点 id', txt.includes(info.id), info.id);
      check('详情面板含四态', txt.includes(info.state));
      check('详情面板含 credibility', txt.includes(String(info.credibility)));
      check('详情面板含攻防计数', txt.includes('受攻击') && txt.includes(`被击败 ${info.defeated}`));
      w.__starmap_hooks.select(-1);
      check('取消固定后回到提示态', !w.__starmap_hooks.detailText().includes(info.id));
    }
  }
  dom.window.close();
}

// ── ③ index.html：系统现状面板（真数据 + 计数动画落位）────────────────────
{
  console.log('\n[3/3] web/index.html —— 系统现状面板 + 首屏计数');
  const dom = await mkDom('index.html');
  const { window: w } = dom;
  const inline = fs.readFileSync(path.join(WEB, 'index.html'), 'utf-8')
    .match(/<script type="module">([\s\S]*?)<\/script>/)[1]
    .replace("from './app.js'", `from '${pathToFileURL(path.join(WEB, 'app.js')).href}'`);
  const tmp = path.join(WEB, '.smoke_inline_655.mjs');
  fs.writeFileSync(tmp, inline, 'utf-8');
  try {
    await import(pathToFileURL(tmp).href);
    const t = (id) => w.document.getElementById(id).textContent.trim();
    const ready = await waitFor(() => t('s-cards') !== '—', 5000);
    check('现状面板已填充', ready);
    if (ready) {
      check('知识卡 = status.json 真值', t('s-cards') === String(status.cards.cards_real),
        `${t('s-cards')} vs ${status.cards.cards_real}`);
      check('规则数 = 67', t('s-rules') === String(status.rules.rules_total), t('s-rules'));
      check('保护器 = 9', t('s-prot') === String(status.protectors.protectors_total), t('s-prot'));
      check('逃逸率 = 0.0711%', t('s-escape') === `${status.escape.rate_pct.toFixed(4)}%`, t('s-escape'));
      check('现状面板脚注含数据来源与生成时间',
        t('status-note').includes('generated') || t('status-note').includes('生成于'));
      const stat0 = w.document.getElementById('stat-0');
      const graph = JSON.parse(fs.readFileSync(path.join(WEB, 'data', 'graph.json'), 'utf-8'));
      check('首屏节点数 = graph.json 真值',
        stat0 && stat0.textContent === String(graph.meta.counts.nodes),
        `${stat0 && stat0.textContent}`);
      check('星图按钮文案现算', w.document.getElementById('starmap-btn').textContent.includes(String(graph.meta.counts.nodes)));
    }
  } finally {
    try { fs.unlinkSync(tmp); } catch { /* 已清理 */ }
  }
  dom.window.close();
}

// ── ④ card.html：学习 MVP 三段式（656 D）────────────────────────────────
{
  console.log('\n[4/4] web/card.html —— 学习 MVP（前置 / 学习 / 自测）');
  const dom = await mkDom('card.html');
  const { window: w } = dom;
  await import(pathToFileURL(path.join(WEB, 'card.js')).href);
  const ready = await waitFor(() => w.__card_ready === true, 8000);
  check('页面就绪（__card_ready）', ready);
  if (ready) {
    const cards = JSON.parse(fs.readFileSync(path.join(WEB, 'data', 'cards.json'), 'utf-8'));
    const first = w.document.getElementById('pick').value;
    check('选卡下拉套数与 cards.json 一致',
      w.document.getElementById('pick').options.length === cards.count,
      `${w.document.getElementById('pick').options.length} vs ${cards.count}`);
    check('默认卡在 cards.json 里', !!cards.cards[first], first);
    check('前置段已渲染', w.document.getElementById('prereq').textContent.trim().length > 0);
    const head = w.document.getElementById('card-head').textContent;
    check('学习段含当前卡 id', head.includes(first), first);
    check('学习段含台账路径（provenance）',
      head.includes(cards.cards[first].path));
    const nSc = w.document.querySelectorAll('#selfcheck qy-card').length;
    check('自测段渲染出题目（≥5 题）', nSc >= 5, `${nSc} 题`);
    check('四态状态组件已写入（qy-status）',
      w.document.body.innerHTML.includes('qy-status state='));
    const prog = w.document.getElementById('progress').textContent;
    check('进度文案读本机存储', /本机已学\s+\d+\/\d+/.test(prog), prog.trim());
  }
  dom.window.close();
}

console.log(`\n[web-smoke-655] ${failures.length ? 'FAIL：' + failures.join(' / ') : '全部通过'}`);
process.exit(failures.length ? 1 : 0);
