#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""perf_audit_670c5.py — 前端性能静态审计（670c5 B1）。

检查每页：HTML 体积 / 首屏 JS·CSS 体积(gzip) / 外部依赖 / CSS 在 head / JS 在 body 末尾或 defer /
图片 width·height / DOM 节点数估算 / console.log·debugger 残留 / 自定义字体。
输出 `data/perf_audit_670c5.json`。退出码：0 = 无 critical；1 = 有 critical。

672d B · `assets_gzip` 口径修正（P3 批判：预算失去约束力）：
  旧口径把**所有** `src|href` 都算进"首屏 gzip"，包括 `<a href="data/metrics_666.json">`
  这类**导航链接** —— 浏览器加载页面时根本不会下载它们（要点一下才下载）。
  后果：台账 / manifest 一变大、或给页面多加几个导航入口，首页"性能"就凭空变差，
  120KB 预算于是失去约束力（它量的不是首屏）。
  新口径只算**加载时资源**：`<link rel=stylesheet|icon|preload|manifest…>`、`<script src>`、`<img src>`。
  导航链接单列到 `nav_refs`（只报告、不计入预算）。
  注意：**数字变小不代表性能提升，只是口径变对了** —— 别写成"性能提升 X%"。
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "web")
OUT = os.path.join(ROOT, "data", "perf_audit_670c5.json")
PAGES = ["index", "cards", "learn", "experiments", "verdicts", "starmap", "verify", "card"]

BUDGET_HTML_KB = 60          # 单页 HTML（未压缩）
BUDGET_DOM_NODES = 1500
BUDGET_HOME_GZIP_KB = 120    # 首页 gzip 合计（672d：口径修正后**不放松**，仍是 120KB）
REF_RE = re.compile(r'(?:src|href)\s*=\s*"([^"]+)"')
TAG_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9-]*)")

# ── 672d B · 加载时资源 vs 导航链接 ──
# 加载时：浏览器解析到就会去下载；导航链接：用户点击才下载（与首屏无关）。
LOAD_TAGS_RE = re.compile(r"<(link|script|img)\b([^>]*)>", re.I)
NAV_A_RE = re.compile(r"<a\b([^>]*)>", re.I)
ATTR_VAL_RE = re.compile(r'(?:src|href)\s*=\s*"([^"]+)"')
REL_RE = re.compile(r'rel\s*=\s*"([^"]+)"')
LOADABLE_REL = {"stylesheet", "icon", "shortcut", "apple-touch-icon", "manifest",
                "preload", "modulepreload", "mask-icon"}
EXTERNAL_PREFIX = ("http", "//", "data:", "#", "mailto:")


def _attr_ref(attrs: str):
    m = ATTR_VAL_RE.search(attrs)
    return m.group(1) if m else None


def load_time_refs(html: str, include_external: bool = False) -> list:
    """页面**加载时**就会下载的资源：link(stylesheet/icon/preload…)、script[src]、img[src]。

    `include_external=True` 时保留 http(s) 引用（供"外部依赖"检查用）——
    672d：`<a href="https://github.com/…">` 这种**引用/导航**链接不算外部依赖，
    只有真的会在加载时去下载的外部 script/css/img 才算（否则加了仓库链接就误报）。
    """
    out = []
    for tag, attrs in LOAD_TAGS_RE.findall(html):
        if tag.lower() == "link":
            rel = REL_RE.search(attrs)
            rels = set(rel.group(1).lower().split()) if rel else set()
            if not (rels & LOADABLE_REL):
                continue          # rel=alternate/canonical 之类不下载
        r = _attr_ref(attrs)
        if not r:
            continue
        if r.startswith(EXTERNAL_PREFIX) and not (include_external and r.startswith(("http://", "https://"))):
            continue
        out.append(r)
    return out


def nav_refs(html: str) -> list:
    """`<a href>`：导航链接，点一下才下载 —— **不算**首屏资源，只报告。"""
    out = []
    for attrs in NAV_A_RE.findall(html):
        r = _attr_ref(attrs)
        if r and not r.startswith(EXTERNAL_PREFIX):
            out.append(r)
    return out


def gz_len(path: str) -> int:
    with open(path, "rb") as fh:
        return len(gzip.compress(fh.read()))


def audit_page(pg: str) -> dict:
    f = os.path.join(WEB, pg + ".html")
    html = open(f, encoding="utf-8").read()
    issues = []
    refs = [r for r in REF_RE.findall(html) if not r.startswith(("http", "//", "data:", "#", "mailto:"))]

    html_kb = len(html.encode("utf-8")) / 1024
    if html_kb > BUDGET_HTML_KB:
        issues.append({"severity": "moderate", "rule": "html-size", "detail": f"HTML {html_kb:.1f}KB > {BUDGET_HTML_KB}KB"})

    dom = len(TAG_RE.findall(html))
    if dom > BUDGET_DOM_NODES:
        issues.append({"severity": "moderate", "rule": "dom-nodes", "detail": f"标签数 {dom} > {BUDGET_DOM_NODES}"})

    # 672d：只判**加载时**外部资源；`<a href="https://…">` 引用链接不算外部依赖
    ext_load = [r for r in load_time_refs(html, include_external=True)
                if r.startswith(("http://", "https://"))]
    if ext_load:
        issues.append({"severity": "moderate", "rule": "external",
                       "detail": f"加载时引用外部 http(s) 资源: {ext_load[:3]}"})

    # CSS 在 head
    head = html.split("</head>")[0] if "</head>" in html else html
    if "<style" in html.split("</head>")[-1]:
        issues.append({"severity": "moderate", "rule": "css-in-body", "detail": "body 内有 <style>"})
    if not re.search(r'<link[^>]+rel="stylesheet"', head):
        issues.append({"severity": "moderate", "rule": "css-head", "detail": "head 内无样式表链接"})

    # JS：模块/defer
    for m in re.finditer(r"<script([^>]*)>", html):
        attrs = m.group(1)
        if "src=" in attrs and "defer" not in attrs and 'type="module"' not in attrs:
            issues.append({"severity": "moderate", "rule": "js-blocking", "detail": f"阻塞脚本: {attrs.strip()[:60]}"})
            break

    # 图片 width/height
    for m in re.finditer(r"<img([^>]*)>", html):
        if "width=" not in m.group(1) or "height=" not in m.group(1):
            issues.append({"severity": "minor", "rule": "img-dim", "detail": "<img> 缺 width/height"})
            break

    # 残留调试
    for bad in ("console.log", "debugger"):
        if bad in html:
            issues.append({"severity": "moderate", "rule": "debug-residue", "detail": f"HTML 含 {bad}"})

    # 体积：672d B —— 只算**加载时资源**（导航链接不计入首屏预算）
    load = load_time_refs(html)
    nav = nav_refs(html)
    refs = load + nav            # 其余检查（外部依赖等）仍看全部引用，行为不变

    def sum_gz(items):
        tot = 0
        for r in items:
            p = os.path.normpath(os.path.join(WEB, r.split("?")[0]))
            if os.path.isfile(p):
                tot += gz_len(p)
        return tot

    gz = sum_gz(load) + gz_len(f)
    gz_legacy = sum_gz(refs) + gz_len(f)   # 旧口径（对照用，672e 可删）
    return {"page": pg + ".html", "html_kb": round(html_kb, 1), "dom_nodes": dom,
            "assets_gzip_kb": round(gz / 1024, 1),
            "assets_gzip_kb_legacy": round(gz_legacy / 1024, 1),
            "load_refs": load, "nav_refs": nav,
            "issues": issues,
            "counts": {s: sum(1 for i in issues if i["severity"] == s) for s in ("critical", "moderate", "minor")}}


def audit() -> dict:
    pages = [audit_page(p) for p in PAGES if os.path.isfile(os.path.join(WEB, p + ".html"))]
    # JS 残留调试
    js_residue = []
    SKIP_DIRS = ("dist", "node_modules", "vendor")
    SKIP_FILES = ("contrast_check.js",)   # Node CLI，console.log 属预期
    for dirpath, _, files in os.walk(WEB):
        if any(s in dirpath for s in SKIP_DIRS):
            continue
        for fn in files:
            if fn.endswith(".js") and fn not in SKIP_FILES:
                p = os.path.join(dirpath, fn)
                t = open(p, encoding="utf-8", errors="replace").read()
                if re.search(r"\bdebugger\b", t) or re.search(r"console\.log\(", t):
                    js_residue.append(os.path.relpath(p, WEB))
    home = next((p for p in pages if p["page"] == "index.html"), None)
    total = {s: sum(p["counts"][s] for p in pages) for s in ("critical", "moderate", "minor")}
    return {"pages": pages, "js_debug_residue": js_residue,
            "home_assets_gzip_kb": home["assets_gzip_kb"] if home else None,
            "home_assets_gzip_kb_legacy": home["assets_gzip_kb_legacy"] if home else None,
            "budget": {"html_kb": BUDGET_HTML_KB, "dom_nodes": BUDGET_DOM_NODES, "home_gzip_kb": BUDGET_HOME_GZIP_KB},
            # 672d B：口径声明写进产物，避免"57.5KB vs 24.9KB"被人误读成性能提升
            "gzip_scope": "load-time only（link/script/img；<a href> 导航链接不计入）",
            "total": total, "critical_total": total["critical"]}


def main() -> int:
    ap = argparse.ArgumentParser(description="前端性能静态审计（670c5 B1）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--out", default=OUT, help="输出路径（672d：默认 data/perf_audit_670c5.json）")
    args = ap.parse_args()
    res = audit()
    if args.write:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"[perf] 首页 gzip {res['home_assets_gzip_kb']}KB（预算 {BUDGET_HOME_GZIP_KB}KB）； 合计 {res['total']}")
        print(f"[perf] 口径：{res['gzip_scope']}")
        if res.get("home_assets_gzip_kb_legacy") is not None:
            print(f"[perf] 旧口径（含导航链接）对照：{res['home_assets_gzip_kb_legacy']}KB "
                  "—— 数字变小是**口径变对**，不是性能变好")
        for p in res["pages"]:
            print(f"  {p['page']:<16} html={p['html_kb']}KB dom={p['dom_nodes']} gzip={p['assets_gzip_kb']}KB {p['counts']}")
            for i in p["issues"]:
                if i["severity"] != "minor":
                    print(f"      [{i['severity'][:4]}] {i['rule']}: {i['detail']}")
        if res["js_debug_residue"]:
            print(f"  JS 调试残留: {res['js_debug_residue']}")
        print("[perf] " + ("PASS" if res["critical_total"] == 0 else "FAIL"))
    return 0 if res["critical_total"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
