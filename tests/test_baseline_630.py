"""630 任务0 · 基线台账 单测（6 例）。"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import baseline_630 as B


def test_standing_is_complete():
    assert len(B.STANDING) >= 15
    for k in ("gate_rules", "gate_hits", "escape", "autoimmune", "poison", "replay",
              "w2", "pck", "authority_v2_ledger", "head", "remote"):
        assert k in B.STANDING, f"§一 缺 {k}"
    assert B.STANDING["gate_rules"] == 67 and B.STANDING["gate_hits"] == 191


def test_measure_counts_and_git():
    """ahead 在 push 前 >0、push 后 =0 ⇒ 只要求是合法非负整数（不写死下限）。"""
    m = B.measure()
    assert isinstance(m["ahead"], int) and m["ahead"] >= 0
    assert len(m["head"]) >= 7 and len(m["remote"]) >= 7
    assert len(m["log5"]) == 5
    assert m["counts"]["tools_py"] >= 300 and m["counts"]["tests_py"] >= 300


def test_measure_is_deterministic():
    a, b = B.measure(), B.measure()
    assert a["head"] == b["head"] and a["ahead"] == b["ahead"]
    assert a["counts"] == b["counts"]


def test_metrics_reuse_readonly_tools():
    mt = B.metrics()
    assert mt["clean_cards"] == 23 and mt["autoimmune_rate_pct"] == 100.0
    assert mt["caliber_cards"] == 22
    assert "coverage" in mt and "/35" in mt["coverage"]
    assert mt["test_failures"] >= 11


def test_measure_has_no_side_effects():
    """只读自证：`measure()` 不改变工作区（快照前后一致）。

    不比对「他批基线是否 dirty」——那是**测试套件再生报告**造成的既有状态，与本工具无关。
    """
    import subprocess

    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain"], cwd=B.ROOT,
                           capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    B.measure()
    B.metrics()
    assert snap() == before, "measure()/metrics() 不得写盘"


def test_report_json_and_selftest():
    p = B.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("standing baseline", "实测核对", "额外测量", "偏差登记", "局限"):
        assert kw in md, f"报告缺：{kw}"
    saved = json.load(open(B.OUT_JSON, encoding="utf-8"))
    assert saved["measure"]["head"] == B.measure()["head"]
    assert B.selftest() == 0
