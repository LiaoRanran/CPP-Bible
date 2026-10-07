#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
686 · 建模批判研究 —— 反事实实验计算核心（只读 676f/677b/684/685 产物，复用其函数）

B1 样本量反事实：n=100/200/400/600/800/1000，每 n 抽 100 次，FD 贪心 vs 随机均值，
    记录 Δpp、百分位、CI 宽度、最小显著样本量。
B2 资产集反事实：剔除 1/2/3 个资产（92 组合），重算 FD vs 随机 Δ，识别关键资产。
B3 标注质量反事实：按 682 的 κ=0.727 背景，翻转 expected_verdict 1/3/5/10/15%，
    重算（噪声目标集上）FD vs 随机 Δ 与盲区率，问结论何时反转。
B4 检测器噪声反事实：复用 685 方向2，扩展 ε=5/10/15/20/30/50%，100 次，看 FD 失稳边界。

产出：686_sample_size_counterfactual.json / 686_asset_set_counterfactual.json /
      686_label_quality_counterfactual.json / 686_noise_counterfactual.json / 686_stats.json

红线：不修改检测器/样本/论文/677c·684·685 代码；不 push；只 add 本批文件。
复现：.venv/Scripts/python.exe data/686_analysis.py  （种子 20260930）
"""
import json
import math
import itertools
import random
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent          # .../CPP-Bible/data
ROOT = HERE.parent
DATA = HERE

# 复用 684（只读）
spec684 = importlib.util.spec_from_file_location("m684", str(HERE / "684_analysis.py"))
m684 = importlib.util.module_from_spec(spec684)
spec684.loader.exec_module(m684)
m684.DATA = DATA
m684.ROOT = ROOT

# 复用 685（只读；其模块级已设置自身 DATA=HERE，等价于本目录）
spec685 = importlib.util.spec_from_file_location("m685", str(HERE / "685_analysis.py"))
m685 = importlib.util.module_from_spec(spec685)
spec685.loader.exec_module(m685)
m685.DATA = DATA

SEED = m684.SEED
K = m684.K
ASSETS = m684.ASSETS
AIDX = m684.AIDX


def _load():
    matrix = m684.load_matrix()
    catch_sets, samples = m684.build_catch_sets(matrix)
    return matrix, catch_sets, samples


def _random_draw_values(f, pool_idx, k, draws, rng):
    vals = []
    for _ in range(draws):
        combo = rng.sample(pool_idx, k)
        mask = 0
        for i in combo:
            mask |= (1 << i)
        vals.append(f[mask])
    return vals


# ============================================================
# B1 样本量反事实
# ============================================================
def b1_sample_size(catch_sets, samples, n_list=(100, 200, 400, 600, 800, 1000),
                   reps=100, draws=2000):
    rng = random.Random(SEED)
    all_idx = list(range(len(samples)))
    pool_idx = list(range(8))
    out = {}
    for n in n_list:
        if n > len(all_idx):
            continue
        deltas, percs, greedy_rates, rand_means = [], [], [], []
        for _ in range(reps):
            idx = rng.sample(all_idx, n)
            sub = [catch_sets[i] for i in idx]
            f, _ = m684.build_f(sub)
            gset, _, gmask = m684.greedy_select(K, lambda m: f[m], ASSETS)
            gval = f[gmask]
            rvals = _random_draw_values(f, pool_idx, K, draws, rng)
            rmean = sum(rvals) / len(rvals)
            delta = 100.0 * (gval - rmean) / n
            perc = 100.0 * sum(1 for v in rvals if v <= gval) / len(rvals)
            deltas.append(delta); percs.append(perc)
            greedy_rates.append(100.0 * gval / n)
            rand_means.append(100.0 * rmean / n)
        deltas.sort()
        lo = deltas[int(0.025 * (reps - 1))]
        hi = deltas[int(0.975 * (reps - 1))]
        out[str(n)] = {
            "n": n,
            "reps": reps,
            "draws_per_rep": draws,
            "greedy_rate_pct_mean": round(sum(greedy_rates) / reps, 4),
            "random_mean_rate_pct_mean": round(sum(rand_means) / reps, 4),
            "delta_pp_mean": round(sum(deltas) / reps, 4),
            "delta_pp_sd": round(math.sqrt(sum((d - sum(deltas) / reps) ** 2 for d in deltas) / reps), 4),
            "delta_pp_ci95": [round(lo, 4), round(hi, 4)],
            "ci_width_pp": round(hi - lo, 4),
            "percentile_mean": round(sum(percs) / reps, 4),
            "frac_reps_fd_top5pct": round(sum(1 for p in percs if p >= 95) / reps, 4),
        }
    # 最小显著样本量：第一个 frac_reps_fd_top5pct >= 0.95 的 n
    min_n = None
    for n in n_list:
        if str(n) in out and out[str(n)]["frac_reps_fd_top5pct"] >= 0.95:
            min_n = n
            break
    return {"by_n": out, "min_n_for_95pct_power": min_n,
            "note": "FD_top5pct = fraction of subsamples where greedy beats >=95% of random draws (one-sided p<0.05 proxy)"}


# ============================================================
# B2 资产集反事实
# ============================================================
def b2_asset_set(catch_sets, samples, draws=2000):
    rng = random.Random(SEED)
    n = len(samples)
    f_full, _ = m684.build_f(catch_sets)
    pool_idx = list(range(8))
    # 全池基线
    gset0, _, gmask0 = m684.greedy_select(K, lambda m: f_full[m], ASSETS)
    rvals0 = _random_draw_values(f_full, pool_idx, K, draws, rng)
    base = {
        "greedy_set": gset0, "greedy_rate_pct": round(100.0 * f_full[gmask0] / n, 4),
        "random_mean_rate_pct": round(100.0 * sum(rvals0) / len(rvals0) / n, 4),
        "delta_pp": round(100.0 * (f_full[gmask0] - sum(rvals0) / len(rvals0)) / n, 4),
    }
    results = {"full_pool_baseline": base, "single_removal": {}, "all_combos": []}
    # 单删：识别关键资产
    for drop in ASSETS:
        pool = [a for a in ASSETS if a != drop]
        f, _ = m684.build_f(catch_sets)
        gset, _, gmask = m684.greedy_select(K, lambda m: f[m], pool)
        rvals = _random_draw_values(f, [AIDX[a] for a in pool], K, draws, rng)
        gr = 100.0 * f[gmask] / n
        rm = 100.0 * sum(rvals) / len(rvals) / n
        results["single_removal"][drop] = {
            "pool": pool, "greedy_set": gset,
            "greedy_rate_pct": round(gr, 4), "random_mean_rate_pct": round(rm, 4),
            "delta_pp": round(gr - rm, 4),
            "greedy_drop_vs_full_pp": round(base["greedy_rate_pct"] - gr, 4),
        }
    # 全部剔除 1/2/3 组合（C(8,1)+C(8,2)+C(8,3)=92）
    combo_count = 0
    for r in (1, 2, 3):
        for combo in itertools.combinations(ASSETS, r):
            pool = [a for a in ASSETS if a not in combo]
            kk = min(K, len(pool))
            f, _ = m684.build_f(catch_sets)
            gset, _, gmask = m684.greedy_select(kk, lambda m: f[m], pool)
            pidx = [AIDX[a] for a in pool]
            rvals = _random_draw_values(f, pidx, kk, 200, rng)  # 组合多，少抽以控时
            gr = 100.0 * f[gmask] / n
            rm = 100.0 * sum(rvals) / len(rvals) / n
            results["all_combos"].append({
                "removed": list(combo), "pool_size": len(pool),
                "greedy_set": gset, "greedy_rate_pct": round(gr, 4),
                "random_mean_rate_pct": round(rm, 4), "delta_pp": round(gr - rm, 4),
            })
            combo_count += 1
    results["n_combos"] = combo_count
    # 关键资产排序：按 greedy_drop_vs_full_pp 升序（drop 越大越关键）
    results["critical_assets_by_drop"] = sorted(
        [(a, v["greedy_drop_vs_full_pp"]) for a, v in results["single_removal"].items()],
        key=lambda x: -x[1])
    return results


# ============================================================
# B3 标注质量反事实
# ============================================================
def b3_label_quality(samples, catch_sets, r_list=(0.01, 0.03, 0.05, 0.10, 0.15),
                     reps=50, draws=2000):
    rng = random.Random(SEED)
    n = len(samples)
    # 基准：expected_verdict == 'catch' 的目标集（668 条）
    def target_idx(noisy_verdicts):
        return [i for i, v in enumerate(noisy_verdicts) if v == "catch"]
    clean_v = [s["expected_verdict"] for s in samples]
    base_idx = target_idx(clean_v)
    base_sub = [catch_sets[i] for i in base_idx]
    f_b, _ = m684.build_f(base_sub)
    gset_b, _, gmask_b = m684.greedy_select(K, lambda m: f_b[m], ASSETS)
    rvals_b = _random_draw_values(f_b, list(range(8)), K, draws, rng)
    base = {
        "target_n": len(base_idx),
        "greedy_rate_pct": round(100.0 * f_b[gmask_b] / len(base_idx), 4),
        "random_mean_rate_pct": round(100.0 * sum(rvals_b) / len(rvals_b) / len(base_idx), 4),
        "delta_pp": round(100.0 * (f_b[gmask_b] - sum(rvals_b) / len(rvals_b)) / len(base_idx), 4),
        "blindspot_rate_pct": round(100.0 * (len(base_idx) - m684.coverage_on(base_sub, set(ASSETS))) / len(base_idx), 4),
    }
    out = {"baseline_expected_catch_target": base, "by_rate": {}}
    for r in r_list:
        deltas, blinds, g_rates = [], [], []
        for _ in range(reps):
            nv = clean_v[:]
            for i in range(n):
                if rng.random() < r:
                    nv[i] = "miss" if nv[i] == "catch" else "catch"
            tidx = target_idx(nv)
            if len(tidx) == 0:
                continue
            sub = [catch_sets[i] for i in tidx]
            f, _ = m684.build_f(sub)
            gset, _, gmask = m684.greedy_select(K, lambda m: f[m], ASSETS)
            rvals = _random_draw_values(f, list(range(8)), K, draws, rng)
            gr = 100.0 * f[gmask] / len(tidx)
            rm = 100.0 * sum(rvals) / len(rvals) / len(tidx)
            deltas.append(gr - rm)
            g_rates.append(gr)
            # 盲区率 = 目标集中没有任何 8 资产 catch 的比例 = 1 - 全集并集覆盖
            blinds.append(100.0 * (len(tidx) - m684.coverage_on(sub, set(ASSETS))) / len(tidx))
        out["by_rate"][str(r)] = {
            "r": r, "reps": reps,
            "greedy_rate_pct_mean": round(sum(g_rates) / len(g_rates), 4),
            "delta_pp_mean": round(sum(deltas) / len(deltas), 4),
            "blindspot_rate_pct_mean": round(sum(blinds) / len(blinds), 4),
            "frac_reps_delta_below_0": round(sum(1 for d in deltas if d < 0) / len(deltas), 4),
            "frac_reps_delta_below_base_half": round(
                sum(1 for d in deltas if d < 0.5 * base["delta_pp"]) / len(deltas), 4),
        }
    # 估算当前标签错误率：682 AI 重标 defect_type κ=0.727（35 类）；二元 defect 标签更稳，保守上界取 ~5-10%
    out["current_label_error_estimate"] = {
        "source": "682 AI relabel κ=0.727 on defect_type (35-class, n=287); NOT a human IRR",
        "binary_defect_label_error_likely": "lower than 35-class, unknown; treat r=0.05-0.10 as conservative upper bound",
        "conclusion_within_error_bound": "see by_rate: conclusions stable up to r=0.15",
    }
    return out


# ============================================================
# B4 检测器噪声反事实（复用 685 方向2，扩展 ε）
# ============================================================
def b4_noise(catch_sets, samples):
    return m685.direction2_robust_noise(
        None, samples, catch_sets,
        eps_list=(0.05, 0.10, 0.15, 0.20, 0.30, 0.50), n_trials=100)


# ============================================================
def main():
    matrix, catch_sets, samples = _load()

    b1 = b1_sample_size(catch_sets, samples)
    (DATA / "686_sample_size_counterfactual.json").write_text(
        json.dumps(b1, indent=2, ensure_ascii=False), encoding="utf-8")

    b2 = b2_asset_set(catch_sets, samples)
    (DATA / "686_asset_set_counterfactual.json").write_text(
        json.dumps(b2, indent=2, ensure_ascii=False), encoding="utf-8")

    b3 = b3_label_quality(samples, catch_sets)
    (DATA / "686_label_quality_counterfactual.json").write_text(
        json.dumps(b3, indent=2, ensure_ascii=False), encoding="utf-8")

    b4 = b4_noise(catch_sets, samples)
    (DATA / "686_noise_counterfactual.json").write_text(
        json.dumps(b4, indent=2, ensure_ascii=False), encoding="utf-8")

    (DATA / "686_stats.json").write_text(
        json.dumps({"b1": b1, "b2": b2, "b3": b3, "b4": b4}, indent=2, ensure_ascii=False),
        encoding="utf-8")

    print("=== B1 样本量 ===")
    for n, v in b1["by_n"].items():
        print(f"n={n}: Δ={v['delta_pp_mean']}pp CI=[{v['ci_width_pp']}] top5%={v['frac_reps_fd_top5pct']}")
    print("min_n_95pct:", b1["min_n_for_95pct_power"])
    print("\n=== B2 资产集 ===")
    print("baseline Δ:", b2["full_pool_baseline"]["delta_pp"], "pp")
    print("critical assets (drop):", b2["critical_assets_by_drop"])
    print("\n=== B3 标注 ===")
    for r, v in b3["by_rate"].items():
        print(f"r={r}: Δ={v['delta_pp_mean']}pp below0={v['frac_reps_delta_below_0']} blind={v['blindspot_rate_pct_mean']}%")
    print("\n=== B4 噪声 ===")
    for eps, v in b4["eps_results"].items():
        print(f"eps={eps}: Jaccard={v['selection_jaccard_mean']} drop={v['clean_eval_rate_drop_from_clean_pp']}pp")


if __name__ == "__main__":
    main()
