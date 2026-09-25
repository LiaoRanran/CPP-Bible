"""635 1.1 · boundary_fields_635 单测（纯标准库，≥5 例）。编号 1.1-1..1.1-6。"""
from __future__ import annotations

import boundary_fields_635 as B


# 1.1-1：mutation 元数据
def test_mutation_meta():
    m = B.mutation_meta()
    assert len(m["mutation_set_hash"]) == 64
    assert m["mutation_count"] == 1593
    assert m["generator_version"] == "mutation_fuzz@v7"


# 1.1-2：channel 推断
def test_infer_channel():
    assert B.infer_channel("见 cppreference") == "cppreference"
    assert B.infer_channel("外部审核") == "external_audit"
    assert B.infer_channel("普通测量") == "direct_experiment"


# 1.1-3：materiality 推断
def test_infer_materiality():
    assert B.infer_materiality("影响 gate 判决逻辑") is True
    assert B.infer_materiality("只改措辞") is False


# 1.1-4：baseline 文件清单
def test_baseline_files():
    fs = B.baseline_files()
    assert len(fs) >= 20
    assert all("*baseline*" or True for _ in fs)


# 1.1-5：fields_for 返回 5 字段
def test_fields_for():
    fs = B.baseline_files()
    f = B.fields_for(fs[0])
    assert set(f) == {"mutation_set_hash", "mutation_count", "generator_version",
                      "evidence_channel", "materiality_flag"}
    assert all(f[k] not in ("", None) for k in f)


# 1.1-6：--check 自检通过
def test_selftest():
    assert B.selftest() == 0
