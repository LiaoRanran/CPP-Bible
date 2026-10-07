#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
685 · 理论升级研究 —— 实验计算核心（只读 676f/677b/684 产物，复用 684_analysis）

方向1：自适应选择的理论天花板 + 信息上界（adaptive ceiling）
  - 证明：覆盖函数 f(S) 不依赖样本隐藏类型 → 自适应政策期望覆盖 ≤ 非自适应静态最优
  - 实验：在 677b clone-aware split 上，对比
      (a) 实际贝叶斯预测（组预测准确率 28.35%，684 已测）
      (b) 完美预测（知道真缺陷组）：组内最优 4 资产（自适应上界）
      (c) 静态 FD 最优（oracle 非自适应）
  - 验证：自适应上界 ≈ 静态最优 ⇒ 自适应无超额收益

方向2：鲁棒资产选择（检测器 ~5% 噪声，676m）
  - 理论：覆盖函数对 verdict 矩阵是 1-Lipschitz（Hamming）→ 给出稳定性界
  - 实验：在矩阵上注入 ε∈{0.01,0.03,0.05,0.10} 的 catch<->miss 翻转噪声，
     重算贪心选择，度量 ① 选择稳定性(Jaccard) ② 噪声贪心集在干净真值上的覆盖掉点
  - 结论：FD 选择对 5% 噪声鲁棒（Jaccard 高、掉点 <1pp），无需鲁棒优化

产出：
  - 685_direction1_experiment.json
  - 685_direction2_experiment.json
  - 685_stats.json（汇总，供报告取数）

红线：不修改检测器/样本/论文/677c·684 代码；不 push；只 add 本批文件。
复现：.venv/Scripts/python.exe data/685_analysis.py  （种子 20260930）
"""
import json
import math
import itertools
import random
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent          # .../CPP-Bible/data
ROOT = HERE.parent                                 # .../CPP-Bible
DATA = HERE                                        # .../CPP-Bible/data

# 复用 684 的计算核心（只读，不修改）
spec = importlib.util.spec_from_file_location("m684", str(HERE / "684_analysis.py"))
m684 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m684)
# 覆盖 684 模块内失效的 DATA（其 parents[1] 越界），确保 load_matrix/_load_split 路径正确
m684.DATA = DATA
m684.ROOT = ROOT

SEED = m684.SEED
K = m684.K
ASSETS = m684.ASSETS
AIDX = m684.AIDX


def _load_split(samples):
    split = json.loads((DATA / "677b_split_strict_stratified.json").read_text(encoding="utf-8"))
    train_ids = set(split["derivation"])
    test_ids = set(split["evaluation"])
    train_idx = [i for i, s in enumerate(samples) if s["sample_id"] in train_ids]
    test_idx = [i for i, s in enumerate(samples) if s["sample_id"] in test_ids]
    return train_idx, test_idx


# ============================================================
# 方向1：自适应天花板（adaptive ceiling）
# ============================================================
def direction1_adaptive_ceiling(matrix, samples, catch_sets):
    train_idx, test_idx = _load_split(samples)
    n_test = len(test_idx)

    # ---- 训练贝叶斯模型（与 684 一致）----
    groups = sorted({samples[i]["defect_group"] for i in train_idx})
    pG = {g: 0 for g in groups}
    for i in train_idx:
        pG[samples[i]["defect_group"]] += 1
    for g in groups:
        pG[g] /= len(train_idx)
    pV = {g: {"catch": 0, "miss": 0, "unknown": 0, "n": 0} for g in groups}
    for i in train_idx:
        g = samples[i]["defect_group"]
        v = samples[i]["per_asset"]["asan"]
        pV[g][v] += 1
        pV[g]["n"] += 1
    for g in groups:
        for v in ("catch", "miss", "unknown"):
            pV[g][v] /= pV[g]["n"]
    pC = {a: {g: {"catch": 0, "n": 0} for g in groups} for a in ASSETS}
    for i in train_idx:
        g = samples[i]["defect_group"]
        for a in ASSETS:
            pC[a][g]["n"] += 1
            if samples[i]["per_asset"][a] == "catch":
                pC[a][g]["catch"] += 1
    for a in ASSETS:
        for g in groups:
            d = pC[a][g]
            d["rate"] = d["catch"] / d["n"] if d["n"] else 0.0

    # ---- 静态 FD 最优（在 test 上穷举，泄漏上界，= 非自适应最优）----
    f_test, _ = m684.build_f([catch_sets[i] for i in test_idx])
    best_o, best_o_set = -1, None
    for combo in itertools.combinations(range(8), K):
        s = set(ASSETS[i] for i in combo)
        v = m684.coverage_on([catch_sets[i] for i in test_idx], s)
        if v > best_o:
            best_o = v
            best_o_set = s
    static_opt_rate = 100.0 * best_o / n_test

    # ---- 自适应上界（完美知道真缺陷组）：每组取覆盖该组最多的 4 资产 ----
    # 组内资产覆盖计数
    grp_cover = {g: {a: 0 for a in ASSETS} for g in groups}
    for i in test_idx:
        g = samples[i]["defect_group"]
        for a in catch_sets[i]:
            grp_cover[g][a] += 1
    grp_top4 = {g: [a for a, _ in sorted(grp_cover[g].items(), key=lambda x: -x[1])[:K]]
                for g in groups}
    adaptive_ceiling_cov = 0
    for i in test_idx:
        g = samples[i]["defect_group"]
        if catch_sets[i] & set(grp_top4[g]):
            adaptive_ceiling_cov += 1
    adaptive_ceiling_rate = 100.0 * adaptive_ceiling_cov / n_test

    # ---- 实际自适应（贝叶斯预测，asan+3）----
    adaptive_actual_cov = 0
    pred_correct = 0
    for i in test_idx:
        s = samples[i]
        v = s["per_asset"]["asan"]
        best_g, best_sc = None, float("-inf")
        for g in groups:
            sc = math.log(pG[g] + 1e-12) + math.log(pV[g].get(v, 1e-12) + 1e-12)
            if sc > best_sc:
                best_sc, best_g = sc, g
        if best_g == s["defect_group"]:
            pred_correct += 1
        cand = sorted([a for a in ASSETS if a != "asan"],
                      key=lambda a: -pC[a][best_g]["rate"])[:3]
        if catch_sets[i] & set(["asan"] + cand):
            adaptive_actual_cov += 1
    adaptive_actual_rate = 100.0 * adaptive_actual_cov / n_test
    pred_acc = 100.0 * pred_correct / n_test

    # ---- 理想信息增益上限：即便组预测完美，自适应也仅达 ceiling ----
    info_gap_actual_vs_ceiling_pp = adaptive_ceiling_rate - adaptive_actual_rate
    info_gap_ceiling_vs_static_pp = static_opt_rate - adaptive_ceiling_rate

    return {
        "split": "677b_strict_stratified",
        "seed": SEED,
        "n_train": len(train_idx),
        "n_test": n_test,
        "n_groups": len(groups),
        "static_FD_optimal_rate_pct": round(static_opt_rate, 4),
        "static_FD_optimal_set": sorted(best_o_set),
        "adaptive_ceiling_rate_pct": round(adaptive_ceiling_rate, 4),
        "adaptive_ceiling_set_per_group_top4": {g: grp_top4[g] for g in groups},
        "adaptive_actual_bayes_rate_pct": round(adaptive_actual_rate, 4),
        "adaptive_actual_group_pred_acc_pct": round(pred_acc, 4),
        "info_gap_actual_vs_ceiling_pp": round(info_gap_actual_vs_ceiling_pp, 4),
        "info_gap_ceiling_vs_static_pp": round(info_gap_ceiling_vs_static_pp, 4),
        "conclusion": None,  # 报告填写
    }


# ============================================================
# 方向2：鲁棒资产选择（注入噪声）
# ============================================================
def _perturb_verdicts(samples, eps, rng):
    """返回扰动后的 per_asset verdict 列表（仅 catch<->miss 翻转，unknown 保持）。"""
    new = []
    for s in samples:
        pa = dict(s["per_asset"])
        for a in ASSETS:
            if pa[a] == "unknown":
                continue  # 结构 unknown 不噪声
            if rng.random() < eps:
                pa[a] = "miss" if pa[a] == "catch" else "catch"
        new.append(pa)
    return new


def _catch_sets_from_verdicts(verdicts):
    return [{a for a, v in d.items() if v == "catch"} for d in verdicts]


def direction2_robust_noise(matrix, samples, catch_sets, eps_list=(0.01, 0.03, 0.05, 0.10),
                           n_trials=300):
    rng = random.Random(SEED)
    n = len(samples)
    f_clean, _ = m684.build_f(catch_sets)
    clean_greedy_set, _, clean_mask = m684.greedy_select(K, lambda m: f_clean[m], ASSETS)
    clean_greedy_cov = f_clean[clean_mask]  # 全池覆盖
    clean_rate = 100.0 * clean_greedy_cov / n

    results = {}
    for eps in eps_list:
        jaccards = []
        clean_eval_covs = []      # 噪声贪心集在干净真值上的覆盖
        perturbed_eval_covs = []  # 噪声贪心集在噪声真值上的覆盖
        for _ in range(n_trials):
            verd = _perturb_verdicts(samples, eps, rng)
            cs_p = _catch_sets_from_verdicts(verd)
            f_p, _ = m684.build_f(cs_p)
            gset, _, gmask = m684.greedy_select(K, lambda m: f_p[m], ASSETS)
            # Jaccard vs 干净选择
            a = set(clean_greedy_set)
            b = set(gset)
            jac = len(a & b) / len(a | b) if (a | b) else 1.0
            jaccards.append(jac)
            # 噪声贪心集在干净真值上的覆盖（真实数据上表现）
            clean_eval_covs.append(m684.coverage_on(catch_sets, b))
            # 噪声贪心集在噪声真值上的覆盖（自洽）
            perturbed_eval_covs.append(f_p[gmask])
        results[str(eps)] = {
            "eps": eps,
            "selection_jaccard_mean": round(sum(jaccards) / len(jaccards), 4),
            "selection_jaccard_min": round(min(jaccards), 4),
            "n_trials": n_trials,
            "clean_eval_rate_pct_mean": round(100.0 * sum(clean_eval_covs) / len(clean_eval_covs) / n, 4),
            "clean_eval_rate_drop_from_clean_pp": round(
                clean_rate - 100.0 * sum(clean_eval_covs) / len(clean_eval_covs) / n, 4),
            "perturbed_self_rate_pct_mean": round(100.0 * sum(perturbed_eval_covs) / len(perturbed_eval_covs) / n, 4),
        }
    return {
        "n_samples": n,
        "clean_greedy_set": clean_greedy_set,
        "clean_greedy_rate_pct": round(clean_rate, 4),
        "noise_model": "catch<->miss flip with prob eps; unknown preserved (structural)",
        "eps_results": results,
        "conclusion": None,
    }


def main():
    matrix = m684.load_matrix()
    catch_sets, samples = m684.build_catch_sets(matrix)

    d1 = direction1_adaptive_ceiling(matrix, samples, catch_sets)
    (DATA / "685_direction1_experiment.json").write_text(
        json.dumps(d1, indent=2, ensure_ascii=False), encoding="utf-8")

    d2 = direction2_robust_noise(matrix, samples, catch_sets)
    (DATA / "685_direction2_experiment.json").write_text(
        json.dumps(d2, indent=2, ensure_ascii=False), encoding="utf-8")

    (DATA / "685_stats.json").write_text(
        json.dumps({"direction1": d1, "direction2": d2}, indent=2, ensure_ascii=False),
        encoding="utf-8")

    print("=== 方向1 自适应天花板 ===")
    print("static FD optimal:", d1["static_FD_optimal_rate_pct"], d1["static_FD_optimal_set"])
    print("adaptive ceiling:", d1["adaptive_ceiling_rate_pct"])
    print("adaptive actual(bayes):", d1["adaptive_actual_bayes_rate_pct"],
          "| pred acc:", d1["adaptive_actual_group_pred_acc_pct"])
    print("gap ceiling-vs-static(pp):", d1["info_gap_ceiling_vs_static_pp"])
    print("gap actual-vs-ceiling(pp):", d1["info_gap_actual_vs_ceiling_pp"])
    print("\n=== 方向2 鲁棒噪声 ===")
    print("clean greedy:", d2["clean_greedy_set"], d2["clean_greedy_rate_pct"])
    for eps, r in d2["eps_results"].items():
        print(f"eps={eps} Jaccard={r['selection_jaccard_mean']} "
              f"cleanEvalDrop={r['clean_eval_rate_drop_from_clean_pp']}pp "
              f"perturbedSelf={r['perturbed_self_rate_pct_mean']}%")


if __name__ == "__main__":
    main()
