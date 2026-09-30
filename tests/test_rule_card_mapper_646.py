# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""646 阶段 A1 · 规则→卡映射单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import counts_659 as counts  # noqa: E402
import rule_card_mapper_646 as a1  # noqa: E402


def test_selftest_passes():
    """--check 只读自检（已知关联必命中）。"""
    assert a1.selftest() == 0


def test_rule_tokens_drop_generic():
    """通用词/数字被剔除。"""
    t = a1._rule_tokens("ATOM-CLAIM-CONCEPT-NORMALIZED")
    assert "atom" not in t and "claim" in t and "normalized" in t


def test_gray_zone_maps_only_ub_cards():
    """670a 去写死：原冻结 2 张（669 新增 4 张 UB 卡后过期）。

    改锁**口径**：GRAY 规则只映射 UB 域卡、且全为 high；关键词命中的
    `ATOM-UB-GRAY-001` 必须在列且 basis 显式带关键词痕迹。
    """
    m = a1.build_mapping()
    gray = m["rules"]["ATOM-GRAY-ZONE"]["cards"]
    assert gray, gray
    assert all(c["card"].startswith("ATOM-UB-") for c in gray), gray
    assert all(c["strength"] == "high" for c in gray), gray
    names = [c["card"] for c in gray]
    assert "ATOM-UB-GRAY-001" in names, names
    hit = next(c for c in gray if c["card"] == "ATOM-UB-GRAY-001")
    assert "关键词命中" in hit["basis"], hit


def test_every_rule_has_mapping():
    """无孤儿规则：67 规则全部有映射。"""
    m = a1.build_mapping()
    assert m["rules_with_mapping"] == m["rule_count"] == 67
    assert all(info["cards"] for info in m["rules"].values())


def test_card_count_matches_fact_source():
    """670a 去写死：卡片域不再冻结 37/27，与 `counts_659.ATOMS_REAL` 跨源对账。"""
    m = a1.build_mapping()
    assert m["card_count"] == counts.ATOMS_REAL
