#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""analyze_683_oc.py — 683-C：operator 四分量全枚举消融（16+16 配置）+ 7 基线统一口径。

判定矩阵与统计原语**全部复用**，不生成新测量：
* 判定矩阵：data/a5_676f_detection_matrix.json（1137×8，676f 冻结）
* 统计原语：tools/run_a5_experiment_673p.py（arm_stats / paired_test / 单点 Random）
* 选择语义：tools/selection_strategies_673p.py::select（FD/Random/Static）
* operator：tools/evolution_operator_677c.py::select_portfolio（一字未改）
* 池定义：data/677c_asset_pools.json（A/B/C，不重新划池）

本批新增（相对 677c 的 5 配置）：
1. **四分量全枚举 2^4 = 16 配置**（每个分量 on=1 / off=0 等权），literal 模式；
2. **unique 模式的 16 配置**（novel 改为"不可替代残余覆盖"，让 novel 成为独立信号）；
3. 7 基线同一批 k 块内并排（Random 单点 + 2000 次分布、Static、FD、Frequency、
   Greedy、Oracle、InfoGain）；
4. all-off 配置的诚实登记（分数恒 0 ⇒ 语义退化为 id 升序，报告明确标注）。

输出：
    data/683_operator_ablation.json     （16+16 配置 × 3 池 × k）
    data/683_baseline_comparison.json   （7 基线 × 3 池 × k）
    data/683_operator_ablation_report.md
    data/683_baseline_comparison.md
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
import run_a5_experiment_673p as a5  # noqa: E402
import selection_strategies_673p as ss  # noqa: E402
import verifier_pool_673p as vp  # noqa: E402

_ana = importlib.import_module("676f_analysis")

MANIFEST = ROOT / "data" / "a5_676f_sample_manifest.json"
MATRIX = ROOT / "data" / "a5_676f_detection_matrix.json"
POOLS = ROOT / "data" / "677c_asset_pools.json"
OUT_ABL = ROOT / "data" / "683_operator_ablation.json"
OUT_BASE = ROOT / "data" / "683_baseline_comparison.json"
OUT_REP = ROOT / "data" / "683_operator_ablation_report.md"
OUT_BASE_MD = ROOT / "data" / "683_baseline_comparison.md"

SEED = a5.SEED
MULTI = a5.MULTI_SEED_N
PRIMARY_K = a5.PRIMARY_K
Index = dict[str, dict[str, str]]

#: 四分量名（与 evolution_operator_677c.score_components 的键一致）
COMPONENTS = ("w_failure", "w_novel", "w_cost", "w_redundancy")
#: 16 配置：每分量 on（1.0）/ off（0.0），等权（消融干净；默认权重版本在 677c 已跑）
CONFIGS_16: dict[str, dict[str, float]] = {}
for _bits in itertools.product((0, 1), repeat=4):
    _name = "".join(("f" if _bits[0] else "x") + ("n" if _bits[1] else "x")
                    + ("c" if _bits[2] else "x") + ("r" if _bits[3] else "x"))
    CONFIGS_16[_name] = {k: float(b) for k, b in zip(COMPONENTS, _bits)}


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _jdump(path: Path, doc: dict[str, Any]) -> None:
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8", newline="\n")
    print(f"[683-C] 写入 {path.relative_to(ROOT).as_posix()}")


def load_data() -> dict[str, Any]:
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    mat = json.loads(MATRIX.read_text(encoding="utf-8"))
    pools_doc = json.loads(POOLS.read_text(encoding="utf-8"))
    index: Index = _ana.index_of(mat)
    samples = man["samples"]
    for r in samples:
        if r["sample_id"] not in index:
            raise KeyError(f"样本 {r['sample_id']} 不在判定矩阵里（fail-loud）")
    deriv = [r for r in samples if r["split"] == "derivation"]
    ev = [r for r in samples if r["split"] == "evaluation"]
    assets = list(_ana.ASSETS)
    return {
        "index": index, "samples": samples, "deriv": deriv, "ev": ev, "assets": assets,
        "deriv_ids": [r["sample_id"] for r in deriv],
        "ev_exec": [{"id": r["sample_id"]} for r in ev],
        "ex": a5.AttributionExecutor(index),
        "fh8": _ana.fail_hits_real(deriv, assets, index),
        "wall": {a: float(v) for a, v in mat["wall_seconds_by_asset"].items()},
        "pools": {pn: pools_doc["pools"][pn]["assets"] for pn in ("A", "B", "C")},
        "pool_names": {pn: pools_doc["pools"][pn]["name"] for pn in ("A", "B", "C")},
    }


# ─────────────────────────────────────────────────────────────────────────────
# 基线（复制 677c 的纯函数实现，口径与产物一致；唯一来源是 677c 报告）
# ─────────────────────────────────────────────────────────────────────────────
def sel_frequency(cands: list[str], k: int, fh: dict[str, int]) -> list[str]:
    return sorted(cands, key=lambda a: (-int(fh.get(a, 0)), a))[:k]


def sel_greedy(cands: list[str], k: int, index: Index, ids: list[str]) -> list[str]:
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
               ev_exec: list[dict[str, Any]]) -> list[str]:
    best_combo: tuple[str, ...] = ()
    best_cnt = -1
    for combo in itertools.combinations(sorted(cands), k):
        cnt = sum(1 for r in ev_exec if ex.verdict(r, combo) == "catch")
        if cnt > best_cnt:
            best_cnt, best_combo = cnt, combo
    return list(best_combo)


def sel_info_gain(cands: list[str], k: int, index: Index, ids: list[str]) -> list[str]:
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
# Stage: ablation（16+16 配置）
# ─────────────────────────────────────────────────────────────────────────────
def run_ablation(ld: dict[str, Any]) -> dict[str, Any]:
    ex, index = ld["ex"], ld["index"]
    ev_exec, deriv_ids = ld["ev_exec"], ld["deriv_ids"]
    pools_out: dict[str, Any] = {}
    for pn in ("A", "B", "C"):
        cands = list(ld["pools"][pn])
        fh_pool = {a: int(ld["fh8"].get(a, 0)) for a in cands}
        blocks: dict[str, Any] = {}
        for k in range(1, len(cands)):
            fd_assets = list(ss.select("failure_driven", vp.ASSET_POOL, max_assets=k,
                                       fail_hits=fh_pool, candidates=cands).assets)
            rnd_sel = list(ss.select("random", vp.ASSET_POOL, max_assets=k, seed=SEED,
                                     candidates=cands).assets)
            configs: dict[str, Any] = {}
            for mode in ("literal", "unique"):
                for name, w in CONFIGS_16.items():
                    tag = name if mode == "literal" else f"u_{name}"
                    r = evo.select_portfolio(cands, k, index, deriv_ids, wall_seconds=ld["wall"],
                                             weights=w, novel_mode=mode)
                    arm = a5.arm_stats(ev_exec, tuple(r["selection"]), ex)
                    configs[tag] = {
                        "weights": w, "novel_mode": mode,
                        "selection": r["selection"],
                        "rate_pct": arm["rate_pct"], "cp95": arm["cp95"],
                        "paired_vs_random_single": a5.paired_test(
                            ev_exec, tuple(r["selection"]), tuple(rnd_sel), ex,
                            label_a=tag, label_b="random_single"),
                        "paired_vs_fd": a5.paired_test(
                            ev_exec, tuple(r["selection"]), tuple(fd_assets), ex,
                            label_a=tag, label_b="fd"),
                    }
            greedy_assets = sel_greedy(cands, k, index, deriv_ids)
            # 补充验证配置：literal 模式下 novel≡failure ⇒ (w_f,w_n) ≡ (w_f+w_n, 0)
            verif: dict[str, Any] = {}
            for tag, wv in (
                    ("f2xx", {"w_failure": 2.0, "w_novel": 0.0, "w_cost": 0.0, "w_redundancy": 0.0}),
                    ("f2cx", {"w_failure": 2.0, "w_novel": 0.0, "w_cost": 1.0, "w_redundancy": 0.0}),
                    ("f2xr", {"w_failure": 2.0, "w_novel": 0.0, "w_cost": 0.0, "w_redundancy": 1.0})):
                rv = evo.select_portfolio(cands, k, index, deriv_ids, wall_seconds=ld["wall"],
                                          weights=wv, novel_mode="literal")
                verif[tag] = {"weights": wv, "selection": rv["selection"]}
            # 语义观察（每 k 记录，用于报告里的等价性表）
            equiv = {
                "alloff_is_id_sorted": configs["xxxx"]["selection"] == sorted(cands)[:k],
                "fd_only_equals_greedy": configs["fxxx"]["selection"] == greedy_assets,
                "fd_only_equals_fd_topk": configs["fxxx"]["selection"] == fd_assets,
                "fnxx_equals_fxxx": configs["fnxx"]["selection"] == configs["fxxx"]["selection"],
                "novel_shift_equivalence": (
                    configs["fncx"]["selection"] == verif["f2cx"]["selection"]
                    and configs["fnxr"]["selection"] == verif["f2xr"]["selection"]),
                "u_fxxx_equals_fd": configs["u_fxxx"]["selection"] == fd_assets,
                "unique_novel_changes_choice": configs["u_xnxx"]["selection"] != configs["xxxx"]["selection"],
            }
            blocks[str(k)] = {"fd_assets": fd_assets, "random_single": rnd_sel,
                              "greedy_assets": greedy_assets,
                              "configs": configs, "verification_configs": verif,
                              "equivalence": equiv}
        pools_out[pn] = {"pool_name": ld["pool_names"][pn], "assets": cands, "k_blocks": blocks}
    return {
        "schema": "queyi-683-operator-ablation/v1", "generated_by": "tools/analyze_683_oc.py",
        "generated_at": _now(),
        "design": {
            "configs": "2^4 全枚举：w_failure/w_novel/w_cost/w_redundancy ∈ {0,1}（等权）",
            "modes": "literal（规格原文；novel≡failure 数学坍缩）与 unique（不可替代残余覆盖，探索性）",
            "all_off_note": "配置 xxxx 全分量 0 ⇒ 分数恒 0，同分 id 升序 ⇒ 选择=按 id 升序前 k；"
                            "本批如实登记而非剔除",
            "statistics": "复用 673p：arm_stats（CP95）+ paired_test（McNemar exact + Δ 95% CI + Cohen's h）",
            "matrix": "676f 冻结判定矩阵（1137×8）；本批不重跑 detect()",
        },
        "pools": pools_out,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Stage: baselines（7 个）
# ─────────────────────────────────────────────────────────────────────────────
def run_baselines(ld: dict[str, Any]) -> dict[str, Any]:
    ex, index = ld["ex"], ld["index"]
    ev_exec, deriv_ids = ld["ev_exec"], ld["deriv_ids"]
    pools_out: dict[str, Any] = {}
    for pn in ("A", "B", "C"):
        cands = list(ld["pools"][pn])
        fh_pool = {a: int(ld["fh8"].get(a, 0)) for a in cands}
        blocks: dict[str, Any] = {}
        for k in range(1, len(cands)):
            fd_assets = list(ss.select("failure_driven", vp.ASSET_POOL, max_assets=k,
                                       fail_hits=fh_pool, candidates=cands).assets)
            # static 臂只认静态资产 ⇒ 预算自动降为池内静态资产数（与 673p/677c 口径一致）
            n_static = len([a for a in cands if a in vp.STATIC_ASSETS])
            static_assets = list(ss.select("static", vp.ASSET_POOL, max_assets=min(k, n_static),
                                           candidates=cands).assets)
            rnd_sel = list(ss.select("random", vp.ASSET_POOL, max_assets=k, seed=SEED,
                                     candidates=cands).assets)
            methods = {
                "random_single": rnd_sel,
                "static": static_assets,
                "fd": fd_assets,
                "frequency": sel_frequency(cands, k, fh_pool),
                "greedy": sel_greedy(cands, k, index, deriv_ids),
                "oracle": sel_oracle(cands, k, ex, ev_exec),
                "info_gain": sel_info_gain(cands, k, index, deriv_ids),
            }
            rows: dict[str, Any] = {}
            for name, sel in methods.items():
                arm = a5.arm_stats(ev_exec, tuple(sel), ex)
                rows[name] = {
                    "selection": sel, "rate_pct": arm["rate_pct"], "cp95": arm["cp95"],
                    "paired_vs_random_single": a5.paired_test(
                        ev_exec, tuple(sel), tuple(rnd_sel), ex,
                        label_a=name, label_b="random_single"),
                    "paired_vs_fd": a5.paired_test(
                        ev_exec, tuple(sel), tuple(fd_assets), ex, label_a=name, label_b="fd"),
                }
            # 2000 次随机分布（均值/中位/SD/95 区间 + fd 百分位）
            dist: list[float] = []
            for s in range(MULTI):
                pick = list(ss.select("random", vp.ASSET_POOL, max_assets=k,
                                      seed=SEED + s + 1, candidates=cands).assets)
                n_catch = sum(1 for r in ev_exec if ex.verdict(r, tuple(pick)) == "catch")
                dist.append(n_catch / len(ev_exec) * 100)
            dist_sorted = sorted(dist)
            fd_rate = rows["fd"]["rate_pct"] or 0.0
            pctile = round(sum(1 for x in dist if x < fd_rate) / len(dist) * 100, 2)
            blocks[str(k)] = {
                "methods": rows,
                "random_distribution": {
                    "n": len(dist), "seed": SEED, "mean_pct": round(sum(dist) / len(dist), 4),
                    "median_pct": round(dist_sorted[len(dist) // 2], 4),
                    "sd_pp": round((sum((x - sum(dist) / len(dist)) ** 2 for x in dist)
                                    / len(dist)) ** 0.5, 4),
                    "p95_lo_pct": round(dist_sorted[int(0.025 * len(dist))], 4),
                    "p95_hi_pct": round(dist_sorted[int(0.975 * len(dist))], 4),
                    "fd_percentile": pctile,
                },
            }
        pools_out[pn] = {"pool_name": ld["pool_names"][pn], "assets": cands, "k_blocks": blocks}
    return {
        "schema": "queyi-683-baseline-comparison/v1", "generated_by": "tools/analyze_683_oc.py",
        "generated_at": _now(),
        "design": {
            "baselines": ["random_single", "static", "fd", "frequency", "greedy", "oracle", "info_gain"],
            "oracle_note": "Oracle 在评估集上穷举 ⇒ 上界参考，不可达（评估泄漏）",
            "frequency_note": "Frequency 与 FD 在本数据模型下同构（排序键同为派生集 catch 计数）",
            "random_distribution": f"{MULTI} 次重抽（seed {SEED}+i），与 682 种子稳定性口径一致",
            "matrix": "676f 冻结判定矩阵（1137×8）",
        },
        "pools": pools_out,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Stage: reports
# ─────────────────────────────────────────────────────────────────────────────
def _fmt_p(p: Any) -> str:
    if p is None:
        return "n/a"
    if p == 0:
        return "<1e-300"
    return f"{p:.2e}" if p < 1e-4 else f"{p:.4g}"


def write_reports(abl: dict[str, Any], base: dict[str, Any]) -> int:
    lines = ["# 683-C1 · Operator 四分量全枚举消融（16 literal + 16 unique 配置）", "",
             "- 判定矩阵：676f 冻结（1137×8）；原语：673p（未改动）；operator：677c（未改动）。",
             "- 16 配置 = w_failure/w_novel/w_cost/w_redundancy ∈ {0,1} 全枚举（等权）。", ""]
    lines.append("## 关键结论（literal 模式，Pool A）")
    blkA = abl["pools"]["A"]["k_blocks"]
    ks = sorted(blkA, key=int)
    kmain = str(PRIMARY_K) if str(PRIMARY_K) in blkA else ks[-1]
    cfgs = blkA[kmain]["configs"]
    ranked = sorted((c for c in cfgs), key=lambda t: -(cfgs[t]["rate_pct"] or 0))
    lines.append(f"\nk={kmain}（主预算）检出率排名（前 8）：\n")
    lines.append("| 配置 | selection | rate% | Δ vs random(pp) | p vs random |")
    lines.append("|---|---|---:|---:|---:|")
    for t in ranked[:8]:
        c = cfgs[t]
        pv = c["paired_vs_random_single"]
        lines.append(f"| `{t}` | {','.join(c['selection'])} | {c['rate_pct']} | "
                     f"{pv.get('delta_pp')} | {_fmt_p(pv.get('mcnemar_p'))} |")
    lines.append("\n## 等价性观察（跨全部池与 k）")
    keys_all = ("alloff_is_id_sorted", "fd_only_equals_greedy", "fd_only_equals_fd_topk",
                "fnxx_equals_fxxx", "novel_shift_equivalence",
                "u_fxxx_equals_fd", "unique_novel_changes_choice")
    tally = {k: 0 for k in keys_all}
    tally["n_blocks"] = 0
    for pn in ("A", "B", "C"):
        for k, blk in abl["pools"][pn]["k_blocks"].items():
            tally["n_blocks"] += 1
            for key in keys_all:
                tally[key] += int(bool(blk["equivalence"][key]))
    lines.append(f"\n- 块数：{tally['n_blocks']}")
    for key in keys_all:
        lines.append(f"- `{key}`：{tally[key]}/{tally['n_blocks']} 块成立")
    lines.append("\n> honest note：literal 模式下 novel≡failure 是**规格的数学性质**（F_t 定义"
                 "使第二条件恒真，一行证明见 677c 设计报告）；`unique` 模式是本批给出的修复变体，"
                 "它让 novel 成为独立信号 —— 上表 `u_` 前缀为 unique 模式结果。")
    OUT_REP.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"[683-C] 写入 {OUT_REP.relative_to(ROOT).as_posix()}")

    bl = ["# 683-C2 · 7 基线统一口径对比（含 2000 次随机分布）", ""]
    for pn in ("A", "B"):
        blk = base["pools"][pn]["k_blocks"]
        km = str(PRIMARY_K) if str(PRIMARY_K) in blk else sorted(blk, key=int)[-1]
        bl.append(f"\n## Pool {pn}（{base['pools'][pn]['pool_name']}），k={km}\n")
        bl.append("| 方法 | selection | rate% | CP95 | Δ vs random(pp) | p |")
        bl.append("|---|---|---:|---|---:|---:|")
        rows = blk[km]["methods"]
        for name in sorted(rows, key=lambda t: -(rows[t]["rate_pct"] or 0)):
            r = rows[name]
            pv = r["paired_vs_random_single"]
            bl.append(f"| {name} | {','.join(r['selection'])} | {r['rate_pct']} | "
                      f"[{r['cp95'][0]}, {r['cp95'][1]}] | {pv.get('delta_pp')} | "
                      f"{_fmt_p(pv.get('mcnemar_p'))} |")
        d = blk[km]["random_distribution"]
        bl.append(f"\n随机分布：n={d['n']}、均值 {d['mean_pct']}%、中位 {d['median_pct']}%、"
                  f"SD {d['sd_pp']}pp、95% 区间 [{d['p95_lo_pct']}, {d['p95_hi_pct']}]%、"
                  f"**FD 位于第 {d['fd_percentile']} 百分位**")
    OUT_BASE_MD.write_text("\n".join(bl) + "\n", encoding="utf-8", newline="\n")
    print(f"[683-C] 写入 {OUT_BASE_MD.relative_to(ROOT).as_posix()}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("ablation", "baselines", "reports", "all"), default="all")
    a = ap.parse_args()
    ld = load_data()
    abl = base = None
    if a.stage in ("ablation", "all"):
        abl = run_ablation(ld)
        _jdump(OUT_ABL, abl)
    if a.stage in ("baselines", "all"):
        base = run_baselines(ld)
        _jdump(OUT_BASE, base)
    if a.stage in ("reports", "all"):
        if abl is None:
            abl = json.loads(OUT_ABL.read_text(encoding="utf-8"))
        if base is None:
            base = json.loads(OUT_BASE.read_text(encoding="utf-8"))
        write_reports(abl, base)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
