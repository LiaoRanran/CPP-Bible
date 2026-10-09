#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""check_drift_correctability.py — 707-C：漂移「可纠错性」检查（698-B 定理 T6）。

科研依据（698-B 定理 T6：可纠错边界）
====================================
**可纠正 ⟺ 漂移只作用于后处理层**（聚合 / 标签 / 记账 / 报告口径）。这类漂移
可以用**已存的逐资产原始矩阵**事后重算纠正。
反之，**获取层漂移**（检测器行为 / 环境可用性 / 资产是否可测量发生变化）**不可事后
纠正** —— 原始矩阵里根本没有那一次测量 ⇒ **必须重测**（re-measure），不能靠事后校正。

实测残留误差（698-B）：纠正后 asan **30.04%** / ubsan **21.38%** / tsan **21.73%**；
而**结构性恒 unknown 列**（`wunsequenced` / `compile-time`，两环境同等缺实现）残留 **0**
⇒ 与「结构缺口可纠正、环境缺口必须重测」一致。

用法
====
    python tools/check_drift_correctability.py --case 692-e1e2       # 验证环境门控撤除=必须重测
    python tools/check_drift_correctability.py --matrices A.json B.json   # 比较两环境逐样本矩阵
    python tools/check_drift_correctability.py --case 692-e1e2 --out data/707_correctability.json

红线：``detect_calls = 0``；只读冻结矩阵；产出只写 ``data/707_*``。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path
from typing import Any, Final

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from asset_capabilities import (  # noqa: E402  707-B 单一事实源
    ALL_ASSETS,
    E1_SUPPORTED,
    E2_SUPPORTED,
    ZERO_YIELD_ASSETS,
)
from utils.data_access import DATA, load_json_cached  # noqa: E402

OUT_JSON: Final[Path] = ROOT / "data" / "707_correctability.json"

# 698-B 实测残留误差（纠正后仍不可信的比例，%）
RESIDUAL_698B_PCT: Final[dict[str, float]] = {"asan": 30.04, "ubsan": 21.38, "tsan": 21.73}


def classify_drift(removed: set[str], added: set[str], *, changed_assets: set[str] | None = None) -> dict[str, Any]:
    """按 T6 对一次漂移分类。

    * 若变化的资产属**获取层**（资产可用性变化：`removed`/`added` 或逐资产裁决变化
      `changed_assets`）⇒ ``must_retest=True``（不可事后纠正）。
    * 若只有后处理层变化（记账/聚合/标签）⇒ ``correctable=True``。
    * 结构性恒 unknown 资产（静态未实现，两环境同等缺）⇒ 结构缺口，``correctable=True``、
      残留 0（不属于获取层漂移）。
    """
    changed_assets = changed_assets or set()
    structural = set(ZERO_YIELD_ASSETS)
    # 获取层漂移 = 任何**非结构**资产的可用性或逐资产裁决发生变化
    # （结构性资产 wunsequenced/compile-time 两环境同等缺 ⇒ 不算获取层漂移）。
    acquisition_changed = (removed | added | changed_assets) - structural
    must_retest = bool(acquisition_changed)

    return {
        "removed_assets": sorted(removed),
        "added_assets": sorted(added),
        "changed_assets": sorted(changed_assets),
        "acquisition_layer_assets": sorted(acquisition_changed),
        "structural_assets": sorted(structural),
        "layer": "acquisition（获取层）" if must_retest else "post_processing（后处理层）",
        "correctable": not must_retest,
        "must_retest": must_retest,
        "action": ("必须重测（re-measure）：原始矩阵无此测量，事后校正不可靠" if must_retest
                   else "可事后纠正：用已存逐资产原始矩阵重算"),
        "residual_698b_pct_reference": (dict(RESIDUAL_698B_PCT) if must_retest else {}),
    }


def case_692_e1e2() -> dict[str, Any]:
    """692 的 E1→E2「环境门控撤除」案例。

    E1 支持 6 个环境门控资产；E2（native）只支持 3 个 ⇒ 撤除 `{asan,ubsan,tsan}`。
    T6 判定：这三个是**获取层**资产（E2 根本无法测量它们）⇒ **必须重测**。
    """
    removed = set(E1_SUPPORTED) - set(E2_SUPPORTED)
    added = set(E2_SUPPORTED) - set(E1_SUPPORTED)
    cls = classify_drift(removed, added)
    return {
        "case": "692-e1e2",
        "E1_supported": list(E1_SUPPORTED),
        "E2_supported": list(E2_SUPPORTED),
        "classification": cls,
        "expected_must_retest_assets": ["asan", "ubsan", "tsan"],
        "claim_T6_holds": (cls["must_retest"]
                           and set(cls["acquisition_layer_assets"]) == {"asan", "ubsan", "tsan"}),
        "note": ("结构性资产 wunsequenced/compile-time 两环境同等缺（静态未实现）⇒ 不算获取层漂移，"
                 "属可纠正的结构缺口（残留 0）。"),
    }


def compare_matrices(path_a: str, path_b: str) -> dict[str, Any]:
    """比较两个环境的逐样本 × 逐资产矩阵，按 T6 分类漂移。"""
    da = load_json_cached(DATA / path_a) if not Path(path_a).is_absolute() else json.loads(Path(path_a).read_text("utf-8"))
    db = load_json_cached(DATA / path_b) if not Path(path_b).is_absolute() else json.loads(Path(path_b).read_text("utf-8"))

    def idx(doc: dict[str, Any]) -> dict[str, dict[str, str]]:
        out: dict[str, dict[str, str]] = {}
        for s in doc.get("samples", []):
            uid = str(s.get("uid") or s.get("sample_id") or "")
            pa = s.get("per_asset") or {}
            out[uid] = {a: str((pa.get(a) or {}).get("verdict") if isinstance(pa.get(a), dict)
                               else pa.get(a, "unknown")) for a in ALL_ASSETS}
        return out

    A, B = idx(da), idx(db)
    common = sorted(set(A) & set(B))
    changed: dict[str, int] = {a: 0 for a in ALL_ASSETS}
    for uid in common:
        for a in ALL_ASSETS:
            if A[uid][a] != B[uid][a]:
                changed[a] += 1
    changed_assets = {a for a, c in changed.items() if c > 0}
    cls = classify_drift(set(), set(), changed_assets=changed_assets)
    return {
        "case": "matrix-diff",
        "matrix_A": path_a, "matrix_B": path_b,
        "n_common": len(common),
        "per_asset_changed_cells": changed,
        "classification": cls,
    }


def _emit(doc: dict[str, Any], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="707-C：漂移可纠错性检查（698-B 定理 T6）")
    ap.add_argument("--case", choices=("692-e1e2",), default="692-e1e2")
    ap.add_argument("--matrices", nargs=2, metavar=("A", "B"), default=None)
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    if args.matrices:
        body = compare_matrices(args.matrices[0], args.matrices[1])
    else:
        body = case_692_e1e2()

    doc: dict[str, Any] = {
        "schema": "queyi-707/drift-correctability/v1",
        "generated_by": "tools/check_drift_correctability.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        # 红线 8：科研依据
        "research_basis": "698-B 定理 T6：可纠正 ⟺ 漂移只作用于后处理层；获取层漂移必须重测",
        "authority_source": "data/700_design_simulation.json（T6 陈述）",
        **body,
    }
    _emit(doc, args.out)

    intro = f"== 707-C 漂移可纠错性（T6）case={doc['case']} =="
    print(intro)
    c = body["classification"]
    print(f"  获取层资产={c['acquisition_layer_assets']}  结构资产={c['structural_assets']}")
    print(f"  层={c['layer']}  correctable={c['correctable']}  must_retest={c['must_retest']}")
    print(f"  动作：{c['action']}")
    if "claim_T6_holds" in body:
        print(f"  T6 断言（环境门控撤除 ⇒ asan/ubsan/tsan 必须重测）= {body['claim_T6_holds']}")
    print(f"  → {args.out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
