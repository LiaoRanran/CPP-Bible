// 669c · jsdom 冒烟测试（页面结构 + 图表 DOM）
// 若环境未装 jsdom，则优雅跳过（不报错退出），不阻塞 CI。
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

async function main() {
  let JSDOM;
  try {
    ({ JSDOM } = await import('jsdom'));
  } catch {
    console.log('SMOKE SKIP: jsdom 未安装（npm i -D jsdom 后重跑）');
    return;
  }
  const dir = new URL('../', import.meta.url);
  const pages = ['index.html', 'cards.html', 'learn.html', 'experiments.html',
    'starmap.html', 'verdicts.html', 'verify.html', 'card.html'];
  let n = 0;
  for (const p of pages) {
    const html = readFileSync(new URL(p, dir), 'utf8');
    const dom = new JSDOM(html, { url: 'http://localhost/' + p });
    const doc = dom.window.document;
    assert.ok(doc.querySelector('qy-nav'), `${p}: 含 qy-nav`);
    assert.ok(doc.querySelector('main'), `${p}: 含 main`);
    n++;
  }

  // 图表 DOM 真渲染（零依赖 SVG）
  const dom = new JSDOM('<!DOCTYPE html><body><div id="h"></div></body>', { url: 'http://localhost/' });
  const { window } = dom;
  globalThis.document = window.document;
  globalThis.getComputedStyle = window.getComputedStyle.bind(window);
  const { barChart, pieChart } = await import('../js/charts.js');
  const h = window.document.getElementById('h');
  barChart(h, [{ label: 'a', value: 5 }, { label: 'b', value: 3 }], {});
  assert.ok(h.querySelector('svg'), 'barChart 产出 <svg>');
  pieChart(h, [{ label: 'x', value: 1 }, { label: 'y', value: 2 }]);
  assert.ok(h.querySelector('svg'), 'pieChart 产出 <svg>');

  console.log(`SMOKE: ${n} 页面结构校验 + 图表 DOM 渲染 ✓`);
}

main().then(() => process.exit(0)).catch((e) => { console.error(e.message); process.exit(1); });
