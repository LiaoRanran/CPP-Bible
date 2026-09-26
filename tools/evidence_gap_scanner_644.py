"""644 阶段 E · E1 全库证据不足扫描。

对 28(27) 张卡片全量跑 B2（证据充分性）：
- 哪些卡证据不足？  缺什么类型的证据？（L1 实测 / L2 标准 / 反例 / 多源）
- 优先级排序；Top 10 最需补证据的卡片。

只读：不修改受控目录。`--check` 只读幂等；`--report` 写不足扫描报告。
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base
import evidence_sufficiency_644 as b2

OUT_MD = os.path.join(base.ROOT, "data", "644_gap_scan_report.md")


def missing_types(rec: dict[str, Any]) -> list[str]:
    out: list[str] = []
    if not rec["has_strong"]:
        out.append("L1/L2 权威证据")
    if rec["independent_count"] < b2.MIN_INDEPENDENT:
        out.append(f"多源(≥{b2.MIN_INDEPENDENT})")
    if not rec["refute_handled"]:
        out.append("反例处理")
    if rec["expired"]:
        out.append("时效性")
    if not rec["hash_consistent"]:
        out.append("hash 一致性")
    return out


def scan() -> dict[str, Any]:
    suf = b2.judge_all()
    gaps = []
    for r in suf:
        if r["verdict"] != "充分":
            prio = len(r["missing"]) + (2 if r["verdict"] == "需人审" else 0)
            gaps.append({"card": r["card"], "verdict": r["verdict"], "n_evidence": r["n_evidence"],
                         "missing": missing_types(r), "priority": prio})
    gaps.sort(key=lambda g: (-g["priority"], g["card"]))
    top10 = gaps[:10]
    return {"n_cards": len(suf), "n_gaps": len(gaps),
            "gaps": gaps, "top10": top10}


def render_md(s: dict[str, Any]) -> str:
    lines = ["# 644 E1 · 全库证据不足扫描", "",
             f"- 卡片总数：**{s['n_cards']}**  证据不足/需人审：**{s['n_gaps']}**", "",
             "## Top 10 最需补证据的卡片", "",
             "| 卡片 | 判定 | 证据数 | 缺什么 | 优先级 |", "|---|---|---|---|---|"]
    for g in s["top10"]:
        lines.append(f"| {g['card']} | {g['verdict']} | {g['n_evidence']} | "
                     f"{'; '.join(g['missing']) or '—'} | {g['priority']} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_report() -> str:
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_md(scan()))
    return OUT_MD


def selftest() -> int:
    s = scan()
    assert s["n_cards"] == len(base.list_atoms())
    # 已知：零证据卡必判不足且缺 L1/L2
    zero = [g for g in s["gaps"] if g["n_evidence"] == 0]
    if zero:
        assert all("L1/L2 权威证据" in g["missing"] for g in zero)
    # 优先级排序合理（非递增即可，top10 非空当存在 gap）
    if s["gaps"]:
        assert len(s["top10"]) <= 10 and len(s["top10"]) > 0
        pris = [g["priority"] for g in s["gaps"]]
        assert pris == sorted(pris, reverse=True)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 E1 全库证据不足扫描")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--report", action="store_true", help="写不足扫描报告")
    a = ap.parse_args(argv)
    if a.report:
        print(f"written {write_report()}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
