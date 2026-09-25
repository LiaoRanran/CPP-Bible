"""635 1.2 · tau_d_635 单测（纯标准库，≥5 例）。编号 1.2-1..1.2-6。"""
from __future__ import annotations

import tau_d_635 as T

_ROWS = [
    {"hash": "a", "date": "2026-09-01", "subject": "escaped 3 条 逃逸"},
    {"hash": "b", "date": "2026-09-05", "subject": "触达 新增 2 条规则"},
    {"hash": "c", "date": "2026-09-10", "subject": "无关提交"},
]


# 1.2-1：逃逸事件识别 + 计数
def test_escape_events():
    ev = T.escape_events(_ROWS)
    assert len(ev) == 1 and ev[0]["count"] == 3


# 1.2-2：修补事件识别
def test_fix_events():
    assert len(T.fix_events(_ROWS)) == 1


# 1.2-3：τ_d 计算
def test_tau_d():
    t = T.tau_d(_ROWS)
    assert len(t) == 1 and t[0]["days"] == 4


# 1.2-4：渠道分类
def test_channel():
    assert T.channel({"subject": "沙箱实跑 escaped"}) == "A(mutation实跑)"
    assert T.channel({"subject": "外部审核 逃逸"}) == "C(外部审核)"


# 1.2-5：stats 分布
def test_stats():
    s = T.stats([1, 2, 3, 4, 5])
    assert s["n"] == 5 and s["median"] == 3 and s["min"] == 1 and s["max"] == 5


# 1.2-6：--check 自检通过
def test_selftest():
    assert T.selftest() == 0
