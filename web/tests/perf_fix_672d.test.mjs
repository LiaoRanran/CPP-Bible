// 672d F1 · perf 口径修正的验收测试（无 DOM；子进程调 perf_audit_670c5.py 真跑）
//
// 锁三件事：
//   1. assets_gzip 只算**加载时资源**（link/script/img），`<a href>` 导航链接不计入；
//   2. 预算仍是 120KB —— 口径修正**不得**顺手放松标准；
//   3. 旧口径数字保留为 legacy 字段，新 ≤ 旧（导航链接只会让数字虚大）。
// 注意：数字变小是**口径变对**，不是性能提升 —— 这里锁的是口径，不是性能结论。
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { join, dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));      // web/tests
const webDir = resolve(here, '..');                        // web/
const repoDir = resolve(webDir, '..');                     // 仓库根
const tool = join(repoDir, 'tools', 'perf_audit_670c5.py');

let n = 0;
const ok = (c, m) => { assert.ok(c, m); n++; };

function pickPython() {
  for (const c of [process.env.PYTHON_BIN, 'python', 'python3']) {
    if (!c) continue;
    const r = spawnSync(c, ['--version'], { encoding: 'utf8' });
    if (r.status === 0) return c;
  }
  return null;
}

const py = pickPython();
if (!py) {
  console.log('perf_fix_672d: 跳过（找不到 python；设 PYTHON_BIN 可指定）');
  process.exit(0);
}

const r = spawnSync(py, [tool, '--json'], { cwd: repoDir, encoding: 'utf8', timeout: 120000 });
ok(r.status === 0, `perf_audit 退出码 0（实际 ${r.status}）${r.stderr ? '\n' + r.stderr.slice(0, 300) : ''}`);
const rep = JSON.parse(r.stdout);

// ① 口径声明与预算
ok(String(rep.gzip_scope || '').includes('load-time'), '产物带口径声明（load-time only）');
ok(rep.budget.home_gzip_kb === 120, '预算仍是 120KB（未放松）');
ok(rep.home_assets_gzip_kb <= rep.budget.home_gzip_kb,
  `首页首屏 gzip ${rep.home_assets_gzip_kb}KB ≤ ${rep.budget.home_gzip_kb}KB`);
ok(rep.home_assets_gzip_kb_legacy > rep.home_assets_gzip_kb,
  `新口径 ${rep.home_assets_gzip_kb}KB < 旧口径 ${rep.home_assets_gzip_kb_legacy}KB（导航链接已剔除）`);

// ② 首页：导航链接在 nav_refs，不在 load_refs
const home = rep.pages.find((p) => p.page === 'index.html');
ok(home, '产物含 index.html');
ok(home.nav_refs.length > 0, '首页确有导航链接（口径修正的前提）');
ok(home.nav_refs.some((x) => /\.json$/.test(x)), '导航链接含 .json 数据文件（旧口径误计入的正是它们）');
ok(!home.load_refs.some((x) => /\.json$/.test(x)), '加载时资源不含 .json');
ok(home.load_refs.every((x) => /\.(css|js|png|jpe?g|svg|ico|webp|woff2?)$/i.test(x)),
  '加载时资源都是 css/js/图片/字体类（' + home.load_refs.length + ' 项）');
ok(home.load_refs.every((x) => !home.nav_refs.includes(x)), '加载时资源与导航链接互不重叠');
ok(home.load_refs.every((x) => existsSync(join(webDir, x.split('?')[0]))),
  '加载时资源全部真实存在（引用有效性）');

// ③ 全部页面：新口径 ≤ 旧口径（逐页单调，不允许任何页反弹）
for (const p of rep.pages) {
  ok(p.assets_gzip_kb <= p.assets_gzip_kb_legacy,
    `${p.page}: 新口径 ${p.assets_gzip_kb}KB ≤ 旧口径 ${p.assets_gzip_kb_legacy}KB`);
}

console.log(`perf_fix_672d: ${n} 断言全绿`);
