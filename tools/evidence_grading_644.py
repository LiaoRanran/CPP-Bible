"""644 阶段 B · B1 证据等级与可信度体系。

定义 5 级证据等级（L1 实测 / L2 权威 / L3 共识 / L4 单点 / L5 未验证）与可信度评分，
参考 A1 调研（GRADE / Daubert / EBSE / 引用层级 / 标准草案）。

- 等级映射修订（00_synthesis 设计输入 1）：cppreference 等二手归 L3，AI 生成默认 L5。
- 可信度是可移动量表（GRADE 思想）：随多编译器 / 多源微调，可人审修正。

分级逻辑统一放在 `evidence_base_644`（单一真源）；本文件是 CLI / 报告封装。
只读：不修改受控目录。`--check` 只读幂等；`--report` 写各证据分级清单。
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base

OUT_MD = os.path.join(base.ROOT, "data", "644_grading_report.md")


def grade_existing_evidence() -> list[dict[str, Any]]:
    return base.grade_existing_evidence()


def grade_distribution(records: list[dict[str, Any]]) -> dict[str, int]:
    c: Counter[str] = Counter(r["grade"] for r in records)
    return {g: c.get(g, 0) for g in base.GRADES}


def render_md(records: list[dict[str, Any]]) -> str:
    lines = ["# 644 B1 · 现有证据等级分布", "", "| 证据 | kind | 编译器数 | 等级 | 可信度 |",
             "|---|---|---|---|---|"]
    for r in sorted(records, key=lambda x: (x["grade"], x["id"])):
        lines.append(f"| {r['id']} | {r['kind']} | {r['compilers']} | {r['grade']} | {r['credibility']:.2f} |")
    dist = grade_distribution(records)
    lines += ["", "## 等级分布", "", "| 等级 | 含义 | 数量 |", "|---|---|---|"]
    for g in base.GRADES:
        lines.append(f"| {g} | {base.GRADE_DESC[g]} | {dist[g]} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_report() -> str:
    recs = grade_existing_evidence()
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_md(recs))
    return OUT_MD


def selftest() -> int:
    # 已知映射（委托 base）
    assert base.grade_evidence_record("compiler_run", compilers=2)[0] == "L1"
    assert base.grade_evidence_record("compiler_run", compilers=1)[0] == "L2"
    assert base.grade_evidence_record("cppreference")[0] == "L3"
    assert base.grade_evidence_record("ai_generated")[0] == "L5"
    # 现有证据可分级且等级合法
    recs = grade_existing_evidence()
    assert len(recs) > 0
    assert all(r["grade"] in base.GRADES for r in recs)
    dist = grade_distribution(recs)
    assert sum(dist.values()) == len(recs)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 B1 证据等级体系")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--report", action="store_true", help="写分级清单")
    a = ap.parse_args(argv)
    if a.report:
        print(f"written {write_report()}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
