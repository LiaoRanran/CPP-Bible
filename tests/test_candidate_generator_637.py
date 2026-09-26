"""637 C · candidate_generator_637 单测（纯标准库，≥5 例）。编号 TC-1..TC-6。"""
from __future__ import annotations

import candidate_generator_637 as C


# TC-1：8 类异常方案库各 ≥2 个
def test_library_coverage():
    assert len(C.LIBRARY) == 8
    assert all(len(v) >= 2 for v in C.LIBRARY.values())


# TC-2：方案字段合法（成本/收益/风险类别）
def test_fields_valid():
    for cs in C.LIBRARY.values():
        for c in cs:
            assert c["cost"] in C.OK_LEVELS
            assert c["benefit"] in C.OK_LEVELS
            assert c["risk_class"] in C.RISK_CLASSES
            assert c["name"] and c["action"]


# TC-3：未知异常走兜底
def test_fallback():
    assert len(C.candidates_for("__unknown__")) >= 1


# TC-4：generate 结构与输入异常一一对应
def test_generate():
    demo = {"anomalies": [{"key": "grounding_pct", "name": "接地率低", "severity": "P1"},
                          {"key": "ahead", "name": "ahead 过多", "severity": "P2"}]}
    items = C.generate(demo)
    assert len(items) == 2
    assert all(len(it["candidates"]) >= 2 for it in items)


# TC-5：风险类别取值受限
def test_risk_class_values():
    assert C.RISK_CLASSES == {"report", "tool", "core"}


# TC-6：--check 自检通过
def test_selftest():
    assert C.selftest() == 0
