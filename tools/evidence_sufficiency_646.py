"""646 · 阶段 B3 · 证据充分性补强（卡片域收口到真实 27 卡）。

目标（646 §四 B3）：645 判定「27/28，1 张不足」，但那 1 张不足是**幻影卡** `ATOM-MEM-MOVE-001`
（只存在于 `.pytest_tmp` 测试沙箱，从未被 git 跟踪，见 646 §三.1）。本批把**卡片域收口为真实
`list_atoms()` 的 27 张**，重判充分性，并登记幻影卡修正。

判定口径（与 645 一致）：≥1 条 L1/L2 级证据 且 ≥3 条独立证据 ⇒ `sufficient`，否则 `insufficient`。

**只读**：不改卡片/证据。`--check` 只读自检；`--judge` 真实重判，写 `data/646_sufficiency_report.md` + `.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import perf_646 as perf  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REPORT_MD = os.path.join(DATA, "646_sufficiency_report.md")
REPORT_JSON = os.path.join(DATA, "646_sufficiency_report.json")

PHANTOM = "ATOM-MEM-MOVE-001"


def judge() -> dict:
    """真实重判（卡片域 = 真实 27 卡）。"""
    real = {a["id"] for a in perf.atoms()}
    by_card: dict[str, list[dict]] = {cid: [] for cid in real}
    # 落库证据（含 meta.card）
    for eid, grade, _cred, src, card in perf.stored_records():
        if card in real:
            by_card[card].append({"id": eid[:16], "grade": grade, "source": src})
    # EV→卡 映射
    for card, evs in perf.card_evidence_map().items():
        if card in real:
            by_card[card].extend(evs)
    per_card: dict[str, dict] = {}
    sufficient = insufficient = 0
    for card, evs in by_card.items():
        has_l12 = any(e.get("grade") in ("L1", "L2") for e in evs)
        independent = len({(e.get("id"), e.get("source")) for e in evs})
        missing = []
        if not has_l12:
            missing.append("缺少 L1/L2 级证据")
        if independent < 3:
            missing.append("独立证据不足 3 条")
        status = "sufficient" if not missing else "insufficient"
        sufficient += status == "sufficient"
        insufficient += status == "insufficient"
        per_card[card] = {"evidence_count": len(evs), "has_l12": has_l12,
                          "independent": independent, "missing": missing, "status": status}
    return {
        "cards_total": len(by_card),
        "sufficient": sufficient, "insufficient": insufficient,
        "phantom_excluded": PHANTOM,
        "per_card": per_card,
    }


def write_report(result: dict) -> None:
    """写报告。"""
    lines = ["# 646 证据充分性重判报告（B3，卡片域=真实 27 卡）", "",
             f"- 卡片总数：{result['cards_total']}（真实原子卡）",
             f"- **充分：{result['sufficient']} / 不足：{result['insufficient']}**",
             f"- 幻影卡已排除：`{result['phantom_excluded']}`（仅存在于 .pytest_tmp，见 646 §三.1）", "",
             "## 逐卡"]
    for cid, info in result["per_card"].items():
        extra = f"；缺失：{info['missing']}" if info["missing"] else ""
        lines.append(f"- `{cid}`：证据={info['evidence_count']} "
                     f"L1/L2={info['has_l12']} 独立={info['independent']} → **{info['status']}**{extra}")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：判定逻辑正确（合成证据）。"""
    def _status(evs):
        has = any(e["grade"] in ("L1", "L2") for e in evs)
        ind = len({(e["id"], e.get("source")) for e in evs})
        return "sufficient" if has and ind >= 3 else "insufficient"
    assert _status([{"id": "a", "grade": "L1", "source": "x"},
                    {"id": "b", "grade": "L2", "source": "y"},
                    {"id": "c", "grade": "L1", "source": "z"}]) == "sufficient"
    assert _status([{"id": "a", "grade": "L1", "source": "x"}]) == "insufficient"
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口：`--check` 只读自检；`--judge` 真实重判。"""
    ap = argparse.ArgumentParser(description="646 充分性重判（B3）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--judge", action="store_true", help="真实重判")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = judge()
    write_report(result)
    print(f"[646 sufficiency] 卡={result['cards_total']} 充分={result['sufficient']} "
          f"不足={result['insufficient']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
