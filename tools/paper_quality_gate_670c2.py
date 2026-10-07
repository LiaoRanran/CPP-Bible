#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""paper_quality_gate_670c2.py — 论文质量门禁（670c2 B5）。

检查项：
  1. 主文页数 ≤ 9（读 `.aux` 的 `page:endmain` 标签；缺 .aux 则跳过并提示先 build）
  2. 0 未定义引用（读 `.log` 的 `undefined`；缺 .log 则跳过）
  3. 0 未定义图表引用（同上）
  4. 所有 `\\section` 都有 `\\label`
  5. 所有 `\\ref` 都有对应 `\\label`
  6. 摘要 ≤ 250 词
  7. 无 TODO/FIXME/HACK 残留（已知占位放行：`\\TODO{670a}` 宏，以及**已登记的** `{{TODO_ablation_*}}`
     占位——登记来源 `data/experiments/ablation_plan_671b.json`；未登记的 `{{TODO_*}}` 仍判失败）

只读。退出码：0 = 全通过；1 = 有失败项。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LATEX = os.path.join(ROOT, "research", "latex")
TEX = os.path.join(LATEX, "queyi_neurips2027_v1.1.tex")
AUX = os.path.join(LATEX, "queyi_neurips2027_v1.1.aux")
LOG = os.path.join(LATEX, "queyi_neurips2027_v1.1.log")
ABLATION_PLAN = os.path.join(ROOT, "data", "experiments", "ablation_plan_671b.json")

MAIN_PAGE_LIMIT = 9
ABSTRACT_WORD_LIMIT = 250


def registered_placeholders() -> set[str]:
    """从 ablation 计划产物读出**已登记**的占位符；读不到则返回空集（更严格）。"""
    try:
        with open(ABLATION_PLAN, encoding="utf-8") as fh:
            plan = json.load(fh)
    except (OSError, ValueError):
        return set()
    names: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
        elif isinstance(node, str) and node.startswith("{{TODO_") and node.endswith("}}"):
            names.add(node)

    walk(plan)
    return names


def run() -> dict:
    tex = open(TEX, encoding="utf-8").read()
    checks = []

    def add(name, ok, detail, skipped=False):
        checks.append({"check": name, "ok": bool(ok), "skipped": skipped, "detail": detail})

    # 1. 主文页数
    if os.path.isfile(AUX):
        aux = open(AUX, encoding="utf-8").read()
        m = re.search(r"\\newlabel\{page:endmain\}\{\{[^}]*\}\{(\d+)\}", aux)
        if m:
            pages = int(m.group(1))
            add("主文页数≤9", pages <= MAIN_PAGE_LIMIT, f"page:endmain -> {pages} 页")
        else:
            add("主文页数≤9", False, "aux 中未找到 page:endmain 标签")
    else:
        add("主文页数≤9", True, "缺 .aux（先运行 build）—— 跳过", skipped=True)

    # 2/3. 未定义引用（从 log）
    if os.path.isfile(LOG):
        log = open(LOG, encoding="utf-8", errors="replace").read()
        undef = re.findall(r"LaTeX Warning: (Citation|Reference) `([^']+)' .*undefined", log)
        add("0 未定义引用", len(undef) == 0, f"undefined 条目 {len(undef)}")
    else:
        add("0 未定义引用", True, "缺 .log —— 跳过", skipped=True)

    # 4. 所有 \section 有 \label（只对主文，即 \appendix 前）
    main_tex = tex.split("\\appendix")[0]
    main_sections = re.findall(r"\\section\*?\{([^}]*)\}(.{0,140})", main_tex, flags=re.DOTALL)
    missing_label = []
    for name, tail in main_sections:
        if "\\label{" not in tail.split("\\section")[0]:
            missing_label.append(name.strip())
    add("所有 \\section 有 \\label", not missing_label,
        f"缺 label 的 section: {missing_label}" if missing_label else f"{len(main_sections)} 个 section 均有 label")

    # 5. \ref 均有 \label
    labels = set(re.findall(r"\\label\{([^}]+)\}", tex))
    refs = set(re.findall(r"\\ref\{([^}]+)\}", tex))
    dangling = sorted(refs - labels)
    add("所有 \\ref 有 \\label", not dangling,
        f"悬空 ref: {dangling}" if dangling else f"{len(refs)} 个 ref 全部有 label")

    # 6. 摘要词数
    am = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, flags=re.DOTALL)
    if am:
        words = len(re.findall(r"[A-Za-z][A-Za-z\-']*", am.group(1)))
        add("摘要≤250词", words <= ABSTRACT_WORD_LIMIT, f"摘要英文词数 = {words}")
    else:
        add("摘要≤250词", False, "未找到 abstract 环境")

    # 7. TODO/FIXME/HACK（放行 \TODO{670a} 宏 与 已登记的 {{TODO_ablation_*}} 占位）
    stripped = re.sub(r"\\newcommand\{\\TODO\}\[1\]\{[^\n]*\}", "", tex)  # 去掉宏定义本身
    stripped = re.sub(r"\\TODO\{[^}]*\}", "", stripped)                   # 去掉已知占位 \TODO{670a}
    # LaTeX 里占位写成 \{\{TODO\_ablation\_A0\}\}：先反解义，再与登记表比对
    stripped = stripped.replace("\\{", "{").replace("\\}", "}").replace("\\_", "_")
    registered = registered_placeholders()
    seen_placeholders = set(re.findall(r"\{\{TODO_[A-Za-z0-9_]*\}\}", stripped))
    unregistered = sorted(seen_placeholders - registered) if registered else sorted(seen_placeholders)
    for ph in registered:                                                 # 只放行已登记的
        stripped = stripped.replace(ph, "")
    todos = re.findall(r"\b(TODO|FIXME|HACK)\b", stripped)
    ok7 = not todos and not unregistered
    detail = f"仅已登记占位（TODO{{670a}} 宏 + {len(registered & seen_placeholders)} 个 ablation 占位）"
    if unregistered:
        detail = f"发现未登记占位: {unregistered}"
    elif todos:
        detail = f"发现 {len(todos)} 处: {sorted(set(todos))}"
    add("无 TODO/FIXME/HACK 残留", ok7, detail)

    failed = [c for c in checks if not c["ok"]]
    return {"checks": checks, "failed": len(failed),
            "skipped": sum(1 for c in checks if c["skipped"])}


def main() -> int:
    ap = argparse.ArgumentParser(description="论文质量门禁（670c2 B5）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    res = run()
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"[paper-gate] {len(res['checks'])} 项检查， 失败 {res['failed']}， 跳过 {res['skipped']}")
        for c in res["checks"]:
            mark = "SKIP" if c["skipped"] else ("OK " if c["ok"] else "FAIL")
            print(f"  [{mark}] {c['check']:<22} {c['detail']}")
        print("[paper-gate] " + ("PASS" if not res["failed"] else "FAIL"))
    return 0 if not res["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
