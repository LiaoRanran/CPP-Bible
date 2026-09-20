"""612 C2 回归测试：oracle 验证优先级排序（只读）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import oracle_priority as c2  # noqa: E402


def test_all_cards_scored():
    rows = c2.score_cards()
    assert len(rows) == 83
    for r in rows:
        assert {"id", "type", "props", "escaped", "coverage_gap", "related_mis", "score"} <= set(r)


def test_top1_is_max():
    rows = c2.score_cards()
    assert rows[0]["score"] == max(r["score"] for r in rows)


def test_check_passes():
    assert c2.main(["--check"]) == 0
