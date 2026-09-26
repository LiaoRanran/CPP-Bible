"""647 A5 · 信任根独立审计回归锁（编号 A5-1..A5-8）。

锁定：审计项完整（A1–A4 四项 + 共置点 + 独立性刻度）；**风险如实登记**（不夸大独立性）；
A1 的沙箱实测**不碰真实仓库**。
"""
from __future__ import annotations

import hashlib
import json
import os

import trust_root_audit_647 as T


# ── A5-1：A1 实测 —— 删已钉文件后 strict=1 / lenient=0，且**真实仓库文件未被删** ──
def test_a5_1_a1_sandbox_proof():
    a = T.sandbox_missing_trust_root()
    assert a["before_delete"] == {"strict": 0, "lenient": 0}
    assert a["after_delete"]["strict"] == 1
    assert a["after_delete"]["lenient"] == 0, "601 宽容口径必须仍可用（兼容性）"
    assert a["after_delete"]["named"] is True, "缺失文件必须被点名"
    assert a["real_repo_file_still_there"] is True
    assert a["fail_open_fixed"] is True


# ── A5-2：A2 实测 —— 三类不完整事件全被拒，但历史宽容通道仍在 ───────────────────
def test_a5_2_a2_event_strictness():
    a = T.audit_event_strictness()
    assert a["all_rejected"] is True
    assert a["rejected"] == {"空 dict": True, "缺 decision_origin": True, "未知字段": True}
    assert a["lenient_legacy"]["result"] == "APPROVE"
    assert a["lenient_legacy"]["decision_origin"] == "human_observed"


# ── A5-3：A3 实测 —— 闭包 OK / 一致 / 假删必 FAIL ─────────────────────────────
def test_a5_3_a3_closure():
    a = T.audit_closure()
    assert a["status"] == "OK" and a["n_rules"] == 67
    assert a["consistent_with_tool_integrity"] is True
    assert a["attack_status"] == "FAIL" and a["attack_named"]


# ── A5-4：A4 实测 —— 接口就绪 + mock 往返 + **未连外部服务** ────────────────────
def test_a5_4_a4_external_anchor():
    a = T.audit_external_anchor()
    assert set(a["contract"]) == {"publish", "verify"}
    assert a["real_external_service_connected"] is False
    assert a["mock_roundtrip"] == {"published": True, "verified": True, "tamper_detected": True}
    assert len(a["reserved"]) == 3


# ── A5-5：共置点如实登记（≥5 条，每条有位置与风险）─────────────────────────────
def test_a5_5_co_located_points_registered():
    pts = T.co_located_points()
    assert len(pts) >= 5
    for p in pts:
        assert p["point"] and p["where"] and p["risk"] and p["resolved_by"]
    names = " ".join(p["point"] for p in pts)
    for must in ("透明日志", "完整性基线", "VSA 公钥", "外部锚"):
        assert must in names, must


# ── A5-6：独立性**不夸大**（L2 已达、L3 未达，且给出到 L3 的路径）───────────────
def test_a5_6_independence_not_overclaimed():
    ind = T.independence_level()
    assert ind["level"] == "L2"
    assert ind["l2"] is True and ind["l3"] is False and ind["l4"] is False
    assert ind["to_l3"]


# ── A5-7：审计是只读的（跑一遍不改变任何信任根文件）──────────────────────────
def test_a5_7_audit_is_read_only():
    targets = ["tools/.tool_checksums", "data/transparency_log.jsonl",
               "data/supply_chain/merkle_roots.json"]
    before = [hashlib.sha256(open(os.path.join(T.ROOT, p), "rb").read()).hexdigest()
              for p in targets]
    T.audit()
    after = [hashlib.sha256(open(os.path.join(T.ROOT, p), "rb").read()).hexdigest()
             for p in targets]
    assert before == after


# ── A5-8：报告与自检 ─────────────────────────────────────────────────────────
def test_a5_8_report_and_selftest():
    assert T.selftest() == 0
    assert T.main(["--report"]) == 0
    assert os.path.isfile(T.OUT_MD) and os.path.isfile(T.OUT_JSON)
    doc = json.load(open(T.OUT_JSON, encoding="utf-8"))
    assert doc["trA1"]["fail_open_fixed"] is True
    assert doc["independence"]["level"] == "L2"
    text = open(T.OUT_MD, encoding="utf-8").read()
    assert "仍存在的信任根共置点" in text
    assert "L3" in text
