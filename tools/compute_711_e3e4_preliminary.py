#!/usr/bin/env python3
"""711-S2: E3/E4 preliminary analysis on the 683-B3 pilot (200 frames x {asan,ubsan}).

Builds the exact three-state transition matrices T^{(g++13.3 -> clang18)} on the
pilot, recomputes agreement/kappa under the 683 caliber (labels = c/m/u), and
compares with the 692 E1->E2 matrix. Read-only: reads the 683 checkpoint + JSON.

Usage:
    python tools/compute_711_e3e4_preliminary.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CKPT = ROOT / "data" / "683_b1_ckpt.jsonl"
RES = ROOT / "data" / "683_cross_toolchain_results.json"
OUT = ROOT / "data" / "711_e3e4_preliminary.json"

LABELS = ("catch", "miss", "unknown")


def cohen_kappa(pairs: list[tuple[str, str]]) -> float:
    n = len(pairs)
    po = sum(1 for a, b in pairs if a == b) / n
    pe = 0.0
    for lab in LABELS:
        pa = sum(1 for a, _ in pairs if a == lab) / n
        pb = sum(1 for _, b in pairs if b == lab) / n
        pe += pa * pb
    return (po - pe) / (1 - pe)


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p over the discordant pairs."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) / 2**n
    return min(1.0, 2.0 * tail)


def main() -> dict:
    rows = [json.loads(ln) for ln in CKPT.read_text(encoding="utf-8").splitlines() if ln.strip()]
    n = len(rows)
    assert n == 200, n
    res683 = json.loads(RES.read_text(encoding="utf-8"))

    per_asset: dict[str, dict] = {}
    for asset in ("asan", "ubsan"):
        mat = {i: {j: 0 for j in LABELS} for i in LABELS}
        for r in rows:
            a = r["gxx_676g"][asset]
            b = r["clang"][asset]["verdict"]
            mat[a][b] += 1
        pairs = [(r["gxx_676g"][asset], r["clang"][asset]["verdict"]) for r in rows]
        agree = sum(1 for a, b in pairs if a == b)
        kappa = cohen_kappa(pairs)
        b_flip = mat["catch"]["miss"] + mat["catch"]["unknown"]  # catch -> not-catch
        c_flip = mat["miss"]["catch"] + mat["unknown"]["catch"]  # not-catch -> catch
        delta_catch = (
            100.0 * (mat["catch"]["catch"] + mat["miss"]["catch"] + mat["unknown"]["catch"]) / n
            - 100.0 * (mat["catch"]["catch"] + mat["catch"]["miss"] + mat["catch"]["unknown"]) / n
        )
        delta_unknown = (
            100.0 * (mat["catch"]["unknown"] + mat["miss"]["unknown"] + mat["unknown"]["unknown"]) / n
            - 100.0 * (mat["unknown"]["catch"] + mat["unknown"]["miss"] + mat["unknown"]["unknown"]) / n
        )
        per_asset[asset] = {
            "matrix_row_gxx_col_clang": mat,
            "agree": agree,
            "agree_pct": round(100.0 * agree / n, 4),
            "kappa_3class_recomputed": round(kappa, 4),
            "kappa_reported_683": res683["b1"]["per_asset"][asset]["kappa"],
            "gxx_catch": sum(mat["catch"].values()),
            "clang_catch": sum(mat[i]["catch"] for i in LABELS),
            "delta_catch_pp": round(delta_catch, 4),
            "delta_unknown_pp": round(delta_unknown, 4),
            "n_diff": n - agree,
            "flip_catch_miss": mat["catch"]["miss"] + mat["miss"]["catch"],
            "reverse_pairs_c_mc": mat["miss"]["catch"],  # m -> c  (T4 purity probe)
            "forward_pairs_c_cm": mat["catch"]["miss"],  # c -> m
            "unknown_out": mat["catch"]["unknown"] + mat["miss"]["unknown"],
            "mcnemar_exact_p": round(mcnemar_exact(b_flip, c_flip), 4),
            "reported_683": {
                "agree_pct": res683["b1"]["per_asset"][asset]["agree_pct"],
                "kappa": res683["b1"]["per_asset"][asset]["kappa"],
                "gxx_catch_pct": res683["b1"]["per_asset"][asset]["gxx_catch_pct"],
                "clang_catch_pct": res683["b1"]["per_asset"][asset]["clang_catch_pct"],
                "delta_pp": res683["b1"]["per_asset"][asset]["delta_pp_clang_minus_gxx"],
            },
        }

    # defect-type composition of the differing frames (for the P3 reading)
    diff_types: dict[str, dict[str, int]] = {a: {} for a in ("asan", "ubsan")}
    for r in rows:
        for asset in ("asan", "ubsan"):
            if r["gxx_676g"][asset] != r["clang"][asset]["verdict"]:
                t = r["defect_type"]
                diff_types[asset][t] = diff_types[asset].get(t, 0) + 1

    # compile-failure ("tool-availability unknown") shares
    ta_unknown = {}
    for asset in ("asan", "ubsan"):
        k = sum(
            1 for r in rows if r["clang"][asset]["verdict"] == "unknown" and "clang 不可用" in r["clang"][asset]["note"]
        )
        ta_unknown[asset] = k

    # 692 E1 -> E2 reference (from 697 drift algebra, A5 evaluation 566)
    ref_e1e2 = {
        "frame": "A5 evaluation 566, E1 wsl-gcc-13.3 -> E2 windows-native-mingw",
        "n": 566,
        "catch_e1": 340,
        "catch_e2": 140,
        "t_catch_to_catch": 140,
        "t_catch_to_miss": 200,
        "t_catch_to_unknown": 0,
        "t_miss_to_catch": 0,
        "p_catch_to_miss": round(200 / 340, 4),
        "p_miss_to_catch": 0.0,
        "delta_unknown_unaware_pp": 0.0,
        "source": "697_measurement_drift_algebra.md §2.1",
    }

    out = {
        "schema": "queyi-711/e3e4-preliminary/v1",
        "generated_by": "tools/compute_711_e3e4_preliminary.py",
        "detect_calls": 0,
        "pilot": {
            "source": "data/683_b1_ckpt.jsonl (683-B3)",
            "n": n,
            "selection_rule": "stratified_sample(seed=6831, n=200) over exp* rows with files, hung skipped (tools/cross_toolchain_683.py)",
            "environment_pair": "E3-direction: WSL g++ 13.3.0 (baseline, frozen 676g reuse) vs WSL clang++ 18.1.3 (same OS/glibc/linker; compiler swap only)",
            "assets_covered": ["asan", "ubsan"],
        },
        "per_asset": per_asset,
        "diff_composition_by_type": diff_types,
        "tool_availability_unknown": ta_unknown,
        "ref_692_e1e2": ref_e1e2,
        "honesty": [
            "Pilot covers the E3 direction only (compiler swap inside WSL), not E4 (OS swap); 2 of 6 assets; 200 of 566 frames.",
            "Recomputed kappa is reported next to the 683-published value; any gap is registered, not overwritten.",
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    for a, v in per_asset.items():
        print(f"== {a} ==")
        print("  matrix (rows=g++13.3, cols=clang18):", v["matrix_row_gxx_col_clang"])
        print(
            f"  agree {v['agree']}/200 = {v['agree_pct']}%  kappa(recomputed) {v['kappa_3class_recomputed']} vs 683 {v['kappa_reported_683']}"
        )
        print(
            f"  dcatch {v['delta_catch_pp']}pp  dunknown {v['delta_unknown_pp']}pp  c->m {v['forward_pairs_c_cm']}  m->c {v['reverse_pairs_c_mc']}  u_out {v['unknown_out']}  McNemar p {v['mcnemar_exact_p']}"
        )
    print("diff types:", json.dumps(diff_types, ensure_ascii=False))
    print("tool-availability unknowns:", ta_unknown)
    print(f"wrote {OUT.relative_to(ROOT)}")
    return out


if __name__ == "__main__":
    main()
