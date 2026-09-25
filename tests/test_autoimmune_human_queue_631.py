"""631 B2 · human 90 条清单 单测（6 例）。"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import autoimmune_human_queue_631 as H


def test_plan_human_rows():
    # 640 A1 更新：631 时清单 90 条（object+signed_by 两类）；632 C2 人审导入 +
    # 634 C1 补签已把 signed_by 类全部消解 ⇒ 剩余 65 条全为 object（语义类）。
    rr = H.rows()
    assert len(rr) == 65
    assert all(r["card_id"] and r["prop_id"] and r["field"] for r in rr)


def test_fields_are_only_machine_forbidden_types():
    rr = H.rows()
    # 640 A1：signed_by 已由 632/634 授权填入（human: 在册实名）⇒ 剩余清单只含 object
    assert {r["field"] for r in rr} == {"object"}, \
        "signed_by 类已被 632/634 人审填充消解，剩余只有语义类 object"


def test_priority_rules():
    rr = H.rows()
    for r in rr:
        if r["field"] == "signed_by":
            assert r["priority"] == "高", "机器永不代签 ⇒ 恒为高"
        else:
            assert r["priority"] == ("中" if r["suggest"] else "高")
    assert H.counts()["高"] + H.counts()["中"] + H.counts()["低"] == 65


def test_every_row_has_reason_and_no_filled_value():
    rr = H.rows()
    assert all(r["why_not_auto"] for r in rr)
    # 「不代填」：清单里不得出现已确定的填值字段（只有 suggest 候选）
    assert all("value" not in r for r in rr)


def test_priority_of_helper():
    assert H.priority_of({"field": "signed_by"})[0] == "高"
    assert H.priority_of({"field": "object", "suggest": None})[0] == "高"
    assert H.priority_of({"field": "object", "suggest": "happens-before"})[0] == "中"
    assert H.priority_of({"field": "unknown_field"})[0] == "低"


def test_outputs_and_readonly():
    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain", "--", "atoms", "evidence"],
                           cwd=H.ROOT, capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    md, jl = H.write_outputs()
    assert snap() == before, "只出清单，绝不写卡"
    text = open(md, encoding="utf-8").read()
    for kw in ("总览", "逐条清单", "机器可读输出", "诚实登记"):
        assert kw in text, f"清单缺：{kw}"
    lines = [json.loads(x) for x in open(jl, encoding="utf-8") if x.strip()]
    assert len(lines) == 65 and all("priority" in x for x in lines)  # 640 A1：90→65
    assert H.selftest() == 0
