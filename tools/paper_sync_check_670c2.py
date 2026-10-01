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
MD = os.path.join(ROOT, "research", "paper_v0.9.md")
TEX = os.path.join(ROOT, "research", "latex", "queyi_neurips2027.tex")

# (name, [tokens]) —— 每个 token 必须在两边都出现（token 已做规范化后的字面量）
# 语言分叉项用 (name, tokens_md, tokens_tex) 三元组：中文稿与英文稿用不同写法表达同一事实。
# 671b 第二批全量更新：旧值（87.5/14/16、43.8/14/32 等）按 reveal_update_671a.json 作废，
# 新值全部来自该产物的 pending_for_671b + 由此重算的三臂/统计量；历史值仅以"历史/作废"身份保留。
FACTS: list = [
    # ── 671a 扩样后主数字 ──
    ("holdout 检出率", ["81.0", "17/21"]),
    ("holdout 95% CI", ["[58.1, 94.5]"]),
    ("corpus 可测", ["54.2", "26/48"]),
    ("corpus 可测 CI", ["[39.2, 68.6]"]),
    ("corpus 全样本", ["43.3", "26/60"]),
    ("corpus 全样本 CI", ["[30.6, 56.8]"]),
    ("对照 FPR", ["18.2", "2/11"]),
    ("可测样本量", ["21/48"]),
    ("Δ CI 最低下界", ["25.7"]),
    # ── corpus 分层（fail-loud：无检测器层拒绝给率）──
    ("corpus sanitizer 层", ["79.2", "19/24"]),
    ("corpus compiler-warn 层", ["42.9", "6/14"]),
    ("corpus cross-compile 层", ["10.0", "1/10"]),
    # ── 口径消融（E3，671a 后重算）──
    ("口径消融 B 臂 holdout", ["77.3", "17/22"]),
    ("口径消融 B 臂 corpus", ["45.6", "26/57"]),
    ("口径差 Δ(A−C) holdout", ["3.7"]),
    ("口径差 Δ(A−C) corpus", ["10.8"]),
    ("669d 历史值作废注记", ["87.5/82.4/82.4"], ["87.5/82.4/82.4"]),
    # ── 实卡/规则/账本（不变）──
    ("实卡数", ["42"]),
    ("判决规则数", ["67"]),
    ("规则 severity", ["44", "16", "7"]),
    ("账本事件数", ["452"]),
    ("Merkle 目录数", ["5"]),
    ("变异 core", ["97.3", "110/113"]),
    ("反事实 F1", ["1.0"]),
    ("反事实分母", ["10"]),
    ("演化 656 core", ["62.5", "30/48"]),
    ("演化 660 holdout", ["80.0"]),
    ("演化 665 holdout", ["66.7"]),
    ("演化 666 未落盘", ["81.2"]),
    ("演化 669 holdout CI", ["[61.7, 98.4]"]),
    ("semantic scope 完整度", ["0/26"]),
    ("边界卡数", ["26"]),
    # ── 670g：baseline 三臂（671a 扩样后重算）──
    ("Static holdout", ["4.8", "1/21"]),
    ("Static corpus", ["14.6", "7/48"]),
    ("Static holdout CI", ["[0.1, 23.8]"]),
    ("Random† holdout", ["9.5", "2/21"]),
    ("Random† corpus", ["4.2", "2/48"]),
    ("Δ static→FD holdout", ["76.2"]),
    ("Δ static→FD corpus", ["39.6"]),
    ("Δ random†→FD holdout", ["71.4"]),
    ("Δ random†→FD corpus", ["50.0"]),
    ("缺陷重注入", ["6/6"]),
    # ── 671b：ablation 框架 + 样本量（来自 tools/sample_size_671b.py 现算）──
    ("ablation A0 占位", ["{{TODO_ablation_A0}}"]),
    ("ablation A5 占位", ["{{TODO_ablation_A5}}"]),
    ("ablation 关键对照 A0-A5", ["A0 - A5"]),
    ("样本量 ±10pp", ["104"]),
    ("样本量 Δ=15pp 配对", ["138"]),
    ("样本量 Δ=15pp 独立", ["170"]),
    # ── 统计检验（671a 扩样后四组；MD 用 Unicode 上标、tex 用 \times）──
    ("McNemar FD vs Static holdout", ["3.1×10⁻⁵"], ["3.1\\times10^{-5}"]),
    ("McNemar FD vs Static corpus", ["3.8×10⁻⁶"], ["3.8\\times10^{-6}"]),
    ("McNemar FD vs Random† holdout", ["6.1×10⁻⁵"], ["6.1\\times10^{-5}"]),
    ("McNemar FD vs Random† corpus", ["1.2×10⁻⁷"], ["1.2\\times10^{-7}"]),
    ("效应量 h holdout", ["1.80"]),
    ("效应量 h corpus", ["0.87"]),
    ("效应量 h random† holdout", ["1.61"]),
    ("效应量 h random† corpus", ["1.24"]),
    # 语言分叉：v0.8 的教训（0.72 应为"中"）两稿都保留为历史
    ("效应量历史教训 0.72", ["0.72", "中"], ["0.72", "medium"]),
    # ── 671b 第二批：新度量 VC / EE ──
    ("Verifier Coverage", ["73.8", "31/42"]),
    ("Verifier Coverage CI", ["[58.0, 86.1]"]),
    ("VC 域级缺口", ["0/8"]),
    ("EE 主口径", ["1.9pp"]),
    ("EE 变异变体", ["8.7pp"]),
    # 语言分叉：扩样无盲态标注
    ("扩样无盲态", ["无盲态"], ["unblinded"]),
]


def normalize(text: str) -> str:
    """把两种排版归一，便于字面量比对。"""
    t = text.replace("\\%", "%")          # LaTeX 转义百分号
    t = t.replace("\\{", "{").replace("\\}", "}")   # 转义花括号（占位符）
    t = t.replace("\\_", "_")             # 转义下划线（占位符）
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
    for fact in FACTS:
        if len(fact) == 2:
            name, tokens = fact
            t_md, t_tex = tokens, tokens
        else:
            name, t_md, t_tex = fact
        miss_md = [t for t in t_md if t not in md]
        miss_tex = [t for t in t_tex if t not in tex]
        rows.append({
            "fact": name,
            "tokens": [t_md, t_tex] if t_md != t_tex else t_md,
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
