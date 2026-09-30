# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""646 阶段 B3 · 充分性重判单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import counts_659 as counts  # noqa: E402
import evidence_sufficiency_646 as b3  # noqa: E402


def test_selftest_passes():
    """--check 只读自检。"""
    assert b3.selftest() == 0


def test_real_cards_judged_and_phantom_excluded():
    """670a 去写死：卡片域取权威源现算；充分/不足不再冻结 27/10，改锁**划分 + 判据自洽**。"""
    res = b3.judge()
    assert res["cards_total"] == counts.ATOMS_REAL
    assert res["sufficient"] + res["insufficient"] == res["cards_total"]
    assert res["sufficient"] > 0 and res["insufficient"] > 0
    # 判据自洽：status 必须等价于 missing 为空（判据改了这里就红）
    for cid, info in res["per_card"].items():
        assert (info["status"] == "sufficient") == (not info["missing"]), cid
    assert res["phantom_excluded"] == "ATOM-MEM-MOVE-001"
    assert "ATOM-MEM-MOVE-001" not in res["per_card"]
