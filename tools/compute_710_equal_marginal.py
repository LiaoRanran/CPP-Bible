#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
r"""compute_710_equal_marginal.py — 710-C1：F1「等边际替换」设计的**只读近似**。

科研依据
========
论文 F1（``research/latex/queyi_neurips2027_v1.1.tex`` 行 428–452）与 677c：
* 全池 $k{=}4$：FD 54.6% vs Random 30.6% ⇒ $\Delta = +24.03$pp（$n{=}566$）；
* Pool A（5 非退化资产）$k{=}1$：$+11.31$pp（$p{=}6.0\times10^{-8}$）；$k{=}4$：$0.00$pp；
* 论文自述：「**composition from mechanism 的分离需要等边际替换设计（we did not run）**」。

本脚本不跑任何新 ``detect()``，只用**已有冻结矩阵**做四类**只读重排**近似：

| # | 近似 | 回答的问题 |
|---|---|---|
| A | **族外选择增益**（clone-family 分折：训练折选资产、测试折评） | +11.31pp 是**选择技能**还是**同一批样本上的构成/记忆**？ |
| B | **外部资产池替换**（692-B 的 clang-tidy / cppcheck 四口径逐样本裁决，同一 566 帧） | 换成**完全不同的资产池**后，选择增益还在吗（≈机制）还是消失（≈池构成）？ |
| C | **列置换零假设**（保持每个资产的 catch 计数 = 等边际，打乱样本对齐） | 观测增益超过「只靠边际异质性 + 偶然对齐」多少？ |
| D | **缺陷类型边际重加权**（把 566 帧的 defect_group 边际重加权到语料/均匀边际） | 选择增益对**样本侧边际**有多敏感？ |

红线：``detect_calls = 0``；只读 ``data/a5_676f_detection_matrix.json``、
``data/692_fair_comparison_raw.jsonl``、``data/677b_clone_families.json``；
**未修改**检测器/样本/冻结矩阵；**0 处**论文正文/bib 修改。
输出：``data/710_equal_marginal.json``。

用法
====
    python tools/compute_710_equal_marginal.py [--perm 400]
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import random
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any, Final, Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_710_equal_marginal")

OUT_JSON: Final[Path] = ROOT / "data" / "710_equal_marginal.json"

A5: Final[str] = "a5_676f_detection_matrix.json"
FAIR_RAW: Final[str] = "692_fair_comparison_raw.jsonl"
FAMILIES: Final[str] = "677b_clone_families.json"

POOL_ALL: Final[tuple[str, ...]] = (
    "asan", "ubsan", "tsan", "compiler-warn", "wunsequenced", "cross-compile",
    "linker", "compile-time",
)
POOL_A: Final[tuple[str, ...]] = ("asan", "compiler-warn", "cross-compile", "tsan", "ubsan")
EXTERNAL_POOL: Final[tuple[str, ...]] = (
    "T1_clang_tidy_C_main", "T2_clang_tidy_C_A",
    "T3_cppcheck_warning", "T4_cppcheck_broad",
)

# 692 的池定义（``data/677c_asset_pools.json``）
POOL_DEFS: Final[dict[str, tuple[str, ...]]] = {
    "full8": POOL_ALL,
    "PoolA(5)": POOL_A,
    "PoolB/C(6)": ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker"),
}


# ══════════════════════════════════════════════════════════════════════════
# 读数
# ══════════════════════════════════════════════════════════════════════════
def _verdict(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell) if cell is not None else "unknown"


def load_families() -> dict[str, str]:
    doc = load_json_cached(DATA / FAMILIES)
    idx: dict[str, str] = {}
    for fid, members in (doc.get("family_index") or {}).items():
        for m in members:
            idx[str(m)] = str(fid)
    return idx


def load_eval_rows() -> list[dict[str, Any]]:
    doc = load_json_cached(DATA / A5)
    fam = load_families()
    rows: list[dict[str, Any]] = []
    for s in doc.get("samples", []):
        if str(s.get("split")) != "evaluation":
            continue
        sid = str(s.get("sample_id"))
        rows.append({
            "uid": sid,
            "defect_type": str(s.get("defect_type") or "unknown"),
            "defect_group": str(s.get("defect_group") or "unknown"),
            "per_asset": {a: _verdict((s.get("per_asset") or {}).get(a, "unknown"))
                          for a in POOL_ALL},
            "family": fam.get(sid) or f"single::{sid}",
        })
    return rows


def load_external_verdicts() -> dict[str, dict[str, str]]:
    """从 692-B 原始 jsonl 逐样本重建四口径裁决（catch/miss/unknown）。"""
    out: dict[str, dict[str, str]] = defaultdict(dict)
    with open(DATA / FAIR_RAW, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            uid, tool = str(rec["uid"]), str(rec["tool"])
            diags = rec.get("diags") or []
            bad = rec.get("status") in ("no_source", "timeout", "compile_error", "tool_error")
            names = (("T1_clang_tidy_C_main", "T2_clang_tidy_C_A") if tool == "clang-tidy"
                     else ("T3_cppcheck_warning", "T4_cppcheck_broad"))
            if bad:
                for n in names:
                    out[uid][n] = "unknown"
                continue
            if tool == "clang-tidy":
                out[uid][names[0]] = "catch" if diags else "miss"
                out[uid][names[1]] = ("catch" if any(
                    str(d.get("check", "")).startswith("clang-analyzer-") for d in diags)
                    else "miss")
            else:
                out[uid][names[0]] = ("catch" if any(
                    str(d.get("severity")) in ("error", "warning") for d in diags) else "miss")
                out[uid][names[1]] = "catch" if diags else "miss"
    return out


# ══════════════════════════════════════════════════════════════════════════
# 报告函数：加权 OR 覆盖率 + 精确随机臂
# ══════════════════════════════════════════════════════════════════════════
def _catches(rows: list[dict[str, Any]], subset: Iterable[str],
             key: str = "per_asset") -> list[int]:
    subset = tuple(subset)
    out = []
    for r in rows:
        pa = r[key]
        out.append(1 if any(pa.get(a) == "catch" for a in subset) else 0)
    return out


def rate(rows: list[dict[str, Any]], subset: Iterable[str],
         weights: list[float] | None = None, key: str = "per_asset") -> float:
    c = _catches(rows, subset, key)
    if weights is None:
        return sum(c) / len(c) if c else 0.0
    num = sum(ci * wi for ci, wi in zip(c, weights))
    den = sum(weights)
    return num / den if den else 0.0


def exact_random_mean(rows: list[dict[str, Any]], pool: tuple[str, ...], k: int,
                      weights: list[float] | None = None,
                      key: str = "per_asset") -> float:
    """随机臂**精确期望**（枚举 $\binom{|P|}{k}$ 个子集，不是抽样）。"""
    subs = list(combinations(pool, k))
    if not subs:
        return 0.0
    return sum(rate(rows, s, weights, key) for s in subs) / len(subs)


def greedy_set_cover(rows: list[dict[str, Any]], pool: tuple[str, ...], k: int,
                     weights: list[float] | None = None,
                     key: str = "per_asset") -> tuple[str, ...]:
    """684/698 的贪心口径：每次选**边际增益最大**的资产（加权）。"""
    chosen: list[str] = []
    covered = [0] * len(rows)
    w = weights if weights is not None else [1.0] * len(rows)
    for _ in range(min(k, len(pool))):
        best, best_gain = None, -1.0
        for a in pool:
            if a in chosen:
                continue
            gain = 0.0
            for i, r in enumerate(rows):
                if covered[i] == 0 and r[key].get(a) == "catch":
                    gain += w[i]
            if gain > best_gain + 1e-12:
                best, best_gain = a, gain
        if best is None:
            break
        chosen.append(best)
        for i, r in enumerate(rows):
            if r[key].get(best) == "catch":
                covered[i] = 1
    return tuple(chosen)


def freq_topk(rows: list[dict[str, Any]], pool: tuple[str, ...], k: int,
              weights: list[float] | None = None) -> tuple[str, ...]:
    """677c 的 FD 口径（frequency ≡ fd）：按**原始 catch 计数**取前 k。"""
    w = weights if weights is not None else [1.0] * len(rows)
    cnt = {a: sum(w[i] for i, r in enumerate(rows) if r["per_asset"].get(a) == "catch")
           for a in pool}
    return tuple(sorted(pool, key=lambda a: (-cnt[a], a))[:k])


def group_folds(groups: list[str], folds: int, seed: int = 697) -> dict[str, int]:
    """与 ``tools/train_697_predictor.py::group_folds`` 逐字同口径（同组必同折）。"""
    sizes: Counter[str] = Counter(groups)
    order = sorted(sizes, key=lambda g: (-sizes[g], g))
    rng = random.Random(seed)
    rng.shuffle(order)
    load = [0] * folds
    assign: dict[str, int] = {}
    for g in order:
        f = min(range(folds), key=lambda k: load[k])
        assign[g] = f
        load[f] += sizes[g]
    return assign


# ══════════════════════════════════════════════════════════════════════════
# 协议 A：族外选择增益
# ══════════════════════════════════════════════════════════════════════════
def protocol_a(rows: list[dict[str, Any]], folds_n: int = 5) -> dict[str, Any]:
    folds = group_folds([r["family"] for r in rows], folds_n)
    out: dict[str, Any] = {"protocol": "族外选择增益（家族分折：训练折选资产、测试折评）",
                           "folds": folds_n, "seed": 697, "pools": {},
                           "selectors": {"fd": "frequency top-k（677c 的 FD 口径）",
                                         "greedy": "684/698 贪心 set-cover（边际增益）"}}
    for pname, pool in POOL_DEFS.items():
        per_k: list[dict[str, Any]] = []
        for k in range(1, len(pool) + 1):
            rec: dict[str, Any] = {"k": k}
            for sname, selector in (("fd", freq_topk), ("greedy", greedy_set_cover)):
                deltas, in_points = [], []
                for f in range(folds_n):
                    tr = [r for r in rows if folds[r["family"]] != f]
                    te = [r for r in rows if folds[r["family"]] == f]
                    sel = selector(tr, pool, k)
                    r_sel = rate(te, sel)
                    r_rand = exact_random_mean(te, pool, k)
                    deltas.append(100.0 * (r_sel - r_rand))
                    in_points.append({"fold": f, "selected": list(sel),
                                      "n_test": len(te),
                                      "r_sel_pct": round(100 * r_sel, 4),
                                      "r_rand_mean_pct": round(100 * r_rand, 4),
                                      "delta_pp": round(100.0 * (r_sel - r_rand), 4)})
                sel_all = selector(rows, pool, k)
                d_in = 100.0 * (rate(rows, sel_all) - exact_random_mean(rows, pool, k))
                rec[sname] = {
                    "selected_full": list(sel_all),
                    "rate_full_pct": round(100 * rate(rows, sel_all), 4),
                    "in_sample_delta_pp": round(d_in, 4),
                    "out_of_family_delta_pp_mean": round(sum(deltas) / len(deltas), 4),
                    "out_of_family_delta_pp_min": round(min(deltas), 4),
                    "out_of_family_delta_pp_max": round(max(deltas), 4),
                    "n_folds_positive": sum(1 for d in deltas if d > 0),
                    "per_fold": in_points,
                }
            per_k.append(rec)
        out["pools"][pname] = {
            "k_rows": per_k,
            "exact_random_mean_by_k": {
                k: round(100 * exact_random_mean(rows, pool, k), 4)
                for k in range(1, len(pool) + 1)},
        }
    return out


# ══════════════════════════════════════════════════════════════════════════
# 协议 B：外部资产池替换
# ══════════════════════════════════════════════════════════════════════════
def protocol_b(rows: list[dict[str, Any]], ext: dict[str, dict[str, str]],
               folds_n: int = 5) -> dict[str, Any]:
    erows: list[dict[str, Any]] = []
    n_unknown = 0
    for r in rows:
        pa = ext.get(r["uid"]) or {}
        per = {a: str(pa.get(a, "unknown")) for a in EXTERNAL_POOL}
        if any(v == "unknown" for v in per.values()):
            n_unknown += 1
        erows.append({"uid": r["uid"], "family": r["family"], "per_asset": per})
    folds = group_folds([r["family"] for r in erows], folds_n)

    marginal = {a: round(100 * rate(erows, (a,)), 4) for a in EXTERNAL_POOL}
    per_k = []
    for k in range(1, len(EXTERNAL_POOL) + 1):
        rec: dict[str, Any] = {"k": k}
        for sname, selector in (("fd", freq_topk), ("greedy", greedy_set_cover)):
            sel = selector(erows, EXTERNAL_POOL, k)
            d_in = 100.0 * (rate(erows, sel) - exact_random_mean(erows, EXTERNAL_POOL, k))
            deltas = []
            for f in range(folds_n):
                tr = [r for r in erows if folds[r["family"]] != f]
                te = [r for r in erows if folds[r["family"]] == f]
                sel_f = selector(tr, EXTERNAL_POOL, k)
                deltas.append(100.0 * (rate(te, sel_f)
                                       - exact_random_mean(te, EXTERNAL_POOL, k)))
            rec[sname] = {
                "selected_full": list(sel),
                "rate_full_pct": round(100 * rate(erows, sel), 4),
                "in_sample_delta_pp": round(d_in, 4),
                "out_of_family_delta_pp_mean": round(sum(deltas) / len(deltas), 4),
                "n_folds_positive": sum(1 for d in deltas if d > 0),
            }
        per_k.append(rec)
    spread = (max(marginal.values()) - min(marginal.values()))
    pool_or = {f"{a}+{b}": round(100 * rate(erows, (a, b)), 4)
               for a, b in combinations(EXTERNAL_POOL, 2)}
    return {
        "protocol": "外部资产池替换（692-B 四口径逐样本裁决，同一 566 帧）",
        "pool": list(EXTERNAL_POOL),
        "n_rows": len(erows), "n_rows_with_unknown": n_unknown,
        "marginal_catch_rate_pct": marginal,
        "marginal_spread_pp": round(spread, 4),
        "pair_or_rate_pct": pool_or,
        "per_k": per_k,
        "full_pool_or_pct": round(100 * rate(erows, EXTERNAL_POOL), 4),
        "note": "四口径 = 2 工具 × 2 口径（T2⊂T1、T3⊂T4 嵌套）⇒ 池内资产高度相关，"
                "这是与 Queyi 内部池（三 sanitizer 各自独立触发）**结构性不同**的点，必须随数字读。",
    }


# ══════════════════════════════════════════════════════════════════════════
# 协议 C：列置换零假设（等边际）
# ══════════════════════════════════════════════════════════════════════════
def _permuted_rows(rows: list[dict[str, Any]], rng: random.Random,
                   pool: tuple[str, ...]) -> list[dict[str, Any]]:
    idx = list(range(len(rows)))
    cols: dict[str, list[int]] = {}
    for a in pool:
        col = [1 if r["per_asset"].get(a) == "catch" else 0 for r in rows]
        rng.shuffle(col)
        cols[a] = col
    return [{"uid": f"perm{i}", "family": rows[i]["family"],
             "per_asset": {a: ("catch" if cols[a][i] else "miss") for a in pool}}
            for i in idx]


def protocol_c(rows: list[dict[str, Any]], draws: int, seed: int = 7101) -> dict[str, Any]:
    out: dict[str, Any] = {"protocol": "列置换零假设（保持每个资产的 catch 计数 = 边际不变，打乱样本对齐）",
                           "draws": draws, "pools": {}}
    for pname in ("full8", "PoolA(5)"):
        pool = POOL_DEFS[pname]
        obs = {}
        for k in (1, 4):
            if k > len(pool):
                continue
            sel = greedy_set_cover(rows, pool, k)
            obs[k] = round(100.0 * (rate(rows, sel) - exact_random_mean(rows, pool, k)), 4)
        rng = random.Random(seed)
        null: dict[int, list[float]] = {k: [] for k in obs}
        for _ in range(draws):
            pr = _permuted_rows(rows, rng, pool)
            for k in obs:
                sel = greedy_set_cover(pr, pool, k)
                null[k].append(100.0 * (rate(pr, sel) - exact_random_mean(pr, pool, k)))
        per = {}
        for k, vals in null.items():
            vals.sort()
            per[k] = {
                "observed_delta_pp": obs[k],
                "null_mean_pp": round(sum(vals) / len(vals), 4),
                "null_p05_pp": round(vals[int(0.05 * len(vals))], 4),
                "null_p95_pp": round(vals[int(0.95 * len(vals))], 4),
                "null_max_pp": round(vals[-1], 4),
                "observed_percentile_in_null": round(
                    100.0 * sum(1 for v in vals if v <= obs[k] + 1e-9) / len(vals), 4),
            }
        out["pools"][pname] = per
    return out


# ══════════════════════════════════════════════════════════════════════════
# 协议 D：缺陷类型边际重加权
# ══════════════════════════════════════════════════════════════════════════
def protocol_d(rows: list[dict[str, Any]]) -> dict[str, Any]:
    doc = load_json_cached(DATA / A5)
    corpus = Counter(str(s.get("defect_group") or "unknown") for s in doc.get("samples", []))
    obs = Counter(r["defect_group"] for r in rows)
    groups = sorted(set(corpus) | set(obs))

    def weights_for(target: dict[str, float]) -> list[float]:
        n = len(rows)
        return [target.get(r["defect_group"], 0.0) / max(1e-9, obs[r["defect_group"]] / n)
                for r in rows]

    uni = {g: 1.0 / len(groups) for g in groups}
    corpus_marg = {g: corpus[g] / sum(corpus.values()) for g in groups}
    eval_marg = {g: obs[g] / len(rows) for g in groups}

    out: dict[str, Any] = {
        "protocol": "缺陷类型（defect_group）边际重加权",
        "groups": groups,
        "eval_marginal": {g: round(eval_marg[g], 6) for g in groups},
        "corpus_marginal_1137": {g: round(corpus_marg[g], 6) for g in groups},
        "scenarios": {},
    }
    for name, target in (("eval_marginal(现状)", eval_marg),
                         ("corpus_marginal(1137)", corpus_marg),
                         ("uniform_over_groups", uni)):
        w = weights_for(target)
        per: dict[str, dict[str, dict[str, Any]]] = {}
        for pname in ("full8", "PoolA(5)"):
            pool = POOL_DEFS[pname]
            per[pname] = {}
            for k in (1, 4):
                if k > len(pool):
                    continue
                sel = greedy_set_cover(rows, pool, k, weights=w)
                d = 100.0 * (rate(rows, sel, w) - exact_random_mean(rows, pool, k, weights=w))
                per[pname][f"k={k}"] = {"selected": list(sel), "delta_pp": round(d, 4)}
        out["scenarios"][name] = per
    return out


# ══════════════════════════════════════════════════════════════════════════
# 主流程
# ══════════════════════════════════════════════════════════════════════════
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="710-C1 等边际替换只读近似")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    ap.add_argument("--perm", type=int, default=400, help="列置换零假设抽样次数")
    args = ap.parse_args(argv)

    rows = load_eval_rows()
    ext = load_external_verdicts()
    _log.info("eval 帧 = %d；外部口径记录 = %d", len(rows), len(ext))

    a = protocol_a(rows)
    b = protocol_b(rows, ext)
    c = protocol_c(rows, args.perm)
    d = protocol_d(rows)

    doc: dict[str, Any] = {
        "schema": "queyi-710/equal-marginal-readonly/v1",
        "generated_by": "tools/compute_710_equal_marginal.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "frame": {"source": A5, "split": "evaluation", "n": len(rows)},
        "protocol_A_out_of_family": a,
        "protocol_B_external_pool": b,
        "protocol_C_permutation_null": c,
        "protocol_D_margin_reweight": d,
        "honest_limits": [
            "四类近似都**不是**论文所指的等边际替换实验（那需要新 detect()）："
            "A/D 是**只读重排**（同裁决矩阵、换折法/权重），B 是**换池不换样本**的既有外部数据，"
            "C 是**零假设模拟**（不是真实资产池）。",
            "协议 B 的外部池只有 4 个资产（且两两嵌套）⇒ 与内部池（5/8 个）不可直接比大小，"
            "只可读**增益是否存在**，不可读倍数。",
            "所有检出率来自 566 帧 holdout evaluation split（92.9% 人工植入）⇒ 不代表真实缺陷分布。",
            "族外折法沿用 697 的 group_folds（seed=697）⇒ 换 seed 会有小幅抖动，本批未做 seed 敏感性。",
        ],
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")

    print("== 710-C1 · 等边际替换（只读近似）==")
    print("  [A] 族外选择增益（家族分折；训练折选、测试折评）")
    for pname, blk in a["pools"].items():
        means = blk["exact_random_mean_by_k"]
        print(f"      {pname}：精确随机均值 = " +
              "  ".join(f"k={k}:{v:.2f}%" for k, v in means.items()))
        for p in blk["k_rows"]:
            fd, gr = p["fd"], p["greedy"]
            print(f"        k={p['k']}: fd in={fd['in_sample_delta_pp']:+.2f} out={fd['out_of_family_delta_pp_mean']:+.2f}"
                  f"   greedy in={gr['in_sample_delta_pp']:+.2f} out={gr['out_of_family_delta_pp_mean']:+.2f}")
    print("  [B] 外部资产池（clang-tidy/cppcheck 四口径）")
    print(f"      边际：{b['marginal_catch_rate_pct']}  极差={b['marginal_spread_pp']}pp")
    for p in b["per_k"]:
        print(f"      k={p['k']}: fd in={p['fd']['in_sample_delta_pp']:+.2f} "
              f"out={p['fd']['out_of_family_delta_pp_mean']:+.2f} | "
              f"greedy in={p['greedy']['in_sample_delta_pp']:+.2f} "
              f"out={p['greedy']['out_of_family_delta_pp_mean']:+.2f}")
    print("  [C] 列置换零假设")
    for pname, per in c["pools"].items():
        for k, v in per.items():
            print(f"      {pname:<12} k={k}: obs={v['observed_delta_pp']:+.2f} "
                  f"null_mean={v['null_mean_pp']:+.2f} p95={v['null_p95_pp']:+.2f} "
                  f"pct={v['observed_percentile_in_null']}%")
    print("  [D] 缺陷边际重加权")
    for name, per in d["scenarios"].items():
        s = "  ".join(f"{pn} {kk}={vv['delta_pp']:+.2f}" for pn, pk in per.items()
                      for kk, vv in pk.items())
        print(f"      {name:<22} {s}")
    print(f"  → {args.out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
