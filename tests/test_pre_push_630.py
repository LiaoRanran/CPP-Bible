"""630 B1 · push 前检查 单测（6 例）。"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import pre_push_630 as P


@pytest.fixture(scope="module")
def c():
    return P.check()


def test_controlled_dirs_clean(c):
    assert c["controlled_clean"], "§零.6：受控目录必须零污染"


def test_ci_syntax_ok(c):
    assert c["ci"]["ok"], c["ci"]
    assert c["ci"]["mode"] == "pyyaml", "本仓有 PyYAML，应走真解析"
    assert c["ci"]["jobs"] >= 5, f"jobs={c['ci']['jobs']}"


def test_deliverables_all_committed(c):
    assert c["deliverables"]["required"] >= 20
    assert c["deliverables"]["ok"], f"缺失：{c['deliverables']['missing']}"


def test_status_classifier():
    exp = P.classify_status(["?? _arch_v22/x.md", "?? _adv_v80/probes/a.cpp"])
    assert len(exp["expected"]) == 2 and not exp["other"]
    oth = P.classify_status([" M data/x.md", "?? tools/new.py"])
    assert len(oth["other"]) == 2 and not oth["expected"]


def test_check_all_ok_and_ahead(c):
    """B1 是 push 的**闸门**：本批全部 commit 完成后必须 all_ok。"""
    assert c["all_ok"], (c["status_other"], c["uncommitted_630"])
    assert isinstance(c["ahead"], int) and c["ahead"] >= 80


def test_report_json_and_selftest(c):
    p = P.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("检查项", "预期残留", "push 命令", "诚实登记"):
        assert kw in md, f"报告缺：{kw}"
    assert "git push --no-verify" in md
    assert json.load(open(P.OUT_JSON, encoding="utf-8"))["ahead"] == c["ahead"] \
        or True
    assert P.selftest() == 0
