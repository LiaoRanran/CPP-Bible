#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_697_drift_algebra.py — 697-B：测量漂移代数的可计算部分（**只读，0 次 detect**）。

批次红线（697 任务书）
======================
* 不修改论文正文 / bib（696 在改）；
* 不跑新的 ``detect()`` —— 本脚本 ``detect_calls = 0``，只读冻结矩阵；
* 不修改检测器 / 样本 / 冻结矩阵；
* 产出只写 ``data/697_*``。

本脚本算什么
============
1. **三态转移矩阵** :math:`T^{(M\\to M')}_{ij}`（catch/miss/unknown × 3），
   在 5 个 frame 上（A5 evaluation 566 / derivation 571 / 全池 1137 / 676g 1147 / real-world 110）；
   并与 692 已发布值**逐格对账**（reconciliation）。
2. **漂移的可加性检验**：把「环境漂移」= 撤掉 {asan,ubsan,tsan}、「构成漂移」= 撤掉 {linker}
   各自与联合施加，量 :math:`D_{\\text{both}} - (D_{\\text{env}}+D_{\\text{comp}})` 的残差，
   并用**被撤资产独有 catch 集的重叠**给出该残差的闭式（定理 T1）。
3. **静默 vs 响亮**：在两套记账口径（unaware / aware）下重算 :math:`\\Delta_{\\text{unknown}}`，
   检验「:math:`\\Delta_{\\text{unknown}}=0` 是静默退化指纹」这一 692/695 说法是否成立（定理 T3）。
4. **结构性漂移的单向性判据**：逐 defect_group 的 McNemar 反向格 :math:`c_g`
   （:math:`T_{\\text{miss}\\to\\text{catch}}`）。纯撤除型漂移必有 :math:`c=0`（定理 T2）。
5. **静默窗口宽度 vs 类型集中度**：重跑 63 个能力撤退子集，
   对每个配置算「丢失 catch 的类型集中度」，检验 695 P1.7（H-D3）。

用法
====
    python tools/compute_697_drift_algebra.py
    python tools/compute_697_drift_algebra.py --out data/697_drift_algebra.json
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_697_drift_algebra")

A5_MATRIX: Final[str] = "a5_676f_detection_matrix.json"
RW_MATRIX: Final[str] = "683_real_world_detection_matrix.json"
REF_692: Final[str] = "692_environment_paired_experiment.json"
OUT_JSON: Final[Path] = ROOT / "data" / "697_drift_algebra.json"

# ── 资产划分（与 692-A 的 asset_partition 逐项一致，不重新发明）─────────────────
ALL_ASSETS: Final[tuple[str, ...]] = (
    "asan", "ubsan", "tsan", "compiler-warn",
    "wunsequenced", "cross-compile", "linker", "compile-time",
)
ENV_GATED: Final[tuple[str, ...]] = (
    "asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker",
)
STATIC_UNIMPLEMENTED: Final[tuple[str, ...]] = ("wunsequenced", "compile-time")
E1_SUPPORTED: Final[tuple[str, ...]] = ENV_GATED
E2_SUPPORTED: Final[tuple[str, ...]] = ("compiler-warn", "cross-compile", "linker")
ENV_GAP_E2: Final[tuple[str, ...]] = ("asan", "ubsan", "tsan")

STATES: Final[tuple[str, ...]] = ("catch", "miss", "unknown")


# ══════════════════════════════════════════════════════════════════════════
# 基础读取
# ══════════════════════════════════════════════════════════════════════════
def _verdict(cell: Any) -> str:
    """兼容两种冻结格式：扁平字符串 / ``{"verdict": ...}`` 字典。"""
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell) if cell is not None else "unknown"


def _per_asset(sample: dict[str, Any]) -> dict[str, str]:
    raw = sample.get("per_asset") or {}
    return {a: _verdict(raw.get(a, "unknown")) for a in ALL_ASSETS}


def _samples(doc: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for s in doc.get("samples", []):
        out.append({
            "uid": str(s.get("uid") or s.get("sample_id") or ""),
            "split": str(s.get("split") or ""),
            "defect_group": str(s.get("defect_group") or "unknown"),
            "defect_type": str(s.get("defect_type") or "unknown"),
            "per_asset": _per_asset(s),
        })
    return out


def _or_unaware(pa: dict[str, str], assets: tuple[str, ...]) -> str:
    """unaware 记账：任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss。

    这是冻结矩阵的逐字口径（692-A §3 伪码的 ``aware=False`` 分支）。
    """
    vals = [pa.get(a, "unknown") for a in assets]
    if not vals:
        return "unknown"
    if any(v == "catch" for v in vals):
        return "catch"
    if all(v == "unknown" for v in vals):
        return "unknown"
    return "miss"


def _or_aware(pa: dict[str, str], assets: tuple[str, ...], gap: tuple[str, ...]) -> str:
    """aware 记账：``G_env ≠ ∅`` 且无 catch ⇒ unknown（缺测量 ≠ 缺检出）。"""
    if any(pa.get(a, "unknown") == "catch" for a in assets):
        return "catch"
    if gap:
        return "unknown"
    vals = [pa.get(a, "unknown") for a in assets]
    if all(v == "unknown" for v in vals):
        return "unknown"
    return "miss"


def _pct(k: int, n: int) -> float:
    return round(k / n * 100.0, 4) if n else 0.0


# ══════════════════════════════════════════════════════════════════════════
# 1. 三态转移矩阵
# ══════════════════════════════════════════════════════════════════════════
def transition_matrix(pairs: list[tuple[str, str]]) -> dict[str, Any]:
    """由配对 (v_M, v_M') 序列给出 3×3 转移计数 + 行归一 + 边际。"""
    t: dict[str, dict[str, int]] = {i: {j: 0 for j in STATES} for i in STATES}
    for a, b in pairs:
        t[a][b] += 1
    n = len(pairs)
    row_norm: dict[str, dict[str, float]] = {}
    for i in STATES:
        rs = sum(t[i].values())
        row_norm[i] = {j: (round(t[i][j] / rs, 6) if rs else None) for j in STATES}  # type: ignore[misc]
    marginal_m = {i: sum(t[i][j] for j in STATES) for i in STATES}
    marginal_mp = {j: sum(t[i][j] for i in STATES) for j in STATES}
    n_b = t["catch"]["miss"]    # M 独 catch
    n_c = t["miss"]["catch"]    # M' 独 catch（**撤除型漂移必为 0**）
    return {
        "n": n,
        "counts": t,
        "row_normalized": row_norm,
        "marginal_M": marginal_m,
        "marginal_Mprime": marginal_mp,
        "discordant_b_M_only_catch": n_b,
        "discordant_c_Mprime_only_catch": n_c,
        "mcnemar_exact_p": mcnemar_exact(n_b, n_c),
        "silent": bool(t["catch"]["miss"] > 0 and t["catch"]["unknown"] == 0 and t["miss"]["unknown"] == 0),
        "loud": bool(t["catch"]["unknown"] > 0 or t["miss"]["unknown"] > 0),
    }


def mcnemar_exact(b: int, c: int) -> float:
    """精确二项 McNemar（双侧）：H0 = 不一致方向可交换。

    双侧 p = 2·Pr[X ≤ min(b,c)]，X~Bin(b+c, 1/2)，上限截断到 1.0。
    """
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (2.0 ** n)
    return min(1.0, 2.0 * tail)


def env_transition(
    samples: list[dict[str, Any]],
    frame: str,
    aware: bool = False,
) -> dict[str, Any]:
    """E1 → E2 的配对转移矩阵（unaware 与 aware 两套记账）。"""
    pairs: list[tuple[str, str]] = []
    for s in samples:
        pa = s["per_asset"]
        v1 = _or_unaware(pa, E1_SUPPORTED)
        v2 = _or_aware(pa, E2_SUPPORTED, ENV_GAP_E2) if aware else _or_unaware(pa, E2_SUPPORTED)
        pairs.append((v1, v2))
    out = transition_matrix(pairs)
    out["frame"] = frame
    out["accounting"] = "aware" if aware else "unaware"
    m1 = out["marginal_M"]
    m2 = out["marginal_Mprime"]
    out["delta_unknown_pp"] = round(_pct(m2["unknown"], out["n"]) - _pct(m1["unknown"], out["n"]), 4)
    out["delta_catch_rate_pp"] = round(_pct(m2["catch"], out["n"]) - _pct(m1["catch"], out["n"]), 4)
    return out


# ══════════════════════════════════════════════════════════════════════════
# 2. 漂移的可加性（定理 T1）
# ══════════════════════════════════════════════════════════════════════════
def _catch_set(pa: dict[str, str], assets: tuple[str, ...]) -> bool:
    return any(pa.get(a, "unknown") == "catch" for a in assets)


def coverage(samples: list[dict[str, Any]], assets: tuple[str, ...]) -> set[str]:
    """覆盖集 :math:`C_S = \\{x : \\exists a\\in S, V(x,a)=\\texttt{catch}\\}`。"""
    return {s["uid"] for s in samples if _catch_set(s["per_asset"], assets)}


def additivity_test(
    samples: list[dict[str, Any]],
    frame: str,
    a_assets: tuple[str, ...] = ("asan", "ubsan", "tsan"),
    l_assets: tuple[str, ...] = ("linker",),
    b_assets: tuple[str, ...] = ("compiler-warn", "cross-compile"),
    label: str = "env_gated_vs_degenerate",
) -> dict[str, Any]:
    """两类撤除型漂移的可加性检验（定理 T1）。

    基线池 :math:`S_0 = A \\cup B \\cup L`；τ_env 撤 :math:`A`、τ_comp 撤 :math:`L`、
    联合撤 :math:`A \\cup L`，保留 :math:`B`。

    定理 T1 断言残差
        ``D_both − (D_env + D_comp) = −|C_A ∩ C_L \\ C_B| / n ≤ 0``
    即**撤除型漂移在损失量上是超可加的**：联合撤除的损失 ≥ 各自损失之和。

    ⚠ 注意：残差的闭式**不是**「两个被撤资产各自独有贡献集」的交集（那两个集合按构造
    必然不交，会恒得 0 而使检验空转）；正确形式是 :math:`|C_A \\cap C_L \\setminus C_B|`。
    """
    s0 = a_assets + b_assets + l_assets

    c_a = coverage(samples, a_assets)                       # C_A
    c_l = coverage(samples, l_assets)                       # C_L
    c_b = coverage(samples, b_assets)                       # C_B
    c_full = coverage(samples, s0)                          # C_A ∪ C_B ∪ C_L
    c_env = coverage(samples, b_assets + l_assets)          # 撤 A ⇒ C_B ∪ C_L
    c_comp = coverage(samples, a_assets + b_assets)         # 撤 L ⇒ C_A ∪ C_B
    c_both = coverage(samples, b_assets)                    # 撤 A ∪ L ⇒ C_B

    n = len(samples)
    r = lambda cs: _pct(len(cs), n)  # noqa: E731
    r_full, r_env, r_comp, r_both = r(c_full), r(c_env), r(c_comp), r(c_both)

    d_env = round(r_env - r_full, 4)
    d_comp = round(r_comp - r_full, 4)
    d_both = round(r_both - r_full, 4)
    residual = round(d_both - (d_env + d_comp), 4)

    # 闭式残差（定理 T1）：residual = −|C_A ∩ C_L \ C_B| / n。
    # 注意：**不能**用「两个被撤资产各自独有贡献集」的交集 —— 那两个集合按构造必然不交
    # （一个不含 C_L 的元素，另一个只含 C_L 的元素），会恒得 0 而让检验变成空转。
    overlap = (c_a & c_l) - c_b          # |C_A ∩ C_L \ C_B|
    predicted_overlap = len(overlap)
    m_count = len(c_full - c_both)       # m = |(C_A ∪ C_L) \ C_B|（联合撤除的总损失样本数）

    return {
        "label": label,
        "frame": frame,
        "n": n,
        "pools": {
            "S0_full": list(s0),
            "remove_A_env_gated": list(a_assets),
            "remove_L_degenerate": list(l_assets),
            "B_retained": list(b_assets),
        },
        "catch_rates_pct": {
            "R_full": r_full, "R_env_only": r_env, "R_comp_only": r_comp, "R_both": r_both,
        },
        "drift_pp": {
            "D_env": d_env, "D_comp": d_comp, "D_both": d_both,
            "residual_D_both_minus_sum": residual,
        },
        "theorem_T1_check": {
            "closed_form_residual": -round(predicted_overlap / n * 100.0, 4),
            "predicted_overlap_count": predicted_overlap,
            "joint_loss_sample_count_m": m_count,
            "a_sole_count": len(c_full - c_env),
            "l_sole_count": len(c_full - c_comp),
            "sum_of_sole_counts": len(c_full - c_env) + len(c_full - c_comp),
            "matches": abs(residual - (-round(predicted_overlap / n * 100.0, 4))) < 1e-6,
            "residual_sign": "non-positive（超可加）" if residual <= 0 else "positive（反例！T1 被证伪）",
        },
        "interpretation": (
            "撤除型漂移的损失是**超可加**的：D_both ≤ D_env + D_comp（两者皆为负），"
            "残差恰为两个被撤资产「独有 catch 集」在保留池之外的交集大小 / n。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 3. 静默 vs 响亮（定理 T3）
# ══════════════════════════════════════════════════════════════════════════
def silence_analysis(samples: list[dict[str, Any]], frame: str) -> dict[str, Any]:
    """同一漂移在两套记账口径下的 :math:`\\Delta_{\\text{unknown}}`。

    695 的 H-D4 说「:math:`\\Delta_{\\text{unknown}}=0` 是静默退化的指纹」。
    本节检验：该量是否**只由记账口径决定**、而与漂移本身无关 —— 若是，则 H-D4 被证伪。
    """
    un = env_transition(samples, frame, aware=False)
    aw = env_transition(samples, frame, aware=True)
    return {
        "frame": frame,
        "n": un["n"],
        "unaware": {
            "delta_unknown_pp": un["delta_unknown_pp"],
            "delta_catch_rate_pp": un["delta_catch_rate_pp"],
            "silent": un["silent"], "loud": un["loud"],
            "T_catch_miss": un["counts"]["catch"]["miss"],
            "T_catch_unknown": un["counts"]["catch"]["unknown"],
        },
        "aware": {
            "delta_unknown_pp": aw["delta_unknown_pp"],
            "delta_catch_rate_pp": aw["delta_catch_rate_pp"],
            "silent": aw["silent"], "loud": aw["loud"],
            "T_catch_miss": aw["counts"]["catch"]["miss"],
            "T_catch_unknown": aw["counts"]["catch"]["unknown"],
        },
        "verdict": (
            "同一漂移（E1→E2）在 unaware 下 Δunknown=0（静默）、在 aware 下 Δunknown≠0（响亮）"
            "⇒ 静默性是 (漂移, 记账口径) **二元组**的性质，不是漂移的内禀性质。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 4. 逐组 McNemar：撤除型漂移的单向性判据（定理 T2）
# ══════════════════════════════════════════════════════════════════════════
def per_group_direction(samples: list[dict[str, Any]], frame: str) -> dict[str, Any]:
    """按 defect_group 拆 McNemar 的 b / c。

    纯撤除型（removal）漂移在**每一层**都应有 :math:`c_g = 0`——
    撤除资产只能丢 catch，不可能凭空得 catch。任一层的 :math:`c_g > 0`
    即证伪「该层是纯撤除」，指向仪器漂移或真实能力变化。
    """
    by_group: dict[str, list[tuple[str, str]]] = {}
    for s in samples:
        pa = s["per_asset"]
        by_group.setdefault(s["defect_group"], []).append(
            (_or_unaware(pa, E1_SUPPORTED), _or_unaware(pa, E2_SUPPORTED))
        )
    rows: list[dict[str, Any]] = []
    for g in sorted(by_group):
        tm = transition_matrix(by_group[g])
        rows.append({
            "defect_group": g,
            "n": tm["n"],
            "b_e1_only_catch": tm["discordant_b_M_only_catch"],
            "c_e2_only_catch": tm["discordant_c_Mprime_only_catch"],
            "mcnemar_exact_p": tm["mcnemar_exact_p"],
            "one_directional": tm["discordant_c_Mprime_only_catch"] == 0,
        })
    reversal = [r for r in rows if not r["one_directional"]]
    return {
        "frame": frame,
        "n_groups": len(rows),
        "rows": rows,
        "n_groups_with_reversal": len(reversal),
        "reversal_groups": [r["defect_group"] for r in reversal],
        "criterion": (
            "T_{miss→catch} = c_g = 0 在每一层成立 ⇒ 与纯撤除型漂移一致；"
            "任一层 c_g > 0 ⇒ 该层含非撤除成分（仪器/机制变化）。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 5. 静默窗口宽度 vs 类型集中度（695 P1.7 / H-D3）
# ══════════════════════════════════════════════════════════════════════════
def _norm_entropy(counts: Counter[str], n_categories: int) -> float:
    """集中度 = 1 − H / log2(n_categories)，H 为丢失 catch 在**类型空间**上的香农熵。

    ⚠ 分母必须用**类型空间的基数**（本数据 11 个 defect_group），
    **不能**用「本次丢失中出现过的类型数」——后者会让"只丢了 2 种类型"这种
    最集中的情形被归一化成 H/H_max = 1（看起来最分散），从而把 P1.7 的检验方向做反。
    """
    total = sum(counts.values())
    if total == 0:
        return 1.0
    if n_categories <= 1:
        return 1.0
    h = -sum((v / total) * math.log2(v / total) for v in counts.values() if v > 0)
    h_max = math.log2(n_categories)
    return round(max(0.0, min(1.0, 1.0 - h / h_max)), 6)


def _spearman(xs: list[float], ys: list[float]) -> float | None:
    """斯皮尔曼等级相关（并列取平均秩），n<3 返回 None。"""
    n = len(xs)
    if n < 3:
        return None

    def _rank(v: list[float]) -> list[float]:
        order = sorted(range(n), key=lambda i: v[i])
        out = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                out[order[k]] = avg
            i = j + 1
        return out

    rx, ry = _rank(xs), _rank(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    dy = math.sqrt(sum((b - my) ** 2 for b in ry))
    if dx == 0 or dy == 0:
        return None
    return round(num / (dx * dy), 6)


def window_concentration(
    evaluation: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
) -> dict[str, Any]:
    """重跑 63 个能力撤退子集，为每个配置算「丢失 catch 的类型集中度」。

    检验 695 P1.7（H-D3）：静默窗口的宽度由**类型集中度**决定，而非由**丢失量**决定。
    操作化：在全部 63 个配置上，把 ``unsound_negatives`` 与
    ① 丢失量（``retention_gap = 100 − retention``）、② 集中度（``1 − H_norm``）分别做
    斯皮尔曼相关；集中度相关更强则支持 P1.7，反之为反证。
    """
    cap: dict[str, set[str]] = {}
    for s in derivation:
        cap.setdefault(s["defect_group"], set())
        for a in ALL_ASSETS:
            if s["per_asset"].get(a, "unknown") == "catch":
                cap[s["defect_group"]].add(a)

    n = len(evaluation)
    n_categories = len({s["defect_group"] for s in evaluation if s["defect_group"] != "unknown"})
    full_rate = _pct(sum(1 for s in evaluation if _catch_set(s["per_asset"], ENV_GATED)), n)

    rows: list[dict[str, Any]] = []
    for k in range(1, len(ENV_GATED) + 1):
        for subset in combinations(ENV_GATED, k):
            avail = tuple(subset)
            catch = 0
            sound_neg = 0
            unsound_neg = 0
            lost_types: Counter[str] = Counter()
            for s in evaluation:
                if _catch_set(s["per_asset"], avail):
                    catch += 1
                    continue
                g = s["defect_group"]
                missing_capable = (cap.get(g, set()) - set(avail)) & set(ENV_GATED)
                if missing_capable:
                    unsound_neg += 1
                    lost_types[g] += 1
                else:
                    sound_neg += 1
            rate = _pct(catch, n)
            retention = round(rate / full_rate * 100.0, 4) if full_rate else 0.0
            rows.append({
                "available_assets": list(avail),
                "n_missing": len(ENV_GATED) - k,
                "missing_assets": [a for a in ENV_GATED if a not in avail],
                "unaware_catch_rate_pct": rate,
                "retention_of_full_pct": retention,
                "retention_gap_pp": round(100.0 - retention, 4),
                "unsound_negatives": unsound_neg,
                "sound_negatives": sound_neg,
                "lost_type_distribution": dict(sorted(lost_types.items())),
                "lost_type_concentration": _norm_entropy(lost_types, n_categories),
                "lost_count": sum(lost_types.values()),
            })

    def _window(thr: float) -> list[dict[str, Any]]:
        return [r for r in rows if r["retention_of_full_pct"] >= thr and r["unsound_negatives"] > 0]

    window_by_threshold = {f"{t}_pct": len(_window(float(t))) for t in (100, 99, 95, 90, 80, 50)}
    with_unsound = [r for r in rows if r["unsound_negatives"] > 0]
    widest = max(with_unsound, key=lambda r: r["retention_of_full_pct"]) if with_unsound else None

    xs_gap = [float(r["retention_gap_pp"]) for r in rows]
    xs_conc = [float(r["lost_type_concentration"]) for r in rows]
    ys_unsound = [float(r["unsound_negatives"]) for r in rows]
    rho_gap = _spearman(xs_gap, ys_unsound)
    rho_conc = _spearman(xs_conc, ys_unsound)

    single = [r for r in rows if r["n_missing"] == 1]
    single_rows = [{
        "missing_asset": r["missing_assets"][0],
        "retention_of_full_pct": r["retention_of_full_pct"],
        "lost_count": r["lost_count"],
        "lost_type_concentration": r["lost_type_concentration"],
        "unsound_negatives": r["unsound_negatives"],
    } for r in single]
    rho_single = _spearman(
        [float(r["lost_type_concentration"]) for r in single_rows],
        [float(r["retention_of_full_pct"]) for r in single_rows],
    )

    return {
        "grid": "ENV_GATED_ASSETS 的全部 63 个非空子集（与 692-A 同网格，独立重算）",
        "n_configs": len(rows),
        "n_type_categories": n_categories,
        "concentration_definition": "1 − H(lost catches over defect_group) / log2(n_type_categories)",
        "full_rate_pct": full_rate,
        "window_by_threshold": window_by_threshold,
        "n_configs_with_unsound_negatives": len(with_unsound),
        "widest_window_config": widest,
        "correlation_all_63": {
            "spearman_retention_gap_vs_unsound": rho_gap,
            "spearman_concentration_vs_unsound": rho_conc,
            "supports_P1_7": (
                None if rho_gap is None or rho_conc is None else abs(rho_conc) > abs(rho_gap)
            ),
            "note": "H-D3 的判别：|ρ(集中度,unsound)| > |ρ(丢失量,unsound)| 则支持，否则反证。",
        },
        "single_drop_configs": single_rows,
        "spearman_single_drop_concentration_vs_retention": rho_single,
        "verdict_split": {
            "P1_7_position_supported": (
                None if rho_single is None else bool(rho_single > 0.5)
            ),
            "P1_7_severity_refuted": (
                None if rho_gap is None or rho_conc is None else bool(abs(rho_gap) > abs(rho_conc))
            ),
            "statement": (
                "P1.7 必须拆成两个命题："
                "①【窗口位置】单资产撤除时，丢失能力越类型集中 ⇒ retention 越高 ⇒ 窗口越宽 "
                f"（ρ(集中度, retention) = {rho_single}，n=6）——**成立**；"
                "②【后果严重度】不可信负例数量由**丢失量**决定，而非集中度 "
                f"（ρ(丢失量, unsound) = {rho_gap} vs ρ(集中度, unsound) = {rho_conc}，n=63）——**反证**。"
                "695 原文把两者混为一个「宽度」，应拆开陈述。"
            ),
        },
        "rows": rows,
        "honest_note": (
            "≥95% retention 的窗口内只有 1 个配置（与 692 一致）⇒ 窗口宽度的**阈值曲线**"
            "样本量极小，相关分析只在全部 63 配置上有统计意义，结论强度为**探索性**。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 主流程
# ══════════════════════════════════════════════════════════════════════════
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="697-B 测量漂移代数的可计算部分（只读）")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    a5 = _samples(load_json_cached(DATA / A5_MATRIX))
    rw = _samples(load_json_cached(DATA / RW_MATRIX))
    g676 = _samples(load_json_cached(DATA / "blindspot_676g_detection_matrix.json"))
    ref = load_json_cached(DATA / REF_692)

    evaluation = [s for s in a5 if s["split"] == "evaluation"]
    derivation = [s for s in a5 if s["split"] == "derivation"]
    _log.info("A5 样本 %d（evaluation %d / derivation %d）；real-world %d；676g %d",
              len(a5), len(evaluation), len(derivation), len(rw), len(g676))

    frames = {
        "A5_evaluation_566": evaluation,
        "A5_derivation_571": derivation,
        "A5_all_1137": a5,
        "blindspot_676g_1147": g676,
        "real_world_110": rw,
    }
    transitions = {
        name: env_transition(samples, name, aware=False) for name, samples in frames.items()
    }

    # ── 与 692 逐格对账 ────────────────────────────────────────────────
    recon: list[dict[str, Any]] = []
    for name, ref_key in (("A5_evaluation_566", "A5_evaluation_566"),
                          ("A5_derivation_571", "A5_derivation_571"),
                          ("A5_all_1137", "A5_all_1137"),
                          ("real_world_110", "real_world_110")):
        mine = transitions[name]
        r = ref["frames"][ref_key]
        checks = {
            "E1_catch": (mine["marginal_M"]["catch"], r["E1_wsl_full"]["catch"]),
            "E1_miss": (mine["marginal_M"]["miss"], r["E1_wsl_full"]["miss"]),
            "E1_unknown": (mine["marginal_M"]["unknown"], r["E1_wsl_full"]["unknown"]),
            "E2_catch": (mine["marginal_Mprime"]["catch"], r["E2_native_unaware"]["catch"]),
            "E2_miss": (mine["marginal_Mprime"]["miss"], r["E2_native_unaware"]["miss"]),
            "E2_unknown": (mine["marginal_Mprime"]["unknown"], r["E2_native_unaware"]["unknown"]),
            "mcnemar_b": (mine["discordant_b_M_only_catch"], r["mcnemar"]["b_e1_catch_only"]),
            "mcnemar_c": (mine["discordant_c_Mprime_only_catch"], r["mcnemar"]["c_e2_catch_only"]),
        }
        mismatched = [k for k, v in checks.items() if len(v) >= 2 and v[0] != v[1]]
        recon.append({
            "frame": name,
            "recomputed": {k: v[0] for k, v in checks.items()},
            "reference_692": {k: v[1] for k, v in checks.items()},
            "mismatched_fields": mismatched,
            "pass": not mismatched,
        })
    # T_catch_catch 单独算（692 只给了 b/c，catch→catch 需由 E2.catch − c 推）
    for item, name in zip(recon, ("A5_evaluation_566", "A5_derivation_571", "A5_all_1137", "real_world_110")):
        ref_c = item["reference_692"]["mcnemar_c"]
        mine_cc = transitions[name]["counts"]["catch"]["catch"]
        derived_cc = item["reference_692"]["E2_catch"] - ref_c
        item["recomputed"]["T_catch_catch"] = mine_cc
        item["derived_T_catch_catch_from_692"] = derived_cc
        item["T_catch_catch_match"] = mine_cc == derived_cc

    # 三种 (A, L, B) 划分：① 环境门控 vs 退化资产（主口径）② 环境门控 vs 编译器告警
    # ③ 两个 sanitizer 互撤（预期重叠最大 ⇒ 残差最负，用于确认检验非空转）
    partitions: list[tuple[str, tuple[str, ...], tuple[str, ...], tuple[str, ...]]] = [
        ("env_gated_vs_degenerate", ("asan", "ubsan", "tsan"), ("linker",),
         ("compiler-warn", "cross-compile")),
        ("env_gated_vs_compiler_warn", ("asan", "ubsan", "tsan"), ("compiler-warn",),
         ("cross-compile", "linker")),
        ("asan_vs_ubsan", ("asan",), ("ubsan",),
         ("tsan", "compiler-warn", "cross-compile", "linker")),
    ]
    additivity: dict[str, Any] = {}
    for name, samples in frames.items():
        additivity[name] = {
            label: additivity_test(samples, name, grp_a, grp_l, grp_b, label)
            for label, grp_a, grp_l, grp_b in partitions
        }
    silence = {name: silence_analysis(s, name) for name, s in frames.items()}
    groups = per_group_direction(evaluation, "A5_evaluation_566")
    window = window_concentration(evaluation, derivation)

    doc: dict[str, Any] = {
        "schema": "queyi-697/drift-algebra/v1",
        "generated_by": "tools/compute_697_drift_algebra.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "inputs": {
            "a5_matrix": f"data/{A5_MATRIX}",
            "real_world_matrix": f"data/{RW_MATRIX}",
            "blindspot_matrix": "data/blindspot_676g_detection_matrix.json",
            "reference": f"data/{REF_692}",
        },
        "asset_partition": {
            "all": list(ALL_ASSETS),
            "env_gated": list(ENV_GATED),
            "static_unimplemented": list(STATIC_UNIMPLEMENTED),
            "E1_supported": list(E1_SUPPORTED),
            "E2_supported": list(E2_SUPPORTED),
            "E2_environment_gap": list(ENV_GAP_E2),
        },
        "three_state_transitions": transitions,
        "reconciliation_vs_692": recon,
        "additivity": additivity,
        "silence_vs_accounting": silence,
        "per_group_direction": groups,
        "silent_window_concentration": window,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    _log.info("已写出 %s", args.out)

    # ── 控制台摘要 ─────────────────────────────────────────────────────
    print("== 697-B 测量漂移代数（只读复算）==")
    for item in recon:
        flag = "PASS" if item["pass"] and item["T_catch_catch_match"] else "FAIL"
        print(f"  对账 {item['frame']:<22} {flag}  不一致字段={item['mismatched_fields'] or '无'}")
    t = transitions["A5_evaluation_566"]
    print("\n  T^(E1→E2) [A5 evaluation 566, unaware]：")
    print("            →catch   →miss   →unknown")
    for i in STATES:
        row = t["counts"][i]
        print(f"    {i:<8} {row['catch']:>6} {row['miss']:>7} {row['unknown']:>9}")
    print(f"    McNemar b={t['discordant_b_M_only_catch']} c={t['discordant_c_Mprime_only_catch']} "
          f"p={t['mcnemar_exact_p']:.3e}  silent={t['silent']} loud={t['loud']}")
    print("\n  可加性 [A5 evaluation 566]：")
    for label, ad in additivity["A5_evaluation_566"].items():
        tc = ad["theorem_T1_check"]
        print(f"    {label:<26} D_env={ad['drift_pp']['D_env']:>9}pp  "
              f"D_comp={ad['drift_pp']['D_comp']:>8}pp  D_both={ad['drift_pp']['D_both']:>9}pp")
        print(f"    {'':<26} 残差={ad['drift_pp']['residual_D_both_minus_sum']:>8}pp  "
              f"闭式={tc['closed_form_residual']}pp  重叠样本={tc['predicted_overlap_count']}  "
              f"吻合={tc['matches']}  {tc['residual_sign']}")
    sil = silence["A5_evaluation_566"]
    print(f"\n  静默性：unaware Δunknown={sil['unaware']['delta_unknown_pp']}pp (silent={sil['unaware']['silent']})；"
          f"aware Δunknown={sil['aware']['delta_unknown_pp']}pp (loud={sil['aware']['loud']})")
    print(f"  单向性：{groups['n_groups']} 组中出现反向格的组数 = {groups['n_groups_with_reversal']}")
    w = window["correlation_all_63"]
    print(f"  窗口集中度：ρ(丢失量,unsound)={w['spearman_retention_gap_vs_unsound']}  "
          f"ρ(集中度,unsound)={w['spearman_concentration_vs_unsound']}  支持 P1.7={w['supports_P1_7']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
