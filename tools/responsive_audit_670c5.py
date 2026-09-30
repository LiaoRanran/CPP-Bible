#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""responsive_audit_670c5.py — 响应式静态审计（670c5 A1）。

**静态**分析 8 个 HTML + 全部 CSS，检查响应式要素（无浏览器 ⇒ 不做真实渲染）：
  viewport / box-sizing / overflow-x / 表格滚动容器 / grid auto-fit / 媒体查询 /
  触控目标 / 图片 max-width / 弹窗窄屏 / 断点统一。

输出 `data/responsive_audit_670c5.json`。退出码：0 = 0 严重；1 = 有严重。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "web")
OUT = os.path.join(ROOT, "data", "responsive_audit_670c5.json")
PAGES = ["index", "cards", "learn", "experiments", "verdicts", "starmap", "verify", "card"]
BREAKPOINTS = {"sm": 640, "md": 768, "lg": 1024, "xl": 1280}
CSS_FILES = ["style.css", "css/design-tokens.css", "css/669c.css", "css/robustness.css",
             "css/a11y.css", "css/responsive.css"]


def load_css() -> str:
    parts = []
    for rel in CSS_FILES:
        p = os.path.join(WEB, rel)
        if os.path.isfile(p):
            parts.append(open(p, encoding="utf-8").read())
    return "\n".join(parts)


def audit() -> dict:
    css = load_css()
    pages, issues = [], []

    # 全局 CSS 要素
    global_checks = {
        "box-sizing": bool(re.search(r"box-sizing\s*:\s*border-box", css)),
        "overflow-x 处理": bool(re.search(r"overflow-x\s*:\s*(auto|hidden|scroll)", css)),
        "grid auto-fit/minmax": bool(re.search(r"(auto-fit|auto-fill|minmax\()", css)),
        "表格滚动容器": bool(re.search(r"(table-scroll|\.table-wrap|overflow-x\s*:\s*auto)", css)),
        "图片 max-width:100%": bool(re.search(r"(img|canvas|svg)[^{]*\{[^}]*max-width\s*:\s*100%", css)),
        "触控目标 ≥44px": bool(re.search(r"min-(height|width)\s*:\s*(44|48)px", css)),
        "弹窗 max-width": bool(re.search(r"\.qy-dialog-box[^{]*\{[^}]*max-width", css)),
        "reduced-motion": bool(re.search(r"prefers-reduced-motion", css)),
    }
    for k, v in global_checks.items():
        if not v:
            issues.append({"severity": "moderate", "scope": "global", "rule": k, "detail": f"CSS 未见 {k} 相关规则"})

    # 断点统一（媒体查询宽度是否落在 sm/md/lg/xl）
    widths = sorted({int(w) for w in re.findall(r"@media[^{]*?(\d{3,4})px", css)})
    offgrid = [w for w in widths if w not in BREAKPOINTS.values() and w not in (320, 375, 414, 480, 600, 900)]
    if offgrid:
        issues.append({"severity": "minor", "scope": "global", "rule": "断点统一",
                       "detail": f"非标准断点: {offgrid}（建议 sm640/md768/lg1024/xl1280）"})

    # 每页
    for pg in PAGES:
        f = os.path.join(WEB, pg + ".html")
        if not os.path.isfile(f):
            continue
        html = open(f, encoding="utf-8").read()
        p_issues = []
        if 'name="viewport"' not in html:
            p_issues.append({"severity": "critical", "rule": "viewport", "detail": "缺 viewport meta"})
        if not re.search(r"<html[^>]*lang=", html):
            p_issues.append({"severity": "moderate", "rule": "lang", "detail": "缺 lang"})
        # 表格是否有滚动容器
        if "<table" in html and not re.search(r'(table-scroll|overflow-x|\.table-wrap)', html + css):
            p_issues.append({"severity": "moderate", "rule": "表格滚动", "detail": "有表格但未见滚动容器"})
        # 外部资源
        if re.search(r'(src|href)="https?://', html):
            p_issues.append({"severity": "moderate", "rule": "外部依赖", "detail": "引用了外部 http(s) 资源"})
        for i in p_issues:
            i["page"] = pg + ".html"
        issues.extend(p_issues)
        pages.append({"page": pg + ".html", "issues": p_issues,
                      "counts": {s: sum(1 for i in p_issues if i["severity"] == s) for s in ("critical", "moderate", "minor")}})

    total = {s: sum(1 for i in issues if i["severity"] == s) for s in ("critical", "moderate", "minor")}
    return {"pages": pages, "global": global_checks, "media_query_widths": widths,
            "total": total, "critical_total": total["critical"]}


def main() -> int:
    ap = argparse.ArgumentParser(description="响应式静态审计（670c5 A1）")
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
        print(f"[responsive] 8 页； 合计 {res['total']}； 媒体查询宽度 {res['media_query_widths']}")
        for k, v in res["global"].items():
            print(f"  [{'OK ' if v else 'MISS'}] {k}")
        for i in res.get("pages", []):
            for it in i["issues"]:
                print(f"  [{it['severity'][:4]}] {i['page']}: {it['rule']} - {it['detail']}")
        print("[responsive] " + ("PASS" if res["critical_total"] == 0 else "FAIL"))
    return 0 if res["critical_total"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
