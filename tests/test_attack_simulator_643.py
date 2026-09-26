"""643 C3 · attack_simulator_643 单测（判定表/随机基线/树指纹/端到端 1 条沙箱跑）。
编号 C3-1..C3-8。**只真跑 1 条**（沙箱复制整树，成本受控）。
"""
from __future__ import annotations

import os

import attack_simulator_643 as C3
import mutation_fuzz as mf
import targeted_mutator_643 as C2


# C3-1：判定表 —— 方向 A
def test_classify_direction_a():
    assert C3.classify("A", True, True, False) == "blocked"
    assert C3.classify("A", True, False, True) == "evaded"
    assert C3.classify("A", True, False, False) == "evaded", "无连带变化也应判逃逸"


# C3-2：判定表 —— 方向 B（含 oracle_mismatch 分流）
def test_classify_direction_b():
    assert C3.classify("B", False, True, True) == "triggered"
    assert C3.classify("B", False, False, True) == "oracle_mismatch"
    assert C3.classify("B", False, False, False) == "not_triggered"


# C3-3：方向 A 优先判逃逸（即使有连带变化）
def test_evaded_takes_precedence():
    assert C3.classify("A", True, True, True) == "blocked"
    assert C3.classify("A", True, False, True) == "evaded"


# C3-4：随机基线同预算且可复现
def test_random_baseline():
    a = C3.random_plans(6, seed=7)
    b = C3.random_plans(6, seed=7)
    assert a == b and len(a) == 6
    assert all(p["generated_by"] == "random_baseline" for p in a)
    assert all(p["card"] and p["op"] in C2.OPS for p in a)


# C3-5：树指纹稳定且区分（同树两次一致；改动即变）
def test_tree_digest(tmp_path):
    d = tmp_path / "t"
    (d / "sub").mkdir(parents=True)
    (d / "a.txt").write_text("x", encoding="utf-8")
    (d / "sub" / "b.txt").write_text("y", encoding="utf-8")
    h1 = C3.tree_digest(str(d))
    assert h1 == C3.tree_digest(str(d)) and len(h1) == 64
    (d / "sub" / "b.txt").write_text("z", encoding="utf-8")
    assert C3.tree_digest(str(d)) != h1


# C3-6：沙箱机制在册（复用本仓既有 sandbox，而不是自造）
def test_sandbox_reused():
    assert hasattr(mf, "sandbox")
    assert C3.mf is mf


# C3-7：端到端 1 条（真跑沙箱）—— 判定合法 + 生产零副作用
def test_end_to_end_one_mutation():
    plans = C2.make_plan()["plans"][:1]
    s = C3.simulate(plans, limit=1)
    assert s["n_planned"] == 1 and len(s["rows"]) == 1
    assert s["production_atoms_unchanged"] is True
    assert s["rows"][0]["verdict"] in ("noop", "blocked", "evaded", "triggered",
                                       "not_triggered", "oracle_mismatch", "infra_error")
    assert os.path.isdir(os.path.join(C3.ROOT, "atoms"))


# C3-8：只读自检
def test_selftest():
    assert C3.selftest() == 0
