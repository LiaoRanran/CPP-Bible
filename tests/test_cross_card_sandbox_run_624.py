"""624 A2 跨卡沙箱实跑结果 · 单元测试（验证已落盘的真实 gate 判决，不重复跑 gate）。"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN = os.path.join(ROOT, "data", "cross_card_sandbox_run_624.json")

# 623 累计触达的 26 条（见 data/rule_touch_heatmap_623.md）
TOUCHED_623 = {
    "ATOM-FM-REQUIRED", "ATOM-ID-FORMAT", "ATOM-ID-UNIQUE", "ATOM-NO-UNVERIFIED",
    "ATOM-STATUS-VALUE", "ATOM-DAL-MATCH", "ATOM-REL-DAG", "ATOM-GRAY-ZONE",
    "ATOM-AUDIENCE", "ATOM-PREREQ-READABLE", "EV-FM-REQUIRED", "EV-ID-UNIQUE",
    "EV-MATRIX", "EV-ARTIFACT-VERSION-MATCH", "EV-ASSERT-COUNT-BELOW-BASELINE",
    "EV-ASSERT-SYMBOL-MAPPED", "EV-ARTIFACT-PRODUCER", "EV-MSCV-NO-VERIFY",
    "EV-FM-DUP-KEY", "EV-FM-YAML-HARDENING", "ATOM-CLAIM-STRUCTURED",
    "ATOM-REL-TARGET", "EV-SERVES-EXIST", "ATOM-VERIFY-REASON",
    "ATOM-REL-UNKNOWN", "CARD-PATH-NOT-CANONICAL",
}


def _load():
    with open(RUN, encoding="utf-8") as fh:
        return json.load(fh)


def test_totals_60():
    d = _load()
    assert d["total"] == 60
    assert len(d["rows"]) == 60
    assert sum(d["distribution"].values()) == 60


def test_no_escaped():
    d = _load()
    assert d["escaped"] == []
    dist = d["distribution"]
    assert dist.get("blocked", 0) + dist.get("detected_nonblock", 0) == 60


def test_new_rules_and_cumulative():
    d = _load()
    touched = set(d["touched_all"])
    new = touched - TOUCHED_623
    assert new == {"ATOM-REL-CONFLICT", "EV-ARTIFACT-FILE-EXISTS"}
    assert len(touched | TOUCHED_623) == 28  # 累计 28/63


def test_prediction_hit_rate():
    d = _load()
    actual = set(d["touched_all"])
    pred = set(d["predicted_rules"])
    hit = pred & actual
    assert len(hit) >= 6  # 6/7
    assert "ATOM-MISCONCEPTION-REF" in (pred - actual)  # 唯一未命中


def test_report_exists():
    p = os.path.join(ROOT, "data", "cross_card_sandbox_run_624.md")
    assert os.path.exists(p)
    assert os.path.getsize(p) > 500
