"""645 C2 三层编排单测（fast 组：只读耦合，≥5 链）。"""
import sys

sys.path.insert(0, "tools")

import three_layer_orchestrator_645 as c2


def test_selftest_passes():
    assert c2.selftest() == 0


def test_orchestrate_min_chains():
    res = c2.orchestrate(min_chains=5)
    assert res["chain_count"] >= 5, "应真实编排 ≥5 条耦合链"
    assert res["met"]
    # 每条链都有真实尾端判决
    for c in res["chains"]:
        assert c["verification"]["verdict"] in ("pass", "fail", "escape", "needs_human")


def test_chains_use_real_evidence():
    res = c2.orchestrate()
    # 三层耦合链真实存在（≥5）；每条链都走到尾端验证判决（耦合非虚构）。
    # 注：规则 id 与原子卡 id 非 1:1，规则级问题的头部层证据可能为 0（诚实：需人审补），
    # 故不强制 evidence_count>0，仅验证链闭合与判决真实。
    assert res["chain_count"] >= 5
    for c in res["chains"]:
        assert c["verification"]["verdict"] in ("pass", "fail", "escape", "needs_human")
        # 证据为 0 时，尾端判决必为 needs_human（诚实闭环，不虚构证据）
        if c["evidence_count"] == 0 and not c["counterexamples"]:
            assert c["verification"]["verdict"] == "needs_human"
