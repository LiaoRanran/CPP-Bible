#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""stats_672k.py — 672k W6：基于扩样后数据的**统计检验重做**。

做了什么
========
1. **配对精确 McNemar + Cohen's h + Δ 的配对 Wald CI**（复用 `ablation_stats_671b`，单一来源）；
2. **post-hoc power**（本工具新增，纯标准库）：给定观测到的不一致对数与比例，
   精确 McNemar（双侧 α=0.05）在 H1: p = b/(b+c) 下的检验功效；
3. **样本量计算**：① 要达到 ±5pp（以及 ±3/±10pp）精度需要多少样本（CP95 半宽口径，现算搜索）；
   ② 要在 power=0.8 下检出观测到的 Δ 需要多少配对样本（复用 `sample_size_paired_mcnemar`）；
4. **序贯检验 / e-value**（复用 `tools/confidence_sequence.py` 的 Beta 混合 e-process，不重造）：
   对不一致对做 H0: p≤0.5 vs p>0.5 的任意停止时刻检验（Ville 不等式），并给出
   任意时刻 95% 置信序列区间（**比 CP 宽**——这就是"偷看"的诚实体面）。

事实源（全部现读，不抄汇总）
============================
* `data/holdout/reveal_5_detail_672h.json`、`data/external_corpus/reveal_detail_672h.json`
* `data/experiments/baseline_random.json`（Random† 的 `selection.{set}.picked` 与 seed）
* `data/experiments/llm_arm_672i.json`（LLM 臂的配对）

产物：`data/experiments/stats_672k.json`

用法
====
    python tools/stats_672k.py            # 现算并落盘
    python tools/stats_672k.py --json     # 机读
    python tools/stats_672k.py --selftest # 自检（不读产物）
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ablation_stats_671b as A  # noqa: E402
import confidence_sequence as CS  # noqa: E402  （e-process 单一来源）
import stat_bounds as SB  # noqa: E402

H_DETAIL = ROOT / "data" / "holdout" / "reveal_5_detail_672h.json"
C_DETAIL = ROOT / "data" / "external_corpus" / "reveal_detail_672h.json"
B_RANDOM = ROOT / "data" / "experiments" / "baseline_random.json"
LLM_ARM = ROOT / "data" / "experiments" / "llm_arm_672i.json"
OUT = ROOT / "data" / "experiments" / "stats_672k.json"

STATIC_INSTRUMENTS = {"compiler-warn", "wunsequenced", "cross-compile", "linker"}
ALPHA = 0.05
E_THRESHOLD = 1.0 / ALPHA        # Ville：E ≥ 20 即任意时刻拒绝 H0（α=0.05）


def jload(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


# ── 臂的逐样本重建（口径与 baseline_670a 一致，现读现算）─────────────────────

def holdout_rows() -> list[dict]:
    return [r for r in jload(H_DETAIL)["per_sample"] if r.get("planted") is True]


def corpus_rows() -> list[dict]:
    return list(jload(C_DETAIL)["per_sample"])


def arm_verdicts(rows: list[dict], arm: str, picked: set[str] | None = None) -> dict[str, str]:
    out: dict[str, str] = {}
    for r in rows:
        v, det = r["verdict"], str(r.get("detector") or "unknown")
        if arm == "fd":
            out[r["id"]] = v
        elif arm == "static":
            out[r["id"]] = v if (v in ("unknown", "not_error") or det in STATIC_INSTRUMENTS) \
                else "miss"
        elif arm == "random":
            if v in ("unknown", "not_error"):
                out[r["id"]] = v
            else:
                out[r["id"]] = "catch" if (v == "catch" and det in (picked or set())) else "miss"
        else:
            raise ValueError(arm)
    return out


def pair(a: dict[str, str], b: dict[str, str]) -> dict[str, Any]:
    """配对检验：只在 FD 可测样本上配对（口径同 672h verify）。"""
    ids = [i for i, v in a.items() if v in ("catch", "miss")]
    n = len(ids)
    ka = sum(1 for i in ids if a[i] == "catch")
    kb = sum(1 for i in ids if b[i] == "catch")
    bb = sum(1 for i in ids if a[i] == "catch" and b[i] == "miss")
    cc = sum(1 for i in ids if a[i] == "miss" and b[i] == "catch")
    mcn = A.mcnemar_exact(bb, cc)
    h = A.cohens_h(ka / n, kb / n) if n else {"h": float("nan"), "abs_h": float("nan")}
    dci = A.delta_ci_paired(bb, cc, n)
    return {
        "n": n, "arm_a_k": ka, "arm_b_k": kb,
        "arm_a_rate_pct": round(ka / n * 100, 2) if n else None,
        "arm_b_rate_pct": round(kb / n * 100, 2) if n else None,
        "delta_pp": round((ka - kb) / n * 100, 2) if n else None,
        "discordant": {"b_a_only": bb, "c_b_only": cc, "n_discordant": bb + cc},
        "mcnemar_p": mcn["p_value"], "mcnemar_method": mcn["method"],
        "cohens_h": round(h["h"], 4) if n else None,
        "delta_ci95_pct": [round(dci["ci_low"] * 100, 2), round(dci["ci_high"] * 100, 2)],
    }


# ── 新增统计：post-hoc power / 样本量 / e-value ───────────────────────────────

def mcnemar_reject(b: int, c: int, alpha: float = ALPHA) -> bool:
    """双侧精确 McNemar 是否拒绝（b = A 独有，c = B 独有；n = b + c）。"""
    nd = b + c
    if nd == 0:
        return False
    return min(1.0, 2.0 * A.binom_tail_le(min(b, c), nd, 0.5)) <= alpha


def posthoc_power(b: int, c: int, alpha: float = ALPHA) -> dict[str, Any]:
    """post-hoc power：以观测不一致比例 p̂ = b/(b+c) 为 H1 真值，算精确 McNemar 的检验功效。

    诚实警告（必须随数字一起报）：post-hoc power 是**观测数据的函数**，不是设计期功效；
    p 值大 ⇒ power 一定低（一一对应），不能用它"证明"研究不足。
    """
    n, k = b + c, b
    if n == 0:
        return {"n_discordant": 0, "p_hat": None, "power": None,
                "note": "无不一致对 ⇒ 功效不可定义"}
    p = k / n
    power = 0.0
    for x in range(n + 1):
        if mcnemar_reject(x, n - x, alpha):
            power += math.comb(n, x) * (p ** x) * ((1 - p) ** (n - x))
    return {"n_discordant": n, "p_hat": round(p, 4), "power": round(power, 4),
            "alpha": alpha,
            "note": "post-hoc：p̂ 取自观测；不得当作设计期功效，也不得用来反推『证据不足』"}


def sample_size_for_precision(p_hat: float, halfwidth_pp: float = 5.0,
                             conf: float = 0.95) -> dict[str, Any]:
    """要达到 CP95 半宽 ≤ halfwidth_pp 需要多少样本（在 p̂ 处现算搜索）。"""
    target = halfwidth_pp / 100.0
    for n in range(2, 200001):
        k = round(p_hat * n)
        r = SB.proportion(k, n, conf)
        if (r["cp_high"] - r["cp_low"]) / 2 <= target:
            return {"p_hat": round(p_hat, 4), "halfwidth_pp": halfwidth_pp, "n": n,
                    "cp95_at_n": [round(r["cp_low"] * 100, 2), round(r["cp_high"] * 100, 2)]}
    return {"p_hat": p_hat, "halfwidth_pp": halfwidth_pp, "n": None,
            "note": "搜索上限内未达标"}


def e_value(b: int, c: int, p0: float = 0.5) -> dict[str, Any]:
    """序贯（任意停止时刻）检验：H0: p=p0 vs H1: p>p0，Beta 混合 e-process（Ville）。"""
    n = b + c
    if n == 0:
        return {"n": 0, "e_value": 1.0, "log10_e": 0.0, "reject_at_alpha": False,
                "anytime_p": 1.0, "cs95_anytime": [0.0, 1.0],
                "note": "无不一致对 ⇒ e=1（无证据）"}
    e = CS.eprocess(p0, b, n)
    cs_lo, cs_hi = CS.cs_interval(n, b, ALPHA)
    return {"n": n, "x": b, "p0": p0, "e_value": round(e, 4),
            "log10_e": round(math.log10(e), 4) if e > 0 else None,
            "reject_at_alpha": e >= E_THRESHOLD,
            "ville_threshold": E_THRESHOLD,
            "anytime_p": round(min(1.0, 1.0 / e), 6) if e > 0 else 1.0,
            "cs95_anytime": [round(cs_lo, 4), round(cs_hi, 4)],
            "note": "e-process 任意时刻有效；区间比固定样本 CP 宽——这是防『偷看』的代价"}


def sample_size_for_delta(p1: float, p2: float, psi: float,
                          power: float = 0.80) -> dict[str, Any]:
    """要在 power=0.8 下检出 Δ=p1−p2（配对 McNemar）需要多少配对样本（规范库实现）。"""
    r = A.sample_size_paired_mcnemar(p1, p2, psi, power=power)
    return {"p1": round(p1, 4), "p2": round(p2, 4), "psi_discordant_rate": round(psi, 4),
            "power": power, "n_pairs": r.get("n"), "method": r.get("method", "paired-mcnemar"),
            "note": r.get("note", "")}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="672k W6：统计检验重做")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()

    br = jload(B_RANDOM)
    sets = {
        "holdout": {
            "rows": holdout_rows(),
            "picked": set(br["selection"]["holdout"]["picked"]),
            "seed": br["seed"],
        },
        "corpus": {
            "rows": corpus_rows(),
            "picked": set(br["selection"]["corpus"]["picked"]),
            "seed": br["seed"],
        },
    }
    out_sets: dict[str, Any] = {}
    for name, cfg in sets.items():
        rows = cfg["rows"]
        fd = arm_verdicts(rows, "fd")
        st = arm_verdicts(rows, "static")
        rn = arm_verdicts(rows, "random", cfg["picked"])
        p_st, p_rn = pair(fd, st), pair(fd, rn)
        out_sets[name] = {
            "fd_vs_static": p_st, "fd_vs_random_proxy": p_rn,
            "posthoc_power_static": posthoc_power(p_st["discordant"]["b_a_only"],
                                                  p_st["discordant"]["c_b_only"]),
            "posthoc_power_random": posthoc_power(p_rn["discordant"]["b_a_only"],
                                                  p_rn["discordant"]["c_b_only"]),
            "e_value_static": e_value(p_st["discordant"]["b_a_only"],
                                      p_st["discordant"]["c_b_only"]),
            "e_value_random": e_value(p_rn["discordant"]["b_a_only"],
                                      p_rn["discordant"]["c_b_only"]),
            "random_selection": {"picked": sorted(cfg["picked"]), "seed": cfg["seed"]},
            "random_caveat": "Random†=仪器级代理（非真 B3）；配对按 670a 口径重建",
        }
    # LLM 臂的配对（b/c 取自 672i 产物，现读现算）
    llm = jload(LLM_ARM)
    lc = llm["metrics"]["paired_mcnemar_fd_vs_llm"]
    llm_pair = {
        "b_a_only_fd": lc["b_fd_only"], "c_b_only_llm": lc["c_llm_only"],
        "mcnemar_p": lc["p_value"],
        "e_value_llm_better": e_value(lc["c_llm_only"], lc["b_fd_only"]),
        "posthoc_power": posthoc_power(lc["c_llm_only"], lc["b_fd_only"]),
        "n": llm["metrics"]["llm_n"],
        "note": "方向取『LLM 更好』（c 为 LLM 独有）；实测 c=6,b=0 ⇒ 固定样本 p=0.031 显著，"
                "但任意时刻 e-process 未过 20（见 e_value_llm_better）——两种口径**都要报**",
    }

    # 样本量：±精度 + 检出 Δ 所需配对样本
    p_holdout = out_sets["holdout"]["fd_vs_static"]["arm_a_rate_pct"] / 100
    p_corpus = out_sets["corpus"]["fd_vs_static"]["arm_a_rate_pct"] / 100
    sizes = {
        "holdout_fd_p_hat": p_holdout,
        "corpus_fd_p_hat": p_corpus,
        "precision": {
            "holdout": {f"±{h}pp": sample_size_for_precision(p_holdout, h) for h in (3, 5, 10)},
            "corpus": {f"±{h}pp": sample_size_for_precision(p_corpus, h) for h in (3, 5, 10)},
        },
        "power_0.8_for_observed_delta": {
            "holdout": {k: sample_size_for_delta(p_holdout, k2 / 100, psi)
                        for k, k2, psi in (("vs_static", 2.44,
                                           out_sets["holdout"]["fd_vs_static"]
                                           ["discordant"]["n_discordant"] / 41),
                                           ("vs_random", 9.76,
                                            out_sets["holdout"]["fd_vs_random_proxy"]
                                            ["discordant"]["n_discordant"] / 41))},
            "corpus": {k: sample_size_for_delta(p_corpus, k2 / 100, psi)
                       for k, k2, psi in (("vs_static", 17.19,
                                           out_sets["corpus"]["fd_vs_static"]
                                           ["discordant"]["n_discordant"] / 64),
                                           ("vs_random", 21.88,
                                            out_sets["corpus"]["fd_vs_random_proxy"]
                                            ["discordant"]["n_discordant"] / 64))},
        },
        "note": "Δ 与 ψ（不一致率）都取自本批观测；作为**后续设计**的输入，不是本批结论",
    }

    rep = {
        "schema": "queyi-stats/672k",
        "generated_by": "tools/stats_672k.py（W6：扩样后统计检验重做）",
        "generated_at": _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prereg_refs": ["data/experiments/prereg_672h.json", "data/experiments/prereg_672g.json",
                        "data/experiments/prereg_672i.json"],
        "alpha": ALPHA,
        "sets": out_sets,
        "llm_arm": llm_pair,
        "sample_size": sizes,
        "implementation_reuse": {
            "mcnemar": "ablation_stats_671b.mcnemar_exact（精确二项）",
            "cohens_h": "ablation_stats_671b.cohens_h",
            "delta_ci": "ablation_stats_671b.delta_ci_paired（paired-wald-on-difference）",
            "cp95": "stat_bounds.proportion（Clopper-Pearson beta）",
            "e_process": "confidence_sequence.eprocess / cs_interval（Beta 混合，Ville）",
            "new_in_672k": "posthoc_power / sample_size_for_precision / e_value 封装",
        },
        "honest_notes": [
            "post-hoc power 是观测数据的函数，不是设计期功效；与 p 值一一对应，不得用来论证『研究不足』",
            "Random† 是仪器级代理（非真 B3）；真 B3 见 data/experiments/b3_real_672g.json",
            "任意时刻 e-value 与固定样本 McNemar 是两种口径：都要报，不许挑好看的",
            "样本量计算里的 Δ/ψ 取自本批观测（对后续设计有参考价值，但不是本批结论）",
        ],
    }
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        for s in ("holdout", "corpus"):
            ps = out_sets[s]["fd_vs_static"]
            pr = out_sets[s]["fd_vs_random_proxy"]
            print(f"[{s}] FD-Static Δ{ps['delta_pp']:+.2f}pp p={ps['mcnemar_p']:.3g} "
                  f"h={ps['cohens_h']} power={out_sets[s]['posthoc_power_static']['power']} "
                  f"e={out_sets[s]['e_value_static']['e_value']}")
            print(f"[{s}] FD-Random† Δ{pr['delta_pp']:+.2f}pp p={pr['mcnemar_p']:.3g} "
                  f"h={pr['cohens_h']} power={out_sets[s]['posthoc_power_random']['power']} "
                  f"e={out_sets[s]['e_value_random']['e_value']}")
        print(f"[llm] FD-LLM（LLM 更好方向）p={llm_pair['mcnemar_p']:.3g} "
              f"e={llm_pair['e_value_llm_better']['e_value']} "
              f"reject={llm_pair['e_value_llm_better']['reject_at_alpha']}")
        print("[样本量] ±5pp：holdout "
              f"{sizes['precision']['holdout']['±5pp']['n']}，corpus "
              f"{sizes['precision']['corpus']['±5pp']['n']}")
    if not a.no_write:
        OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")
        print(f"[stats-672k] 写入 {OUT.relative_to(ROOT).as_posix()}")
    return 0


def selftest() -> int:
    ok = 0
    # post-hoc power：单调性与端点
    assert posthoc_power(0, 0)["power"] is None
    assert posthoc_power(33, 0)["power"] == 1.0                    # 33:0 必拒
    assert posthoc_power(1, 0)["power"] < 0.2                      # n=1 不可能显著
    assert posthoc_power(10, 5)["power"] < posthoc_power(20, 5)["power"]
    ok += 4
    # 拒绝域一致性：与 mcnemar_exact 的 p 值对齐
    for b, c in ((13, 0), (5, 5), (6, 1), (10, 2)):
        assert mcnemar_reject(b, c) == (A.mcnemar_exact(b, c)["p_value"] <= ALPHA)
    ok += 1
    # 样本量：±5pp 比 ±3pp 少、比 ±10pp 多
    n5 = sample_size_for_precision(0.83, 5.0)["n"]
    n3 = sample_size_for_precision(0.83, 3.0)["n"]
    n10 = sample_size_for_precision(0.83, 10.0)["n"]
    assert n3 and n5 and n10 and n3 > n5 > n10 > 0
    ok += 1
    # e-value：33:0 远超 20；0:0 = 1；方向对（a 越多 e 越大）
    e1 = e_value(33, 0)
    assert e1["e_value"] > 20 and e1["reject_at_alpha"] is True
    assert e_value(0, 0)["e_value"] == 1.0
    assert e_value(10, 3)["e_value"] > e_value(7, 6)["e_value"]
    ok += 3
    # 任意时刻区间比固定样本 CP 宽（防偷看的代价）
    n, x = 33, 33
    lo_cs, hi_cs = CS.cs_interval(n, x, ALPHA)
    r = SB.proportion(x, n, 0.95)
    assert (hi_cs - lo_cs) >= (r["cp_high"] - r["cp_low"]) - 1e-9
    ok += 1
    # 配对重建口径：static 把 sanitizer 样本记 miss；random 只认 picked
    rows = [{"id": "a", "verdict": "catch", "detector": "asan"},
            {"id": "b", "verdict": "miss", "detector": "compiler-warn"},
            {"id": "c", "verdict": "unknown", "detector": "asan"}]
    assert arm_verdicts(rows, "static") == {"a": "miss", "b": "miss", "c": "unknown"}
    assert arm_verdicts(rows, "random", {"asan"}) == {"a": "catch", "b": "miss", "c": "unknown"}
    ok += 2
    # 配对统计与规范库一致
    p = pair({"a": "catch", "b": "miss", "c": "catch"},
             {"a": "miss", "b": "miss", "c": "catch"})
    assert p["n"] == 3 and p["discordant"] == {"b_a_only": 1, "c_b_only": 0, "n_discordant": 1}
    assert abs(p["mcnemar_p"] - 1.0) < 1e-12
    ok += 2
    print(f"[stats-672k-selftest] {ok} 项通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
