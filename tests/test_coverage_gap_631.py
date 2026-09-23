"""631 D1 · coverage 缺口清单 单测（6 例）。"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import coverage_gap_631 as G


def test_never_run_is_19_with_6_no_probe():
    rr = G.rows()
    cov = G.coverage()
    assert len(rr) == 19 == cov["never_run_count"]
    assert cov["no_probe_count"] == 6
    assert set(cov["no_probe"]) <= {r["id"] for r in rr}


def test_rows_have_all_fields():
    for r in G.rows():
        for k in ("id", "layer", "name", "risk", "has_probe", "priority",
                  "difficulty", "difficulty_why"):
            assert r[k] not in (None, ""), f"{r['id']} 缺 {k}"


def test_priority_rule():
    """P0 = high risk 且无探针；其余按规则落 P1/P2。"""
    rr = G.rows()
    assert any(r["priority"] == "P0" for r in rr)
    for r in rr:
        if r["priority"] == "P0":
            assert r["risk"] == "high" and not r["has_probe"], r["id"]
    assert G.priority_of("high", True) == "P0"
    assert G.priority_of("high", False) == "P1"
    assert G.priority_of("medium", True) == "P1"
    assert G.priority_of("low", False) == "P2"


def test_difficulty_overrides_are_documented():
    for vid, (lvl, why) in G.DIFFICULTY_OVERRIDE.items():
        assert lvl in ("低", "中", "高") and why
    assert G.difficulty_of({"id": "L2.3", "layer": "L2"}, True)[0] == "中"
    assert G.difficulty_of({"id": "L9.9", "layer": "L9"}, False)[0] == "低"


def test_counts_sum():
    assert sum(G.counts().values()) == 19


def test_readonly_and_report():
    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain"], cwd=G.ROOT,
                           capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    G.rows()
    md = G.write_report()
    assert snap() == before, "只读：不跑探针、不改工作区"
    text = open(md, encoding="utf-8").read()
    for kw in ("19 个未跑向量逐条清单", "优先级与难度规则", "诚实登记"):
        assert kw in text, f"报告缺：{kw}"
    saved = json.load(open(G.OUT_JSON, encoding="utf-8"))
    assert saved["counts"] == G.counts()
    assert G.selftest() == 0
