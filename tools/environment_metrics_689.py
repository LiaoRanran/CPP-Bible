#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""environment_metrics_689.py — 689-B3：三组件环境指标（catch / unknown / conditional recall）。

背景
====
评审与 686 硬伤 #9 指出：环境依赖若只报单一 recall，会因为**分母病理**误导——
当环境变化把原本"可测"的样本变成 unknown 时，单一 recall 可能不变（unknown 被
分母吞掉）或虚升（unknown 从分母剔除）。本脚本为每个 environment profile 同时报告：

* ``catch_rate   = catch / total``
* ``unknown_rate = unknown / total``
* ``conditional_recall = catch / (catch + miss)``（排除 unknown）

并对 profile 对做 Δ_catch / Δ_unknown / Δ_conditional_recall。

Profiles（哪些实测、哪些推断，逐条登记）
========================================
* ``wsl-gcc-13.3``（实测）：676g 合成矩阵 1147 条 + 683 真实矩阵 110 条；
* ``wsl-clang-18.1.3``（实测）：683-B1 分层抽样 200 条（asan/ubsan 两资产，
  判定字符串与 661 SAN 分支逐字一致）；
* ``windows-native-mingw``（**口径推断，非实测**）：真实 110 条上仅有
  compiler-warn / cross-compile / linker 可用；asan/ubsan/tsan 不可用按
  688 的架构推断处理——给出两种记账：
    - *unaware*（静默退化）：不可用资产记 miss ⇒ catch_rate 23.64%、unknown 0%；
    - *aware*（感知协议）：不可用资产记 unknown ⇒ 资产级 unknown=100%、
      样本级 OR 不变但能力边界显式声明。
  纯 Windows 的 sanitizer 需要非 MinGW 工具链（clang-cl），本机未配置 ⇒ 标"待实测"。

只读上游；标准库；确定性；输出 ``data/689_environment_metrics.{json,md}``。

用法
====
    python tools/environment_metrics_689.py
"""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REAL_MATRIX = ROOT / "data" / "683_real_world_detection_matrix.json"
SYN_MATRIX = ROOT / "data" / "blindspot_676g_detection_matrix.json"
XTOOL_JSON = ROOT / "data" / "683_cross_toolchain_results.json"
XTOOL_CKPT = ROOT / "data" / "683_b1_ckpt.jsonl"
OUT_JSON = ROOT / "data" / "689_environment_metrics.json"
OUT_MD = ROOT / "data" / "689_environment_metrics_report.md"

SEED = 6891  # 确定性脚本；种子注册供元数据

ALL_ASSETS = ("asan", "ubsan", "tsan", "compiler-warn", "wunsequenced", "cross-compile", "linker", "compile-time")
NATIVE_AVAILABLE = ("compiler-warn", "cross-compile", "linker")
SANITIZER_ASSETS = ("asan", "ubsan", "tsan")

#: 家族映射（tools/repair_681_labels.py::FAMILY8，681 归一化口径）
FAMILY8: dict[str, tuple[str, ...]] = {
    "memory": ("memory_safety", "use_after_free", "double_free", "memory_leak",
               "smart_pointer", "raii_violation", "move_semantics", "uninitialized_read"),
    "bounds": ("out_of_bounds", "null_pointer_deref"),
    "integer": ("integer_overflow", "bit_operation"),
    "alias_type": ("type_punning", "strict_aliasing", "alignment", "endianness"),
    "concurrency": ("data_race", "atomic_ub", "memory_order", "deadlock", "condition_variable"),
    "stl": ("iterator_invalidation", "stl_container_ub", "string_ub", "algorithm_misuse"),
    "language_oop": ("virtual_function", "lambda_capture", "logic_error", "cross_tu_ub", "other_ub"),
    "embedded_link": ("volatile_misuse", "register_ub", "interrupt_safety", "linker_odr"),
}
TYPE_TO_FAMILY: dict[str, str] = {t: f for f, ts in FAMILY8.items() for t in ts}


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _triple(catch: int, miss: int, unknown: int) -> dict[str, Any]:
    total = catch + miss + unknown
    denom = catch + miss
    return {
        "catch": catch, "miss": miss, "unknown": unknown, "total": total,
        "catch_rate_pct": (catch / total * 100.0) if total else None,
        "unknown_rate_pct": (unknown / total * 100.0) if total else None,
        "conditional_recall_pct": (catch / denom * 100.0) if denom else None,
    }


def _count_verdicts(verdicts: list[str]) -> dict[str, Any]:
    return _triple(verdicts.count("catch"), verdicts.count("miss"), verdicts.count("unknown"))


def _asset_triples(samples: list[dict[str, Any]], field: str, assets: tuple[str, ...]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for a in assets:
        vs = [str(s[field].get(a, {}).get("verdict", "unknown")) for s in samples]
        out[a] = _count_verdicts(vs)
    return out


def _or_triple(samples: list[dict[str, Any]], field: str, assets: tuple[str, ...]) -> dict[str, Any]:
    """OR 口径：任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss（只用给定资产集）。"""
    vs = []
    for s in samples:
        verdicts = [str(s[field].get(a, {}).get("verdict", "unknown")) for a in assets]
        if "catch" in verdicts:
            vs.append("catch")
        elif all(v == "unknown" for v in verdicts):
            vs.append("unknown")
        else:
            vs.append("miss")
    return _count_verdicts(vs)


def _delta(a: dict[str, Any], b: dict[str, Any], key: str) -> float | None:
    va, vb = a.get(key), b.get(key)
    if va is None or vb is None:
        return None
    return float(va) - float(vb)


def build() -> dict[str, Any]:
    real_doc: dict[str, Any] = json.loads(REAL_MATRIX.read_text(encoding="utf-8"))
    syn_doc: dict[str, Any] = json.loads(SYN_MATRIX.read_text(encoding="utf-8"))
    real = list(real_doc["samples"])
    syn = list(syn_doc["samples"])

    # ---------------- P1: WSL g++ 13.3 ----------------
    p1_real_asset = _asset_triples(real, "per_asset", ALL_ASSETS)
    p1_real_or = _or_triple(real, "per_asset", ALL_ASSETS)
    p1_syn_asset = _asset_triples(syn, "per_asset", ALL_ASSETS)
    p1_syn_or = _or_triple(syn, "per_asset", ALL_ASSETS)
    # 交叉核对：矩阵自带 or_verdict_all8 与重算一致（fail-loud）
    ors = [str(s["or_verdict_all8"]) for s in syn]
    assert p1_syn_or["catch"] == ors.count("catch"), "676g or_verdict_all8 与重算不一致"

    # ---------------- P2: native Windows（口径推断） ----------------
    p2_unaware = _or_triple(real, "per_asset", NATIVE_AVAILABLE)  # 不可用资产按 miss 记账
    p2_aware_asset = {a: dict(p1_real_asset[a]) for a in NATIVE_AVAILABLE}
    for a in SANITIZER_ASSETS + ("wunsequenced", "compile-time"):
        src = p1_real_asset.get(a)
        assert src is not None
        p2_aware_asset[a] = _triple(0, 0, src["total"])  # 不可用 ⇒ 资产级 unknown=100%
    p2_aware_note = ("感知协议下 asan/ubsan/tsan 记资产级 unknown=100%；样本级 OR 仍为 23.64%，"
                     "但该数字必须随\"能力边界声明\"使用，不得与 P1 的 59.09% 直接相减后当\"退化\""
                     "而不说明分母构成")

    # ---------------- P3: WSL clang 18.1.3（200 抽样，asan/ubsan） ----------------
    xtool: dict[str, Any] = json.loads(XTOOL_JSON.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for line in XTOOL_CKPT.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    assert len(rows) == 200, f"683_b1_ckpt 行数 {len(rows)} != 200"

    p3_asset: dict[str, Any] = {}
    for a in ("asan", "ubsan"):
        g = [str(r["gxx_676g"][a]) for r in rows]
        c = [str(r["clang"][a]["verdict"]) for r in rows]
        p3_asset[a] = {
            "gcc": _count_verdicts(g),
            "clang": _count_verdicts(c),
            "agreement_pct": xtool["b1"]["per_asset"][a]["agree_pct"],
            "kappa": xtool["b1"]["per_asset"][a]["kappa"],
            "n_diff": xtool["b1"]["per_asset"][a]["n_diff"],
        }
    # 家族分层（asan+ubsan 池化：每样本 2 个资产格）
    fam_stats: dict[str, dict[str, int]] = {}
    for r in rows:
        f = TYPE_TO_FAMILY[str(r["defect_type"])]
        cell = fam_stats.setdefault(f, {"cells": 0, "gcc_catch": 0, "clang_catch": 0,
                                        "gcc_unknown": 0, "clang_unknown": 0})
        for a in ("asan", "ubsan"):
            gv = str(r["gxx_676g"][a])
            cv = str(r["clang"][a]["verdict"])
            cell["cells"] += 1
            cell["gcc_catch"] += int(gv == "catch")
            cell["clang_catch"] += int(cv == "catch")
            cell["gcc_unknown"] += int(gv == "unknown")
            cell["clang_unknown"] += int(cv == "unknown")
    fam_table: list[dict[str, Any]] = []
    for f in FAMILY8:
        fc = fam_stats.get(f)
        if not fc or fc["cells"] == 0:
            continue
        fam_table.append({
            "family": f, "cells": fc["cells"],
            "gcc_catch_pct": fc["gcc_catch"] / fc["cells"] * 100.0,
            "clang_catch_pct": fc["clang_catch"] / fc["cells"] * 100.0,
            "delta_clang_minus_gcc_pp": (fc["clang_catch"] - fc["gcc_catch"]) / fc["cells"] * 100.0,
            "gcc_unknown_rate_pct": fc["gcc_unknown"] / fc["cells"] * 100.0,
            "clang_unknown_rate_pct": fc["clang_unknown"] / fc["cells"] * 100.0,
        })

    # ---------------- Δ 报告 ----------------
    deltas = {
        "p3_vs_p1_200sample": {
            "scope": "同一 200 条分层抽样，仅 asan/ubsan 两资产",
            "asan": {
                "delta_catch_rate_pp": _delta(p3_asset["asan"]["clang"], p3_asset["asan"]["gcc"], "catch_rate_pct"),
                "delta_unknown_rate_pp": _delta(p3_asset["asan"]["clang"], p3_asset["asan"]["gcc"], "unknown_rate_pct"),
                "delta_conditional_recall_pp": _delta(p3_asset["asan"]["clang"], p3_asset["asan"]["gcc"],
                                                      "conditional_recall_pct"),
            },
            "ubsan": {
                "delta_catch_rate_pp": _delta(p3_asset["ubsan"]["clang"], p3_asset["ubsan"]["gcc"], "catch_rate_pct"),
                "delta_unknown_rate_pp": _delta(p3_asset["ubsan"]["clang"], p3_asset["ubsan"]["gcc"], "unknown_rate_pct"),
                "delta_conditional_recall_pp": _delta(p3_asset["ubsan"]["clang"], p3_asset["ubsan"]["gcc"],
                                                      "conditional_recall_pct"),
            },
        },
        "p2_unaware_vs_p1_real110": {
            "scope": "真实 110 条，OR 层（P2=跨平台资产并集，按 miss 记账）",
            "delta_catch_rate_pp": _delta(p2_unaware, p1_real_or, "catch_rate_pct"),
            "delta_unknown_rate_pp": _delta(p2_unaware, p1_real_or, "unknown_rate_pct"),
            "delta_conditional_recall_pp": _delta(p2_unaware, p1_real_or, "conditional_recall_pct"),
            "delta_catch_rate_pp_if_unknown_accounting": 0.0,
            "note": ("静默退化记账：Δcatch=−35.45pp、Δunknown=0pp（guard 仍绿）；"
                     "感知记账：Δcatch=0（可用资产集不变）但新增 3 个资产的 unknown=100% 边界声明。"
                     "两种记账的差别本身就是\"分母病理\"的演示。"),
        },
        "p2_vs_p1_syn": {
            "scope": "合成 1147 条，OR 层（P1 全 8 资产 vs P2 跨平台资产并集）",
            "p1_or": p1_syn_or,
            "p2_or_estimate": _or_triple(syn, "per_asset", NATIVE_AVAILABLE),
            "note": "合成侧同样只作口径推断（非实测）；用于展示退化方向与真实侧一致。",
        },
    }

    return {
        "schema": "queyi-689-environment-metrics/v1",
        "generated_by": "tools/environment_metrics_689.py",
        "generated_at": _now(),
        "seed": SEED,
        "metric_definitions": {
            "catch_rate_pct": "catch / total",
            "unknown_rate_pct": "unknown / total",
            "conditional_recall_pct": "catch / (catch + miss)（排除 unknown）",
            "why_three": "环境变化可能通过 unknown 改变分母：单看 recall 会把\"不可测\"吞掉或虚升；三组件并报使分母变化显式。",
        },
        "profiles": {
            "wsl-gcc-13.3": {
                "status": "实测",
                "environment": {"os": "Ubuntu 24.04 (WSL2)", "compiler": "g++ 13.3.0",
                                "flags": "-O0/-O2 双档，任一档报出即 catch", "assets": list(ALL_ASSETS)},
                "real110_per_asset": p1_real_asset,
                "real110_or": p1_real_or,
                "syn1147_per_asset": p1_syn_asset,
                "syn1147_or": p1_syn_or,
            },
            "windows-native-mingw": {
                "status": "口径推断（非实测；纯 Windows sanitizer 需 clang-cl，本机未配置）",
                "environment": {"os": "win32", "compiler": "MinGW g++ 13.1.0 / clang 22.1.8（ASan 缺运行库）",
                                "available_assets": list(NATIVE_AVAILABLE)},
                "real110_or_unaware": p2_unaware,
                "real110_per_asset_aware": p2_aware_asset,
                "aware_note": p2_aware_note,
            },
            "wsl-clang-18.1.3": {
                "status": "实测（683-B1 分层抽样 200 条，asan/ubsan 双档）",
                "environment": {"os": "Ubuntu (WSL2)", "compiler": "clang 18.1.3",
                                "samples": "1147 全池分层抽样（按 defect_type 比例，种子 6831，挂起样本跳过并等量替补）"},
                "per_asset": p3_asset,
                "family_table": fam_table,
            },
        },
        "deltas": deltas,
        "readings": {
            "r1_cross_toolchain_stable": ("同 OS 换编译器（g++↔clang）在 200 抽样上 asan/ubsan 一致率 93.5%，"
                                          "κ=0.864/0.843，Δcatch ≤2pp、Δunknown ≤1.5pp ⇒ 工具链敏感性有限（实测）。"),
            "r2_environment_loss_dominant": ("跨环境（WSL→native）真实 110 的 catch_rate 59.09%→23.64%"
                                              "（−35.45pp，口径推断）；且静默退化时 unknown 不上升（Δunknown=0）"
                                              "——单看 recall 会误以为\"只是低了\"，看不到\"39 个捕获的测量根本未执行\"。"),
            "r3_denominator_pathology": ("wunsequenced/compile-time 在真实 110 上的资产级 unknown_rate=100%，"
                                         "但在 OR 口径被其他资产掩盖（样本级 unknown=0）。"
                                         "任何单资产分析若不并报 unknown 率，都会把这两个资产读成\"0 检出\"。"),
            "r4_family_layer": ("clang↔gcc 的差异集中在 stl 家族（+8/56 格 = +14.3pp，clang 更高），"
                                "其余家族 Δ 极小；家族层无反转 ⇒ 一致率不是被单一家族拉高的。"),
        },
        "caveats": [
            "windows-native 一档为**架构/口径推断**，非本机实测；不得写成实测数字。",
            "wsl-clang 档为 200 条分层抽样（非全池），其 catch 率不可与全池 61.64%/59.09% 直接比；仅用于同一样本上的 gcc↔clang 配对对比。",
            "clang 侧 unknown（7/200）高于 gcc（4/200）：其中含 1 条 clang 编译失败（expF:F176），如实保留为 unknown。",
            "P2 的\"26/110\"来自 683 矩阵中跨平台资产 verdict 的并集；若 Windows 上链接器/编译器行为与记录环境不同，绝对值会移动。",
        ],
    }


def _pct(x: Any) -> str:
    return f"{float(x):.2f}%" if x is not None else "—（分母为 0）"


def _md(doc: dict[str, Any]) -> str:
    lines = [
        "# 689-B3 · 三组件环境指标（catch / unknown / conditional recall）",
        "",
        f"- 生成：{doc['generated_at']}｜脚本：tools/environment_metrics_689.py｜种子：{doc['seed']}（确定性）",
        "- 指标定义：catch_rate = catch/total；unknown_rate = unknown/total；"
        "conditional_recall = catch/(catch+miss)。",
        "",
        "## 1. WSL g++ 13.3（实测）",
        "",
        "### 1.1 真实 110 条 · 逐资产",
        "",
        "| 资产 | catch | miss | unknown | catch_rate | unknown_rate | cond_recall |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    p1 = doc["profiles"]["wsl-gcc-13.3"]
    for a, t in p1["real110_per_asset"].items():
        lines.append(f"| {a} | {t['catch']} | {t['miss']} | {t['unknown']} | {_pct(t['catch_rate_pct'])} | "
                     f"{_pct(t['unknown_rate_pct'])} | {_pct(t['conditional_recall_pct'])} |")
    o = p1["real110_or"]
    lines += [
        f"| **OR（8 资产）** | {o['catch']} | {o['miss']} | {o['unknown']} | {_pct(o['catch_rate_pct'])} | "
        f"{_pct(o['unknown_rate_pct'])} | {_pct(o['conditional_recall_pct'])} |",
        "",
        "### 1.2 合成 1147 条 · 逐资产",
        "",
        "| 资产 | catch | miss | unknown | catch_rate | unknown_rate | cond_recall |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for a, t in p1["syn1147_per_asset"].items():
        lines.append(f"| {a} | {t['catch']} | {t['miss']} | {t['unknown']} | {_pct(t['catch_rate_pct'])} | "
                     f"{_pct(t['unknown_rate_pct'])} | {_pct(t['conditional_recall_pct'])} |")
    so = p1["syn1147_or"]
    lines += [
        f"| **OR（8 资产）** | {so['catch']} | {so['miss']} | {so['unknown']} | {_pct(so['catch_rate_pct'])} | "
        f"{_pct(so['unknown_rate_pct'])} | {_pct(so['conditional_recall_pct'])} |",
        "",
        "## 2. Windows native（口径推断，非实测）· 真实 110",
        "",
        f"- **unaware（静默退化记账）**：跨平台资产并集 OR = "
        f"{doc['profiles']['windows-native-mingw']['real110_or_unaware']['catch']}/110 = "
        f"{doc['profiles']['windows-native-mingw']['real110_or_unaware']['catch_rate_pct']:.2f}%，"
        f"unknown {doc['profiles']['windows-native-mingw']['real110_or_unaware']['unknown_rate_pct']:.0f}%。",
        f"- **aware（感知记账）**：asan/ubsan/tsan 资产级 unknown=100%；"
        f"{doc['profiles']['windows-native-mingw']['aware_note']}",
        "",
        "## 3. Δ 对比表",
        "",
        "| 对比 | 指标 | Δ |",
        "|---|---|---:|",
    ]
    d3 = doc["deltas"]["p3_vs_p1_200sample"]
    for a in ("asan", "ubsan"):
        for k, label in (("delta_catch_rate_pp", "Δcatch_rate"), ("delta_unknown_rate_pp", "Δunknown_rate"),
                         ("delta_conditional_recall_pp", "Δcond_recall")):
            v = d3[a][k]
            lines.append(f"| clang vs gcc（{a}，n=200） | {label} | {v:+.2f}pp |")
    d2 = doc["deltas"]["p2_unaware_vs_p1_real110"]
    lines += [
        f"| native vs WSL（真实 110，OR） | Δcatch_rate（静默记账） | {d2['delta_catch_rate_pp']:+.2f}pp |",
        f"| native vs WSL（真实 110，OR） | Δunknown_rate（静默记账） | {d2['delta_unknown_rate_pp']:+.2f}pp |",
        f"| native vs WSL（真实 110，OR） | Δcond_recall | {d2['delta_conditional_recall_pp']:+.2f}pp |",
        "",
        "## 4. clang↔gcc 家族分层（asan+ubsan 池化格）",
        "",
        "| 家族 | 格数 | gcc catch% | clang catch% | Δ(clang−gcc)pp | gcc unknown% | clang unknown% |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in doc["profiles"]["wsl-clang-18.1.3"]["family_table"]:
        lines.append(f"| {r['family']} | {r['cells']} | {r['gcc_catch_pct']:.1f} | {r['clang_catch_pct']:.1f} | "
                     f"{r['delta_clang_minus_gcc_pp']:+.1f} | {r['gcc_unknown_rate_pct']:.1f} | "
                     f"{r['clang_unknown_rate_pct']:.1f} |")
    lines += ["", "## 5. 读法（四条）", ""]
    lines += [f"- **{k}**：{v}" for k, v in doc["readings"].items()]
    lines += ["", "## 6. 诚实边界", ""]
    lines += [f"- {c}" for c in doc["caveats"]]
    lines += ["", "复算：`python tools/environment_metrics_689.py`。", ""]
    return "\n".join(lines)


def main() -> None:
    doc = build()
    OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    OUT_MD.write_text(_md(doc), encoding="utf-8", newline="\n")
    p1 = doc["profiles"]["wsl-gcc-13.3"]
    print("[689-B3] real110 OR catch_rate:", round(p1["real110_or"]["catch_rate_pct"], 2))
    print("[689-B3] native unaware catch_rate:",
          round(doc["profiles"]["windows-native-mingw"]["real110_or_unaware"]["catch_rate_pct"], 2))
    print("[689-B3] wrote", OUT_JSON.name, OUT_MD.name)


if __name__ == "__main__":
    main()
