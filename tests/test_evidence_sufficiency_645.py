"""645 B6 证据充分性单测（fast 组：真实 28 卡判定）。"""
import sys

sys.path.insert(0, "tools")

import evidence_grading_645 as b6  # 647 D1：B6 已并入证据判定套件


def test_selftest_passes():
    assert b6.sufficiency_selftest() == 0


def test_judge_covers_real_cards():
    res = b6.judge()
    # 真实卡片（EV→card 映射）至少覆盖一部分原子卡
    assert res["cards_total"] > 0
    for info in res["per_card"].values():
        assert info["status"] in ("sufficient", "insufficient")
        # 不足时必须列出缺失项（真实、不隐藏）
        if info["status"] == "insufficient":
            assert info["missing"]
