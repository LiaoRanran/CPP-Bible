#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_698_detectability_bound.py — 698-C：可检测性的理论上限（**只读，0 次 detect**）。

承接 697-C 的负面发现（族外泛化 AUC 0.7662 的朴素基线 > 0.7551 的特征模型），
本批深入回答："哪些缺陷在**原理上**就不可检测"。

四项内容
========
1. **34 类缺陷的可判定性分类**（D 可判定 / S 半可判定 / U 需规约）：
   给出**判据**（不是逐类证明），并用实测检出率做**预测效度检验** ——
   若分类有信息，S 类的检出率应显著高于 U 类。
2. **信息论下界**：逐类型的香农熵 H(Y) 与 Bayes 误差下界 min(q, 1−q)；
   与 697-C 的**族内**下界 7.50% 对比，给出**族间（类型间）**下界。
3. **检测器能力上限曲线**：贪心 k=1..8 的 OR 检出率，拟合饱和曲线并外推到 k=16/32；
   同时给**子模上界**（684 已验证 f 子模）。
4. **"不可检测"的三级操作化定义**（L1/L2/L3），对 34 类逐类分级。

红线：``detect_calls = 0``；只读冻结矩阵；产出只写 ``data/698_*``。

用法
====
    python tools/compute_698_detectability_bound.py
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_698_detectability_bound")

MATRIX_1147: Final[str] = "blindspot_676g_detection_matrix.json"
FAMILIES_677B: Final[str] = "677b_clone_families.json"
A5: Final[str] = "a5_676f_detection_matrix.json"
OUT_JSON: Final[Path] = ROOT / "data" / "698_detectability_bound.json"

ASSETS: Final[tuple[str, ...]] = (
    "asan", "ubsan", "tsan", "compiler-warn",
    "wunsequenced", "cross-compile", "linker", "compile-time",
)

# ══════════════════════════════════════════════════════════════════════════
# 可判定性分类的**判据**（重要：这是论证，不是逐类证明）
# ══════════════════════════════════════════════════════════════════════════
# D（decidable）      ：性质只依赖语法 / 静态类型 / 有界状态，存在对**所有**输入
#                        都正确终止的判定程序。
# S（semi-decidable）：「∃ 一条执行使其违反」—— 可由动态检测器在**观察到**时报告
#                        （报告的阳性可靠），但对阴性**不完备** ⇒ 漏报原理上不可避免。
# U（needs-oracle）  ：判定"输出是否符合**意图**"，需要先验规约（oracle）；
#                        即便给了规约，程序等价性仍不可判定（Rice）。
DECIDABILITY: Final[dict[str, tuple[str, str]]] = {
    # ── S：运行时可观察的违反（报告即真，但阴性不完备）──
    "use_after_free": ("S", "存在执行使已释放内存被访问 ⇒ ∃-性质，RE；asan 可观察"),
    "double_free": ("S", "∃ 执行重复释放 ⇒ RE"),
    "memory_leak": ("S", "∃ 执行使分配未释放 ⇒ RE（asan/LSan 可观察）"),
    "out_of_bounds": ("S", "∃ 执行越界访问 ⇒ RE"),
    "null_pointer_deref": ("S", "∃ 执行空指针解引用 ⇒ RE"),
    "uninitialized_read": ("S", "∃ 执行读未初始化值 ⇒ RE（UBSan/MSan 可观察）"),
    "integer_overflow": ("S", "∃ 输入使有符号整数溢出 ⇒ RE（UBSan）"),
    "data_race": ("S", "∃ 执行使两个无同步访问冲突 ⇒ RE（TSan，happens-before 可观察）"),
    "atomic_ub": ("S", "∃ 执行的原子操作序列违反内存序 ⇒ RE"),
    "memory_order": ("S", "∃ 执行的内存序使用不当 ⇒ RE"),
    "deadlock": ("S", "∃ 执行使锁循环等待 ⇒ RE（TSan 的 lock-order-inversion 可观察）"),
    "iterator_invalidation": ("S", "∃ 执行使迭代器失效后仍使用 ⇒ RE"),
    "stl_container_ub": ("S", "∃ 执行触发 STL 前置条件违反 ⇒ RE"),
    "string_ub": ("S", "∃ 执行触发字符串 UB ⇒ RE"),
    "strict_aliasing": ("S", "∃ 执行通过不兼容类型访问 ⇒ RE（-fstrict-aliasing 下可观察）"),
    "type_punning": ("S", "同上，∃-性质"),
    "alignment": ("S", "∃ 执行访问未对齐地址 ⇒ RE（UBSan alignment check）"),
    "endianness": ("S", "∃ 执行在不同字节序下行为不同 ⇒ RE（cross-compile 可观察）"),
    "volatile_misuse": ("S", "∃ 执行使 volatile 语义被违反 ⇒ RE"),
    "register_ub": ("S", "∃ 执行使寄存器/存储类使用不当 ⇒ RE"),
    "raii_violation": ("S", "∃ 执行使资源未按时释放 ⇒ RE（与 memory_leak 同类）"),
    "cross_tu_ub": ("S", "∃ 链接单元组合使 ODR 违反 ⇒ RE（linker 可观察）"),
    "linker_odr": ("S", "同上，ODR 违反是链接期可检查的 ∃-性质"),
    "smart_pointer": ("S", "∃ 执行的智能指针生命周期错误 ⇒ RE"),
    "move_semantics": ("S", "∃ 执行使用已移动对象 ⇒ RE"),
    "memory_safety": ("S", "内存安全族（∃ 执行违反空间/时间安全）⇒ RE"),
    "lambda_capture": ("S", "∃ 执行使悬垂捕获被使用 ⇒ RE"),
    "unspecified": ("S", "∃ 执行顺序导致未指定行为 ⇒ RE"),
    # ── U：需要"正确行为"的规约（oracle）──
    "logic_error": ("U", "判定输出是否符合**意图**，需外部规约；无规约时不可判定"),
    "state_machine": ("U", "协议状态机正确性需规约（如 CCS 应被拒绝）⇒ 需 oracle"),
    "algorithm_misuse": ("U", "「误用」相对 API 契约 ⇒ 需契约规约"),
    "resource_exhaustion": ("U", "是否耗尽依赖输入规模与资源模型 ⇒ 需资源规约"),
    "interrupt_safety": ("U", "中断安全性需并发/时序规约 ⇒ 需 oracle"),
    "condition_variable": ("U", "条件变量的正确等待/通知需活性规约 ⇒ 需 oracle"),
    "virtual_function": ("U", "虚函数行为是否符合设计意图 ⇒ 需规约"),
    "bit_operation": ("S", "∃ 输入使位运算 UB（移位数越界等）⇒ RE"),
    "other_ub": ("U", "笼统标签，无确定语义 ⇒ 无法归类（诚实标注）"),
}


def _verdict(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell) if cell is not None else "unknown"


def _entropy_binary(q: float) -> float:
    if q <= 0.0 or q >= 1.0:
        return 0.0
    return -(q * math.log2(q) + (1 - q) * math.log2(1 - q))


def load() -> tuple[list[dict[str, Any]], dict[str, set[str]]]:
    doc = load_json_cached(DATA / MATRIX_1147)
    rows: list[dict[str, Any]] = []
    catch: dict[str, set[str]] = {a: set() for a in ASSETS}
    for s in doc.get("samples", []):
        uid = str(s.get("uid") or "")
        pa = s.get("per_asset") or {}
        caught_by = [a for a in ASSETS if _verdict(pa.get(a, "unknown")) == "catch"]
        for a in caught_by:
            catch[a].add(uid)
        rows.append({
            "uid": uid,
            "sample_id": str(s.get("sample_id") or uid),
            "defect_type": str(s.get("defect_type") or "unknown"),
            "source_batch": str(s.get("source_batch") or "unknown"),
            "caught": bool(caught_by),
        })
    return rows, catch


def load_clone_families() -> dict[str, str]:
    fam_doc = load_json_cached(DATA / FAMILIES_677B)
    a5 = load_json_cached(DATA / A5)
    sid2orig = {str(s.get("sample_id")): str(s.get("orig_id") or s.get("sample_id"))
                for s in a5.get("samples", [])}
    idx: dict[str, str] = {}
    for fam in fam_doc.get("families", []):
        fid = str(fam.get("family_id"))
        for m in fam.get("members", []):
            idx[str(m)] = fid
            # 与 697-C 的 build_family_index 用**同一规则**（直接赋值，不用 setdefault），
            # 这样两批的族内下界可以逐位对账，而不是"各自一套映射"。
            if str(m) in sid2orig:
                idx[sid2orig[str(m)]] = fid
    return idx


# ══════════════════════════════════════════════════════════════════════════
# 1. 可判定性分类 + 预测效度检验
# ══════════════════════════════════════════════════════════════════════════
def decidability_table(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_type: dict[str, list[int]] = defaultdict(list)
    for r in rows:
        by_type[r["defect_type"]].append(1 if r["caught"] else 0)

    table: list[dict[str, Any]] = []
    for t in sorted(by_type):
        v = by_type[t]
        q = sum(v) / len(v)
        cls, why = DECIDABILITY.get(t, ("U", "**未分类**：本批判据未覆盖，诚实标为 U"))
        table.append({
            "defect_type": t,
            "n": len(v),
            "catch_rate": round(q, 6),
            "blindspot_rate": round(1 - q, 6),
            "decidability": cls,
            "reason": why,
            "entropy_bits": round(_entropy_binary(q), 6),
            "bayes_error_lower_bound": round(min(q, 1 - q), 6),
        })

    # 预测效度：S 类的检出率是否显著高于 U 类（置换检验，10k 次）
    sq = [r["catch_rate"] for r in table if r["decidability"] == "S"]
    uq = [r["catch_rate"] for r in table if r["decidability"] == "U"]
    obs = (sum(sq) / len(sq)) - (sum(uq) / len(uq)) if sq and uq else 0.0
    rng = random.Random(698)
    allq = sq + uq
    perm_hits = 0
    trials = 10000
    for _ in range(trials):
        rng.shuffle(allq)
        d = (sum(allq[:len(sq)]) / len(sq)) - (sum(allq[len(sq):]) / len(uq))
        if d >= obs:
            perm_hits += 1
    p = (perm_hits + 1) / (trials + 1)

    counts = Counter(r["decidability"] for r in table)
    return {
        "criterion": {
            "D": "只依赖语法 / 静态类型 / 有界状态 ⇒ 存在全输入正确终止的判定程序",
            "S": "「∃ 执行使其违反」⇒ RE（半可判定）：阳性可靠，阴性不完备 ⇒ 漏报原理上不可避免",
            "U": "需「输出是否符合意图」的规约（oracle）⇒ 即便给规约，等价性仍不可判定（Rice）",
        },
        "n_types": len(table),
        "class_counts": dict(counts),
        "table": table,
        "predictive_validity": {
            "mean_catch_rate_S": round(sum(sq) / len(sq), 6) if sq else None,
            "mean_catch_rate_U": round(sum(uq) / len(uq), 6) if uq else None,
            "observed_difference": round(obs, 6),
            "permutation_p_one_sided": round(p, 6),
            "n_S": len(sq), "n_U": len(uq),
            "verdict": ("分类具有预测效度" if p < 0.05 else "分类**未**显示预测效度（差异可能由样本量/构成造成）"),
        },
        "honest_note": (
            "这是**论证性分类**，不是逐类的可判定性证明。判据是缺陷属性本身的逻辑形式"
            "（∃-执行性质 vs 需规约性质）。Rice 定理给的是「不存在对所有程序正确的判定程序」，"
            "而检测任务允许有错误率 —— 两者不矛盾；S 类**可以学**，U 类**没有规约就无从学起**。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 2. 信息论下界（族内 vs 族间）
# ══════════════════════════════════════════════════════════════════════════
def information_bounds(rows: list[dict[str, Any]], fam_idx: dict[str, str]) -> dict[str, Any]:
    def _bayes_bound(keys: list[str]) -> dict[str, Any]:
        grp: dict[str, list[int]] = defaultdict(list)
        for r, k in zip(rows, keys):
            grp[k].append(1 if r["caught"] else 0)
        irr = 0.0
        for v in grp.values():
            q = sum(v) / len(v)
            irr += min(q, 1 - q) * len(v)
        n = len(rows)
        return {
            "n_groups": len(grp),
            "irreducible_error_pct": round(irr / n * 100.0, 4),
            "implied_accuracy_upper_bound": round(1 - irr / n, 6),
        }

    type_keys = [r["defect_type"] for r in rows]
    # ⚠ 键必须是 sample_id（如 "sample_001"），**不能**用 uid（"expA:sample_001"）——
    # 用错键会让所有样本落回 singleton ⇒ 族内不可约误差恒为 0（本批第一版踩了这个坑）。
    fam_keys = [fam_idx.get(r["sample_id"]) or f"singleton::{r['uid']}" for r in rows]
    batch_keys = [r["source_batch"] for r in rows]

    overall_q = sum(1 for r in rows if r["caught"]) / len(rows)
    return {
        "n": len(rows),
        "overall_catch_rate": round(overall_q, 6),
        "unconditional_entropy_bits": round(_entropy_binary(overall_q), 6),
        "by_defect_type_inter_family": _bayes_bound(type_keys),
        "by_clone_family_intra_family": _bayes_bound(fam_keys),
        "by_source_batch": _bayes_bound(batch_keys),
        "cross_check_697C": {
            "intra_family_bound_from_697C_pct": 7.4978,
            "note": "697-C 的族内下界为 7.4978%；本批独立重算见 by_clone_family_intra_family（应逐位一致）",
        },
        "interpretation": (
            "**族间（类型层）下界低于族内下界**是预期的：类型粒度更粗 ⇒ 组内更混杂 ⇒ "
            "不可约错误更高。反过来，族内下界低说明『同一模板的不同变体裁决不一致』只贡献了一部分，"
            "大头是**同类型内不同模板之间的差异**。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 3. 检测器能力上限曲线
# ══════════════════════════════════════════════════════════════════════════
def capability_curve(catch: dict[str, set[str]], n: int) -> dict[str, Any]:
    """贪心 k=1..8 的 OR 检出率 + 饱和曲线外推 + 子模上界。"""
    chosen: list[str] = []
    cur: set[str] = set()
    curve: list[dict[str, Any]] = []
    remaining = list(ASSETS)
    while remaining:
        best_a, best_gain = None, -1
        for a in remaining:
            gain = len(catch.get(a, set()) - cur)
            if gain > best_gain:
                best_a, best_gain = a, gain
        if best_a is None:
            break
        chosen.append(best_a)
        cur |= catch.get(best_a, set())
        remaining.remove(best_a)
        curve.append({
            "k": len(chosen), "asset_added": best_a,
            "marginal_gain_samples": best_gain,
            "or_catch_rate_pct": round(len(cur) / n * 100.0, 4),
        })

    # 边际是否单调不增（684 子模性的一个可观测后果）
    margins = [c["marginal_gain_samples"] for c in curve]
    diminishing = all(margins[i] >= margins[i + 1] for i in range(len(margins) - 1))

    # 饱和曲线拟合：**双参数** f(k) = f_sat·(1 − e^{−λk})。
    # ⚠ 不能只拟合 λ 而把 f_sat 钉死为 n —— 那会得到一个 k=16 时 95% 的荒谬外推
    #   （因为纯指数无法表达"k=6 就已平台"这一实测事实）。给定 λ 时 f_sat 是线性的，
    #   可解析求解 ⇒ λ 网格搜索 + f_sat 最小二乘闭式。
    ys = [c["or_catch_rate_pct"] / 100.0 * n for c in curve]
    ks = [c["k"] for c in curve]
    best: tuple[float, float, float] | None = None
    for i in range(1, 4001):
        lam = i / 1000.0
        g = [1.0 - math.exp(-lam * k) for k in ks]
        denom = sum(x * x for x in g)
        if denom < 1e-12:
            continue
        f_sat = sum(y * x for y, x in zip(ys, g)) / denom
        sse = sum((y - f_sat * x) ** 2 for y, x in zip(ys, g))
        if best is None or sse < best[2]:
            best = (lam, f_sat, sse)
    lam, f_sat, sse_best = best if best else (0.0, 0.0, 0.0)

    def fit_rate(k: int) -> float:
        return round(f_sat * (1 - math.exp(-lam * k)) / n * 100.0, 4)

    extrapolate = {
        "lambda": round(lam, 6),
        "f_sat_samples": round(f_sat, 2),
        "f_sat_pct_of_n": round(f_sat / n * 100.0, 4),
        "fit_at_k8_pct": fit_rate(8),
        "predicted_at_k16_pct": fit_rate(16),
        "predicted_at_k32_pct": fit_rate(32),
        "sse_samples2": round(sse_best, 3),
        "model": "f(k) = f_sat·(1 − e^{−λk})，**双参数**拟合（λ 网格搜索 + f_sat 闭式最小二乘）",
        "observed_plateau": {
            "plateau_from_k": next((c["k"] for c in curve
                                    if c["or_catch_rate_pct"] == curve[-1]["or_catch_rate_pct"]), None),
            "zero_marginal_assets": [c["asset_added"] for c in curve if c["marginal_gain_samples"] == 0],
            "note": "实测 k=6 即达 61.64%，k=7/8 边际为 0（两个结构性恒 unknown 资产）⇒ 曲线已平台",
        },
    }

    # 子模上界：f(k) ≤ f(8) + (k−8)·Δ_last，Δ_last = 最后一个**非零**边际
    nonzero = [m for m in margins if m > 0]
    d_last = nonzero[-1] if nonzero else 0
    f8 = len(cur)
    submodular_bound = {
        "f8_samples": f8,
        "last_nonzero_marginal_samples": d_last,
        "upper_bound_k16_samples": min(n, f8 + 8 * d_last),
        "upper_bound_k32_samples": min(n, f8 + 24 * d_last),
        "upper_bound_k16_pct": round(min(n, f8 + 8 * d_last) / n * 100.0, 4),
        "upper_bound_k32_pct": round(min(n, f8 + 24 * d_last) / n * 100.0, 4),
        "note": "由 f 子模 ⇒ 边际递减 ⇒ f(8+j) ≤ f(8) + j·Δ_last（684-A2 已实测验证子模性）",
    }

    # 与 684 的子模性交叉验证：随机抽 200 组 (S, a, b) 检验边际递减
    rng = random.Random(698)
    viol = 0
    tests = 0
    asset_list = [a for a in ASSETS if catch.get(a)]
    for _ in range(200):
        if len(asset_list) < 3:
            break
        k = rng.randint(1, len(asset_list) - 2)
        s = tuple(sorted(rng.sample(asset_list, k)))
        rest = [a for a in asset_list if a not in s]
        if len(rest) < 2:
            continue
        a, b = rng.sample(rest, 2)
        base = len(set().union(*[catch[x] for x in s])) if s else 0
        ga = len(set().union(*[catch[x] for x in s]) | catch[a]) - base
        gab = len(set().union(*[catch[x] for x in s]) | catch[a] | catch[b]) - base
        gb = len(set().union(*[catch[x] for x in s]) | catch[b]) - base
        # 子模性要求 Δ_a(S) ≥ Δ_a(S∪{b})
        da_s = ga
        da_sb = gab - gb
        tests += 1
        if da_s + 1e-9 < da_sb:
            viol += 1
    return {
        "n": n,
        "greedy_curve": curve,
        "marginals_diminishing": diminishing,
        "saturation_fit": extrapolate,
        "submodular_upper_bound": submodular_bound,
        "submodularity_random_check": {
            "tests": tests, "violations": viol,
            "pass": viol == 0,
            "note": "随机抽 200 组 (S,a,b) 检验 Δ_a(S) ≥ Δ_a(S∪{b})；与 684-A2 的结论交叉验证",
        },
        "honest_note": (
            "k>8 的外推是**模型外推**，不是实测：Queyi 只有 8 个资产。"
            "饱和曲线与子模上界给出的是**两个不同强度**的界 —— 前者是拟合（可能过拟合 8 个点），"
            "后者是**严格上界**（只要子模性成立就成立）。引用时应以后者为准。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 4. 三级操作化定义
# ══════════════════════════════════════════════════════════════════════════
def operational_levels(dec_table: dict[str, Any]) -> dict[str, Any]:
    levels: list[dict[str, Any]] = []
    for r in dec_table["table"]:
        q = r["catch_rate"]
        cls = r["decidability"]
        if q > 0.5:
            lvl, why = "L1", "现有检测器已可检测（>50%）"
        elif cls in ("D", "S"):
            lvl, why = "L2", "当前 <50%，但属 ∃-执行性质 ⇒ 换/加检测器在原理上可达"
        else:
            lvl, why = "L3", "需外部规约（oracle）才能判定 ⇒ 加检测器也难以根本解决"
        levels.append({
            "defect_type": r["defect_type"], "n": r["n"],
            "catch_rate": r["catch_rate"], "decidability": cls,
            "level": lvl, "why": why,
        })
    cnt = Counter(x["level"] for x in levels)
    by_lvl: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for x in levels:
        by_lvl[x["level"]].append(x)
    return {
        "definitions": {
            "L1": "现有检测器可检测（检出率 >50%）",
            "L2": "需要新检测器才能检测（当前 <50%，但缺陷属 ∃-执行性质 ⇒ 原理上可达）",
            "L3": "即使新检测器也很难（判定需外部规约 / oracle）",
        },
        "counts": dict(cnt),
        "by_level": {k: sorted(v, key=lambda d: -d["catch_rate"]) for k, v in sorted(by_lvl.items())},
        "sample_weighted_share": {
            k: round(sum(x["n"] for x in v) / sum(x["n"] for x in levels) * 100.0, 2)
            for k, v in by_lvl.items()
        },
    }


# ══════════════════════════════════════════════════════════════════════════
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="698-C 可检测性理论上限（只读）")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    rows, catch = load()
    n = len(rows)
    fam_idx = load_clone_families()
    _log.info("样本 %d；克隆家族索引 %d 项", n, len(fam_idx))

    dec = decidability_table(rows)
    out: dict[str, Any] = {
        "schema": "queyi-698/detectability-bound/v1",
        "generated_by": "tools/compute_698_detectability_bound.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "n": n,
        "decidability": dec,
        "information_bounds": information_bounds(rows, fam_idx),
        "capability_curve": capability_curve(catch, n),
        "operational_levels": operational_levels(dec),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    _log.info("已写出 %s", args.out)

    print("== 698-C 可检测性理论上限（只读）==")
    pv = dec["predictive_validity"]
    print(f"  可判定性分类：{dec['class_counts']}（共 {dec['n_types']} 类）")
    print(f"    S 类平均检出率={pv['mean_catch_rate_S']}  U 类={pv['mean_catch_rate_U']}  "
          f"差={pv['observed_difference']}  置换 p={pv['permutation_p_one_sided']}  ⇒ {pv['verdict']}")
    ib = out["information_bounds"]
    print(f"  信息论下界：族间(类型)={ib['by_defect_type_inter_family']['irreducible_error_pct']}%  "
          f"族内(克隆家族)={ib['by_clone_family_intra_family']['irreducible_error_pct']}%  "
          f"批次={ib['by_source_batch']['irreducible_error_pct']}%")
    cc = out["capability_curve"]
    print("  能力曲线（贪心）：" + " ".join(f"k{c['k']}={c['or_catch_rate_pct']:.2f}%" for c in cc["greedy_curve"]))
    print(f"    边际递减={cc['marginals_diminishing']}；子模随机抽检违规={cc['submodularity_random_check']['violations']}"
          f"/{cc['submodularity_random_check']['tests']}")
    print(f"    外推 k=16: 拟合 {cc['saturation_fit']['predicted_at_k16_pct']}% / "
          f"子模上界 {cc['submodular_upper_bound']['upper_bound_k16_pct']}%")
    print(f"    外推 k=32: 拟合 {cc['saturation_fit']['predicted_at_k32_pct']}% / "
          f"子模上界 {cc['submodular_upper_bound']['upper_bound_k32_pct']}%")
    ol = out["operational_levels"]
    print(f"  三级分级：{ol['counts']}；按样本量份额 {ol['sample_weighted_share']}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
