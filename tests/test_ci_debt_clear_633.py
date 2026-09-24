"""633 A2 · ci_debt_clear 单测（纯标准库，≥5 例）。编号 A2-1..A2-6。"""
from __future__ import annotations

import tools.ci_debt_clear_633 as m


# A2-1：630 断言过期归类
def test_classify_assertion_expired():
    assert m.classify("tests/test_autoimmune_diagnose_630.py::test_x") == "断言过期型"
    assert m.classify("tests/test_autoimmune_human_queue_631.py::test_y") == "断言过期型"


# A2-2：mypy 归类
def test_classify_mypy():
    assert m.classify("tests/test_mypy_fix_625.py::test_mypy_tools_clean") == "类型检查(mypy)"


# A2-3：完整性归类
def test_classify_integrity():
    assert m.classify("tests/test_merkle_proof_613.py::test_all_proofs_verify") == "完整性/仓库漂移"
    assert m.classify("tests/test_tool_integrity.py::test_567_check_flag_on_real_repo") == "完整性/仓库漂移"


# A2-4：未命中→默认类
def test_classify_default():
    assert m.classify("tests/test_no_such_rule_999.py::t") == m.DEFAULT_CAT


# A2-5：load + summarize 计数一致
def test_load_and_summarize():
    f = m.load_failures()
    assert set(f) >= {"run1_baseline", "run2_after_fixes"}
    ids = f.get("run2_after_fixes", [])
    s = m.summarize(ids)
    assert sum(s.values()) == len(ids)


# A2-6：skipif 模板 + --check 自检
def test_skipif_and_selftest():
    snip = m.skipif_snippet("tests/x.py::t", dep="data/foo")
    assert "pytest.mark.skipif" in snip and "data/foo" in snip
    assert m.selftest() == 0
