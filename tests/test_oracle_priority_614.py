#!/usr/bin/env python3
"""614 E1 回归测试：oracle_priority_614（离线优先级排序）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import oracle_priority_614 as e1  # noqa: E402


def test_card_count_83() -> None:
    rows = e1.score_cards()
    assert len(rows) == 83


def test_sorted_desc() -> None:
    rows = e1.score_cards()
    scores = [r["score"] for r in rows]
    assert scores == sorted(scores, reverse=True)


def test_known_tce_bonus() -> None:
    rows = e1.score_cards()
    tce = [r for r in rows if r["known_tce"]]
    assert tce, "应至少有 1 张 known_tce 卡"
    for r in tce:
        assert r["score"] == r["base_score"] + 5 + (1 if r["kc_related"] else 0)


def test_fields_complete() -> None:
    rows = e1.score_cards()
    need = {"id", "path", "type", "props", "escaped", "coverage_gap",
            "related_mis", "base_score", "kc_related", "known_tce", "score"}
    for r in rows:
        assert need <= set(r)
