// 670c5 · dist 构建脚本（web/ → web/dist/）
// 站点是零构建静态站；本脚本只做**确定性同步**（复制运行期资源），供发布/验证用。
// 用法：node web/build.mjs        或在 web/ 下 node build.mjs
import { cpSync, mkdirSync, rmSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const SRC = dirname(fileURLToPath(import.meta.url));
const DIST = join(SRC, 'dist');

// 运行期资源（白名单：不含 tests/ node_modules/ dist/ 自身）
const DIRS = ['css', 'js', 'components', 'vendor', 'data'];
const GLOBS = ['.html', '.js', '.css', '.json'];

rmSync(DIST, { recursive: true, force: true });
mkdirSync(DIST, { recursive: true });

let copied = 0;
for (const d of DIRS) {
  const src = join(SRC, d);
  if (existsSync(src)) { cpSync(src, join(DIST, d), { recursive: true }); copied++; }
}
for (const f of readdirSync(SRC)) {
  const p = join(SRC, f);
  if (statSync(p).isFile() && GLOBS.some((e) => f.endsWith(e)) && f !== 'build.mjs') {
    cpSync(p, join(DIST, f));
    copied++;
  }
}
console.log(`[build] dist 重建完成：复制 ${copied} 项 → ${DIST}`);
