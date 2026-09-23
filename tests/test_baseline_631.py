"""631 任务0 · 基线台账 单测（6 例）。"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import baseline_631 as B


def test_standing_is_complete():
    assert len(B.STANDING) >= 15
    for k in ("gate_rules", "gate_hits", "escape", "autoimmune", "coverage",
              "poison", "replay", "w2", "pck", "authority_v2_ledger",
              "head", "remote", "ci_pytest"):
        assert k in B.STANDING, f"§一 缺 {k}"
    assert B.STANDING["gate_rules"] == 67 and B.STANDING["gate_hits"] == 191
    assert B.STANDING["head"] == "1438cd5e"


def test_git_facts_and_counts():
    g, c = B.measure()["git"], B.file_counts()
    assert len(g["head"]) >= 7 and len(g["remote"]) >= 7
    assert isinstance(g["ahead"], int) and g["ahead"] >= 0
    assert isinstance(g["behind"], int) and g["behind"] >= 0
    assert len(g["log3"]) == 3
    assert c["tools_py"] >= 300 and c["tests_py"] >= 300


def test_metrics_match_standing_baseline():
    mt = B.metrics()
    assert mt["clean_cards"] == 23, "干净卡 23 张（自身免疫率分母）"
    assert mt["autoimmune_rate_pct"] == 100.0, "自身免疫率 100%"
    assert mt["caliber_cards"] == 22, "其中 22 张口径级"
    assert mt["coverage"] == "16/35 (45.7%)", "coverage 16/35"


def test_ci_failures_parser():
    """解析器只认 `FAILED <nodeid>` 行；无原始文件时为空（不报错）。"""
    if not os.path.exists(B.RAW):
        assert B.ci_failures() == []
        return
    ids = B.ci_failures()
    assert ids and all(n.startswith("tests/") and "::" in n for n in ids)
    assert len(ids) == len(set(ids)), "必须去重"


def test_measure_has_no_side_effects():
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
    assert saved["measure"]["git"]["head"] == B.measure()["git"]["head"]
    assert B.selftest() == 0
