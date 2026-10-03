#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""blindspot_676g_partial.py — 676g 任务 D：部分可见类型（盲区 20%-50%）的条件分析。

输入  data/blindspot_676g_stats.json + data/blindspot_676g_detection_matrix.json
输出  data/blindspot_676g_partial_visibility.json

每个部分可见类型输出：
  1. 数字画像：n / catch / miss / unknown / 盲区比例；各资产 catch 数与 catch 率。
  2. 能抓到的条件：哪个资产抓的（样本例证）、sanitizer 命中出现在 -O0 还是 -O2
     （从 detect note 的命中段解析）、compiler-warn 抓的告警文本形态。
  3. 抓不到的条件：miss 样本例证 + note（无报告 / 被优化掉 / 触发条件未满足…）。
  4. 互补性：该类型需要哪些资产组合（单资产覆盖 vs 并集覆盖的缺口）。
条件分析文本由脚本从矩阵 note 自动归集，人工复核后在报告 MD 里展开。
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STATS = HERE / "blindspot_676g_stats.json"
MATRIX = HERE / "blindspot_676g_detection_matrix.json"
OUT = HERE / "blindspot_676g_partial_visibility.json"

AVAILABLE = ["asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker"]

_OPT_HIT_RE = re.compile(r"(-O[02])\(rc=-?\d+\)")


def opt_hits(note: str) -> list[str]:
    """从 sanitizer 命中 note 解析命中发生在哪些档位（note 前 400 字符内）。"""
    head = note.split("]（档位")[0]          # 命中段在 ']' 前
    return sorted(set(_OPT_HIT_RE.findall(head)))


def main() -> int:
    st = json.loads(STATS.read_text(encoding="utf-8"))
    doc = json.loads(MATRIX.read_text(encoding="utf-8"))
    band = st["blindspot_bands"]["partial_visibility(20-50%)"]
    by_type_rows = {r["defect_type"]: r for r in st["by_type"]}

    out_types = []
    for t in band:
        row = by_type_rows[t]
        samples = [s for s in doc["samples"] if s["defect_type"] == t]
        # 每资产的命中例证与档位/告警形态
        catch_by_asset: dict[str, list] = defaultdict(list)
        miss_notes: list[dict] = []
        for s in samples:
            for a in AVAILABLE:
                cell = s["per_asset"].get(a, {})
                if cell.get("verdict") == "catch" and len(catch_by_asset[a]) < 3:
                    entry = {"uid": s["uid"], "note": cell.get("note", "")[:200]}
                    if a in ("asan", "ubsan", "tsan"):
                        entry["opt_levels_hit"] = opt_hits(cell.get("note", ""))
                    if a == "compiler-warn":
                        m = re.search(r"警告 (\d+) 条: (.*)", cell.get("note", ""))
                        if m:
                            entry["n_warnings"] = int(m.group(1))
                            entry["first_warning"] = m.group(2)[:120]
                    catch_by_asset[a].append(entry)
            if s["or_verdict_all8"] == "miss" and len(miss_notes) < 4:
                miss_notes.append({
                    "uid": s["uid"], "batch": s["source_batch"],
                    "asset_notes": {a: s["per_asset"].get(a, {}).get("note", "")[:150]
                                    for a in AVAILABLE
                                    if s["per_asset"].get(a, {}).get("verdict") == "miss"},
                })
        # 互补性：该类型里"仅被单一资产抓到"的样本比例
        single = multi = 0
        asset_solo_catch = defaultdict(int)
        for s in samples:
            caught = [a for a in AVAILABLE
                      if s["per_asset"].get(a, {}).get("verdict") == "catch"]
            if len(caught) == 1:
                single += 1
                asset_solo_catch[caught[0]] += 1
            elif len(caught) > 1:
                multi += 1
        out_types.append({
            "defect_type": t, "n": row["n"], "catch": row["catch"],
            "miss": row["miss"], "unknown": row["unknown"],
            "blindspot_ratio": row["blindspot_ratio"], "batches": row["batches"],
            "asset_catch": row["asset_catch"],
            "asset_catch_rate": row["asset_catch_rate"],
            "catch_by_asset_examples": dict(catch_by_asset),
            "miss_examples": miss_notes,
            "complementarity": {
                "caught_by_single_asset_only": single,
                "caught_by_multiple_assets": multi,
                "solo_catcher_counts": dict(asset_solo_catch),
                "union_gap": ("并集覆盖 = " + str(row["catch"]) + "/" + str(row["n"])
                              + "；单资产最高 = " + max(
                                  ((a, row["asset_catch"].get(a, 0)) for a in AVAILABLE),
                                  key=lambda kv: kv[1]).__repr__()),
            },
        })
    out_types.sort(key=lambda x: -x["blindspot_ratio"])

    doc_out = {
        "schema": "queyi-blindspot-partial-visibility/676g",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": {"stats": STATS.relative_to(ROOT).as_posix(),
                   "matrix": MATRIX.relative_to(ROOT).as_posix()},
        "caliber": "部分可见 = 盲区比例在 [20%, 50%] 的细粒度缺陷类型；"
                   "条件分析从判定矩阵 note 自动归集（sanitizer 档位 / 告警文本 / 互补覆盖），"
                   "叙述性结论见 676g_检测器盲区地图报告.md",
        "n_types": len(out_types),
        "types": out_types,
    }
    OUT.write_text(json.dumps(doc_out, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8", newline="\n")
    print(f"[676g] partial_visibility: {len(out_types)} 类型 → {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
