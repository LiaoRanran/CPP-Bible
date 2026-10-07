#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""analyze_annotation.py — 689-C2：人类标注一致性统计（第二标注者结果填入后即跑）。

用法
====
    python data/annotation_package/analyze_annotation.py            # 读同目录 annotation_template.csv
    python data/annotation_package/analyze_annotation.py --csv <path>

输入
====
* ``annotation_template.csv``（第二标注者填写；未填条目自动跳过并报告覆盖数）；
* ``data/689_annotation_key_mapping.json``（协调者密钥：anon_id → 原始标签）。

输出
====
* ``data/689_annotation_agreement.json``（逐字段 κ / agreement% / 分歧计数 / 分歧清单）；
* ``data/689_annotation_agreement_report.md``（可读报告，含预注册阈值判定）。

预注册阈值（689_human_annotation_protocol.md §6）
================================================
verdict κ≥0.8；family κ≥0.7；planted/severity κ≥0.6（宽松）。
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
from collections import Counter
from pathlib import Path
from typing import Any

PKG = Path(__file__).resolve().parent
ROOT = PKG.parents[1]
MAPPING = ROOT / "data" / "689_annotation_key_mapping.json"
OUT_JSON = ROOT / "data" / "689_annotation_agreement.json"
OUT_MD = ROOT / "data" / "689_annotation_agreement_report.md"

FIELDS = ("expected_verdict", "defect_type_family", "planted", "severity")
THRESHOLDS = {"expected_verdict": 0.8, "defect_type_family": 0.7, "planted": 0.6, "severity": 0.6}

FAMILIES = ("memory", "bounds", "integer", "alias_type", "concurrency", "stl",
            "language_oop", "embedded_link")


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def cohen_kappa(a: list[str], b: list[str]) -> float | None:
    """Cohen's κ（标准库实现）；样本为空或完全一致且单类时返回 None/1.0 语义由调用方处理。"""
    n = len(a)
    if n == 0:
        return None
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ca, cb = Counter(a), Counter(b)
    labels = set(ca) | set(cb)
    pe = sum((ca.get(k, 0) / n) * (cb.get(k, 0) / n) for k in labels)
    if pe >= 1.0:
        return 1.0 if po >= 1.0 else None
    return (po - pe) / (1.0 - pe)


def _norm_verdict(v: str) -> str:
    s = v.strip().lower()
    if s in ("catch", "c", "是", "有报告", "1"):
        return "catch"
    if s in ("miss", "m", "否", "无报告", "0"):
        return "miss"
    return s


def _norm_planted(v: str) -> str:
    s = v.strip().lower()
    if s in ("true", "t", "1", "是", "y", "yes"):
        return "true"
    if s in ("false", "f", "0", "否", "n", "no"):
        return "false"
    if s in ("unsure", "?", "不确定", "存疑"):
        return "unsure"
    return s


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(PKG / "annotation_template.csv"))
    args = ap.parse_args()

    mapping: dict[str, Any] = json.loads(MAPPING.read_text(encoding="utf-8"))
    key = {str(r["anon_id"]): r for r in mapping["rows"]}

    filled: list[dict[str, str]] = []
    with open(args.csv, encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            anon = (row.get("anon_id") or "").strip()
            if not anon:
                continue
            filled.append({k: (v or "").strip() for k, v in row.items() if k})

    have = [r for r in filled if r.get("expected_verdict(catch/miss)") or r.get("expected_verdict")]
    report: dict[str, Any] = {
        "schema": "queyi-689-annotation-agreement/v1",
        "generated_by": "data/annotation_package/analyze_annotation.py",
        "generated_at": _now(),
        "input_csv": str(args.csv),
        "n_expected": mapping["n_total"],
        "n_rows_in_csv": len(filled),
        "n_with_verdict": sum(1 for r in filled if (r.get("expected_verdict(catch/miss)") or "").strip()),
        "fields": {},
        "disagreements": [],
        "threshold_check": {},
        "status": "pending" if not have else "analyzed",
    }
    if not have:
        report["note"] = ("标注尚未填写（annotation_template.csv 为空）：本脚本已就绪，"
                          "第二标注者完成后重跑即可产出 κ/agreement%/分歧清单。")
        OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n",
                            encoding="utf-8", newline="\n")
        OUT_MD.write_text(_md(report), encoding="utf-8", newline="\n")
        print("[689-C2] 未检测到已填标注；已输出占位报告（status=pending）。")
        return

    pairs: dict[str, tuple[list[str], list[str]]] = {f: ([], []) for f in FIELDS}
    dis: list[dict[str, Any]] = []
    for r in filled:
        anon = r["anon_id"]
        k = key.get(anon)
        if k is None:
            continue
        mine = {
            "expected_verdict": _norm_verdict((r.get("expected_verdict(catch/miss)") or "").strip()),
            "defect_type_family": (r.get("defect_type_family") or "").strip(),
            "planted": _norm_planted((r.get("planted(true/false/unsure)") or "").strip()),
            "severity": (r.get("severity(low/medium/high)") or "").strip().lower(),
        }
        their = {
            "expected_verdict": str(k["expected_verdict"]),
            "defect_type_family": _family_of(str(k["defect_type"])),
            "planted": ("true" if k.get("planted") is True else
                        ("false" if k.get("planted") is False else "unsure")),
            "severity": "",  # 作者侧 severity 权威源为逐样本 JSON；材料包未载入 ⇒ 该字段跳过
        }
        for f in FIELDS:
            if not mine[f]:
                continue
            pairs[f][0].append(mine[f])
            pairs[f][1].append(their[f])
        bad = [f for f in ("expected_verdict", "defect_type_family") if mine[f] and mine[f] != their[f]]
        if bad:
            dis.append({"anon_id": anon, "uid": k["uid"], "fields": bad,
                        "annotator": {f: mine[f] for f in bad},
                        "author": {f: their[f] for f in bad}})

    for f in FIELDS:
        a, b = pairs[f]
        n = len(a)
        agree = sum(1 for x, y in zip(a, b) if x == y)
        entry: dict[str, Any] = {
            "n": n,
            "agreement_pct": (agree / n * 100.0) if n else None,
            "n_disagree": n - agree,
            "kappa": cohen_kappa(a, b) if n else None,
            "annotator_distribution": dict(Counter(a)),
            "author_distribution": dict(Counter(b)),
        }
        thr = THRESHOLDS.get(f)
        if thr is not None:
            kap = entry["kappa"]
            entry["threshold"] = thr
            entry["passes_threshold"] = bool(kap is not None and kap >= thr)
        report["fields"][f] = entry
    report["disagreements"] = dis
    report["threshold_check"] = {f: report["fields"][f].get("passes_threshold")
                                 for f in FIELDS if "passes_threshold" in report["fields"][f]}
    report["family_disagreement_counts"] = dict(Counter(
        x["annotator"].get("defect_type_family", "?") for x in dis
        if "defect_type_family" in x["fields"]))

    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")
    OUT_MD.write_text(_md(report), encoding="utf-8", newline="\n")
    print(f"[689-C2] 已分析 {report['n_with_verdict']} 条；"
          f"verdict κ={report['fields']['expected_verdict']['kappa']}")


def _family_of(defect_type: str) -> str:
    for fam, types in {
        "memory": ("memory_safety", "use_after_free", "double_free", "memory_leak",
                   "smart_pointer", "raii_violation", "move_semantics", "uninitialized_read"),
        "bounds": ("out_of_bounds", "null_pointer_deref"),
        "integer": ("integer_overflow", "bit_operation"),
        "alias_type": ("type_punning", "strict_aliasing", "alignment", "endianness"),
        "concurrency": ("data_race", "atomic_ub", "memory_order", "deadlock", "condition_variable"),
        "stl": ("iterator_invalidation", "stl_container_ub", "string_ub", "algorithm_misuse"),
        "language_oop": ("virtual_function", "lambda_capture", "logic_error", "cross_tu_ub", "other_ub"),
        "embedded_link": ("volatile_misuse", "register_ub", "interrupt_safety", "linker_odr"),
    }.items():
        if defect_type in types:
            return fam
    return "language_oop"


def _md(doc: dict[str, Any]) -> str:
    lines = [
        "# 689-C2 · 人类标注一致性报告（第二标注者）",
        "",
        f"- 生成：{doc['generated_at']}｜脚本：data/annotation_package/analyze_annotation.py",
        f"- 状态：**{doc['status']}**"
        + ("（标注未填：本报告为占位，填完后重跑即可）" if doc["status"] == "pending" else ""),
        f"- 材料包应有 {doc['n_expected']} 条；CSV 读到 {doc['n_rows_in_csv']} 行；"
        f"已填 verdict {doc['n_with_verdict']} 条。",
        "",
    ]
    if doc["status"] == "pending":
        lines += [doc.get("note", ""), ""]
        return "\n".join(lines)
    lines += [
        "## 1. 逐字段一致性（预注册阈值：verdict κ≥0.8；family κ≥0.7）",
        "",
        "| 字段 | n | agreement% | 分歧数 | Cohen's κ | 阈值 | 达标 |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for f, e in doc["fields"].items():
        kap = "—" if e["kappa"] is None else f"{e['kappa']:.3f}"
        ag = "—" if e["agreement_pct"] is None else f"{e['agreement_pct']:.1f}"
        thr = e.get("threshold", "—")
        ok = e.get("passes_threshold")
        lines.append(f"| {f} | {e['n']} | {ag} | {e['n_disagree']} | {kap} | {thr} | "
                     f"{'✅' if ok else ('❌' if ok is False else '—')} |")
    lines += [
        "",
        "> 注：κ 在类别强偏斜时会误导，必须与 agreement% 和分歧数并列阅读；"
        "`severity` 需作者侧权威逐样本 JSON 才能算（当前版本跳过，暴露为 —）。",
        "",
        "## 2. 分歧清单（verdict / family）",
        "",
    ]
    if doc["disagreements"]:
        lines += ["| anon_id | 字段 | 标注者 | 作者 |", "|---|---|---|---|"]
        for d in doc["disagreements"][:200]:
            for f in d["fields"]:
                lines.append(f"| {d['anon_id']} | {f} | {d['annotator'][f]} | {d['author'][f]} |")
    else:
        lines.append("（无分歧）")
    lines += [
        "",
        "## 3. 家族分歧集中度",
        "",
        f"- 分歧按标注家族计数：{json.dumps(doc.get('family_disagreement_counts', {}), ensure_ascii=False)}",
        "",
        "## 4. 后续动作",
        "",
        "1. 对分歧条目做双标注者盲讨论 → 仍不一致交第三方裁决（记录 `689_annotation_adjudication.md`）；",
        "2. 用第二标注标签重算：A5 主端点 Δ、盲区率、家族检出率（敏感性分析）；",
        "3. 把 κ 与敏感性结果写入论文 §7 T1（标签有效性）。",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
