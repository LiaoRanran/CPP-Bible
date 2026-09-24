"""633 E1 · test_debt_taxonomy 单测（纯标准库，≥5 例）。编号 E1-1..E1-6。"""
from __future__ import annotations

import tools.test_debt_taxonomy_633 as m


# E1-1：slow / skipif / 批次号 三个正则
def test_matchers():
    assert m.SLOW_RE.search("@pytest.mark.slow\ndef t():")
    assert m.SKIPIF_RE.search('@pytest.mark.skipif(not os.path.exists("x"), reason="")')
    assert m.BATCH_HARD_RE.search("assert batch == 629") is not None


# E1-2：slow_tests 返回文件列表
def test_slow_tests_type():
    r = m.slow_tests()
    assert isinstance(r, list)
    assert all(isinstance(x, str) for x in r)


# E1-3：跨批脆弱返回 (file,line,text) 三元组
def test_cross_batch_shape():
    r = m.cross_batch_fragile()
    for item in r[:10]:
        assert len(item) == 3 and isinstance(item[1], int)


# E1-4：环境依赖返回 (file,skipif数)
def test_env_dependent_shape():
    r = m.env_dependent()
    assert isinstance(r, list)
    for f, n in r[:10]:
        assert isinstance(f, str) and isinstance(n, int)


# E1-5：长期方案非空 + 剩余失败为 list
def test_plan_and_remaining():
    assert len(m.plan()) >= 3
    assert isinstance(m.remaining_failures(), list)


# E1-6：--check 自检通过
def test_selftest_passes():
    assert m.selftest() == 0
