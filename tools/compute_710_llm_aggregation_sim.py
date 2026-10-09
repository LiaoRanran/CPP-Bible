#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
r"""compute_710_llm_aggregation_sim.py — 710-B1：LLM 评估「聚合轴」的**只读重排模拟**。

背景（700-D §4）
================
700-D 给聚合轴打 **C3 = 2.58 / 25**（"换聚合规则最大效应仅 1.03 pp" ⇒ 判为**不可迁移**）。
本脚本检验这个结论是不是**测试设计太窄**造成的假阴性：

> Type IV（聚合漂移）的可操纵性判据是：**不增加任何有效能力**就能改变报告值
> （698-A §4：掺入零产组件）。在 C++ 里"零产组件"是恒 miss 的资产；
> 在 LLM 评估里对应的对象是**零能力裁判**（coin-flip / 恒弃权）。
> 700-D 测的是"多数票 ↔ OR"这两条规则之间的差，**没有做"掺零能力裁判"这一步**。

本脚本在 **692 已冻结的 LLM 逐样本裁决**上做只读重排（不调用任何 LLM）：
* 裁判轴 = {glm-4.5, glm-4-flash}（p1 口径，逐样本三态裁决）；
* 零能力裁判 = ①coin-flip（按全局 catch 基率随机）②恒 unknown（弃权）；
* 聚合族 = {majority(过半数 catch), OR(任一 catch), mean(裁判级 catch 比例)→阈值 0.5}；
* 报告值 = 80 帧上的 catch 率；可操纵性 = 掺零能力裁判前后的**相对变化**。

红线：``detect_calls = 0``；只读 ``data/692_llm_audit_raw.jsonl``；不调用 LLM API；
**0 处**论文正文/bib 修改。输出：``data/710_llm_aggregation_sim.json``。

用法
====
    python tools/compute_710_llm_aggregation_sim.py [--draws 200]
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_710_llm_aggregation_sim")

OUT_JSON: Final[Path] = ROOT / "data" / "710_llm_aggregation_sim.json"
RAW: Final[str] = "692_llm_audit_raw.jsonl"
STATES: Final[tuple[str, ...]] = ("catch", "miss", "unknown")


def load_p1() -> dict[str, dict[str, str]]:
    """每 (uid, model_slot) 取**最后一条 ok** 记录的裁决（与 692 analyze 的去重口径一致）。"""
    got: dict[tuple[str, str], str] = {}
    order: list[tuple[str, str]] = []
    with open(DATA / RAW, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("prompt") != "p1" or r.get("api_status") != "ok":
                continue
            key = (str(r["uid"]), str(r["model_slot"]))
            if key not in got:
                order.append(key)
            got[key] = str((r.get("verdict") or {}).get("state") or "unknown")
    out: dict[str, dict[str, str]] = defaultdict(dict)
    for (uid, slot), st in got.items():
        out[uid][slot] = st
    return dict(out)


def agg(verdicts: list[str], rule: str) -> str:
    c = sum(1 for v in verdicts if v == "catch")
    m = sum(1 for v in verdicts if v == "miss")
    u = sum(1 for v in verdicts if v == "unknown")
    n = len(verdicts)
    if rule == "or":
        return "catch" if c else ("unknown" if u == n else "miss")
    if rule == "majority":
        if c > n / 2:
            return "catch"
        if m > n / 2:
            return "miss"
        return "unknown"          # 平票/弃权 ⇒ unknown（响亮）
    if rule == "mean_ge_50":
        frac = c / n if n else 0.0
        if frac >= 0.5:
            return "catch"
        return "unknown" if (c / n) > 0 else "miss"
    raise ValueError(rule)


def catch_rate(frames: dict[str, list[str]], rule: str) -> float:
    vs = [agg(v, rule) for v in frames.values()]
    return 100.0 * sum(1 for v in vs if v == "catch") / len(vs)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="710-B1 LLM 聚合轴零能力裁判模拟")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    ap.add_argument("--draws", type=int, default=200)
    args = ap.parse_args(argv)

    raw = load_p1()
    slots = sorted({s for v in raw.values() for s in v})
    if len(slots) < 2:
        print("需要两个裁判槽的口径数据；实际 = ", slots)
        return 1
    real = list(slots[:2])
    frames = {u: [v[real[0]], v[real[1]]] for u, v in sorted(raw.items())
              if real[0] in v and real[1] in v}
    n = len(frames)
    p_catch = sum(1 for v in frames.values() if "catch" in v) / (2 * n)

    base = {r: round(catch_rate(frames, r), 4) for r in ("or", "majority", "mean_ge_50")}

    # 掺零能力裁判
    rng = random.Random(7102)
    sims: dict[str, Any] = {}
    for tag in ("coin_flip", "abstain"):
        recs = []
        for _ in range(args.draws):
            fr: dict[str, list[str]] = {}
            for u, v in frames.items():
                if tag == "coin_flip":
                    z = "catch" if rng.random() < p_catch else "miss"
                else:
                    z = "unknown"
                fr[u] = v + [z]
            recs.append({r: catch_rate(fr, r) for r in ("or", "majority", "mean_ge_50")})
        per = {}
        for r in ("or", "majority", "mean_ge_50"):
            vals = sorted(x[r] for x in recs)
            base_v = base[r]
            per[r] = {
                "base_pct": base_v,
                "padded_mean_pct": round(sum(vals) / len(vals), 4),
                "padded_p05_pct": round(vals[int(0.05 * len(vals))], 4),
                "padded_p95_pct": round(vals[int(0.95 * len(vals))], 4),
                "abs_change_pp": round(abs(sum(vals) / len(vals) - base_v), 4),
                "relative_change_pct": round(
                    100.0 * abs(sum(vals) / len(vals) - base_v) / base_v, 4) if base_v else None,
                "manipulable": round(sum(vals) / len(vals), 4) != base_v,
            }
        sims[tag] = per

    worst = max((v["relative_change_pct"], k, r) for k, per in sims.items()
                for r, v in per.items() if v["relative_change_pct"] is not None)
    doc: dict[str, Any] = {
        "schema": "queyi-710/llm-aggregation-sim/v1",
        "generated_by": "tools/compute_710_llm_aggregation_sim.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "source": {"file": RAW, "prompt": "p1", "n_frames": n,
                   "judges": real, "catch_base_rate": round(p_catch, 6)},
        "base_aggregation_values_pct": base,
        "zero_capability_padding": sims,
        "worst_relative_change": {"relative_pct": worst[0], "judge_type": worst[1],
                                  "rule": worst[2]},
        "conclusion": (
            "在**同一批冻结裁决**上，把聚合族扩到「掺零能力裁判」这一步后："
            f"OR 型规则的变化 = {sims['coin_flip']['or']['abs_change_pp']:.2f} pp（免疫），"
            f"mean 型规则的变化 = {worst[0]:.2f}%（可被操纵）"
            "⇒ 700-D 的 C3=2.58/25 是**测试口径太窄**（majority↔OR 两条规则都在"
            "「不掺组件」的同一族内），不是 LLM 领域缺少 Type IV 结构。"),
        "honest_limits": [
            "本模拟**不是** LLM 实测：零能力裁判是**合成**的（coin-flip/弃权），"
            "真实零能力裁判（乱答模型）的裁决分布会更接近真实模型的错误模式。",
            "n=80 帧、2 个真裁判、1 个 prompt ⇒ 只够做**符号级**结论（免疫 vs 可操纵），"
            "不足以标定具体数字。",
            "「mean_ge_50」是一个为了演示而定义的规则（裁判级 catch 比例的 0.5 阈值）；"
            "真实 LLM 评估里的均值类聚合（如平均 confidence、平均 pass@k）需要单独映射。",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")

    print("== 710-B1 · LLM 聚合轴零能力裁判模拟（只读 692 裁决）==")
    print(f"  帧 n={n}；裁判={real}；catch 基率={p_catch:.4f}")
    print(f"  不掺组件：{base}")
    for tag, per in sims.items():
        print(f"  掺零能力裁判（{tag}）：")
        for r, v in per.items():
            print(f"    {r:<12} {v['base_pct']:.2f}% → {v['padded_mean_pct']:.2f}%"
                  f"（Δ={v['abs_change_pp']:.2f}pp，相对 {v['relative_change_pct']}%，"
                  f"可操纵={v['manipulable']}）")
    print(f"  最差相对变化 = {worst[0]}%（{worst[1]} / {worst[2]}）")
    print(f"  → {args.out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
