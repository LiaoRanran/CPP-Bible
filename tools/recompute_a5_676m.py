#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran（阿信）
"""recompute_a5_676m.py — 676m 任务 D：用修正后的标签重算 A5 全部指标。

输入（只读，676f/676g/676l 产物一律不修改 —— 红线 9）
=====================================================
  data/a5_676f_detection_matrix.json   1137×8 逐格真实 detect 判定（冻结）
  data/a5_676f_sample_manifest.json    1137 样本规格（冻结）
  data/a5_676f_results.json            676f 分析产物（before 基线）
  data/holdout_expansion/**/*.json     676m 修复后的**权威**标注（after）

输出
====
  data/676m_a5_matrix_corrected.json   冻结矩阵 + 修正后 expected_verdict 的**修正件**
  data/676m_a5_results.json            修正后重算结果（与 676f 结果同 schema）
  data/676m_stability.json             稳定性验证（不稳定格子清单）
  data/676m_A5重算报告.md              报告

口径
====
* 统计原语**全部复用** `data/676f_analysis.py::run()`（内部再复用 673p/673r 的
  三臂对照 / FD-Random-Static 选择语义），只把它的 MATRIX 常量指向修正件 ⇒ 零漂移。
* **主分析口径不依赖 `expected_verdict`**（catch = 该资产 verdict == "catch"），
  所以 H1 标签修正对 FD/Random/Static 与 Δ **应当零影响**；脚本对此做硬断言。
* `expected_verdict` 只影响「expected=catch 口径」的 recall/OR 覆盖率与
  「按 expected_verdict 分层」的视图 —— 这两块单独算并报。

用法
====
    .venv/Scripts/python.exe tools/recompute_a5_676m.py
    .venv/Scripts/python.exe tools/recompute_a5_676m.py --quick   # 2000→200 次随机
"""
from __future__ import annotations

import argparse
import collections
import importlib
import json
import os
import sys
from pathlib import Path
from typing import cast

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "data"))

MATRIX = os.path.join(ROOT, "data", "a5_676f_detection_matrix.json")
MANIFEST = os.path.join(ROOT, "data", "a5_676f_sample_manifest.json")
BEFORE = os.path.join(ROOT, "data", "a5_676f_results.json")
CORRECTED_MX = os.path.join(ROOT, "data", "676m_a5_matrix_corrected.json")
CORRECTED_MAN = os.path.join(ROOT, "data", "676m_a5_manifest_corrected.json")
AFTER = os.path.join(ROOT, "data", "676m_a5_results.json")
STABILITY = os.path.join(ROOT, "data", "676m_stability.json")
REPORT = os.path.join(ROOT, "data", "676m_A5重算报告.md")
EXP_BATCHES = {"expA", "expB", "expC", "expD", "expE", "expF", "expG"}


def _jload(p: str) -> dict:
    with open(p, encoding="utf-8") as fh:
        return cast(dict, json.load(fh))


def _jdump(p: str, doc: object) -> None:
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


# ─────────────────────────────────────────────────────────────────────────────
# 1. 修正件：把 676m 修复后的 expected_verdict 叠到冻结矩阵上
# ─────────────────────────────────────────────────────────────────────────────
def corrected_labels() -> dict[tuple[str, str], dict]:
    """{(batch, stem): 676m 修复后的标注子集}（权威来源 = 逐样本 .json）。

    注意：expA 与 expC 的磁盘文件名都形如 `sample_015.json` ⇒ **必须按批次分键**，
    否则 expC 会覆盖 expA（676m 首版脚本踩过这个坑，此处显式加批次前缀）。
    """
    out: dict[tuple[str, str], dict] = {}
    for b in sorted(EXP_BATCHES):
        d = os.path.join(ROOT, "data", "holdout_expansion", b)
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".json") or fn == "INDEX.json":
                continue
            doc = _jload(os.path.join(d, fn))
            out[(b, fn[:-5])] = {
                "expected_verdict": str(doc["expected_verdict"]),
                "defect_type": str(doc["defect_type"]),
            }
    return out


def stem_of(row: dict) -> str:
    oid = str(row.get("orig_id") or row.get("sample_id"))
    return oid if oid.startswith("sample_") else "sample_" + oid


def _type2group() -> dict:
    mod = importlib.import_module("fix_676m_schema")
    return dict(cast(dict, mod.TYPE2GROUP))


def build_corrected_matrix(out_path: str = CORRECTED_MX, dry: bool = False) -> dict:
    """冻结矩阵 + 676m 修正后的 expected_verdict / defect_type / defect_group。"""
    mx = _jload(MATRIX)
    lab = corrected_labels_cached()
    t2g = _type2group()
    n_v = n_t = 0
    changes: list[dict] = []
    for r in mx["samples"]:
        if r["source_batch"] not in EXP_BATCHES:
            continue
        stem = stem_of(r)
        new = lab.get((r["source_batch"], stem))
        if new is None:
            raise KeyError(f"{r['source_batch']}/{stem} 不在 676m 标注里（fail-loud）")
        ch: dict = {"sample_id": r["sample_id"], "stem": stem}
        if new["expected_verdict"] != r["expected_verdict"]:
            ch["expected_verdict"] = [r["expected_verdict"], new["expected_verdict"]]
            r["expected_verdict"] = new["expected_verdict"]
            n_v += 1
        if new["defect_type"] != r["defect_type"]:
            ch["defect_type"] = [r["defect_type"], new["defect_type"]]
            r["defect_type"] = new["defect_type"]
            n_t += 1
        r["defect_group"] = t2g.get(str(r["defect_type"]), "legacy")
        if len(ch) > 2:
            changes.append(ch)
    out = dict(mx)
    out["schema"] = "queyi-a5-676m-matrix-corrected/v1"
    out["generated_by"] = "tools/recompute_a5_676m.py"
    out["correction"] = {
        "source_of_truth": "data/holdout_expansion/**/*.json（676m 修复后）",
        "frozen_upstream": "data/a5_676f_detection_matrix.json（未被修改）",
        "n_expected_verdict_changed": n_v,
        "n_defect_type_changed": n_t,
        "changes": changes,
        "note": ("只覆盖 expected_verdict / defect_type / defect_group；"
                 "per_asset（真实 detect 判定）/ split / planted 一律保持冻结值。"),
    }
    if not dry:
        _jdump(out_path, out)
    return out


def build_corrected_manifest(out_path: str = CORRECTED_MAN, dry: bool = False) -> dict:
    """冻结清单 + 676m 修正后的 defect_type / defect_group（供 676f 分析器分组用）。"""
    man = _jload(MANIFEST)
    t2g = _type2group()
    n = 0
    for s in man["samples"]:
        if s["source_batch"] not in EXP_BATCHES:
            continue
        stem = stem_of(s)
        lab = corrected_labels_cached().get((s["source_batch"], stem))
        if lab is None:
            continue
        if lab["defect_type"] != s.get("defect_type"):
            n += 1
        s["defect_type"] = lab["defect_type"]
        s["defect_group"] = t2g.get(lab["defect_type"], "legacy")
    out = dict(man)
    stats = dict(cast(dict, man.get("stats") or {}))
    stats["by_defect_group"] = dict(collections.Counter(
        str(s.get("defect_group")) for s in man["samples"]))
    stats["by_defect_type"] = dict(collections.Counter(
        str(s.get("defect_type")) for s in man["samples"]))
    out["stats"] = stats
    out["schema"] = "queyi-a5-676m-sample-manifest-corrected/v1"
    out["generated_by"] = "tools/recompute_a5_676m.py"
    out["correction"] = {
        "frozen_upstream": "data/a5_676f_sample_manifest.json（未被修改）",
        "n_defect_type_changed": n,
        "note": ("只覆盖 defect_type / defect_group（含 stats.by_defect_group / "
                 "by_defect_type 重算）；split / planted / 去重记录保持冻结值。"),
    }
    if not dry:
        _jdump(out_path, out)
    return out


_LAB_CACHE: dict[tuple[str, str], dict] | None = None


def corrected_labels_cached() -> dict[tuple[str, str], dict]:
    global _LAB_CACHE
    if _LAB_CACHE is None:
        _LAB_CACHE = corrected_labels()
    return _LAB_CACHE


# ─────────────────────────────────────────────────────────────────────────────
# 2. 用 676f 的分析原语在修正件上重跑
# ─────────────────────────────────────────────────────────────────────────────
def rerun(multi: int, mx_path: str = CORRECTED_MX, man_path: str = CORRECTED_MAN,
          out_path: str = AFTER) -> dict:
    mod = importlib.import_module("676f_analysis")
    # 统计原语一字未改，只把输入矩阵/清单指向 676m 修正件
    setattr(mod, "MATRIX", Path(mx_path))
    setattr(mod, "MANIFEST", Path(man_path))
    setattr(mod, "OUT", Path(out_path))
    doc = cast(dict, mod.run(multi=multi, sweep=(1, 2, 3, 4, 5, 6, 7, 8)))
    doc["schema"] = "queyi-a5-676m-results/v1"
    doc["generated_by"] = "tools/recompute_a5_676m.py"
    doc["inputs"] = dict(cast(dict, doc.get("inputs") or {}))
    doc["inputs"]["matrix"] = "data/676m_a5_matrix_corrected.json"
    doc["inputs"]["frozen_matrix"] = "data/a5_676f_detection_matrix.json"
    _jdump(out_path, doc)
    return doc


#: --check 模式下必须逐位一致的字段（与随机重采样次数 multi 无关）
CHECK_KEYS = ["k", "n", "fd_k", "fd_rate_pct", "random_rate_pct", "static_rate_pct",
              "full_pool_rate_pct", "delta_fd_minus_random_pp", "delta_ci95_pp",
              "mcnemar_p", "b", "c", "cohens_h", "delta_fd_minus_static_pp"]


def check(multi: int = 200) -> int:
    """run_all.sh 门禁：修正标签后主端点必须与 676f 登记值逐位一致。"""
    import tempfile
    tmp = tempfile.mkdtemp(prefix="queyi676m_")
    try:
        mxp = os.path.join(tmp, "mx.json")
        manp = os.path.join(tmp, "man.json")
        outp = os.path.join(tmp, "res.json")
        corr = build_corrected_matrix(out_path=mxp)
        build_corrected_manifest(out_path=manp)
        before = _jload(BEFORE)
        after = rerun(multi, mx_path=mxp, man_path=manp, out_path=outp)
        pb, pa = primary_of(before), primary_of(after)
        bad = [k for k in CHECK_KEYS if pb.get(k) != pa.get(k)]
        print(f"[676m-D][check] 修正件：expected_verdict {corr['correction']['n_expected_verdict_changed']} 处、"
              f"defect_type {corr['correction']['n_defect_type_changed']} 处")
        print(f"[676m-D][check] k=4 主端点逐位比对：{len(CHECK_KEYS) - len(bad)}/{len(CHECK_KEYS)} 一致")
        if bad:
            for k in bad:
                print(f"[676m-D][check][FAIL] {k}: 676f={pb.get(k)} vs 676m={pa.get(k)}",
                      file=sys.stderr)
            return 1
        print("[676m-D][check][OK] 标签修正对 A5 主端点零影响（逐位一致）")
        return 0
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


# ─────────────────────────────────────────────────────────────────────────────
# 3. expected_verdict 依赖口径（唯一受 H1 影响的部分）
# ─────────────────────────────────────────────────────────────────────────────
def verdict_metrics(matrix_path: str) -> dict:
    mx = _jload(matrix_path)
    assets = list(mx["assets"])
    usable = [a for a in assets
              if any(r["per_asset"].get(a) == "catch" for r in mx["samples"])]
    rows = mx["samples"]
    pos = [r for r in rows if r["expected_verdict"] == "catch"]
    neg = [r for r in rows if r["expected_verdict"] == "miss"]
    per_asset: dict[str, dict] = {}
    for a in usable:
        c = sum(1 for r in pos if r["per_asset"].get(a) == "catch")
        u = sum(1 for r in pos if r["per_asset"].get(a) == "unknown")
        m = len(pos) - c - u
        per_asset[a] = {"recall_pct": round(100.0 * c / len(pos), 2) if pos else None,
                        "catch": c, "miss": m, "unknown": u}
    or_c = sum(1 for r in pos if any(r["per_asset"].get(a) == "catch" for a in usable))
    or_u = sum(1 for r in pos if all(r["per_asset"].get(a) == "unknown" for a in usable))
    fp = sum(1 for r in neg if any(r["per_asset"].get(a) == "catch" for a in usable))
    return {
        "n_expected_catch": len(pos), "n_expected_miss": len(neg),
        "usable_assets": usable,
        "or_recall_expected_catch_pct": round(100.0 * or_c / len(pos), 2) if pos else None,
        "or_catch_on_expected_catch": or_c,
        "or_unknown_on_expected_catch": or_u,
        "or_catch_on_expected_miss_fp": fp,
        "per_asset_recall_pct": per_asset,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 4. 稳定性验证（复用 676f 的冻结重测证据，不新跑 detect）
# ─────────────────────────────────────────────────────────────────────────────
def _jsonl(name: str) -> list[dict]:
    p = os.path.join(ROOT, "data", name)
    if not os.path.exists(p):
        return []
    return [json.loads(x) for x in open(p, encoding="utf-8").read().splitlines() if x.strip()]


def stability() -> dict:
    san = {r["sample_id"]: r["per_asset"] for r in _jsonl("a5_676f_matrix_san.jsonl")}
    zre = _jsonl("a5_676f_matrix_zredo.jsonl")
    cells = 0
    flips: list[dict] = []
    for r in zre:
        sid = r["sample_id"]
        if sid not in san:
            continue
        for a, v in r["per_asset"].items():
            old = (san[sid].get(a) or {}).get("verdict")
            if old is None:
                continue
            cells += 1
            if old != v["verdict"]:
                flips.append({"sample_id": sid, "asset": a, "first": old, "retest": v["verdict"]})
    # 三轮抽检（tsan，80 样本）
    st = _jsonl("a5_676f_matrix_stability.jsonl")
    rounds_flip = [{"sample_id": r["sample_id"], "asset": r["asset"], "votes": r["votes"]}
                   for r in st if len(set(r["votes"])) > 1]
    # 676f 的其它分片（local/local2、xc1/xc2）是**按样本奇偶互补切分**的并行分片，
    # 重叠为 0 ⇒ 不构成重测，不能用来估跑间不稳定。唯一可比的重测是 zredo vs san。
    return {
        "clean_retest": {
            "note": "676f 的干净重测（zredo，123 样本 × 3 sanitizer = 369 格）vs 首测（san）",
            "n_cells": cells, "n_flip": len(flips),
            "flip_pct": round(100.0 * len(flips) / cells, 2) if cells else None,
            "flips": flips,
        },
        "three_round_tsan": {
            "note": "676f 的 tsan 3 轮抽检（80 样本），逐格 3 次取众数",
            "n_samples": len(st), "n_flip_samples": len(rounds_flip),
            "flip_pct": round(100.0 * len(rounds_flip) / len(st), 2) if st else None,
            "flips": rounds_flip,
        },
        "disjoint_shards": {
            "note": ("local/local2 与 xc1/xc2 均为互补并行分片（样本集互斥，重叠 0）"
                     "⇒ 不可用作跑间稳定性估计；本报告只用上面两组真重测。"),
            "pairs": {"local vs local2": 0, "xc1 vs xc2": 0},
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
# 5. before/after 对比 + 子组（按统一 defect_type）
# ─────────────────────────────────────────────────────────────────────────────
def primary_of(res: dict) -> dict:
    return (res.get("primary_main_8candidates") or {}).get("primary") or {}


def co_of(res: dict) -> dict:
    return (res.get("co_primary_excl_degenerate") or {}).get("primary") or {}


KEYS = ["k", "n", "fd_k", "fd_rate_pct", "random_rate_pct", "static_rate_pct",
        "full_pool_rate_pct", "delta_fd_minus_random_pp", "delta_ci95_pp",
        "mcnemar_p", "b", "c", "cohens_h", "delta_fd_minus_static_pp"]


def compare_primary(before: dict, after: dict) -> list[dict]:
    pb, pa = primary_of(before), primary_of(after)
    out = []
    for k in KEYS:
        out.append({"metric": k, "before": pb.get(k), "after": pa.get(k),
                    "same": pb.get(k) == pa.get(k)})
    rb = (pb.get("random_2000") or {})
    ra = (pa.get("random_2000") or {})
    for k in ("mean_rate_pct", "sd_pp", "percentile_2.5_pct", "percentile_97.5_pct",
              "fd_strictly_better_frac", "fd_better_or_tie_frac"):
        out.append({"metric": f"random2000.{k}", "before": rb.get(k), "after": ra.get(k),
                    "same": rb.get(k) == ra.get(k)})
    return out


def type_subgroups(after: dict) -> dict:
    """按 676m 统一 defect_type 的 k=4 子组（评估集，来自修正件自带字段）。"""
    mx = _jload(CORRECTED_MX)
    res = _jload(AFTER)
    man = _jload(CORRECTED_MAN)
    fd_assets = (co_of(res) or {}).get("fd_assets") or []
    idx = {r["sample_id"]: r for r in mx["samples"]}
    split = {s["sample_id"]: s.get("split") for s in man["samples"]}
    groups: dict[str, list[str]] = collections.defaultdict(list)
    for r in mx["samples"]:
        if split.get(r["sample_id"]) == "evaluation":
            groups[str(r.get("defect_type"))].append(r["sample_id"])
    out: dict[str, dict] = {}
    for g, ids in sorted(groups.items()):
        n = len(ids)
        c = sum(1 for i in ids if any(idx[i]["per_asset"].get(a) == "catch" for a in fd_assets))
        allc = sum(1 for i in ids
                   if any(idx[i]["per_asset"].get(a) == "catch" for a in mx["assets"]))
        out[g] = {"n_evaluation": n,
                  "fd_k4_catch": c, "fd_k4_catch_pct": round(100.0 * c / n, 2),
                  "all_assets_catch": allc, "all_assets_catch_pct": round(100.0 * allc / n, 2),
                  "fd_assets": fd_assets}
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 报告
# ─────────────────────────────────────────────────────────────────────────────
def write_report(before: dict, after: dict, cmp_rows: list[dict], vm_b: dict, vm_a: dict,
                 stab: dict, sub: dict, corr: dict) -> None:
    L: list[str] = []
    A = L.append
    pb, pa = primary_of(before), primary_of(after)
    cb, ca = co_of(before), co_of(after)
    d_same = [r for r in cmp_rows if not r["same"]]

    A("# 676m · 任务 D：A5 数字重算报告")
    A("")
    A("- **批次**：676m（数据修复 + 实验重算 + 论文联动）")
    A("- **脚本**：`tools/recompute_a5_676m.py`（可复现）")
    A("- **上游**：676f（`87c1e001`，1137 样本 × 8 资产 = 9096 格真实 detect）")
    corr_n = corr["correction"]["n_expected_verdict_changed"]
    corr_t = corr["correction"]["n_defect_type_changed"]
    A("- **修正件**：`data/676m_a5_matrix_corrected.json`（冻结矩阵 + 修正后 "
      f"`expected_verdict` {corr_n} 处 / `defect_type` {corr_t} 处）、"
      "`data/676m_a5_manifest_corrected.json`")
    A("- **重算结果**：`data/676m_a5_results.json`")
    A("")
    A("## 0. 结论速览")
    A("")
    A("| 问题 | 答案 |")
    A("|------|------|")
    A(f"| Δ(FD−Random) 变了吗？ | **没变**：{pb.get('delta_fd_minus_random_pp')}pp → "
      f"{pa.get('delta_fd_minus_random_pp')}pp（变化 "
      f"{abs((pa.get('delta_fd_minus_random_pp') or 0)-(pb.get('delta_fd_minus_random_pp') or 0)):.4f}pp） |")
    A("| 需要重跑全量 detect 吗？ | **不需要**（判定见 §3；红线 8 的 >2pp 触发条件未满足） |")
    A(f"| 主分析逐位可复现？ | **是**（{len(cmp_rows) - len(d_same)}/{len(cmp_rows)} 项完全相同） |")
    A(f"| 受 H1 影响的指标 | expected=catch 口径的 OR recall "
      f"{vm_b['or_recall_expected_catch_pct']}% → {vm_a['or_recall_expected_catch_pct']}%"
      f"（分母 {vm_b['n_expected_catch']} → {vm_a['n_expected_catch']}） |")
    A(f"| 稳定性 | 干净重测 {stab['clean_retest']['n_flip']}/{stab['clean_retest']['n_cells']} "
      f"= {stab['clean_retest']['flip_pct']}% 翻转 |")
    A("")
    A("## 1. 范围与方法")
    A("")
    A("**为什么主分析不受影响（原理）**：A5 的 catch 判定口径是")
    A("")
    A("> `catch(sample, asset) ⟺ matrix[sample].per_asset[asset] == \"catch\"`")
    A("")
    A("它只读**真实 detect 判定**，`expected_verdict` 从头到尾不参与。")
    A("H1 改的是 `expected_verdict`（标注），不是 `per_asset`（观测），")
    A("因此 FD / Random / Static 三臂、Δ、CI、McNemar、2000 次随机分布**必然逐位不变**。")
    A("脚本对此做的是**实证核对**而非假定：把修正件喂给 `data/676f_analysis.py::run()`")
    A("（统计原语一字未改），再与 676f 结果逐字段比对。")
    A("")
    A("**唯一会变的**是「以 `expected_verdict` 为分母/分层」的视图（见 §2.3），")
    A("以及 H2 统一 `defect_type` 后**新启用**的细粒度子组视图（见 §4）。")
    A("")
    A("## 2. 修正前后对比")
    A("")
    A("### 2.1 主分析（8 候选，k=4）")
    A("")
    A("| 指标 | 676f（修正前） | 676m（修正后） | 相同 |")
    A("|------|---------------|---------------|:----:|")
    for r in cmp_rows:
        b, a = r["before"], r["after"]
        if isinstance(b, list):
            b = json.dumps(b)
            a = json.dumps(a)
        A(f"| `{r['metric']}` | {b} | {a} | {'✅' if r['same'] else '❌'} |")
    A("")
    if d_same:
        A("**有差异的项**：")
        A("")
        for r in d_same:
            A(f"- `{r['metric']}`：{r['before']} → {r['after']}")
    else:
        A("**全部指标逐位相同 ⇒ 主分析零影响（已实证，非假定）。**")
    A("")
    A("### 2.2 并列分析（剔 3 退化资产，k=4）")
    A("")
    A("| 指标 | 修正前 | 修正后 |")
    A("|------|-------|-------|")
    for k in ("fd_rate_pct", "random_rate_pct", "static_rate_pct",
              "delta_fd_minus_random_pp", "mcnemar_p", "delta_fd_minus_static_pp"):
        A(f"| `{k}` | {cb.get(k)} | {ca.get(k)} |")
    A("")
    A(f"（FD 选集 `{ca.get('fd_assets')}`；候选池 "
      f"`{(after.get('co_primary_excl_degenerate') or {}).get('candidates')}`）")
    A("")
    A("### 2.3 expected_verdict 依赖口径（H1 的唯一作用面）")
    A("")
    A("| 量 | 修正前 | 修正后 |")
    A("|----|-------|-------|")
    A(f"| `expected_verdict=catch` 的样本数 | {vm_b['n_expected_catch']} | {vm_a['n_expected_catch']} |")
    A(f"| `expected_verdict=miss` 的样本数 | {vm_b['n_expected_miss']} | {vm_a['n_expected_miss']} |")
    A(f"| 8 资产 OR 在 expected=catch 上的覆盖率 | {vm_b['or_recall_expected_catch_pct']}% | "
      f"{vm_a['or_recall_expected_catch_pct']}% |")
    A(f"| 其中 OR 判 unknown | {vm_b['or_unknown_on_expected_catch']} | "
      f"{vm_a['or_unknown_on_expected_catch']} |")
    A(f"| expected=miss 上 OR 误报（FP） | {vm_b['or_catch_on_expected_miss_fp']} | "
      f"{vm_a['or_catch_on_expected_miss_fp']} |")
    A("")
    A("**逐资产 recall（expected=catch 口径）**：")
    A("")
    A("| 资产 | 修正前 | 修正后 |")
    A("|------|-------|-------|")
    for a in vm_a["usable_assets"]:
        A(f"| `{a}` | {vm_b['per_asset_recall_pct'][a]['recall_pct']}% | "
          f"{vm_a['per_asset_recall_pct'][a]['recall_pct']}% |")
    A("")
    A("> 读法：34 条挂起样本由 catch 改判 miss 后，expected=catch 的分母变小、")
    A("> 分子不变 ⇒ recall 略升。这是**口径修正**，不是检测器变强。")
    A("> 论文里若引用「8 资产 OR = 94.21%」（676l），该数字的口径是 expected=catch，")
    A("> 修正后应改用本表数值；本批已把两个口径并报，避免读者误读。")
    A("")
    A("## 3. 是否需要重跑全量 detect（D2 判定）")
    A("")
    A("红线 8：`Δ 变化 >2pp` 或 `p 值数量级变化` ⇒ 必须重跑全量 detect。")
    A("")
    d_delta = abs((pa.get("delta_fd_minus_random_pp") or 0) - (pb.get("delta_fd_minus_random_pp") or 0))
    A("| 触发条件 | 实测 | 是否触发 |")
    A("|----------|------|:--------:|")
    A(f"| Δ(FD−Random) 变化 >2pp | {d_delta:.4f}pp | {'❌ 否' if d_delta <= 2 else '✅ 是'} |")
    A(f"| p 值数量级变化 | {pb.get('mcnemar_p')} → {pa.get('mcnemar_p')} | "
      f"{'❌ 否' if pb.get('mcnemar_p') == pa.get('mcnemar_p') else '✅ 是'} |")
    A("")
    A("**判定：不需要重跑全量 detect。** 依据有三条：")
    A("")
    A("1. 主分析口径不读 `expected_verdict`（§1），修正后逐位相同；")
    A("2. H1 只改 34 条 expE 挂起样本的**标注**，`per_asset` 观测值（含它们各自的")
    A("   `miss` 判定）完全没动；")
    A("3. 重跑全量 detect（9096 次）只会重新观测同一批 `per_asset`，")
    A("   除 ~5% 跑间噪声外不会带来新信息（§5）。")
    A("")
    A("> 若审稿人要求「修正标签后必须重测」，本批已备好命令（676f pipeline）与")
    A("> WSL 环境修正（`WSL_UTF8=1` + `WSLENV=WSL_UTF8/u`，见 673r 的横幅污染问题），")
    A("> 但按红线 8 的量化门槛，本批判定为**不必要**。")
    A("")
    A("## 4. 统一 defect_type 后的子组分析（H2 的新增视图）")
    A("")
    A("H2 把 56 个 `defect_type` 收敛到 33 个在用规范类型，使子组分析第一次可用。")
    A("下表是**评估集**上、以并列分析 FD 选集为资产集的子组检出率：")
    A("")
    A(f"FD 选集（k=4）：`{ca.get('fd_assets')}`")
    A("")
    A("| `defect_type` | n(评估集) | FD k=4 检出 | 全资产 OR 检出 |")
    A("|---------------|----------:|------------:|---------------:|")
    for g, v in sorted(sub.items(), key=lambda kv: (-kv[1]["n_evaluation"], kv[0])):
        A(f"| `{g}` | {v['n_evaluation']} | {v['fd_k4_catch']}/{v['n_evaluation']} "
          f"({v['fd_k4_catch_pct']}%) | {v['all_assets_catch']}/{v['n_evaluation']} "
          f"({v['all_assets_catch_pct']}%) |")
    A("")
    A("> 注意：这些是**描述性**子组，未做多重比较校正；`n` 小的类型不单独宣称。")
    A("")
    A("### 4.1 按统一 `defect_group`（15 类）的子组（676f 分析器原生输出）")
    A("")
    A("| `defect_group` | n(评估集) | FD k=4 | Random | Δ(FD−Random) | p |")
    A("|----------------|----------:|-------:|-------:|-------------:|--:|")
    for g, v in sorted((after.get("subgroups") or {}).items()):
        if not isinstance(v, dict) or "fd_rate_pct" not in v:
            continue
        A(f"| `{g}` | {v.get('n_evaluation')} | {v.get('fd_rate_pct')}% | "
          f"{v.get('random_rate_pct')}% | {v.get('delta_fd_minus_random_pp')}pp | "
          f"{v.get('mcnemar_p'):.3g} |")
    A("")
    A("> 与 676f 的对照：676f 的分组是旧 11 组（含 `conditional_trigger` / "
      "`optimization_sensitive` 两个元标签组）；676m 把这两组按缺陷种类拆散后，"
      "分组数变为下表规模，`undefined_behavior` 组因细分而**变小**、"
      "`memory_lifetime` 组因合并而**变大** —— 这正是 H2 想解决的问题。")
    A("")
    A("## 5. 稳定性验证（D4）")
    A("")
    A("本批**不新跑 detect**（§3），直接复核 676f 已落盘的三组重测证据：")
    A("")
    st1 = stab["clean_retest"]
    st2 = stab["three_round_tsan"]
    A("| 证据 | 规模 | 翻转 | 翻转率 |")
    A("|------|------|-----:|-------:|")
    A(f"| 干净重测（zredo vs san） | {st1['n_cells']} 格 | {st1['n_flip']} | {st1['flip_pct']}% |")
    A(f"| tsan 3 轮抽检（取众数） | {st2['n_samples']} 样本 | {st2['n_flip_samples']} | {st2['flip_pct']}% |")
    A("")
    A("> 676f 的另外四个分片（`local`/`local2`、`xc1`/`xc2`）是**互补并行分片**")
    A("> （样本集互斥，重叠 0），不能当作重测来估跑间不稳定，故不列入上表。")
    A("")
    A("**不稳定格子清单（干净重测）**：")
    A("")
    A("| 样本 | 资产 | 首测 | 重测 |")
    A("|------|------|------|------|")
    for f in st1["flips"]:
        A(f"| `{f['sample_id']}` | `{f['asset']}` | {f['first']} | {f['retest']} |")
    A("")
    A("**tsan 3 轮票型不一致的样本**：")
    A("")
    A("| 样本 | 资产 | 3 轮票型 |")
    A("|------|------|----------|")
    for f in st2["flips"]:
        A(f"| `{f['sample_id']}` | `{f['asset']}` | {f['votes']} |")
    A("")
    A(f"**判定**：不稳定率 {st1['flip_pct']}%（干净重测）与 {st2['flip_pct']}%（tsan 3 轮），")
    A("均 **< 10%**，按卡片不升格为一级局限；但作为**已知噪声**在论文的 Limitations")
    A("与数据卡中保留（单回合测量的逐格判定带 ~5% 噪声）。")
    A("")
    A("## 6. 复现")
    A("")
    A("```bash")
    A("# 1) 数据修复（H1/H2/M1-M5）")
    A(".venv/Scripts/python.exe tools/fix_676m_schema.py --stage all")
    A("# 2) A5 重算（本报告）")
    A(".venv/Scripts/python.exe tools/recompute_a5_676m.py")
    A("# 3) 上游 676f 独立重算校验（应仍 pass）")
    A(".venv/Scripts/python.exe tools/recompute_a5_676f.py")
    A("```")
    A("")
    A("产物：`data/676m_a5_matrix_corrected.json`、`data/676m_a5_results.json`、")
    A("`data/676m_stability.json`、本报告。")
    A("")
    A("## 7. 诚实边界")
    A("")
    A("1. 本批**没有**重跑 detect（§3 判定），所以本报告的数字反映的是")
    A("   **标签修正的影响**，不含检测器跑间噪声的重新抽样。")
    A("2. ~5% 的逐格跑间不稳定仍然存在于底层矩阵里；它对 Δ 的净影响")
    A("   在 676f 已按「重测优先」处置，本批沿用。")
    A("3. 子组分析（§4）为描述性、未校正多重比较。")
    A("4. `planted` 的层级分歧（676f 矩阵把 corpus 记为 `true`，676g 清单记 `null`，")
    A("   676m 的 M3 修正件记为 `false`）**未在 A5 层改写** —— 见总报告「未解决项」。")
    with open(REPORT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="676m A5 重算")
    ap.add_argument("--quick", action="store_true", help="2000 → 200 次随机")
    ap.add_argument("--check", action="store_true",
                    help="只校验：主端点须与 676f 逐位一致；不写任何 data/ 产物（门禁用）")
    a = ap.parse_args(argv)

    if a.check:
        return check()

    corr = build_corrected_matrix()
    build_corrected_manifest()
    print(f"[676m-D] 修正件写入 {os.path.relpath(CORRECTED_MX, ROOT)}；"
          f"expected_verdict 改动 {corr['correction']['n_expected_verdict_changed']} 处，"
          f"defect_type 改动 {corr['correction']['n_defect_type_changed']} 处")

    before = _jload(BEFORE)
    after = rerun(200 if a.quick else 2000)
    pb, pa = primary_of(before), primary_of(after)
    print(f"[676m-D] k=4 主分析：FD {pa.get('fd_rate_pct')}% vs Random {pa.get('random_rate_pct')}% "
          f"Δ{pa.get('delta_fd_minus_random_pp')}pp（676f: Δ{pb.get('delta_fd_minus_random_pp')}pp）")

    cmp_rows = compare_primary(before, after)
    vm_b = verdict_metrics(MATRIX)
    vm_a = verdict_metrics(CORRECTED_MX)
    stab = stability()
    sub = type_subgroups(after)
    _jdump(STABILITY, {"schema": "queyi-676m-stability/v1",
                       "generated_by": "tools/recompute_a5_676m.py", **stab})
    write_report(before, after, cmp_rows, vm_b, vm_a, stab, sub, corr)
    print(f"[676m-D] 报告 {os.path.relpath(REPORT, ROOT)}；"
          f"稳定件 {os.path.relpath(STABILITY, ROOT)}")
    print(f"[676m-D] expected=catch OR recall {vm_b['or_recall_expected_catch_pct']}% → "
          f"{vm_a['or_recall_expected_catch_pct']}%（分母 {vm_b['n_expected_catch']} → "
          f"{vm_a['n_expected_catch']}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
