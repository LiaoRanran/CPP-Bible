#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""a11y_audit_670c4.py — WCAG 2.1 AA 静态审计（670c4 A1）。

扫描 8 个 HTML 页面，检查：alt / label / 空链接 / table caption / heading 层级 /
唯一 h1 / 重复 id / lang / viewport / 可交互元素命名 / 表单控件关联。
输出 `data/a11y_audit_670c4.json`（每页问题清单 + 严重度）。

严重度：critical（缺 alt/label/名称，直接影响可用）> moderate（heading/结构）> minor（语义建议）。
只读 HTML，写 JSON。退出码：0 = 0 critical；1 = 有 critical。

672a E · 口径诚实化（**只加元数据，不改审计逻辑**）：
    本工具只 parse **静态 HTML 源码**；首页表格、卡库网格、实验页图表等由 JS 渲染的
    DOM 全在盲区。旧验收写"8 页 0 问题"是越界表述 —— 现在把覆盖率写进 JSON 与 stdout，
    让"0 问题"始终带着"覆盖了什么"一起读。
    升级到 jsdom 审计（真渲染后再扫）成本高，归后续批次。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "web")
OUT = os.path.join(ROOT, "data", "a11y_audit_670c4.json")
PAGES = ["index", "cards", "learn", "experiments", "verdicts", "starmap", "verify", "card"]

VOID = {"img", "input", "br", "hr", "meta", "link", "source", "area", "base", "col", "embed", "track", "wbr"}
# 需要无障碍名称的可交互元素
INTERACTIVE = {"button", "a", "qy-button", "qy-panel", "input", "select", "textarea"}

# ── 672a E · 覆盖率声明（写进 JSON 与 stdout，防止"0 问题"被读成"全站无问题"）──
COVERAGE = "static_html_only"
COVERAGE_STDOUT = "[a11y audit] coverage: static HTML only (JS-rendered DOM not audited)"
LIMITATIONS = [
    "仅审计静态HTML源码",
    "JS渲染的DOM（首页表格/卡库网格/实验页图表）未覆盖",
    "焦点环颜色需contrast_check辅助验证",
]


class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elems = []          # {tag, attrs(dict), text, line}
        self.stack = []          # indices of open elems
        self.ids = []
        self.headings = []
        self.noscript_depth = 0
        self.label_for = []      # <label for="..."> 的目标 id

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "noscript":
            self.noscript_depth += 1
        in_label = any(self.elems[i]["tag"] == "label" for i in self.stack)
        el = {"tag": tag, "attrs": a, "text": "", "line": self.getpos()[0],
              "in_noscript": self.noscript_depth > 0, "in_label": in_label}
        if tag == "label" and a.get("for"):
            self.label_for.append(a["for"])
        self.elems.append(el)
        idx = len(self.elems) - 1
        if "id" in a and a["id"]:
            self.ids.append(a["id"])
        if re.fullmatch(r"h[1-6]", tag):
            self.headings.append((tag, a.get("id", ""), el["line"]))
        if tag not in VOID:
            self.stack.append(idx)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.elems[self.stack[-1]]["tag"] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag == "noscript":
            self.noscript_depth = max(0, self.noscript_depth - 1)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.elems[self.stack[i]]["tag"] == tag:
                self.stack.pop(i)
                break

    def handle_data(self, data):
        t = data.strip()
        if not t:
            return
        for i in self.stack:
            self.elems[i]["text"] += " " + t


def accessible_name(el: dict) -> str:
    a = el["attrs"]
    for k in ("aria-label", "aria-labelledby", "title", "label", "alt"):
        if a.get(k):
            return a[k]
    return el.get("text", "").strip()


def audit_page(path: str) -> dict:
    html = open(path, encoding="utf-8").read()
    p = Collector()
    p.feed(html)
    issues = []

    def add(sev, rule, detail, line=None):
        issues.append({"severity": sev, "rule": rule, "detail": detail, "line": line})

    # 1. img alt
    for el in p.elems:
        if el["tag"] == "img" and "alt" not in el["attrs"]:
            add("critical", "img-alt", "<img> 缺 alt", el["line"])

    # 2. 可交互元素有名称（表单控件走 label 关联，其它走文本/aria-label）
    labelled_ids = set(p.label_for)

    def has_label(el):
        a = el["attrs"]
        if a.get("aria-label") or a.get("aria-labelledby") or a.get("title"):
            return True
        if el.get("in_label"):
            return True
        return bool(a.get("id") and a["id"] in labelled_ids)

    for el in p.elems:
        if el["tag"] in ("input", "select", "textarea"):
            if el["attrs"].get("type") in ("hidden",) or "hidden" in el["attrs"]:
                continue
            if not has_label(el):
                add("critical", "input-label",
                    f"<{el['tag']}> 无关联 <label> / aria-label", el["line"])
        elif el["tag"] in ("button", "a", "qy-button"):
            if not accessible_name(el):
                add("critical", "name", f"<{el['tag']}> 无可访问名称（文本/aria-label）", el["line"])

    # 4. 空链接
    for el in p.elems:
        if el["tag"] == "a":
            a = el["attrs"]
            if not accessible_name(el) and not a.get("aria-label"):
                add("critical", "empty-link", "<a> 无文本内容（空链接）", el["line"])
            if a.get("href", "").strip() in ("#", "javascript:void(0)", "javascript:;"):
                add("moderate", "link-as-button", f"<a href=\"{a.get('href')}\"> 当按钮用（应用 <button>）", el["line"])

    # 5. table caption / aria-label（逐表：caption 归属最近的上一张表）
    tables = [e for e in p.elems if e["tag"] == "table"]
    for i, el in enumerate(tables):
        nxt = tables[i + 1]["line"] if i + 1 < len(tables) else 10 ** 9
        has_caption = any(c["tag"] == "caption" and el["line"] < c["line"] < nxt for c in p.elems)
        if not (el["attrs"].get("aria-label") or el["attrs"].get("aria-labelledby") or has_caption):
            add("moderate", "table-caption", "<table> 缺 <caption> 或 aria-label", el["line"])

    # 6. heading 层级
    levels = [int(h[0][1]) for h in p.headings if not any(
        e["in_noscript"] for e in p.elems if e["line"] == h[2])]
    prev = 0
    for lv in levels:
        if prev and lv > prev + 1:
            add("moderate", "heading-skip", f"heading 从 h{prev} 跳到 h{lv}", None)
        prev = lv

    # 7. 唯一 h1（noscript 里的 h1 不算渲染层）
    h1s = [h for h in p.headings if h[0] == "h1"
           and not any(e["in_noscript"] for e in p.elems if e["line"] == h[2])]
    if len(h1s) == 0:
        add("moderate", "h1-missing", "页面无 <h1>")
    elif len(h1s) > 1:
        add("moderate", "h1-multiple", f"页面有 {len(h1s)} 个 <h1>（应仅 1 个）")

    # 8. 重复 id
    for idv, c in Counter(p.ids).items():
        if c > 1:
            add("critical", "dup-id", f"重复 id=\"{idv}\"（{c} 次）")

    # 9. lang
    if not re.search(r"<html[^>]*\blang=", html):
        add("critical", "lang", "<html> 缺 lang 属性")

    # 10. viewport
    if 'name="viewport"' not in html:
        add("moderate", "viewport", "缺 <meta name=viewport>")

    # 11. 跳过链接
    if "skip-link" not in html and 'href="#main"' not in html:
        add("moderate", "skip-link", "缺跳到主内容链接")

    # 12. 语义化建议
    if "<header" not in html:
        add("minor", "semantic-header", "建议用 <header> 包页面头部")
    if "<nav" not in html and "qy-nav" not in html:
        add("minor", "semantic-nav", "建议用 <nav> 包导航")
    if "<footer" not in html:
        add("minor", "semantic-footer", "建议用 <footer> 包页脚")

    return {"page": os.path.basename(path), "issues": issues,
            "counts": dict(Counter(i["severity"] for i in issues))}


def audit_all() -> dict:
    pages = []
    for pg in PAGES:
        f = os.path.join(WEB, pg + ".html")
        if os.path.isfile(f):
            pages.append(audit_page(f))
    total = Counter()
    for p in pages:
        for k, v in p["counts"].items():
            total[k] += v
    # 672a E：审计逻辑一字未改，只补元数据（覆盖率 / 局限）
    return {"pages": pages, "total": dict(total),
            "critical_total": total.get("critical", 0),
            "coverage": COVERAGE,
            "js_rendered_dom_audited": False,
            "limitations": list(LIMITATIONS)}


def main() -> int:
    ap = argparse.ArgumentParser(description="WCAG 2.1 AA 静态审计（670c4 A1）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    res = audit_all()
    if args.write:
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        # 672a E：覆盖率声明必须和"0 问题"一起被读到
        print(COVERAGE_STDOUT)
        print(f"[a11y] {len(res['pages'])} 页， 合计 {res['total']}， critical={res['critical_total']}")
        for p in res["pages"]:
            sev = p["counts"]
            print(f"  {p['page']:<16} {sev}")
            for i in p["issues"]:
                if i["severity"] == "critical":
                    print(f"      [CRIT] {i['rule']}: {i['detail']} (L{i['line']})")
        print("[a11y] " + ("PASS" if res["critical_total"] == 0 else "FAIL(critical>0)"))
    return 0 if res["critical_total"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
