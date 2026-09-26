"""645 · 阶段 B5 · 证据等级真实判定（替代 644 B1 启发式）。

目标（645 §四 B5）：基于真实证据库，对每条证据真实判定等级（L1 多编译器实测 / L2 标准 /
L3 共识 / L4 单点 / L5 未验证）；≥30 条证据有真实等级判定。

真实、非代理：复用 644 `evidence_base_644` 的 `EvidenceRecord` 与 `grade_from_source`；
对**真实已存证据**（evidence/ 下 EV 卡 + data/evidence_store 本批新存证据）逐条判定等级与可信度。
`--check`：只读自检。`--grade`：真实分级，写 `data/645_evidence_grading_report.md`+`.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(ROOT, "data", "645_evidence_grading_report.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_evidence_grading_report.json")
GRADES = base.GRADES


def grade_all() -> dict:
    """真实分级：现有 EV 卡 + 本批新存证据库。"""
    graded: list[dict] = []
    # 1) 现有 evidence/ 下 EV 卡（真实编译器/标准/来源 → 等级）
    for e in base.grade_existing_evidence():
        graded.append({
            "id": e["id"], "source": "evidence_card", "kind": e["kind"],
            "grade": e["grade"], "credibility": e["credibility"],
            "compilers": e["compilers"], "verdict": e["verdict"],
        })
    # 2) 本批新存 evidence_store（compiler_probe_645 / standard_fetcher_645 落库）
    for rec in base.iter_stored():
        graded.append({
            "id": rec.evidence_id[:16], "source": "evidence_store",
            "kind": rec.source_type, "grade": rec.grade, "credibility": rec.credibility,
            "compilers": rec.meta.get("compilers", 1), "verdict": "",
        })
    # 等级分布
    dist: dict[str, int] = {g: 0 for g in GRADES}
    for g in graded:
        if g["grade"] in dist:
            dist[g["grade"]] += 1
    return {
        "total": len(graded),
        "grade_distribution": dist,
        "graded": graded,
    }


def write_report(result: dict) -> None:
    """把结果写为 `data/645_*.md` + `.json` 报告（人类可读 + 机器可读）。"""
    lines = ["# 645 证据等级报告（B5，真实判定）", "",
             f"- **已判等级证据总数：{result['total']}**（B5 目标 ≥30）",
             f"- 等级分布：{result['grade_distribution']}", ""]
    lines.append("## 等级分布说明")
    for g in GRADES:
        lines.append(f"- {g}：{result['grade_distribution'][g]}")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：分级逻辑（复用 base，不写盘）。"""
    g, c = base.grade_from_source("compiler_run", compilers=2)
    assert g == "L1" and c > 0.9
    g2, _ = base.grade_from_source("iso_standard")
    assert g2 == "L2"
    # 真实证据可读
    assert isinstance(base.grade_existing_evidence(), list)
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 证据等级真实判定")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--grade", action="store_true", help="真实分级全量证据")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = grade_all()
    write_report(result)
    print(f"[645 grading] 已判等级证据={result['total']} 分布={result['grade_distribution']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
