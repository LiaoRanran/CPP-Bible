"""631 D2 · 探针 L1.2（命题多义指代）单测（4 例）。"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import coverage_probe_l1_2_631 as P


def test_detector_basics():
    assert P.scan_text("返回它的值") == ["它"]
    assert P.scan_text("其它情况") == [], "『其它』不是指代，不能误报"
    assert P.scan_text("该值 与 它 和 该值") == ["该值", "它"], "去重且保序"


def test_scan_props_parses_frontmatter():
    sample = """---
id: ATOM-X
claim_structured:
  - id: prop-1
    subject: 该值
    predicate: 被返回
    object: 它
    statement: 无
  - id: prop-2
    subject: 明确主体
    predicate: 明确谓词
    object: 明确客体
    statement: 无
---
"""
    hits = P.scan_props(sample)
    assert [h["prop_id"] for h in hits] == ["prop-1"]
    assert "它" in hits[0]["hits"] and "该值" in hits[0]["hits"]


def test_measure_is_consistent():
    m = P.measure()
    assert m["vector"] == "L1.2" and m["cards_scanned"] > 0
    assert m["props_hit"] == sum(len(r["props"]) for r in m["rows"])
    assert m["hits_total"] == sum(len(list(pr["hits"]))
                                  for r in m["rows"] for pr in r["props"])


def test_readonly_and_report():
    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain"], cwd=P.ROOT,
                           capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    P.measure()
    assert snap() == before, "探针只读，不写卡"
    md = P.write_report()
    text = open(md, encoding="utf-8").read()
    for kw in ("命题多义指代", "诚实登记"):
        assert kw in text
    assert json.load(open(P.OUT_JSON, encoding="utf-8"))["vector"] == "L1.2"
    assert P.selftest() == 0
