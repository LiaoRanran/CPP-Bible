#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""paper_sync_check_670c2.py — markdown ↔ LaTeX 数字一致性检查器（670c2 B1）。

把 `research/paper_v0.7.md`（中文稿）与 `research/latex/queyi_neurips2027.tex`（英文投稿稿）
里**同一批关键数字**逐一对照：任一在一边缺失即报错，并列出位置与差值线索。

只读，不写仓库。用法：
    python tools/paper_sync_check_670c2.py            # 人类可读报告
    python tools/paper_sync_check_670c2.py --json     # 机器可读
退出码：0 = 全部一致；1 = 存在不一致。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "research", "paper_v0.7.md")
TEX = os.path.join(ROOT, "research", "latex", "queyi_neurips2027.tex")

# (name, [tokens]) —— 每个 token 必须在两边都出现（token 已做规范化后的字面量）
FACTS: list[tuple[str, list[str]]] = [
    ("holdout 检出率", ["87.5", "14/16"]),
    ("holdout 95% CI", ["[61.7, 98.4]"]),
    ("external 全样本", ["35.0", "14/40"]),
    ("external 全样本 CI", ["[20.6, 51.7]"]),
    ("external 可测", ["43.8", "14/32"]),
    ("external 可测 CI", ["[26.4, 62.3]"]),
    ("对照 FPR", ["11.1", "1/9"]),
    ("口径消融 B 臂", ["82.4", "14/17"]),
    ("口径消融 C 臂 external", ["37.8", "14/37"]),
    ("口径差 Δ(A−C) external", ["8.8"]),
    ("实卡数", ["42"]),
    ("判决规则数", ["67"]),
    ("规则 severity", ["44", "16", "7"]),
    ("账本事件数", ["452"]),
    ("Merkle 目录数", ["5"]),
    ("变异 core", ["97.3", "110/113"]),
    # 注：v0.7 的 E3 表只列 core 变异（all=81.5% 属 v0.6 §6.4，压缩时未保留）⇒ 不入对账范围
    ("反事实 F1", ["1.0"]),
    ("反事实分母", ["10"]),
    ("演化 656 core", ["62.5", "30/48"]),
    ("演化 660 holdout", ["80.0"]),
    ("演化 665 holdout", ["66.7"]),
    ("演化 666 未落盘", ["81.2"]),
    ("semantic scope 完整度", ["0/26"]),
    ("边界卡数", ["26"]),
]


def normalize(text: str) -> str:
    """把两种排版归一，便于字面量比对。"""
    t = text.replace("\\%", "%")          # LaTeX 转义百分号
    t = t.replace("\\,", "").replace("~", " ")
    t = re.sub(r"\s+", " ", t)
    t = t.replace("（", "(").replace("）", ")")   # 全角括号
    t = t.replace("−", "-").replace("–", "-").replace("—", "-")
    return t


def load(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return normalize(fh.read())


def check() -> dict:
    md, tex = load(MD), load(TEX)
    rows = []
    for name, tokens in FACTS:
        miss_md = [t for t in tokens if t not in md]
        miss_tex = [t for t in tokens if t not in tex]
        rows.append({
            "fact": name,
            "tokens": tokens,
            "in_md": not miss_md,
            "in_tex": not miss_tex,
            "missing_in_md": miss_md,
            "missing_in_tex": miss_tex,
            "ok": not miss_md and not miss_tex,
        })
    bad = [r for r in rows if not r["ok"]]
    return {"checked": len(rows), "mismatches": len(bad), "rows": rows}


def main() -> int:
    ap = argparse.ArgumentParser(description="markdown↔LaTeX 数字一致性检查（670c2 B1）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    res = check()
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"[paper-sync] 检查 {res['checked']} 项， 不一致 {res['mismatches']} 项")
        for r in res["rows"]:
            mark = "OK " if r["ok"] else "BAD"
            print(f"  [{mark}] {r['fact']:<24} tokens={r['tokens']}")
            if r["missing_in_md"]:
                print(f"        - 缺失于 md : {r['missing_in_md']}")
            if r["missing_in_tex"]:
                print(f"        - 缺失于 tex: {r['missing_in_tex']}")
        print("[paper-sync] " + ("PASS" if res["mismatches"] == 0 else "FAIL"))
    return 0 if res["mismatches"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
