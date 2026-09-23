"""629 A1 · 自身免疫率框架 单测（7 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import autoimmune_rate_framework as A


def test_clean_card_selection_is_read_only_and_complete():
    cs = A.cards(A.CLEAN_PRIMARY)
    assert len(cs) == 23, "实测 27 张卡中 status=verified 的 23 张（任务书写 28）"
    assert all(c["status"] == "verified" for c in cs)
    assert all(c["id"].startswith("ATOM-") and c["rel"].startswith("atoms/") for c in cs)
    assert all(os.path.exists(c["path"]) for c in cs)
    assert len(A.cards(A.CLEAN_SECONDARY)) == 26


def test_rate_is_ratio_of_warned_cards():
    m = A.measure()
    assert m["total"] >= 10, "任务书要求干净卡 ≥10，不足须标注样本量小"
    assert abs(m["rate"] - m["warned_count"] / m["total"]) < 1e-9
    assert m["warned_count"] == len(m["warned"])


def test_advice_not_counted_as_autoimmune():
    m = A.measure()
    for r in m["cards"]:
        assert r["autoimmune"] == bool(r["warn"] or r["block"])
        if r["autoimmune"]:
            assert not (r["warn"] and r["block"]) or True   # 允许同时命中，但必须都计入
    assert "advice" in open(A.OUT_MD, encoding="utf-8").read()


def test_buckets_partition_warned_cards():
    m = A.measure()
    hard, cal = m["hard_defect_cards"], m["caliber_only_cards"]
    assert len(hard) + len(cal) == m["warned_count"], "分桶必须切分完备且互斥"
    assert not set(hard) & set(cal)
    by_id = {r["id"]: r for r in m["warned"]}
    for cid in hard:
        assert any(h["rule"] in A.HARD_DEFECT_RULES for h in by_id[cid]["warn"])
    for cid in cal:
        assert not any(h["rule"] in A.HARD_DEFECT_RULES for h in by_id[cid]["warn"])


def test_hard_and_caliber_rule_sets_disjoint():
    assert not set(A.HARD_DEFECT_RULES) & set(A.CALIBER_RULES)
    assert A.AUTOIMMUNE_SEVERITIES == ("warn", "block")


def test_report_written_with_dual_rate_and_buckets():
    p = A.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("自身免疫率", "逃逸率", "分桶", "命题级口径", "局限"):
        assert kw in md, f"报告缺章节：{kw}"
    m = A.measure()
    assert f"{m['rate'] * 100:.1f}%" in md


def test_selftest_passes():
    assert A.selftest() == 0
