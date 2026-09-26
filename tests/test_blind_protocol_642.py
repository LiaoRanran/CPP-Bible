"""642 A3 · blind_protocol_642 单测（盲化可逆 / 盲态不可读 / 揭盲分歧 / 历史只读）。编号 A3-1..A3-8。"""
from __future__ import annotations

import dataclasses

import blind_protocol_636 as shadow
import blind_protocol_642 as B


# A3-1：盲化可逆（揭盲精确还原 AI 值）
def test_blinding_is_reversible():
    for v in (0.0, 7.0, 35.8, -12.25, 1000.0):
        it = B.open_item(f"T-{v}", v)
        assert shadow.reveal({"masked": it.masked, "sign": it.sign,
                              "offset": it.offset}) == v


# A3-2：AI 推荐在盲态**不可读**（可见视图不含该字段，也不含原值）
def test_ai_recommendation_not_visible_while_blind():
    it = B.open_item("T-1", 35.8)
    view = it.visible_view()
    assert "ai_recommendation" not in view
    assert 35.8 not in view.values()
    assert view["blind_state"] == "BLIND"
    assert "masked" in view and "residual" in view


# A3-3：揭盲后可见 + 分歧率计算
def test_reveal_then_disagreement_rate():
    a = B.reveal_after_human(B.open_item("T-1", 35.8), 40.0)   # 分歧
    b = B.reveal_after_human(B.open_item("T-2", 12.5), 12.5)   # 一致
    assert a.visible_view()["ai_recommendation"] == 35.8
    assert B.disagreement(a)["disagree"] is True
    assert B.disagreement(b)["disagree"] is False
    assert B.disagreement_rate([a, b]) == 0.5


# A3-4：无已揭盲条 ⇒ 分歧率 None（不编造）
def test_rate_is_none_without_revealed_items():
    assert B.disagreement_rate([B.open_item("T-3", 1.0)]) is None
    assert B.disagreement_rate([]) is None
    assert B.disagreement(B.open_item("T-4", 1.0)) is None


# A3-5：只有 ITEM_BLIND 强制盲化，其余方法不盲化
def test_only_item_blind_requires_blinding():
    assert B.requires_blinding("ITEM_BLIND") is True
    for m in ("BATCH_AUTH", "MIRROR_DERIVED", "ITEM_OPEN"):
        assert B.requires_blinding(m) is False
    plain = B.open_item("T-9", 9.0, review_method="BATCH_AUTH")
    assert plain.blinded is False
    assert plain.visible_view()["ai_recommendation"] == 9.0


# A3-6：揭盲失真 ⇒ 抛错（盲化不可逆时必须炸，不静默给错值）
def test_reveal_detects_corruption():
    it = B.open_item("T-1", 35.8)
    broken = dataclasses.replace(it, masked=it.masked + 1.0)
    try:
        B.reveal_after_human(broken, 1.0)
    except RuntimeError:
        return
    raise AssertionError("揭盲失真未被检出")


# A3-7：历史 452 条**只标记不修改**（账本字节前后一致，违规数=258）
def test_history_scan_is_readonly():
    h = B.scan_history()
    assert h["n_decisions"] == 452
    assert h["n_violations"] == 258
    assert h["ledger_unchanged"] is True
    assert all(m["violation"] == (m["decision_origin"] in B.AI_VISIBLE_ORIGINS)
               for m in h["marked"])


# A3-8：--check 自检通过
def test_selftest():
    assert B.selftest() == 0
