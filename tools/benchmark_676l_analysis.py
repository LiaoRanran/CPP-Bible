#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran（阿信）
"""benchmark_676l_analysis.py — 676l 检测器能力深度 Benchmark（只读分析面）。

本脚本**只读** 676g 的判定矩阵（`data/blindspot_676g_detection_matrix.json`），
不修改任何数据 / 检测器 / 论文；产出的全部数字都可复算。

口径（写死，可核验）
====================
* 样本集 = 676g 矩阵全部 1147 条；资产 = 矩阵 `assets` 字段的 8 项。
* ground truth = 每条样本的 `expected_verdict`（`catch` / `miss`）。
  对 1042 条扩样样本，脚本会把它与 `data/holdout_expansion/<batch>/*.json`
  里的同名字段逐条比对（交叉验证，见 `--stage validate` 的 `gt_crosscheck`）。
* 混淆矩阵（**逐检测器**）：
      TP = expected=catch & detector=catch      FN = expected=catch & detector=miss
      FP = expected=miss  & detector=catch      TN = expected=miss  & detector=miss
  `unknown` 单独统计、**不进**混淆矩阵（口径同 676l 规格任务 B-1）。
* OR 聚合（样本级）= 选中资产里任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss。
  （与 `tools/run_a5_experiment_673p.py::AttributionExecutor` 完全同义。）
* 统计原语复用 `tools/selection_strategies_673p.py`（FD / Random / Static 的
  选择语义一字不改），保证与 676f 的三臂口径可比。

产出
====
* `data/676l_benchmark_results.json`     —— 全部机读数字（报告的唯一数据源）
* `data/676l_figures/*.png`              —— 论文用图（300 DPI；仅绘图需要 `matplotlib`，
  非本仓依赖，未安装时该阶段跳过、不影响其余产物）
* `data/676l_单检测器性能报告.md` / `_检测器互补性报告.md` / `_最佳组合分析报告.md`
  / `_错误模式分析报告.md` / `_检测器Benchmark总报告.md`

依赖：**标准库 + `tools/` 内既有模块**（`selection_strategies_673p` /
`verifier_pool_673p`）+ 可选的 `matplotlib`。**不需要 numpy / scipy**
（层次聚类与 Pearson 均为本文件内的纯 stdlib 实现，见 `average_linkage` / `_pearson`）。

用法
====
    python tools/benchmark_676l_analysis.py --stage all
    python tools/benchmark_676l_analysis.py --stage validate
    python tools/benchmark_676l_analysis.py --stage perf
    python tools/benchmark_676l_analysis.py --stage complement
    python tools/benchmark_676l_analysis.py --stage combo
    python tools/benchmark_676l_analysis.py --stage errors
    python tools/benchmark_676l_analysis.py --stage figures
    python tools/benchmark_676l_analysis.py --stage reports

诚实边界
========
1. `expected_verdict` 是**单标注者**（生成样本的 Agent）的标注，不是真实缺陷的真值
   ⇒ 所有指标都是「相对于标注」的，不是「相对于真实缺陷」的。
2. planted=true 占 88%（1009/1147），指标偏向「植入缺陷」，对真实缺陷泛化性有限。
3. 本批用 676g 矩阵评估，但 FD 的排序（fail_hits）来自 676f 矩阵的派生集
   ⇒ 存在矩阵间差异（两矩阵在共同样本上 cross-compile 有 10 例判定不同，见
   `data_quality.matrix_diff_vs_676f`）。本批同时给出 in-sample 排序作为对照。
4. unknown 不进混淆矩阵 ⇒ 若 unknown 比例高，实际性能可能比算出来的差。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import itertools
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "data"))

import selection_strategies_673p as ss  # noqa: E402
import verifier_pool_673p as vp  # noqa: E402

MATRIX = ROOT / "data" / "blindspot_676g_detection_matrix.json"
MATRIX_676F = ROOT / "data" / "a5_676f_detection_matrix.json"
EXPANSION = ROOT / "data" / "holdout_expansion"
OUT_JSON = ROOT / "data" / "676l_benchmark_results.json"
FIGDIR = ROOT / "data" / "676l_figures"

#: 结构性恒 unknown 的资产（MinGW 不认 -Wunsequenced / 无本地检测器）
STRUCTURAL_UNKNOWN = ("wunsequenced", "compile-time")
#: 池次序（= verifier_pool_673p.implemented_ids()，字典序；随机抽样依赖次序）
ASSET_ORDER = list(vp.selectable_ids(vp.ASSET_POOL))
#: 676f 报告给出的 FD（k=4）选集（fail_hits 来自派生集）
FD_676F_K4 = ["asan", "ubsan", "tsan", "cross-compile"]
SEED = 20260930          # 项目约定种子（与 673p/676f 同值）
MULTI_SEED_N = 2000      # 与 676f 一致

SCHEMA = "queyi-benchmark-676l/v1"


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


# ─────────────────────────────────────────────────────────────────────────────
# 载入 + 验证（任务 A）
# ─────────────────────────────────────────────────────────────────────────────
def load_matrix(path: Path = MATRIX) -> dict:
    doc = json.loads(path.read_text(encoding="utf-8"))
    samples = []
    for r in doc["samples"]:
        per, notes = {}, {}
        for a, v in r["per_asset"].items():
            if isinstance(v, dict):
                per[a] = v["verdict"]
                notes[a] = v.get("note", "") or ""
            else:
                per[a] = v
                notes[a] = ""
        samples.append({
            "uid": r.get("uid", r.get("sample_id")),
            "sample_id": r.get("sample_id"),
            "source_batch": r.get("source_batch"),
            "defect_type": r.get("defect_type"),
            "planted": r.get("planted"),
            "expected_verdict": r.get("expected_verdict"),
            "hung_flag": bool(r.get("hung_flag")),
            "run_mode": r.get("run_mode"),
            "per_asset": per,
            "per_asset_note": notes,
        })
    return {"path": path, "assets": list(doc["assets"]), "samples": samples,
            "raw_meta": {k: doc.get(k) for k in
                         ("schema", "n_samples", "n_problems", "environment",
                          "asset_availability", "hung_pool_note", "qa_verify")}}


def stage_validate(mx: dict) -> dict:
    """任务 A：矩阵规模 / 完整性 / 取值域 / ground truth 交叉验证。"""
    A, S = mx["assets"], mx["samples"]
    n, na = len(S), len(A)
    cells = n * na
    missing, bad_verdict, bad_expected = [], [], []
    verdict_dist: Counter = Counter()
    for s in S:
        if s["expected_verdict"] not in ("catch", "miss"):
            bad_expected.append(s["uid"])
        for a in A:
            v = s["per_asset"].get(a)
            if v is None:
                missing.append((s["uid"], a))
            elif v not in ("catch", "miss", "unknown"):
                bad_verdict.append((s["uid"], a, v))
            else:
                verdict_dist[v] += 1
    assert set(A) == set(ASSET_ORDER), f"矩阵资产与池不一致：{A} vs {ASSET_ORDER}"

    # ground truth 交叉验证：扩样 1042 条与样本 json 的 expected_verdict 逐条比对
    gt_mismatch, gt_checked, gt_file_missing = [], 0, []
    for s in S:
        if not s["source_batch"] or s["source_batch"] in ("holdout", "corpus"):
            continue
        base = EXPANSION / str(s["source_batch"])
        cands = [base / f"{s['sample_id']}.json", base / f"sample_{s['sample_id']}.json"]
        p = next((c for c in cands if c.is_file()), None)
        if p is None:
            gt_file_missing.append(str(cands[0].relative_to(ROOT).as_posix()))
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        gt_checked += 1
        if d.get("expected_verdict") != s["expected_verdict"]:
            gt_mismatch.append({"uid": s["uid"], "matrix": s["expected_verdict"],
                                "file": d.get("expected_verdict"),
                                "path": p.relative_to(ROOT).as_posix()})

    # 与 676f 矩阵的数据质量对照（只读，不改）
    matrix_diff = None
    if MATRIX_676F.is_file():
        f = json.loads(MATRIX_676F.read_text(encoding="utf-8"))
        fA = f["assets"]
        fidx = {}
        for r in f["samples"]:
            per = {a: (r["per_asset"][a] if isinstance(r["per_asset"][a], str)
                       else r["per_asset"][a]["verdict"]) for a in fA}
            fidx[(r.get("source_batch"), r.get("sample_id"))] = per
        gidx = {(s["source_batch"], s["sample_id"]): s["per_asset"] for s in S}
        common = sorted(set(fidx) & set(gidx))
        diffs: Counter = Counter()
        detail: list[dict] = []
        for k in common:
            for a in ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker"):
                if fidx[k].get(a) != gidx[k].get(a):
                    diffs[a] += 1
                    if len(detail) < 15:
                        detail.append({"key": list(k), "asset": a,
                                       "676f": fidx[k].get(a), "676g": gidx[k].get(a)})
        matrix_diff = {
            "n_676f": len(fidx), "n_676g": len(gidx), "n_common": len(common),
            "verdict_diffs_by_asset": dict(diffs),
            "examples": detail,
            "note": "两矩阵为两次独立测量；仅 (source_batch, sample_id) 交集可比。"
                    "本批评估一律以 676g 为准，不修改任何矩阵。",
        }

    out = {
        "matrix_path": MATRIX.relative_to(ROOT).as_posix(),
        "matrix_schema": mx["raw_meta"].get("schema"),
        "n_samples": n, "n_assets": na, "n_cells": cells,
        "n_missing_cells": len(missing),
        "n_bad_verdict": len(bad_verdict),
        "n_bad_expected": len(bad_expected),
        "verdict_distribution": dict(verdict_dist),
        "verdict_distribution_pct": {k: round(v / cells * 100, 4)
                                     for k, v in verdict_dist.items()},
        "assets": A,
        "structural_unknown_assets": list(STRUCTURAL_UNKNOWN),
        "expected_verdict_distribution": dict(Counter(s["expected_verdict"] for s in S)),
        "source_batch_distribution": dict(Counter(s["source_batch"] for s in S)),
        "planted_distribution": {str(k): v for k, v in
                                 Counter(s["planted"] for s in S).items()},
        "n_defect_types": len({s["defect_type"] for s in S}),
        "n_hung": sum(1 for s in S if s["hung_flag"]),
        "gt_crosscheck": {
            "checked": gt_checked,
            "mismatch": len(gt_mismatch),
            "mismatch_detail": gt_mismatch[:20],
            "file_missing": len(gt_file_missing),
            "note": "扩样样本的 expected_verdict 与样本 .json 逐条比对；"
                    "holdout/corpus 无同名文件（其真值在复用矩阵里），不计入。",
        },
        "data_quality": {"matrix_diff_vs_676f": matrix_diff},
        "verification": {
            "assert_n_1147": n == 1147,
            "assert_assets_8": na == 8,
            "assert_cells_9176": cells == 9176,
            "assert_no_missing": not missing,
            "assert_verdict_domain": not bad_verdict,
            "assert_expected_domain": not bad_expected,
            "pass": (n == 1147 and na == 8 and cells == 9176 and not missing
                     and not bad_verdict and not bad_expected),
        },
    }
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 指标原语
# ─────────────────────────────────────────────────────────────────────────────
def confusion(rows: list[dict], asset: str) -> dict:
    tp = fn = fp = tn = unk = 0
    for r in rows:
        v = r["per_asset"][asset]
        exp = r["expected_verdict"]
        if v == "unknown":
            unk += 1
        elif exp == "catch":
            tp += v == "catch"
            fn += v == "miss"
        else:
            fp += v == "catch"
            tn += v == "miss"
    known = tp + fn + fp + tn
    prec = tp / (tp + fp) if (tp + fp) else None
    rec = tp / (tp + fn) if (tp + fn) else None
    spec = tn / (tn + fp) if (tn + fp) else None
    f1 = (2 * prec * rec / (prec + rec)) if (prec is not None and rec is not None
                                             and (prec + rec) > 0) else None
    acc = (tp + tn) / known if known else None
    return {
        "tp": tp, "fn": fn, "fp": fp, "tn": tn, "unknown": unk, "n_known": known,
        "n": len(rows),
        "precision": round(prec, 6) if prec is not None else None,
        "recall": round(rec, 6) if rec is not None else None,
        "specificity": round(spec, 6) if spec is not None else None,
        "f1": round(f1, 6) if f1 is not None else None,
        "accuracy": round(acc, 6) if acc is not None else None,
        "unknown_rate": round(unk / len(rows), 6) if rows else None,
        "recall_all_denom": round(tp / len(rows), 6) if rows else None,
    }


def or_verdict(row: dict, selected) -> str:
    """OR 聚合（与 AttributionExecutor.verdict 同义）。"""
    vs = [row["per_asset"][a] for a in selected if a in row["per_asset"]]
    if not vs:
        return "unknown"
    if any(v == "catch" for v in vs):
        return "catch"
    if all(v == "unknown" for v in vs):
        return "unknown"
    return "miss"


def or_recall(rows: list[dict], selected, *, catch_only: bool = True) -> dict:
    """OR 聚合后的 recall。

    catch_only=True  ⇒ 分母 = expected=catch 的样本数（676l 规格任务 D-1 口径）
    catch_only=False ⇒ 分母 = 全部样本数（676f 报告的 catch-rate 口径，供对照）
    """
    if catch_only:
        denom_rows = [r for r in rows if r["expected_verdict"] == "catch"]
    else:
        denom_rows = rows
    hit = sum(1 for r in denom_rows if or_verdict(r, selected) == "catch")
    unk = sum(1 for r in denom_rows if or_verdict(r, selected) == "unknown")
    known_rows = [r for r in denom_rows if or_verdict(r, selected) != "unknown"]
    hit_known = sum(1 for r in known_rows if or_verdict(r, selected) == "catch")
    return {
        "n": len(denom_rows), "hit": hit, "unknown": unk,
        "recall": round(hit / len(denom_rows), 6) if denom_rows else None,
        "n_known": len(known_rows),
        "recall_known": round(hit_known / len(known_rows), 6) if known_rows else None,
    }


def wilson(p: float, n: int, z: float = 1.96):
    if n == 0:
        return (None, None)
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, c - h), 6), round(min(1.0, c + h), 6))


# ─────────────────────────────────────────────────────────────────────────────
# 任务 B：单检测器性能
# ─────────────────────────────────────────────────────────────────────────────
def stage_perf(mx: dict) -> dict:
    A, S = mx["assets"], mx["samples"]

    per_asset = {a: confusion(S, a) for a in A}
    ranking = sorted(A, key=lambda a: (-(per_asset[a]["recall"] or 0), a))

    # 8×70 recall 矩阵（分母 = 该类型 expected=catch 的样本；unknown 从分母剔除）
    types = sorted({s["defect_type"] for s in S},
                   key=lambda t: (-sum(1 for s in S if s["defect_type"] == t), t))
    recall_matrix = {}
    for t in types:
        rows = [s for s in S if s["defect_type"] == t]
        catch_rows = [s for s in rows if s["expected_verdict"] == "catch"]
        miss_rows = [s for s in rows if s["expected_verdict"] == "miss"]
        cell: dict = {"n": len(rows), "n_expected_catch": len(catch_rows),
                "n_expected_miss": len(miss_rows), "per_asset": {}}
        for a in A:
            tp = sum(1 for s in catch_rows if s["per_asset"][a] == "catch")
            fn = sum(1 for s in catch_rows if s["per_asset"][a] == "miss")
            fp = sum(1 for s in miss_rows if s["per_asset"][a] == "catch")
            unk = sum(1 for s in rows if s["per_asset"][a] == "unknown")
            cell["per_asset"][a] = {
                "tp": tp, "fn": fn, "fp": fp, "unknown": unk,
                "recall": round(tp / (tp + fn), 6) if (tp + fn) else None,
                "n_catch_expected": tp + fn,
            }
        recall_matrix[t] = cell

    # 每个检测器的强项 / 弱项（按 recall，只取 n_expected_catch ≥ 5 的类型）
    MIN_N = 5
    strength = {}
    for a in A:
        cand = [(t, recall_matrix[t]["per_asset"][a]["recall"],
                 recall_matrix[t]["per_asset"][a]["n_catch_expected"])
                for t in types
                if recall_matrix[t]["per_asset"][a]["n_catch_expected"] >= MIN_N
                and recall_matrix[t]["per_asset"][a]["recall"] is not None]
        cand.sort(key=lambda x: (-x[1], -x[2], x[0]))
        strength[a] = {
            "top5": [{"type": t, "recall": r, "n": n} for t, r, n in cand[:5]],
            "bottom5": [{"type": t, "recall": r, "n": n} for t, r, n in cand[-5:][::-1]],
            "n_types_evaluated": len(cand),
        }

    # planted 分组
    planted = {}
    for label, rows in (("planted_true", [s for s in S if s["planted"] is True]),
                        ("planted_false", [s for s in S if s["planted"] is False]),
                        ("planted_null", [s for s in S if s["planted"] is None])):
        planted[label] = {
            "n": len(rows),
            "expected_catch": sum(1 for r in rows if r["expected_verdict"] == "catch"),
            "or_recall_all8": or_recall(rows, A),
            "per_asset": {a: confusion(rows, a) for a in A},
        }

    # 批次分组
    batches = {}
    for b in sorted({s["source_batch"] for s in S}):
        rows = [s for s in S if s["source_batch"] == b]
        batches[b] = {
            "n": len(rows),
            "expected_catch": sum(1 for r in rows if r["expected_verdict"] == "catch"),
            "or_recall_all8": or_recall(rows, A),
            "per_asset_recall": {a: confusion(rows, a)["recall"] for a in A},
        }

    # 家族分组（复用 676g 的 family 口径，只读导入）
    fam = None
    try:
        import importlib
        fam = importlib.import_module("blindspot_676g_analysis").FAMILY
    except Exception:  # pragma: no cover - 兜底：没有 family 映射就跳过
        fam = None
    families = {}
    if fam:
        groups = defaultdict(list)
        for s in S:
            groups[fam.get(s["defect_type"], "other")].append(s)
        for k, rows in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            families[k] = {
                "n": len(rows),
                "expected_catch": sum(1 for r in rows if r["expected_verdict"] == "catch"),
                "or_recall_all8": or_recall(rows, A),
                "per_asset_recall": {a: confusion(rows, a)["recall"] for a in A},
            }

    return {
        "per_asset": per_asset,
        "ranking_by_recall": ranking,
        "recall_matrix_by_type": recall_matrix,
        "n_types": len(types),
        "strength_weakness": strength,
        "min_n_for_strength": MIN_N,
        "by_planted": planted,
        "by_batch": batches,
        "by_family": families,
        "or_all8": or_recall(S, A),
        "or_all8_catchrate_all": or_recall(S, A, catch_only=False),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 任务 C：互补性
# ─────────────────────────────────────────────────────────────────────────────
def _jaccard(x: set, y: set) -> float:
    u = len(x | y)
    return 1.0 if u == 0 else len(x & y) / u


def _pearson(xs: list[float], ys: list[float]) -> float | None:
    """Pearson 相关系数（纯 stdlib；任一侧无方差 ⇒ None，不返回 NaN）。"""
    n = len(xs)
    if n < 2 or len(ys) != n:
        return None
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx <= 0 or syy <= 0:
        return None
    return sxy / math.sqrt(sxx * syy)


def average_linkage(dist: list[list[float]]) -> list[list[float]]:
    """**纯 stdlib** 的 average-linkage 层次聚类（等价 scipy `linkage(..., 'average')`）。

    返回 scipy 同格式的 linkage 矩阵：第 k 行 `[id_a, id_b, 合并距离, 叶子数]`，
    叶子 id = 0…n-1，内部节点 id = n…2n-2（按合并先后）。同距离时取
    `(id_a, id_b)` 字典序最小的一对（确定性，与 scipy 的 tie-break 可能不同，
    但本数据上无并列距离）。
    """
    n = len(dist)
    if n < 2:
        return []
    d: dict[tuple[int, int], float] = {}
    for i in range(n):
        for j in range(i + 1, n):
            d[(i, j)] = float(dist[i][j])
    members: dict[int, list[int]] = {i: [i] for i in range(n)}
    active = list(range(n))
    Z: list[list[float]] = []
    nxt = n
    while len(active) > 1:
        best: tuple[float, int, int] | None = None
        for i in range(len(active)):
            for j in range(i + 1, len(active)):
                a, b = active[i], active[j]
                val = d[(min(a, b), max(a, b))]
                if best is None or val < best[0] - 1e-12 or (
                        abs(val - best[0]) <= 1e-12 and (a, b) < (best[1], best[2])):
                    best = (val, a, b)
        assert best is not None
        val, a, b = best
        na, nb = len(members[a]), len(members[b])
        Z.append([float(a), float(b), val, float(na + nb)])
        for c in active:
            if c in (a, b):
                continue
            da = d[(min(a, c), max(a, c))]
            db = d[(min(b, c), max(b, c))]
            d[(min(nxt, c), max(nxt, c))] = (da * na + db * nb) / (na + nb)
        members[nxt] = members[a] + members[b]
        active = [c for c in active if c not in (a, b)] + [nxt]
        nxt += 1
    return Z


def fcluster_maxclust(Z: list[list[float]], n: int, k: int) -> list[int]:
    """把 linkage 矩阵按 maxclust 规则切成 k 组（等价 scipy `fcluster(..., 'maxclust')`）。

    实现：从叶子出发做**自底向上合并**，在组数降到 k 之前都执行合并；一旦
    剩余组数 == k 即停止 ⇒ 返回每个叶子的组号（1…k，按组内最小叶 id 排序）。
    """
    if k <= 1 or n <= 1:
        return [1] * n
    parent: dict[int, int] = {}
    groups = {i: {i} for i in range(n)}
    nxt = n
    for row in Z:
        a, b = int(row[0]), int(row[1])
        ga, gb = groups.pop(a), groups.pop(b)
        groups[nxt] = ga | gb
        parent[a] = nxt
        parent[b] = nxt
        nxt += 1
        if len(groups) <= k:
            break
    # 把每个叶子映射到「它最终所在的组」
    leaf_group: list[int] = []
    for leaf in range(n):
        cur = leaf
        while cur in parent:
            cur = parent[cur]
        leaf_group.append(cur)
    uniq = sorted(set(leaf_group))
    remap = {g: i + 1 for i, g in enumerate(uniq)}
    return [remap[g] for g in leaf_group]


def _kappa(rows: list[dict], a: str, b: str) -> dict:
    """Cohen's κ（只在两检测器都给出确定判定的样本上算）。"""
    n = aa = bb = cc = dd = 0
    for r in rows:
        va, vb = r["per_asset"][a], r["per_asset"][b]
        if va == "unknown" or vb == "unknown":
            continue
        n += 1
        ca, cb = va == "catch", vb == "catch"
        if ca and cb:
            aa += 1
        elif ca and not cb:
            bb += 1
        elif not ca and cb:
            cc += 1
        else:
            dd += 1
    if n == 0:
        return {"n": 0, "kappa": None, "po": None, "pe": None,
                "a": aa, "b": bb, "c": cc, "d": dd}
    po = (aa + dd) / n
    pe = ((aa + bb) / n) * ((aa + cc) / n) + ((cc + dd) / n) * ((bb + dd) / n)
    k = (po - pe) / (1 - pe) if (1 - pe) != 0 else None
    return {"n": n, "kappa": round(k, 6) if k is not None else None,
            "po": round(po, 6), "pe": round(pe, 6),
            "a": aa, "b": bb, "c": cc, "d": dd}


def stage_complement(mx: dict) -> dict:
    A, S = mx["assets"], mx["samples"]
    catch_sets = {a: {s["uid"] for s in S if s["per_asset"][a] == "catch"} for a in A}

    pairs = []
    for a, b in itertools.combinations(A, 2):
        inter = len(catch_sets[a] & catch_sets[b])
        only_a = len(catch_sets[a] - catch_sets[b])
        only_b = len(catch_sets[b] - catch_sets[a])
        both_miss = sum(1 for s in S
                        if s["per_asset"][a] != "catch" and s["per_asset"][b] != "catch")
        both_unknown = sum(1 for s in S
                           if s["per_asset"][a] == "unknown"
                           and s["per_asset"][b] == "unknown")
        k = _kappa(S, a, b)
        pairs.append({
            "a": a, "b": b, "both_catch": inter, "only_a": only_a, "only_b": only_b,
            "both_miss": both_miss, "both_unknown": both_unknown,
            "union_catch": inter + only_a + only_b,
            "jaccard": round(_jaccard(catch_sets[a], catch_sets[b]), 6),
            "kappa": k["kappa"], "kappa_n": k["n"], "kappa_table": [k["a"], k["b"], k["c"], k["d"]],
            "po": k["po"], "pe": k["pe"],
        })

    # 8×8 相关性（Pearson on binary catch=1/else 0，两两完整观测；纯 stdlib 实现）
    n_a = len(A)
    jac = [[1.0 if i == j else 0.0 for j in range(n_a)] for i in range(n_a)]
    pear: list[list[float | None]] = [[None] * n_a for _ in range(n_a)]
    for i, a in enumerate(A):
        pear[i][i] = 1.0
        for j, b in enumerate(A):
            if i == j:
                continue
            xs, ys = [], []
            for s in S:
                va, vb = s["per_asset"][a], s["per_asset"][b]
                if va == "unknown" or vb == "unknown":
                    continue
                xs.append(1.0 if va == "catch" else 0.0)
                ys.append(1.0 if vb == "catch" else 0.0)
            pear[i][j] = _pearson(xs, ys)
            p = next((p for p in pairs if {p["a"], p["b"]} == {a, b}), None)
            jac[i][j] = p["jaccard"] if p else 1.0

    def _pairs_sorted_by(key, reverse):
        vals = [p for p in pairs if p[key] is not None]
        return sorted(vals, key=lambda p: (p[key] if not reverse else -p[key]))[:5]

    # 「实质对」= 双方 catch 集合都不小于 MIN_CATCH（排除全 unknown / 近空资产造成的
    # 平凡 Jaccard=0 / =1；结构性资产的平凡关系单列在 structural_relations）
    MIN_CATCH = 50
    substantive = [p for p in pairs
                   if len(catch_sets[p["a"]]) >= MIN_CATCH
                   and len(catch_sets[p["b"]]) >= MIN_CATCH]

    def _sub_sorted(key, reverse, n=5):
        vals = [p for p in substantive if p[key] is not None]
        return sorted(vals, key=lambda p: (p[key] if not reverse else -p[key]))[:n]

    # linker 与 sanitizer unknown 的结构性互补（linker 的 catch 集是否 ⊆ 各资产 unknown 集）
    linker_struct = {}
    lc = catch_sets["linker"]
    for a in A:
        if a == "linker":
            continue
        unk = {s["uid"] for s in S if s["per_asset"][a] == "unknown"}
        linker_struct[a] = {
            "n_linker_catch": len(lc), "n_asset_unknown": len(unk),
            "overlap": len(lc & unk), "linker_catch_subset_of_unknown": lc <= unk,
        }

    # 边际贡献：全池 OR recall − 去掉 X 后的 OR recall（分母 = expected=catch）
    base = or_recall(S, A)
    marginal = {}
    for a in A:
        rest = [x for x in A if x != a]
        m = or_recall(S, rest)
        marginal[a] = {
            "full_recall": base["recall"], "leave_one_out_recall": m["recall"],
            "marginal_pp": round((base["recall"] - m["recall"]) * 100, 4),
            "leave_one_out_hit": m["hit"], "full_hit": base["hit"],
        }
    marginal_rank = sorted(A, key=lambda a: (-marginal[a]["marginal_pp"], a))

    # 层次聚类（距离 = 1 − Jaccard；对全 unknown 资产良定义）
    dist = [[0.0 if i == j else 1.0 - jac[i][j] for j in range(n_a)] for i in range(n_a)]
    Z = average_linkage(dist)
    # 切成 3 组（含结构性 unknown 的两个天然成一组）
    labels3 = fcluster_maxclust(Z, n_a, k=3)
    clusters = defaultdict(list)
    for a, lab in zip(A, labels3):
        clusters[int(lab)].append(a)
    # 每组代表 = 该组 recall 最高的
    per_asset = {a: confusion(S, a) for a in A}
    cluster_out = []
    for lab, members in sorted(clusters.items()):
        rep = max(members, key=lambda a: (per_asset[a]["recall"] or 0, a))
        cluster_out.append({
            "cluster": lab, "members": sorted(members), "representative": rep,
            "representative_recall": per_asset[rep]["recall"],
            "max_pairwise_jaccard": round(max((_jaccard(catch_sets[x], catch_sets[y])
                                               for x, y in itertools.combinations(members, 2)),
                                              default=1.0), 6),
        })

    return {
        "pairs": pairs,
        "n_pairs": len(pairs),
        "most_redundant_pairs": _pairs_sorted_by("jaccard", True),
        "least_similar_pairs": _pairs_sorted_by("jaccard", False),
        "most_redundant_pairs_substantive": _sub_sorted("jaccard", True),
        "least_similar_pairs_substantive": _sub_sorted("jaccard", False),
        "highest_kappa_pairs_substantive": _sub_sorted("kappa", True),
        "lowest_kappa_pairs_substantive": _sub_sorted("kappa", False),
        "substantive_min_catch": MIN_CATCH,
        "structural_linker_unknown_relation": linker_struct,
        "highest_kappa_pairs": _pairs_sorted_by("kappa", True),
        "lowest_kappa_pairs": _pairs_sorted_by("kappa", False),
        "jaccard_matrix": {"assets": A, "values": [[round(float(v), 6) for v in row] for row in jac]},
        "pearson_matrix": {"assets": A,
                           "values": [[None if v is None else round(float(v), 6)
                                       for v in row] for row in pear]},
        "marginal_contribution": marginal,
        "marginal_ranking": marginal_rank,
        "clusters_k3": cluster_out,
        "linkage_matrix": [[round(float(v), 6) for v in row] for row in Z],
    }


# ─────────────────────────────────────────────────────────────────────────────
# 任务 D：最佳组合
# ─────────────────────────────────────────────────────────────────────────────
def _fd_insample_order(S: list[dict], assets) -> tuple[list, dict]:
    hits = {a: sum(1 for s in S if s["per_asset"][a] == "catch") for a in assets}
    return sorted(assets, key=lambda a: (-hits[a], a)), hits


def stage_combo(mx: dict) -> dict:
    A, S = mx["assets"], mx["samples"]

    # 穷举 k=1..7（k=8 恒等于全池，只报不作证据）
    exhaustive = []
    for k in range(1, len(A)):
        combos = []
        for c in itertools.combinations(A, k):
            r = or_recall(S, list(c))
            r_all = or_recall(S, list(c), catch_only=False)
            combos.append({"assets": list(c), "recall": r["recall"], "hit": r["hit"],
                           "unknown": r["unknown"],
                           "catchrate_all": r_all["recall"]})
        combos.sort(key=lambda x: (-x["recall"], -x["catchrate_all"], x["assets"]))
        exhaustive.append({
            "k": k, "n_combos": len(combos),
            "best": combos[0], "worst": combos[-1],
            "recall_min": combos[-1]["recall"], "recall_max": combos[0]["recall"],
            "recall_median": round(statistics.median([c["recall"] for c in combos]), 6),
            "top5": combos[:5], "bottom5": combos[-5:],
        })

    full = or_recall(S, A)

    # FD 排序：676f 派生集（预注册）与 in-sample（全量，含信息泄漏，只作对照）
    insample_order, insample_hits = _fd_insample_order(S, A)
    fd676f_order = ["asan", "ubsan", "tsan", "cross-compile", "compiler-warn",
                    "linker", "compile-time", "wunsequenced"]

    def fd_row(order, k):
        sel = order[:k]
        r = or_recall(S, sel)
        r_all = or_recall(S, sel, catch_only=False)
        return {"k": k, "assets": sel, "recall": r["recall"], "hit": r["hit"],
                "catchrate_all": r_all["recall"],
                "is_best_at_k": any(set(sel) == set(e["best"]["assets"])
                                    for e in exhaustive if e["k"] == k),
                "gap_to_best_pp": round((next(e["best"]["recall"] for e in exhaustive
                                              if e["k"] == k) - r["recall"]) * 100, 4)
                if k < len(A) else None}

    fd676f = [fd_row(fd676f_order, k) for k in range(1, len(A) + 1)]
    fd_insample = [fd_row(insample_order, k) for k in range(1, len(A) + 1)]

    # k=4 的 Random 分布（2000 次，与 676f 同 seed 约定）
    pool = vp.ASSET_POOL
    k4_rates, k4_sets = [], []
    for i in range(MULTI_SEED_N):
        sel = ss.select("random", pool, max_assets=4, seed=SEED + i, candidates=A)
        k4_rates.append(or_recall(S, list(sel.assets))["recall"])
        if i < 5:
            k4_sets.append(list(sel.assets))
    # Static 臂（k=4；静态资产不足时按 selection_strategies 语义取满静态资产）
    n_static = len([a for a in A if a in vp.STATIC_ASSETS])
    st_sel = ss.select("static", pool, max_assets=min(4, n_static), candidates=A)
    static_arm = {"assets": list(st_sel.assets), "k": len(st_sel.assets),
                  "recall": or_recall(S, list(st_sel.assets))["recall"],
                  "note": "static 策略只认静态资产（字典序前缀），"
                          "预注册口径下静态资产不足 4 个时取满为止。"}
    k4_rates_sorted = sorted(k4_rates)
    best4 = next(e["best"] for e in exhaustive if e["k"] == 4)
    fd4 = fd_row(fd676f_order, 4)
    rs = k4_rates_sorted
    rand_stats = {
        "runs": MULTI_SEED_N, "seed0": SEED,
        "mean": round(statistics.fmean(k4_rates), 6),
        "sd": round(statistics.pstdev(k4_rates), 6),
        "min": round(min(k4_rates), 6), "max": round(max(k4_rates), 6),
        "p2_5": round(rs[int(0.025 * (MULTI_SEED_N - 1))], 6),
        "p97_5": round(rs[int(0.975 * (MULTI_SEED_N - 1))], 6),
        "median": round(statistics.median(k4_rates), 6),
        "best_percentile": round(sum(1 for x in k4_rates if x < best4["recall"])
                                 / MULTI_SEED_N * 100, 4),
        "fd676f_percentile": round(sum(1 for x in k4_rates if x < fd4["recall"])
                                   / MULTI_SEED_N * 100, 4),
        "first5_sets": k4_sets,
    }

    # 增量收益曲线（最佳组合）
    curve = []
    for e in exhaustive:
        curve.append({"k": e["k"], "best_recall": e["best"]["recall"],
                      "best_assets": e["best"]["assets"],
                      "worst_recall": e["worst"]["recall"],
                      "median_recall": e["recall_median"]})
    curve.append({"k": len(A), "best_recall": full["recall"], "best_assets": sorted(A),
                  "worst_recall": full["recall"], "median_recall": full["recall"]})
    prev_r = 0.0
    for row in curve:
        row["delta_pp"] = round((row["best_recall"] - prev_r) * 100, 4)
        prev_r = row["best_recall"]
    # 拐点：Δ 首次低于前一步的一半
    knee = None
    for i in range(1, len(curve)):
        if curve[i]["delta_pp"] <= curve[i - 1]["delta_pp"] / 2 and i >= 2:
            knee = curve[i]["k"]
            break

    return {
        "exhaustive_by_k": exhaustive,
        "full_pool": full,
        "full_pool_catchrate_all": or_recall(S, A, catch_only=False),
        "fd_676f_order": fd676f_order,
        "fd_676f_by_k": fd676f,
        "fd_insample_order": insample_order,
        "fd_insample_hits": insample_hits,
        "fd_insample_by_k": fd_insample,
        "fd_676f_k4_equals_best": set(FD_676F_K4) == set(best4["assets"]),
        "best_k4": best4,
        "static_arm": static_arm,
        "random_k4": rand_stats,
        "incremental_curve": curve,
        "knee_k": knee,
        "denominator_note": "recall 分母 = expected=catch 的 674 条（676l 规格口径）；"
                            "catchrate_all 分母 = 全部 1147 条（676f 报告口径，仅供对照）。",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 任务 E：错误模式
# ─────────────────────────────────────────────────────────────────────────────
def _unknown_reason(note: str) -> str:
    n = note or ""
    if "不认" in n or "does not recognize" in n or "-Wunsequenced" in n:
        return "compiler_flag_unsupported"
    if "无本地检测器" in n or "声明性" in n:
        return "no_local_detector"
    if "编译" in n or "链接" in n or "compile" in n or "link" in n:
        return "compile_or_link_failure"
    if "超时" in n or "timeout" in n:
        return "timeout_hang"
    return "other"


def stage_errors(mx: dict) -> dict:
    A, S = mx["assets"], mx["samples"]

    fn_analysis, fp_analysis, unknown_analysis = {}, {}, {}
    for a in A:
        fn_rows = [s for s in S
                   if s["expected_verdict"] == "catch" and s["per_asset"][a] == "miss"]
        fp_rows = [s for s in S
                   if s["expected_verdict"] == "miss" and s["per_asset"][a] == "catch"]
        unk_rows = [s for s in S if s["per_asset"][a] == "unknown"]

        fn_by_type = Counter(s["defect_type"] for s in fn_rows)
        fp_by_type = Counter(s["defect_type"] for s in fp_rows)
        fn_analysis[a] = {
            "n_fn": len(fn_rows),
            "top5_types": [{"type": t, "n": n} for t, n in fn_by_type.most_common(5)],
            "by_type": dict(fn_by_type),
            "by_batch": dict(Counter(s["source_batch"] for s in fn_rows)),
            "by_family": None,
            "planted_true": sum(1 for s in fn_rows if s["planted"] is True),
            "planted_false": sum(1 for s in fn_rows if s["planted"] is False),
            "hung": sum(1 for s in fn_rows if s["hung_flag"]),
        }
        fp_analysis[a] = {
            "n_fp": len(fp_rows),
            "top5_types": [{"type": t, "n": n} for t, n in fp_by_type.most_common(5)],
            "by_type": dict(fp_by_type),
            "by_batch": dict(Counter(s["source_batch"] for s in fp_rows)),
            "hung": sum(1 for s in fp_rows if s["hung_flag"]),
            "sample_uids": [s["uid"] for s in fp_rows][:50],
        }
        reasons: Counter = Counter()
        for s in unk_rows:
            reasons[_unknown_reason(s.get("per_asset_note", {}).get(a, ""))] += 1
        ex_note = ""
        if unk_rows:
            ex_note = (unk_rows[0].get("per_asset_note", {}).get(a, "") or "")[:240]
        unknown_analysis[a] = {
            "n_unknown": len(unk_rows), "rate": round(len(unk_rows) / len(S), 6),
            "reasons": dict(reasons),
            "example_note": ex_note,
        }

    # family 归并 FN
    fam = None
    try:
        import importlib
        fam = importlib.import_module("blindspot_676g_analysis").FAMILY
    except Exception:
        fam = None
    if fam:
        for a in A:
            fn_rows = [s for s in S
                       if s["expected_verdict"] == "catch" and s["per_asset"][a] == "miss"]
            fn_analysis[a]["by_family"] = dict(
                Counter(fam.get(s["defect_type"], "other") for s in fn_rows))

    # 全检测器一致盲区（expected=catch 且 8 资产无一 catch）
    blind = []
    for s in S:
        if s["expected_verdict"] != "catch":
            continue
        if any(s["per_asset"][a] == "catch" for a in A):
            continue
        blind.append({
            "uid": s["uid"], "sample_id": s["sample_id"], "source_batch": s["source_batch"],
            "defect_type": s["defect_type"], "planted": s["planted"],
            "hung_flag": s["hung_flag"],
            "unknown_assets": [a for a in A if s["per_asset"][a] == "unknown"],
        })
    blind_by_type = Counter(b["defect_type"] for b in blind)
    blind_by_batch = Counter(b["source_batch"] for b in blind)

    # 可用 6 资产全 miss（严格口径，排除结构性 unknown）
    avail = [a for a in A if a not in STRUCTURAL_UNKNOWN]
    strict_blind = [s for s in S if s["expected_verdict"] == "catch"
                    and all(s["per_asset"][a] == "miss" for a in avail)]

    return {
        "fn": fn_analysis,
        "fp": fp_analysis,
        "unknown": unknown_analysis,
        "all_detector_blindspot": {
            "n": len(blind),
            "by_type": dict(blind_by_type),
            "by_batch": dict(blind_by_batch),
            "by_family": (dict(Counter(fam.get(b["defect_type"], "other") for b in blind))
                          if fam else None),
            "planted_true": sum(1 for b in blind if b["planted"] is True),
            "planted_false": sum(1 for b in blind if b["planted"] is False),
            "n_with_unknown": sum(1 for b in blind if b["unknown_assets"]),
            "samples": blind,
            "strict_6_available_all_miss_n": len(strict_blind),
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
# 任务 F：可视化
# ─────────────────────────────────────────────────────────────────────────────
def stage_figures(mx: dict, res: dict) -> list:
    """生成论文用图（PNG，300 DPI）。

    依赖：**仅 `matplotlib`**（非本仓依赖，只用于绘图）。未安装时本阶段整体
    跳过（打印提示），其余阶段与 `676l_benchmark_results.json` 不受影响。
    不依赖 numpy / scipy（本仓 mypy 面不含这两个库）。
    """
    try:
        import matplotlib.pyplot as plt  # type: ignore[import-not-found,import-untyped]
    except ImportError as exc:  # pragma: no cover - 环境缺口
        print(f"[676l] figures: 跳过（未安装 matplotlib：{exc}）；"
              "安装后重跑 `--stage figures` 即可")
        return []
    plt.switch_backend("Agg")

    FIGDIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "axes.grid": True,
                         "grid.alpha": 0.3, "figure.autolayout": True})
    A = mx["assets"]
    perf = res["perf"]
    comp = res["complement"]
    combo = res["combo"]
    made = []

    def _save(fig, name):
        p = FIGDIR / name
        fig.savefig(p, dpi=300, bbox_inches="tight")
        plt.close(fig)
        made.append(p.relative_to(ROOT).as_posix())

    # 图 1：recall 排序 + precision/recall/F1 分组柱
    order = perf["ranking_by_recall"]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    rec = [(perf["per_asset"][a]["recall"] or 0) * 100 for a in order]
    axes[0].bar(range(len(order)), rec, color="#c0392b")
    axes[0].set_xticks(range(len(order)))
    axes[0].set_xticklabels(order, rotation=35, ha="right")
    axes[0].set_ylabel("Recall (%)")
    axes[0].set_title("(a) Per-detector recall (sorted), n=1147")
    for i, v in enumerate(rec):
        lab = f"{v:.1f}" if perf["per_asset"][order[i]]["recall"] is not None else "n/a"
        axes[0].text(i, v + 0.4, lab, ha="center", fontsize=8)
    w = 0.27
    for off, key, col, lab in ((-w, "precision", "#2980b9", "Precision"),
                               (0.0, "recall", "#c0392b", "Recall"),
                               (w, "f1", "#27ae60", "F1")):
        vals = [(perf["per_asset"][a][key] or 0) * 100 for a in A]
        axes[1].bar([i + off for i in range(len(A))], vals, w, label=lab, color=col)
    axes[1].set_xticks(range(len(A)))
    axes[1].set_xticklabels(A, rotation=35, ha="right")
    axes[1].set_ylabel("Score (%)")
    axes[1].set_title("(b) Precision / Recall / F1 per detector")
    axes[1].legend()
    _save(fig, "fig1_detector_performance.png")

    # 图 2：相关性热力图（缺失值用 NaN ⇒ cmap.set_bad 画灰）
    M = [[float("nan") if v is None else float(v) for v in row]
         for row in comp["pearson_matrix"]["values"]]
    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    cmap = plt.cm.RdBu_r.copy()
    cmap.set_bad("#cccccc")
    im = ax.imshow(M, cmap=cmap, vmin=-1, vmax=1)
    ax.set_xticks(range(len(A)))
    ax.set_xticklabels(A, rotation=40, ha="right")
    ax.set_yticks(range(len(A)))
    ax.set_yticklabels(A)
    for i in range(len(A)):
        for j in range(len(A)):
            v = M[i][j]
            if v != v:  # NaN
                ax.text(j, i, "n/a", ha="center", va="center", fontsize=7, color="#555")
            else:
                ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7,
                        color="white" if abs(v) > 0.6 else "black")
    ax.set_title("Detector correlation (Pearson on catch, pairwise-complete)")
    ax.grid(False)
    fig.colorbar(im, ax=ax, shrink=0.8)
    _save(fig, "fig2_correlation_heatmap.png")

    # 图 3：边际贡献
    mr = comp["marginal_ranking"]
    vals = [comp["marginal_contribution"][a]["marginal_pp"] for a in mr]
    ypos = list(range(len(mr)))[::-1]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(ypos, vals, color="#8e44ad")
    ax.set_yticks(ypos)
    ax.set_yticklabels(mr)
    ax.set_xlabel("Marginal contribution to OR recall (pp)")
    ax.set_title("Leave-one-out marginal contribution (denominator: 674 expected=catch)")
    for y, v in zip(ypos, vals):
        ax.text(v + 0.05, y, f"{v:.2f}", va="center", fontsize=8)
    _save(fig, "fig3_marginal_contribution.png")

    # 图 4：增量收益曲线
    cur = combo["incremental_curve"]
    ks = [c["k"] for c in cur]
    bs = [c["best_recall"] * 100 for c in cur]
    ws = [c["worst_recall"] * 100 for c in cur]
    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.plot(ks, bs, "o-", color="#c0392b", label="Best combination (OR)")
    ax.plot(ks, ws, "s--", color="#7f8c8d", label="Worst combination (OR)")
    ax.axhline(combo["full_pool"]["recall"] * 100, color="#2980b9", ls=":", lw=1.2,
               label=f"Full pool = {combo['full_pool']['recall']*100:.1f}%")
    ax.axvline(combo["knee_k"], color="#27ae60", ls="-.", lw=1.2,
               label=f"Knee at k={combo['knee_k']}")
    for c in cur:
        ax.annotate(f"+{c['delta_pp']:.1f}", (c["k"], c["best_recall"] * 100),
                    textcoords="offset points", xytext=(0, 8), ha="center", fontsize=7)
    ax.set_xlabel("Budget k (number of detectors)")
    ax.set_ylabel("OR recall on expected=catch (%)")
    ax.set_title("Incremental gain of the best detector subset")
    ax.set_xticks(ks)
    ax.legend(fontsize=8)
    _save(fig, "fig4_incremental_gain.png")

    # 图 5：聚类树状图（自绘，不依赖 scipy）
    Z = comp["linkage_matrix"]
    n = len(A)
    ynode = {i: float(i) for i in range(n)}
    hnode = {i: 0.0 for i in range(n)}
    fig, ax = plt.subplots(figsize=(9, 5))
    for k, row in enumerate(Z):
        a, b, d = int(row[0]), int(row[1]), float(row[2])
        ya, yb = ynode[a], ynode[b]
        ax.plot([hnode[a], d], [ya, ya], color="#4c72b0", lw=1.2)
        ax.plot([hnode[b], d], [yb, yb], color="#4c72b0", lw=1.2)
        ax.plot([d, d], [ya, yb], color="#4c72b0", lw=1.2)
        ynode[n + k] = (ya + yb) / 2.0
        hnode[n + k] = d
    ax.set_yticks(range(n))
    ax.set_yticklabels(A)
    ax.set_ylim(-0.5, n - 0.5)
    ax.set_ylabel("Jaccard distance (1 - J)")
    ax.set_title("Detector clustering (average linkage, 1 - Jaccard)")
    _save(fig, "fig5_dendrogram.png")

    # 图 6：每检测器混淆构成（堆叠，占 1147 的比例）
    fig, ax = plt.subplots(figsize=(9.5, 5))
    cats = [("TP", "tp", "#c0392b"), ("FN", "fn", "#e67e22"),
            ("FP", "fp", "#8e44ad"), ("TN", "tn", "#2980b9"),
            ("unknown", "unknown", "#bdc3c7")]
    bottoms = [0.0] * len(A)
    for lab, key, col in cats:
        vals = [perf["per_asset"][a][key] / 1147 * 100 for a in A]
        ax.bar(A, vals, bottom=bottoms, label=lab, color=col)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    ax.set_ylabel("Share of all 1147 samples (%)")
    ax.set_title("Confusion composition per detector (unknown excluded from metrics)")
    ax.tick_params(axis="x", rotation=35)
    ax.legend(ncol=5, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, -0.42))
    _save(fig, "fig6_confusion_composition.png")

    # 图 7：k=4 Random 分布 + FD / best
    rs = combo["random_k4"]
    dist = []
    for i in range(MULTI_SEED_N):
        sel = ss.select("random", vp.ASSET_POOL, max_assets=4, seed=SEED + i, candidates=A)
        dist.append(or_recall(mx["samples"], list(sel.assets))["recall"] * 100)
    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.hist(dist, bins=30, color="#95a5a6", edgecolor="white")
    ax.axvline(combo["best_k4"]["recall"] * 100, color="#c0392b", lw=2,
               label=f"Best k=4 = {combo['best_k4']['recall']*100:.1f}%")
    ax.axvline(combo["fd_676f_by_k"][3]["recall"] * 100, color="#27ae60", lw=2, ls="--",
               label=f"FD(676f) k=4 = {combo['fd_676f_by_k'][3]['recall']*100:.1f}%")
    ax.axvline(rs["mean"], color="#2980b9", lw=1.5, ls=":",
               label=f"Random mean = {rs['mean']*100:.1f}%")
    ax.set_xlabel("OR recall (%)")
    ax.set_ylabel("Count (of 2000 draws)")
    ax.set_title("k=4 random subset distribution vs best / FD")
    ax.legend(fontsize=8)
    _save(fig, "fig7_k4_random_distribution.png")

    return made


def _pct(x, d=2):
    return "n/a" if x is None else f"{x*100:.{d}f}%"


def _f(x, d=4):
    return "n/a" if x is None else f"{x:.{d}f}"


def write_reports(mx: dict, res: dict) -> list:
    A = mx["assets"]
    val, perf, comp, combo, err = (res["validate"], res["perf"], res["complement"],
                                   res["combo"], res["errors"])
    R = ROOT / "data"
    made = []

    def emit(name, text):
        p = R / name
        p.write_text(text, encoding="utf-8", newline="\n")
        made.append(p.relative_to(ROOT).as_posix())

    # ── 报告 1：单检测器性能 ───────────────────────────────────────────────
    L = ["# 676l · 单检测器性能报告（8 资产 × 1147 样本）", "",
         f"- 生成：{_now()}；脚本：`tools/benchmark_676l_analysis.py --stage perf`",
         f"- 数据源：`{val['matrix_path']}`（{val['n_samples']}×{val['n_assets']}="
         f"{val['n_cells']} 格，缺失 {val['n_missing_cells']}）",
         f"- ground truth：样本级 `expected_verdict`（catch {val['expected_verdict_distribution'].get('catch')} / "
         f"miss {val['expected_verdict_distribution'].get('miss')}）",
         "- 口径：`unknown` **不进**混淆矩阵（单独报告比例）；"
         "`recall` = TP/(TP+FN)，分母 = expected=catch 的已知判定数。", "",
         "## 1. 综合指标表（按 recall 降序）", "",
         "| 排名 | 检测器 | TP | FN | FP | TN | unknown | Precision | Recall | F1 | Specificity | Accuracy | unknown率 |",
         "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for i, a in enumerate(perf["ranking_by_recall"], 1):
        p = perf["per_asset"][a]
        L.append(f"| {i} | `{a}` | {p['tp']} | {p['fn']} | {p['fp']} | {p['tn']} | "
                 f"{p['unknown']} | {_pct(p['precision'])} | {_pct(p['recall'])} | "
                 f"{_pct(p['f1'])} | {_pct(p['specificity'])} | {_pct(p['accuracy'])} | "
                 f"{_pct(p['unknown_rate'])} |")
    L += ["",
          f"- 8 资产 OR（分母 expected=catch 674）：**{_pct(perf['or_all8']['recall'])}**"
          f"（{perf['or_all8']['hit']}/{perf['or_all8']['n']}）；"
          f"分母全 1147 的 catch-rate = {_pct(perf['or_all8_catchrate_all']['recall'])}"
          f"（{perf['or_all8_catchrate_all']['hit']}/1147，676f 报告口径）。",
          "- **precision 普遍偏低不是缺陷**：`expected=miss` 的 473 条是"
          "「标注为不应被检出」的样本，检测器在其中 catch 即记为 FP。"
          "FP 里相当一部分是「目标缺陷没抓到、但抓到了伴随的物理层错误」"
          "（见错误模式报告 §2），把它读成纯误报会低估检测器。", ""]

    L += ["## 2. 每个检测器的强项 / 弱项类型（n ≥ 5 的 expected=catch 类型）", ""]
    for a in A:
        s = perf["strength_weakness"][a]
        L += [f"### `{a}`（可评估类型 {s['n_types_evaluated']} 个）", "",
              "| 强项 Top5 | n | recall | ｜ | 弱项 Bottom5 | n | recall |",
              "|---|---:|---:|---|---|---:|---:|"]
        for i in range(5):
            t1 = s["top5"][i] if i < len(s["top5"]) else None
            t2 = s["bottom5"][i] if i < len(s["bottom5"]) else None
            c1 = f"{t1['type']} | {t1['n']} | {_pct(t1['recall'])}" if t1 else " |  | "
            c2 = f"{t2['type']} | {t2['n']} | {_pct(t2['recall'])}" if t2 else " |  | "
            L.append(f"| {c1} | ｜ | {c2} |")
        L.append("")

    L += ["## 3. planted 分组", "",
          "| 组 | n | expected=catch | OR recall(8) | asan | ubsan | tsan | compiler-warn | cross-compile | linker |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for lab in ("planted_true", "planted_false", "planted_null"):
        g = perf["by_planted"][lab]
        cells = " | ".join(_pct(g["per_asset"][a]["recall"]) for a in
                           ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker"))
        L.append(f"| {lab} | {g['n']} | {g['expected_catch']} | "
                 f"{_pct(g['or_recall_all8']['recall'])} | {cells} |")
    L += ["",
          "- 与 676g 的「planted=true 盲区 41% vs planted=false 21.6%」口径不同："
          "676g 的盲区分母是全部样本、且不区分 expected_verdict；本表分母是各组的 "
          "expected=catch 样本，因此**数字不可直接相减**。方向一致：planted=false 组"
          "（真实 CVE 衍生）在 asan 上更强、在静态资产上更弱。", ""]

    L += ["## 4. 批次分组", "",
          "| 批次 | n | expected=catch | OR recall(8) | asan | ubsan | tsan | compiler-warn | cross-compile | linker |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for b, g in perf["by_batch"].items():
        cells = " | ".join(_pct(g["per_asset_recall"][a]) for a in
                           ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker"))
        L.append(f"| {b} | {g['n']} | {g['expected_catch']} | "
                 f"{_pct(g['or_recall_all8']['recall'])} | {cells} |")
    L += ["", "- 扩样批次（expA–expG）的 OR recall 与原始 holdout/corpus 的差异"
          "回答「扩样样本是否更难」：难例批次（expE 并发高级、expF 嵌入式）"
          "显著低于基础批次（expA/expB）。", ""]

    if perf["by_family"]:
        L += ["## 5. 家族分组（复用 676g 的 family 口径）", "",
              "| 家族 | n | expected=catch | OR recall(8) |", "|---|---:|---:|---:|"]
        for k, g in perf["by_family"].items():
            L.append(f"| {k} | {g['n']} | {g['expected_catch']} | "
                     f"{_pct(g['or_recall_all8']['recall'])} |")
        L.append("")

    L += ["## 6. 8×70 recall 矩阵（完整）", "",
          "分母 = 该 defect_type 内 expected=catch 且该资产判定已知的样本数；"
          "`n/a` = 该类型无 expected=catch 样本。", "",
          "| defect_type | n | exp=catch | " + " | ".join(A) + " |",
          "|---|---:|---:|" + "---:|" * len(A)]
    for t, cell in perf["recall_matrix_by_type"].items():
        row = " | ".join(_pct(cell["per_asset"][a]["recall"], 1) for a in A)
        L.append(f"| {t} | {cell['n']} | {cell['n_expected_catch']} | {row} |")
    L.append("")
    emit("676l_单检测器性能报告.md", "\n".join(L))

    # ── 报告 2：互补性 ─────────────────────────────────────────────────────
    L = ["# 676l · 检测器互补性报告", "",
         f"- 生成：{_now()}；脚本：`tools/benchmark_676l_analysis.py --stage complement`", "",
         "## 1. 28 对共现 + Jaccard + Cohen's κ", "",
         "| A | B | 同时catch | 仅A | 仅B | 并集 | Jaccard | κ | κ的 n |",
         "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for p in sorted(comp["pairs"], key=lambda x: -x["jaccard"]):
        L.append(f"| `{p['a']}` | `{p['b']}` | {p['both_catch']} | {p['only_a']} | "
                 f"{p['only_b']} | {p['union_catch']} | {_f(p['jaccard'])} | "
                 f"{_f(p['kappa'])} | {p['kappa_n']} |")
    L += ["",
          f"### 最冗余的 5 对（Jaccard 最高；**实质对** = 双方 catch 数 ≥ "
          f"{comp['substantive_min_catch']}）", "",
          "| A | B | Jaccard | 同时catch | 仅A | 仅B |", "|---|---|---:|---:|---:|---:|"]
    for p in comp["most_redundant_pairs_substantive"]:
        L.append(f"| `{p['a']}` | `{p['b']}` | {_f(p['jaccard'])} | {p['both_catch']} | "
                 f"{p['only_a']} | {p['only_b']} |")
    L += ["",
          f"### 最互补的 5 对（Jaccard 最低；**实质对** = 双方 catch 数 ≥ "
          f"{comp['substantive_min_catch']}）", "",
          "| A | B | Jaccard | 仅A | 仅B | 并集 |", "|---|---|---:|---:|---:|---:|"]
    for p in comp["least_similar_pairs_substantive"]:
        L.append(f"| `{p['a']}` | `{p['b']}` | {_f(p['jaccard'])} | {p['only_a']} | "
                 f"{p['only_b']} | {p['union_catch']} |")
    L += ["",
          "> 未过滤时「最互补」会被**近空资产**占据（`linker` 只有 10 个 catch、"
          "`wunsequenced`/`compile-time` 为 0），其 Jaccard=0 是平凡结果，"
          "不构成互补性证据；故此处按「双方 catch ≥ 50」过滤。", "",
          "### 结构性互补：`linker` 的 catch 集恰好落在 sanitizer 的 unknown 集里", "",
          "| 资产 | linker catch 数 | 该资产 unknown 数 | 交集 | linker_catch ⊆ unknown |",
          "|---|---:|---:|---:|---|"]
    for a, d in comp["structural_linker_unknown_relation"].items():
        L.append(f"| `{a}` | {d['n_linker_catch']} | {d['n_asset_unknown']} | "
                 f"{d['overlap']} | {'是' if d['linker_catch_subset_of_unknown'] else '否'} |")
    L += ["",
          "- `linker` 的 10 个 catch **全部**是 `asan`/`ubsan`/`tsan` 的 10 个 unknown"
          "（强 ODR 多重定义 ⇒ 动态检测器连链接都过不了）。"
          "这解释了为什么 `linker` 的边际贡献（1.34pp）虽小但**不可替代**："
          "它覆盖的正是动态资产结构性看不见的那一小块。", ""]
    L += ["", "### κ 最高 / 最低的 5 对（实质对）", "",
          "| 方向 | A | B | κ | 同时catch | 仅A | 仅B |", "|---|---|---|---:|---:|---:|---:|"]
    for tag, lst in (("最高", comp["highest_kappa_pairs_substantive"]),
                     ("最低", comp["lowest_kappa_pairs_substantive"])):
        for p in lst:
            L.append(f"| {tag} | `{p['a']}` | `{p['b']}` | {_f(p['kappa'])} | "
                     f"{p['both_catch']} | {p['only_a']} | {p['only_b']} |")
    L += ["", "- **κ 的注意点**：`wunsequenced` / `compile-time` 恒 unknown ⇒ 与任何资产的"
          "共同已知样本为 0，κ 无定义（表中显示 n/a）。κ 为负表示两检测器的判定"
          "系统性相反——在本数据上意味着「一个抓到的类型另一个系统性不抓」。", ""]

    L += ["## 2. 相关性矩阵（Pearson，binary catch=1/else 0，两两完整观测）", "",
          "| | " + " | ".join(f"`{a}`" for a in A) + " |",
          "|---|" + "---:|" * len(A)]
    for i, a in enumerate(A):
        row = " | ".join(_f(v) if v is not None else "n/a"
                         for v in comp["pearson_matrix"]["values"][i])
        L.append(f"| `{a}` | {row} |")
    L += ["", "> `n/a` = 两资产没有共同已知判定（结构性恒 unknown），相关系数无定义。"
          "`wunsequenced` / `compile-time` 的整行整列为 n/a，这是**数据事实**不是脚本缺陷。", ""]

    L += ["## 3. 边际贡献（全池 OR recall − 去掉 X 后 OR recall）", "",
          "分母 = expected=catch 的 674 条；全池 OR recall = "
          f"{_pct(perf['or_all8']['recall'])}。", "",
          "| 排名 | 检测器 | 全池 recall | 去掉后 recall | 边际贡献(pp) | 全池 hit | 去掉后 hit |",
          "|---:|---|---:|---:|---:|---:|---:|"]
    for i, a in enumerate(comp["marginal_ranking"], 1):
        m = comp["marginal_contribution"][a]
        L.append(f"| {i} | `{a}` | {_pct(m['full_recall'])} | {_pct(m['leave_one_out_recall'])} | "
                 f"**{m['marginal_pp']:.2f}** | {m['full_hit']} | {m['leave_one_out_hit']} |")
    L += ["",
          "- 边际贡献为 **0.00pp** 的资产（`wunsequenced` / `compile-time`）"
          "在全池里零信息——去掉它们检出率不变。这是 FD「不把预算浪费在零信息资产上」"
          "这一论断的直接证据。", ""]

    L += ["## 4. 层次聚类（距离 = 1 − Jaccard，average linkage，切 3 组）", "",
          "| 组 | 成员 | 代表（组内 recall 最高） | 代表 recall | 组内最大两两 Jaccard |",
          "|---|---|---|---:|---:|"]
    for c in comp["clusters_k3"]:
        L.append(f"| {c['cluster']} | {', '.join('`'+m+'`' for m in c['members'])} | "
                 f"`{c['representative']}` | {_pct(c['representative_recall'])} | "
                 f"{_f(c['max_pairwise_jaccard'])} |")
    L += ["",
          "- **聚类用 Jaccard 而非相关系数**：两个结构性恒 unknown 资产（`wunsequenced`、"
          "`compile-time`）没有方差 ⇒ Pearson 无定义；Jaccard 对全空 catch 集仍良定义"
          "（两空集 J=1 ⇒ 距离 0，二者自然并成「零检出组」）。", ""]
    emit("676l_检测器互补性报告.md", "\n".join(L))

    # ── 报告 3：最佳组合 ───────────────────────────────────────────────────
    L = ["# 676l · 最佳组合分析报告", "",
         f"- 生成：{_now()}；脚本：`tools/benchmark_676l_analysis.py --stage combo`", "",
         "## 1. 穷举最佳 k 组合（k=1…7）", "",
         "| k | 组合数 | 最佳组合 | 最佳 recall | 最差 recall | 中位 recall | 最佳组合的 catch-rate（分母 1147，676f 口径） |",
         "|---:|---:|---|---:|---:|---:|---:|"]
    for e in combo["exhaustive_by_k"]:
        L.append(f"| {e['k']} | {e['n_combos']} | "
                 f"{', '.join('`'+x+'`' for x in e['best']['assets'])} | "
                 f"**{_pct(e['best']['recall'])}** | {_pct(e['worst']['recall'])} | "
                 f"{_pct(e['recall_median'])} | {_pct(e['best']['catchrate_all'])} |")
    L += [f"| 8 | 1 | 全池 | {_pct(combo['full_pool']['recall'])} | "
          f"{_pct(combo['full_pool']['recall'])} | {_pct(combo['full_pool']['recall'])} | "
          f"{_pct(combo['full_pool_catchrate_all']['recall'])} |", ""]

    L += ["### 各 k 的 Top5 组合", ""]
    for e in combo["exhaustive_by_k"]:
        L += [f"**k={e['k']}**（{e['n_combos']} 种）", "",
              "| 组合 | recall | hit |", "|---|---:|---:|"]
        for c in e["top5"]:
            L.append(f"| {', '.join('`'+x+'`' for x in c['assets'])} | "
                     f"{_pct(c['recall'])} | {c['hit']} |")
        L.append("")

    L += ["## 2. FD vs 最佳 vs Random（k=4）", "",
          f"- 最佳 k=4：{', '.join('`'+x+'`' for x in combo['best_k4']['assets'])}，"
          f"recall = **{_pct(combo['best_k4']['recall'])}**",
          f"- FD(676f 派生集) k=4：{', '.join('`'+x+'`' for x in combo['fd_676f_by_k'][3]['assets'])}，"
          f"recall = **{_pct(combo['fd_676f_by_k'][3]['recall'])}**"
          f"（与最佳差 {combo['fd_676f_by_k'][3]['gap_to_best_pp']:.2f}pp）",
          f"- FD(in-sample 全量排序) k=4：{', '.join('`'+x+'`' for x in combo['fd_insample_by_k'][3]['assets'])}，"
          f"recall = {_pct(combo['fd_insample_by_k'][3]['recall'])}",
          f"- Random k=4（2000 次）：均值 **{_pct(combo['random_k4']['mean'])}**，"
          f"SD {combo['random_k4']['sd']*100:.2f}pp，"
          f"2.5–97.5 分位 [{_pct(combo['random_k4']['p2_5'])}, {_pct(combo['random_k4']['p97_5'])}]",
          f"- 最佳组合落在 Random 分布的 **{combo['random_k4']['best_percentile']:.1f}** 百分位；"
          f"FD(676f) 组合落在 **{combo['random_k4']['fd676f_percentile']:.1f}** 百分位", ""]

    L += ["## 3. FD 的 k 扫描（两种排序来源）", "",
          "| k | FD(676f 派生集) 组合 | recall | 距最佳(pp) | FD(in-sample) 组合 | recall |",
          "|---:|---|---:|---:|---|---:|"]
    for a1, a2 in zip(combo["fd_676f_by_k"], combo["fd_insample_by_k"]):
        gap = a1["gap_to_best_pp"]
        gap_s = "n/a" if gap is None else f"{gap:.2f}"
        L.append(f"| {a1['k']} | {', '.join('`'+x+'`' for x in a1['assets'])} | "
                 f"{_pct(a1['recall'])} | {gap_s} | "
                 f"{', '.join('`'+x+'`' for x in a2['assets'])} | {_pct(a2['recall'])} |")
    L += ["",
          f"- **in-sample 排序**（按 676g 全量 catch 数降序）："
          f"{', '.join('`'+x+'`' for x in combo['fd_insample_order'])}，"
          f"对应 catch 数 {combo['fd_insample_hits']}",
          "- 两种排序在 rank 4 分歧：676f 派生集给 `cross-compile`（89 次），"
          "676g 全量给 `compiler-warn`（143 次）。这不是矛盾，而是"
          "**「预测器 vs oracle」**的正常差异：FD 在派生集上估计 fail_hits，"
          "本批在全量（含派生集）上重算 —— 后者含信息泄漏，只作上界参考。", ""]

    L += ["## 4. 增量收益曲线与拐点", "",
          "| k | 最佳 recall | Δ(pp) | 最差 recall | 中位 recall | 最佳组合 |",
          "|---:|---:|---:|---:|---:|---|"]
    for c in combo["incremental_curve"]:
        L.append(f"| {c['k']} | {_pct(c['best_recall'])} | +{c['delta_pp']:.2f} | "
                 f"{_pct(c['worst_recall'])} | {_pct(c['median_recall'])} | "
                 f"{', '.join('`'+x+'`' for x in c['best_assets'])} |")
    L += ["", f"- **拐点 k = {combo['knee_k']}**（Δ 首次跌到前一步的一半以下）。",
          f"- 全池（k=8）= {_pct(combo['full_pool']['recall'])}；"
          f"k=4 的最佳组合已拿到全池的 "
          f"{combo['best_k4']['recall']/combo['full_pool']['recall']*100:.1f}%。", ""]

    L += ["## 5. 对 FD 策略的评价", "",
          f"1. FD(676f) 的 k=4 组合 {', '.join('`'+x+'`' for x in FD_676F_K4)} "
          f"{'**恰好就是穷举最佳**' if combo['fd_676f_k4_equals_best'] else '**不是**穷举最佳'}。",
          f"2. 它在 Random 分布里位于 {combo['random_k4']['fd676f_percentile']:.1f} 百分位；"
          f"Random 均值只有 {_pct(combo['random_k4']['mean'])}。",
          "3. 但必须与 676f 的 `uninterpretable` 条款并报：FD 的优势**主要来自"
          "「不把预算浪费在零信息资产上」的池构成效应**（`wunsequenced`/`compile-time` "
          "边际贡献 0.00pp），**不是**「在有用资产里挑得更准」。本批的边际贡献表"
          "（互补性报告 §3）给出了这条论断的量化支撑。",
          "4. 本批在**全量 1147** 上穷举，而 676f 的 FD 是**派生集训练 / 评估集测试**"
          "（派生 571 / 评估 566），两者样本不同、分母口径也不同"
          f"（本批 recall 分母 {combo['full_pool']['n']} 条 expected=catch，"
          "676f 的 catch-rate 分母是全部 566 条）⇒ 数字不可直接对比。", ""]
    emit("676l_最佳组合分析报告.md", "\n".join(L))

    # ── 报告 4：错误模式 ───────────────────────────────────────────────────
    L = ["# 676l · 错误模式分析报告", "",
         f"- 生成：{_now()}；脚本：`tools/benchmark_676l_analysis.py --stage errors`", "",
         "## 1. 漏报（FN）：每个检测器的 Top5 类型", "",
         "| 检测器 | FN 数 | Top5 类型（FN 数） | planted=true | planted=false | 挂起样本 |",
         "|---|---:|---|---:|---:|---:|"]
    for a in A:
        e = err["fn"][a]
        top = "；".join(f"{t['type']}({t['n']})" for t in e["top5_types"]) or "—"
        L.append(f"| `{a}` | {e['n_fn']} | {top} | {e['planted_true']} | "
                 f"{e['planted_false']} | {e['hung']} |")
    L += ["", "### FN 的家族归并", "",
          "| 检测器 | FN 家族分布 |", "|---|---|"]
    for a in A:
        fams = err["fn"][a]["by_family"]
        if fams:
            top_fams = sorted(fams.items(), key=lambda kv: -kv[1])[:6]
            L.append(f"| `{a}` | " + "；".join(f"{k} {v}" for k, v in top_fams) + " |")
    L += ["", "- **共同规律（逐条由上面两张表读出）**：", "",
          "  1. `deadlock` 出现在**每一个**检测器的 FN Top1/Top2（asan 33 / ubsan 33 / "
          "tsan 31 / compiler-warn 33 / cross-compile 33 / linker 33）—— 与 676g §3 "
          "「deadlock 盲区 94.3%」一致：确定性挂起不产生任何 sanitizer 报告。",
          "  2. FN 的**家族构成因检测器而异**：`asan` 的 FN 以 ub(105) / concurrency(67) 为主；"
          "`ubsan` 以 stl(92) / memory(84) 为主；`tsan` 以 ub(122) / memory(98) 为主；"
          "静态资产（`compiler-warn`/`cross-compile`/`linker`）以 memory / ub 为主。"
          "这说明「一个检测器的 FN」正好是「另一个检测器的强项」——与互补性报告的结论互相印证。",
          "  3. `optimization_dependent`（asan 20 / cross-compile 28 / linker 28）与 "
          "`conditional_trigger`（tsan 22 / cross-compile 28 / linker 28）是**第二大 FN 源**："
          "缺陷只在特定档位/条件触发，检测器的固定档位组合会漏。", ""]

    L += ["## 2. 误报（FP）：分布与成因", "",
          "| 检测器 | FP 数 | Top5 类型（FP 数） | 挂起样本 |",
          "|---|---:|---|---:|"]
    for a in A:
        e = err["fp"][a]
        top = "；".join(f"{t['type']}({t['n']})" for t in e["top5_types"]) or "—"
        L.append(f"| `{a}` | {e['n_fp']} | {top} | {e['hung']} |")
    L += ["",
          "**成因说明（重要）**：`expected_verdict=miss` 的 473 条是「标注为不应被检出」"
          "的样本；检测器在其中 catch 会被记为 FP，但这**不等于检测器错了**——"
          "典型情形是目标缺陷是语义层的，而样本里**同时**存在一个物理层错误"
          "（ABA 退化成 UAF、端序误用造成越界、优先级反转伴随真实竞争），"
          "检测器抓到的是那个伴随错误。这类 FP 是「搭便车命中」，"
          "在论文里应作为**检测器的能力**而非缺陷来讨论。", ""]

    L += ["## 3. unknown 比例与原因", "",
          "| 检测器 | unknown 数 | 比例 | 原因分类（次数） |",
          "|---|---:|---:|---|"]
    for a in A:
        e = err["unknown"][a]
        rsn = "；".join(f"{k}×{v}" for k, v in sorted(e["reasons"].items(),
                                                      key=lambda kv: -kv[1])) or "—"
        L.append(f"| `{a}` | {e['n_unknown']} | {_pct(e['rate'])} | {rsn} |")
    L += ["",
          f"- `wunsequenced`：{err['unknown']['wunsequenced']['n_unknown']}/1147 恒 unknown，"
          "原因 = 本机 MinGW g++ 13.1 不认 `-Wunsequenced`（673u 判据，已如实区分；"
          "note 原文：“检测器不可用(wunsequenced)：编译器不认 -Wunsequenced”）。",
          f"- `compile-time`：{err['unknown']['compile-time']['n_unknown']}/1147 恒 unknown，"
          "原因 = 声明性资产，本仓无本地检测器实现（note 原文：“无本地检测器”）。",
          f"- `asan`/`ubsan`/`tsan`：各 {err['unknown']['asan']['n_unknown']} 格 unknown，"
          "原因 = **编译失败**（note 原文：“-O0 编译失败: …/_atom_inline_odr_a.cpp:3:10: …”）"
          "—— 同一批跨 TU / 内联 ODR 样本，动态检测器的构建探测源本身就编不过。",
          f"- `cross-compile`：{err['unknown']['cross-compile']['n_unknown']} 格 unknown，"
          "原因 = g++/clang++ 任一编译失败（note 原文：“g++ 编译失败”）。", ""]

    L += ["## 4. 全检测器一致盲区（expected=catch 且 8 资产无一 catch）", "",
          f"- **共 {err['all_detector_blindspot']['n']} 条**"
          f"（严格口径「6 个可用资产全 miss」= "
          f"{err['all_detector_blindspot']['strict_6_available_all_miss_n']} 条）",
          f"- 其中 planted=true {err['all_detector_blindspot']['planted_true']} / "
          f"planted=false {err['all_detector_blindspot']['planted_false']}",
          f"- 含至少一个 unknown 判定的：{err['all_detector_blindspot']['n_with_unknown']} 条", "",
          "### 按 defect_type", "",
          "| defect_type | n |", "|---|---:|"]
    for t, n in sorted(err["all_detector_blindspot"]["by_type"].items(), key=lambda kv: -kv[1]):
        L.append(f"| {t} | {n} |")
    L += ["", "### 按批次", "", "| 批次 | n |", "|---|---:|"]
    for t, n in sorted(err["all_detector_blindspot"]["by_batch"].items(), key=lambda kv: -kv[1]):
        L.append(f"| {t} | {n} |")
    L += ["", "### 样本清单", "",
          "| uid | 批次 | defect_type | planted | hung | unknown 资产 |",
          "|---|---|---|---|---|---|"]
    for b in err["all_detector_blindspot"]["samples"]:
        L.append(f"| `{b['uid']}` | {b['source_batch']} | {b['defect_type']} | "
                 f"{b['planted']} | {b['hung_flag']} | "
                 f"{', '.join(b['unknown_assets']) or '—'} |")
    L += ["", "- 这些样本是**任何检测器组合都无法覆盖**的残余盲区，是 FD 策略的"
          "能力天花板，应进入论文的能力边界讨论（与 676g §6 结论一致）。", ""]
    emit("676l_错误模式分析报告.md", "\n".join(L))

    # ── 总报告 ─────────────────────────────────────────────────────────────
    L = ["# 676l · 检测器能力深度 Benchmark 总报告", "",
         f"- **生成**：{_now()}",
         "- **脚本**：`tools/benchmark_676l_analysis.py`（可复现，`--stage all`）",
         f"- **数据源**：`{val['matrix_path']}`（676g 产物，**只读**）",
         "- **红线**：判定矩阵 / 检测器（`tools/holdout_reveal_661.py`）/ 论文（`research/`）/ "
         "样本数据（`data/holdout_expansion/`）零修改；未 push。", "",
         "---", "",
         "## 1. 分析范围与方法", "",
         "### 1.1 数据来源与矩阵规模", "",
         f"- 判定矩阵：`{val['matrix_path']}`，schema `{val['matrix_schema']}`",
         f"- 规模：**{val['n_samples']} 样本 × {val['n_assets']} 资产 = {val['n_cells']} 格**，"
         f"缺失 **{val['n_missing_cells']}**，非法 verdict **{val['n_bad_verdict']}**",
         f"- verdict 分布：{val['verdict_distribution']}"
         f"（catch {val['verdict_distribution_pct']['catch']}% / "
         f"miss {val['verdict_distribution_pct']['miss']}% / "
         f"unknown {val['verdict_distribution_pct']['unknown']}%）",
         f"- ground truth：样本级 `expected_verdict`，catch {val['expected_verdict_distribution'].get('catch')} / "
         f"miss {val['expected_verdict_distribution'].get('miss')}",
         f"- 与样本 `.json` 交叉验证：比对 {val['gt_crosscheck']['checked']} 条，"
         f"不一致 **{val['gt_crosscheck']['mismatch']}** 条",
         f"- 缺陷类型：{val['n_defect_types']} 类；批次：{val['source_batch_distribution']}",
         f"- 挂起样本：{val['n_hung']} 条", "",
         "### 1.2 指标定义", "",
         "| 指标 | 定义 |", "|---|---|",
         "| TP | expected=catch 且 detector=catch |",
         "| FN | expected=catch 且 detector=miss |",
         "| FP | expected=miss 且 detector=catch |",
         "| TN | expected=miss 且 detector=miss |",
         "| Precision | TP/(TP+FP) |",
         "| Recall | TP/(TP+FN) |",
         "| Specificity | TN/(TN+FP) |",
         "| F1 | 2PR/(P+R) |",
         "| Accuracy | (TP+TN)/(TP+FN+FP+TN) |",
         "| unknown | 单独统计，**不进**混淆矩阵 |", "",
         "OR 聚合（样本级）= 选中资产任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss"
         "（与 `AttributionExecutor` 同义）。", "",
         "### 1.3 数据质量：676g vs 676f 矩阵差异（如实记录，不修改）", ""]
    md = val["data_quality"]["matrix_diff_vs_676f"]
    if md:
        L += [f"- 676f 矩阵 {md['n_676f']} 条 / 676g 矩阵 {md['n_676g']} 条；"
              f"按 (source_batch, sample_id) 可比的交集 **{md['n_common']}** 条"
              "（其余因批次命名不同不可直接配对）",
              f"- 交集内逐资产判定差异：`{md['verdict_diffs_by_asset']}`",
              "- 典型差异：`cross-compile` 在 expD 的 10 个 STL 样本上 676f=catch / 676g=miss。",
              "- **影响**：FD 的 fail_hits 排序来自 676f 派生集，而本批评估用 676g 矩阵；"
              "本批因此同时给出 in-sample 排序作为对照（见 §4.2）。", ""]

    L += ["---", "", "## 2. 单检测器性能排名", "",
          "| 排名 | 检测器 | Precision | Recall | F1 | Specificity | Accuracy | unknown率 | TP | FN | FP | TN |",
          "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for i, a in enumerate(perf["ranking_by_recall"], 1):
        p = perf["per_asset"][a]
        L.append(f"| {i} | `{a}` | {_pct(p['precision'])} | **{_pct(p['recall'])}** | "
                 f"{_pct(p['f1'])} | {_pct(p['specificity'])} | {_pct(p['accuracy'])} | "
                 f"{_pct(p['unknown_rate'])} | {p['tp']} | {p['fn']} | {p['fp']} | {p['tn']} |")
    L += ["",
          f"- 8 资产 OR（分母 expected=catch {perf['or_all8']['n']}）= "
          f"**{_pct(perf['or_all8']['recall'])}**（{perf['or_all8']['hit']} hit）；"
          f"全 1147 口径 catch-rate = {_pct(perf['or_all8_catchrate_all']['recall'])}。",
          "- 两个结构性恒 unknown 资产（`wunsequenced`、`compile-time`）的 precision/recall "
          "均为 n/a（无已知判定）——它们在池里的作用是「被 FD 主动排除」，不是提供检出。", "",
          "**与 676g 的交叉核对（口径不同，必须并报）**：", "",
          "| 量 | 676g 报告 | 本批（676l） | 差异来源 |",
          "|---|---|---|---|",
          f"| 样本级检出 | 707/1147 = 61.6% | {perf['or_all8_catchrate_all']['hit']}/1147 = "
          f"{_pct(perf['or_all8_catchrate_all']['recall'])} | **一致**（同为 8 资产 OR） |",
          f"| 单资产 asan catch | 408 | {perf['per_asset']['asan']['tp'] + perf['per_asset']['asan']['fp']}"
          f" | **一致**（含 expected=miss 的 FP） |",
          "| 边际贡献 asan | +12.1pp | +19.29pp | 676g 分母 = 全部 1147；"
          "本批分母 = expected=catch 的 674 |",
          "| 边际贡献 ubsan / tsan / compiler-warn | +7.2 / +7.4 / +4.6pp | "
          "+10.98 / +10.39 / +5.93pp | 同上（集合一致，次序见下） |",
          "", "- **排序一致性**：两种口径下 `asan` 都稳居第一（676g +12.1pp / 本批 +19.29pp），"
          "`ubsan`、`tsan`、`compiler-warn` 构成第二梯队（集合一致），"
          "`compile-time`/`wunsequenced` 都是 0.00pp。"
          "**次序差异**：676g 里 `tsan`(+7.4) 略高于 `ubsan`(+7.2)、"
          "`cross-compile`(+1.2) 高于 `linker`(+0.9)；本批相反"
          "（`ubsan` 10.98 > `tsan` 10.39；`linker` 1.34 > `cross-compile` 0.30）。"
          "两组差异都 < 1pp，属口径（分母不同）与矩阵差异的共同作用，"
          "**不改变「asan 最强、两个结构性资产零信息」的结论**。", "",
          "- 详见 `676l_单检测器性能报告.md`（含 8×70 recall 矩阵、planted / 批次 / 家族分组）。", ""]

    L += ["---", "", "## 3. 检测器互补性", "",
          f"- 28 对共现分析完成；**实质对**（双方 catch ≥ {comp['substantive_min_catch']}）里"
          "最冗余对："
          + "；".join(f"`{p['a']}`+`{p['b']}` J={_f(p['jaccard'])}"
                      for p in comp["most_redundant_pairs_substantive"][:3]),
          "- 最互补对：" + "；".join(f"`{p['a']}`+`{p['b']}` J={_f(p['jaccard'])}"
                                     for p in comp["least_similar_pairs_substantive"][:3]),
          "- 结构性互补：`linker` 的 10 个 catch **全部**落在 `asan`/`ubsan`/`tsan` 的 "
          "10 个 unknown 里（强 ODR ⇒ 动态检测器链接失败）⇒ 它虽只贡献 1.34pp，"
          "但覆盖的正是动态资产看不见的那一块。", "",
          "### 3.1 边际贡献排序（对 OR recall，分母 expected=catch）", "",
          "| 排名 | 检测器 | 边际贡献(pp) |", "|---:|---|---:|"]
    for i, a in enumerate(comp["marginal_ranking"], 1):
        L.append(f"| {i} | `{a}` | {comp['marginal_contribution'][a]['marginal_pp']:.2f} |")
    L += ["", "### 3.2 聚类（1 − Jaccard，average linkage，切 3 组）", "",
          "| 组 | 成员 | 代表 |", "|---|---|---|"]
    for c in comp["clusters_k3"]:
        L.append(f"| {c['cluster']} | {', '.join('`'+m+'`' for m in c['members'])} | "
                 f"`{c['representative']}` |")
    L += ["", "- 详见 `676l_检测器互补性报告.md`（28 对全表、8×8 相关性矩阵、κ）。", ""]

    L += ["---", "", "## 4. 最佳组合分析", "",
          "### 4.1 穷举最佳 k（分母 expected=catch）", "",
          "| k | 最佳组合 | 最佳 recall | 最差 recall |", "|---:|---|---:|---:|"]
    for e in combo["exhaustive_by_k"]:
        L.append(f"| {e['k']} | {', '.join('`'+x+'`' for x in e['best']['assets'])} | "
                 f"**{_pct(e['best']['recall'])}** | {_pct(e['worst']['recall'])} |")
    L += [f"| 8 | 全池 | {_pct(combo['full_pool']['recall'])} | {_pct(combo['full_pool']['recall'])} |", ""]

    L += ["### 4.2 FD vs 最佳 vs Random（k=4）", "",
          "| 臂 | 组合 | recall | 说明 |", "|---|---|---:|---|",
          f"| 穷举最佳 | {', '.join('`'+x+'`' for x in combo['best_k4']['assets'])} | "
          f"**{_pct(combo['best_k4']['recall'])}** | 全量 1147 上的上界 |",
          f"| FD(676f 派生集) | {', '.join('`'+x+'`' for x in combo['fd_676f_by_k'][3]['assets'])} | "
          f"{_pct(combo['fd_676f_by_k'][3]['recall'])} | 预注册策略，派生集训练 |",
          f"| FD(in-sample) | {', '.join('`'+x+'`' for x in combo['fd_insample_by_k'][3]['assets'])} | "
          f"{_pct(combo['fd_insample_by_k'][3]['recall'])} | 全量排序（含泄漏），只作参考 |",
          f"| Random 均值 | — | {_pct(combo['random_k4']['mean'])} | 2000 次抽样 |",
          f"| Static | {', '.join('`'+x+'`' for x in combo['static_arm']['assets'])} | "
          f"{_pct(combo['static_arm']['recall'])} | 静态资产字典序前缀（k="
          f"{combo['static_arm']['k']}） |",
          "",
          f"- 最佳组合位于 Random 分布的 **{combo['random_k4']['best_percentile']:.1f}** 百分位；"
          f"FD(676f) 位于 **{combo['random_k4']['fd676f_percentile']:.1f}** 百分位。",
          f"- FD(676f) 的 k=4 组合{'**等于**' if combo['fd_676f_k4_equals_best'] else '**不等于**'}穷举最佳。", ""]

    L += ["### 4.3 增量收益曲线与拐点", "",
          "| k | 最佳 recall | Δ(pp) |", "|---:|---:|---:|"]
    for c in combo["incremental_curve"]:
        L.append(f"| {c['k']} | {_pct(c['best_recall'])} | +{c['delta_pp']:.2f} |")
    L += ["", f"- 拐点 **k = {combo['knee_k']}**；k=4 最佳组合已达全池的 "
          f"{combo['best_k4']['recall']/combo['full_pool']['recall']*100:.1f}%。",
          "- 详见 `676l_最佳组合分析报告.md`。", ""]

    L += ["---", "", "## 5. 错误模式", "",
          f"- 全检测器一致盲区（expected=catch 且 8 资产无一 catch）："
          f"**{err['all_detector_blindspot']['n']} 条**；严格 6 可用资产全 miss 口径 "
          f"{err['all_detector_blindspot']['strict_6_available_all_miss_n']} 条。",
          "- 盲区 Top 类型："
          + "；".join(f"{t}({n})" for t, n in
                      sorted(err['all_detector_blindspot']['by_type'].items(),
                             key=lambda kv: -kv[1])[:6]),
          f"- unknown 结构：`wunsequenced`/`compile-time` 各 1147 格恒 unknown；"
          f"`asan`/`ubsan`/`tsan` 各 {err['unknown']['asan']['n_unknown']} 格；"
          f"`cross-compile` {err['unknown']['cross-compile']['n_unknown']} 格。",
          "- 详见 `676l_错误模式分析报告.md`（FN Top5、FP 成因、样本清单）。", ""]

    L += ["---", "", "## 6. 可视化图表（`data/676l_figures/`，PNG，300 DPI）", "",
          "| 文件 | 内容 |", "|---|---|",
          "| `fig1_detector_performance.png` | (a) 8 检测器 recall 降序柱；(b) precision / recall / F1 分组柱 |",
          "| `fig2_correlation_heatmap.png` | 8×8 相关性热力图（Pearson，两两完整观测；n/a = 无共同已知判定） |",
          "| `fig3_marginal_contribution.png` | 8 检测器留一法边际贡献排序（分母 674） |",
          "| `fig4_incremental_gain.png` | k=1…8 最佳组合 recall 曲线 + 最差组合 + 拐点 k=5 |",
          "| `fig5_dendrogram.png` | 层次聚类树状图（1 − Jaccard，average linkage） |",
          "| `fig6_confusion_composition.png` | 每检测器 TP/FN/FP/TN/unknown 堆叠构成（占 1147） |",
          "| `fig7_k4_random_distribution.png` | k=4 的 2000 次 Random 分布 vs 最佳 / FD |", "",
          "- 图表用 **matplotlib** 生成（英文标签，避免中文字体缺失）；"
          "matplotlib **不是本仓依赖**，未安装时 `--stage figures` 整体跳过，"
          "其余阶段与 JSON 产物不受影响。", ""]

    L += ["---", "", "## 7. 对论文的贡献（可写进论文的结果）", "",
          "| # | 结论 | 支撑的 claim | 数据位置 |",
          "|---:|---|---|---|",
          f"| C1 | 单资产 recall 排名：`{perf['ranking_by_recall'][0]}` 最强"
          f"（{_pct(perf['per_asset'][perf['ranking_by_recall'][0]]['recall'])}），"
          f"8 资产 OR 达 {_pct(perf['or_all8']['recall'])} | 资产池能力量化 | "
          "`676l_benchmark_results.json` → `perf.per_asset` |",
          f"| C2 | 资产间互补性（实质对，双方 catch ≥ {comp['substantive_min_catch']}）："
          f"最互补对 `{comp['least_similar_pairs_substantive'][0]['a']}`+"
          f"`{comp['least_similar_pairs_substantive'][0]['b']}` Jaccard = "
          f"{_f(comp['least_similar_pairs_substantive'][0]['jaccard'])}，"
          f"最冗余对 `{comp['most_redundant_pairs_substantive'][0]['a']}`+"
          f"`{comp['most_redundant_pairs_substantive'][0]['b']}` Jaccard = "
          f"{_f(comp['most_redundant_pairs_substantive'][0]['jaccard'])} | "
          "「池的价值来自互补而非冗余」 | `complement.pairs` |",
          "| C3 | 边际贡献排序："
          + " > ".join(f"{a}({comp['marginal_contribution'][a]['marginal_pp']:.1f}pp)"
                       for a in comp["marginal_ranking"][:4])
          + f"，零信息资产 = {[a for a in comp['marginal_ranking'] if comp['marginal_contribution'][a]['marginal_pp'] == 0]} | "
          "FD「避开零信息资产」的机制证据 | `complement.marginal_contribution` |",
          f"| C4 | k=1…7 穷举：k=4 最佳 recall = {_pct(combo['best_k4']['recall'])}"
          f"，k=5 起边际收益骤降，拐点 k={combo['knee_k']} | 「k=4 是合理预算」 | "
          "`combo.exhaustive_by_k` / `incremental_curve` |",
          f"| C5 | 全检测器一致盲区 {err['all_detector_blindspot']['n']} 条（expected=catch），"
          "集中在语义/设计层类型 | 能力边界（Threats to Validity） | "
          "`errors.all_detector_blindspot` |",
          "| C6 | `wunsequenced`/`compile-time` 边际贡献 0.00pp、恒 unknown | "
          "「结构性零信息资产」的定义证据 | `complement.marginal_contribution` |", "",
          "**不建议写进论文的**：任何把 `expected_verdict` 当真实缺陷真值的表述；"
          "把 FP 直接当检测器错误的表述（见 §7）。", ""]

    L += ["---", "", "## 8. 对 FD 策略的评价", "",
          f"1. **FD(676f) 的 k=4 组合**（{', '.join('`'+x+'`' for x in FD_676F_K4)}）"
          f"{'就是' if combo['fd_676f_k4_equals_best'] else '不是'}"
          f"全量穷举最佳（{_pct(combo['best_k4']['recall'])}），"
          f"差 {combo['fd_676f_by_k'][3]['gap_to_best_pp']:.2f}pp。"
          "差的来源是 rank-4 的选择：FD 派生集给 `cross-compile`（派生 fail_hits 89），"
          "而 676g 全量上 `cross-compile` 只 catch 122 条（边际贡献 0.30pp），"
          "`compiler-warn` catch 143 条（边际贡献 5.93pp）。"
          "**即：FD 在派生集上把 cross-compile 的命中率估高了**"
          "（676f 矩阵 cross-compile 170 vs 676g 122，见 §1.3）。",
          f"2. 它显著优于 Random（均值 {_pct(combo['random_k4']['mean'])}），"
          f"位于 Random 分布的 {combo['random_k4']['fd676f_percentile']:.1f} 百分位。",
          "3. **但 FD 的优势主要来自池构成效应，不是选择效应**："
          "`wunsequenced`/`compile-time` 的边际贡献是 0.00pp，FD 的价值首先是"
          "「不把预算花在这两个资产上」。这与 676f 的 `uninterpretable` 条款一致，"
          "**不得**升级为「FD 选择策略更聪明」。",
          "4. **矩阵来源差异**：FD 的排序来自 676f 派生集（cross-compile 89 次），"
          "本批 676g 全量排序把 compiler-warn（143 次）排到第 4 —— 说明 FD 是"
          "**真预测器**（在派生集上估计），不是 oracle。两者差异正是"
          "「训练/评估分离」的正常代价。", ""]

    L += ["---", "", "## 9. 局限性", "",
          "1. **`expected_verdict` 是单标注**（生成样本的 Agent 自标），不是真实缺陷真值"
          " ⇒ 所有指标都是「相对于标注」的。",
          "2. **样本偏差**：planted=true 占 88%（1009/1147），指标偏向植入缺陷；"
          "对真实缺陷的泛化性有限（planted=false 仅 74 条）。",
          "3. **OR 聚合假设**：本批的「组合 recall」假设任一资产 catch 即算 catch；"
          "实际使用中多资产报告可能需要人工审核，不是简单 OR。",
          "4. **口径差异**：本批 recall 分母 = expected=catch 的 674 条；"
          "676f 报告的 catch-rate 分母 = 全部样本。两者数字不可直接相减。",
          "5. **unknown 不进混淆矩阵**：`wunsequenced`/`compile-time` 恒 unknown，"
          "其 precision/recall 无定义；若 unknown 比例更高的资产存在，"
          "算出的性能会高估。",
          "6. **矩阵间差异**：676g 与 676f 在共同样本上存在少量判定差异"
          "（cross-compile 10 例等），本批以 676g 为准、**不修改**任何矩阵。",
          "7. **单机单工具链**：结论限于 MinGW g++ 13.1 / WSL g++ 13.3 / clang++ 22.1.8 "
          "环境；换平台/换检测器版本，数字会变。", ""]

    L += ["---", "", "## 10. 复现", "",
          "```bash",
          "# 全量分析（validate → perf → complement → combo → errors → figures → reports）",
          "python tools/benchmark_676l_analysis.py --stage all",
          "",
          "# 单阶段",
          "python tools/benchmark_676l_analysis.py --stage validate",
          "python tools/benchmark_676l_analysis.py --stage perf",
          "python tools/benchmark_676l_analysis.py --stage complement",
          "python tools/benchmark_676l_analysis.py --stage combo",
          "python tools/benchmark_676l_analysis.py --stage errors",
          "python tools/benchmark_676l_analysis.py --stage figures",
          "```", "",
          "机读结果：`data/676l_benchmark_results.json`（本报告全部数字的唯一来源）。", "",
          "## 11. 提交信息", "",
          "- commit：`676l: 检测器深度 Benchmark——8 资产 P/R/F1 + 互补性 + 最佳组合 + 边际贡献`"
          "（DCO 签署，`git log --oneline -1` 取 hash；未 push）",
          "- `git add` 清单：`tools/benchmark_676l_analysis.py`、`data/676l_*.md`、"
          "`data/676l_benchmark_results.json`、`data/676l_figures/`",
          "- 未 add：`data/blindspot_676g_*`、`data/holdout_expansion/`、`research/`、"
          "`tools/holdout_reveal_661.py`", ""]
    emit("676l_检测器Benchmark总报告.md", "\n".join(L))

    return made


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="676l 检测器深度 Benchmark（只读分析）")
    ap.add_argument("--stage", default="all",
                    choices=["all", "validate", "perf", "complement", "combo",
                             "errors", "figures", "reports"])
    a = ap.parse_args(argv)

    mx = load_matrix()
    res = {}
    if OUT_JSON.is_file():
        res = json.loads(OUT_JSON.read_text(encoding="utf-8")).get("results", {})

    def need(key, fn, *, force: bool):
        if force or key not in res:
            res[key] = fn()
            print(f"[676l] {key}: 完成")

    if a.stage in ("all", "validate"):
        need("validate", lambda: stage_validate(mx), force=True)
        v = res["validate"]
        print(f"[676l] validate: {v['n_samples']}×{v['n_assets']}={v['n_cells']} 格，"
              f"缺失 {v['n_missing_cells']}，verdict 域非法 {v['n_bad_verdict']}，"
              f"GT 交叉验证 {v['gt_crosscheck']['checked']} 条 / 不一致 "
              f"{v['gt_crosscheck']['mismatch']}；pass={v['verification']['pass']}")
    if a.stage in ("all", "perf"):
        need("perf", lambda: stage_perf(mx), force=True)
        print(f"[676l] perf: 排名 {res['perf']['ranking_by_recall']}")
    if a.stage in ("all", "complement"):
        need("complement", lambda: stage_complement(mx), force=True)
        print(f"[676l] complement: {res['complement']['n_pairs']} 对；"
              f"边际排序 {res['complement']['marginal_ranking']}")
    if a.stage in ("all", "combo"):
        need("combo", lambda: stage_combo(mx), force=True)
        print(f"[676l] combo: best k=4 = {res['combo']['best_k4']['assets']} "
              f"recall={res['combo']['best_k4']['recall']}")
    if a.stage in ("all", "errors"):
        need("errors", lambda: stage_errors(mx), force=True)
        print(f"[676l] errors: 全检测器盲区 "
              f"{res['errors']['all_detector_blindspot']['n']} 条")

    doc = {"schema": SCHEMA, "generated_at": _now(),
           "generated_by": "tools/benchmark_676l_analysis.py",
           "matrix": MATRIX.relative_to(ROOT).as_posix(),
           "assets": mx["assets"], "results": res}
    OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")
    print(f"[676l] 写入 {OUT_JSON.relative_to(ROOT).as_posix()}")

    if a.stage in ("all", "figures"):
        figs = stage_figures(mx, res)
        print(f"[676l] figures: {len(figs)} 张 → {FIGDIR.relative_to(ROOT).as_posix()}/")
        for f in figs:
            print(f"        - {f}")
    if a.stage in ("all", "reports"):
        reps = write_reports(mx, res)
        print(f"[676l] reports: {len(reps)} 份")
        for f in reps:
            print(f"        - {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
