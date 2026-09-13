"""472 P1-3（452 E16）回归锁：闪卡默认不含 draft 原子。"""
from __future__ import annotations

import gate_engine as ge
import flashcard_export as fe


def test_draft_atom_excluded_by_default():
    """默认导出不得含 draft 原子（未验证内容不直达学习者）。"""
    drafts = {str(ge._meta(p).get("id")) for p in ge._cards(ge.ATOMS, "ATOM-*.md")
              if str(ge._meta(p).get("status")) == "draft"}
    assert drafts, "本用例前提是存在 draft 原子"
    ids = {c["id"] for c in fe.build_cards()}
    assert not (ids & drafts), f"draft 原子被导出：{ids & drafts}"


def test_include_draft_flag_includes_them():
    """阴性对照：显式 --include-draft 时应包含 draft 原子（flag 有效）。"""
    drafts = {str(ge._meta(p).get("id")) for p in ge._cards(ge.ATOMS, "ATOM-*.md")
              if str(ge._meta(p).get("status")) == "draft"}
    ids = {c["id"] for c in fe.build_cards(include_draft=True)}
    assert drafts <= ids


def test_verified_intermediate_states_kept():
    """red-team-verified 属已验证链，不得被误过滤（工单「==verified」会误伤这 3 颗）。"""
    keep = {str(ge._meta(p).get("id")) for p in ge._cards(ge.ATOMS, "ATOM-*.md")
            if str(ge._meta(p).get("status")) == "red-team-verified"}
    ids = {c["id"] for c in fe.build_cards()}
    assert keep <= ids, f"已验证中间态被误过滤：{keep - ids}"


def test_card_count_is_total_minus_drafts():
    """总数 = 全部原子 - draft 原子 + 全部误解。"""
    n_draft = sum(1 for p in ge._cards(ge.ATOMS, "ATOM-*.md")
                  if str(ge._meta(p).get("status")) == "draft")
    n_atom = len(list(ge._cards(ge.ATOMS, "ATOM-*.md")))
    n_mis = len(list(ge._cards(ge.MISCONCEPTIONS, "MIS-*.md")))
    assert len(fe.build_cards()) == (n_atom - n_draft) + n_mis
