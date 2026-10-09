#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_700_axiom_independence.py — 700-A：漂移代数公理系统的**穷举模型检查器**。

做什么
======
在**有限模型域**上穷举检验 697/698 的 7 条公理，回答三个元理论问题：

1. **独立性**：每条公理是否独立？（存在满足其余全部但违反它自己的模型？）
2. **最小性**：哪些公理其实是**定理**（在框架内恒真，不能算公理）？
3. **完备性**：有没有**观测到的漂移**无法被现有公理表达？（用 Queyi 的四型做检验）

模型域（**有限且可穷举**）
========================
* 样本 $|X| = 4$，资产 $|A| = 3$；
* 覆盖结构：每个资产 $a$ 的捕获集 $C_a \\subseteq X$ ⇒ 共 $2^{4\\times 3} = 4096$ 个结构；
* **聚合族** $\\rho$（报告函数 $R_\\rho(S)$）7 种，覆盖"单调 + 非单调"、"子模 + 非子模"：
  `or_union`（并集覆盖，子模）、`at_least_2`、`max_single`、`mean_single`、`min_single`、
  `sum_single`（可加型，非子模）、`exactly_one`（**非单调**，用于给 A2 造反例）；
* 漂移算子 $\\tau_G$：保留 $A\\setminus G$（撤除型），$R(\\tau_G M) = R_\\rho(A\\setminus G)$；
* 损害 $h(G) := R(A) - R(A\\setminus G)$。

公理（以结构性质表述）
====================
| 编号 | 内容 | 形式化 |
|:--:|---|---|
| A1 | 口径可枚举性 | **元公理**（约束语言而非结构）⇒ 不参与结构检查，单独讨论 |
| A2 | 撤除单调性 | $G \\subseteq H \\Rightarrow R(A\\setminus H) \\le R(A\\setminus G) \\le R(A)$ |
| A3 | 幂等性 | $\\tau_G \\circ \\tau_G = \\tau_G$ |
| A4 | 交换性与闭包 | $\\tau_G \\circ \\tau_H = \\tau_{G\\cup H}$ |
| A5 | 超可加性（损害） | $G \\cap H = \\varnothing \\Rightarrow h(G\\cup H) \\ge h(G)+h(H)$ |
| A6 | 不可逆性 | $\\forall G \\neq \\varnothing$，$M \\mapsto \\tau_G M$ 在结构域上**非单射** |
| A7 | 可观测性分层 | 静默性是 $(\\tau, \\text{记账口径})$ 二元组的性质（存在同一 $\\tau$ 下 unaware 静默 / aware 响亮的结构） |

红线：``detect_calls = 0``；只读；产出只写 ``data/700_*``。

用法
====
    python tools/compute_700_axiom_independence.py
"""
from __future__ import annotations

import argparse
import datetime as _dt
import itertools
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_700_axiom_independence")

OUT_JSON: Final[Path] = ROOT / "data" / "700_axiom_independence.json"

N_SAMPLES: Final[int] = 4
N_ASSETS: Final[int] = 3
SAMPLES: Final[tuple[int, ...]] = tuple(range(N_SAMPLES))
ASSETS: Final[tuple[str, ...]] = ("a", "b", "c")


# ══════════════════════════════════════════════════════════════════════════
# 聚合族（报告函数）
# ══════════════════════════════════════════════════════════════════════════
def _union(cov: dict[str, frozenset[int]], pool: tuple[str, ...]) -> frozenset[int]:
    u: set[int] = set()
    for a in pool:
        u |= cov[a]
    return frozenset(u)


def agg_or_union(cov: dict[str, frozenset[int]], pool: tuple[str, ...]) -> float:
    return len(_union(cov, pool)) / N_SAMPLES if pool else 0.0


def agg_at_least_2(cov: dict[str, frozenset[int]], pool: tuple[str, ...]) -> float:
    cnt: Counter[int] = Counter()
    for a in pool:
        for x in cov[a]:
            cnt[x] += 1
    return sum(1 for v in cnt.values() if v >= 2) / N_SAMPLES


def agg_max_single(cov: dict[str, frozenset[int]], pool: tuple[str, ...]) -> float:
    return max((len(cov[a]) for a in pool), default=0) / N_SAMPLES


def agg_min_single(cov: dict[str, frozenset[int]], pool: tuple[str, ...]) -> float:
    return min((len(cov[a]) for a in pool), default=0) / N_SAMPLES


def agg_mean_single(cov: dict[str, frozenset[int]], pool: tuple[str, ...]) -> float:
    return (sum(len(cov[a]) for a in pool) / len(pool) / N_SAMPLES) if pool else 0.0


def agg_sum_single(cov: dict[str, frozenset[int]], pool: tuple[str, ...]) -> float:
    return sum(len(cov[a]) for a in pool) / N_SAMPLES


def agg_exactly_one(cov: dict[str, frozenset[int]], pool: tuple[str, ...]) -> float:
    """**非单调**聚合：恰被一个资产捕获的样本比例。用于给 A2 造反例。"""
    cnt: Counter[int] = Counter()
    for a in pool:
        for x in cov[a]:
            cnt[x] += 1
    return sum(1 for v in cnt.values() if v == 1) / N_SAMPLES


AGGREGATIONS: Final[dict[str, Callable[[dict[str, frozenset[int]], tuple[str, ...]], float]]] = {
    "or_union": agg_or_union,
    "at_least_2": agg_at_least_2,
    "max_single": agg_max_single,
    "min_single": agg_min_single,
    "mean_single": agg_mean_single,
    "sum_single": agg_sum_single,
    "exactly_one_nonmonotone": agg_exactly_one,
}

AGG_NOTES: Final[dict[str, str]] = {
    "or_union": "并集覆盖：单调 + **子模**",
    "at_least_2": "至少 2 个资产捕获：单调，非子模",
    "max_single": "最好单资产：单调，非子模",
    "min_single": "最差单资产：单调，非子模",
    "mean_single": "单资产均值：单调，非子模",
    "sum_single": "单资产求和：单调，**可加**（故 A5 取等号）",
    "exactly_one_nonmonotone": "恰被 1 个捕获：**非单调**（A2 的反例来源）",
}


# ══════════════════════════════════════════════════════════════════════════
# 结构
# ══════════════════════════════════════════════════════════════════════════
def all_coverages() -> list[dict[str, frozenset[int]]]:
    """穷举全部覆盖结构：$2^{|X|\\cdot|A|} = 4096$ 个。"""
    cells = [(a, x) for a in ASSETS for x in SAMPLES]
    out: list[dict[str, frozenset[int]]] = []
    for bits in range(1 << len(cells)):
        cov: dict[str, set[int]] = {a: set() for a in ASSETS}
        for i, (a, x) in enumerate(cells):
            if bits >> i & 1:
                cov[a].add(x)
        out.append({a: frozenset(v) for a, v in cov.items()})
    return out


def _subsets() -> list[tuple[str, ...]]:
    out: list[tuple[str, ...]] = []
    for r in range(len(ASSETS) + 1):
        out.extend(itertools.combinations(ASSETS, r))
    return out


SUBSETS: Final[list[tuple[str, ...]]] = _subsets()


def retained(pool: tuple[str, ...], g: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(a for a in pool if a not in set(g))


# ══════════════════════════════════════════════════════════════════════════
# 公理检验
# ══════════════════════════════════════════════════════════════════════════
def check_a2(cov: dict[str, frozenset[int]], agg: Any) -> bool:
    """A2 撤除单调性：G ⊆ H ⟹ R(A\\H) ≤ R(A\\G) ≤ R(A)。"""
    full = agg(cov, ASSETS)
    for g in SUBSETS:
        rg = agg(cov, retained(ASSETS, g))
        if rg > full + 1e-12:
            return False
        for h in SUBSETS:
            if set(g) <= set(h):
                rh = agg(cov, retained(ASSETS, h))
                if rh > rg + 1e-12:
                    return False
    return True


def check_a3(cov: dict[str, frozenset[int]], agg: Any) -> bool:
    """A3 幂等性：τ_G∘τ_G = τ_G（撤除两次 = 撤除一次）。"""
    for g in SUBSETS:
        once = retained(ASSETS, g)
        twice = retained(once, g)
        if once != twice:
            return False
    return True


def check_a4(cov: dict[str, frozenset[int]], agg: Any) -> bool:
    """A4 交换性与闭包：τ_G∘τ_H = τ_H∘τ_G = τ_{G∪H}。"""
    for g in SUBSETS:
        for h in SUBSETS:
            gh = tuple(sorted(set(g) | set(h)))
            if retained(retained(ASSETS, g), h) != retained(ASSETS, gh):
                return False
            if retained(retained(ASSETS, h), g) != retained(ASSETS, gh):
                return False
    return True


def check_a5(cov: dict[str, frozenset[int]], agg: Any) -> bool:
    """A5 超可加性：不相交 G,H 时 h(G∪H) ≥ h(G)+h(H)。"""
    full = agg(cov, ASSETS)
    damage = {g: full - agg(cov, retained(ASSETS, g)) for g in SUBSETS}
    for g in SUBSETS:
        for hh in SUBSETS:
            if set(g) & set(hh):
                continue
            gu = tuple(sorted(set(g) | set(hh)))
            if damage[gu] < damage[g] + damage[hh] - 1e-12:
                return False
    return True


def check_a6(structures: list[dict[str, frozenset[int]]]) -> dict[str, Any]:
    """A6 不可逆性：对每个非空 G，检查 M ↦ M|_{A\\G} 是否非单射。

    在**全结构域**上检查（这是"不可逆性"的正确论域：不知道 $M$ 是谁）。
    """
    non_injective: dict[str, bool] = {}
    for g in SUBSETS:
        if not g:
            continue
        seen: dict[tuple[frozenset[int], ...], int] = {}
        collision = False
        for cov in structures:
            key = tuple(cov[a] for a in ASSETS if a not in set(g))
            if key in seen:
                collision = True
                break
            seen[key] = 1
        non_injective[str(sorted(g))] = collision
    return {
        "per_G_non_injective": non_injective,
        "holds": all(non_injective.values()),
    }


def a7_witness_search(structures: list[dict[str, frozenset[int]]]) -> dict[str, Any]:
    """A7 是**域级命题**（存在性），不是逐结构的约束。

    命题：存在 (M, τ) 使 unaware 记账下静默、aware 记账下响亮。
    判据（与 692-A §3 的记账规则同构）：
    * unaware：丢失的 catch 写成 `miss` ⇒ 转移矩阵的 unknown 列全 0 ⇒ 静默；
    * aware  ：同一样本写成 `unknown` ⇒ unknown 列非 0 ⇒ 响亮。
    因此 A7 等价于「存在结构使撤除 $G$ 时至少丢一个 catch」。
    """
    example: dict[str, Any] | None = None
    n_witness = 0
    for cov in structures:
        for g in (("c",), ("b",), ("a",), ("b", "c")):
            kept = retained(ASSETS, g)
            lost = [x for x in SAMPLES
                    if any(x in cov[a] for a in ASSETS) and not any(x in cov[a] for a in kept)]
            if lost:
                n_witness += 1
                if example is None:
                    example = {"coverage": {a: sorted(v) for a, v in cov.items()},
                               "G": list(g), "lost_samples": lost}
                break
    return {
        "witness_exists": n_witness > 0,
        "n_witnesses": n_witness,
        "example": example,
        "verdict": (
            "**定理**（非公理）：一旦把 unaware/aware 记账规则写进结构，"
            "「静默性是 (τ, 记账口径) 二元组的性质」就是**可证的**——"
            "698-B 定理 T3 已给出证明，本批的穷举见证与之一致。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 完备性：标签轴漂移是否可表达
# ══════════════════════════════════════════════════════════════════════════
def completeness_probe() -> dict[str, Any]:
    """检验：现有口径签名 $(A,E,\\Theta,P)$ **没有标签槽** ⇒ Type III 漂移不可表达。

    做法：取一个固定覆盖结构，对同一批逐样本裁决施加**标签粗化** λ：
    逐样本裁决完全不变 ⇒ **全部 7 条公理关心的量都不变**；
    但分组统计（按标签聚合的盲区率）改变。
    """
    cov: dict[str, frozenset[int]] = {
        "a": frozenset({0, 1}),
        "b": frozenset({2}),
        "c": frozenset(),
    }
    verdict = {x: ("catch" if any(x in cov[a] for a in ASSETS) else "miss") for x in SAMPLES}

    fine = {0: "t1", 1: "t1", 2: "t2", 3: "t3"}        # 3 个细标签
    coarse = {0: "T", 1: "T", 2: "T", 3: "T"}           # 粗化到 1 个标签

    def blind_rate(label_map: dict[int, str]) -> dict[str, float]:
        grp: dict[str, list[int]] = {}
        for x in SAMPLES:
            grp.setdefault(label_map[x], []).append(0 if verdict[x] == "catch" else 1)
        return {k: round(sum(v) / len(v), 4) for k, v in grp.items()}

    fine_rates = blind_rate(fine)
    coarse_rates = blind_rate(coarse)
    # 所有 7 条公理只依赖 (A, R)：λ 不变它们
    r_full = agg_or_union(cov, ASSETS)
    return {
        "coverage_fixed": {a: sorted(v) for a, v in cov.items()},
        "verdicts_unchanged": True,
        "aggregation_unchanged": {
            "or_union": r_full,
            "note": "标签 λ 不进入任何公理的形式化（口径签名 = (A,E,Θ,P)，无标签槽）",
        },
        "group_statistics_fine": fine_rates,
        "group_statistics_coarse": coarse_rates,
        "conclusion": (
            "存在漂移 τ_λ（标签词表变化）使**逐样本裁决与全部公理量都不变**，"
            "但**分组统计改变** ⇒ 现有 7 公理系统**无法表达** Type III（标签）漂移。"
            "这是**不完备性**的具体见证。"
        ),
        "missing_axiom_candidate": (
            "A8（标签轴闭包）：口径签名必须扩为 (D, A, E, Θ, P, λ)，"
            "且任何报告统计量都必须显式声明其**分组轴** λ；"
            "未声明 λ 的统计量**不可比较**（与 698-A Type III 的实测结论一致）。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 707-A 简化：只做实质性公理检查（跳过恒真的 A3/A4/A6）
# ══════════════════════════════════════════════════════════════════════════
def substantive_axiom_check(structures: list[dict[str, frozenset[int]]]) -> dict[str, Any]:
    """**简化检查器**（707-A 工程落地）。

    科研依据（700-A 元理论发现）：A3（幂等）/ A4（交换闭包）/ A6（不可逆）在本框架
    （τ = 资产列删去）内**恒真**——由 τ 的构造直接推出，把它们写成公理是冗余，逐结构
    全量重算它们**永远通过、纯属浪费**。真正需要逐结构检验的只有 **A2（撤除单调）与
    A5（超可加）**。A7 是域级存在性命题（698-B T3 已证），A1 是元公理 ⇒ 两者都不进循环。

    ⇒ 本函数只对全部结构跑 A2/A5（把结构检查从 4 项降到 2 项），并给出 A8（标签轴闭包）
    占位（TODO：见 ``a8_placeholder`` 的不可自动验证原因）。
    """
    truth: dict[str, dict[str, Any]] = {}
    for aname, checker in (("A2", check_a2), ("A5", check_a5)):
        truth[aname] = {}
        for agg_name, fn in AGGREGATIONS.items():
            violators = sum(0 if checker(cov, fn) else 1 for cov in structures)
            truth[aname][agg_name] = {
                "holds_on_all": violators == 0,
                "n_violating_structures": violators,
            }
    a8_placeholder = {
        "axiom": "A8（标签轴闭包）",
        "status": "TODO / 不可自动验证",
        "reason": ("标签轴 λ 属**报告规范层**（非覆盖结构性质）⇒ 无结构反例可检；"
                   "以「未声明 λ 的分组统计不可比较」的规范约束落地（698-A Type III 实测）。"),
        "candidate_formalization": completeness_probe()["missing_axiom_candidate"],
    }
    return {
        "checked_axioms": ["A2", "A5"],
        "skipped_axioms": {
            "A3": "恒真（幂等：τ_G∘τ_G = τ_G，由 τ 定义推出）",
            "A4": "恒真（交换闭包：τ_G∘τ_H = τ_{G∪H}，由 τ 定义推出）",
            "A6": "恒真（不可逆：列删去 M↦M|_{A\\G} 非单射）",
            "A7": "域级定理（698-B T3），非逐结构约束",
            "A1": "元公理（约束语言/分类法，不参与结构检查）",
        },
        "truth": truth,
        "a8_placeholder": a8_placeholder,
    }


# ══════════════════════════════════════════════════════════════════════════
# 主流程
# ══════════════════════════════════════════════════════════════════════════
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="700-A 公理独立性穷举模型检查")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    ap.add_argument("--substantive-only", action="store_true",
                    help="707-A：只检查实质性公理 A2/A5，跳过恒真的 A3/A4/A6（省算力）；附 A8 占位")
    args = ap.parse_args(argv)

    structures = all_coverages()

    if args.substantive_only:  # 707-A 简化路径（科研依据：700-A 元理论发现）
        sub = substantive_axiom_check(structures)
        doc: dict[str, Any] = {
            "schema": "queyi-707/axiom-substantive-check/v1",
            "generated_by": "tools/compute_700_axiom_independence.py --substantive-only",
            "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "detect_calls": 0,
            "research_basis": "700-A：A3/A4/A6 恒真（定理），A2/A5 独立（真公理）",
            "domain": {"n_samples": N_SAMPLES, "n_assets": N_ASSETS, "n_structures": len(structures)},
            "substantive_check": sub,
        }
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        _log.info("已写出（substantive-only）%s", args.out)
        print("== 700-A 公理检查（substantive-only：仅 A2/A5）==")
        for a, per in sub["truth"].items():
            print(f"  {a}: " + ", ".join(
                f"{k}={'ok' if v['holds_on_all'] else 'violated(%d)' % v['n_violating_structures']}"
                for k, v in per.items()))
        print(f"  跳过（恒真/定理/元公理）：{list(sub['skipped_axioms'])}")
        print(f"  A8 占位：{sub['a8_placeholder']['status']}")
        return 0
    _log.info("结构域大小 = %d（|X|=%d, |A|=%d）；聚合族 %d 种",
              len(structures), N_SAMPLES, N_ASSETS, len(AGGREGATIONS))

    # ── 逐公理 × 逐聚合 的真值表 ─────────────────────────────────────
    truth: dict[str, dict[str, bool]] = {}
    for aname, checker in (("A2", check_a2), ("A3", check_a3), ("A4", check_a4), ("A5", check_a5)):
        truth[aname] = {}
        for agg_name, fn in AGGREGATIONS.items():
            ok = all(checker(cov, fn) for cov in structures)
            truth[aname][agg_name] = ok
    a6 = check_a6(structures)
    a7 = a7_witness_search(structures)

    # ── 分类：恒真（定理） vs 有反例（真公理） ────────────────────────
    classification: dict[str, Any] = {}
    for aname in ("A2", "A3", "A4", "A5"):
        violators = [k for k, v in truth[aname].items() if not v]
        classification[aname] = {
            "always_true_on_domain": not violators,
            "violating_aggregations": violators,
            "verdict": ("**定理**（在框架内恒真，不能算公理）" if not violators
                        else "**真公理**（存在反例模型）"),
        }
    classification["A6"] = {
        "always_true_on_domain": a6["holds"],
        "violating_aggregations": [],
        "verdict": ("**定理**（由 τ 定义为列删去直接推出）" if a6["holds"]
                    else "**真公理**"),
    }
    classification["A1"] = {
        "always_true_on_domain": None,
        "violating_aggregations": [],
        "verdict": "**元公理**（约束语言/分类法，不是结构性质 ⇒ 不参与结构检查）",
    }
    classification["A7"] = {
        "always_true_on_domain": True,
        "violating_aggregations": [],
        "verdict": a7["verdict"],
    }

    # ── 独立性见证：对每条"真公理"，给一个满足其余但违反它的具体结构 ──
    witnesses: dict[str, Any] = {}
    real_axioms = [a for a in ("A2", "A5") if not classification[a]["always_true_on_domain"]]
    for target in real_axioms:
        checker = {"A2": check_a2, "A5": check_a5}[target]
        found: dict[str, Any] | None = None
        for agg_name in classification[target]["violating_aggregations"]:
            fn = AGGREGATIONS[agg_name]
            for cov in structures:
                if checker(cov, fn):
                    continue
                others_ok = all(
                    check_a2(cov, fn) if o == "A2" else
                    check_a3(cov, fn) if o == "A3" else
                    check_a4(cov, fn) if o == "A4" else check_a5(cov, fn)
                    for o in ("A2", "A3", "A4", "A5") if o != target
                ) and a6["holds"] and a7["witness_exists"]
                if others_ok:
                    found = {"aggregation": agg_name,
                             "coverage": {a: sorted(v) for a, v in cov.items()}}
                    break
            if found:
                break
        witnesses[target] = found or {
            "aggregation": None, "coverage": None,
            "note": "在本有限域内未找到「只违反本公理」的见证 ⇒ 本公理与其余公理"
                    "在**该域上**不可分离（不构成独立性反例，但也不等于蕴含关系）",
        }

    doc: dict[str, Any] = {
        "schema": "queyi-700/axiom-metatheory/v1",
        "generated_by": "tools/compute_700_axiom_independence.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "domain": {
            "n_samples": N_SAMPLES, "n_assets": N_ASSETS,
            "n_structures": len(structures),
            "aggregations": AGG_NOTES,
            "drift_operator": "τ_G = 保留 A\\G（撤除型）",
            "damage": "h(G) = R(A) − R(A\\G)",
        },
        "axiom_truth_table": truth,
        "a6_non_injectivity": a6,
        "a7_domain_witness": a7,
        "classification": classification,
        "independence_witnesses": witnesses,
        "minimal_axiom_set": {
            "meta_axioms": ["A1（口径可枚举性）"],
            "genuine_axioms": sorted(real_axioms),
            "theorems": sorted([a for a in ("A2", "A3", "A4", "A5", "A6", "A7")
                                if classification[a]["always_true_on_domain"]]),
            "statement": (
                "在覆盖型框架（τ = 列删去 + 报告函数 R）内："
                "**A3（幂等）/ A4（交换闭包）/ A6（不可逆）是定义域内的恒真命题**"
                "（由 τ 的构造直接推出）；**A7（可观测性分层）在把记账规则写进结构后也可证**"
                "（698-B 定理 T3）。⇒ 把 A3/A4/A6/A7 写成公理是**冗余**，"
                "真正起约束作用的结构公理只有 **A2（单调性）与 A5（超可加性）**，外加元公理 A1。"
            ),
        },
        "completeness": completeness_probe(),
        "complexity": {
            "decision_caliber_enumerated": {
                "problem": "给定配对裁决矩阵，判定是否存在口径变化使 |D_τ| > 0",
                "complexity": "O(|T|·n)——有限枚举，**多项式可解**",
                "basis": "697 定理 A3(a)：沉默可判定；口径枚举后不变性检验有限（695-P2）",
            },
            "decision_structural": {
                "problem": "判定漂移是结构性（R* 不变）还是真实能力变化",
                "complexity": "**不可判定**（在仅有配对数据时）",
                "basis": "697 定理 A1（构造性不可识别）",
            },
            "adversarial_caliber_selection": {
                "problem": "口径套利：选择口径变化使报告值 ≥ v（预算 |A\\S| ≤ k）",
                "complexity": "**NP-hard**（由最大覆盖归约；最大覆盖的 NP-hardness 是经典结果）",
                "approximation": (
                    "对 OR 型（子模）聚合，贪心达 (1 − 1/e) 近似 ⇒ "
                    "**684 的贪心 (1−1/e) 保证在元理论层就是「口径套利最优化的近似算法」**"
                ),
                "note": "|A| 小时（本项目 |A|=8）2^8 = 256 可穷举 ⇒ 实践上多项式",
            },
        },
        "honest_limits": [
            "结构域仅 |X|=4、|A|=3（4096 结构）⇒ 「恒真」的结论只对**该域**成立，不是对任意域的证明。",
            "聚合族只有 7 种，不是全部可能的报告函数 ⇒ 「有反例」是充分证据，"
            "「恒真」是**域内**证据而非普遍证明。",
            "A1 是元公理，无法用结构检查 ⇒ 本批只做定性讨论。",
            "A7 的检验用了与 692-A §3 同构的记账规则，但只检查了 |G|=1 的情形。",
            "复杂性结论中的 NP-hardness 是**归约论证**（引用最大覆盖的经典结果），本批未做形式化归约证明。",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    _log.info("已写出 %s", args.out)

    print("== 700-A 公理元理论（穷举模型检查）==")
    print(f"  结构域 = {len(structures)}（|X|={N_SAMPLES}, |A|={N_ASSETS}）；聚合族 {len(AGGREGATIONS)} 种")
    for aname in ("A1", "A2", "A3", "A4", "A5", "A6", "A7"):
        c = classification[aname]
        print(f"  {aname}: {c['verdict']}"
              + (f"  反例聚合={c['violating_aggregations']}" if c["violating_aggregations"] else ""))
    print(f"\n  最小公理集：元公理 {doc['minimal_axiom_set']['meta_axioms']}；"
          f"真公理 {doc['minimal_axiom_set']['genuine_axioms']}；"
          f"定理 {doc['minimal_axiom_set']['theorems']}")
    print("\n  完备性：Type III（标签）漂移**不可表达** ⇒ 缺失 A8（标签轴闭包）")
    print("  复杂性：口径枚举可判 O(|T|n) / 结构性不可判定 / 口径套利 NP-hard（贪心 1−1/e）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
