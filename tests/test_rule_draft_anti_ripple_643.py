"""643 D4 · rule_draft_anti_ripple_643 单测（等级/阈值/代理标记/边界登记）。
编号 D4-1..D4-7。
"""
from __future__ import annotations

import rule_draft_anti_ripple_643 as D4


# D4-1：四级判据
def test_grading():
    assert D4.grade(0) == "安全"
    assert D4.grade(1) == "有涟漪"
    assert D4.grade(3) == "有涟漪"
    assert D4.grade(4) == "危险"
    assert D4.grade(None) == "数据不足"


# D4-2：阈值边界（0 / 3 / 4）
def test_threshold_edges():
    assert (D4.RIPPLE_SAFE, D4.RIPPLE_MILD) == (0, 3)
    assert D4.grade(D4.RIPPLE_MILD) == "有涟漪"
    assert D4.grade(D4.RIPPLE_MILD + 1) == "危险"


# D4-3：无证据一律"数据不足"（不猜）
def test_no_evidence_never_guesses():
    assert D4.grade(None) == "数据不足"


# D4-4：**草案注入未实现**（硬边界必须如实暴露）
def test_injection_flag_is_false():
    a = D4.assess()
    assert a["injection_implemented"] is False


# D4-5：逐条覆盖 + 等级分布自洽
def test_rows_and_distribution():
    a = D4.assess()
    assert a["n"] == len(a["rows"]) > 0
    assert sum(a["by_grade"].values()) == a["n"]


# D4-6：危险项与"可上线"清单不相交
def test_no_contradiction():
    a = D4.assess()
    assert not (set(a["dangerous"]) & set(a["safe_to_上线"]))


# D4-7：代理结论必带 proxy 标记 + 只读自检
def test_proxy_flagged():
    a = D4.assess()
    for r in a["rows"]:
        if r["ripple_grade"] != "跳过":
            assert r["proxy"] is True
    assert D4.selftest() == 0
