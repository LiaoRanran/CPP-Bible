#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_716_axiom_constructive.py — 716-1.3：A2/A5 反例的**构造性证明**（含机器验证）。

背景（700-A 的登记缺口）
======================
A2（撤除单调性）与 A5（超可加）（是真公理的）证据此前**完全来自** |X|=4、|A|=3 的 4096 结构
穷举模型检查（`tools/compute_700_axiom_independence.py`）。评审意见："穷举 ≠ 一般证明"。

本文件给出两个**构造性证明**（参数化于任意 n=|X| 与 |A|≥2，不依赖任何枚举）：

* 定理 A2w：`min_single` 口径（R(S)=min_{a∈S} |C_a|/n，R(∅)=0）违反 A2；
  非单调口径 `exactly_one`（恰被一个资产捕获）同样违反 A2（更强的见证）；
* 定理 A5w：`at_least_2` 口径（被 ≥2 个资产捕获）违反 A5（损害次可加）。

两条证明都是**一行代数**（见报告 §2/§3），枚举降级为"独立经验核对"：本文件用 700-A 的
检查器在 4096 结构上重算，确认 (i) 构造的见证在该域上确实违反对应公理；(ii) 不存在**反驳**
构造性定理的结构（定理不依赖域，枚举只是抽样核对）。

附带：登记缺口的**锐化尝试** —— A2 与 A5 的严格分离（存在违反 A2 但满足 A5 的口径）。
在"序统计量加权口径"（g(S)=Σ_i c_i·r_(i)，r_(i) 为池内逐资产率升序）这一族里做定向搜索：
找到 ⇒ 严格分离成立（构造性）；找不到 ⇒ 缺口**锐化后**登记（限定族内不存在）。

红线：`detect_calls = 0`；只读；只写 `data/716_*`。
用法：``python tools/compute_716_axiom_constructive.py``
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "tools"
sys.path.insert(0, str(HERE))
OUT = ROOT / "data" / "716_axiom_constructive.json"

N_SAMPLES, N_ASSETS = 4, 3
SAMPLES = tuple(range(N_SAMPLES))
ASSETS = ("a", "b", "c")


def load_700():
    spec = importlib.util.spec_from_file_location(
        "cm700", str(HERE / "compute_700_axiom_independence.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["cm700"] = mod
    spec.loader.exec_module(mod)
    return mod


# ═══════════════════════════════════════════════════════════════════════════
# 构造性见证：在任意 n、|A| 上展开（用 Fraction 精确算，不依赖浮点）
# ═══════════════════════════════════════════════════════════════════════════
def theorem_A2w(n: int, m: int) -> dict:
    """定理 A2w（min_single）：任意 n≥1、m≥2 的池上 A2 失效。

    构造：a 捕获空集，**其余每个资产都捕获全部样本**。
    则 R(A) = min(0, 1, …, 1) = 0，而 R(A\\{a}) = min(1, …, 1) = 1
    ⇒ R(τ_{{a}} M) = 1 > 0 = R(M) ⇒ A2 的 "R(τ_G M) ≤ R(M)" 失败。
    """
    cov = {"a": set(), "b": set(SAMPLES[:n])}
    for x in range(2, m):
        cov[chr(ord("a") + x)] = set(SAMPLES[:n])

    def R_min(pool: tuple[str, ...]) -> Fraction:
        if not pool:
            return Fraction(0)
        return min(Fraction(len(cov[a]), n) for a in pool)

    full = R_min(tuple(cov))
    after = R_min(tuple(a for a in cov if a != "a"))
    return {"n": n, "m": m, "R_full": str(full), "R_after_removing_a": str(after),
            "A2_clause_failed": after > full, "R_delta": str(after - full)}


def theorem_A2w_nonmonotone(n: int, m: int) -> dict:
    """定理 A2w'（exactly_one，非单调更强见证）：任意 n≥1、m≥2。

    构造：a、b 都恰好捕获同一个样本 x0（其余样本无人捕获），其余资产空。
    则 R(A) = 0（x0 被 2 个资产捕获），R(A\\{a}) = 1/n（x0 恰被 1 个捕获）。
    """
    cov = {"a": {0}, "b": {0}}
    for x in range(2, m):
        cov[chr(ord("a") + x)] = set()

    def R_exactly_one(pool: tuple[str, ...]) -> Fraction:
        cnt: Counter[int] = Counter()
        for a in pool:
            for x in cov[a]:
                cnt[x] += 1
        return Fraction(sum(1 for v in cnt.values() if v == 1), n)

    full = R_exactly_one(tuple(cov))
    after = R_exactly_one(tuple(a for a in cov if a != "a"))
    return {"n": n, "m": m, "R_full": str(full), "R_after_removing_a": str(after),
            "A2_clause_failed": after > full, "R_delta": str(after - full)}


def theorem_A5w(n: int, m: int) -> dict:
    """定理 A5w（at_least_2）：任意 n≥1、m≥2 的池上 A5 失效。

    构造：a、b 都恰好捕获样本 x0（≥2 个资产捕获 ⇒ R(A) ⊇ {x0}），其余资产空。
    h({{a}}) = R(A) − R(A\\{{a}}) = 1/n − 0，h({{b}}) 同；
    h({{a,b}}) = R(A) − R(A\\{{a,b}}) = 1/n − 0 < 2/n ⇒ A5（h(G∪H) ≥ h(G)+h(H)）失败。
    """
    cov = {"a": {0}, "b": {0}}
    for x in range(2, m):
        cov[chr(ord("a") + x)] = set()

    def R_at_least_2(pool: tuple[str, ...]) -> Fraction:
        cnt: Counter[int] = Counter()
        for a in pool:
            for x in cov[a]:
                cnt[x] += 1
        return Fraction(sum(1 for v in cnt.values() if v >= 2), n)

    full = R_at_least_2(tuple(cov))
    keep = lambda g: tuple(a for a in cov if a not in set(g))  # noqa: E731
    h_a = full - R_at_least_2(keep(("a",)))
    h_b = full - R_at_least_2(keep(("b",)))
    h_ab = full - R_at_least_2(keep(("a", "b")))
    return {"n": n, "m": m, "R_full": str(full), "h_a": str(h_a), "h_b": str(h_b),
            "h_ab": str(h_ab), "A5_clause_failed": h_ab < h_a + h_b,
            "gap": str(h_a + h_b - h_ab)}


# ═══════════════════════════════════════════════════════════════════════════
# 独立经验核对：700-A 检查器在 4096 结构上重算
# ═══════════════════════════════════════════════════════════════════════════
def empirical_crosscheck() -> dict:
    cm = load_700()
    structures = cm.all_coverages()
    out: dict = {"n_structures": len(structures), "per_aggregation": {}}
    for name, fn in cm.AGGREGATIONS.items():
        viol_a2 = sum(1 for cov in structures if not cm.check_a2(cov, fn))
        viol_a5 = sum(1 for cov in structures if not cm.check_a5(cov, fn))
        out["per_aggregation"][name] = {"A2_violating_structures": viol_a2,
                                        "A5_violating_structures": viol_a5}
    # 构造见证落回域内的实例（min_single / exactly_one / at_least_2 的最小见证）
    w_a2 = {"a": [0], "b": [0], "c": []}
    w_a2_min = {"a": [], "b": [0], "c": []}
    w_a5 = {"a": [0], "b": [0], "c": []}
    to_cov = lambda d: {a: frozenset(v) for a, v in d.items()}  # noqa: E731
    out["witnesses_in_domain"] = {
        "A2_min_single": {"coverage": w_a2_min,
                          "violates": not cm.check_a2(to_cov(w_a2_min), cm.AGGREGATIONS["min_single"]),
                          "satisfies_A5": cm.check_a5(to_cov(w_a2_min), cm.AGGREGATIONS["min_single"])},
        "A2_exactly_one": {"coverage": w_a2,
                           "violates": not cm.check_a2(to_cov(w_a2), cm.AGGREGATIONS["exactly_one_nonmonotone"]),
                           "satisfies_A5": cm.check_a5(to_cov(w_a2), cm.AGGREGATIONS["exactly_one_nonmonotone"])},
        "A5_at_least_2": {"coverage": w_a5,
                          "violates": not cm.check_a5(to_cov(w_a5), cm.AGGREGATIONS["at_least_2"]),
                          "satisfies_A2": cm.check_a2(to_cov(w_a5), cm.AGGREGATIONS["at_least_2"])},
    }
    # 严格分离：存在同时"违反 A2 且满足 A5"的（结构, 聚合）对吗？
    sep = []
    for name, fn in cm.AGGREGATIONS.items():
        for cov in structures:
            if not cm.check_a2(cov, fn) and cm.check_a5(cov, fn):
                sep.append(name)
                break
    out["strict_separation_in_7family"] = sorted(set(sep))
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 锐化缺口：序统计量加权族里的定向搜索（A2 违反 + A5 满足）
# ═══════════════════════════════════════════════════════════════════════════
def order_stat_family_search() -> dict:
    """族：g_c(S) = Σ_i c_i · r_(i)(S)，r_(i) 为池内逐资产率（升序），|S| ≤ 3。

    * 池为空 ⇒ g=0；|S|=1 ⇒ g = r_(1)；
    * 系数从 {-2,-1,-1/2,0,1/2,1,2} 里取（三系数、Σ|c| ≤ 4）⇒ 有限族；
    * 对全 4096 结构判定 A2/A5，找 "违反 A2 且满足 A5" 的成员。
    """
    cm = load_700()
    structures = cm.all_coverages()
    grid = [Fraction(-2), Fraction(-1), Fraction(-1, 2), Fraction(0),
            Fraction(1, 2), Fraction(1), Fraction(2)]

    def make_rule(c: tuple[Fraction, Fraction, Fraction]):
        def rule(cov: dict[str, frozenset[int]], pool: tuple[str, ...]) -> float:
            if not pool:
                return 0.0
            rates = sorted(len(cov[a]) / N_SAMPLES for a in pool)
            k = len(rates)
            if k == 1:
                return float(c[2]) * rates[0]
            if k == 2:
                return float(c[1] * Fraction(rates[0]).limit_denominator(10)
                             + c[2] * Fraction(rates[1]).limit_denominator(10))
            return float(sum(ci * Fraction(r).limit_denominator(10)
                             for ci, r in zip(c, rates)))
        return rule

    found = []
    found_ratelike = []
    for c in itertools.product(grid, repeat=3):
        if sum(abs(x) for x in c) > 4:
            continue
        fn = make_rule(c)
        ok_a5_all = True
        viol_a2 = False
        rate_like = True
        for cov in structures:
            if not cm.check_a2(cov, fn):
                viol_a2 = True
            if not cm.check_a5(cov, fn):
                ok_a5_all = False
                break
            vals = [fn(cov, pool) for pool in cm.SUBSETS]
            if min(vals) < -1e-12 or max(vals) > 1 + 1e-12:
                rate_like = False
        if viol_a2 and ok_a5_all:
            found.append([str(x) for x in c])
            if rate_like:
                found_ratelike.append([str(x) for x in c])
    return {"n_members_searched": len([c for c in itertools.product(grid, repeat=3)
                                       if sum(abs(x) for x in c) <= 4]),
            "separators_found": found[:12], "n_separators": len(found),
            "rate_like_separators": found_ratelike[:12],
            "n_rate_like_separators": len(found_ratelike),
            "verdict": ("构造性严格分离成立（族内存在违反 A2、满足 A5 的口径）" if found
                        else "族内未找到 ⇒ 缺口**锐化后**登记：严格分离仍开放（但已不限于 7 族）")}


def transform_mean_family_search() -> dict:
    """第二族（**pool-size 无关的一致族**）：g_φ(S) = mean_{a∈S} φ(r_a)，R(∅)=0。

    与上一族的区别：系数不随 |S| 重排，φ 作用在每个资产的率上 ⇒ 没有"同一条规则在
    不同池规模下含义漂移"的口径问题（这正是上一族分离者被质疑的地方）。φ(0) 约定为 0。

    φ 网格：r^p（p=1/2,1,2,3）、r+λr²（λ=−2,−1,−1/2,1/2,1,2,4）、ln(1+r)。
    """
    import math
    cm = load_700()
    structures = cm.all_coverages()

    def make(phi):
        def rule(cov: dict[str, frozenset[int]], pool: tuple[str, ...]) -> float:
            if not pool:
                return 0.0
            return sum(phi(len(cov[a]) / N_SAMPLES) for a in pool) / len(pool)
        return rule

    cands: dict[str, object] = {}
    for p in (0.5, 1.0, 2.0, 3.0):
        cands[f"r^{p}"] = (lambda r, p=p: r ** p)
    for lam in (-2.0, -1.0, -0.5, 0.5, 1.0, 2.0, 4.0):
        cands[f"r{lam:+.1f}r^2"] = (lambda r, lam=lam: r + lam * r * r)
    cands["ln(1+r)"] = (lambda r: math.log1p(r))

    out: dict = {}
    sep: list[str] = []
    for name, phi in cands.items():
        fn = make(phi)
        viol_a2 = any(not cm.check_a2(cov, fn) for cov in structures)
        viol_a5 = any(not cm.check_a5(cov, fn) for cov in structures)
        out[name] = {"violates_A2": viol_a2, "violates_A5": viol_a5}
        if viol_a2 and not viol_a5:
            sep.append(name)
    return {"family": "mean-of-transform（一致族）", "members": out,
            "separators": sep,
            "verdict": ("**一致族内即存在严格分离者**：%s ⇒ 缺口可关闭" % ", ".join(sep)
                        if sep else
                        "一致族内未找到分离者 ⇒ 缺口只被'秩加权族'部分锐化，仍然开放")}


def main() -> int:
    doc = {
        "schema": "queyi-716/axiom-constructive/v1",
        "generated_by": "tools/compute_716_axiom_constructive.py",
        "detect_calls": 0,
        "theorem_A2w_min_single": [theorem_A2w(n, m) for n, m in
                                   ((1, 2), (2, 2), (4, 3), (10, 8))],
        "theorem_A2w_exactly_one": [theorem_A2w_nonmonotone(n, m) for n, m in
                                    ((1, 2), (4, 3), (10, 8))],
        "theorem_A5w_at_least_2": [theorem_A5w(n, m) for n, m in
                                   ((1, 2), (4, 3), (10, 8))],
        "empirical_crosscheck": empirical_crosscheck(),
        "gap_sharpening_order_stat_family": order_stat_family_search(),
        "gap_sharpening_transform_mean_family": transform_mean_family_search(),
        "honesty": [
            "构造性定理覆盖**任意** n≥1、|A|≥2；4096 域枚举只作独立核对（不再承担证明责任）。",
            "两条定理证明的是'A2/A5 不是定理（有反例）'；它们**不**证明 A2/A5 的相互独立性"
            "（那仍是登记缺口，本批在序统计量族里做定向搜索并在 §gap 里如实登记结论）。",
            "min_single 的 A2 见证在域内还同时违反 A5（与 700-A 的观察一致）；"
            "exactly_one 亦然 —— 这一点未被本批的构造性证明改变。",
        ],
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8", newline="\n")
    print("== 716-1.3 A2/A5 构造性证明 ==")
    for k in ("theorem_A2w_min_single", "theorem_A2w_exactly_one", "theorem_A5w_at_least_2"):
        bad = [d for d in doc[k] if not any(v is True for kk, v in d.items()
                                           if "failed" in kk)]
        print(f"  {k}: {len(doc[k])} 个 (n,m) 实例，全部违反对应公理：{not bad}")
    ec = doc["empirical_crosscheck"]["witnesses_in_domain"]
    for name, w in ec.items():
        print(f"  域内核验 {name}: {json.dumps(w, ensure_ascii=False)}")
    g = doc["gap_sharpening_order_stat_family"]
    print(f"  严格分离搜索（秩加权族）：族成员 {g['n_members_searched']}，"
          f"找到 {g['n_separators']} 个分离者（其中 rate-like {g['n_rate_like_separators']}）")
    t = doc["gap_sharpening_transform_mean_family"]
    print(f"  严格分离搜索（一致族 mean-of-transform）：分离者={t['separators']}")
    for name, v in t["members"].items():
        print(f"    {name:<10} A2违反={v['violates_A2']}  A5违反={v['violates_A5']}")
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
