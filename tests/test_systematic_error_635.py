"""635 V26-2 · systematic_error_635 单测（纯标准库，≥5 例）。编号 V2-1..V2-6。"""
from __future__ import annotations

import systematic_error_635 as S


# V2-1：可收敛非空
def test_convergent():
    assert len(S.convergent()) >= 1


# V2-2：不可收敛非空
def test_non_convergent():
    assert len(S.non_convergent()) >= 1


# V2-3：逃逸率属可收敛
def test_escape_convergent():
    assert any("逃逸率" == n for n, _ in S.convergent())


# V2-4：自身免疫率属不可收敛
def test_autoimmune_non_convergent():
    assert any("自身免疫率" in n for n, _ in S.non_convergent())


# V2-5：分类互斥且全覆盖
def test_partition():
    cv = {n for n, _ in S.convergent()}
    nv = {n for n, _ in S.non_convergent()}
    assert not (cv & nv)
    assert len(cv) + len(nv) == len(S.METRICS)


# V2-6：--check 自检通过
def test_selftest():
    assert S.selftest() == 0
