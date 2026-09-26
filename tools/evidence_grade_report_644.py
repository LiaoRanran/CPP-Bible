"""644 阶段 B · B4 证据等级体系联调报告。

对全量卡片跑 B1（等级）/ B2（充分性）/ B3（冲突），输出证据质量报告：
- 各等级证据数量分布
- 充分 / 不足 / 需人审 的卡片数量
- 冲突清单
- Top 10 证据最薄弱的卡片

只读：不修改受控目录。`--check` 只读幂等；`--report` 写联调报告。
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base
import evidence_conflict_644 as b3
import evidence_grading_644 as b1
import evidence_sufficiency_644 as b2

OUT_MD = os.path.join(base.ROOT, "data", "644_evidence_quality_report.md")


def build() -> dict[str, Any]:
    graded = b1.grade_existing_evidence()
    dist = b1.grade_distribution(graded)
    suf = b2.judge_all()
    suf_counts = {"充分": 0, "不足": 0, "需人审": 0}
    for r in suf:
        suf_counts[r["verdict"]] += 1
    conflicts = b3.detect_all()
    n_conflicts = sum(len(v) for v in conflicts.values())
    weak = sorted(suf, key=lambda r: (r["verdict"] != "不足", -r["n_evidence"]))[:10]
    return {
        "n_evidence": len(graded),
        "grade_distribution": dist,
        "sufficiency_counts": suf_counts,
        "n_cards": len(suf),
        "conflict_cards": len(conflicts),
        "n_conflicts": n_conflicts,
        "conflicts": conflicts,
        "weakest_top10": weak,
    }


def render_md(r: dict[str, Any]) -> str:
    lines = ["# 644 B4 · 证据质量联调报告", "",
             f"- 证据总数：**{r['n_evidence']}**  卡片总数：**{r['n_cards']}**",
             "", "## 各等级证据数量分布", "", "| 等级 | 含义 | 数量 |", "|---|---|---|"]
    for g in base.GRADES:
        lines.append(f"| {g} | {base.GRADE_DESC[g]} | {r['grade_distribution'][g]} |")
    sc = r["sufficiency_counts"]
    lines += ["", "## 充分性", "",
              f"- 充分：**{sc['充分']}**  不足：**{sc['不足']}**  需人审：**{sc['需人审']}**",
              "", "## 冲突清单", "",
              f"- 冲突卡片：**{r['conflict_cards']}**  冲突条目：**{r['n_conflicts']}**"]
    if r["conflicts"]:
        for cid, cs in sorted(r["conflicts"].items()):
            for c in cs:
                lines.append(f"  - [{c['severity']}] {cid} {c['type']} {c['pair']}：{c['description']}")
    else:
        lines.append("  （未检出冲突）")
    lines += ["", "## Top 10 证据最薄弱的卡片", "",
              "| 卡片 | 判定 | 证据数 | 缺失 |", "|---|---|---|---|"]
    for w in r["weakest_top10"]:
        lines.append(f"| {w['card']} | {w['verdict']} | {w['n_evidence']} | {'; '.join(w['missing']) or '—'} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_report() -> str:
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_md(build()))
    return OUT_MD


def selftest() -> int:
    r = build()
    assert r["n_evidence"] > 0
    assert sum(r["grade_distribution"].values()) == r["n_evidence"]
    assert r["sufficiency_counts"]["充分"] + r["sufficiency_counts"]["不足"] + \
        r["sufficiency_counts"]["需人审"] == r["n_cards"]
    assert r["n_conflicts"] >= 0
    assert len(r["weakest_top10"]) <= 10
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 B4 证据质量联调报告")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--report", action="store_true", help="写联调报告")
    a = ap.parse_args(argv)
    if a.report:
        print(f"written {write_report()}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
