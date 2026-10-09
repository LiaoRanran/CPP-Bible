#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_710_predictor.py — 710-C3：只用**语义 + 上下文**特征的可检测性预测器。

科研依据
========
697-C（``data/697_capability_boundary_prediction.md``）的两个负面/边界结果：
* **族迁移天花板**：只用「同 defect_type 的其它家族 catch 率」的朴素基线 AUC = **0.7662**，
  **高于**所有源码结构特征模型（最高 0.7551，Tier B 装袋 CART，家族感知 5 折）；
* ⇒ **结构特征在「泛化到全新家族」时不迁移**。

本批的问题：换成**语义特征（跨族可迁移的粗粒度信息）+ 上下文特征（批次/植入标记/多 TU）**
能不能**超过 0.7662**？—— 即：不合格的不是"除结构外没有别的信号"，而是"结构信号是族内记忆"。

特征（全部**只用训练折**估计，测试折不可见 ⇒ 无泄漏）
=====================================================
| 组 | 特征 | 说明 |
|---|---|---|
| 语义 | ``type_rate`` | defect_type 级 catch 率（其它折，无该类型取全局率） |
| 语义 | ``group_rate`` | 681 的 14 组级 catch 率（其它折） |
| 语义 | ``family_rate`` | 8 家族级 catch 率（其它折） |
| 语义 | ``type_det`` / ``det_val`` | 训练折内该类型是否**裁决全同**（Rice「可判定岛」）与取值 |
| 语义 | ``type_n`` | 训练折内该类型的样本数（可靠度） |
| 语义 | ``shrunk_rate`` | 层次收缩 $(n_t r_t + m r_g)/(n_t+m)$（$m{=}5$） |
| 上下文 | ``batch_rate`` | source_batch 级 catch 率（其它折；批次效应，697 §4.2 登记过） |
| 上下文 | ``planted`` | 植入缺陷 vs 真实缺陷 |
| 上下文 | ``n_files`` | 该样本的翻译单元数（多 TU 样本） |

对照：``type_rate`` 单特征 = 697 的族迁移天花板（应复现 ≈0.7662）。

红线：``detect_calls = 0``；只读冻结矩阵 + 677b 家族 + 681 词表；**0 处**论文正文/bib 修改。
输出：``data/710_predictor_features.json``。

用法
====
    python tools/compute_710_predictor.py
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from train_697_predictor import (  # noqa: E402
    BaggedCart,
    Logistic,
    auc,
    build_family_index,
    confusion,
    group_folds,
)
from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_710_predictor")

OUT_JSON: Final[Path] = ROOT / "data" / "710_predictor_features.json"
MATRIX: Final[str] = "blindspot_676g_detection_matrix.json"
FAMILIES: Final[str] = "677b_clone_families.json"
TYPE_STATS: Final[str] = "681_type_stats_normalized.json"

ASSETS6: Final[tuple[str, ...]] = ("asan", "ubsan", "tsan", "compiler-warn",
                                   "cross-compile", "linker")

FAMILY_OF: Final[dict[str, str]] = {
    "memory_safety": "memory", "use_after_free": "memory", "double_free": "memory",
    "memory_leak": "memory", "smart_pointer": "memory", "raii_violation": "memory",
    "move_semantics": "memory", "uninitialized_read": "memory",
    "out_of_bounds": "bounds", "null_pointer_deref": "bounds",
    "integer_overflow": "integer", "bit_operation": "integer",
    "type_punning": "alias_type", "strict_aliasing": "alias_type",
    "alignment": "alias_type", "endianness": "alias_type", "linker_odr": "alias_type",
    "data_race": "concurrency", "atomic_ub": "concurrency",
    "memory_order": "concurrency", "deadlock": "concurrency",
    "condition_variable": "concurrency",
    "iterator_invalidation": "stl", "stl_container_ub": "stl",
    "string_ub": "stl", "algorithm_misuse": "stl",
    "virtual_function": "language_oop", "lambda_capture": "language_oop",
    "cross_tu_ub": "language_oop", "logic_error": "language_oop", "other_ub": "language_oop",
    "volatile_misuse": "embedded", "register_ub": "embedded", "interrupt_safety": "embedded",
}

SEMANTIC: Final[tuple[str, ...]] = (
    "type_rate", "group_rate", "family_rate", "type_det", "det_val",
    "type_n_log", "shrunk_rate",
)
CONTEXT: Final[tuple[str, ...]] = ("batch_rate", "planted", "n_files")
FULL: Final[tuple[str, ...]] = SEMANTIC + CONTEXT

SHRINK_M: Final[float] = 5.0


def _verdict(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell) if cell is not None else "unknown"


def build_rows() -> list[dict[str, Any]]:
    doc = load_json_cached(DATA / MATRIX)
    grp = {t: str(v.get("group") or "unknown")
           for t, v in load_json_cached(DATA / TYPE_STATS).get("per_type", {}).items()}
    # ⚠ 必须复用 697 的索引构造（它同时注册 A5 sample_id 与 orig_id 两个键）——
    #   若只按 A5 的 sample_id 查，676g 的 sid（如 sample_001）会静默退化成单成员族，
    #   家族感知 CV 就变成随机折（697 §4.2 已登记过这个陷阱）。
    idx = build_family_index()

    rows: list[dict[str, Any]] = []
    for s in doc.get("samples", []):
        uid = str(s.get("uid") or "")
        sid = str(s.get("sample_id") or "")
        pa = s.get("per_asset") or {}
        y = 1 if any(_verdict(pa.get(a, "unknown")) == "catch" for a in ASSETS6) else 0
        dt = str(s.get("defect_type") or "unknown")
        rows.append({
            "uid": uid,
            "defect_type": dt,
            "group": grp.get(dt, "unknown"),
            "family": FAMILY_OF.get(dt, "language_oop"),
            "source_batch": str(s.get("source_batch") or "unknown"),
            "planted": 1.0 if s.get("planted") is True else 0.0,
            "n_files": float(len(s.get("files") or [])),
            "clone_family": idx.get(sid) or idx.get(uid.split(":", 1)[-1]) or f"single::{uid}",
            "y": y,
        })
    return rows


def _rates(rows: list[dict[str, Any]], key: str) -> tuple[dict[str, float], float]:
    cnt: dict[str, list[int]] = defaultdict(list)
    for r in rows:
        cnt[str(r[key])].append(int(r["y"]))
    return ({k: sum(v) / len(v) for k, v in cnt.items()},
            sum(int(r["y"]) for r in rows) / max(1, len(rows)))


def _build_features(tr: list[dict[str, Any]], te: list[dict[str, Any]]) -> None:
    """把训练折统计量写进**测试折**行（不碰训练折，避免自我泄漏）。"""
    tr_rate, tr_glob = _rates(tr, "defect_type")
    gr_rate, _ = _rates(tr, "group")
    fam_rate, _ = _rates(tr, "family")
    b_rate, _ = _rates(tr, "source_batch")
    tr_typ: dict[str, list[int]] = defaultdict(list)
    for r in tr:
        tr_typ[str(r["defect_type"])].append(int(r["y"]))
    for r in te:
        t, g, f, b = str(r["defect_type"]), str(r["group"]), str(r["family"]), str(r["source_batch"])
        n_t = len(tr_typ.get(t, []))
        rt = tr_rate.get(t, tr_glob)
        rg = gr_rate.get(g, tr_glob)
        hist = tr_typ.get(t, [])
        det = 1.0 if hist and (sum(hist) == 0 or sum(hist) == len(hist)) else 0.0
        r["type_rate"] = rt
        r["group_rate"] = rg
        r["family_rate"] = fam_rate.get(f, tr_glob)
        r["batch_rate"] = b_rate.get(b, tr_glob)
        r["type_det"] = det
        r["det_val"] = (sum(hist) / len(hist)) if hist else 0.5
        r["type_n_log"] = math.log1p(n_t)
        r["shrunk_rate"] = ((n_t * rt + SHRINK_M * rg) / (n_t + SHRINK_M)) if n_t else rg


def _cv(rows: list[dict[str, Any]], names: tuple[str, ...], model: Any,
        folds: int = 5) -> dict[str, Any]:
    ga = group_folds([str(r["clone_family"]) for r in rows], folds)
    pred = [0.0] * len(rows)
    imp: Counter[str] = Counter()
    for f in range(folds):
        tr = [r for r in rows if ga[str(r["clone_family"])] != f]
        te = [r for r in rows if ga[str(r["clone_family"])] == f]
        _build_features(tr, te)
        if model == "raw":
            key = names[0]
            for i, r in enumerate(rows):
                if ga[str(r["clone_family"])] == f:
                    pred[i] = float(r.get(key, 0.0))
            continue
        X = [[float(r.get(n, 0.0)) for n in names] for r in te]
        ytr = [int(r["y"]) for r in tr]
        Xtr = [[float(r.get(n, 0.0)) for n in names] for r in tr]
        if model == "lr":
            mdl: Any = Logistic().fit(Xtr, ytr)
        else:
            mdl = BaggedCart().fit(Xtr, ytr, list(names))
            imp.update(mdl.importance())   # type: ignore[attr-defined]
        p = mdl.predict(X)
        j = 0
        for i, r in enumerate(rows):
            if ga[str(r["clone_family"])] == f:
                pred[i] = float(p[j])
                j += 1
    y = [int(r["y"]) for r in rows]
    out: dict[str, Any] = {"auc": auc(y, pred), **confusion(y, pred),
                           "feature_set": list(names)}
    if imp:
        out["bagcart_fold_summed_importance_top10"] = imp.most_common(10)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="710-C3 语义+上下文预测器")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    rows = build_rows()
    n = len(rows)
    base = sum(int(r["y"]) for r in rows) / n
    _log.info("n=%d 正类率=%.6f 家族=%d", n, base, len({r["clone_family"] for r in rows}))

    # 基线（复现 697 的族迁移天花板口径）
    ga = group_folds([str(r["clone_family"]) for r in rows], 5)
    bl = [0.0] * n
    grp = [0.0] * n
    for f in range(5):
        tr = [r for r in rows if ga[str(r["clone_family"])] != f]
        r1, glob = _rates(tr, "defect_type")
        r2, _ = _rates(tr, "group")
        for i, r in enumerate(rows):
            if ga[str(r["clone_family"])] == f:
                bl[i] = r1.get(str(r["defect_type"]), glob)
                grp[i] = r2.get(str(r["group"]), glob)
    y = [int(r["y"]) for r in rows]
    baseline = {
        "type_rate_only_auc": auc(y, bl),
        "type_rate_only_confusion": confusion(y, bl),
        "group_rate_only_auc": auc(y, grp),
        "group_rate_only_confusion": confusion(y, grp),
        "replicates_697_ceiling": "697 的族迁移天花板 AUC = 0.7662（同口径：group_folds seed=697）",
    }

    results: dict[str, Any] = {}
    results["M0_type_rate(raw)"] = {"auc": auc(y, bl), **confusion(y, bl),
                                    "feature_set": ["type_rate"]}
    results["M1_hier_shrunk(raw)"] = _cv(rows, ("shrunk_rate",), "raw")
    results["M2_语义_lr"] = _cv(rows, SEMANTIC, "lr")
    results["M3_语义+上下文_lr"] = _cv(rows, FULL, "lr")
    results["M4_语义+上下文_bagcart"] = _cv(rows, FULL, "bagcart")
    results["M5_语义_bagcart"] = _cv(rows, SEMANTIC, "bagcart")

    # 收缩强度敏感性（不预注册主值以外的调参；报告全表）
    sens = {}
    for m in (2.0, 5.0, 10.0, 20.0):
        globals()["SHRINK_M"] = m
        sens[f"m={m:g}"] = _cv(rows, ("shrunk_rate",), "raw")["auc"]
    globals()["SHRINK_M"] = 5.0

    doc: dict[str, Any] = {
        "schema": "queyi-710/predictor-semantic-context/v1",
        "generated_by": "tools/compute_710_predictor.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "protocol": {
            "cv": "clone-family 感知 5 折（group_folds seed=697，与 697/693 同口径）",
            "target": "样本级 OR(6) == catch（wunsequenced/compile-time 结构性恒 unknown）",
            "leakage_control": "所有目标编码（type/group/family/batch 率）**只用训练折**估计；"
                               "测试折行在评估前才写入特征",
        },
        "frame": {"n": n, "positive_rate": round(base, 6),
                  "n_clone_families": len({r["clone_family"] for r in rows})},
        "baselines": baseline,
        "models": results,
        "shrink_sensitivity_auc": sens,
        "reference_697": {
            "family_transfer_ceiling_auc": 0.7662,
            "best_structural_model_auc": 0.7551,
            "note": "697 的族迁移天花板 = 只用 defect_type 均值；本批的 M0 即其复现。",
        },
        "honest_limits": [
            "纯标准库实现（无 sklearn/xgboost）；超参未做嵌套搜索，结果不是调参上限。",
            "目标编码在**同一批样本**上估计 ⇒ 即便只用训练折，仍属于「同源样本」；"
            "真正的跨语料迁移未测（无外部语料标签）。",
            "所有检出率来自 1147 条（92.9% 人工植入）冻结矩阵 ⇒ 不代表真实缺陷分布。",
            "``type_det``/``det_val`` 是训练折内的经验量，稀有类型上极不稳（type_n_log 作为补偿特征）。",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")

    print("== 710-C3 · 语义+上下文预测器（家族感知 5 折）==")
    print(f"  帧 n={n} 正类率={base:.4f} 家族={doc['frame']['n_clone_families']}")
    print(f"  基线：type_rate AUC={baseline['type_rate_only_auc']:.4f}"
          f"（697 天花板 0.7662）；group_rate AUC={baseline['group_rate_only_auc']:.4f}")
    for name, m in results.items():
        print(f"  {name:<26} AUC={m['auc']:.4f} F1={m.get('f1', float('nan')):.4f}")
    print(f"  收缩敏感性 m: {sens}")
    best = max(results.items(), key=lambda kv: kv[1]["auc"])
    print(f"  最优 = {best[0]}（AUC={best[1]['auc']:.4f}；"
          f"vs 0.7662 = {best[1]['auc'] - 0.7662:+.4f}）")
    print(f"  → {args.out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
