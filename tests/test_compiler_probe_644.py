"""644 D2 编译器实测获取器单测（P2-1..P2-4）。"""
from __future__ import annotations

import os

import compiler_probe_644 as d2
import evidence_base_644 as base

SNIPPET = "#include <iostream>\nint main(){ std::cout << \"42\" << std::endl; return 0; }\n"


# P2-1：已知片段输出正确
def test_output_correct():
    if d2.find_compiler("g++") is None:
        return
    r = d2.probe(SNIPPET)
    assert r["ok"] is True
    assert "42" in r["output"]
    assert r["exit_code"] == 0


# P2-2：多选项支持
def test_multi_option():
    if d2.find_compiler("g++") is None:
        return
    r = d2.probe(SNIPPET, ["-std=c++17", "-O0"])
    assert r["ok"] is True


# P2-3：沙箱不污染（临时目录生成且可清理，不碰生产）
def test_sandbox():
    if d2.find_compiler("g++") is None:
        return
    r = d2.probe(SNIPPET)
    assert r["sandbox"] is not None
    d2.cleanup(r["sandbox"])
    assert not os.path.isdir(r["sandbox"])


# P2-4：等级判定 L1 + selftest
def test_grade_l1_and_selftest():
    if d2.find_compiler("g++") is None:
        return
    r = d2.probe(SNIPPET)
    rec = d2.make_evidence(SNIPPET, r)
    assert rec.grade == "L1"
    os.remove(base.store_path(rec.evidence_id))
    assert d2.selftest() == 0
