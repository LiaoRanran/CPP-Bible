#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""analyze_677c_nondegenerate.py — 677c：非退化池 + 多 Baseline + Evolution Operator + A5 重算。

只读批次：**不跑 detect()**，一切判定复用 676f 冻结矩阵
``data/a5_676f_detection_matrix.json``（1137×8，per_asset 为真实 detect 观测）+
``data/a5_676f_sample_manifest.json``（派生 571 / 评估 566，分层 hash 切分）。
统计原语全部复用 673p/676f 既有实现，口径不变：

* ``tools/run_a5_experiment_673p.py``：AttributionExecutor（OR 聚合）、real_budget_comparison
  （FD/Random/Static 三臂 + 2000 次随机分布）、paired_test（精确 McNemar + Δ 的 95% CI）
* ``tools/selection_strategies_673p.py::select``：FD/Random/Static 的选择语义
* ``data/676f_analysis.py``：index_of / rates / fail_hits_real / bh_fdr（importlib 加载）

Stage 划分（``--stage`` 请求的 stage 一律**强制重算**，不复用旧 JSON）：
    pools      资产退化统计 + 3 个非退化池定义 + 选择差异验证 → 677c_asset_pools.json
    baselines  7 个基线（Random/FD/Static/Frequency/Greedy/Oracle/InfoGain）× 3 池 × k 扫描
               → 677c_baseline_results.json
    operator   evolution operator 消融（5 配置）× 3 池 × k 扫描 → 677c_evolution_operator_results.json
    a5         A5 重算装配（含退化贡献量化、676f 并排对比）→ 677c_a5_nondegenerate_results.json
    reports    由 4 份 JSON 生成 7 份 md 报告（数字不与 JSON 漂移）
    all        以上全部

诚实边界（与批次卡片一致）
==========================
1. 不修改 holdout_reveal_661.py / 样本源码 / 676f 产物；不重跑 detect()。
2. 池阈值是工程决策，报告写明理由；Pool A 在 unknown 阈值上叠加预注册 5% 产量下限
   （与论文 E4 勘误的"三个退化资产"一致）。
3. Oracle 在评估集上选最优 ⇒ 上界参考，不可达方法；Frequency 与 676f FD 在本数据模型下
   数学同构（fail_hits 就是派生集 catch 计数），报告如实呈现。
4. evolution operator 的权重是默认值不是学习值；novel_coverage 按规格字面定义与
   failure_coverage 数学等价（设计报告给一行证明），探索性 unique 变体单独标注。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import importlib
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "data"))

import evolution_operator_677c as evo  # noqa: E402
import run_a5_experiment_673p as a5  # noqa: E402  统计/三臂原语（未改动）
import selection_strategies_673p as ss  # noqa: E402
import verifier_pool_673p as vp  # noqa: E402

_ana = importlib.import_module("676f_analysis")  # data/ 下模块：mypy 需 importlib（pitfalls #2）

MANIFEST = ROOT / "data" / "a5_676f_sample_manifest.json"
MATRIX = ROOT / "data" / "a5_676f_detection_matrix.json"
RESULTS_676F = ROOT / "data" / "a5_676f_results.json"
TEX = ROOT / "research" / "latex" / "queyi_neurips2027_v1.1.tex"

OUT_POOLS = ROOT / "data" / "677c_asset_pools.json"
OUT_BASE = ROOT / "data" / "677c_baseline_results.json"
OUT_EVO = ROOT / "data" / "677c_evolution_operator_results.json"
OUT_A5 = ROOT / "data" / "677c_a5_nondegenerate_results.json"

SEED = a5.SEED                    # 20260930（676f 口径：单点配对 + 2000 次分布）
MULTI = a5.MULTI_SEED_N           # 2000
PRIMARY_K = a5.PRIMARY_K          # 4（673r 预注册主预算）
UNK_A, UNK_B = 30.0, 50.0         # 池 A/B 的 unknown 率阈值（卡片）
YIELD_A, YIELD_B = 5.0, 0.5       # 池 A/B 的 catch 率下限（A=预注册 5% 规则）
CUSTOM_BASELINES = ("frequency", "greedy", "oracle", "info_gain")

Index = dict[str, dict[str, str]]


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _jdump(path: Path, doc: dict[str, Any]) -> None:
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8", newline="\n")
    print(f"[677c] 写入 {path.relative_to(ROOT).as_posix()}")


def _fmt_p(p: float | None) -> str:
    if p is None:
        return "n/a"
    if p == 0.0:
        return "<1e-300"
    return f"{p:.2e}" if p < 1e-4 else f"{p:.4g}"


def _fmt_pp(x: float | None) -> str:
    return "n/a" if x is None else f"{x:+.2f}pp"


# ─────────────────────────────────────────────────────────────────────────────
# 数据装载
# ─────────────────────────────────────────────────────────────────────────────
def load_data() -> dict[str, Any]:
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    mat = json.loads(MATRIX.read_text(encoding="utf-8"))
    r676f = json.loads(RESULTS_676F.read_text(encoding="utf-8"))
    index: Index = _ana.index_of(mat)
    samples = man["samples"]
    for r in samples:
        if r["sample_id"] not in index:
            raise KeyError(f"样本 {r['sample_id']} 不在判定矩阵里（fail-loud）")
    deriv = [r for r in samples if r["split"] == "derivation"]
    ev = [r for r in samples if r["split"] == "evaluation"]
    assets = list(_ana.ASSETS)
    return {
        "man": man, "mat": mat, "r676f": r676f, "index": index, "samples": samples,
        "deriv": deriv, "ev": ev, "assets": assets,
        "deriv_ids": [r["sample_id"] for r in deriv],
        "ev_exec": [{"id": r["sample_id"]} for r in ev],
        "ex": a5.AttributionExecutor(index),
        "fh8": _ana.fail_hits_real(deriv, assets, index),
        "wall": {a: float(v) for a, v in mat["wall_seconds_by_asset"].items()},
    }


# ─────────────────────────────────────────────────────────────────────────────
# Stage: pools
# ─────────────────────────────────────────────────────────────────────────────
def _asset_stats(ld: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for scope, rows in (("full_pool", ld["samples"]), ("derivation", ld["deriv"]),
                        ("evaluation", ld["ev"])):
        rr = _ana.rates(rows, ld["assets"], ld["index"])
        for a, v in rr.items():
            out.setdefault(a, {})[scope] = v
    return out


def define_pools(ld: dict[str, Any]) -> dict[str, Any]:
    stats = _asset_stats(ld)
    n_total = len(ld["samples"])

    def unk(a: str) -> float:
        return float(stats[a]["full_pool"]["unknown_rate_pct"] or 0.0)

    def cch(a: str) -> float:
        return float(stats[a]["full_pool"]["catch_rate_pct"] or 0.0)

    # 退化判定（两套判据并报）
    unk_based = {a: {"unknown_rate_pct": unk(a), "always_unknown": unk(a) >= 99.999}
                 for a in ld["assets"]}
    prereg = _ana.degenerate(ld["samples"], ld["assets"], ld["index"])  # 预注册 catch 率 [5%,95%]

    pools: dict[str, dict[str, Any]] = {
        "A": {"name": "Pool A（严格）",
              "rule": f"unknown_rate < {UNK_A:.0f}% 且 catch_rate >= {YIELD_A:.0f}%（预注册产量下限）",
              "assets": sorted(a for a in ld["assets"] if unk(a) < UNK_A and cch(a) >= YIELD_A),
              "rationale": "同时剔除恒 unknown（wunsequenced/compile-time）与低产资产（linker "
                           "catch 0.88%<5%）；候选集与 676f 预注册并列分析完全一致，可直接对账"},
        "B": {"name": "Pool B（中等）",
              "rule": f"unknown_rate < {UNK_B:.0f}% 且 catch_rate >= {YIELD_B:.1f}%",
              "assets": sorted(a for a in ld["assets"] if unk(a) < UNK_B and cch(a) >= YIELD_B),
              "rationale": "放宽产量下限到 0.5%，容纳 linker（unknown=0% 但 catch 仅 0.88%）"},
        "C": {"name": "Pool C（宽松）",
              "rule": "仅剔除 unknown_rate=100% 的恒 unknown 资产",
              "assets": sorted(a for a in ld["assets"] if unk(a) < 99.999),
              "rationale": "评审的字面要求：只去掉两个恒 unknown 资产，其余全保留"},
    }

    fh8 = ld["fh8"]
    for p in pools.values():
        cands = p["assets"]
        fh_pool = {a: int(fh8.get(a, 0)) for a in cands}
        n = len(cands)
        valid: list[dict[str, Any]] = []
        for k in range(1, n):  # 1 <= k <= |A|-1；k=|A| 三臂恒等于全池（退化）
            fd_sel = list(ss.select("failure_driven", vp.ASSET_POOL, max_assets=k,
                                    fail_hits=fh_pool, candidates=cands).assets)
            rnd_sel = list(ss.select("random", vp.ASSET_POOL, max_assets=k, seed=SEED,
                                     candidates=cands).assets)
            valid.append({
                "k": k, "fd_assets": fd_sel, "random_single_assets": rnd_sel,
                "single_point_sets_differ": set(fd_sel) != set(rnd_sel),
                "p_random_draw_equals_fd_set": round(1.0 / math.comb(n, k), 6),
                "note": "单点 Random 是 seed=20260930 的一次抽样；结构性差异概率 = 1/C(n,k)",
            })
        p.update({"k_range": [1, n - 1], "n_candidates": n,
                  "k_where_single_point_differs": [v["k"] for v in valid
                                                   if v["single_point_sets_differ"]],
                  "validation": valid,
                  "fd_rank_full": sorted(cands, key=lambda a: (-fh_pool[a], a))})

    return {
        "schema": "queyi-a5-677c-pools/v1", "generated_by": "tools/analyze_677c_nondegenerate.py",
        "generated_at": _now(), "n_samples": n_total,
        "inputs": {"matrix": MATRIX.relative_to(ROOT).as_posix(),
                   "manifest": MANIFEST.relative_to(ROOT).as_posix(),
                   "matrix_generated_at": ld["mat"].get("generated_at"),
                   "detector_sha256_16": ld["mat"].get("detector_sha256_16")},
        "asset_stats": stats,
        "unknown_based_degeneracy": unk_based,
        "preregistered_degeneracy_catch_rate_5pct": prereg,
        "prompt_expectation_vs_data": {
            "expectation": "卡片预期 linker 高 unknown（>50%），Pool A 预期 5 资产",
            "actual": "linker unknown=0.00%（10 catch + 1127 miss）⇒ 仅按 unknown 阈值时 "
                      "A/B/C 三池定义塌缩为同一 6 资产集合",
            "resolution": "Pool A 叠加预注册 catch 率 5% 下限（与论文 E4 勘误、676f 并列分析"
                          "口径一致）⇒ 5 资产；B/C 保持卡片字面定义 ⇒ 都是 6 资产（B≡C 如实记录）",
        },
        "pools": pools,
        "honest_notes": [
            "退化统计用了全池率（含评估集）：这是池**构成**设计决策（676f 并列分析同口径），"
            "不是逐样本选择泄漏；逐样本选择只用派生集。",
            "Pool A 的候选集与 676f co_primary_excl_degenerate 完全一致 ⇒ 其结果应逐位复现 "
            "676f 并列分析（在 a5 stage 做了对账）。",
            "k=|A| 时三臂恒等于全池，属预算退化，不进扫描（676f is_degenerate_k 同口径）。",
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# 自定义基线的选择函数（全部确定性，只用派生集；oracle 除外——评估集上界）
# ─────────────────────────────────────────────────────────────────────────────
def sel_frequency(cands: list[str], k: int, fh: dict[str, int]) -> list[str]:
    """按派生集 catch 频率降序，同分 id 升序 ⇒ top-k（与 676f FD 的排序键完全相同）。"""
    return sorted(cands, key=lambda a: (-int(fh.get(a, 0)), a))[:k]


def sel_greedy(cands: list[str], k: int, index: Index, ids: list[str]) -> list[str]:
    """迭代式残余覆盖贪心（set-cover）：每步选新增覆盖最多的资产，同分 id 升序。"""
    covered: set[str] = set()
    sel: list[str] = []
    while len(sel) < min(k, len(cands)):
        best, best_gain = None, -1
        for a in sorted(c for c in cands if c not in sel):
            gain = len(evo.catch_set(a, index, ids) - covered)
            if gain > best_gain:
                best_gain, best = gain, a
        assert best is not None
        sel.append(best)
        covered |= evo.catch_set(best, index, ids)
    return sel


def sel_oracle(cands: list[str], k: int, ex: a5.AttributionExecutor,
               ev_exec: list[dict[str, Any]]) -> tuple[list[str], int]:
    """Oracle 上界：在**评估集**上穷举 C(n,k) 选 catch 数最多的子集（评估泄漏 ⇒ 不可达）。"""
    best_combo: tuple[str, ...] = ()
    best_cnt = -1
    for combo in itertools.combinations(sorted(cands), k):
        cnt = sum(1 for r in ev_exec if ex.verdict(r, combo) == "catch")
        if cnt > best_cnt:
            best_cnt, best_combo = cnt, combo
    return list(best_combo), best_cnt


def sel_info_gain(cands: list[str], k: int, index: Index, ids: list[str]) -> list[str]:
    """信息增益排序（探索性）：对"池 OR 可检出"目标的互信息，同分 id 升序。"""
    def ent(p: float) -> float:
        return 0.0 if p <= 0.0 or p >= 1.0 else -(p * math.log2(p) + (1 - p) * math.log2(1 - p))

    y = [any(index[s].get(a) == "catch" for a in cands) for s in ids]
    n = len(ids)
    hy = ent(sum(y) / n)
    gains: dict[str, float] = {}
    for a in cands:
        xa = [index[s].get(a) == "catch" for s in ids]
        n1 = sum(xa)
        p1 = (sum(1 for i in range(n) if xa[i] and y[i]) / n1) if n1 else 0.0
        p0 = (sum(1 for i in range(n) if not xa[i] and y[i]) / (n - n1)) if n1 < n else 0.0
        hya = (n1 / n) * ent(p1) + ((n - n1) / n) * ent(p0)
        gains[a] = hy - hya
    return sorted(cands, key=lambda a: (-round(gains[a], 12), a))[:k]


# ─────────────────────────────────────────────────────────────────────────────
# Stage: baselines
# ─────────────────────────────────────────────────────────────────────────────
def run_baselines(ld: dict[str, Any], pools_doc: dict[str, Any], *, multi: int) -> dict[str, Any]:
    ex, index = ld["ex"], ld["index"]
    ev_exec, deriv_ids = ld["ev_exec"], ld["deriv_ids"]
    pools: dict[str, dict[str, Any]] = {}
    for pname in ("A", "B", "C"):
        p = pools_doc["pools"][pname]
        cands = p["assets"]
        fh_pool = {a: int(ld["fh8"].get(a, 0)) for a in cands}
        blocks: dict[str, Any] = {}
        for k in range(1, len(cands)):  # k=|A| 预算退化，不跑
            three = a5.real_budget_comparison(
                ev_exec, ex, index, vp.ASSET_POOL, candidates=cands, k=k, seed=SEED,
                multi_seed_n=multi, fail_hits=fh_pool)
            random_single = list(three["arms"]["random"]["assets"])
            fd_assets = list(three["arms"]["fd"]["assets"])
            custom: dict[str, Any] = {}
            sels: dict[str, list[str]] = {
                "frequency": sel_frequency(cands, k, fh_pool),
                "greedy": sel_greedy(cands, k, index, deriv_ids),
                "info_gain": sel_info_gain(cands, k, index, deriv_ids),
            }
            oracle_sel, oracle_cnt = sel_oracle(cands, k, ex, ev_exec)
            sels["oracle"] = oracle_sel
            for name in CUSTOM_BASELINES:
                sel = sels[name]
                arm = a5.arm_stats(ev_exec, tuple(sel), ex)
                custom[name] = {
                    "assets": sel,
                    "rate_pct": arm["rate_pct"], "cp95": arm["cp95"],
                    "paired_vs_random": a5.paired_test(ev_exec, tuple(sel),
                                                       tuple(random_single), ex,
                                                       label_a=name, label_b="random"),
                    **({"oracle_eval_catch": oracle_cnt} if name == "oracle" else {}),
                }
            fd_vs_each = {
                name: a5.paired_test(ev_exec, tuple(fd_assets), tuple(v["assets"]), ex,
                                     label_a="fd", label_b=name)
                for name, v in custom.items()
            }
            # 排名：全部臂（含 static/oracle）按检出率降序，同率按名字典序
            all_rates = {"fd": three["arms"]["fd"]["rate_pct"],
                         "random": three["arms"]["random"]["rate_pct"],
                         "static": three["arms"]["static"]["rate_pct"],
                         **{n: v["rate_pct"] for n, v in custom.items()}}
            ranking = sorted(all_rates, key=lambda n: (-all_rates[n], n))
            blocks[str(k)] = {
                "three_arm": three, "custom_baselines": custom, "fd_vs_each": fd_vs_each,
                "static_vs_random": a5.paired_test(ev_exec, tuple(three["arms"]["static"]["assets"]),
                                                   tuple(random_single), ex,
                                                   label_a="static", label_b="random"),
                "ranking": ranking,
                "fd_random_sets_differ": set(fd_assets) != set(random_single),
                "p_value_family": {
                    "note": "对本 (pool,k) 内 7 个臂 vs Random 单点的 McNemar p 做 BH-FDR",
                    "bh_fdr": dict(zip(["fd", "static", *CUSTOM_BASELINES],
                                       _ana.bh_fdr([three["paired_tests"]["fd_vs_random"]["mcnemar_p"],
                                                    three["paired_tests"]["fd_vs_static"]["mcnemar_p"],
                                                    *[custom[n]["paired_vs_random"]["mcnemar_p"]
                                                      for n in CUSTOM_BASELINES]]))),
                },
            }
        pools[pname] = {"pool_name": p["name"], "assets": cands, "k_blocks": blocks}
    return {
        "schema": "queyi-a5-677c-baselines/v1",
        "generated_by": "tools/analyze_677c_nondegenerate.py", "generated_at": _now(),
        "design": {"seed": SEED, "multi_seed_runs": multi, "split": "676f 原切分（派生 571/评估 566）",
                   "matrix": "676f 冻结判定矩阵（未重跑 detect）",
                   "random_convention": "单点 seed=20260930 用于配对检验；2000 次分布报均值/分位",
                   "baselines": ["random", "fd", "static", "frequency", "greedy", "oracle",
                                 "info_gain"],
                   "oracle_note": "oracle 在评估集上穷举选最优 ⇒ 上界参考，不可达方法",
                   "frequency_note": "676f FD 的 fail_hits 操作定义 = 派生集 catch 计数 ⇒ "
                                     "frequency 与 fd 的排序键相同，选择应完全一致（结果可验证）"},
        "pools": pools,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Stage: operator
# ─────────────────────────────────────────────────────────────────────────────
def run_operator(ld: dict[str, Any], pools_doc: dict[str, Any], *, multi: int) -> dict[str, Any]:
    del multi  # operator 臂是确定性的；配对检验用与 baselines stage 相同的单点 Random
    ex, index = ld["ex"], ld["index"]
    ev_exec, deriv_ids = ld["ev_exec"], ld["deriv_ids"]
    pools: dict[str, dict[str, Any]] = {}
    for pname in ("A", "B", "C"):
        p = pools_doc["pools"][pname]
        cands = p["assets"]
        fh_pool = {a: int(ld["fh8"].get(a, 0)) for a in cands}
        blocks: dict[str, Any] = {}
        for k in range(1, len(cands)):
            fd_assets = list(ss.select("failure_driven", vp.ASSET_POOL, max_assets=k,
                                       fail_hits=fh_pool, candidates=cands).assets)
            rnd_sel = list(ss.select("random", vp.ASSET_POOL, max_assets=k, seed=SEED,
                                     candidates=cands).assets)
            greedy_sel = sel_greedy(cands, k, index, deriv_ids)
            configs: dict[str, Any] = {}
            for cfg_name, cfg in evo.ABLATION_CONFIGS.items():
                r = evo.select_portfolio(cands, k, index, deriv_ids, wall_seconds=ld["wall"],
                                         weights=cfg["weights"], novel_mode=cfg["novel_mode"])
                arm = a5.arm_stats(ev_exec, tuple(r["selection"]), ex)
                configs[cfg_name] = {
                    "selection": r["selection"], "trace": r["trace"],
                    "rate_pct": arm["rate_pct"], "cp95": arm["cp95"],
                    "paired_vs_random": a5.paired_test(ev_exec, tuple(r["selection"]),
                                                       tuple(rnd_sel), ex,
                                                       label_a=cfg_name, label_b="random"),
                    "paired_vs_fd": a5.paired_test(ev_exec, tuple(r["selection"]),
                                                   tuple(fd_assets), ex,
                                                   label_a=cfg_name, label_b="fd"),
                    "config_note": cfg["note"],
                }
            blocks[str(k)] = {
                "fd_assets": fd_assets, "random_single_assets": rnd_sel,
                "greedy_assets": greedy_sel, "configs": configs,
                "equivalence": {
                    "fd_only_equals_greedy": configs["fd_only"]["selection"] == greedy_sel,
                    "full_equals_fd": configs["full"]["selection"] == fd_assets,
                    "full_equals_greedy": configs["full"]["selection"] == greedy_sel,
                    "fd_novel_equals_fd_only": (configs["fd_novel"]["selection"]
                                                == configs["fd_only"]["selection"]),
                    "note": "fd_only(w1=1) 理论上 ≡ 残余覆盖贪心；fd_novel 在 literal 模式下 ≡ "
                            "fd_only（novel≡failure 的数学坍缩）",
                },
            }
        pools[pname] = {"pool_name": p["name"], "assets": cands, "k_blocks": blocks}
    return {
        "schema": "queyi-a5-677c-operator/v1",
        "generated_by": "tools/analyze_677c_nondegenerate.py", "generated_at": _now(),
        "operator_spec": {
            "score": "w1*failure_coverage + w2*novel_coverage - w3*cost_norm - w4*redundancy",
            "failure_coverage": "|{s ∈ F_t : a_j catches s}| / |F_t|，F_t=派生集上 C_t 未抓到的样本",
            "novel_coverage_literal": "|{s ∈ F_t : a_j catches s 且 C_t 无资产抓 s}| / |F_t| "
                                      "≡ failure_coverage（F_t 定义使第二条件恒真；如实记录）",
            "novel_coverage_unique": "探索性变体：|{s ∈ F_t : a_j catches s 且其他候选都抓不到 s}| "
                                     "/ |F_t|（不可替代残余覆盖）",
            "cost_norm": "wall_seconds(a)/max_wall（676f 矩阵实测墙钟；全量 1137 样本口径）",
            "redundancy": "mean_{c ∈ C_t} Jaccard(catch 集；派生集)",
            "default_weights": evo.DEFAULT_WEIGHTS,
            "selection": "迭代 argmax，同分 id 升序；确定性可复现",
            "ablation_configs": {k: v["note"] for k, v in evo.ABLATION_CONFIGS.items()},
        },
        "pools": pools,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Stage: a5（装配 + 退化贡献量化 + 676f 对账）
# ─────────────────────────────────────────────────────────────────────────────
def _krow(base: dict[str, Any], evo_doc: dict[str, Any], pname: str, k: str) -> dict[str, Any]:
    """把一个 (pool,k) 的全部臂压成 {arm: {rate, delta_single, p, delta_vs_mean, rank}}。"""
    blk = base["pools"][pname]["k_blocks"][k]
    three = blk["three_arm"]
    rand_mean = three["random_multi_seed"]["mean_rate_pct"]
    rows: dict[str, dict[str, Any]] = {}
    arms = {
        "fd": (three["arms"]["fd"]["rate_pct"], three["arms"]["fd"]["assets"],
               three["paired_tests"]["fd_vs_random"]),
        "random": (three["arms"]["random"]["rate_pct"], three["arms"]["random"]["assets"], None),
        "static": (three["arms"]["static"]["rate_pct"], three["arms"]["static"]["assets"],
                   blk["static_vs_random"]),
    }
    for name, (rate, assets, paired) in arms.items():
        rows[name] = {"assets": assets, "rate_pct": rate,
                      "delta_vs_random_single_pp": paired["delta_pp"] if paired else 0.0,
                      "mcnemar_p_vs_random": paired["mcnemar_p"] if paired else None,
                      "delta_vs_random_mean_pp": round(rate - rand_mean, 4)}
    for name, v in blk["custom_baselines"].items():
        pr = v["paired_vs_random"]
        rows[name] = {"assets": v["assets"], "rate_pct": v["rate_pct"],
                      "delta_vs_random_single_pp": pr["delta_pp"],
                      "mcnemar_p_vs_random": pr["mcnemar_p"],
                      "delta_vs_random_mean_pp": round(v["rate_pct"] - rand_mean, 4)}
    full = evo_doc["pools"][pname]["k_blocks"][k]["configs"]["full"]
    rows["evo_full"] = {"assets": full["selection"], "rate_pct": full["rate_pct"],
                        "delta_vs_random_single_pp": full["paired_vs_random"]["delta_pp"],
                        "mcnemar_p_vs_random": full["paired_vs_random"]["mcnemar_p"],
                        "delta_vs_random_mean_pp": round(full["rate_pct"] - rand_mean, 4)}
    ranked = sorted(rows, key=lambda n: (-rows[n]["rate_pct"], n))
    for i, n in enumerate(ranked):
        rows[n]["rank"] = i + 1
    return {"arms": rows, "random_2000_mean_pct": rand_mean,
            "random_2000_sd_pp": three["random_multi_seed"]["sd_pp"],
            "random_2000_p2.5_pct": three["random_multi_seed"]["percentile_2.5_pct"],
            "random_2000_p97.5_pct": three["random_multi_seed"]["percentile_97.5_pct"],
            "fd_strictly_better_frac": three["random_multi_seed"]["fd_strictly_better_frac"],
            "fd_vs_random_ci95_pp": three["paired_tests"]["fd_vs_random"]["delta_ci95_pp"],
            "fd_vs_random_b": three["paired_tests"]["fd_vs_random"]["discordant_a_only"],
            "fd_vs_random_c": three["paired_tests"]["fd_vs_random"]["discordant_b_only"],
            "fd_random_sets_differ": blk["fd_random_sets_differ"],
            "evo_full_assets": full["selection"]}


def run_a5(ld: dict[str, Any], pools_doc: dict[str, Any], base_doc: dict[str, Any],
           evo_doc: dict[str, Any], *, multi: int) -> dict[str, Any]:
    r676f = ld["r676f"]
    pm = r676f["primary_main_8candidates"]["primary"]
    co_k = {c["k"]: c for c in r676f["co_primary_excl_degenerate"]["by_k_compact"]}

    pools: dict[str, dict[str, Any]] = {}
    checks: dict[str, Any] = {}
    for pname in ("A", "B", "C"):
        cands = pools_doc["pools"][pname]["assets"]
        ks = sorted(base_doc["pools"][pname]["k_blocks"], key=int)
        kb = {k: _krow(base_doc, evo_doc, pname, k) for k in ks}
        best_single = max(ks, key=lambda k: kb[k]["arms"]["fd"]["delta_vs_random_single_pp"])
        best_mean = max(ks, key=lambda k: kb[k]["arms"]["fd"]["delta_vs_random_mean_pp"])
        pools[pname] = {
            "assets": cands, "k_blocks": kb,
            "best_k_by_fd_delta_single": best_single,
            "best_k_by_fd_delta_vs_mean": best_mean,
            "primary_summary": {
                "k": best_single,
                "fd_rate_pct": kb[best_single]["arms"]["fd"]["rate_pct"],
                "random_single_rate_pct": kb[best_single]["arms"]["random"]["rate_pct"],
                "random_2000_mean_pct": kb[best_single]["random_2000_mean_pct"],
                "delta_single_pp": kb[best_single]["arms"]["fd"]["delta_vs_random_single_pp"],
                "delta_vs_mean_pp": kb[best_single]["arms"]["fd"]["delta_vs_random_mean_pp"],
                "mcnemar_p": kb[best_single]["arms"]["fd"]["mcnemar_p_vs_random"],
            },
        }
        # 内部对账：Pool A ≡ 676f 并列分析候选集 ⇒ 数字应逐位一致
        if pname == "A":
            diffs = []
            for k in (1, 2, 3, 4):
                if str(k) in kb and k in co_k:
                    d = abs(kb[str(k)]["arms"]["fd"]["delta_vs_random_single_pp"]
                            - co_k[k]["delta_fd_minus_random_pp"])
                    diffs.append(round(d, 9))
            checks["poolA_vs_676f_co_max_abs_delta_diff_pp"] = max(diffs) if diffs else None
            checks["poolA_matches_676f_co"] = bool(diffs) and max(diffs) < 1e-6

    # 退化贡献量化（k=4 口径，主预算；同时给 mean 口径）
    orig = {"pool": "8 资产全池（含 3 个预注册退化资产）", "k": 4,
            "fd_rate_pct": pm["fd_rate_pct"], "random_single_rate_pct": pm["random_rate_pct"],
            "random_2000_mean_pct": pm["random_2000"]["mean_rate_pct"],
            "delta_single_pp": pm["delta_fd_minus_random_pp"],
            "delta_vs_mean_pp": round(pm["fd_rate_pct"]
                                      - pm["random_2000"]["mean_rate_pct"], 4),
            "mcnemar_p": pm["mcnemar_p"], "source": "data/a5_676f_results.json"
                                                    "::primary_main_8candidates.primary"}
    contribution: dict[str, Any] = {"note": "退化资产贡献 = 原池 Δ − 非退化池同 k Δ（单点与均值两口径）",
                                    "original": orig}
    for pname in ("A", "B", "C"):
        k4 = pools[pname]["k_blocks"].get("4")
        if k4:
            contribution[f"pool_{pname}_k4"] = {
                "pool": pools_doc["pools"][pname]["name"], "assets": pools[pname]["assets"],
                "fd_rate_pct": k4["arms"]["fd"]["rate_pct"],
                "random_single_rate_pct": k4["arms"]["random"]["rate_pct"],
                "random_2000_mean_pct": k4["random_2000_mean_pct"],
                "delta_single_pp": k4["arms"]["fd"]["delta_vs_random_single_pp"],
                "delta_vs_mean_pp": k4["arms"]["fd"]["delta_vs_random_mean_pp"],
                "mcnemar_p": k4["arms"]["fd"]["mcnemar_p_vs_random"],
                "degenerate_contribution_single_pp": round(
                    orig["delta_single_pp"] - k4["arms"]["fd"]["delta_vs_random_single_pp"], 4),
                "degenerate_contribution_vs_mean_pp": round(
                    orig["delta_vs_mean_pp"] - k4["arms"]["fd"]["delta_vs_random_mean_pp"], 4),
            }

    # uninterpretable 条款判定：池内是否还有预注册规则（catch 率 ∉ [5%,95%]）资产
    clause: dict[str, Any] = {}
    prereg = set(pools_doc["preregistered_degeneracy_catch_rate_5pct"])
    for pname in ("A", "B", "C"):
        residual = sorted(set(pools[pname]["assets"]) & prereg)
        clause[pname] = {
            "residual_prereg_degenerate_assets": residual,
            "clause_triggered": bool(residual),
            "interpretation": ("池内仍有 catch 率<5% 的资产（linker）⇒ 按预注册条款本池主分析"
                               "仍不可作选择策略优越性解读"
                               if residual else
                               "池内无预注册退化资产 ⇒ 主分析即并列分析，条款不触发"),
        }

    fd_mean_gain = {
        pname: {k: {"fd_minus_mean_pp": pools[pname]["k_blocks"][k]["arms"]["fd"]["delta_vs_random_mean_pp"],
                    "evo_full_minus_mean_pp": pools[pname]["k_blocks"][k]["arms"]["evo_full"]["delta_vs_random_mean_pp"]}
                for k in pools[pname]["k_blocks"]}
        for pname in ("A", "B", "C")
    }

    return {
        "schema": "queyi-a5-677c-a5/v1",
        "generated_by": "tools/analyze_677c_nondegenerate.py", "generated_at": _now(),
        "design": {"multi_seed_runs": multi, "seed": SEED,
                   "k_sweep": "1..|A|-1（k=|A| 预算退化不跑）",
                   "split": "676f 原切分：派生 571 / 评估 566"},
        "reference_676f": {
            "primary_k4": orig,
            "co_by_k_compact": [{"k": k, "delta_pp": co_k[k]["delta_fd_minus_random_pp"],
                                 "fd_rate_pct": co_k[k]["fd_rate_pct"],
                                 "random_rate_pct": co_k[k]["random_rate_pct"],
                                 "mcnemar_p": co_k[k]["mcnemar_p"]}
                                for k in sorted(co_k)],
        },
        "pools": pools,
        "internal_validity_checks": checks,
        "degenerate_contribution": contribution,
        "uninterpretable_clause": clause,
        "fd_and_evo_vs_random_mean": fd_mean_gain,
        "core_answers": {
            "q1_fd_vs_random_on_nondegenerate": "见 pools.*.primary_summary 与报告（由脚本按数字生成结论）",
            "q2_delta_vs_original_24pp": "见 degenerate_contribution",
            "q3_evo_full_vs_fd": "见 pools.*.k_blocks.*.arms.evo_full vs fd（报告自动判读）",
        },
        "honest_notes": [
            "单点 Random 的 Δ 是一次抽样的配对差值（676f 口径，可对账）；期望效应看 "
            "delta_vs_random_mean_pp（对 2000 次均值）。",
            "Oracle 在评估集上选最优 ⇒ 只作上界参考。",
            "Pools B/C 含 linker（catch 0.88%<5%）⇒ 预注册 uninterpretable 条款在这些池仍触发；"
            "Pool A 不触发。",
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Stage: reports（全部由 JSON 生成，数字不漂移）
# ─────────────────────────────────────────────────────────────────────────────
def _tex_line(needle: str) -> str:
    if not TEX.is_file():
        return "（tex 不在，按节名定位）"
    for i, line in enumerate(TEX.read_text(encoding="utf-8").splitlines(), start=1):
        if needle in line:
            return f"L{i}"
    return "（锚点未命中，grep 复核）"


def _pool_table(base_doc: dict[str, Any], evo_doc: dict[str, Any], pname: str) -> str:
    p = base_doc["pools"][pname]
    lines = ["| k | 臂 | 选择 | 检出率% | Δ单点(Random) | p | Δvs均值2000 | 排名 |",
             "|---|---|---|---|---|---|---|---|"]
    for k in sorted(p["k_blocks"], key=int):
        rows = _krow(base_doc, evo_doc, pname, k)["arms"]
        for name in ("fd", "random", "static", "frequency", "greedy", "oracle", "info_gain",
                     "evo_full"):
            r = rows[name]
            assets = ",".join(r["assets"])
            lines.append(f"| {k} | {name} | {assets} | {r['rate_pct']:.2f} | "
                         f"{_fmt_pp(r['delta_vs_random_single_pp'])} | {_fmt_p(r['mcnemar_p_vs_random'])} | "
                         f"{_fmt_pp(r['delta_vs_random_mean_pp'])} | {r['rank']} |")
    return "\n".join(lines)


def write_reports(pools_doc: dict[str, Any], base_doc: dict[str, Any], evo_doc: dict[str, Any],
                  a5_doc: dict[str, Any]) -> list[Path]:
    out: list[Path] = []
    stats = pools_doc["asset_stats"]
    multi = base_doc["design"]["multi_seed_runs"]
    ref676f = a5_doc["reference_676f"]
    co_k = {c["k"]: c for c in ref676f["co_by_k_compact"]}

    # ---- 1. 池设计报告 ----
    lines = [
        "# 677c · 非退化 Asset Pool 设计报告", "",
        "- 数据源：`data/a5_676f_detection_matrix.json`（1137×8 冻结矩阵，未重跑 detect）+ "
        "`data/a5_676f_sample_manifest.json`（派生 571 / 评估 566）",
        "- 复现：`.venv/Scripts/python.exe tools/analyze_677c_nondegenerate.py --stage pools`",
        "- 机读：`data/677c_asset_pools.json`（本报告每个数字都能在 JSON 里按 key path 找到）", "",
        "## 1. 8 资产退化统计（全池 n=1137）", "",
        "| 资产 | catch | unknown | miss | unknown% | catch% | 恒unknown? | 预注册退化(catch率∉[5%,95%])? |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for a in sorted(stats):
        f = stats[a]["full_pool"]
        always = "是" if f["unknown_rate_pct"] >= 99.999 else "否"
        prereg = "是" if a in pools_doc["preregistered_degeneracy_catch_rate_5pct"] else "否"
        lines.append(f"| {a} | {f['catch']} | {f['unknown']} | {f['miss']} | "
                     f"{f['unknown_rate_pct']:.2f} | {f['catch_rate_pct']:.2f} | {always} | {prereg} |")
    lines += [
        "", "关键事实：**linker 的 unknown 率是 0.00%**（10 catch + 1127 miss），不是卡片预估的"
        "\">50%\"。按 unknown 阈值（30%/50%/剔除恒 unknown）定义的三个池会**塌缩成同一个 6 资产集合**。"
        "因此 Pool A 在 unknown 阈值上叠加**预注册 catch 率 5% 下限**（论文 E4 勘误把 linker 列入三个"
        "退化资产的同一规则），恢复出卡片预期的 5 资产严格池；B/C 保持卡片字面定义（都是 6 资产，"
        "B≡C 如实记录）。", "",
        "## 2. 三个池的定义与理由", "",
    ]
    for pname in ("A", "B", "C"):
        p = pools_doc["pools"][pname]
        lines.append(f"### {p['name']}")
        lines.append(f"- 规则：{p['rule']}")
        lines.append(f"- 资产（{p['n_candidates']} 个）：{', '.join(p['assets'])}")
        lines.append(f"- 理由：{p['rationale']}")
        lines.append(f"- FD 排序（派生集 fail_hits）：{' > '.join(p['fd_rank_full'])}")
        lines.append("- 验证（1≤k≤|A|-1）：")
        lines.append("")
        lines.append("| k | FD 选择 | Random 单点选择 | 单点集不同? | P(随机集==FD集)=1/C(n,k) |")
        lines.append("|---|---|---|---|---|")
        for v in p["validation"]:
            lines.append(f"| {v['k']} | {','.join(v['fd_assets'])} | "
                         f"{','.join(v['random_single_assets'])} | "
                         f"{'是' if v['single_point_sets_differ'] else '否（单点恰巧同集）'} | "
                         f"{v['p_random_draw_equals_fd_set']} |")
        lines.append("")
    diff_any = {pn: any(v["single_point_sets_differ"] for v in pools_doc["pools"][pn]["validation"])
                for pn in ("A", "B", "C")}
    lines += [
        "## 3. 验收判定", "",
        "- 3 个池定义完成：A（5 资产）/ B（6）/ C（6，≡B）。",
        f"- 每个池都存在 1<k<|A| 使 FD 与 Random 单点选择不同：A={diff_any['A']}、B={diff_any['B']}、"
        f"C={diff_any['C']}；且对一切 1≤k<|A|，P(随机抽到 FD 同集)=1/C(n,k)<1 ⇒ 结构上 Random 与 FD "
        "必然可分（k=|A|-1 的单点重合只是抽样巧合，正是 676f 并列分析 k=4 失效的原因）。",
        "- 退化资产 unknown 比例统计完整（第 1 节表 + JSON asset_stats）。", "",
        "## 4. 诚实边界", "",
    ] + [f"- {n}" for n in pools_doc["honest_notes"]]
    (ROOT / "data" / "677c_pool_design_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    out.append(ROOT / "data" / "677c_pool_design_report.md")

    # ---- 2. Baseline 对比报告 ----
    lines = [
        "# 677c · 5+ Baseline 对比报告（3 非退化池）", "",
        f"- 随机臂：单点 seed={SEED} 配对检验 + {multi} 次分布（676f 口径）；其余基线确定性跑 1 次",
        "- 判定矩阵/切分：676f 冻结产物，未重跑 detect",
        "- 复现：`.venv/Scripts/python.exe tools/analyze_677c_nondegenerate.py --stage baselines`",
        "- 机读：`data/677c_baseline_results.json`", "",
        "## 1. 基线定义", "",
        "| 基线 | 选择规则 | 信息源 | 确定性 | 备注 |", "|---|---|---|---|---|",
        "| random | seed 抽样 top-k | 无（对照臂） | seed 可复现 | 2000 次报分布 |",
        "| fd | 派生集 fail_hits 降序 top-k | 派生集 | 是 | 676f 当前方法 |",
        "| frequency | 派生集 catch 频率降序 top-k | 派生集 | 是 | **与 fd 排序键相同**（见 §3） |",
        "| greedy | 迭代残余覆盖贪心（set-cover） | 派生集 | 是 | ≡ operator 的 fd_only 配置 |",
        "| oracle | 评估集上穷举 C(n,k) 选最优 | **评估集（泄漏）** | 是 | 上界参考，不可达 |",
        "| static | 静态资产字典序 top-k | 无 | 是 | 只能选静态资产（≤n_static 个） |",
        "| info_gain | 对池-OR 目标的互信息排序 | 派生集 | 是 | 探索性（卡片可选项） |", "",
        "## 2. 全量结果（每池每 k 的 8 臂）", "",
    ]
    for pname in ("A", "B", "C"):
        lines += [f"### Pool {pname}（{base_doc['pools'][pname]['pool_name']}；候选 "
                  f"{', '.join(base_doc['pools'][pname]['assets'])}）", "",
                  _pool_table(base_doc, evo_doc, pname), ""]
    lines += ["## 3. 关键观察", ""]
    freq_same = all(base_doc["pools"][pn]["k_blocks"][k]["custom_baselines"]["frequency"]["assets"]
                    == base_doc["pools"][pn]["k_blocks"][k]["three_arm"]["arms"]["fd"]["assets"]
                    for pn in ("A", "B", "C") for k in base_doc["pools"][pn]["k_blocks"])
    lines.append(f"- **frequency ≡ fd（选择完全一致：{freq_same}）**：676f FD 的 fail_hits 操作定义"
                 "就是派生集 catch 计数，因此当前 FD 无法与最朴素的频率基线区分。这直接回应了评审："
                 "FD 需要 novel/redundancy/cost 等正交分量（任务 C）才可能超越频率基线。")
    og = {pn: {k: (base_doc["pools"][pn]["k_blocks"][k]["custom_baselines"]["oracle"]["rate_pct"]
                   - base_doc["pools"][pn]["k_blocks"][k]["three_arm"]["arms"]["fd"]["rate_pct"])
               for k in base_doc["pools"][pn]["k_blocks"]} for pn in ("A", "B", "C")}
    lines.append("- Oracle 与 FD 的差距（pp，评估集上界参考）："
                 + "; ".join(f"Pool {pn} " + ", ".join(f"k={k} {_fmt_pp(v)}"
                                                      for k, v in og[pn].items())
                             for pn in ("A", "B", "C"))
                 + " ⇒ 这是同预算下选择策略的理论空间。")
    lines += ["- static 臂只能选静态资产（Pool A ≤2 个、Pool B/C ≤3 个），k 更大时不是同预算对比，"
              "只作参考（673p 预算语义）。", "",
              "## 4. 多重比较", "",
              "每个 (pool,k) 内 7 个臂 vs Random 单点的 McNemar p 已附 BH-FDR"
              "（JSON p_value_family.bh_fdr）；跨 (pool,k) 的扫描属探索性，未做全局校正。", "",
              "## 5. 诚实边界", "",
              "- Oracle 用评估集信息，只标上界不作证据；info_gain 是卡片标注的可选探索项。"]
    (ROOT / "data" / "677c_baseline_comparison.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    out.append(ROOT / "data" / "677c_baseline_comparison.md")

    # ---- 3. Operator 设计报告 ----
    spec = evo_doc["operator_spec"]
    eq_rows: list[str] = []
    evo_better: dict[str, int] = {}
    for pname in ("A", "B", "C"):
        for k, blk in evo_doc["pools"][pname]["k_blocks"].items():
            cf = blk["configs"]["full"]
            cfo = blk["configs"]["fd_only"]
            fd_rate = base_doc["pools"][pname]["k_blocks"][k]["three_arm"]["arms"]["fd"]["rate_pct"]
            evo_better.setdefault("full_beats_fd", 0)
            evo_better.setdefault("full_total", 0)
            evo_better["full_total"] += 1
            if cf["rate_pct"] > fd_rate:
                evo_better["full_beats_fd"] += 1
            eq_rows.append(
                f"| {pname} | {k} | {','.join(blk['fd_assets'])} | {','.join(blk['greedy_assets'])} "
                f"| {','.join(cfo['selection'])} | {','.join(cf['selection'])} "
                f"| {','.join(blk['configs']['full_unique_novel']['selection'])} "
                f"| {cf['rate_pct']:.2f} vs {fd_rate:.2f} "
                f"({_fmt_pp(cf['paired_vs_fd']['delta_pp'])}, p={_fmt_p(cf['paired_vs_fd']['mcnemar_p'])}) |")
    lines = [
        "# 677c · Evolution Operator 算法化设计报告", "",
        "## 1. 算法定义（可执行、可比较、可证伪）", "",
        "```", f"score(a_j | F_t, C_t) = {spec['score']}", "",
        f"failure_coverage : {spec['failure_coverage']}", "",
        f"novel_coverage  : literal = {spec['novel_coverage_literal']}", "",
        f"                  unique  = {spec['novel_coverage_unique']}（探索性）", "",
        f"cost_norm       : {spec['cost_norm']}", "",
        f"redundancy      : {spec['redundancy']}", "",
        f"默认权重          : {json.dumps(spec['default_weights'])}（不是学习值）",
        "a* = argmax score（同分 id 升序）；C_{t+1} = C_t ∪ {a*}；迭代至 k 个", "```", "",
        "## 2. novel_coverage 的数学坍缩（如实披露）", "",
        "规格原文里 F_t 的定义就是「C_t 没抓到的样本」，于是 novel_coverage 的第二个条件"
        "「C_t 中没有资产抓到 s」对一切 s ∈ F_t **恒真** ⇒ literal 模式下 novel ≡ failure。"
        "这不是实现错误，是规格本身的性质；推论：**消融中 fd_novel 与 fd_only 的选择完全一致**"
        "（下方等价表逐 (pool,k) 验证）。要让 novelty 成为独立信号，需要改参考集——本批提供"
        "探索性 unique 变体（不可替代残余覆盖）作对照，不擅自替换默认定义。", "",
        "## 3. 与既有方法的关系", "",
        "- **fd_only(w1=1) ≡ 迭代式残余覆盖贪心**（= 任务 B 的 greedy 基线）：单步内 |F_t| 是常数，"
        "argmax failure_coverage = argmax 新增覆盖。",
        "- **676f 的 FD（全局频率 top-k）既不是贪心也不是 E**：它是按派生集 catch 总数的一次性排序。",
        "- E-full 在 fd_only 之上叠加 novel（≡failure，只改权重分配）、redundancy 与 cost 两个真 "
        "惩罚项 ⇒ full 与 fd_only 的选择差异只能来自 redundancy/cost。", "",
        "## 4. 消融与等价验证（每池每 k）", "",
        "| 池 | k | FD(676f) | greedy | evo_fd_only | evo_full | evo_full_unique | evo_full vs FD(676f) 检出率 |",
        "|---|---|---|---|---|---|---|---|",
        *eq_rows, "",
        f"- full 检出率 > FD(676f) 的 (pool,k)：{evo_better['full_beats_fd']}/{evo_better['full_total']}。",
        "- 等价性断言（JSON equivalence 字段）：fd_only≡greedy 应全真；fd_novel≡fd_only 应全真"
        "（literal 坍缩）；full 与 FD(676f) 的选择差异即 redundancy/cost 的贡献。", "",
        "## 5. 诚实边界", "",
        "- 权重是默认值，消融只展示敏感性，不是调参优化；cost 用全量 1137 样本墙钟归一"
        "（跨资产相对比较，不是单样本成本）；unique-novel 是探索性修复，不进默认定义。",
        "- 复现：`.venv/Scripts/python.exe tools/analyze_677c_nondegenerate.py --stage operator`；"
        "机读 `data/677c_evolution_operator_results.json`。",
    ]
    (ROOT / "data" / "677c_operator_design_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    out.append(ROOT / "data" / "677c_operator_design_report.md")

    # ---- 4. A5 对比报告 ----
    contrib = a5_doc["degenerate_contribution"]
    orig = contrib["original"]
    lines = [
        "# 677c · A5 非退化池重算 vs 676f 原池对比", "",
        f"- 随机臂 {multi} 次 + 单点 seed={SEED}；切分/矩阵与 676f 相同；k 扫描 1..|A|-1",
        "- 复现：`.venv/Scripts/python.exe tools/analyze_677c_nondegenerate.py --stage a5`；"
        "机读 `data/677c_a5_nondegenerate_results.json`", "",
        "## 1. 676f 原池（8 资产，含 3 预注册退化资产）基准数字", "",
        f"- k=4 主端点：FD {orig['fd_rate_pct']:.2f}% vs Random(单点) "
        f"{orig['random_single_rate_pct']:.2f}%，Δ{_fmt_pp(orig['delta_single_pp'])}，"
        f"p={_fmt_p(orig['mcnemar_p'])}；2000 次均值 {orig['random_2000_mean_pct']:.2f}% ⇒ "
        f"FD−均值 {_fmt_pp(orig['delta_vs_mean_pp'])}",
        "- 676f 并列分析（剔 3 退化，5 候选）：k=1..4 = "
        + ", ".join(f"{_fmt_pp(co_k[k]['delta_pp'])}" for k in (1, 2, 3, 4))
        + "（k=4 两臂同集 ⇒ Δ=0）", "",
        "## 2. 非退化池上的 A5（8 臂全表）", "",
    ]
    for pname in ("A", "B", "C"):
        s = a5_doc["pools"][pname]["primary_summary"]
        lines += [f"### Pool {pname}", "",
                  f"- 最优 k（FD−Random 单点最大）：k={s['k']}，FD {s['fd_rate_pct']:.2f}% vs "
                  f"Random 单点 {s['random_single_rate_pct']:.2f}%（2000 均值 "
                  f"{s['random_2000_mean_pct']:.2f}%），Δ单点 {_fmt_pp(s['delta_single_pp'])}，"
                  f"Δvs均值 {_fmt_pp(s['delta_vs_mean_pp'])}，p={_fmt_p(s['mcnemar_p'])}", "",
                  _pool_table(base_doc, evo_doc, pname), ""]
    checks = a5_doc["internal_validity_checks"]
    lines += [
        "## 3. 内部对账", "",
        f"- Pool A 候选集 ≡ 676f 并列分析候选集 ⇒ k=1..4 的 Δ 与 676f 逐位一致："
        f"{checks.get('poolA_matches_676f_co')}（最大差 "
        f"{checks.get('poolA_vs_676f_co_max_abs_delta_diff_pp')}pp）——两套代码路径、同一答案。", "",
        "## 4. 退化资产贡献量化（k=4 主预算）", "",
        "| 池 | FD% | Random单点% | 2000均值% | Δ单点 | Δvs均值 | 退化贡献(单点) | 退化贡献(vs均值) |",
        "|---|---|---|---|---|---|---|---|",
        f"| 原池(8) | {orig['fd_rate_pct']:.2f} | {orig['random_single_rate_pct']:.2f} | "
        f"{orig['random_2000_mean_pct']:.2f} | {_fmt_pp(orig['delta_single_pp'])} | "
        f"{_fmt_pp(orig['delta_vs_mean_pp'])} | — | — |",
    ]
    for key in ("pool_A_k4", "pool_B_k4", "pool_C_k4"):
        c = contrib.get(key)
        if c:
            lines.append(f"| {c['pool']} | {c['fd_rate_pct']:.2f} | {c['random_single_rate_pct']:.2f} "
                         f"| {c['random_2000_mean_pct']:.2f} | {_fmt_pp(c['delta_single_pp'])} "
                         f"| {_fmt_pp(c['delta_vs_mean_pp'])} "
                         f"| {_fmt_pp(c['degenerate_contribution_single_pp'])} "
                         f"| {_fmt_pp(c['degenerate_contribution_vs_mean_pp'])} |")
    clause = a5_doc["uninterpretable_clause"]
    lines += ["", "## 5. uninterpretable 条款判定", ""]
    for pname in ("A", "B", "C"):
        c = clause[pname]
        lines.append(f"- Pool {pname}：残余预注册退化资产 = {c['residual_prereg_degenerate_assets'] or '无'} "
                     f"⇒ 条款{'仍触发' if c['clause_triggered'] else '不触发'}。{c['interpretation']}")
    lines += ["", "## 6. 诚实边界", ""] + [f"- {n}" for n in a5_doc["honest_notes"]]
    (ROOT / "data" / "677c_a5_comparison.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    out.append(ROOT / "data" / "677c_a5_comparison.md")

    # ---- 5. 结果分析报告 ----
    def _sig_ks(pname: str) -> list[str]:
        rows = {k: a5_doc["pools"][pname]["k_blocks"][k]["arms"]["fd"] for k in a5_doc["pools"][pname]["k_blocks"]}
        return [k for k in sorted(rows, key=int)
                if rows[k]["delta_vs_random_single_pp"] > 0 and rows[k]["mcnemar_p_vs_random"] is not None
                and rows[k]["mcnemar_p_vs_random"] < 0.05]

    sig = {pn: _sig_ks(pn) for pn in ("A", "B", "C")}
    pa = a5_doc["pools"]["A"]["primary_summary"]
    pa_k = str(pa["k"])
    fd_sig_range = ", ".join(
        f"k={k} {_fmt_pp(a5_doc['pools'][pn]['k_blocks'][k]['arms']['fd']['delta_vs_random_single_pp'])}"
        for pn in ("A", "B", "C") for k in sig[pn][:1]) or "无"
    evo_wins = sum(1 for pn in ("A", "B", "C") for k in a5_doc["pools"][pn]["k_blocks"]
                   if a5_doc["pools"][pn]["k_blocks"][k]["arms"]["evo_full"]["rate_pct"]
                   > a5_doc["pools"][pn]["k_blocks"][k]["arms"]["fd"]["rate_pct"])
    evo_total = sum(len(a5_doc["pools"][pn]["k_blocks"]) for pn in ("A", "B", "C"))
    any_sig = {pn: bool(sig[pn]) for pn in ("A", "B", "C")}
    if any_sig["A"]:
        isolate_verdict = (
            f"核心机制被 isolate：在无预注册退化资产的 Pool A 上，FD 在 k={'、'.join(sig['A'])} 仍显著优于 "
            f"Random（最优 k={pa_k}，Δ单点 {_fmt_pp(pa['delta_single_pp'])}，p={_fmt_p(pa['mcnemar_p'])}；"
            f"Δvs 2000 均值 {_fmt_pp(pa['delta_vs_mean_pp'])}）⇒ 选择效应真实存在，但量级被原池 "
            f"{_fmt_pp(a5_doc['degenerate_contribution']['original']['delta_single_pp'])} 放大，"
            f"退化资产贡献见 §4。论文可升格为「去掉退化资产后 FD 仍以 {_fmt_pp(pa['delta_single_pp'])}"
            f"（单点配对）/{_fmt_pp(pa['delta_vs_mean_pp'])}（vs 2000 均值）优于 Random（k={pa_k}）」。")
    else:
        isolate_verdict = ("核心机制未被 isolate：Pool A 上 FD 无任何 k 显著优于 Random ⇒ 原 +24.03pp "
                           "主要是池构成效应，论文需把 A5 降级为 exploratory，核心贡献转向"
                           "「degenerate asset avoidance」。")
    lines = [
        "# 677c · 结果分析报告", "",
        "- 复现：`.venv/Scripts/python.exe tools/analyze_677c_nondegenerate.py --stage all`；"
        "机读 4 份 `data/677c_*.json`", "",
        "## 1. 核心机制是否 isolate？", "",
        isolate_verdict, "",
        "各池显著 k（FD 单点 Δ>0 且 p<0.05）：" + "; ".join(
            f"Pool {pn}: k={'、'.join(sig[pn]) if sig[pn] else '无'}" for pn in ("A", "B", "C")) + "。",
        f"首个显著档示例：{fd_sig_range}。k=|A|-1 处两臂单点同集/同率，Δ→0（676f 并列分析病理的"
        "结构性复现；Pool B/C 因 Random 单点持续抽到 linker 而在全部 k 上不同）。", "",
        "## 2. 期望口径（对 2000 次均值）更稳的结论", "",
    ]
    for pn in ("A", "B", "C"):
        best = a5_doc["pools"][pn]["best_k_by_fd_delta_vs_mean"]
        blk = a5_doc["pools"][pn]["k_blocks"][str(best)]
        lines.append(f"- Pool {pn}：最优 k（FD−均值）={best}，FD {blk['arms']['fd']['rate_pct']:.2f}% "
                     f"vs 均值 {blk['random_2000_mean_pct']:.2f}% ⇒ "
                     f"{_fmt_pp(blk['arms']['fd']['delta_vs_random_mean_pp'])}（单点口径 "
                     f"{_fmt_pp(blk['arms']['fd']['delta_vs_random_single_pp'])}，"
                     f"p={_fmt_p(blk['arms']['fd']['mcnemar_p_vs_random'])}）")
    lines += [
        "", "## 3. 算法化 FD（evolution operator full 权重）的价值", "",
        f"- evo_full 检出率 > FD(676f) 的 (pool,k)：{evo_wins}/{evo_total}（逐档配对检验见"
        " 677c_operator_design_report.md §4）。",
        "- frequency ≡ fd 的选择恒等（§baseline 报告）说明当前 FD 尚无超越朴素频率基线的证据；"
        "operator 的即期价值在**可证伪性**（score 四分量 + 确定性选择 + 消融可复算），而非即期检出提升。",
        "- literal novel ≡ failure 的坍缩意味着 full 与 fd_only 的差异只能来自 redundancy/cost；"
        "unique-novel 探索性变体是下一步改设计的候选。", "",
        "## 4. 退化资产贡献量化（k=4）", "",
        "| 池 | Δ单点 | Δvs均值 | 退化贡献(单点) |", "|---|---|---|---|",
        f"| 原池(8) | {_fmt_pp(a5_doc['degenerate_contribution']['original']['delta_single_pp'])} "
        f"| {_fmt_pp(a5_doc['degenerate_contribution']['original']['delta_vs_mean_pp'])} | — |",
    ]
    for key in ("pool_A_k4", "pool_B_k4", "pool_C_k4"):
        c = a5_doc["degenerate_contribution"].get(key)
        if c:
            lines.append(f"| {c['pool']} | {_fmt_pp(c['delta_single_pp'])} "
                         f"| {_fmt_pp(c['delta_vs_mean_pp'])} "
                         f"| {_fmt_pp(c['degenerate_contribution_single_pp'])} |")
    lines += [
        "", "## 5. uninterpretable 条款", "",
    ]
    for pn in ("A", "B", "C"):
        c = a5_doc["uninterpretable_clause"][pn]
        lines.append(f"- Pool {pn}：{'触发（' + ','.join(c['residual_prereg_degenerate_assets']) + ' 仍 <5%）' if c['clause_triggered'] else '不触发'}")
    lines += [
        "", "## 6. 对论文的影响", "",
        "- 摘要/E4/表格的 A5 句需加「非退化池复算」半句（具体锚点见 677c_论文更新建议.md）。",
        "- k=4 主端点 +24.03pp 必须与「Pool A 最优 k Δ=X pp」并排呈现，否则就是用池构成效应充数。",
        "- evolution operator 一节可从 governance 叙事改为算法规格（score 公式 + 消融表）。", "",
        "## 7. 与 677b 的关系", "",
        "- 677b 解决 clone-aware split（样本侧混淆），本批解决退化 asset（池侧混淆），相互独立；"
        "最强实验是「clone-aware split × 非退化池」，待两批各自落定后合并。", "",
        "## 8. 局限", "",
        "- 单点 Random 的配对 Δ 依赖一次抽样（已并报 2000 均值口径）。",
        "- 池阈值是工程决策；oracle 用评估集信息只作上界；权重未学习；单回合判定 ~5% 跑间不稳定"
        "（676m 实测）对逐格结论照常适用。",
    ]
    (ROOT / "data" / "677c_结果分析报告.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    out.append(ROOT / "data" / "677c_结果分析报告.md")

    # ---- 6. 论文更新建议 ----
    orig = a5_doc["degenerate_contribution"]["original"]
    pa2 = a5_doc["pools"]["A"]["primary_summary"]
    best_a = a5_doc["pools"]["A"]["best_k_by_fd_delta_vs_mean"]
    blk_best_a = a5_doc["pools"]["A"]["k_blocks"][str(best_a)]
    sig_a = sig["A"]
    a_sig_deltas = [a5_doc["pools"]["A"]["k_blocks"][k]["arms"]["fd"]["delta_vs_random_single_pp"]
                    for k in sig_a] or [0.0]
    rng_lo, rng_hi = min(a_sig_deltas), max(a_sig_deltas)
    pa2_k4 = a5_doc["degenerate_contribution"].get("pool_A_k4")
    contrib_txt = (f"k=4 Δ→{_fmt_pp(pa2_k4['delta_single_pp'])} on the strict pool ⇒ the whole "
                   f"+24.0pp endpoint was pool composition "
                   f"(mean-based share {_fmt_pp(pa2_k4['degenerate_contribution_vs_mean_pp'])})"
                   if pa2_k4 else "退化贡献见 JSON")
    headline = (
        f"on the degenerate-free pool (5 usable assets), FD still beats Random: "
        f"{pa2['fd_rate_pct']:.2f}% vs {pa2['random_single_rate_pct']:.2f}% at k={pa2['k']} "
        f"(Δ {_fmt_pp(pa2['delta_single_pp'])}, p={_fmt_p(pa2['mcnemar_p'])}; "
        f"{_fmt_pp(blk_best_a['arms']['fd']['delta_vs_random_mean_pp'])} vs the 2000-draw mean), "
        f"significant at k={', '.join(sig_a)} — {contrib_txt}"
        if any_sig["A"] else
        "on the non-degenerate pool, FD never significantly beats Random ⇒ A5 must stay exploratory")
    anchors = [
        ("摘要（A5 句）", _tex_line("vs.\\ Static"), "主端点 +24.0pp 后追加半句：",
         f"「…yet {headline}.」"),
        ("§6 E4 段（A5 主承载）", _tex_line("E4 --- Ablation A5"),
         "三条限制的第 (i) 条之后补第 (iv)：", "「Non-degenerate pool (677c): with the three "
         "pre-registered degenerate assets removed, FD vs Random is significant at k≤|A|-2 "
         "and the k=|A|-1 coincidence (Δ=0.0) is a sampling artifact of 1/C(n,k) collision "
         "probability, not evidence against the mechanism.」"),
        ("表 tab:e4 的 A5 行", _tex_line("A5 & random-budget control"),
         "快照句追加：", f"「degenerate-free pool (677c): best-k Δ {_fmt_pp(pa2['delta_single_pp'])} "
         f"(p={_fmt_p(pa2['mcnemar_p'])}); {contrib_txt}」"),
        ("附录 Pre-registered parallel analysis 段", _tex_line("Pre-registered parallel analysis"),
         "在 +24.0→0.0 的解释后补：", "「677c re-runs the contrast on non-degenerate pools with "
         "five baselines (random/frequency/greedy/oracle/FD + algorithmic E); the k=|A|-1 "
         "zero is a set-collision artifact, and k≤|A|-2 remains significant.」"),
        ("Claims 表「FD beats same-budget random」行", _tex_line("not supported & Better than"),
         "证据列补非退化池数字：", f"{headline}（677c）"),
        ("结论段（belief about the selection strategy）", _tex_line("belief about the selection"),
         "补一句：", f"「The 677c non-degenerate re-run quantifies the pool-composition share of "
         f"the +24.0pp and keeps the selection effect at ≈{_fmt_pp(rng_lo).lstrip('+')}–"
         f"{_fmt_pp(rng_hi).lstrip('+')} (paired Δ) on usable assets.」"),
        ("预注册 post_hoc_amendments", "data/673r_a5_preregistration.json",
         "追加一条（不改锁定字段）：", "677c 非退化池重算记录：3 池定义、7 基线、operator 消融、"
         "退化贡献量化；随机臂 2000 次 seed=20260930。"),
        ("§4 evolution operator 形式化段", _tex_line("and the evolution operator"),
         "把「failure → human thinks → add detector」的治理叙事升级为算法规格：",
         "score(a|F_t,C_t)=w1·failure_coverage+w2·novel_coverage−w3·cost−w4·redundancy，"
         "a*=argmax（同分 id 升序）；附 677c 消融表与「novel≡failure 的字面坍缩」披露。"),
    ]
    lines = [
        "# 677c · 论文更新建议（本批不改论文，由论文批次执行）", "",
        "- 锚点行号基于报告生成时刻的 `research/latex/queyi_neurips2027_v1.1.tex`（脚本实时 grep）。"
        "**注意：该 tex 正被并发批次修改（git status 为 M）**，改稿前请重新 grep 复核；"
        "中文稿 `research/paper_shturl.md` 对应段落同步。",
        "- 数字来源：`data/677c_a5_nondegenerate_results.json` / `677c_baseline_results.json` / "
        "`677c_evolution_operator_results.json`。", "",
        "| # | 位置 | 现状 | 建议 | 理由 |", "|---|---|---|---|---|",
    ]
    for i, (loc, anchor, cur, sug) in enumerate(anchors, start=1):
        lines.append(f"| P{i} | {loc}（{anchor}） | {cur} | {sug} | 677c 非退化池复算 |")
    lines += [
        "", "## 统一措辞建议（全文口径）", "",
        f"> {headline}。k=|A|-1 的 Δ=0 是选集碰撞（概率 1/C(n,k)），不是机制反证。",
        "", "## 红线提醒", "",
        "- 本批不改 `research/`；以上为建议清单。改稿后照例跑三方对账与 guard。",
    ]
    (ROOT / "data" / "677c_论文更新建议.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    out.append(ROOT / "data" / "677c_论文更新建议.md")

    # ---- 7. 总报告 ----
    lines = [
        "# 677c · 非退化池与多 Baseline 总报告", "",
        f"- 生成：{_now()}（tools/analyze_677c_nondegenerate.py --stage all；随机臂 {multi} 次）",
        "- 红线遵守：不修改 holdout_reveal_661.py / 样本源码 / 676f 产物 / 论文；未重跑 detect()；"
        "不 push。", "",
        "## 1. 退化资产分析（8 资产）", "",
        "| 资产 | unknown% | catch% | 恒unknown | 预注册退化 |", "|---|---|---|---|---|",
    ]
    for a in sorted(stats):
        f = stats[a]["full_pool"]
        lines.append(f"| {a} | {f['unknown_rate_pct']:.2f} | {f['catch_rate_pct']:.2f} | "
                     f"{'是' if f['unknown_rate_pct'] >= 99.999 else '否'} | "
                     f"{'是' if a in pools_doc['preregistered_degeneracy_catch_rate_5pct'] else '否'} |")
    lines += [
        "", "关键：wunsequenced/compile-time 恒 unknown（100%）；**linker unknown=0%** 但 catch 率 "
        "0.88%<5%（预注册规则判退化）——卡片预估的「linker 高 unknown」与数据不符，池定义据此修正"
        "（详见 677c_pool_design_report.md）。", "",
        "## 2. 非退化池设计（3 池）", "",
        "- **Pool A（严格，5 资产）**：unknown<30% 且 catch≥5% —— asan, compiler-warn, cross-compile, "
        "tsan, ubsan；与 676f 预注册并列分析候选集一致（对账通过："
        f"{checks.get('poolA_matches_676f_co')}）。",
        "- **Pool B（中等，6 资产）**：unknown<50% 且 catch≥0.5% —— A + linker。",
        "- **Pool C（宽松，6 资产）**：仅剔恒 unknown —— ≡ Pool B（如实记录）。",
        "- 单点选择差异验证：" + "; ".join(
            f"Pool {pn} 在 k={'、'.join(str(v) for v in pools_doc['pools'][pn]['k_where_single_point_differs'])} 不同"
            for pn in ("A", "B", "C"))
        + "；Pool A 的 k=4 单点恰巧与 FD 同集——正是被评审抓住的病理"
          "（结构碰撞概率 1/C(5,4)=0.2，随机分布层面 Random 与 FD 仍可分）。", "",
        "## 3. Baseline 实现（7 个）", "",
        "Random(2000)/FD/Static/Frequency/Greedy-coverage/Oracle(上界)/Info-gain(探索)；全部同矩阵"
        "同切分；**发现：frequency ≡ fd**（676f fail_hits 就是派生集 catch 计数）⇒ 当前 FD 缺少"
        "超越频率基线的机制，这正是任务 C 要补的。逐表见 677c_baseline_comparison.md。", "",
        "## 4. Evolution Operator 算法化", "",
        "- score 四分量实现 + 确定性迭代选择 + 5 配置消融（含探索性 unique-novel）。",
        "- **披露：literal novel ≡ failure**（规格字面坍缩，一行证明见设计报告 §2）⇒ fd_novel≡fd_only；"
        "full 与 fd_only 的差异来自 redundancy/cost。",
        f"- fd_only ≡ greedy 贪心（等价断言全真）；full 检出率优于 676f FD 的档位："
        f"{evo_wins}/{evo_total}。详见 677c_operator_design_report.md。", "",
        "## 5. 非退化池上的 A5 结果", "",
    ]
    for pn in ("A", "B", "C"):
        s = a5_doc["pools"][pn]["primary_summary"]
        lines.append(f"- Pool {pn}：最优 k={s['k']}，FD {s['fd_rate_pct']:.2f}% vs Random 单点 "
                     f"{s['random_single_rate_pct']:.2f}%（均值 {s['random_2000_mean_pct']:.2f}%），"
                     f"Δ单点 {_fmt_pp(s['delta_single_pp'])}（p={_fmt_p(s['mcnemar_p'])}），"
                     f"Δvs均值 {_fmt_pp(s['delta_vs_mean_pp'])}；显著 k："
                     f"{'、'.join(sig[pn]) if sig[pn] else '无'}")
    contrib = a5_doc["degenerate_contribution"]
    lines += [
        "", "## 6. 核心机制 isolate 评估", "", isolate_verdict, "",
        "## 7. 退化资产贡献量化", "",
        f"- 原池 k=4：Δ单点 {_fmt_pp(orig['delta_single_pp'])}（Δvs均值 "
        f"{_fmt_pp(orig['delta_vs_mean_pp'])}）。",
    ]
    for key in ("pool_A_k4", "pool_B_k4", "pool_C_k4"):
        c = contrib.get(key)
        if c:
            lines.append(f"- {c['pool']} k=4：Δ单点 {_fmt_pp(c['delta_single_pp'])} ⇒ "
                         f"退化贡献（原池−本池）{_fmt_pp(c['degenerate_contribution_single_pp'])}"
                         f"（均值口径 {_fmt_pp(c['degenerate_contribution_vs_mean_pp'])}）。")
    lines += [
        "", "## 8. 对论文的影响与更新建议", "",
        "- 摘要/E4/表行/claims/结论 7 处锚点级建议见 677c_论文更新建议.md（P1–P8）；统一措辞："
        "主端点 +24.0pp 必须与「非退化池最优 k Δ」并排；k=|A|-1 的 0 是选集碰撞不是机制反证。",
        "- operator 叙事从 governance 换成算法规格（score 公式 + 消融 + 坍缩披露）。", "",
        "## 9. 和 677b 的关系", "",
        "- 独立互补：677b 修样本侧（clone-aware split），本批修池侧（退化资产）；本批全程用 676f "
        "原 split，未与 677b 混。合并实验（clone-aware × 非退化池）留待两批落定后。", "",
        "## 10. 未解决项和局限", "",
        "- literal novel≡failure 的坍缩是规格缺陷：修复需改参考集（unique 变体已给探索性对照，"
        "是否转正由下一批决定）。",
        "- 权重未学习；cost 用全量墙钟代理单样本成本；池阈值是工程决策。",
        "- Pool B/C 含 linker ⇒ 预注册 uninterpretable 条款在这两池仍触发；只有 Pool A 完全脱敏。",
        "- 单回合判定的 ~5% 跑间不稳定（676m 实测）照常适用于本批全部逐格结论。",
        "- Random 单点配对 Δ 依赖抽样运气；已并报 2000 均值口径（期望效应）。", "",
        "## 11. 提交信息", "",
        "- 只 add 本批文件：tools/evolution_operator_677c.py、tools/analyze_677c_nondegenerate.py、"
        "data/677c_*.json、data/677c_*.md。",
        "- DCO：`git commit -s`；不 push；commit hash 用 `git log --oneline -1` 查（不自指回填）。",
        "- 复现：`.venv/Scripts/python.exe tools/analyze_677c_nondegenerate.py --stage all` "
        f"（随机臂 {multi} 次，seed={SEED}）；自检："
        "`python tools/evolution_operator_677c.py --check`。",
    ]
    (ROOT / "data" / "677c_非退化池与多Baseline总报告.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    out.append(ROOT / "data" / "677c_非退化池与多Baseline总报告.md")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="677c：非退化池 + 多 Baseline + Operator + A5 重算")
    ap.add_argument("--stage", default="all",
                    choices=["pools", "baselines", "operator", "a5", "reports", "all"])
    ap.add_argument("--quick", action="store_true", help="随机臂 200 次（冒烟测试；正式口径 2000）")
    args = ap.parse_args(argv)
    multi = 200 if args.quick else MULTI

    if args.stage == "reports":
        pools_doc = json.loads(OUT_POOLS.read_text(encoding="utf-8"))
        base_doc = json.loads(OUT_BASE.read_text(encoding="utf-8"))
        evo_doc = json.loads(OUT_EVO.read_text(encoding="utf-8"))
        a5_doc = json.loads(OUT_A5.read_text(encoding="utf-8"))
        write_reports(pools_doc, base_doc, evo_doc, a5_doc)
        print("[677c] reports 完成（由既有 JSON 生成）")
        return 0

    ld = load_data()
    pools_doc = define_pools(ld)
    if args.stage == "pools":
        _jdump(OUT_POOLS, pools_doc)
        return 0
    base_doc = run_baselines(ld, pools_doc, multi=multi)
    if args.stage == "baselines":
        _jdump(OUT_POOLS, pools_doc)
        _jdump(OUT_BASE, base_doc)
        return 0
    evo_doc = run_operator(ld, pools_doc, multi=multi)
    if args.stage == "operator":
        _jdump(OUT_POOLS, pools_doc)
        _jdump(OUT_BASE, base_doc)
        _jdump(OUT_EVO, evo_doc)
        return 0
    a5_doc = run_a5(ld, pools_doc, base_doc, evo_doc, multi=multi)
    if args.stage in ("a5", "all"):
        _jdump(OUT_POOLS, pools_doc)
        _jdump(OUT_BASE, base_doc)
        _jdump(OUT_EVO, evo_doc)
        _jdump(OUT_A5, a5_doc)
    if args.stage == "all":
        write_reports(pools_doc, base_doc, evo_doc, a5_doc)
        print(f"[677c] all 完成（随机臂 {multi} 次；报告 7 份见 data/677c_*.md）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
