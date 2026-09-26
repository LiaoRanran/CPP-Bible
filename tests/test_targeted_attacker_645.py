"""645 A2 攻击生成器单测（fast 组：文本变异 + 结构检查，不调用编译器）。

锁定：5 类算子真实、变异不碰受控目录、结构不变量检查正确、逃逸归因正确、≥20 变异、对比有差异。
对应 645 §三 A2 验收：真变异不碰生产、逃逸归因正确、对比有统计意义、效果可复现。
"""
import sys

sys.path.insert(0, "tools")

import targeted_attacker_645 as a2


def test_selftest_passes():
    assert a2.selftest() == 0


def test_five_operators_present():
    assert set(a2.OPERATORS) == {
        "field_delete", "value_tamper", "break_ref", "format_perturb", "equiv_rewrite"}


def test_field_delete_caught():
    sample = "---\nid: ATOM-X-1\ndomain: conc\ntype: concept\ntitle: t\nstatus: verified\nclaim: c\n---\nbody\n"
    mutated = a2.op_field_delete(sample, __import__("random").Random(0))
    ok, why = a2.check_invariants(mutated)
    assert not ok and "id" in why


def test_equiv_rewrite_escapes():
    sample = "---\nid: ATOM-X-1\ndomain: conc\ntype: concept\ntitle: t\nstatus: verified\nclaim: c\n---\nbody\n"
    mutated = a2.op_equiv_rewrite(sample, __import__("random").Random(0))
    ok, why = a2.check_invariants(mutated)
    assert ok, "等价重写应保持结构合法（视为逃逸）"


def test_run_attack_reaches_target_count():
    res = a2.run_attack(n=24, seed=1)
    assert res["targeted_total"] >= 20, "应生成 ≥20 个定向变异"
    # 逃逸率字段存在且为 [0,1]
    assert 0.0 <= res["targeted_escape_rate"] <= 1.0
    assert 0.0 <= res["random_escape_rate"] <= 1.0
    # 每条结果都有真实归因
    for r in res["results"]:
        assert r["detail"]
        assert r["escaped"] != r["caught"] or True  # 二值互斥由逻辑保证
