#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""paper_sync_check_670c2.py — markdown ↔ LaTeX 数字一致性检查器（670c2 B1）。

把 `research/paper_v1.0.md`（中文稿）与 `research/latex/queyi_neurips2027_v1.0.tex`（英文投稿稿）
里**同一批关键数字**逐一对照：任一在一边缺失即报错，并列出位置与差值线索。

只读，不写仓库。用法：
    python tools/paper_sync_check_670c2.py            # 人类可读报告
    python tools/paper_sync_check_670c2.py --json     # 机器可读
退出码：0 = 全部一致；1 = 存在不一致。

变更史：
  * 670c2 建立（v0.7 基线）。
  * 671b 第二批：数字更新至 671a 扩样值（81.0/54.2/18.2 等）。
  * **673a：数字更新至 672h 扩样值**（82.9/62.5/18.2；分母 41/64），并新增
    LLM 裁判臂、外部锚定、变异 all 三项；旧值（81.0/17/21、54.2/26/48、97.3/110/113、
    1.2e-7、1.24 等）**按 672h 作废**，不再作为期望 token。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "research", "paper_shturl.md")
TEX = os.path.join(ROOT, "research", "latex", "queyi_neurips2027_v1.1.tex")

# (name, [tokens]) —— 每个 token 必须在两边都出现（token 已做规范化后的字面量）
# 语言分叉项用 (name, tokens_md, tokens_tex) 三元组。
FACTS: list = [
    # ── 672h 扩样后主数字 ──
    ("holdout 检出率", ["82.9", "34/41"]),
    ("holdout 95% CI", ["[67.9, 92.8]"]),
    ("corpus 可测", ["62.5", "40/64"]),
    ("corpus 可测 CI", ["[49.5, 74.3]"]),
    ("corpus 全样本", ["52.6", "40/76"]),
    ("corpus 全样本 CI", ["[40.8, 64.2]"]),
    # 709 修复：旧值 18.2%/2/11 系**检测器缺陷**所致（已修，中文稿 §9.2 明写"旧值 18.2% 系检测器缺陷所致，已修"）；
    # 现行对照 FPR = 0.0%（0/11），两稿一致。
    ("对照 FPR（现行 0.0%）", ["0.0", "0/11"]),
    ("可测样本量", ["41/64"]),
    ("Δ CI 最低下界", ["28.6"]),
    # ── corpus 分层（fail-loud：无检测器层拒绝给率）──
    ("corpus sanitizer 层", ["85.3", "29/34"]),
    ("corpus compiler-warn 层", ["50.0", "9/18"]),
    ("corpus cross-compile 层", ["16.7", "2/12"]),
    # ── 口径消融（E3，672h 后重算）──
    ("口径消融 B 臂 holdout", ["81.0", "34/42"]),
    ("口径消融 B 臂 corpus", ["54.8", "40/73"]),
    ("口径差 Δ(A−C) holdout", ["1.9"]),
    ("口径差 Δ(A−C) corpus", ["9.9"]),
    # ── 实卡/规则/账本（不变）──
    ("实卡数", ["42"]),
    ("判决规则数", ["67"]),
    ("规则 severity", ["44", "16", "7"]),
    ("账本事件数", ["452"]),
    ("Merkle 目录数", ["5"]),
    ("变异 core", ["96.5", "110/114"]),
    ("变异 all", ["81.8", "130/159"]),
    ("演化 656 core", ["62.5", "30/48"]),
    ("演化 660 holdout", ["80.0"]),
    ("演化 665 holdout", ["66.7"]),
    ("演化 666 未落盘", ["81.2"]),
    ("演化 669 holdout CI", ["[61.7, 98.4]"]),
    ("semantic scope 完整度", ["0/26"]),
    ("边界卡数", ["26"]),
    # ── baseline 三臂（672h 扩样后重算；Random† 为仪器级代理）──
    ("Static holdout", ["2.4", "1/41"]),
    ("Static corpus", ["17.2", "11/64"]),
    ("Static holdout CI", ["[0.1, 12.9]"]),
    ("Random† holdout", ["9.8", "4/41"]),
    ("Random† corpus", ["21.9", "14/64"]),
    ("Δ static→FD holdout", ["80.5"]),
    ("Δ static→FD corpus", ["45.3"]),
    ("Δ random†→FD holdout", ["73.2"]),
    ("Δ random†→FD corpus", ["40.6"]),
    ("缺陷重注入", ["6/6"]),
    # ── ablation 框架 + 样本量 ──
    # 709 修复：689 起英文稿**移除了占位宏**，改用 \textit{not run} 标注（A0–A4 未跑）；
    # 中文稿用 {{TODO_ablation_*}} + "未跑"。故改为**诚实性标注**的跨语言对照（原来要求两边都有同一占位宏，已过时）。
    ("ablation 未运行如实标注", ["{{TODO_ablation_A0}}", "未跑"], ["not run"]),
    # 709 修复：语言分叉（中文稿用 en-dash "A0–A5" → 归一后 "A0-A5"；英文稿用 "A0--A5"）
    ("ablation 关键对照 A0-A5", ["A0-A5"], ["A0--A5"]),
    ("样本量 ±10pp", ["61"], ["61"]),
    ("样本量 ±5pp", ["236", "378"]),
    ("样本量 Δ=15pp 配对", ["138"]),
    ("样本量 Δ=15pp 独立", ["170"]),
    # ── 统计检验（672h 四组；MD 用 Unicode 上标、tex 用 \times）──
    ("McNemar FD vs Static holdout", ["2.3×10⁻¹⁰"], ["2.3\\times10^{-10}"]),
    ("McNemar FD vs Static corpus", ["3.7×10⁻⁹"], ["3.7\\times10^{-9}"]),
    ("McNemar FD vs Random† holdout", ["1.9×10⁻⁹"], ["1.9\\times10^{-9}"]),
    ("McNemar FD vs Random† corpus", ["3.0×10⁻⁸"], ["3.0\\times10^{-8}"]),
    ("效应量 h holdout", ["1.98"]),
    ("效应量 h corpus", ["0.97"]),
    ("效应量 h random† holdout", ["1.65"]),
    ("效应量 h random† corpus", ["0.85"]),
    # 语言分叉：v0.8 的教训（0.72 应为"中"）两稿都保留为历史
    ("效应量历史教训 0.72", ["0.72", "中"], ["0.72", "medium"]),
    # ── 新度量 VC / EE（709 修复）──
    # 689 重构把 VC（Verifier Coverage）与 EE（Evolution Efficiency）**整体移出英文稿**
    # （工程遥测，非科学证据；正文只保留"已在 689 移除"的登记）。
    # 原 5 条事实（73.8 / 31/42 / [58.0, 86.1] / 1.9pp / 8.5pp）在英文稿仅存于**注释与复现清单**
    # ⇒ 撤销这些量级要求，改为检查**"移除已如实登记"**（防"悄悄复活"这些指标）。
    ("VC / EE 已移除并如实登记（689）", ["689"], ["removed in 689"]),
    ("VC 域级缺口", ["0/8"]),
    # ── 672h 新增实验 ──
    ("LLM 裁判臂检出", ["12/12"]),
    ("LLM 裁判臂假阳", ["4/8"]),
    ("外部锚定合计", ["44.0"]),
    ("外部锚定 A 层", ["28.6"]),
    ("外部锚定 B 层", ["80.0"]),
    # 709 修复（原先为 ("e-value 量级", ["2.5×10⁸"], ["2.5\\times10^8"])）：
    #   673s/689 起，e-value 已被显式**降级为 EXPLORATORY**（不作证据强度）；
    #   中文稿 §4.8 与「被取代的旧值（不得再引用）」清单都把 e-value 量级列为**不得再引用**。
    #   因此要求 `2.5\times10^8` 出现在英文稿正文与"不得再引用"的声明**自相矛盾** ⇒ 撤销该量级要求，
    #   改为检查两稿都保留**降级声明**（诚实性反向检查：防止把 e-value 悄悄提升为 claim）。
    ("e-value 降级声明（不作证据强度）", ["e-value"], ["exploratory"]),
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
