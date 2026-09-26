"""644 阶段 E · E3 头部层-尾端验证器联动。

功能（只读联动，§九.7）：头部层获取的新证据，喂给尾端验证器；
尾端验证：新证据是否支持卡片结论？有没有冲突？
输出：联动报告（新证据对尾端验证的影响）。

**只读联动**——不修改任何生产数据。`--check` 只读幂等；`--report` 写联动报告。
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base

OUT_MD = os.path.join(base.ROOT, "data", "644_head_tail_bridge_report.md")


def tail_verify(evidence: base.EvidenceRecord, card_id: str) -> dict[str, Any]:
    """只读：判断一条头部层新证据对卡片尾端结论的影响。

    简化尾端校验（不调用生产 gate_engine，避免副作用；纯只读启发式）：
    - grade 为 L1/L2 且 verdict=confirm → supports
    - verdict=refute → conflicts（需人审）
    - 其余 → neutral（信息不足，留人审）
    """
    verdict = (evidence.meta.get("verdict") or "confirm")
    if evidence.grade in ("L1", "L2") and verdict == "confirm":
        impact = "supports"
    elif verdict == "refute":
        impact = "conflicts"
    else:
        impact = "neutral"
    return {"evidence_id": evidence.evidence_id, "card_id": card_id,
            "grade": evidence.grade, "impact": impact}


def bridge(card_id: str, evidences: list[base.EvidenceRecord]) -> dict[str, Any]:
    results = [tail_verify(e, card_id) for e in evidences]
    supports = sum(1 for r in results if r["impact"] == "supports")
    conflicts = sum(1 for r in results if r["impact"] == "conflicts")
    neutral = sum(1 for r in results if r["impact"] == "neutral")
    return {"card_id": card_id, "n_evidence": len(evidences),
            "supports": supports, "conflicts": conflicts, "neutral": neutral,
            "results": results, "read_only": True}


def render_md(bridges: list[dict[str, Any]]) -> str:
    lines = ["# 644 E3 · 头部层-尾端联动报告", "",
             f"- 联动卡片数：**{len(bridges)}**",
             "> 只读联动：未修改任何生产数据（read_only=True）。", "",
             "| 卡片 | 新证据 | 支持 | 冲突 | 中性 |", "|---|---|---|---|---|"]
    for b in bridges:
        lines.append(f"| {b['card_id']} | {b['n_evidence']} | {b['supports']} | "
                     f"{b['conflicts']} | {b['neutral']} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_from_stored() -> list[dict[str, Any]]:
    """对 store 中所有（头部层获取的）证据，逐条做只读尾端联动（演示）。"""
    recs = base.iter_stored()
    # 这些证据尚未关联卡片（人审后才关联），演示用：以 origin 字段回指（若有）
    out = []
    for rec in recs:
        origin = rec.meta.get("origin")
        cid = origin.split("/")[-1].replace(".md", "") if origin else "UNLINKED"
        out.append(bridge(cid, [rec]))
    return out


def write_report() -> str:
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_md(build_from_stored()))
    return OUT_MD


def selftest() -> int:
    # 构造一条 L1 confirm 证据 → supports
    rec = base.EvidenceRecord(evidence_id="a" * 64, content="x", source_type="compiler_run",
                            grade="L1", credibility=0.95, acquired_at="2026-09-26",
                            acquisition_method="test", meta={"verdict": "confirm"})
    r = bridge("C1", [rec])
    assert r["supports"] == 1 and r["conflicts"] == 0
    assert r["read_only"] is True
    # refute → conflicts
    rec2 = base.EvidenceRecord(evidence_id="b" * 64, content="y", source_type="single_blog",
                             grade="L4", credibility=0.5, acquired_at="2026-09-26",
                             acquisition_method="test", meta={"verdict": "refute"})
    r2 = bridge("C2", [rec2])
    assert r2["conflicts"] == 1
    # 只读：不修改任何生产数据（未触碰 atoms/evidence）
    atom = base.list_atoms()[0]
    with open(atom["path"], encoding="utf-8") as fh:
        before = fh.read()
    bridge("C1", [rec])
    with open(atom["path"], encoding="utf-8") as fh:
        after = fh.read()
    assert before == after
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 E3 头部层-尾端联动")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--report", action="store_true", help="写联动报告（基于 store）")
    a = ap.parse_args(argv)
    if a.report:
        print(f"written {write_report()}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
