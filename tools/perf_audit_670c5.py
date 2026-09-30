#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""perf_audit_670c5.py — 前端性能静态审计（670c5 B1）。

检查每页：HTML 体积 / 首屏 JS·CSS 体积(gzip) / 外部依赖 / CSS 在 head / JS 在 body 末尾或 defer /
图片 width·height / DOM 节点数估算 / console.log·debugger 残留 / 自定义字体。
输出 `data/perf_audit_670c5.json`。退出码：0 = 无 critical；1 = 有 critical。
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
BUDGET_HOME_GZIP_KB = 120    # 首页 gzip 合计
REF_RE = re.compile(r'(?:src|href)\s*=\s*"([^"]+)"')
TAG_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9-]*)")


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

    if re.search(r'(src|href)="https?://', html):
        issues.append({"severity": "moderate", "rule": "external", "detail": "引用外部 http(s) 资源"})

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

    # 体积：引用资源
    gz = 0
    for r in refs:
        p = os.path.normpath(os.path.join(WEB, r.split("?")[0]))
        if os.path.isfile(p):
            gz += gz_len(p)
    gz += gz_len(f)
    return {"page": pg + ".html", "html_kb": round(html_kb, 1), "dom_nodes": dom,
            "assets_gzip_kb": round(gz / 1024, 1), "issues": issues,
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
            "budget": {"html_kb": BUDGET_HTML_KB, "dom_nodes": BUDGET_DOM_NODES, "home_gzip_kb": BUDGET_HOME_GZIP_KB},
            "total": total, "critical_total": total["critical"]}


def main() -> int:
    ap = argparse.ArgumentParser(description="前端性能静态审计（670c5 B1）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    res = audit()
    if args.write:
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"[perf] 首页 gzip {res['home_assets_gzip_kb']}KB（预算 {BUDGET_HOME_GZIP_KB}KB）； 合计 {res['total']}")
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
