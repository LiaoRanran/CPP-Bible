"""634 B2 · horizon_634 单测（纯标准库，≥5 例）。编号 B2-1..B2-6。"""
from __future__ import annotations

import horizon_634 as H


# B2-1：曲线可读
def test_curve_readable():
    c = H.load_curve()
    assert isinstance(c, list) and len(c) >= 1


# B2-2：623 run 可读
def test_run_readable():
    r = H.load_run()
    assert r.get("rows")


# B2-3：band60_80 可取值
def test_band():
    v = H.band60_80(H.load_curve()[-1])
    assert v is not None and 0.0 <= v <= 1.0


# B2-4：新触达规则 ≥5（达标）
def test_touched_rules():
    assert len(H.touched_rules()) >= 5


# B2-5：判定分布非空且含 blocked
def test_verdicts():
    d = H.verdict_distribution()
    assert d.get("blocked", 0) >= 1


# B2-6：--check 自检通过
def test_selftest():
    assert H.selftest() == 0
