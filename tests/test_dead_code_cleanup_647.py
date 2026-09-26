"""647 D3 · 死代码清理回归锁（编号 D3-1..D3-5）。"""
from __future__ import annotations

import json
import os

import dead_code_cleanup_647 as D


def test_d3_1_targets_exist():
    assert len(D._paths()) == len(D.TARGETS) == 10
    for t in D.TARGETS:
        assert os.path.isfile(os.path.join(D.HERE, t + ".py")), t


def test_d3_2_no_dead_imports_left():
    r = D.ruff_dead_code()
    if not r.get("available"):
        return  # ruff 不可用 ⇒ 如实跳过（不伪造）
    assert r["n_remaining"] == 0, r["violations"]


def test_d3_3_dead_function_scan_shape():
    df = D.dead_function_candidates()
    assert "n_candidates" in df and isinstance(df["candidates"], list)
    # 只报不删：候选里出现的函数必须**仍然存在**（本工具不得删任何函数）
    for c in df["candidates"]:
        p = os.path.join(D.HERE, c["module"] + ".py")
        assert c["function"] in open(p, encoding="utf-8").read()


def test_d3_4_cleaned_baseline_recorded():
    assert D.CLEANED_IN_D1 == 15, "647 D1 用 ruff --fix 清掉的死 import 行数"


def test_d3_5_report_and_selftest():
    assert D.selftest() == 0
    assert D.main(["--report"]) == 0
    doc = json.load(open(D.OUT_JSON, encoding="utf-8"))
    assert doc["cleaned_in_d1"] == 15
    assert os.path.isfile(D.OUT_MD)
