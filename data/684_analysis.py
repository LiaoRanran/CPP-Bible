#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
684 · 算法增强研究 —— 实验计算核心脚本（只读既有产物，不修改检测器/样本/论文）

产出（均为 data/684_*.json，便于验收自证）：
  - 684_submodularity_test.json   (A2 子模性全枚举 + 曲率 + 近似比)
  - 684_information_analysis.json (B1 信息论：熵/互信息/条件熵)
  - 684_complementarity_matrix.json (B2 8x8 互补性矩阵)
  - 684_adaptive_experiment.json  (B3 五策略对比，clone-aware split，无泄漏)
  - 684_stats.json                (内部汇总，供 markdown 报告取数)

红线遵守：
  - 不 import / 不修改 tools/holdout_reveal_661.py
  - 不修改 data/holdout_expansion/**/*.cpp
  - 不修改 677c 的 evolution_operator_677c.py
  - 不修改论文核心数字（A5 Δ=+24.03pp、盲区38.4% 等） —— 本脚本只读引用
  - 不 push；不 git add 其他批次文件

复现：.venv/Scripts/python.exe data/684_analysis.py
随机种子：20260930（与 676f/677c 口径一致，可复现）
"""
import json
import math
import itertools
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

SEED = 20260930
K = 4  # 主预算

# ---- 资产顺序（与 676f 矩阵一致；a1..a8）----
ASSETS = ["asan", "compile-time", "compiler-warn", "cross-compile",
          "linker", "tsan", "ubsan", "wunsequenced"]
AIDX = {a: i for i, a in enumerate(ASSETS)}


def load_matrix():
    m = json.loads((DATA / "a5_676f_detection_matrix.json").read_text(encoding="utf-8"))
    return m


def build_catch_sets(matrix):
    """返回 list[set]: 每个样本的 catch 资产集合（只含 verdict=='catch'）。"""
    samples = matrix["samples"]
    catch = []
    for s in samples:
        cs = {a for a, v in s["per_asset"].items() if v == "catch"}
        catch.append(cs)
    return catch, samples


def build_f(catch_sets):
    """预计算所有 2^8=256 子集的覆盖计数 f[mask]（OR 覆盖：至少一资产 catch 即计入）。

    正确口径：f[mask] = |{s : catch_set(s) ∩ mask ≠ ∅}|。
    注意与“子集枚举”的区别——覆盖是资产集合的*并集*，不是样本的 catch 集合的超集。
    """
    n = len(catch_sets)
    sample_masks = [0] * n
    for i, cs in enumerate(catch_sets):
        m = 0
        for a in cs:
            m |= (1 << AIDX[a])
        sample_masks[i] = m
    f = [0] * 256
    for mask in range(1, 256):
        cnt = 0
        for sm in sample_masks:
            if sm & mask:
                cnt += 1
        f[mask] = cnt
    f[0] = 0
    return f, n


def greedy_select(k, f_func, asset_pool):
    """标准集合覆盖贪心：每步选边际收益最大的资产。返回 (资产列表, 逐步边际)。"""
    chosen = []
    covered_mask_tracker = set()  # 不直接用，改用逐步重算
    # 用逐步覆盖计数实现（对 train/test 子集通用，通过 f_func 提供 f）
    remaining = set(asset_pool)
    chosen_mask = 0
    margins = []
    for _ in range(k):
        if not remaining:
            break
        best_a, best_marg = None, -1
        base = f_func(chosen_mask)
        for a in remaining:
            cand = chosen_mask | (1 << AIDX[a])
            marg = f_func(cand) - base
            if marg > best_marg:
                best_marg = marg
                best_a = a
        chosen.append(best_a)
        chosen_mask |= (1 << AIDX[best_a])
        remaining.discard(best_a)
        margins.append(best_marg)
    return chosen, margins, chosen_mask


def coverage_on(catch_sets, asset_set):
    """给定样本列表（索引）与资产集合，返回被覆盖（至少一资产 catch）的样本数。"""
    amask = 0
    for a in asset_set:
        amask |= (1 << AIDX[a])
    cnt = 0
    for cs in catch_sets:
        if cs & asset_set:
            cnt += 1
    return cnt


# ============================ A2 子模性检验 ============================
def submodularity_test(f, n):
    """全枚举 A⊆B⊆ASSETS, a∉B，检验 f(A∪{a})-f(A) ≥ f(B∪{a})-f(B)。"""
    violations = []
    total = 0
    for B in range(256):
        # 枚举 B 的所有子集 A
        # 枚举 B 的位
        b_bits = [i for i in range(8) if (B >> i) & 1]
        # 遍历 A ⊆ B
        # 用 B 的所有子集
        sub = B
        while True:
            A = sub
            # 枚举 a ∉ B
            for a in range(8):
                if (B >> a) & 1:
                    continue
                total += 1
                a_bit = 1 << a
                lhs = f[A | a_bit] - f[A]
                rhs = f[B | a_bit] - f[B]
                if lhs + 1e-9 < rhs:
                    violations.append({
                        "A": A, "B": B, "a": a,
                        "lhs": lhs, "rhs": rhs, "diff": rhs - lhs
                    })
            if sub == 0:
                break
            sub = (sub - 1) & B
    # 曲率（标准 Conforti-Cornuejols）：κ = 1 - min_{a,S:a∉S, Δ_a(∅)>0} Δ_a(S)/Δ_a(∅)
    curv_min = 1.0
    per_asset_delta0 = {}
    for a in range(8):
        per_asset_delta0[a] = f[1 << a]  # Δ_a(∅) = f({a})
    for S in range(256):
        for a in range(8):
            if (S >> a) & 1:
                continue
            d0 = per_asset_delta0[a]
            if d0 <= 0:
                continue
            marg = f[S | (1 << a)] - f[S]
            ratio = marg / d0
            if ratio < curv_min:
                curv_min = ratio
    kappa_std = 1.0 - curv_min
    # 任务所给公式（用于对照，标注其口径）：A=全集
    full = 255
    per_a_task = {}
    for a in range(8):
        fa = f[full]
        fam = f[full ^ (1 << a)]
        marg = fa - fam
        if marg > 0:
            per_a_task[ASSETS[a]] = 1.0 - fam / marg
        else:
            per_a_task[ASSETS[a]] = None  # 边际为 0，公式无定义
    # 近似比：贪心 vs 最优（k=4，全集 8 资产）
    f_full = lambda m: f[m]
    greedy_set, _, greedy_mask = greedy_select(K, f_full, ASSETS)
    greedy_val = f[greedy_mask]
    best_val = -1
    best_set = None
    for combo in itertools.combinations(range(8), K):
        mask = 0
        for i in combo:
            mask |= (1 << i)
        v = f[mask]
        if v > best_val:
            best_val = v
            best_set = combo
    optimal_val = best_val
    optimal_assets = [ASSETS[i] for i in best_set]
    approx_ratio = greedy_val / optimal_val if optimal_val > 0 else None
    return {
        "n_samples": n,
        "n_subsets_enumerated": 256,
        "total_triples": total,
        "violations_count": len(violations),
        "violations_pct": 100.0 * len(violations) / total if total else 0,
        "submodular": len(violations) == 0,
        "sample_violations": violations[:50],
        "curvature_standard_kappa": round(kappa_std, 6),
        "curvature_task_formula_per_asset": per_a_task,
        "greedy_set": greedy_set,
        "greedy_value": greedy_val,
        "greedy_rate_pct": round(100.0 * greedy_val / n, 4),
        "optimal_set": optimal_assets,
        "optimal_value": optimal_val,
        "optimal_rate_pct": round(100.0 * optimal_val / n, 4),
        "greedy_over_optimal_ratio": round(approx_ratio, 6) if approx_ratio else None,
        "guarantee_1_minus_1e": round(1 - 1 / math.e, 6),
    }


# ============================ A4 退化资产 ============================
def degenerate_analysis(f, n, catch_per_asset):
    degen = {"compile-time": 0, "wunsequenced": 0}  # 恒 unknown
    low = {"linker": catch_per_asset["linker"]}      # 低产
    # 各池
    poolA = ["asan", "compiler-warn", "cross-compile", "tsan", "ubsan"]  # 5 非退化
    poolBC = ["asan", "compiler-warn", "cross-compile", "linker", "tsan", "ubsan"]  # 6 含 linker
    full8 = ASSETS
    rng = random.Random(SEED)

    def random_mean(pool, k, trials=2000):
        vals = []
        idx = [AIDX[a] for a in pool]
        for _ in range(trials):
            combo = rng.sample(idx, k)
            mask = 0
            for i in combo:
                mask |= (1 << i)
            vals.append(f[mask])
        return sum(vals) / len(vals)

    def greedy_on_pool(pool, k):
        _, _, mask = greedy_select(k, lambda m: f[m], pool)
        return f[mask], [ASSETS[i] for i in range(8) if (mask >> i) & 1]

    res = {}
    for name, pool in [("full8", full8), ("poolA_5nondeg", poolA), ("poolBC_6incllinker", poolBC)]:
        gv, gs = greedy_on_pool(pool, K)
        rm = random_mean(pool, K)
        res[name] = {
            "pool": pool,
            "greedy_set": gs,
            "greedy_value": gv,
            "greedy_rate_pct": round(100.0 * gv / n, 4),
            "random_mean_value": round(rm, 4),
            "random_mean_rate_pct": round(100.0 * rm / n, 4),
            "greedy_minus_random_mean_pp": round(100.0 * (gv - rm) / n, 4),
            "n_candidates": len(pool),
            "n_degenerate_in_pool": sum(1 for a in pool if a in degen or a in low),
        }
    # 公式验证：E[浪费槽位] = k*d/n；以 poolBC (d=1 linker, n=6, k=4) 为例
    # 经验随机均值 vs 贪心；报告浪费槽位期望
    return res


# ============================ B1 信息论 ============================
def entropy(probs):
    s = 0.0
    for p in probs:
        if p > 0:
            s -= p * math.log2(p)
    return s


def information_analysis(matrix, samples, catch_sets):
    n = len(samples)
    # 每资产 verdict 分布
    verdict_counts = {a: {"catch": 0, "miss": 0, "unknown": 0} for a in ASSETS}
    for s in samples:
        for a in ASSETS:
            verdict_counts[a][s["per_asset"][a]] += 1
    # 缺陷组
    groups = {}
    for s in samples:
        groups.setdefault(s["defect_group"], 0)
        groups[s["defect_group"]] += 1
    grp_list = sorted(groups.keys())
    # H(G)
    pG = [groups[g] / n for g in grp_list]
    H_G = entropy(pG)
    info = {"n_samples": n, "n_groups": len(grp_list), "H_defect_group_bits": round(H_G, 6),
            "groups": groups, "assets": {}}
    # 每资产
    for a in ASSETS:
        c = verdict_counts[a]
        pc, pm, pu = c["catch"] / n, c["miss"] / n, c["unknown"] / n
        H_binary = entropy([pc, pm])  # 任务公式（catch,miss）
        H_ternary = entropy([pc, pm, pu])
        # 互信息 I(a; G) —— 用 verdict∈{catch,miss,unknown} 与 G 的联合
        # 联合计数
        joint = {(v, g): 0 for v in ("catch", "miss", "unknown") for g in grp_list}
        for s in samples:
            v = s["per_asset"][a]
            joint[(v, s["defect_group"])] += 1
        # H(G|a) = Σ_v P(v) H(G|v)
        HG_given_a = 0.0
        for v in ("catch", "miss", "unknown"):
            nv = sum(joint[(v, g)] for g in grp_list)
            if nv == 0:
                continue
            pvs = [joint[(v, g)] / nv for g in grp_list]
            HG_given_a += (nv / n) * entropy(pvs)
        I_a_G = H_G - HG_given_a
        # H(a|G) = H(a) - I
        H_a = H_ternary
        H_a_given_G = H_a - I_a_G
        info["assets"][a] = {
            "p_catch": round(pc, 6), "p_miss": round(pm, 6), "p_unknown": round(pu, 6),
            "H_binary_catch_miss_bits": round(H_binary, 6),
            "H_ternary_bits": round(H_ternary, 6),
            "I_a_defect_group_bits": round(I_a_G, 6),
            "H_a_given_G_bits": round(H_a_given_G, 6),
            "H_defect_group_given_a_bits": round(HG_given_a, 6),
        }
    return info


# ============================ B2 互补性 ============================
def complementarity_matrix(f):
    n = sum(1 for _ in range(256))  # placeholder
    # 直接由 f 计算
    total_n = f[255]  # 全集覆盖（catch）
    M = {}
    for ai in ASSETS:
        M[ai] = {}
        for aj in ASSETS:
            mask_i = 1 << AIDX[ai]
            mask_j = 1 << AIDX[aj]
            fi = f[mask_i]
            fj = f[mask_j]
            fij = f[mask_i | mask_j]
            comp = fij - fi - fj  # f(∅)=0
            M[ai][aj] = {
                "f_i": fi, "f_j": fj, "f_ij": fij,
                "complementarity": comp,
                "classification": ("self" if ai == aj else
                                   ("complementary" if comp > 0 else
                                    ("redundant" if comp < 0 else "neutral")))
            }
    return M, total_n


# ============================ B3 自适应实验 ============================
def adaptive_experiment(matrix, samples, catch_sets):
    # 加载 677b clone-aware strict_stratified split
    split = json.loads((DATA / "677b_split_strict_stratified.json").read_text(encoding="utf-8"))
    train_ids = set(split["derivation"])
    test_ids = set(split["evaluation"])
    # 索引样本
    by_id = {s["sample_id"]: s for s in samples}
    train_idx = [i for i, s in enumerate(samples) if s["sample_id"] in train_ids]
    test_idx = [i for i, s in enumerate(samples) if s["sample_id"] in test_ids]
    n_train, n_test = len(train_idx), len(test_idx)

    # 训练：先验 + P(asan verdict | group) + P(catch | asset, group)
    groups = sorted({samples[i]["defect_group"] for i in train_idx})
    pG = {g: 0 for g in groups}
    for i in train_idx:
        pG[samples[i]["defect_group"]] += 1
    for g in groups:
        pG[g] /= n_train
    # P(v_asan | g)
    pV_given_g = {}
    for g in groups:
        pV_given_g[g] = {"catch": 0, "miss": 0, "unknown": 0, "n": 0}
    for i in train_idx:
        g = samples[i]["defect_group"]
        v = samples[i]["per_asset"]["asan"]
        pV_given_g[g][v] += 1
        pV_given_g[g]["n"] += 1
    for g in groups:
        for v in ("catch", "miss", "unknown"):
            pV_given_g[g][v] /= pV_given_g[g]["n"]
    # P(catch | asset, g)
    pCatch_a_g = {}
    for a in ASSETS:
        pCatch_a_g[a] = {}
        for g in groups:
            pCatch_a_g[a][g] = {"catch": 0, "n": 0}
    for i in train_idx:
        g = samples[i]["defect_group"]
        for a in ASSETS:
            pCatch_a_g[a][g]["n"] += 1
            if samples[i]["per_asset"][a] == "catch":
                pCatch_a_g[a][g]["catch"] += 1
    for a in ASSETS:
        for g in groups:
            d = pCatch_a_g[a][g]
            d["rate"] = d["catch"] / d["n"] if d["n"] else 0.0

    # ---- 策略定义 ----
    # FD 贪心：在 train 上选 k=4（复制 676f 选择流程，评估在 test）
    f_train = build_f([catch_sets[i] for i in train_idx])[0]
    fd_set, _, _ = greedy_select(K, lambda m: f_train[m], ASSETS)
    # FD_frequency：论文实际方法——按派生集 catch 计数降序 top-k（676f fail_hits 键）
    freq_rank = sorted(ASSETS, key=lambda a: -sum(
        1 for i in train_idx if samples[i]["per_asset"][a] == "catch"))
    fd_freq_set = freq_rank[:K]
    # Static：固定静态资产字典序 top-k（677c 定义：只能选静态资产）
    static_pool = ["compiler-warn", "cross-compile", "linker", "compile-time"]
    static_set = static_pool[:K]
    # Random：seed 固定单次抽样 + 2000 次均值
    rng = random.Random(SEED)
    rand_single = rng.sample(ASSETS, K)
    rand_vals = []
    for _ in range(2000):
        combo = rng.sample(ASSETS, K)
        rand_vals.append(coverage_on([catch_sets[i] for i in test_idx], set(combo)))
    rand_mean = sum(rand_vals) / len(rand_vals)
    # Oracle：在 test 上穷举最优（泄漏上界）
    best_o, best_o_set = -1, None
    for combo in itertools.combinations(range(8), K):
        s = set(ASSETS[i] for i in combo)
        v = coverage_on([catch_sets[i] for i in test_idx], s)
        if v > best_o:
            best_o = v
            best_o_set = s
    # Adaptive：1+3
    test_samples = [samples[i] for i in test_idx]
    test_catch = [catch_sets[i] for i in test_idx]
    adaptive_covered = 0
    pred_correct = 0
    # 记录每个 test 样本的（预测组, 实际组）用于诊断
    for s, cs in zip(test_samples, test_catch):
        v = s["per_asset"]["asan"]
        # 贝叶斯预测组
        best_g, best_score = None, float('-inf')
        for g in groups:
            score = math.log(pG[g] + 1e-12) + math.log(pV_given_g[g].get(v, 1e-12) + 1e-12)
            if score > best_score:
                best_score = score
                best_g = g
        if best_g == s["defect_group"]:
            pred_correct += 1
        # 选 3 个最高 P(catch|a, g_hat) 且 != asan
        cand = [(a, pCatch_a_g[a][best_g]["rate"]) for a in ASSETS if a != "asan"]
        cand.sort(key=lambda x: -x[1])
        chosen3 = [a for a, _ in cand[:3]]
        used = set(["asan"] + chosen3)
        if cs & used:
            adaptive_covered += 1
    adaptive_rate = 100.0 * adaptive_covered / n_test

    def rate_on(idx, asset_set):
        return 100.0 * coverage_on([catch_sets[i] for i in idx], asset_set) / len(idx)

    out = {
        "split": "677b_strict_stratified",
        "seed": SEED,
        "n_train": n_train, "n_test": n_test,
        "strategies": {
            "Static": {
                "assets": static_set,
                "train_selected_on": "fixed",
                "test_rate_pct": round(rate_on(test_idx, set(static_set)), 4),
            },
            "FD_greedy": {
                "assets": fd_set,
                "train_selected_on": "derivation(train)",
                "test_rate_pct": round(rate_on(test_idx, set(fd_set)), 4),
            },
            "FD_frequency": {
                "assets": fd_freq_set,
                "train_selected_on": "derivation(train) catch-count top-k (676f method)",
                "test_rate_pct": round(rate_on(test_idx, set(fd_freq_set)), 4),
            },
            "Random_single": {
                "assets": rand_single,
                "train_selected_on": "seed=%d" % SEED,
                "test_rate_pct": round(rate_on(test_idx, set(rand_single)), 4),
            },
            "Random_mean2000": {
                "assets": "mean over 2000 draws",
                "train_selected_on": "seed=%d" % SEED,
                "test_rate_pct": round(100.0 * rand_mean / n_test, 4),
            },
            "Oracle": {
                "assets": sorted(best_o_set),
                "train_selected_on": "evaluation(test) [leaky upper bound]",
                "test_rate_pct": round(100.0 * best_o / n_test, 4),
            },
            "Adaptive_1p3": {
                "assets": "asan + 3 (bayes-predicted group)",
                "train_selected_on": "derivation(train) for bayes model",
                "test_rate_pct": round(adaptive_rate, 4),
                "group_prediction_accuracy_pct": round(100.0 * pred_correct / n_test, 4),
            },
        },
        "conclusion": None,  # 由报告填写
    }
    return out


def main():
    matrix = load_matrix()
    catch_sets, samples = build_catch_sets(matrix)
    n = len(samples)
    f, _ = build_f(catch_sets)
    catch_per_asset = {a: sum(1 for cs in catch_sets if a in cs) for a in ASSETS}

    # A2
    sub = submodularity_test(f, n)
    (DATA / "684_submodularity_test.json").write_text(
        json.dumps(sub, indent=2, ensure_ascii=False), encoding="utf-8")

    # A4
    degen = degenerate_analysis(f, n, catch_per_asset)
    (DATA / "684_degenerate_tmp.json").write_text(
        json.dumps(degen, indent=2, ensure_ascii=False), encoding="utf-8")

    # B1
    info = information_analysis(matrix, samples, catch_sets)
    (DATA / "684_information_analysis.json").write_text(
        json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")

    # B2
    comp, total_n = complementarity_matrix(f)
    comp_out = {"n_samples": total_n, "assets": ASSETS, "matrix": comp}
    (DATA / "684_complementarity_matrix.json").write_text(
        json.dumps(comp_out, indent=2, ensure_ascii=False), encoding="utf-8")

    # B3
    adp = adaptive_experiment(matrix, samples, catch_sets)
    (DATA / "684_adaptive_experiment.json").write_text(
        json.dumps(adp, indent=2, ensure_ascii=False), encoding="utf-8")

    # 汇总
    stats = {
        "n_samples": n,
        "assets": ASSETS,
        "catch_per_asset": catch_per_asset,
        "A2_submodularity": {k: sub[k] for k in
            ("submodular", "violations_count", "total_triples", "violations_pct",
             "curvature_standard_kappa", "greedy_set", "greedy_rate_pct",
             "optimal_set", "optimal_rate_pct", "greedy_over_optimal_ratio",
             "guarantee_1_minus_1e")},
        "A4_degenerate": degen,
        "B3_adaptive": {k: adp[k] for k in ("n_train", "n_test", "strategies")},
    }
    (DATA / "684_stats.json").write_text(
        json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")

    # 控制台摘要
    print("=== A2 子模性 ===")
    print("submodular:", sub["submodular"], "| violations:", sub["violations_count"],
          "/", sub["total_triples"])
    print("curvature(standard κ):", sub["curvature_standard_kappa"])
    print("greedy:", sub["greedy_set"], sub["greedy_rate_pct"], "%")
    print("optimal:", sub["optimal_set"], sub["optimal_rate_pct"], "%")
    print("greedy/optimal:", sub["greedy_over_optimal_ratio"])
    print("\n=== A4 退化资产（各池 贪心 vs 随机均值）===")
    for k, v in degen.items():
        print(k, "greedy", v["greedy_rate_pct"], "randMean", v["random_mean_rate_pct"],
              "Δpp", v["greedy_minus_random_mean_pp"])
    print("\n=== B3 自适应（test 集覆盖率）===")
    for name, v in adp["strategies"].items():
        print(name, v["test_rate_pct"], "%")


if __name__ == "__main__":
    main()
