#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran（阿信）
"""676f 分析面：在全量判定矩阵上重跑 A5（主 / 并列 / 子组 / planted=false / k 敏感）。

统计原语**全部复用** 673p/673r 既有实现（不改口径）：
* `tools/run_a5_experiment_673p.py::real_budget_comparison`（三臂 + 配对检验 + 2000 次随机分布）
* `tools/selection_strategies_673p.py::select`（FD / Random / Static 的选择语义）
* `tools/verifier_pool_673p.py::ASSET_POOL`（8 项已实测资产）

输入：data/a5_676f_sample_manifest.json + data/a5_676f_detection_matrix.json
输出：data/a5_676f_results.json

诚实边界：本脚本不做任何“挑好看”的筛选——所有视图（主/并列/子组/子集/扫描）都落盘，
子组 p 值另附 BH-FDR 与 Bonferroni 校正。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "data"))

import run_a5_experiment_673p as a5  # noqa: E402  统计/三臂原语（未改动）
import selection_strategies_673p as ss  # noqa: E402
import verifier_pool_673p as vp  # noqa: E402

MANIFEST = ROOT / "data" / "a5_676f_sample_manifest.json"
MATRIX = ROOT / "data" / "a5_676f_detection_matrix.json"
OUT = ROOT / "data" / "a5_676f_results.json"

ASSETS = list(vp.selectable_ids(vp.ASSET_POOL))
PRIMARY_K = a5.PRIMARY_K              # 4（673r 预注册主预算）
SEED = a5.SEED                        # 20260930（Random 臂单点 + 2000 次分布）
MULTI = a5.MULTI_SEED_N               # 2000
SWEEP = (1, 2, 3, 4, 5, 6, 7, 8)
DEG_HI, DEG_LO = 0.95, 0.05           # 676f 卡的退化阈值（>95% 或 <5% ⇒ 常量资产）


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _jload(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


# ─────────────────────────────────────────────────────────────────────────────
# 基础量
# ─────────────────────────────────────────────────────────────────────────────
def index_of(matrix: dict) -> dict:
    return {r["sample_id"]: {a: r["per_asset"][a] for a in ASSETS} for r in matrix["samples"]}


def fail_hits_real(rows: list[dict], assets, index) -> dict:
    cnt = {a: 0 for a in assets}
    for r in rows:
        row = index[r["sample_id"]]
        for a in assets:
            if row.get(a) == "catch":
                cnt[a] += 1
    return cnt


def rates(rows: list[dict], assets, index) -> dict:
    n = len(rows)
    out = {}
    for a in assets:
        k = sum(1 for r in rows if index[r["sample_id"]].get(a) == "catch")
        unk = sum(1 for r in rows if index[r["sample_id"]].get(a) == "unknown")
        out[a] = {"catch": k, "unknown": unk, "miss": n - k - unk, "n": n,
                  "catch_rate_pct": round(k / n * 100, 4) if n else None,
                  "unknown_rate_pct": round(unk / n * 100, 4) if n else None}
    return out


def degenerate(rows: list[dict], assets, index, hi=DEG_HI, lo=DEG_LO) -> dict:
    rr = rates(rows, assets, index)
    out = {}
    for a, v in rr.items():
        rate = (v["catch_rate_pct"] or 0) / 100
        if v["n"] and (rate > hi or rate < lo):
            out[a] = {"catch_rate_pct": v["catch_rate_pct"], "flag": "degenerate_constant",
                      "why": f"catch 率 {v['catch_rate_pct']}% 越出 [{lo*100:.0f}%, {hi*100:.0f}%]"}
    return out


def as_exec_rows(rows: list[dict]) -> list[dict]:
    """给 a5 的 Executor/统计函数用的行（它们只认 `id` 键）。"""
    return [{"id": r["sample_id"]} for r in rows]


def compare(rows: list[dict], index, candidates: list[str], k: int,
            fail_hits: dict, *, multi: int = MULTI) -> dict:
    """复用 673r 的三臂对照（FD 的 fail_hits 必须来自派生集）。"""
    ex = a5.AttributionExecutor(index)
    return a5.real_budget_comparison(
        as_exec_rows(rows), ex, index, vp.ASSET_POOL,
        candidates=list(candidates), k=k, seed=SEED, multi_seed_n=multi,
        fail_hits={a: int(fail_hits.get(a, 0)) for a in candidates})


def by_k(rows: list[dict], index, candidates: list[str], fail_hits: dict,
         ks=SWEEP, *, multi: int = MULTI) -> list[dict]:
    out = []
    for k in ks:
        if k > len(candidates):
            continue
        row = compare(rows, index, candidates, k, fail_hits, multi=multi)
        row["k_requested"] = k
        out.append(row)
    return out


def compact(block: dict) -> dict:
    """把一档 k 的三臂结果压成可读结构（全部字段原样保留在 by_k 里）。"""
    ar = block["arms"]
    t = block["paired_tests"]
    return {
        "k": block["budget_k"],
        "fd_assets": ar["fd"]["assets"], "random_assets": ar["random"]["assets"],
        "static_assets": ar["static"]["assets"], "full_pool_assets": ar["fd_full_pool"]["assets"],
        "fd_rate_pct": ar["fd"]["rate_pct"], "fd_k": ar["fd"]["k"], "n": ar["fd"]["n"],
        "random_rate_pct": ar["random"]["rate_pct"],
        "static_rate_pct": ar["static"]["rate_pct"],
        "full_pool_rate_pct": ar["fd_full_pool"]["rate_pct"],
        "delta_fd_minus_random_pp": t["fd_vs_random"]["delta_pp"],
        "delta_ci95_pp": t["fd_vs_random"]["delta_ci95_pp"],
        "mcnemar_p": t["fd_vs_random"]["mcnemar_p"],
        "mcnemar_log10_bound": mcnemar_log10_bound(t["fd_vs_random"]["discordant_a_only"],
                                                   t["fd_vs_random"]["discordant_b_only"]),
        "b": t["fd_vs_random"]["discordant_a_only"], "c": t["fd_vs_random"]["discordant_b_only"],
        "cohens_h": t["fd_vs_random"]["cohens_h"],
        "delta_fd_minus_static_pp": t["fd_vs_static"]["delta_pp"],
        "mcnemar_p_vs_static": t["fd_vs_static"]["mcnemar_p"],
        "random_2000": {kk: block["random_multi_seed"][kk] for kk in
                        ("mean_rate_pct", "sd_pp", "min_rate_pct", "max_rate_pct",
                         "percentile_2.5_pct", "percentile_97.5_pct",
                         "fd_strictly_better_frac", "fd_better_or_tie_frac")},
    }


def primary_of(rows_by_k: list[dict], k: int = PRIMARY_K) -> dict | None:
    for r in rows_by_k:
        if r["budget_k"] == k:
            return compact(r)
    return None


# ─────────────────────────────────────────────────────────────────────────────
# 多重比较校正
# ─────────────────────────────────────────────────────────────────────────────
def mcnemar_log10_bound(b: int, c: int) -> float | None:
    """精确 McNemar 在双精度下溢（p==0.0）时，给出双侧 p 的 log10 上界。"""
    n = b + c
    if n == 0 or a5.mcnemar_exact_p(b, c) > 0.0:
        return None
    m = min(b, c)
    ln10 = math.log(10)
    logs = [(math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1)) / ln10
            for i in range(m + 1)]
    mx = max(logs)
    s = mx + math.log10(sum(10 ** (x - mx) for x in logs))
    return round(math.log10(2) + s - n * math.log10(2), 1)


def _stability_split() -> dict:
    """稳定性抽检按“超时帽前后”分开统计（两批的 cap 口径不同，不得混算）。"""
    p = ROOT / "data" / "a5_676f_matrix_stability.jsonl"
    if not p.is_file():
        return {"status": "skip"}
    rows = [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
    out: dict[str, dict] = {}
    for name, lo, hi in (("pre_cap_run(120s/180s)", "", "2026-10-04T00:40"),
                         ("capped_run(5s)", "2026-10-04T00:40", "")):
        sel = [r for r in rows if (not lo or r["at"] >= lo) and (not hi or r["at"] < hi)]
        if not sel:
            continue
        same = sum(1 for r in sel if len(set(r["votes"])) == 1)
        out[name] = {"n": len(sel), "rounds": len(sel[0]["votes"]),
                     "all_rounds_identical": same,
                     "identical_pct": round(same / len(sel) * 100, 2),
                     "flip_samples": [r["sample_id"] for r in sel if len(set(r["votes"])) > 1],
                     "vote_distribution": _dist_votes(sel)}
    return out if out else {"status": "skip"}


def _dist_votes(rows: list[dict]) -> dict:
    out: dict[str, int] = {}
    for r in rows:
        for v in r["votes"]:
            out[v] = out.get(v, 0) + 1
    return out


def _split_x_group(samples: list[dict]) -> dict:
    out: dict[str, int] = {}
    for r in samples:
        k = f"{r['split']}/{r['defect_group']}"
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items()))


def bh_fdr(pvals: list[float]) -> list[float]:
    """Benjamini–Hochberg FDR（同序返回）。"""
    m = len(pvals)
    if m == 0:
        return []
    order = sorted(range(m), key=lambda i: pvals[i])
    q = [0.0] * m
    prev = 1.0
    for rank, i in enumerate(reversed(order), start=1):
        idx = m - rank + 1
        val = min(prev, pvals[i] * m / idx)
        q[i] = val
        prev = val
    return q


def bonferroni(pvals: list[float]) -> list[float]:
    m = len(pvals)
    return [min(1.0, p * m) for p in pvals]


# ─────────────────────────────────────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────────────────────────────────────
def run(multi: int = MULTI, sweep: tuple = SWEEP) -> dict:
    man = _jload(MANIFEST)
    mat = _jload(MATRIX)
    index = index_of(mat)
    samples = man["samples"]
    for r in samples:
        if r["sample_id"] not in index:
            raise KeyError(f"样本 {r['sample_id']} 不在判定矩阵里（fail-loud）")

    deriv = [r for r in samples if r["split"] == "derivation"]
    ev = [r for r in samples if r["split"] == "evaluation"]
    planted_t = [r for r in samples if r["planted"]]
    planted_f = [r for r in samples if not r["planted"]]
    fh = fail_hits_real(deriv, ASSETS, index)

    t0 = time.perf_counter()

    # 退化诊断：全池（卡片口径）与派生集（无评估信息口径）各算一份
    degen_full = degenerate(samples, ASSETS, index)
    degen_deriv = degenerate(deriv, ASSETS, index)
    co_full = [a for a in ASSETS if a not in degen_full]
    co_deriv = [a for a in ASSETS if a not in degen_deriv]

    # 主分析（8 项候选）
    main_by_k = by_k(ev, index, ASSETS, fh, ks=sweep, multi=multi)
    # 并列分析（剔除退化资产；卡片口径 = 全池率）
    co_by_k = by_k(ev, index, co_full, fh, ks=sweep, multi=multi) if len(co_full) < len(ASSETS) else []
    co_deriv_by_k = (by_k(ev, index, co_deriv, fh, ks=sweep, multi=multi)
                     if len(co_deriv) < len(ASSETS) else [])
    # 全池对照（fail_hits 来自评测集自身 ⇒ oracle，仅连续性对照）
    oracle_by_k = []
    for k in (PRIMARY_K,):
        row = compare(ev, index, ASSETS, k, fail_hits_real(ev, ASSETS, index), multi=multi)
        row["oracle_note"] = "fail_hits 与评测集同一批样本 ⇒ oracle，不作证据"
        oracle_by_k.append(row)

    # 子组（按粗粒度缺陷组）
    groups: dict[str, list[dict]] = {}
    for r in samples:
        groups.setdefault(r["defect_group"], []).append(r)
    subgroups = {}
    for g, rows_all in sorted(groups.items()):
        g_ev = [r for r in rows_all if r["split"] == "evaluation"]
        g_der = [r for r in rows_all if r["split"] == "derivation"]
        if len(g_ev) < 10:
            subgroups[g] = {"status": "skip", "why": f"评估集 n={len(g_ev)} < 10",
                            "n_derivation": len(g_der), "n_evaluation": len(g_ev)}
            continue
        bk = by_k(g_ev, index, ASSETS, fh, ks=(PRIMARY_K,), multi=multi)
        c = compact(bk[0])
        c.update({"n_derivation": len(g_der), "n_evaluation": len(g_ev),
                  "fd_fail_hits_top": sorted(fh.items(), key=lambda kv: (-kv[1], kv[0]))[:4],
                  "rates_evaluation": rates(g_ev, ASSETS, index)})
        subgroups[g] = c

    # planted=false（外部效度）与 planted=true 对照：都用派生集 fail_hits
    def subset_block(rows_all: list[dict], name: str) -> dict:
        s_ev = [r for r in rows_all if r["split"] == "evaluation"]
        s_der = [r for r in rows_all if r["split"] == "derivation"]
        if not s_ev:
            return {"status": "skip", "why": "评估集为空"}
        bk = by_k(s_ev, index, ASSETS, fh, ks=(PRIMARY_K,), multi=multi)
        c = compact(bk[0])
        c.update({"n_derivation": len(s_der), "n_evaluation": len(s_ev),
                  "n_evaluation_batches": sorted({r["source_batch"] for r in s_ev}),
                  "or_catch_rate_evaluation_pct": round(
                      sum(1 for r in s_ev
                          if any(index[r["sample_id"]].get(a) == "catch" for a in ASSETS))
                      / len(s_ev) * 100, 4)})
        return c

    pf = subset_block(planted_f, "planted_false")
    pt = subset_block(planted_t, "planted_true")
    # 只在扩样-G 的 planted=false 上（卡片指定）
    g_pf = [r for r in planted_f if r["source_batch"] == "expG"]
    gpf = subset_block(g_pf, "expG_planted_false")

    # 旧口径对照（时间切分：派生=legacy 95 / 评估=扩样 1042）
    legacy = [r for r in samples if r["origin"] == "legacy"]
    expansion = [r for r in samples if r["origin"] == "expansion"]
    fh_legacy = fail_hits_real(legacy, ASSETS, index)
    legacy_view = by_k(expansion, index, ASSETS, fh_legacy, ks=(PRIMARY_K,), multi=multi)
    legacy_co = [a for a in ASSETS if a not in degenerate(legacy, ASSETS, index)]
    legacy_co_view = by_k(expansion, index, legacy_co, fh_legacy, ks=(PRIMARY_K,), multi=multi)

    doc = {
        "schema": "queyi-a5-676f-results/v1",
        "generated_by": "data/676f_analysis.py",
        "generated_at": _now(),
        "inputs": {
            "manifest": "data/a5_676f_sample_manifest.json",
            "matrix": "data/a5_676f_detection_matrix.json",
            "matrix_generated_at": mat.get("generated_at"),
            "detector_sha256_16": mat.get("detector_sha256_16"),
        },
        "design": {
            "primary_k": PRIMARY_K, "sweep_k": list(sweep), "seed": SEED,
            "multi_seed_runs": multi,
            "candidates": ASSETS,
            "split_rule": man["split_rule"],
            "fd_fail_hits_source": "派生集（split=derivation，n=%d）——不含评估集信息" % len(deriv),
            "statistics": {
                "paired": "exact McNemar（双侧）+ Δ 的 95% CI（不一致对标准误，McNemar 口径 Wald）",
                "arms": "Clopper–Pearson 95%（tools/stat_bounds.py）",
                "effect_size": "Cohen's h",
                "multiplicity": "子组 p 值另附 BH-FDR 与 Bonferroni（报告里同时给原始 p）",
                "random_arm": "单点 seed=20260930 用于配对检验；另跑 %d 次报分布" % multi,
            },
        },
        "sample_stats": {
            "n_total": len(samples),
            "n_derivation": len(deriv), "n_evaluation": len(ev),
            "n_planted_true": len(planted_t), "n_planted_false": len(planted_f),
            "n_legacy": len(legacy), "n_expansion": len(expansion),
            "by_batch": man["stats"]["by_source_batch"],
            "by_group": man["stats"]["by_defect_group"],
            "by_split_x_group": _split_x_group(samples),
            "dedup": {"by_id": man["n_dedup_by_id"], "by_content": man["n_dedup_by_content"],
                      "detail": man["dedup_by_content"]},
        },
        "matrix_quality": {
            "coverage": mat["coverage"],
            "unknown_ratio": mat["unknown_ratio"],
            "per_asset_distribution": mat["per_asset_distribution"],
            "or_verdict_distribution": mat["or_verdict_distribution"],
            "verify_old_vs_673r": mat["verify_old_vs_673r"],
            "stability_concurrency": mat["stability_concurrency"],
            "stability_concurrency_by_cap_regime": _stability_split(),
            "wall_seconds_by_asset": mat["wall_seconds_by_asset"],
        },
        "asset_diagnostics": {
            "full_pool": rates(samples, ASSETS, index),
            "derivation": rates(deriv, ASSETS, index),
            "evaluation": rates(ev, ASSETS, index),
            "degenerate_full_pool": degen_full,
            "degenerate_derivation": degen_deriv,
            "co_primary_candidates_full_pool_rule": co_full,
            "co_primary_candidates_derivation_rule": co_deriv,
        },
        "derivation_fail_hits": fh,
        "primary_main_8candidates": {
            "by_k": main_by_k,
            "by_k_compact": [compact(r) for r in main_by_k],
            "primary": primary_of(main_by_k),
        },
        "co_primary_excl_degenerate": {
            "candidates": co_full, "by_k": co_by_k, "by_k_compact": [compact(r) for r in co_by_k],
            "primary": primary_of(co_by_k),
            "candidates_derivation_rule": co_deriv,
            "by_k_derivation_rule": co_deriv_by_k,
            "by_k_compact_derivation_rule": [compact(r) for r in co_deriv_by_k],
            "primary_derivation_rule": primary_of(co_deriv_by_k),
        },
        "oracle_fullset_continuity": {"by_k": oracle_by_k, "by_k_compact": [compact(r) for r in oracle_by_k],
                                      "primary": primary_of(oracle_by_k)},
        "subgroups": subgroups,
        "subgroup_multiplicity": _multiplicity(subgroups),
        "planted_false": pf,
        "planted_true": pt,
        "expG_planted_false_only": gpf,
        "legacy_time_split_view": {
            "note": "673r 口径的连续性视角：派生集 = 旧 105（去重后 %d），评估集 = 扩样 %d" %
                    (len(legacy), len(expansion)),
            "fail_hits": fh_legacy,
            "primary_8candidates": primary_of(legacy_view),
            "co_primary": primary_of(legacy_co_view),
            "co_candidates": legacy_co,
        },
        "wall_seconds_analysis": round(time.perf_counter() - t0, 2),
        "honest_notes": [
            "所有判定来自真实 detect()；unknown 绝不当 miss（OR 聚合与 673r 同口径）。",
            "旧 105 样本复用 673r 矩阵（post-673u），其中 12 个样本本次现场重跑做抽检。",
            "FD 的 fail_hits 只来自派生集（split=derivation）⇒ FD 不是 oracle。",
            "k 扫描与子组分析为探索性：子组 p 附 BH-FDR/Bonferroni，未校正的原始 p 不得单独宣称显著。",
            "退化资产的并列分析给两套口径：全池率（卡片指定）与派生集率（不含评估信息）；两套都落盘。",
            "oracle_fullset_continuity 的 fail_hits 与评测集同批 ⇒ 仅作与 673p 的连续性对照，不作证据。",
        ],
    }
    return doc


def _multiplicity(subgroups: dict) -> dict:
    tested = [(g, v) for g, v in subgroups.items() if isinstance(v, dict) and "mcnemar_p" in v]
    if not tested:
        return {"n_tests": 0}
    ps = [v["mcnemar_p"] for _, v in tested]
    qs = bh_fdr(ps)
    bs = bonferroni(ps)
    rows = [{"group": g, "p_raw": v["mcnemar_p"], "p_bh_fdr": round(q, 6),
             "p_bonferroni": round(b, 6), "delta_pp": v["delta_fd_minus_random_pp"],
             "n_evaluation": v["n_evaluation"]}
            for (g, v), q, b in zip(tested, qs, bs)]
    rows.sort(key=lambda r: r["p_raw"])
    return {"n_tests": len(rows), "method": "BH-FDR + Bonferroni（对子组 McNemar p）", "rows": rows}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="676f A5 分析")
    ap.add_argument("--multi-seed", type=int, default=MULTI)
    ap.add_argument("--quick", action="store_true", help="只跑主/并列（k=4），少跑 2000 次")
    a = ap.parse_args(argv)
    multi = 200 if a.quick else a.multi_seed
    sweep = (PRIMARY_K,) if a.quick else SWEEP
    doc = run(multi=multi, sweep=sweep)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8", newline="\n")
    pm = doc["primary_main_8candidates"]["primary"]
    cp = doc["co_primary_excl_degenerate"]["primary"]
    print(f"[676f] n={doc['sample_stats']['n_total']} "
          f"(派生 {doc['sample_stats']['n_derivation']} / 评估 {doc['sample_stats']['n_evaluation']})")
    print(f"[676f] 主分析 k=4: FD {pm['fd_rate_pct']}% vs Random {pm['random_rate_pct']}% "
          f"Δ{pm['delta_fd_minus_random_pp']:+.2f}pp p={pm['mcnemar_p']:.4g} "
          f"CI{pm['delta_ci95_pp']} | FD 优于随机 {pm['random_2000']['fd_strictly_better_frac']*100:.1f}%")
    if cp:
        print(f"[676f] 并列（剔除退化 {doc['co_primary_excl_degenerate']['candidates']}）k=4: "
              f"FD {cp['fd_rate_pct']}% vs Random {cp['random_rate_pct']}% "
              f"Δ{cp['delta_fd_minus_random_pp']:+.2f}pp p={cp['mcnemar_p']:.4g}")
    print(f"[676f] 退化（全池率）: {list(doc['asset_diagnostics']['degenerate_full_pool'])}")
    print(f"[676f] 写入 {OUT.relative_to(ROOT).as_posix()}（分析墙钟 {doc['wall_seconds_analysis']}s）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
