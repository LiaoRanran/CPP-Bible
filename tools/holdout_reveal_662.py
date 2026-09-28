#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""holdout_reveal_662.py — 662 A2：标签修正后的第二次 reveal（reveal_2）。

不同点（相对 661 B1）：
  - 分母改用修正后的 planted=true 子集（7 个），而不是全部 20 个；
  - 对照子集（planted=false，9 个）上检出器报错 → 记 **false_positive**；
  - 与 reveal_1 逐样本对比，量化"标签修正带来多少数字变化"。

复用 tools/holdout_reveal_661.py 的检测器（detect/PLAN），不自造第二套。
铁律：不回盲（.revealed 保留）；本文件是 reveal_2 报告，不修改 holdout 盲态。
输出：data/holdout_reveal_2_662.json
"""
from __future__ import annotations

import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
HOLD = os.path.join(ROOT, "data", "holdout", "holdout.json")
R1 = os.path.join(ROOT, "data", "holdout_reveal_1_661.json")
OUT = os.path.join(ROOT, "data", "holdout_reveal_2_662.json")


def _load_rv661():
    spec = importlib.util.spec_from_file_location("rv661", os.path.join(HERE, "holdout_reveal_661.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main() -> int:
    rv = _load_rv661()
    h = json.load(open(HOLD, encoding="utf-8"))
    r1 = json.load(open(R1, encoding="utf-8")) if os.path.isfile(R1) else {"results": []}
    r1_map = {x["id"]: x for x in r1.get("results", [])}

    results = []
    # 真错子集的混淆矩阵
    err_total = err_catch = err_miss = err_unknown = 0
    # 对照子集上的误报
    ctrl_total = ctrl_fp = 0
    unknown_label = 0
    changes = []
    for s in h["seeds"]:
        kind, files = rv.PLAN.get(s["id"], ("unknown", []))
        verdict, note = rv.detect(kind, files)
        lab = s.get("planted")
        if lab is True:
            err_total += 1
            if verdict == "catch":
                err_catch += 1
            elif verdict == "miss":
                err_miss += 1
            else:
                err_unknown += 1
        elif lab is False:
            ctrl_total += 1
            if verdict == "catch":
                ctrl_fp += 1
        else:
            unknown_label += 1
        prev = r1_map.get(s["id"], {}).get("verdict")
        if prev != verdict:
            changes.append({"id": s["id"], "reveal_1": prev, "reveal_2": verdict})
        results.append({"id": s["id"], "planted": lab, "detector": kind,
                        "verdict": verdict, "note": note})

    det_rate = (err_catch / (err_catch + err_miss) * 100) if (err_catch + err_miss) else 0.0
    rep = {
        "schema": "queyi-holdout-reveal/v2",
        "reveal_index": 2,
        "revealed_at": "2026-09-28",
        "generated_by": "tools/holdout_reveal_662.py",
        "based_on": "661 B1 标签经 662 A1 人工复核修正",
        "labels": {"error": err_total, "control": ctrl_total, "unknown": unknown_label},
        "error_subset": {"catch": err_catch, "miss": err_miss, "unknown": err_unknown,
                         "detect_rate_pct": round(det_rate, 1)},
        "control_subset": {"false_positive": ctrl_fp, "total": ctrl_total},
        "compare_reveal_1": {
            "changed_verdicts": changes,
            "note": ("reveal_1 把全部 20 个当出错样本 → catch=7/miss=9/unknown=4；"
                     "reveal_2 以修正标签分母（真错 7）统计 → 检出率见 error_subset。"
                     "miss 的大部分是对照/边界类，'不报'是正确行为。"),
        },
        "detectors": rv.__dict__.get("SAN", {}),
        "results": results,
    }
    json.dump(rep, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"真错子集({err_total}): catch={err_catch} miss={err_miss} unknown={err_unknown} "
          f"→ 检出率={rep['error_subset']['detect_rate_pct']}%")
    print(f"对照子集({ctrl_total}): false_positive={ctrl_fp}")
    print(f"unknown 标签={unknown_label}")
    print(f"与 reveal_1 判定变化：{changes}")
    print(f"已写 {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
