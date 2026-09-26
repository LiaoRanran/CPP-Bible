"""644 阶段 B · B3 证据冲突检测器。

检测同一张卡的多条证据之间是否冲突（设计输入 3）：
- 两条 L2 证据说法矛盾（verdict confirm vs refute）？
- L1 实测和 L2 标准不一致？
- 不同编译器版本结果不同？

输出：冲突清单 + 严重度（high/medium/low）+ 建议（人审 / 进一步实测 / 标记争议）。
只读：不修改受控目录。`--check` 只读幂等；`--report` 写冲突报告。
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base

OUT_MD = os.path.join(base.ROOT, "data", "644_conflict_report.md")


def detect_conflicts(card_id: str, ev_list: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """纯函数：检测一组证据内部的冲突。"""
    conflicts: list[dict[str, Any]] = []
    by_id = {e["id"]: e for e in ev_list}
    verdicts = {e["id"]: str(e.get("verdict", "")).lower() for e in ev_list}

    # 1. L1 实测 vs L2 标准不一致（verdict 相左）
    l1 = [e for e in ev_list if e["grade"] == "L1"]
    l2 = [e for e in ev_list if e["grade"] == "L2"]
    for a in l1:
        for b in l2:
            if _contradictory(verdicts.get(a["id"]), verdicts.get(b["id"])):
                conflicts.append(_mk(card_id, "L1_vs_L2", [a["id"], b["id"]],
                                    "实测(L1)与权威(L2)结论相左", "high",
                                    "进一步实测并人审"))

    # 2. 两条 L2 互相矛盾
    for i in range(len(l2)):
        for j in range(i + 1, len(l2)):
            if _contradictory(verdicts.get(l2[i]["id"]), verdicts.get(l2[j]["id"])):
                conflicts.append(_mk(card_id, "L2_vs_L2", [l2[i]["id"], l2[j]["id"]],
                                    "两条权威(L2)证据矛盾", "medium", "人审裁决"))

    # 3. 不同编译器版本结果不同（同 kind 且都有实际输出但 verdict 相左）
    runs = [e for e in ev_list if e.get("source_type") == "compiler_run"]
    for i in range(len(runs)):
        for j in range(i + 1, len(runs)):
            ci, cj = runs[i].get("compilers", 1), runs[j].get("compilers", 1)
            if ci != cj or _contradictory(verdicts.get(runs[i]["id"]), verdicts.get(runs[j]["id"])):
                if _contradictory(verdicts.get(runs[i]["id"]), verdicts.get(runs[j]["id"])):
                    conflicts.append(_mk(card_id, "compiler_diff", [runs[i]["id"], runs[j]["id"]],
                                        "不同编译器/版本结论不同", "low", "标记争议并复测"))

    # 4. 任意 confirm vs refute（跨等级）兜底
    confirms = {i for i, e in by_id.items() if verdicts.get(i) == "confirm"}
    refutes = {i for i, e in by_id.items() if verdicts.get(i) == "refute"}
    for a in confirms:
        for b in refutes:
            if not any(c["pair"] == sorted([a, b]) for c in conflicts):
                conflicts.append(_mk(card_id, "confirm_vs_refute", [a, b],
                                    "存在确认证据与反驳证据直接矛盾", "high", "人审裁决"))

    return conflicts


def _contradictory(v1: str | None, v2: str | None) -> bool:
    s = {v1 or "", v2 or ""}
    return "confirm" in s and "refute" in s


def _mk(card_id: str, ctype: str, pair: list[str], desc: str,
        severity: str, suggestion: str) -> dict[str, Any]:
    return {"card": card_id, "type": ctype, "pair": sorted(pair),
            "description": desc, "severity": severity, "suggestion": suggestion}


def detect_all() -> dict[str, list[dict[str, Any]]]:
    m = base.card_evidence_map()
    out: dict[str, list[dict[str, Any]]] = {}
    for card in base.list_atoms():
        cid = card["id"]
        cs = detect_conflicts(cid, m.get(cid, []))
        if cs:
            out[cid] = cs
    return out


def render_md(all_conflicts: dict[str, list[dict[str, Any]]]) -> str:
    total = sum(len(v) for v in all_conflicts.values())
    lines = ["# 644 B3 · 证据冲突检测报告", "",
             f"- 冲突卡片数：**{len(all_conflicts)}**  冲突条目：**{total}**", "", ""]
    if not all_conflicts:
        lines.append("（未检出冲突）")
    for cid, cs in sorted(all_conflicts.items()):
        lines.append(f"## {cid}")
        for c in cs:
            lines.append(f"- [{c['severity']}] {c['type']} {c['pair']}：{c['description']} → 建议：{c['suggestion']}")
        lines.append("")
    return "\n".join(lines) + "\n"


def write_report() -> str:
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_md(detect_all()))
    return OUT_MD


def selftest() -> int:
    # 已知冲突：L1 confirm vs L2 refute
    evs = [
        {"id": "E1", "grade": "L1", "verdict": "confirm", "source_type": "compiler_run", "compilers": 2},
        {"id": "E2", "grade": "L2", "verdict": "refute", "source_type": "iso_standard", "compilers": 1},
    ]
    cs = detect_conflicts("C-x", evs)
    assert any(c["type"] == "L1_vs_L2" and c["severity"] == "high" for c in cs)
    # 两条 L2 矛盾
    evs2 = [
        {"id": "A", "grade": "L2", "verdict": "confirm", "source_type": "iso_standard", "compilers": 1},
        {"id": "B", "grade": "L2", "verdict": "refute", "source_type": "committee", "compilers": 1},
    ]
    cs2 = detect_conflicts("C-y", evs2)
    assert any(c["type"] == "L2_vs_L2" for c in cs2)
    # 无冲突不误报
    evs3 = [
        {"id": "P", "grade": "L1", "verdict": "confirm", "source_type": "compiler_run", "compilers": 2},
        {"id": "Q", "grade": "L2", "verdict": "confirm", "source_type": "iso_standard", "compilers": 1},
    ]
    assert detect_conflicts("C-z", evs3) == []
    # 全量可跑
    assert isinstance(detect_all(), dict)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 B3 证据冲突检测器")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--report", action="store_true", help="写冲突报告")
    a = ap.parse_args(argv)
    if a.report:
        print(f"written {write_report()}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
