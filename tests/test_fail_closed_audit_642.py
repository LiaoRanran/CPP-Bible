"""642 B3 · fail_closed_audit_642 单测（两处已知点实测 + 全量扫描 + 只审计不改）。
编号 B3-1..B3-7。
"""
from __future__ import annotations

import hashlib
import os

import fail_closed_audit_642 as F

_AUDITED = (os.path.join(F.HERE, "tool_integrity.py"),
            os.path.join(F.HERE, "decision_event_v2_626.py"))


def _digest(p: str) -> str:
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# B3-1：FO-A 实测 —— 缺文件只警告、**退出码仍为 0**（fail-open 可复现）
def test_fo_a_missing_file_does_not_fail():
    a = F.known_point_supply_chain()
    assert a["fail_open"] is True
    assert a["evidence"]["exit_code"] == 0
    assert a["evidence"]["warnings"], "缺文件必须留下警告"
    assert a["severity"] == "中"


# B3-2：FO-B 实测 —— 空 dict 被补成 APPROVE（最"信任假设"的默认）
def test_fo_b_empty_dict_becomes_approve():
    b = F.known_point_decision_event()
    assert b["fail_open"] is True
    assert b["evidence"]["result"] == "APPROVE"
    assert b["severity"] == "高"


# B3-3：FO-B 默认 origin 是 human_observed（把"无人审来源"伪造成有人审）
def test_fo_b_default_origin_is_human_observed():
    b = F.known_point_decision_event()
    assert b["evidence"]["decision_origin"] == "human_observed"
    assert b["evidence"]["review_method"] == "BATCH_AUTH"


# B3-4：FO-B 未知键被静默丢弃（拼错字段名 = 没写，不报错）
def test_fo_b_unknown_keys_silently_dropped():
    b = F.known_point_decision_event()
    assert b["evidence"]["unknown_keys_silently_dropped"] is True


# B3-5：全量扫描覆盖广度 + 四条规则齐备 + 命中可复现
def test_scan_coverage_and_reproducibility():
    sc = F.scan_all()
    assert sc["scanned_files"] > 400
    assert set(F.RULE_META) == {"FO-1", "FO-2", "FO-3", "FO-4"}
    assert sc["n_hits"] == F.scan_all()["n_hits"], "同一状态两次扫描必须一致"
    assert any(h["rule"] == "FO-4" and "tool_integrity" in h["file"] for h in sc["hits"])


# B3-6：只审计不改（被审计文件字节不变）
def test_audit_does_not_modify_audited_code():
    before = [_digest(p) for p in _AUDITED]
    F.known_points()
    F.scan_all()
    after = [_digest(p) for p in _AUDITED]
    assert before == after, "fail-closed 审计不得改动被审计代码"


# B3-7：严重度汇总含两处已知点 + --check 自检
def test_severity_summary_and_selftest():
    t = F.severity_table()
    assert t["高"] >= 1 and t["中"] >= 1
    assert F.selftest() == 0
