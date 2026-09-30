#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""anonymity_check_670c2.py — 投稿匿名化持续检查（670c2 B4）。

双层黑名单：
  STRICT（全文任何位置都禁止）：姓名 / 邮箱 / GitHub 用户名 / 机构名
  MAIN_ONLY（主文禁止，附录白名单允许）：仓库名 / 拆仓名 / 本地绝对路径 / 仓库相对路径

主文 = `\\appendix` 之前的文本；附录 D 的复现命令按任务约定白名单放行。
退出码：0 = 主文 0 命中；1 = 有命中。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "research", "latex", "queyi_neurips2027.tex")

# 全文禁止
STRICT = [
    r"LiaoRanran",
    r"1026708211@qq\.com",
    r"ranzhif2138@gmail\.com",
    r"github\.com/LiaoRanran",
    r"hfuu",
    r"合肥大学",
    r"阿信",
]
# 仅主文禁止（附录允许）
MAIN_ONLY = [
    r"CPP-Bible",
    r"queyi-verifier",
    r"C:\\CodeLearnling",
    r"(?<![\w/])data/",
    r"(?<![\w/])tools/",
    r"(?<![\w/])docs/",
    r"(?<![\w/])research/",
]


def split_main(tex: str) -> str:
    idx = tex.find("\\appendix")
    return tex if idx == -1 else tex[:idx]


def scan() -> dict:
    tex = open(TEX, encoding="utf-8").read()
    main = split_main(tex)
    hits = []

    for pat in STRICT:
        for m in re.finditer(pat, tex):
            line = tex.count("\n", 0, m.start()) + 1
            hits.append({"scope": "STRICT(anywhere)", "pattern": pat, "line": line,
                         "match": m.group(0)})
    for pat in MAIN_ONLY:
        for m in re.finditer(pat, main):
            line = main.count("\n", 0, m.start()) + 1
            hits.append({"scope": "MAIN_ONLY(main text)", "pattern": pat, "line": line,
                         "match": m.group(0)})

    return {"hits": hits, "strict_hits": sum(1 for h in hits if h["scope"].startswith("STRICT")),
            "main_hits": sum(1 for h in hits if h["scope"].startswith("MAIN"))}


def main() -> int:
    ap = argparse.ArgumentParser(description="投稿匿名化检查（670c2 B4）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    res = scan()
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"[anonymity] STRICT 命中 {res['strict_hits']}， MAIN 命中 {res['main_hits']}")
        for h in res["hits"]:
            print(f"  [HIT] {h['scope']} line {h['line']}: /{h['pattern']}/ -> {h['match']!r}")
        print("[anonymity] " + ("PASS" if not res["hits"] else "FAIL"))
    return 0 if not res["hits"] else 1


if __name__ == "__main__":
    sys.exit(main())
