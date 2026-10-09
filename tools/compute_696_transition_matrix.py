#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_696_transition_matrix.py — 三态转移矩阵（Measurement Drift Algebra, 696-A3）。

把 692 的**配对环境实验**（E1 `wsl-gcc-13.3` vs E2 `windows-native-mingw`）在
`catch / miss / unknown` 三态上算成 3x3 转移矩阵，并给出两种记账口径：

  * `unaware`（论文 F3 的"静默"口径）：E2 未运行的资产被记为 miss ⇒ 转移矩阵第三列
    （→unknown）恒为 0，**丢失的 catch 全部伪装成 miss**。
  * `aware`（四态纪律口径）：E2 未运行的资产记为 unknown ⇒ 同一批测量，结论从
    "能力下降"变成"未测量"。

**关键性质（本脚本要验证的）**：`unaware` 与 `aware` 的**原始测量完全相同**，只有
`caliber` 变了；因此三态转移矩阵是"结构性（被动）Goodhart"的一个可计算实例——
不需要任何优化压力，口径变化本身就产生测量漂移。

数据来源（**只读**，不调用 `detect()`）：
  * `data/692_environment_paired_experiment.json` —— 每 frame 的 E1/E2 计数
    （`E1_wsl_full` / `E2_native_unaware` / `E2_native_aware`）。

守恒律（脚本内断言）：矩阵每行之和 = 该行 E1 的样本数；矩阵总和 = n。

用法
====
  python tools/compute_696_transition_matrix.py                 # 打印 + 写 data/696_transition_matrix.json
  python tools/compute_696_transition_matrix.py --no-write      # 只打印
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "692_environment_paired_experiment.json"
OUT = ROOT / "data" / "696_transition_matrix.json"

STATES = ("catch", "miss", "unknown")


def _frame_counts(frame: dict[str, Any], key: str) -> dict[str, int]:
    """从 frame 里取出某口径的三态计数，并校验 total 一致。"""
    node = frame[key]
    counts = {s: int(node[s]) for s in STATES}
    total = int(node["total"])
    if sum(counts.values()) != total:
        raise ValueError(f"{key}: 三态之和 {sum(counts.values())} != total {total}")
    return counts


def transition_matrix(e1: dict[str, int], e2: dict[str, int]) -> dict[str, dict[str, int]]:
    """E1 -> E2 的三态转移矩阵。

    现有配对数据是**逐样本状态**的聚合（692 只发布了计数，不发布逐样本状态），
    故这里用**边际一致（marginal-consistent）**的标准构造：

      * `catch->catch` = min(E1.catch, E2.catch)（E2 的 catch 是 E1 catch 的子集：
        换环境不会**新增** catch——692 的 `gained_e2_catches` 恒为 0）
      * `catch->miss`   = E1.catch - catch->catch
      * `catch->unknown`= 0（E2 unaware 下没有 unknown；aware 下见下）
      * `miss->catch`   = E2.catch - catch->catch（= 0）
      * `miss->miss`    = E1.miss - miss->catch
      * `miss->unknown` = 0（unaware）
      * unknown 行：E1 的聚合 unknown = 0 ⇒ 整行为 0

    对 aware 口径，`unknown` 列改由 E2 的 unknown 数填充（见 `aware_matrix`）。
    """
    cc = min(e1["catch"], e2["catch"])
    mc = max(0, e2["catch"] - cc)
    cm = e1["catch"] - cc
    mm = e1["miss"] - mc
    return {
        "catch": {"catch": cc, "miss": cm, "unknown": 0},
        "miss": {"catch": mc, "miss": mm, "unknown": 0},
        "unknown": {"catch": 0, "miss": 0, "unknown": e1["unknown"]},
    }


def aware_matrix(e1: dict[str, int], e2: dict[str, int]) -> dict[str, dict[str, int]]:
    """四态纪律口径：E2 未测量的样本记为 unknown（而非 miss）。

    E2(aware) 的 miss 恒为 0、unknown = 全部"未运行资产"的样本。因为 E2 的 catch
    仍是 E1 catch 的子集，故：

      * catch->catch = min(E1.catch, E2.catch)，catch->unknown = 其余 catch
      * miss->unknown = E1.miss（E2 aware 下没有可信负例）
    """
    cc = min(e1["catch"], e2["catch"])
    return {
        "catch": {"catch": cc, "miss": 0, "unknown": e1["catch"] - cc},
        "miss": {"catch": 0, "miss": 0, "unknown": e1["miss"]},
        "unknown": {"catch": 0, "miss": 0, "unknown": e1["unknown"]},
    }


def row_sums(m: dict[str, dict[str, int]]) -> dict[str, int]:
    return {r: sum(m[r].values()) for r in STATES}


def col_sums(m: dict[str, dict[str, int]]) -> dict[str, int]:
    return {c: sum(m[r][c] for r in STATES) for c in STATES}


def build() -> dict[str, Any]:
    raw = json.loads(SRC.read_text(encoding="utf-8"))
    frames = raw["frames"]
    out: dict[str, Any] = {
        "schema": "queyi-696/transition-matrix/v1",
        "generated_by": "tools/compute_696_transition_matrix.py",
        "source": str(SRC.relative_to(ROOT)).replace("\\", "/"),
        "detect_calls": 0,
        "states": list(STATES),
        "note": (
            "三态转移矩阵基于 692 的**单一环境对**（E1 wsl-gcc-13.3 / E2 windows-native-mingw）；"
            "n_env=1，不声称普适。unaware 与 aware 的**原始测量完全相同**，只有 caliber 不同 ⇒ "
            "本矩阵是'结构性（被动）Goodhart'的可计算实例。"
        ),
        "frames": {},
    }
    for fname, frame in frames.items():
        e1 = _frame_counts(frame, "E1_wsl_full")
        e2u = _frame_counts(frame, "E2_native_unaware")
        e2a = _frame_counts(frame, "E2_native_aware")
        m_un = transition_matrix(e1, e2u)
        m_aw = aware_matrix(e1, e2a)
        # 守恒律断言
        assert row_sums(m_un) == {s: e1[s] for s in STATES}, (fname, row_sums(m_un), e1)
        assert row_sums(m_aw) == {s: e1[s] for s in STATES}, (fname, row_sums(m_aw), e1)
        assert col_sums(m_un)["catch"] == e2u["catch"], (fname, col_sums(m_un), e2u)
        assert col_sums(m_aw)["catch"] == e2a["catch"], (fname, col_sums(m_aw), e2a)
        assert col_sums(m_aw)["unknown"] == e2a["unknown"], (fname, col_sums(m_aw), e2a)
        out["frames"][fname] = {
            "frame": frame["frame"],
            "n": frame["n"],
            "E1": e1,
            "E2_unaware": e2u,
            "E2_aware": e2a,
            "T_unaware": m_un,
            "T_aware": m_aw,
            "row_sums_unaware": row_sums(m_un),
            "col_sums_unaware": col_sums(m_un),
            "row_sums_aware": row_sums(m_aw),
            "col_sums_aware": col_sums(m_aw),
            "reclassified_miss_to_unknown": m_aw["catch"]["unknown"] + m_aw["miss"]["unknown"],
            "mcnemar": frame.get("mcnemar", {}),
            "silent_false_miss": frame.get("silent_false_miss", {}),
        }
    # 主 frame（论文 F3 用 A5_evaluation_566；110 真实语料作对照）
    out["headline"] = {
        "primary_frame": "A5_evaluation_566",
        "secondary_frame": "real_world_110",
    }
    return out


def _fmt(m: dict[str, dict[str, int]]) -> str:
    head = "            " + "".join(f"{c:>10}" for c in STATES)
    lines = [head]
    for r in STATES:
        lines.append(f"  {r:>8}" + "".join(f"{m[r][c]:>10}" for c in STATES))
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="三态转移矩阵（696-A3）")
    ap.add_argument("--no-write", action="store_true", help="只打印，不写 data/696_transition_matrix.json")
    args = ap.parse_args()

    res = build()
    for fname, fr in res["frames"].items():
        print(f"=== {fname} ({fr['frame']}, n={fr['n']}) ===")
        print("  E1 (wsl-gcc-13.3) :", fr["E1"])
        print("  E2 (native, unaware):", fr["E2_unaware"])
        print("  E2 (native, aware)  :", fr["E2_aware"])
        print("  T_unaware (rows=E1, cols=E2):")
        print(_fmt(fr["T_unaware"]))
        print("  T_aware (rows=E1, cols=E2):")
        print(_fmt(fr["T_aware"]))
        print("  reclassified miss->unknown:", fr["reclassified_miss_to_unknown"])
        print()

    if not args.no_write:
        OUT.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8", newline="\n")
        print(f"[696-A3] 已写 {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
