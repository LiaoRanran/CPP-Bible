// C2 真实解析校验：用 mermaid 官方 parser（mermaid.parse）验证 Book/ 下所有
// ```mermaid 代码块。比纯静态括号校验更强——能捕获 mermaid 语法层面的真实报错。
//
// 依赖：mermaid + jsdom（装在受管 node workspace 的 node_modules 里）。
// 运行：
//   NODE_PATH=<managed>/node_modules node tools/mermaid_parse_check.mjs [bookDir]
// 退出码：0 = 全部通过；1 = 有块解析失败。
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';
import { createRequire } from 'module';

// mermaid + jsdom 装在受管 node workspace，不在本仓库 node_modules。
// ESM 不认 NODE_PATH，故用 createRequire 从指定目录解析包入口后再动态导入。
const MODULES = process.env.MERMAID_NODE_MODULES
  || 'C:/Users/ASUS/.workbuddy/binaries/node/workspace/node_modules';
const req = createRequire(pathToFileURL(path.join(MODULES, 'anchor.js')));
const { JSDOM } = await import(pathToFileURL(req.resolve('jsdom')));

// 为 mermaid 提供浏览器环境
const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>', { pretendToBeVisual: true });
global.window = dom.window;
global.document = dom.window.document;
try { global.navigator = dom.window.navigator; } catch {}

const mermaid = (await import(pathToFileURL(req.resolve('mermaid')))).default;
mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(__dirname, '..');
const ROOT = process.argv[2] || path.join(REPO, 'Book');

function extractBlocks(fp) {
  const text = fs.readFileSync(fp, 'utf-8');
  const lines = text.split(/\r?\n/);
  const blocks = [];
  let inBlock = false, buf = [], start = 0;
  lines.forEach((line, i) => {
    if (!inBlock) {
      if (line.trim().startsWith('```mermaid')) { inBlock = true; buf = []; start = i + 1; }
    } else {
      if (line.trim().startsWith('```')) { blocks.push({ start, code: buf.join('\n') }); inBlock = false; }
      else buf.push(line);
    }
  });
  return blocks;
}

function* walk(dir) {
  yield dir;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory() && !e.name.startsWith('_legacy')) yield* walk(path.join(dir, e.name));
  }
}

let total = 0, fail = 0;
const failures = [];

for (const dp of walk(ROOT)) {
  for (const fn of fs.readdirSync(dp)) {
    if (!fn.endsWith('.md')) continue;
    const fp = path.join(dp, fn);
    for (const { start, code } of extractBlocks(fp)) {
      if (!code.trim()) continue;
      total++;
      try {
        await mermaid.parse(code);
      } catch (e) {
        fail++;
        const msg = (e && e.message) ? e.message.split('\n')[0] : String(e);
        failures.push({ file: path.relative(REPO, fp), line: start, msg });
        console.log(`  x ${path.relative(REPO, fp)}:${start}  ${msg}`);
      }
    }
  }
}

console.log(`\nmermaid.parse 真实解析：总计 ${total} 块，失败 ${fail}`);
process.exit(fail ? 1 : 0);
