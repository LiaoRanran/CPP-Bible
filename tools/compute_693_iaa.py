#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_693_iaa.py — 693-A4：人类裁决回来后的一致性统计（现在不跑）。

状态：**已就绪、未执行**。``data/693_human_adjudication_package.csv`` 的
``human_verdict`` 列当前全为空，脚本会自动以 ``status=pending`` 退出并写占位报告。

设计要点
========
1. **绝不填补**：``human_verdict`` 为空的条目一律跳过，绝不推断、绝不默认。
2. **三组配对**都算：人 vs A（主指标）、人 vs B、A vs B（对照）。
3. **泄漏敏感性**：13 条源码残留 ``expected_verdict`` 注释的样本单列 κ。
4. **κ 与 agreement 并列**：类别强偏斜时 κ 会误导，必须一起读。

用法
====
    python tools/compute_693_iaa.py
    python tools/compute_693_iaa.py --csv <path> --json <out.json> --md <out.md>

输出
====
* ``data/693_human_iaa.json``
* ``data/693_human_iaa_report.md``
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "693_human_adjudication_package.csv"
DOUBLE = ROOT / "data" / "693_ai_double_label.json"
OUT_JSON = ROOT / "data" / "693_human_iaa.json"
OUT_MD = ROOT / "data" / "693_human_iaa_report.md"

VERDICTS = ("catch", "miss", "unknown", "contradiction")
THRESHOLD_KAPPA = 0.8  # 689 协议 §6 预注册：verdict κ≥0.8


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def cohen_kappa(a: list[str], b: list[str]) -> float | None:
    """Cohen's κ（标准库实现）；n=0 返回 None；pe→1 且非完全一致返回 None。"""
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


def _norm(v: str) -> str:
    """归一化 human_verdict：容忍大小写/中英文/简写。"""
    s = (v or "").strip().lower()
    table = {
        "catch": "catch", "c": "catch", "是": "catch", "有报告": "catch", "1": "catch",
        "miss": "miss", "m": "miss", "否": "miss", "无报告": "miss", "0": "miss",
        "unknown": "unknown", "u": "unknown", "?": "unknown", "不确定": "unknown",
        "contradiction": "contradiction", "x": "contradiction", "矛盾": "contradiction",
    }
    return table.get(s, s)


def _pair_stats(pairs: list[tuple[str, str]]) -> dict[str, Any]:
    """给定配对序列，算 n / raw agreement% / κ / 混淆矩阵 / 分歧数。"""
    n = len(pairs)
    if n == 0:
        return {"n": 0, "raw_agreement_pct": None, "kappa": None,
                "confusion": {}, "n_disagree": 0, "distributions": {}}
    a = [x for x, _ in pairs]
    b = [y for _, y in pairs]
    agree = sum(1 for x, y in pairs if x == y)
    labels = sorted(set(a) | set(b))
    confusion = {x: {y: sum(1 for p, q in pairs if p == x and q == y) for y in labels}
                 for x in labels}
    return {
        "n": n,
        "raw_agreement_pct": round(agree / n * 100.0, 2),
        "kappa": round(kappa, 4) if (kappa := cohen_kappa(a, b)) is not None else None,
        "confusion": confusion,
        "n_disagree": n - agree,
        "distributions": {"human_or_left": dict(Counter(a)), "reference_or_right": dict(Counter(b))},
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(DEFAULT_CSV))
    ap.add_argument("--json", dest="json_out", default=str(OUT_JSON))
    ap.add_argument("--md", dest="md_out", default=str(OUT_MD))
    args = ap.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(f"[693-A4] 找不到裁决表：{csv_path}")

    rows: list[dict[str, str]] = []
    with csv_path.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            rows.append({k: (v or "").strip() for k, v in r.items() if k is not None})

    filled = [r for r in rows if _norm(r.get("human_verdict", "")) in VERDICTS]
    doc: dict[str, Any] = {
        "schema": "queyi-693-human-iaa/v1",
        "generated_by": "tools/compute_693_iaa.py",
        "generated_at": _now(),
        "input_csv": str(csv_path),
        "n_rows": len(rows),
        "n_filled": len(filled),
        "threshold": {"verdict_kappa": THRESHOLD_KAPPA, "source": "689 协议 §6 预注册"},
        "status": "analyzed" if filled else "pending",
    }

    if not filled:
        doc["note"] = ("human_verdict 列为空：人类裁决尚未执行，脚本已就绪但未产生任何统计。"
                       "填完后重跑本脚本即出 κ / agreement% / 混淆矩阵。")
        Path(args.json_out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                       encoding="utf-8", newline="\n")
        Path(args.md_out).write_text(_md(doc), encoding="utf-8", newline="\n")
        print(f"[693-A4] 未检测到已填裁决（0/{len(rows)}）；已输出占位报告 status=pending。")
        return

    dbl = json.loads(DOUBLE.read_text(encoding="utf-8"))
    a_of = {s["anon_id"]: s["annotator_a"]["verdict"] for s in dbl["per_sample"]}
    b_of = {s["anon_id"]: s["annotator_b"]["verdict"] for s in dbl["per_sample"]}
    leak_of = {s["anon_id"]: bool(s["leak_exposed"]) for s in dbl["per_sample"]}

    h_vs_a: list[tuple[str, str]] = []
    h_vs_b: list[tuple[str, str]] = []
    a_vs_b: list[tuple[str, str]] = []
    clean_h_vs_a: list[tuple[str, str]] = []
    per_item: list[dict[str, Any]] = []
    invalid: list[str] = []

    for r in rows:
        sid = r.get("sample_id", "")
        raw = r.get("human_verdict", "")
        hv = _norm(raw)
        if not raw:
            continue
        if hv not in VERDICTS:
            invalid.append(f"{sid}:{raw!r}")
            continue
        av, bv = a_of.get(sid, ""), b_of.get(sid, "")
        h_vs_a.append((hv, av))
        h_vs_b.append((hv, bv))
        if av and bv:
            a_vs_b.append((av, bv))
        if not leak_of.get(sid, False):
            clean_h_vs_a.append((hv, av))
        per_item.append({
            "sample_id": sid,
            "human": hv, "annotator_a": av, "annotator_b": bv,
            "human_agrees_with_a": hv == av,
            "human_agrees_with_b": hv == bv,
            "leak_exposed": leak_of.get(sid, False),
            "human_note": r.get("human_note", ""),
        })

    doc["invalid_verdicts"] = invalid
    doc["pairwise"] = {
        "human_vs_A": _pair_stats(h_vs_a),
        "human_vs_B": _pair_stats(h_vs_b),
        "A_vs_B": _pair_stats(a_vs_b),
    }
    doc["sensitivity_excluding_leak"] = {
        "human_vs_A": _pair_stats(clean_h_vs_a),
        "n_excluded": sum(1 for p in per_item if p["leak_exposed"]),
    }
    doc["threshold_check"] = {
        k: (v["kappa"] is not None and v["kappa"] >= THRESHOLD_KAPPA)
        for k, v in doc["pairwise"].items() if v["n"] > 0
    }
    doc["per_item"] = per_item
    doc["adjudication_outcome"] = {
        "human_sided_with_A": sum(1 for p in per_item if p["human_agrees_with_a"]),
        "human_sided_with_B": sum(1 for p in per_item if p["human_agrees_with_b"]),
        "human_sided_with_neither": sum(
            1 for p in per_item
            if not p["human_agrees_with_a"] and not p["human_agrees_with_b"]),
    }

    Path(args.json_out).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                   encoding="utf-8", newline="\n")
    Path(args.md_out).write_text(_md(doc), encoding="utf-8", newline="\n")
    print(f"[693-A4] 已分析 {len(filled)} 条；human vs A κ="
          f"{doc['pairwise']['human_vs_A']['kappa']}")


def _md(doc: dict[str, Any]) -> str:
    lines = [
        "# 693-A4 · 人类裁决一致性报告",
        "",
        f"- 生成：{doc['generated_at']}｜脚本：tools/compute_693_iaa.py",
        f"- 状态：**{doc['status']}**",
        f"- 裁决表 {doc['input_csv']}：共 {doc['n_rows']} 行，已填 {doc['n_filled']} 行。",
        f"- 预注册阈值：verdict κ ≥ {doc['threshold']['verdict_kappa']}（{doc['threshold']['source']}）",
        "",
    ]
    if doc["status"] == "pending":
        lines += [f"> {doc.get('note', '')}", ""]
        return "\n".join(lines)
    lines += [
        "## 1. 三组配对的一致性",
        "",
        "| 配对 | n | raw agreement% | 分歧数 | Cohen's κ | 达标(κ≥0.8) |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for k, v in doc["pairwise"].items():
        if v["n"] == 0:
            continue
        kap = "—" if v["kappa"] is None else f"{v['kappa']:.3f}"
        ok = doc["threshold_check"].get(k)
        lines.append(f"| {k} | {v['n']} | {v['raw_agreement_pct']:.1f} | {v['n_disagree']} | "
                     f"{kap} | {'✅' if ok else '❌'} |")
    lines += [
        "",
        "## 2. 泄漏敏感性（剔除 13 条源码残留标签的样本）",
        "",
        f"- human vs A：n={doc['sensitivity_excluding_leak']['human_vs_A']['n']}，"
        f"κ={doc['sensitivity_excluding_leak']['human_vs_A']['kappa']}，"
        f"剔除 {doc['sensitivity_excluding_leak']['n_excluded']} 条。",
        "",
        "## 3. 裁决去向",
        "",
        f"- 站 A：{doc['adjudication_outcome']['human_sided_with_A']} 条；"
        f"站 B：{doc['adjudication_outcome']['human_sided_with_B']} 条；"
        f"两边都不站（unknown/contradiction 或第三结论）："
        f"{doc['adjudication_outcome']['human_sided_with_neither']} 条。",
        "",
        "## 4. 后续动作",
        "",
        "1. κ 达标 ⇒ 写入论文 §7 T1（标签有效性）：人类 IAA 不再为 0；",
        "2. κ 不达标 ⇒ 逐条看 `per_item` 里两边都不站的条目，判断是**标签错**还是**口径歧义**；",
        "3. 用人类裁决后的标签重算 A5 主端点 Δ 与盲区率（敏感性分析）。",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
