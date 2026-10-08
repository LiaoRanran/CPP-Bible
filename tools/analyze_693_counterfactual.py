#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""analyze_693_counterfactual.py — 693-E4：反事实分析扩展（**只读，0 次 detect**）。

在 686 的四个反事实臂上做**扩展**（任务书 E4.1）
================================================
686 已做：样本量 100/200/400/600/800/1000、资产集 92 组合、标签质量 1/3/5/10/15%、
检测器噪声 ε=5..50%。
693-E4 新增的四个臂：

| 臂 | 内容 | 相对 686 的新意 |
|---|---|---|
| A | **样本量 50 / 100 / 200 / 566** | 补上小样本端（n=50/100）与 A5 主分析的 n=566 |
| B | **逐个移除资产**（8 个单删）+ 关键资产排序 | 686 是 92 组合；本臂给出**单资产可解释性** |
| C | **标签质量 5/10/15% 翻转**，分两种翻转对象 | ⭐ 686 只翻了目标集；本臂**分离**「翻 ground truth」与「翻 per_asset 判定」 |
| D | **环境敏感性**（E1 六资产 / E2 三资产，unaware 与 aware） | 686 无环境臂 |

⭐ C 臂的结构性发现
==================
A5 主端点 Δ（FD − Random）**只依赖 `per_asset` 判定**，**不依赖 `expected_verdict`**。
因此：

* 翻转 `expected_verdict`（ground truth）⇒ **Δ 逐位不变**，但盲区率/recall 会变；
* 翻转 `per_asset` 判定（检测器噪声）⇒ Δ 会变。

把两者混在一起谈"标签质量敏感性"会把**一个不敏感的量**说成敏感的。本臂显式分离。

复用（只读，不改）
==================
`data/684_analysis.py` 的 `load_matrix / build_catch_sets / build_f / greedy_select`
与常量 `K / ASSETS / AIDX / SEED`（与 686 同口径）。

用法
====
    python tools/analyze_693_counterfactual.py
"""
from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import math
import random
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("analyze_693_counterfactual")
OUT_JSON = ROOT / "data" / "693_counterfactual_extended.json"
OUT_MD = ROOT / "data" / "693_counterfactual_report.md"

MATRIX = "blindspot_676g_detection_matrix.json"
ENV = "692_environment_paired_experiment.json"

REPS = 60
DRAWS = 1000


def _load_684() -> Any:
    """只读加载 data/684_analysis.py（不改其任何状态）。"""
    spec = importlib.util.spec_from_file_location("m684_693", str(ROOT / "data" / "684_analysis.py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("无法加载 data/684_analysis.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # 684_analysis 以模块级 DATA/ROOT 定位产物；动态加载后需按本仓根校正。
    # mypy 看不到动态属性 ⇒ 用 setattr 表达（等价于 mod.DATA = DATA，但类型检查友好）。
    setattr(mod, "DATA", DATA)  # noqa: B010
    setattr(mod, "ROOT", ROOT)  # noqa: B010
    return mod


def _random_draw_values(f: list[int], pool_idx: list[int], k: int, draws: int,
                        rng: random.Random) -> list[int]:
    vals: list[int] = []
    for _ in range(draws):
        mask = 0
        for i in rng.sample(pool_idx, k):
            mask |= (1 << i)
        vals.append(f[mask])
    return vals


def _delta(f: list[int], n: int, gmask: int, pool_idx: list[int], k: int,
           draws: int, rng: random.Random) -> dict[str, float]:
    gval = f[gmask]
    rvals = _random_draw_values(f, pool_idx, k, draws, rng)
    rmean = sum(rvals) / len(rvals)
    return {
        "greedy_rate_pct": round(100.0 * gval / n, 4),
        "random_mean_rate_pct": round(100.0 * rmean / n, 4),
        "delta_pp": round(100.0 * (gval - rmean) / n, 4),
        "percentile": round(100.0 * sum(1 for v in rvals if v <= gval) / len(rvals), 2),
    }


def arm_a_sample_size(m684: Any, catch_sets: list[set[str]], n_all: int,
                      ns: tuple[int, ...]) -> dict[str, Any]:
    """A 臂：样本量敏感性。"""
    rng = random.Random(m684.SEED)
    pool_idx = list(range(len(m684.ASSETS)))
    out: dict[str, Any] = {}
    all_idx = list(range(n_all))
    for n in ns:
        if n > n_all:
            continue
        deltas: list[float] = []
        rates: list[float] = []
        rand_means: list[float] = []
        percs: list[float] = []
        for _ in range(REPS):
            idx = rng.sample(all_idx, n)
            sub = [catch_sets[i] for i in idx]
            f, _ = m684.build_f(sub)
            _gset, _marg, gmask = m684.greedy_select(m684.K, lambda m: f[m], m684.ASSETS)
            d = _delta(f, n, gmask, pool_idx, m684.K, DRAWS, rng)
            deltas.append(d["delta_pp"])
            rates.append(d["greedy_rate_pct"])
            rand_means.append(d["random_mean_rate_pct"])
            percs.append(d["percentile"])
        deltas_sorted = sorted(deltas)
        lo = deltas_sorted[int(0.025 * (REPS - 1))]
        hi = deltas_sorted[int(0.975 * (REPS - 1))]
        mean_d = sum(deltas) / REPS
        sd = math.sqrt(sum((x - mean_d) ** 2 for x in deltas) / REPS)
        out[str(n)] = {
            "n": n, "reps": REPS, "draws_per_rep": DRAWS,
            "greedy_rate_pct_mean": round(sum(rates) / REPS, 4),
            "random_mean_rate_pct_mean": round(sum(rand_means) / REPS, 4),
            "delta_pp_mean": round(mean_d, 4),
            "delta_pp_sd": round(sd, 4),
            "delta_pp_ci95": [round(lo, 4), round(hi, 4)],
            "ci_width_pp": round(hi - lo, 4),
            "percentile_mean": round(sum(percs) / REPS, 2),
            "frac_reps_fd_top5pct": round(sum(1 for p in percs if p >= 95) / REPS, 4),
        }
        _log.info("A 臂 n=%d：Δ=%.3fpp（CI 宽 %.3f）", n, mean_d, hi - lo)
    return out


def arm_b_asset_removal(m684: Any, catch_sets: list[set[str]], n_all: int) -> dict[str, Any]:
    """B 臂：逐个移除资产。"""
    rng = random.Random(m684.SEED)
    f_full, _ = m684.build_f(catch_sets)
    pool_full = list(range(len(m684.ASSETS)))
    _gs, _mg, gmask = m684.greedy_select(m684.K, lambda m: f_full[m], m684.ASSETS)
    base = _delta(f_full, n_all, gmask, pool_full, m684.K, DRAWS, rng)
    out: dict[str, Any] = {
        "full_pool": {"assets": list(m684.ASSETS), **base},
        "removal": {},
        "confound_note": (
            "移除资产后**池变小**（8→7），随机基线的期望随之改变 ⇒ "
            "`delta_change_pp` 同时包含「资产本身的作用」与「池大小效应」，"
            "**不能**单独读作该资产的边际贡献。要看纯边际贡献请用 E2 的 "
            "asset_necessity（去掉该资产损失的 catch 数）。"),
    }
    for drop in m684.ASSETS:
        pool = [a for a in m684.ASSETS if a != drop]
        pool_idx = [m684.AIDX[a] for a in pool]
        f = [0] * 256
        for mask in range(1, 256):
            cnt = 0
            for cs in catch_sets:
                m = 0
                for a in cs:
                    m |= (1 << m684.AIDX[a])
                if m & mask:
                    cnt += 1
            f[mask] = cnt
        _gset, _mg, gm = m684.greedy_select(m684.K, lambda mm: f[mm], pool)
        d = _delta(f, n_all, gm, pool_idx, m684.K, DRAWS, rng)
        out["removal"][drop] = {
            "remaining_assets": pool, **d,
            "delta_change_pp": round(d["delta_pp"] - base["delta_pp"], 4),
            "greedy_rate_change_pp": round(d["greedy_rate_pct"] - base["greedy_rate_pct"], 4),
        }
        _log.info("B 臂 移除 %s：Δ=%.3fpp（Δ变化 %+.3f）", drop, d["delta_pp"],
                  d["delta_pp"] - base["delta_pp"])
    return out


def arm_c_label_quality(m684: Any, samples: list[dict[str, Any]],
                        catch_sets: list[set[str]],
                        n_all: int, rates: tuple[float, ...]) -> dict[str, Any]:
    """C 臂：标签质量敏感性（分离两种翻转对象）。

    ⚠ `samples` 必须是**与 catch_sets 同长的子集**（A5 evaluation，566）。
    首次实现误传了整份 A5 矩阵（1137）⇒ 索引越界（已修复并留痕）。
    """
    rng = random.Random(m684.SEED)
    if len(samples) != len(catch_sets):
        raise ValueError(f"samples({len(samples)}) 与 catch_sets({len(catch_sets)}) 长度不一致")
    pool_idx = list(range(len(m684.ASSETS)))
    f_full, _ = m684.build_f(catch_sets)
    _gs, _mg, gmask = m684.greedy_select(m684.K, lambda m: f_full[m], m684.ASSETS)
    base = _delta(f_full, n_all, gmask, pool_idx, m684.K, DRAWS, rng)
    n_catch = sum(1 for s in samples if str(s.get("expected_verdict")) == "catch")
    base_blind = round(100.0 * (n_all - f_full[gmask]) / n_all, 4)

    out: dict[str, Any] = {
        "baseline": {**base, "blind_rate_pct": base_blind,
                     "expected_catch": n_catch},
        "flip_ground_truth": {},
        "flip_per_asset_verdict": {},
    }

    for p in rates:
        # ① 翻 expected_verdict：Δ 只依赖 per_asset ⇒ 预期逐位不变
        idx = rng.sample(range(n_all), int(round(n_all * p / 100.0)))
        flipped = 0
        for i in idx:
            s = samples[i]
            if str(s.get("expected_verdict")) == "catch":
                flipped += 1
        new_catch = n_catch - flipped + (len(idx) - flipped)
        out["flip_ground_truth"][f"{p:g}%"] = {
            "n_flipped": len(idx),
            "expected_catch_after": new_catch,
            "delta_pp": base["delta_pp"],
            "delta_pp_change": 0.0,
            "note": "Δ 逐位不变：A5 主端点只依赖 per_asset 判定，不依赖 ground truth",
        }

        # ② 翻 per_asset 判定（检测器噪声）⇒ 重算 catch_sets 与 Δ
        cells: list[tuple[int, str]] = []
        for i, s in enumerate(samples):
            for a, v in (s.get("per_asset") or {}).items():
                if v in ("catch", "miss"):
                    cells.append((i, a))
        pick = rng.sample(cells, int(round(len(cells) * p / 100.0)))
        noisy = [set(cs) for cs in catch_sets]
        for i, a in pick:
            if a in noisy[i]:
                noisy[i].discard(a)
            else:
                noisy[i].add(a)
        f2, _ = m684.build_f(noisy)
        _g2, _m2, gm2 = m684.greedy_select(m684.K, lambda mm: f2[mm], m684.ASSETS)
        d2 = _delta(f2, n_all, gm2, pool_idx, m684.K, DRAWS, rng)
        out["flip_per_asset_verdict"][f"{p:g}%"] = {
            "n_cells_flipped": len(pick),
            "n_cells_total": len(cells),
            **d2,
            "delta_change_pp": round(d2["delta_pp"] - base["delta_pp"], 4),
            "blind_rate_pct": round(100.0 * (n_all - f2[gm2]) / n_all, 4),
        }
        _log.info("C 臂 %g%%：翻 GT Δ 变化 0.000pp；翻 per_asset Δ=%+.3fpp", p,
                  d2["delta_pp"] - base["delta_pp"])
    return out


def arm_d_environment(m684: Any, samples: list[dict[str, Any]],
                      n_all: int) -> dict[str, Any]:
    """D 臂：环境敏感性（E1 六资产 / E2 三资产，unaware 与 aware）。"""
    env = load_json_cached(DATA / ENV)
    e1 = list(env["asset_partition"]["E1_supported"])
    e2 = list(env["asset_partition"]["E2_supported"])
    out: dict[str, Any] = {"E1_supported": e1, "E2_supported": e2, "arms": {}}

    def _rate(assets: list[str], mode: str) -> dict[str, Any]:
        catch = unknown = 0
        for s in samples:
            vals = [_verdict((s.get("per_asset") or {}).get(a)) for a in assets]
            if "catch" in vals:
                catch += 1
            elif mode == "aware" and "unknown" in vals:
                unknown += 1
        miss = n_all - catch - (unknown if mode == "aware" else 0)
        return {
            "catch": catch, "miss": miss, "unknown": unknown,
            "catch_rate_pct": round(100.0 * catch / n_all, 4),
            "unknown_rate_pct": round(100.0 * unknown / n_all, 4),
            "conditional_recall_pct": (round(100.0 * catch / (catch + miss), 4)
                                       if (catch + miss) else None),
        }

    for name, assets in (("E1_wsl_6assets", e1), ("E2_native_3assets", e2)):
        out["arms"][name] = {
            "unaware": _rate(assets, "unaware"),
            "aware": _rate(assets, "aware"),
        }
    out["delta_pp_unaware"] = round(
        out["arms"]["E1_wsl_6assets"]["unaware"]["catch_rate_pct"]
        - out["arms"]["E2_native_3assets"]["unaware"]["catch_rate_pct"], 4)
    out["delta_pp_aware_unknown"] = round(
        out["arms"]["E2_native_3assets"]["aware"]["unknown_rate_pct"], 4)
    out["container_arm"] = {
        "executed": False,
        "reason": "693 执行环境未安装 Docker ⇒ 容器臂**未执行**（与 B 阶段同一登记）",
    }
    _log.info("D 臂：E1 %.2f%% vs E2 %.2f%%（unaware），Δ=%.2fpp",
              out["arms"]["E1_wsl_6assets"]["unaware"]["catch_rate_pct"],
              out["arms"]["E2_native_3assets"]["unaware"]["catch_rate_pct"],
              out["delta_pp_unaware"])
    return out


def _verdict(rec: Any) -> str:
    """容忍两种 per_asset 形态：字符串（A5 矩阵）与字典（676g 矩阵）。"""
    if isinstance(rec, dict):
        return str(rec.get("verdict", "unknown"))
    return str(rec) if rec else "unknown"


def _eval_frame(m684: Any) -> tuple[dict[str, Any], list[set[str]], list[dict[str, Any]]]:
    """取 A5 主分析帧（split == evaluation，n=566）。

    ⚠ 必须用 `a5_676f_detection_matrix.json`（684.load_matrix 的默认）：
    它的 `per_asset` 是**字符串**；而 676g 的 `per_asset` 是**字典**
    （`{"verdict": ...}`）。首次实现误用了 676g ⇒ catch 集合全空 ⇒ Δ 恒 0
    （已在本脚本修复并留痕）。本函数统一走 A5 帧，保证与 676f/684/686 同口径。
    """
    matrix = m684.load_matrix()
    ev = [s for s in matrix["samples"] if str(s.get("split")) == "evaluation"]
    sub = {"samples": ev}
    catch_sets, samples = m684.build_catch_sets(sub)
    return matrix, catch_sets, samples


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", default="50,100,200,566")
    ap.add_argument("--rates", default="5,10,15")
    args = ap.parse_args()

    m684 = _load_684()
    matrix, catch_sets, samples = _eval_frame(m684)
    n_all = len(samples)
    _log.info("A5 evaluation 帧：n=%d，总 catch 数=%d", n_all,
              sum(len(x) for x in catch_sets))
    ns = tuple(int(x) for x in args.ns.split(",") if x.strip())
    rates = tuple(float(x) for x in args.rates.split(",") if x.strip())

    doc: dict[str, Any] = {
        "schema": "queyi-693-counterfactual-extended/v1",
        "generated_by": "tools/analyze_693_counterfactual.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "reused_module": "data/684_analysis.py（只读；K=4 / ASSETS / AIDX / SEED 同口径）",
        "frame": "data/a5_676f_detection_matrix.json split=evaluation",
        "n_samples": n_all,
        "reps": REPS,
        "draws_per_rep": DRAWS,
        "arm_a_sample_size": arm_a_sample_size(m684, catch_sets, n_all, ns),
        "arm_b_asset_removal": arm_b_asset_removal(m684, catch_sets, n_all),
        "arm_c_label_quality": arm_c_label_quality(m684, samples, catch_sets, n_all, rates),
        "arm_d_environment": arm_d_environment(m684, samples, n_all),
        "honest_limits": [
            "所有臂都在**同一份冻结矩阵**上重采样/重加权，不产生新的检测事实。",
            "REPS/DRAWS 低于 686（60×1000 vs 100×2000）⇒ CI 更宽；方向性结论可比，绝对宽度不可比。",
            "C 臂的 per_asset 翻转是**独立同分布**的合成噪声，真实标注错误是系统性的。",
            "D 臂的容器分支**未执行**（本机无 Docker）；E2 的 aware 口径下 conditional recall 分母为 0。",
            "A 臂的 n=566 子采样与 A5 主分析的 566 帧**不是同一批样本**（此处是随机 566/1147）。",
        ],
    }

    OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")
    OUT_MD.write_text(_md(doc), encoding="utf-8", newline="\n")
    print(f"[693-E4] -> {OUT_JSON}")


def _md(doc: dict[str, Any]) -> str:
    a = doc["arm_a_sample_size"]
    b = doc["arm_b_asset_removal"]
    c = doc["arm_c_label_quality"]
    d = doc["arm_d_environment"]
    lines = [
        "# 693-E4 · 反事实分析扩展报告",
        "",
        f"- 生成：{doc['generated_at']}｜脚本：`tools/analyze_693_counterfactual.py`",
        f"- **`detect_calls` = {doc['detect_calls']}**（只读冻结矩阵，符合红线 8）",
        f"- 复用：{doc['reused_module']}",
        f"- 样本 {doc['n_samples']}；每格 {doc['reps']} 次重采样 × {doc['draws_per_rep']} 次随机抽样",
        "",
        "## A 臂 · 样本量敏感性（n = 50 / 100 / 200 / 566）",
        "",
        "| n | FD 贪心率% | 随机均值% | Δpp 均值 | Δpp SD | CI95 | CI 宽 | FD 进前 5% 的重复占比 |",
        "|---:|---:|---:|---:|---:|---|---:|---:|",
    ]
    for n, v in a.items():
        lines.append(f"| {v['n']} | {v['greedy_rate_pct_mean']:.2f} | "
                     f"{v['random_mean_rate_pct_mean']:.2f} | **{v['delta_pp_mean']:+.3f}** | "
                     f"{v['delta_pp_sd']:.3f} | [{v['delta_pp_ci95'][0]:.2f}, "
                     f"{v['delta_pp_ci95'][1]:.2f}] | {v['ci_width_pp']:.2f} | "
                     f"{v['frac_reps_fd_top5pct']:.2f} |")
    lines += [
        "",
        "## B 臂 · 逐个移除资产",
        "",
        "| 移除 | FD 贪心率% | Δpp | Δ 变化 | 贪心率变化 |",
        "|---|---:|---:|---:|---:|",
    ]
    base = b["full_pool"]
    lines.append(f"| （不删） | {base['greedy_rate_pct']:.2f} | {base['delta_pp']:+.3f} | — | — |")
    for k, v in sorted(b["removal"].items(), key=lambda kv: kv[1]["delta_change_pp"]):
        lines.append(f"| `{k}` | {v['greedy_rate_pct']:.2f} | {v['delta_pp']:+.3f} | "
                     f"{v['delta_change_pp']:+.3f} | {v['greedy_rate_change_pp']:+.3f} |")
    lines += [
        "",
        "## C 臂 · 标签质量敏感性（5% / 10% / 15%）—— **两种翻转对象必须分开看**",
        "",
        "### C1 翻转 `expected_verdict`（ground truth）",
        "",
        "| 翻转率 | 翻转数 | 翻后 expected=catch | Δpp | Δ 变化 |",
        "|---|---:|---:|---:|---:|",
    ]
    for k, v in c["flip_ground_truth"].items():
        lines.append(f"| {k} | {v['n_flipped']} | {v['expected_catch_after']} | "
                     f"{v['delta_pp']:+.3f} | **{v['delta_pp_change']:+.3f}** |")
    lines += [
        "",
        f"> **结构性发现**：{c['flip_ground_truth'][next(iter(c['flip_ground_truth']))]['note']}",
        "> 把这一臂与下一臂混在一起谈「标签质量敏感性」，会把一个**不敏感的量**说成敏感的。",
        "",
        "### C2 翻转 `per_asset` 判定（检测器噪声）",
        "",
        "| 翻转率 | 翻转格数 | FD 贪心率% | Δpp | Δ 变化 | 盲区率% |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for k, v in c["flip_per_asset_verdict"].items():
        lines.append(f"| {k} | {v['n_cells_flipped']} | {v['greedy_rate_pct']:.2f} | "
                     f"{v['delta_pp']:+.3f} | **{v['delta_change_pp']:+.3f}** | "
                     f"{v['blind_rate_pct']:.2f} |")
    lines += [
        "",
        "## D 臂 · 环境敏感性",
        "",
        "| 臂 | 资产 | catch | miss | unknown | catch% | unknown% | 条件 recall% |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, block in d["arms"].items():
        assets = d["E1_supported"] if name.startswith("E1") else d["E2_supported"]
        for mode in ("unaware", "aware"):
            v = block[mode]
            lines.append(f"| {name} · {mode} | {'/'.join(assets)} | {v['catch']} | {v['miss']} | "
                         f"{v['unknown']} | **{v['catch_rate_pct']:.2f}** | "
                         f"{v['unknown_rate_pct']:.2f} | {v['conditional_recall_pct']} |")
    lines += [
        "",
        f"- **E1 − E2（unaware）Δ = {d['delta_pp_unaware']:.2f}pp**",
        f"- E2 aware 的 unknown 率 = **{d['delta_pp_aware_unknown']:.2f}%**",
        f"- 容器臂：**{'已执行' if d['container_arm']['executed'] else '未执行'}**"
        f"（{d['container_arm']['reason']}）",
        "",
        "## 诚实边界",
        "",
    ]
    lines += [f"- {x}" for x in doc["honest_limits"]]
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
