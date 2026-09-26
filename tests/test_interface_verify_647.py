"""647 D2 · 合并后接口统一验证回归锁（编号 D2-1..D2-6）。"""
from __future__ import annotations

import json
import os

import interface_verify_647 as V


def test_d2_1_merge_plan_is_15_to_10():
    assert sum(len(g["members"]) - 1 for g in V.MERGE_PLAN) == 5
    assert len(V.CORE_10) == 10


def test_d2_2_all_core_tools_exist():
    present = [n for n in V.CORE_10 if os.path.isfile(os.path.join(V.HERE, n + ".py"))]
    assert present == list(V.CORE_10)


def test_d2_3_members_removed():
    for g in V.MERGE_PLAN:
        for m in g["members"]:
            if m != g["target"]:
                assert not os.path.isfile(os.path.join(V.HERE, m + ".py")), m


def test_d2_4_merge_is_lossless():
    loss = V.merge_loss_check()
    assert all(x["ok"] for x in loss), [x["target"] for x in loss if not x["ok"]]


def test_d2_5_every_tool_satisfies_interface():
    res = V.audit()
    bad = [t["tool"] for t in res["tools"] if not t["ok"]]
    assert bad == [], bad
    assert res["all_ok"] is True


def test_d2_6_report_and_selftest():
    assert V.selftest() == 0
    assert V.main(["--report"]) == 0
    doc = json.load(open(V.OUT_JSON, encoding="utf-8"))
    assert doc["n_tools"] == 10 and doc["all_ok"] is True
    assert os.path.isfile(V.OUT_MD)
