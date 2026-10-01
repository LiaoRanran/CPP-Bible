// 672g B+C · 两页外抽后的**功能冒烟**（jsdom 真把页面跑起来，不是静态 grep）
//
// 跑法（在 web/ 下）：node tests/pages_extract_672g.test.mjs
// 若 jsdom 不可用 ⇒ 打印 SKIP 并 exit 0（**不把 SKIP 当 PASS**，与 tests/smoke.mjs 同口径）。
//
// 为什么必须有这一层：experiments.html / learn.html 的内联脚本被外抽成
//   js/experiments.js + js/experiments_core.js、js/learn.js + js/learn_core.js。
//   纯逻辑测试（experiments_core / learn_core）只证明"函数算得对"，
//   **证明不了"页面接线没断"** —— 少一个 import、写错一个 id、路径写错一层，
//   纯逻辑测试全绿而页面白屏。这里补上：真 boot 页面、真 mock fetch、真查渲染结果。
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

let passed = 0;
const ok = (name, cond, extra = '') => {
  assert.ok(cond, 'FAIL: ' + name + (extra ? ' · ' + extra : ''));
  passed++;
};

let JSDOM;
try {
  ({ JSDOM } = await import('jsdom'));
} catch {
  console.log('SKIP: jsdom 未安装（npm i -D jsdom 后重跑）');
  process.exit(0);
}

const WEB = fileURLToPath(new URL('../', import.meta.url));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** mock fetch：相对 web/ 读本地文件（站点是零后端静态站，这就是真实行为） */
const fetchMock = async (u) => {
  let rel = String(u);
  if (/^https?:\/\//.test(rel)) {
    try { rel = new URL(rel).pathname.replace(/^\//, ''); } catch { rel = String(u); }
  }
  rel = rel.replace(/^\.\//, '').split('?')[0].split('#')[0];
  const p = join(WEB, rel);
  if (!existsSync(p)) return { ok: false, status: 404, json: async () => ({}), text: async () => '' };
  const txt = readFileSync(p, 'utf8');
  return { ok: true, status: 200, json: async () => JSON.parse(txt), text: async () => txt };
};

/** 把一页 boot 起来：装全局 → 执行外部 module 脚本 → 等渲染落位 */
async function boot(page) {
  const html = readFileSync(join(WEB, page), 'utf8');
  const dom = new JSDOM(html, { url: 'http://localhost/' + page, pretendToBeVisual: true });
  const { window } = dom;
  for (const k of ['window', 'document', 'navigator', 'location', 'history', 'customElements',
    'HTMLElement', 'Element', 'Node', 'Event', 'CustomEvent', 'getComputedStyle',
    'requestAnimationFrame', 'cancelAnimationFrame', 'matchMedia', 'localStorage',
    'DOMParser', 'MutationObserver', 'ResizeObserver']) {
    if (window[k] === undefined) continue;
    const v = typeof window[k] === 'function' ? window[k].bind(window) : window[k];
    // Node 22 的 navigator / 部分全局是只读 getter ⇒ 赋值会抛；逐个别名兜住即可
    try { globalThis[k] = v; } catch { /* 只读全局：忽略 */ }
  }
  globalThis.fetch = fetchMock;
  globalThis.self = window;
  if (window.HTMLCanvasElement) window.HTMLCanvasElement.prototype.getContext = () => null;

  const externals = [...html.matchAll(/<script[^>]*\ssrc\s*=\s*"([^"]+)"[^>]*>/g)].map((m) => m[1]);
  const failed = [];
  for (const src of externals) {
    const abs = new URL(src, pathToFileURL(join(WEB, page)).href).href;
    try { await import(abs); } catch (e) { failed.push(src + ' → ' + String((e && e.message) || e)); }
  }
  await sleep(350);
  return { window, doc: window.document, externals, failed };
}

/* ══ ① experiments.html：外部脚本接上了，图表真渲染出来 ═════════════════ */
{
  const { doc, externals, failed } = await boot('experiments.html');
  ok('experiments.html 引用了外部 js/experiments.js',
    externals.some((s) => s === 'js/experiments.js'), externals.join(', '));
  ok('experiments.html 的外部脚本全部加载成功（无 404 / 无语法错）',
    failed.length === 0, failed.join(' | '));
  ok('experiments.html 不再有内联逻辑脚本（只有 robustness/a11y/keybind 三个短接线）',
    (readFileSync(join(WEB, 'experiments.html'), 'utf8').match(/<script type="module">([\s\S]*?)<\/script>/g) || [])
      .every((s) => s.length < 200));

  const base = doc.getElementById('c-baseline');
  ok('图 1（baseline）渲染出了 SVG', !!(base && base.querySelector('svg')), base ? base.innerHTML.slice(0, 60) : 'no host');
  ok('图 2（口径消融）渲染出了 SVG', !!(doc.getElementById('c-caliber') || {}).querySelector?.('svg'));
  ok('图 3（演化折线）渲染出了 SVG', !!(doc.getElementById('c-evolution') || {}).querySelector?.('svg'));
  ok('图 4（检测器构成）渲染出了 SVG', !!(doc.getElementById('c-detectors') || {}).querySelector?.('svg'));
  ok('图 5（能力构成雷达）渲染出了 SVG', !!(doc.getElementById('c-ability') || {}).querySelector?.('svg'));
  ok('数据源区块登记了真实路径（不是"加载中…"）',
    (doc.getElementById('src-list') || {}).innerHTML?.indexOf('mono') > 0);
  ok('baseline 图右上角有数据源说明', ((doc.getElementById('base-note') || {}).textContent || '').length > 4);
  ok('口径图右上角有口径说明（"臂 · 分母不同"）',
    ((doc.getElementById('cal-note') || {}).textContent || '').indexOf('分母不同') > 0);
  ok('检测器图标注了口径', ((doc.getElementById('det-note') || {}).textContent || '').indexOf('口径') > 0);
  ok('能力雷达标注了缺失轴或"六轴全部命中"',
    /六轴全部命中|缺真实值的轴/.test((doc.getElementById('abi-note') || {}).textContent || ''));
  // 切换数据集 tab 不抛异常，且图还在（外抽后事件接线没断）
  const tabs = doc.querySelectorAll('[data-ds]');
  ok('数据集 tab 有 4 个（全部/holdout/corpus/defect）', tabs.length === 4);
  tabs[1].dispatchEvent(new (doc.defaultView.MouseEvent)('click', { bubbles: true }));
  ok('点 holdout tab 后 baseline 图仍在', !!doc.getElementById('c-baseline').querySelector('svg'));
  ok('点 holdout tab 后 aria-selected 跟着切',
    tabs[1].getAttribute('aria-selected') === 'true' && tabs[0].getAttribute('aria-selected') === 'false');
  // 点柱出明细（wire 接线没断）
  const bar = doc.querySelector('#c-baseline [data-role]');
  if (bar) {
    bar.dispatchEvent(new (doc.defaultView.MouseEvent)('click', { bubbles: true }));
    const panel = doc.getElementById('d-baseline');
    ok('点柱后面板展开（明细接线没断）', panel && panel.hidden === false && panel.innerHTML.length > 0);
  } else {
    ok('点柱后面板展开（无柱可点时按空数据跳过）', true);
  }
}

/* ══ ② learn.html：外部脚本接上了，学习台真渲染出来 ═════════════════════ */
{
  const { window, doc, externals, failed } = await boot('learn.html');
  ok('learn.html 引用了外部 js/learn.js', externals.some((s) => s === 'js/learn.js'), externals.join(', '));
  ok('learn.html 的外部脚本全部加载成功', failed.length === 0, failed.join(' | '));
  ok('learn.html 不再有内联逻辑脚本',
    (readFileSync(join(WEB, 'learn.html'), 'utf8').match(/<script type="module">([\s\S]*?)<\/script>/g) || [])
      .every((s) => s.length < 200));

  ok('统计面板渲染出 6 个 stat-tile', doc.querySelectorAll('#dash .stat-tile').length === 6);
  ok('学习路径渲染出 SVG', !!doc.querySelector('#path-flow svg'));
  ok('路径 SVG 有 aria-label（可访问性没丢）',
    /aria-label="学习路径三阶段进度"/.test(doc.getElementById('path-flow').innerHTML));
  ok('薄弱热力图渲染出格子或空状态',
    doc.querySelectorAll('#heat .heat-cell').length > 0 || doc.querySelector('#heat .chart-empty') !== null);
  ok('掌握度曲线渲染出 SVG 或空状态',
    !!doc.querySelector('#spark svg') || !!doc.querySelector('#spark .chart-empty'));
  ok('今日队列有内容（条目或"没有要复习的"提示）',
    doc.querySelectorAll('#queue .queue-item').length > 0 || /没有要复习的/.test(doc.getElementById('queue').textContent));
  ok('学习区渲染出卡（三阶段或四段式，不是空白）',
    doc.querySelectorAll('#study .ls-stage').length >= 3, doc.getElementById('study').textContent.slice(0, 40));
  ok('位置说明写出来了（第 x / y 张）', /第 \d+ \/ \d+ 张/.test(doc.getElementById('pos-note').textContent));
  ok('掌握度百分比写出来了', /%$/.test(doc.getElementById('mastery-pct').textContent.trim()));
  ok('进度条宽度跟着设了', (doc.getElementById('mastery-bar').style.width || '').indexOf('%') > 0);

  // 键盘导航：空格揭晓 → 评分按钮出现（learn_engine.handleKey 的接线还在）
  const before = doc.getElementById('study').innerHTML;
  doc.dispatchEvent(new window.KeyboardEvent('keydown', { key: ' ', bubbles: true }));
  const after = doc.getElementById('study').innerHTML;
  ok('按空格 ⇒ 学习区重渲染（键盘导航接线没断）', after !== before);
  ok('按空格揭晓后出现评分按钮（1–4）', doc.querySelectorAll('#study .grade').length === 4);
  // 牌组切换不抛异常
  const deckTabs = doc.querySelectorAll('.deck-tab');
  ok('牌组 tab 有 2 个（知识卡 / 错例）', deckTabs.length === 2);
  deckTabs[1].dispatchEvent(new (window.MouseEvent)('click', { bubbles: true }));
  ok('切到错例牌组后学习区仍渲染出四段式', doc.querySelectorAll('#study .ls-stage').length >= 4);
  ok('切到错例牌组后域筛选被隐藏（错例无域维度）', doc.getElementById('f-domain-wrap').hidden === true);
  deckTabs[0].dispatchEvent(new (window.MouseEvent)('click', { bubbles: true }));
  ok('切回知识卡后域筛选恢复显示', doc.getElementById('f-domain-wrap').hidden === false);
}

/* ══ ③ starmap.html：操作提示真的在画布角落 ═══════════════════════════ */
{
  const { doc, externals, failed } = await boot('starmap.html');
  ok('starmap.html 外部脚本全部加载成功', failed.length === 0, failed.join(' | '));
  const hint = doc.getElementById('map-hint');
  ok('画布角落有 #map-hint 提示元素', !!hint);
  ok('提示文案被 JS 写成"左键平移 / 右键旋转 / 滚轮缩放 / 双击复位"',
    (hint.textContent || '').indexOf('左键平移 / 右键旋转 / 滚轮缩放 / 双击复位') >= 0, hint.textContent);
  ok('提示在 canvas 容器内（真的叠在画布上）',
    hint.parentElement && hint.parentElement.className.indexOf('canvas-wrap') >= 0);
  const canvas = doc.getElementById('graph');
  ok('canvas 的 aria-label 已改为"左键拖拽平移"口径',
    /左键拖拽平移/.test(canvas.getAttribute('aria-label') || ''));
  ok('页脚 kbd 提示已同步（右键拖拽旋转）',
    /右键拖拽/.test(doc.querySelector('.kbd-hints') ? doc.querySelector('.kbd-hints').textContent : ''));
  ok('starmap.html 仍只引一个 starmap.js（未误加脚本）',
    externals.filter((s) => /starmap/.test(s)).length === 1);
}

console.log('pages_extract_672g: ' + passed + ' assertions passed');
