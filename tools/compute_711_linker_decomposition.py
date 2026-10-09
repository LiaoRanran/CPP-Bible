#!/usr/bin/env python3
"""711-S1/S3: read-only decomposition of the F1 linker component.

S3 (this script): decompose the "remove linker" contribution of the F1
sequential decomposition (710-C2: pool-6 -> Pool-A at k=4, -4.6525pp) into
(a) a slot/pool-size structural effect and (b) linker's own coverage effect,
then quantify: cross-environment alignment (permutation null), environment-pure
sub-pool analogues, and sample-difficulty reweighting sensitivity.

Red lines: detect_calls = 0; reads only the frozen A5 matrix; writes one JSON.

Usage:
    python tools/compute_711_linker_decomposition.py
"""

from __future__ import annotations

import itertools
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "a5_676f_detection_matrix.json"
OUT = ROOT / "data" / "711_linker_decomposition.json"

ZERO_YIELD = ("wunsequenced", "compile-time")
WSL_TRIAD = ("asan", "ubsan", "tsan")
NATIVE_TRIAD = ("compiler-warn", "cross-compile", "linker")
POOL6 = ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker")
POOLA = ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile")


def or_covered(sample_verdicts: dict[str, str], assets: tuple[str, ...] | list[str]) -> bool:
    return any(sample_verdicts.get(a) == "catch" for a in assets)


def coverage(rows, assets) -> int:
    return sum(1 for r in rows if or_covered(r["per_asset"], assets))


def mean_coverage_enum(rows, assets, k: int) -> float:
    """Exact expectation over all C(|assets|,k) subsets (uniform random arm)."""
    n = len(rows)
    total = 0
    cnt = 0
    for sub in itertools.combinations(assets, k):
        total += coverage(rows, sub)
        cnt += 1
    return 100.0 * total / (cnt * n)


def fd_arm(rows, assets, k: int) -> tuple[list[str], float]:
    """FD arm as used by 677c / 710-C1: pick the top-k assets by marginal
    (per-asset catch count) -- the rule whose k=1 value equals mu_max."""
    marg = sorted(assets, key=lambda a: -coverage(rows, [a]))
    chosen = marg[:k]
    return chosen, 100.0 * coverage(rows, chosen) / len(rows)


def load_rows() -> tuple[list[dict], list[dict]]:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    all_rows = data["samples"]
    eval_rows = [r for r in all_rows if r.get("split") == "evaluation"]
    return all_rows, eval_rows


def main() -> dict:
    all_rows, eval_rows = load_rows()
    n = len(eval_rows)
    per_asset = {a: sum(1 for r in eval_rows if r["per_asset"].get(a) == "catch") for a in POOL6}

    # ---------- 0. anchor checks vs 710-C1 / 692 ----------
    or_full8 = 100.0 * coverage(eval_rows, tuple(eval_rows[0]["per_asset"].keys())) / n
    anchors = {
        "n_evaluation": n,
        "or_full_pool_catch_pct": round(or_full8, 4),
        "per_asset_catch": per_asset,
    }
    assert n == 566, n
    assert abs(or_full8 - 60.071) < 0.01, or_full8

    # ---------- 1. random-arm exact expectations + FD arm ----------
    arms = {}
    for name, pool, ks in (
        ("full8", tuple(POOL6) + ZERO_YIELD, (1, 2, 3, 4, 5, 6, 7, 8)),
        ("pool6", POOL6, (1, 2, 3, 4)),
        ("poolA", POOLA, (1, 2, 3, 4)),
    ):
        arms[name] = {}
        for k in ks:
            mean = mean_coverage_enum(eval_rows, pool, k)
            fd_sel, fd = fd_arm(eval_rows, pool, k)
            arms[name][k] = {
                "random_mean_pct": round(mean, 4),
                "fd_selected": fd_sel,
                "fd_pct": round(fd, 4),
                "delta_mean_pp": round(fd - mean, 4),
            }

    # anchor checks against 710-C1 (exact enumeration table)
    assert abs(arms["poolA"][1]["random_mean_pct"] - 20.742) < 0.01
    assert abs(arms["poolA"][3]["random_mean_pct"] - 45.353) < 0.01
    assert abs(arms["poolA"][4]["random_mean_pct"] - 53.039) < 0.01
    assert abs(arms["full8"][1]["random_mean_pct"] - 13.052) < 0.01
    assert abs(arms["full8"][4]["random_mean_pct"] - 40.1136) < 0.01
    assert abs(arms["pool6"][4]["random_mean_pct"] - 48.386) < 0.01
    assert abs(arms["pool6"][4]["delta_mean_pp"] - 6.2073) < 0.01
    assert abs(arms["poolA"][4]["delta_mean_pp"] - 1.5548) < 0.01
    assert abs(arms["full8"][4]["delta_mean_pp"] - 14.4801) < 0.01
    assert abs(arms["poolA"][4]["fd_pct"] - 54.5936) < 0.01

    # ---------- 2. exact slot/link contribution split (k=4) ----------
    n4 = mean_coverage_enum(eval_rows, POOLA, 4)  # m4 = mean over 4-subsets of the 5
    n3 = mean_coverage_enum(eval_rows, POOLA, 3)  # m3 = mean over 3-subsets of the 5
    n6_full = mean_coverage_enum(eval_rows, POOL6, 4)
    n6 = arms["pool6"][4]["random_mean_pct"]

    # linker-plus-3 subsets: mean coverage of {linker} u T, T a 3-subset of the 5
    tot = 0
    cnt = 0
    for sub in itertools.combinations(POOLA, 3):
        tot += coverage(eval_rows, list(sub) + ["linker"])
        cnt += 1
    m_lin3 = 100.0 * tot / (cnt * n)

    slot_effect = (10.0 / 15.0) * (n4 - n3)  # pure pool-size effect (zero-yield 6th asset)
    link_effect = (10.0 / 15.0) * (m_lin3 - n3)  # linker's net coverage vs a zero-yield slot
    baseline_shift = n4 - n6_full  # = slot_effect - link_effect
    assert abs(slot_effect - link_effect - baseline_shift) < 1e-6
    assert abs(n6_full - n6) < 0.01

    # zero-yield counterfactual using the *real* zero-yield columns
    zreal = {}
    for zname in ZERO_YIELD:
        pool_z = list(POOLA) + [zname]
        mz = mean_coverage_enum(eval_rows, tuple(pool_z), 4)
        zreal[zname] = round(mz, 4)
        assert abs(mz - (5 * n4 + 10 * n3) / 15) < 0.01, (zname, mz)

    # per-sample stratum contributions (d = number of poolA assets catching x)
    # psi(d) = P(x covered by a uniform 4-subset of the 5)   [complement: d=0 -> 1, d=1 -> 1/5]
    # phi(d) = P(x covered by a uniform 3-subset of the 5)   [complement: C(5-d,2)/C(5,2) for d<=2]
    def psi(d: int) -> float:
        if d == 0:
            return 0.0
        if d == 1:
            return 4.0 / 5.0
        return 1.0

    def phi(d: int) -> float:
        """P(x covered by a uniform 3-subset of the 5)."""
        return 1.0 - link_uncovered(d)

    def link_uncovered(d: int) -> float:
        """P(x uncovered by a uniform 3-subset of the 5) = C(5-d, 2-d)/C(5,2)."""
        if d > 2:
            return 0.0
        from math import comb

        return comb(5 - d, 2 - d) / 10.0

    strat = {d: {"n": 0, "slot_contrib_pp": 0.0, "link_contrib_pp": 0.0} for d in range(6)}
    linker_catches_by_d: dict[int, int] = {d: 0 for d in range(6)}
    for r in eval_rows:
        v = r["per_asset"]
        d = sum(1 for a in POOLA if v.get(a) == "catch")
        strat[d]["n"] += 1
        strat[d]["slot_contrib_pp"] += 100.0 / 566.0 * (2.0 / 3.0) * (psi(d) - phi(d))
        if v.get("linker") == "catch":
            linker_catches_by_d[d] += 1
            if d <= 2:
                strat[d]["link_contrib_pp"] += 100.0 / 566.0 * (2.0 / 3.0) * link_uncovered(d)
    for d in range(6):
        strat[d]["slot_contrib_pp"] = round(strat[d]["slot_contrib_pp"], 4)
        strat[d]["link_contrib_pp"] = round(strat[d]["link_contrib_pp"], 4)
    sum_slot = sum(strat[d]["slot_contrib_pp"] for d in range(6))
    sum_link = sum(strat[d]["link_contrib_pp"] for d in range(6))
    assert abs(sum_slot - slot_effect) < 0.01, (sum_slot, slot_effect)
    assert abs(sum_link - link_effect) < 0.01, (sum_link, link_effect)

    # ---------- 3. difficulty reweighting sensitivity ----------
    all_groups = {}
    for r in all_rows:
        all_groups.setdefault(r.get("defect_group") or "NA", 0)
        all_groups[r.get("defect_group") or "NA"] += 1
    corpus_share = {g: c / len(all_rows) for g, c in all_groups.items()}

    eval_groups = {}
    for r in eval_rows:
        eval_groups.setdefault(r.get("defect_group") or "NA", 0)
        eval_groups[r.get("defect_group") or "NA"] += 1

    def weights(kind: str) -> list[float]:
        if kind == "eval":
            return [1.0 / 566.0] * 566
        if kind == "corpus":
            return [
                corpus_share.get(r.get("defect_group") or "NA", 0.0) / eval_groups.get(r.get("defect_group") or "NA", 1)
                for r in eval_rows
            ]
        if kind == "uniform_d":
            cnt = {
                d: sum(1 for r in eval_rows if sum(1 for a in POOLA if r["per_asset"].get(a) == "catch") == d)
                for d in range(6)
            }
            return [1.0 / cnt[sum(1 for a in POOLA if r["per_asset"].get(a) == "catch")] / 6.0 for r in eval_rows]
        raise ValueError(kind)

    reweight = {}
    for kind in ("eval", "corpus", "uniform_d"):
        w = weights(kind)
        s = sum(w) * 100.0
        slot_w = 0.0
        link_w = 0.0
        for r, wi in zip(eval_rows, w):
            v = r["per_asset"]
            d = sum(1 for a in POOLA if v.get(a) == "catch")
            slot_w += wi * 100.0 * (2.0 / 3.0) * (psi(d) - phi(d))
            if v.get("linker") == "catch" and d <= 2:
                link_w += wi * 100.0 * (2.0 / 3.0) * link_uncovered(d)
        reweight[kind] = {
            "weight_sum": round(s, 4),
            "slot_effect_pp": round(slot_w, 4),
            "link_effect_pp": round(link_w, 4),
            "component_pp": round(slot_w - link_w, 4),
        }

    # ---------- 4. environment: pure sub-pool analogues + alignment null ----------
    def triad_component(triad: tuple[str, str, str], removed: str, k: int = 1) -> float:
        keep = [a for a in triad if a != removed]
        return mean_coverage_enum(eval_rows, keep, k) - mean_coverage_enum(eval_rows, triad, k)

    env_pure = {
        "wsl_triad_remove_tsan_k1_pp": round(triad_component(WSL_TRIAD, "tsan"), 4),
        "wsl_triad_remove_asan_k1_pp": round(triad_component(WSL_TRIAD, "asan"), 4),
        "native_triad_remove_linker_k1_pp": round(triad_component(NATIVE_TRIAD, "linker"), 4),
        "native_triad_remove_cw_k1_pp": round(triad_component(NATIVE_TRIAD, "compiler-warn"), 4),
        "mixed_pool6_remove_linker_k4_pp": round(n4 - n6, 4),
    }

    # cross-environment alignment null: permute native-side pair (cw,cc) as a block
    # and, separately, the WSL-side triple, keeping each block's joint rows intact.
    rng = random.Random(711)
    idx = list(range(566))

    def permuted_slot(block: tuple[str, ...], reps: int = 400) -> dict:
        vals = []
        for _ in range(reps):
            perm = idx[:]
            rng.shuffle(perm)
            rows_p = []
            for i, r in enumerate(eval_rows):
                v = dict(r["per_asset"])
                src = eval_rows[perm[i]]["per_asset"]
                for a in block:
                    v[a] = src.get(a)
                rows_p.append(v)
            s = 0.0
            for v in rows_p:
                d = sum(1 for a in POOLA if v.get(a) == "catch")
                s += 100.0 / 566.0 * (2.0 / 3.0) * (psi(d) - phi(d))
            vals.append(s)
        vals.sort()
        return {
            "reps": reps,
            "mean_pp": round(sum(vals) / reps, 4),
            "p2_5": round(vals[int(0.025 * reps)], 4),
            "p97_5": round(vals[int(0.975 * reps)], 4),
        }

    null_native = permuted_slot(("compiler-warn", "cross-compile"))
    null_wsl = permuted_slot(("asan", "ubsan", "tsan"))

    # ---------- 5. component across k (order-dependence caveat) ----------
    comp_by_k = {}
    for k in (1, 2, 3, 4):
        a = mean_coverage_enum(eval_rows, POOLA, k)
        b = mean_coverage_enum(eval_rows, POOL6, k)
        comp_by_k[k] = {"mean_poolA": round(a, 4), "mean_pool6": round(b, 4), "component_pp": round(a - b, 4)}

    out = {
        "schema": "queyi-711/linker-decomposition/v1",
        "generated_by": "tools/compute_711_linker_decomposition.py",
        "detect_calls": 0,
        "inputs": {
            "matrix": "data/a5_676f_detection_matrix.json",
            "split": "evaluation",
            "pools": {"pool6": list(POOL6), "poolA": list(POOLA)},
        },
        "anchors": anchors,
        "arms": arms,
        "decomposition_k4": {
            "m4_poolA_mean_pct": round(n4, 4),
            "m3_poolA_mean_pct": round(n3, 4),
            "m_linker_plus_3sub_pct": round(m_lin3, 4),
            "mean_pool6_k4_pct": round(n6, 4),
            "slot_effect_pp": round(slot_effect, 4),
            "link_effect_pp": round(link_effect, 4),
            "baseline_shift_pp": round(baseline_shift, 4),
            "component_gain_pp": round(link_effect - slot_effect, 4),
            "zero_yield_counterfactual_mean_pct": zreal,
            "identity_check": "slot - link == mean(poolA) - mean(pool6)",
        },
        "strata_detail_by_d": {
            "definition": "d = # of Pool-A assets catching the sample (0..5)",
            "psi_minus_phi_note": "slot contribution per sample = (2/3)*(psi(d)-phi(d)); positive only at d=4, negative at d=3",
            "strata": strat,
            "linker_catches_by_d": linker_catches_by_d,
        },
        "difficulty_reweighting": reweight,
        "environment": {
            "pure_subpool_analogues": env_pure,
            "alignment_null_native_block": null_native,
            "alignment_null_wsl_block": null_wsl,
        },
        "component_by_k": comp_by_k,
        "notes": [
            "All expectations are exact enumerations over subsets (no sampling).",
            "The slot/link split uses a zero-yield sixth asset as the separator; it is an identity, not an approximation.",
            "The alignment null permutes the native pair (cw,cc) jointly across samples, preserving the native-side joint row; ditto for the WSL triple.",
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"n(evaluation) = {n}")
    print(f"OR full pool = {or_full8:.4f}%")
    print(f"m4 = {n4:.4f}  m3 = {n3:.4f}  m_lin3 = {m_lin3:.4f}  mean6 = {n6:.4f}")
    print(
        f"slot = {slot_effect:.4f} pp   link = {link_effect:.4f} pp   component(gain) = {link_effect - slot_effect:.4f} pp"
    )
    print("zero-yield counterfactual means:", zreal)
    print("reweighting:", json.dumps(reweight, ensure_ascii=False))
    print("env pure:", json.dumps(env_pure, ensure_ascii=False))
    print("null native:", null_native, " null wsl:", null_wsl)
    print("component by k:", json.dumps(comp_by_k, ensure_ascii=False))
    print("strata:", json.dumps(strat, ensure_ascii=False))
    print("linker catches by d:", linker_catches_by_d)
    print(f"wrote {OUT.relative_to(ROOT)}")
    return out


if __name__ == "__main__":
    main()
