// 672d A · 测试入口：**先 build，再跑测试**
//
// 病（P3 批判）：package.json 的 test 直接跑 tests/*.test.mjs，没有先跑 build.mjs。
//   perf_670c5.test.mjs 读的是 **dist/**（dist/index.html、dist/js/*.js）—— 改完源码
//   直接跑测试，绿的是**上一次构建**的产物。测试越绿，越不可信。
//
// 修：build 前置，且 **build 失败即短路**（不跑测试、返回 build 的退出码）。
//   测试本身跑完全部（不中途停），最后汇总 —— 一次性看到所有红，比"第一个红就停"有用。
//
// 用法：node run_tests.mjs   （npm test 走的就是它）
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));

// 顺序：纯逻辑 → 组件 → 页面级（依赖 jsdom/dist 的放后面）
const TESTS = [
  'tests/learn_engine.test.mjs',
  'tests/learn_core.test.mjs',
  'tests/charts.test.mjs',
  'tests/experiments_core.test.mjs',
  'tests/cards.test.mjs',
  'tests/verdicts.test.mjs',
  'tests/starmap.test.mjs',
  'tests/starmap_672e.test.mjs',
  'tests/starmap_interaction_672g.test.mjs',
  'tests/contrast.test.mjs',
  'tests/robustness_670c3.test.mjs',
  'tests/a11y_670c4.test.mjs',
  'tests/keybind_670c5.test.mjs',
  'tests/perf_670c5.test.mjs',
  'tests/home_dom_672d.test.mjs',
  'tests/pages_extract_672g.test.mjs',
  'tests/perf_fix_672d.test.mjs',
  'tests/smoke.mjs',
  'tests/data_672b.test.mjs',
  'tests/prune_672b.test.mjs',
  'tests/home_672c.test.mjs',
  'tests/debt_672c.test.mjs',
];

/** 从测试自己的输出里抓断言数（"N 断言全绿" / "N assertions passed"） */
const COUNT_RE = /(\d+)\s*(?:断言全绿|assertions passed)/;

function run(args) {
  return spawnSync(process.execPath, args, { cwd: here, encoding: 'utf8' });
}

const t0 = Date.now();

// ── 1/2 build：dist 必须是最新的，否则后面的 perf / dist 断言都在测旧产物 ──
console.log('[test] 1/2 build：重建 dist（perf / dist 断言读的是 dist，旧产物 = 假绿）');
const b = run(['build.mjs']);
if (b.stdout) process.stdout.write(b.stdout);
if (b.stderr) process.stderr.write(b.stderr);
if (b.status !== 0) {
  console.error(`[test] build 失败（退出码 ${b.status ?? 1}）⇒ 不继续跑测试`);
  process.exit(b.status ?? 1);
}

// ── 2/2 测试 ──
console.log(`[test] 2/2 跑 ${TESTS.length} 个测试`);
const failed = [];
let assertions = 0;
for (const t of TESTS) {
  const r = run([t]);
  const out = (r.stdout || '') + (r.stderr || '');
  const m = COUNT_RE.exec(out);
  if (m) assertions += Number(m[1]);
  if (r.status === 0) {
    console.log(`  ✓ ${t}${m ? ` (${m[1]})` : ''}`);
  } else {
    failed.push(t);
    console.log(`  ✗ ${t}  (退出码 ${r.status})`);
    if (out.trim()) console.log(out.trim().split('\n').map((l) => '      ' + l).join('\n'));
  }
}

const secs = ((Date.now() - t0) / 1000).toFixed(1);
if (failed.length) {
  console.error(`[test] ${failed.length}/${TESTS.length} 个测试失败：${failed.join(', ')}`);
  process.exit(1);
}
console.log(`[test] ${TESTS.length}/${TESTS.length} 全绿，${assertions} 条断言，${secs}s`);
