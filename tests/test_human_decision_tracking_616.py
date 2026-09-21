#!/usr/bin/env python3
"""616 E1 回归测试：交人项跟踪台账。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "data" / "human_decision_tracking_616.md"

STATES = {"待决策", "部分推进", "已决策", "已执行"}


def _rows() -> list[list[str]]:
    out = []
    for ln in DOC.read_text(encoding="utf-8").splitlines():
        if ln.startswith("| ") and not ln.startswith("| 描述") and not re.match(r"^\|\s*-+", ln):
            cells = [c.strip() for c in ln.strip("|").split("|")]
            if cells and cells[0].isdigit():
                out.append(cells)
    return out


def test_tracking_doc_exists_with_rows() -> None:
    assert DOC.is_file()
    rows = _rows()
    assert len(rows) >= 10                       # 615 七项 + 616 三项


def test_all_items_have_status() -> None:
    rows = _rows()
    assert rows
    for r in rows:
        assert len(r) >= 5
        assert r[4].replace("*", "") in STATES, f"状态非法：{r[4]!r}"
