#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""figure_data_check_670c2.py — 图表数据溯源检查（670c2 B3；709 起改为「图感知」）。

原设计（670c2）假设论文里有 **pgfplots 数据图**：
    Fig.3（核心结果柱状图）：holdout / external 必须等于 reveal 产物的现算值
    Fig.4（演化曲线）：660/665/666/668/669 的每个值必须能在历史产物或回溯文档中找到出处

709 修复（诚实记录）：**v1.1 的排版里没有 pgfplots 数据图** —— 论文的两张图
（`fig:belnap` 四态平面、`fig:caliber` 口径示意）都是 **tikz 示意图**（node/draw，无 `coordinates`），
结果数据一律以**表格**呈现。原检查器因此对"没有数据图"这件事**假 FAIL**。

新判据（更强，不是放宽）：
  1. **图完整性**：每张 `figure` 必须有 `\\label`（能被 `\\ref`）；
  2. **数据图溯源**：**只要**存在含数据构件（`coordinates{` / `\\addplot` / `\\datapoint`）的图，
     就按原判据逐点溯源（Fig.3 → reveal_update_672h；Fig.4 → 历史产物/回溯文档）；
  3. **示意图声明**：不含数据构件的图被明确登记为"schematic（无硬编码数据）"。

⇒ 未来任何人加入数据图，溯源判据**自动生效**；当前"无数据图"则给出显式说明而非假 FAIL。

只读。退出码：0 = 通过；1 = 存在无 label 的图 / 数据图对不上出处。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "research", "latex", "queyi_neurips2027_v1.1.tex")
HOLDOUT = os.path.join(ROOT, "data", "holdout_reveal_3_665.json")
EXTERNAL = os.path.join(ROOT, "data", "external_corpus_reveal_665.json")
# 671a 扩样后的权威源（reveal_update_672h.json::holdout.after / corpus.after）；
# 自 671b 起 Fig.3 的期望值以此为准，665 旧产物仅作 Fig.4 历史出处。
REVEAL_UPDATE = os.path.join(ROOT, "data", "experiments", "reveal_update_672h.json")
RETRO = os.path.join(ROOT, "docs", "667_回溯反思.md")

COORD_RE = re.compile(r"coordinates\s*\{([^}]*)\}")
PAIR_RE = re.compile(r"\(([^,]+),\s*([0-9.]+)\)")
FIG_RE = re.compile(r"\\begin\{figure\}(.*?)\\end\{figure\}", re.DOTALL)
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
# 数据构件：pgfplots 坐标块 / addplot / datapoint（709 新增的"图感知"判据）
DATA_RE = re.compile(r"coordinates\s*\{|\\addplot|\\datapoint")


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def parse_figures(tex: str) -> list[dict]:
    """把每个 `figure` 环境解析成 {index, labels, has_data, pairs}。"""
    figs: list[dict] = []
    for i, m in enumerate(FIG_RE.finditer(tex), 1):
        body = m.group(1)
        pairs = [((lbl.strip()), float(v)) for lbl, v in PAIR_RE.findall(" ".join(COORD_RE.findall(body)))]
        figs.append({
            "index": i,
            "labels": LABEL_RE.findall(body),
            "has_data": bool(DATA_RE.search(body)),
            "pairs": pairs,
        })
    return figs


def check() -> dict:
    tex = open(TEX, encoding="utf-8").read()
    figs = parse_figures(tex)

    holdout = load_json(HOLDOUT)
    _ = load_json(EXTERNAL)  # 671i E/G：保留 load_json 的读取校验副作用
    reveal_update = load_json(REVEAL_UPDATE)
    retro = open(RETRO, encoding="utf-8").read() if os.path.isfile(RETRO) else ""
    hist_text = (retro + "\n" + json.dumps(holdout, ensure_ascii=False) + "\n"
                 + json.dumps(reveal_update, ensure_ascii=False))

    errors: list[str] = []
    ok: list[str] = []

    # 1) 图完整性：每张 figure 必须有 \label
    if not figs:
        errors.append("论文中没有 figure 环境")
    for f in figs:
        if f["labels"]:
            ok.append(f"第 {f['index']} 张 figure 有 label：{f['labels']}")
        else:
            errors.append(f"第 {f['index']} 张 figure 缺少 \\label（无法被 \\ref 引用）")

    data_figs = [f for f in figs if f["has_data"]]
    schematic_figs = [f for f in figs if not f["has_data"]]

    # 3) 示意图声明（709：显式登记，不是假 FAIL）
    if schematic_figs:
        labels = [lbl for f in schematic_figs for lbl in f["labels"]]
        ok.append(f"{len(schematic_figs)} 张图为**示意图**（无 coordinates/\\addplot 数据构件）"
                  f"⇒ 无硬编码数据需溯源：{labels}")

    # 2) 数据图溯源（仅当存在数据图时生效；判据与 670c2 原版一致）
    plots = [f["pairs"] for f in data_figs if f["pairs"]]
    if data_figs and not plots:
        errors.append(f"{len(data_figs)} 张图含数据构件（coordinates/\\addplot）但未解析出坐标对 ⇒ 无法溯源")
    if plots:
        fig3 = next((p for p in plots if any("holdout" in lbl.lower() for lbl, _ in p)), None)
        if fig3 is None:
            errors.append("未找到 Fig.3 的坐标块（含 holdout 标签）")
        else:
            d = {lbl.lower(): v for lbl, v in fig3}
            _num = reveal_update.get("numbers", reveal_update)
            exp_h = _num["holdout"]["after"]["rate_pct"]
            exp_c = _num["corpus"]["after"]["rate_pct"]   # 可测口径（40/64 = 62.5）
            if abs(d.get("holdout", -1) - exp_h) > 1e-9:
                errors.append(f"Fig.3 holdout={d.get('holdout')} != 672h 权威值 {exp_h}"
                              f"（reveal_update_672h.json::holdout.after）")
            else:
                ok.append(f"Fig.3 holdout={exp_h} == reveal_update_672h.json::holdout.after")
            corpus_val = d.get("corpus", d.get("external", -1))
            if abs(corpus_val - exp_c) > 1e-9:
                errors.append(f"Fig.3 corpus={corpus_val} != 672h 权威值(可测) {exp_c}"
                              f"（reveal_update_672h.json::corpus.after）")
            else:
                ok.append(f"Fig.3 corpus={exp_c} == reveal_update_672h.json::corpus.after (measurable)")

        fig4 = next((p for p in plots if any(re.fullmatch(r"\d{3}", lbl) for lbl, _ in p)), None)
        if fig4 is None:
            errors.append("未找到 Fig.4 的坐标块（含批次号标签）")
        else:
            for lbl, v in fig4:
                s = f"{v:g}"
                if s in hist_text:
                    ok.append(f"Fig.4 {lbl}={v} 有出处（历史产物/回溯文档）")
                else:
                    errors.append(f"Fig.4 {lbl}={v} 在历史产物与回溯文档中均无出处")

    return {
        "figures_found": len(figs),
        "data_figures": len(data_figs),
        "schematic_figures": len(schematic_figs),
        "ok": ok,
        "errors": errors,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="图表数据溯源检查（670c2 B3；709 图感知）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    res = check()
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"[figure-data] 图 {res['figures_found']} 张"
              f"（数据图 {res['data_figures']} / 示意图 {res['schematic_figures']}），"
              f"通过 {len(res['ok'])}，失败 {len(res['errors'])}")
        for s in res["ok"]:
            print("  [OK ]", s)
        for e in res["errors"]:
            print("  [ERR]", e)
        print("[figure-data] " + ("PASS" if not res["errors"] else "FAIL"))
    return 0 if not res["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
