#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""figure_data_check_670c2.py — 图表数据溯源检查（670c2 B3）。

把 LaTeX 里 pgfplots 的**硬编码数字**与仓库**真实产物**比对：
  Fig.3（核心结果柱状图）：holdout / external 必须等于 reveal 产物的现算值
  Fig.4（演化曲线）：660/665/666/668/669 的每个值必须能在历史产物或回溯文档中找到出处

只读。退出码：0 = 全部可溯源；1 = 存在对不上/无出处的数字。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "research", "latex", "queyi_neurips2027.tex")
HOLDOUT = os.path.join(ROOT, "data", "holdout_reveal_3_665.json")
EXTERNAL = os.path.join(ROOT, "data", "external_corpus_reveal_665.json")
RETRO = os.path.join(ROOT, "docs", "667_回溯反思.md")

COORD_RE = re.compile(r"coordinates\s*\{([^}]*)\}")
PAIR_RE = re.compile(r"\(([^,]+),\s*([0-9.]+)\)")


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def parse_plots(tex: str) -> list[list[tuple[str, float]]]:
    plots = []
    for block in COORD_RE.findall(tex):
        pairs = [(lbl.strip(), float(v)) for lbl, v in PAIR_RE.findall(block)]
        if pairs:
            plots.append(pairs)
    return plots


def check() -> dict:
    tex = open(TEX, encoding="utf-8").read()
    plots = parse_plots(tex)

    holdout = load_json(HOLDOUT)
    external = load_json(EXTERNAL)
    retro = open(RETRO, encoding="utf-8").read() if os.path.isfile(RETRO) else ""
    hist_text = retro + "\n" + json.dumps(holdout, ensure_ascii=False)

    errors, ok = [], []

    # Fig.3 —— 找含 "holdout" 标签的坐标块
    fig3 = next((p for p in plots if any("holdout" in lbl.lower() for lbl, _ in p)), None)
    if fig3 is None:
        errors.append("未找到 Fig.3 的坐标块（含 holdout 标签）")
    else:
        d = {lbl.lower(): v for lbl, v in fig3}
        exp_h = holdout["error_subset"]["detect_rate_pct"]
        exp_e = external["rate_pct_all_samples"]
        if abs(d.get("holdout", -1) - exp_h) > 1e-9:
            errors.append(f"Fig.3 holdout={d.get('holdout')} != 产物 {exp_h}")
        else:
            ok.append(f"Fig.3 holdout={exp_h} == holdout_reveal_3_665.json")
        if abs(d.get("external", -1) - exp_e) > 1e-9:
            errors.append(f"Fig.3 external={d.get('external')} != 产物 {exp_e}")
        else:
            ok.append(f"Fig.3 external={exp_e} == external_corpus_reveal_665.json")

    # Fig.4 —— 找含批次标签(660/665/...)的坐标块
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

    return {"plots_found": len(plots), "ok": ok, "errors": errors}


def main() -> int:
    ap = argparse.ArgumentParser(description="图表数据溯源检查（670c2 B3）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    res = check()
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"[figure-data] 坐标块 {res['plots_found']} 个， 通过 {len(res['ok'])}， 失败 {len(res['errors'])}")
        for s in res["ok"]:
            print("  [OK ]", s)
        for e in res["errors"]:
            print("  [ERR]", e)
        print("[figure-data] " + ("PASS" if not res["errors"] else "FAIL"))
    return 0 if not res["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
