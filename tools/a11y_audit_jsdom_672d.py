#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""a11y_audit_jsdom_672d.py — **渲染后**的 WCAG 2.1 AA 审计（672d C，第一阶段：只报告不修）。

背景（P3 批判）：tools/a11y_audit_670c4.py 只 parse **静态 HTML 源码** ——
首页表格、卡库网格、实验页图表等 JS 渲染出来的 DOM 全在盲区，但验收写"8 页 0 问题"越界了。

本工具补上那块盲区：
  1. 用 **jsdom** 把每页 boot 起来（执行页面 module + 内联 module 脚本、mock fetch 读本地数据）；
  2. 把渲染后的 DOM 序列化成 HTML；
  3. **复用** a11y_audit_670c4.py 的成熟规则做审计（同一套判据，便于两份报告对比）；
  4. 焦点环可见性走 CSS 文本检查（jsdom 不执行 CSS，这条它管不了）。

为什么不直接在 Python 里跑 jsdom：jsdom 是 Node 库。本脚本把渲染用的 JS 写成临时文件、
用 node 跑、读回产物 —— 仍然只有一个 .py 交付，不额外污染仓库。

输出 `data/a11y_audit_jsdom_672d.json`，字段与 670c4 对齐，另加 coverage / 渲染统计。
退出码：0 = 无 critical；1 = 有 critical（**本批只报告不修**，红是正常的、是要修的清单）。
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "web")
OUT = os.path.join(ROOT, "data", "a11y_audit_jsdom_672d.json")
PAGES = ["index", "cards", "learn", "experiments", "verdicts", "starmap", "verify", "card"]

# 复用静态审计的**判据**（不修改它，只 import）
sys.path.insert(0, os.path.join(ROOT, "tools"))
import a11y_audit_670c4 as STATIC  # noqa: E402

COVERAGE = "jsdom_rendered"
LIMITATIONS = [
    "jsdom 不是真实浏览器：无布局、无真实 canvas/WebGL 绘制、无 CSS 计算",
    "焦点环颜色靠 CSS 文本检查（jsdom 不执行 CSS），真实可见性仍需 contrast_check.js 与人工确认",
    "内联 module 脚本以 data: URL 方式执行（相对 import 已重写为绝对 URL），与浏览器加载顺序不完全等价",
    "数据来自本地文件 mock 的 fetch，不是真实 HTTP（404/超时等真实故障模式未覆盖）",
    "672d 第一阶段：**只报告不修**；修复与双工具合并归 672e",
]

# ── Node 侧渲染脚本（临时文件里跑）────────────────────────────────────────
RENDER_JS = r"""
// 672d C · 用 jsdom 把页面 boot 起来，导出渲染后的 DOM
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const [webDir, outDir, pagesCsv, jsdomEntry] = process.argv.slice(2);
const pages = pagesCsv.split(',').filter(Boolean);
const SETTLE_MS = Number(process.env.QY_SETTLE_MS || 400);
const base = pathToFileURL(join(webDir, 'index.html')).href;

// jsdom 装在仓库根 node_modules；本脚本跑在系统临时目录里，裸 import 'jsdom' 解析不到
// ⇒ 由 Python 侧解析出入口的绝对路径，这里按 file:// 直接导入。
const jsdomMod = await import(pathToFileURL(jsdomEntry).href);
const JSDOM = jsdomMod.JSDOM || (jsdomMod.default && jsdomMod.default.JSDOM);
if (typeof JSDOM !== 'function') { console.error('jsdom 入口不可用: ' + jsdomEntry); process.exit(2); }

/** mock fetch：相对 web/ 读本地文件（站点是零后端静态站，这就是真实行为） */
const fetchMock = async (u) => {
  let rel = String(u);
  if (/^https?:\/\//.test(rel)) {
    try { rel = new URL(rel).pathname.replace(/^\//, ''); } catch { rel = String(u); }
  }
  rel = rel.replace(/^\.\//, '').split('?')[0].split('#')[0];
  const p = join(webDir, rel);
  if (!existsSync(p)) {
    return { ok: false, status: 404, json: async () => ({}), text: async () => '' };
  }
  const txt = readFileSync(p, 'utf8');
  return { ok: true, status: 200, json: async () => JSON.parse(txt), text: async () => txt };
};

/** 把内联 module 里的相对 import 改写成绝对 file:// URL，再用 data: URL 执行 */
const absUrl = (spec) => new URL(spec, base).href;
const toDataUrl = (code) => 'data:text/javascript;base64,' + Buffer.from(
  code.replace(/(\bfrom\s+|import\s*\(?\s*)(['"])(\.\.?\/[^'"]+)\2/g,
    (m, pre, q, spec) => pre + q + absUrl(spec) + q),
  'utf8').toString('base64');

const setGlobal = (k, v) => { try { globalThis[k] = v; } catch { /* 只读全局：忽略 */ } };

// 页面 boot 时会调 canvas.getContext —— jsdom 不实现（未装 canvas 包）。
// shim 成返回 null：站点本来就有"无 canvas ⇒ 2D 降级"的路径，正好走它。
// 这与真实浏览器的"WebGL 不可用"降级是同一类故障模式，如实登记到 limitations。
const uncaught = [];
process.on('unhandledRejection', (e) => uncaught.push(String((e && e.stack) || e).slice(0, 300)));
process.on('uncaughtException', (e) => uncaught.push(String((e && e.stack) || e).slice(0, 300)));

const report = [];
for (const pg of pages) {
  const file = join(webDir, pg + '.html');
  if (!existsSync(file)) continue;
  const html = readFileSync(file, 'utf8');
  const dom = new JSDOM(html, { url: 'http://localhost/' + pg + '.html', pretendToBeVisual: true });
  const { window } = dom;
  for (const k of ['window', 'document', 'navigator', 'location', 'history', 'customElements',
    'HTMLElement', 'Element', 'Node', 'Event', 'CustomEvent', 'getComputedStyle',
    'requestAnimationFrame', 'cancelAnimationFrame', 'matchMedia', 'localStorage',
    'DOMParser', 'MutationObserver', 'ResizeObserver']) {
    if (window[k] !== undefined) setGlobal(k, typeof window[k] === 'function' ? window[k].bind(window) : window[k]);
  }
  setGlobal('fetch', fetchMock);
  setGlobal('self', window);   // 浏览器里 self === window；jsdom/Node 没有这个全局（实测踩过）
  // 注意：**不要**把 window.performance 覆盖到全局 —— jsdom 的 hr-time 实现会
  // 引用全局 performance，覆盖后 performance.now() 自引用，栈溢出（实测踩过）。

  const nodesStatic = window.document.getElementsByTagName('*').length;
  if (window.HTMLCanvasElement && !window.HTMLCanvasElement.prototype.getContext.__shimmed) {
    window.HTMLCanvasElement.prototype.getContext = function getContext() { return null; };
    window.HTMLCanvasElement.prototype.getContext.__shimmed = true;
  }

  // ① 外部 module 脚本
  const externals = [...html.matchAll(/<script[^>]*\ssrc\s*=\s*"([^"]+)"[^>]*>/g)].map((m) => m[1]);
  // ② 内联 module 脚本
  const inlines = [...html.matchAll(/<script[^>]*type\s*=\s*"module"[^>]*>([\s\S]*?)<\/script>/g)]
    .map((m) => m[1]).filter((c) => c.trim());

  const modules = [];
  for (const src of externals) {
    try {
      await import(absUrl(src));
      modules.push({ src, kind: 'external', ok: true });
    } catch (e) {
      modules.push({ src, kind: 'external', ok: false, error: String((e && e.message) || e).slice(0, 200) });
    }
  }
  for (const code of inlines) {
    try {
      await import(toDataUrl(code));
      modules.push({ src: 'inline#' + code.slice(0, 24).replace(/\s+/g, ' '), kind: 'inline', ok: true });
    } catch (e) {
      modules.push({ src: 'inline#' + code.slice(0, 24).replace(/\s+/g, ' '), kind: 'inline', ok: false,
        error: String((e && e.message) || e).slice(0, 200) });
    }
  }

  await new Promise((r) => setTimeout(r, SETTLE_MS));
  const rendered = window.document.documentElement.outerHTML;
  writeFileSync(join(outDir, pg + '.html'), rendered, 'utf8');
  report.push({
    page: pg + '.html',
    nodes_static: nodesStatic,
    nodes_rendered: window.document.getElementsByTagName('*').length,
    modules,
  });
  dom.window.close();
}
console.log(JSON.stringify({ pages: report, uncaught }));
"""


def find_node() -> str:
    for cand in (os.environ.get("NODE_BIN"), shutil.which("node"), shutil.which("node.exe")):
        if cand:
            return cand
    return ""


def find_jsdom_entry(node: str) -> str:
    """解析 jsdom 的入口绝对路径（本脚本跑在系统临时目录，裸 import 解析不到仓库的 node_modules）。"""
    probe = subprocess.run(
        [node, "-e", "console.log(require.resolve('jsdom'))"],
        cwd=ROOT, capture_output=True, text=True)
    p = (probe.stdout or "").strip().splitlines()
    if probe.returncode == 0 and p and p[-1].strip():
        return p[-1].strip()
    # 兜底：手工向上找 node_modules/jsdom/lib/api.js
    d = ROOT
    while True:
        cand = os.path.join(d, "node_modules", "jsdom", "lib", "api.js")
        if os.path.isfile(cand):
            return cand
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    raise RuntimeError("找不到 jsdom（仓库根 node_modules 未安装；先 npm i -D jsdom）")


def render_pages(pages) -> tuple:
    """返回 (render_report, tmp_dir)；tmp_dir 里的 HTML 供静态规则复用。"""
    node = find_node()
    if not node:
        raise RuntimeError("找不到 node（PATH 或 NODE_BIN 都没有）")
    jsdom_entry = find_jsdom_entry(node)
    tmp = tempfile.mkdtemp(prefix="a11y_jsdom_672d_")
    js_path = os.path.join(tmp, "render.mjs")
    with open(js_path, "w", encoding="utf-8") as fh:
        fh.write(RENDER_JS)
    proc = subprocess.run([node, js_path, WEB, tmp, ",".join(pages), jsdom_entry],
                          capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise RuntimeError(f"jsdom 渲染失败（{proc.returncode}）：{proc.stderr[:800]}")
    # stdout 里混着页面自己的 console.error 等，从尾部找**能解析且带 pages 键**的那一行
    for line in reversed(proc.stdout.strip().splitlines()):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and "pages" in data:
            return data, tmp
    raise RuntimeError(f"jsdom 渲染无产物：{proc.stdout[:400]}")


def stale_aria_busy_issues(rendered_path: str) -> list:
    """渲染完成后的 aria-busy 残留检查（**只有渲染后的 DOM 才查得出来**）。

    实测踩点：robustness.js 的 setState(el,'ready') 只改 data-qy-state 和 class，
    **不清 aria-busy="true"** ⇒ 内容都渲染完了，屏幕阅读器仍认为该区域"正在更新"。
    启发式（第一阶段，从严报告）：aria-busy=true 且 (状态已到 ready/error/empty 或 已有内容)
    ⇒ moderate。真"仍在加载"（空 + loading）不算。
    """
    html = open(rendered_path, encoding="utf-8").read()
    p = STATIC.Collector()
    p.feed(html)
    issues = []
    for el in p.elems:
        a = el["attrs"]
        if a.get("aria-busy") != "true":
            continue
        state = a.get("data-qy-state")
        has_content = bool(el.get("text", "").strip())
        if state in ("ready", "error", "empty") or has_content:
            issues.append({
                "severity": "moderate",
                "rule": "stale-aria-busy",
                "detail": (f"<{el['tag']}> 渲染完成后 aria-busy=\"true\" 仍残留"
                           f"（state={state or '未设置'}，内容{'已渲染' if has_content else '为空'}）"
                           "—— 屏幕阅读器会认为仍在更新；setState 应同步清 aria-busy"),
                "line": el["line"],
            })
    return issues


def focus_ring_check() -> dict:
    """焦点环可见性：jsdom 不执行 CSS ⇒ 这里做 CSS 文本检查（672a 已令牌化，本批只验证）。"""
    res = {"css_files": [], "issues": []}
    a11y = os.path.join(WEB, "css", "a11y.css")
    tokens = os.path.join(WEB, "css", "design-tokens.css")
    if not os.path.isfile(a11y):
        res["issues"].append({"severity": "critical", "rule": "focus-ring-css", "detail": "缺 css/a11y.css"})
        return res
    css = open(a11y, encoding="utf-8").read()
    tok = open(tokens, encoding="utf-8").read() if os.path.isfile(tokens) else ""
    res["css_files"] = ["css/a11y.css", "css/design-tokens.css"]
    if ":focus-visible" not in css:
        res["issues"].append({"severity": "critical", "rule": "focus-ring-css",
                              "detail": "a11y.css 无 :focus-visible 规则"})
    if "var(--focus-ring)" not in css:
        res["issues"].append({"severity": "critical", "rule": "focus-ring-token",
                              "detail": "焦点环未使用 var(--focus-ring)（硬编码色会击穿令牌层）"})
    if "--focus-ring:" not in tok:
        res["issues"].append({"severity": "critical", "rule": "focus-ring-token",
                              "detail": "design-tokens.css 未定义 --focus-ring"})
    if "forced-colors" not in css:
        res["issues"].append({"severity": "moderate", "rule": "focus-ring-forced-colors",
                              "detail": "无 forced-colors 高对比度兜底"})
    res["ok"] = not any(i["severity"] == "critical" for i in res["issues"])
    return res


def audit(pages) -> dict:
    rendered, tmp = render_pages(pages)
    page_reports = rendered["pages"]
    uncaught = rendered.get("uncaught", [])
    out_pages = []
    for r in page_reports:
        path = os.path.join(tmp, r["page"])
        res = STATIC.audit_page(path) if os.path.isfile(path) else {
            "page": r["page"], "issues": [], "counts": {}}
        # 672d：渲染后专属规则（静态审计物理上看不到这类问题）
        extra = stale_aria_busy_issues(path) if os.path.isfile(path) else []
        res["issues"] = list(res.get("issues", [])) + extra
        res["counts"] = {s: sum(1 for i in res["issues"] if i["severity"] == s)
                         for s in ("critical", "moderate", "minor")}
        res.update({
            "nodes_static": r["nodes_static"],
            "nodes_rendered": r["nodes_rendered"],
            "nodes_added_by_js": r["nodes_rendered"] - r["nodes_static"],
            "modules": r["modules"],
            "modules_failed": [m for m in r["modules"] if not m["ok"]],
        })
        out_pages.append(res)
    total = {"critical": 0, "moderate": 0, "minor": 0}
    for p in out_pages:
        for k, v in p.get("counts", {}).items():
            total[k] += v
    focus = focus_ring_check()
    for i in focus["issues"]:
        total[i["severity"]] = total.get(i["severity"], 0) + 1
    total["moderate"] += len(uncaught)   # 渲染期未捕获异常：如实计入 moderate
    shutil.rmtree(tmp, ignore_errors=True)
    return {
        "coverage": COVERAGE,
        "js_rendered_dom_audited": True,
        "static_only_tool": "tools/a11y_audit_670c4.py",
        "pages": out_pages,
        "focus_ring": focus,
        "uncaught": uncaught,
        "total": total,
        "critical_total": total["critical"],
        "limitations": LIMITATIONS,
        "nodes_added_by_js_total": sum(p.get("nodes_added_by_js", 0) for p in out_pages),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="渲染后（jsdom）的 WCAG 2.1 AA 审计（672d C）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--pages", default=",".join(PAGES))
    args = ap.parse_args()
    pages = [p for p in args.pages.split(",") if p]
    res = audit(pages)
    if args.write:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("[a11y-jsdom] coverage: jsdom_rendered（渲染后的 DOM；静态源码版见 a11y_audit_670c4.py）")
        print(f"[a11y-jsdom] {len(res['pages'])} 页，合计 {res['total']}，"
              f"JS 新增节点 {res['nodes_added_by_js_total']}")
        for p in res["pages"]:
            print(f"  {p['page']:<16} {p['counts']} 节点 {p['nodes_static']}→{p['nodes_rendered']}"
                  f" (+{p['nodes_added_by_js']})")
            for m in p.get("modules_failed", []):
                print(f"      [模块失败] {m['src']}: {m.get('error','')[:90]}")
            for i in p["issues"]:
                if i["severity"] == "critical":
                    print(f"      [CRIT] {i['rule']}: {i['detail']} (L{i.get('line')})")
        for i in res["focus_ring"]["issues"]:
            print(f"  [焦点环] {i['severity']}: {i['rule']} — {i['detail']}")
        for u in res.get("uncaught", []):
            print(f"  [渲染异常] {u.splitlines()[0][:110] if u else u}")
        print("[a11y-jsdom] " + ("PASS（0 critical）" if res["critical_total"] == 0
                                else f"发现 {res['critical_total']} 个 critical（本批只报告不修 → 672e）"))
    return 0 if res["critical_total"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
