"""643 B2 · attack_gap_scanner_643 单测（深度判据/35 向量/低深度清单/引用扫描/只读）。
编号 B2-1..B2-8。
"""
from __future__ import annotations

import attack_gap_scanner_643 as B2


# B2-1：深度判据单调（0→1→2→3）
def test_depth_monotonic():
    d0, _ = B2.depth_of("X", False, set(), set(), set())
    d1, _ = B2.depth_of("X", True, set(), set(), set())
    d2, _ = B2.depth_of("X", True, {"X"}, set(), set())
    d3, _ = B2.depth_of("X", True, {"X"}, set(), {"X"})
    assert (d0, d1, d2, d3) == (0, 1, 2, 3)


# B2-2：无探针但有真实事件 ⇒ 不停在深度 0
def test_no_probe_but_real_event():
    d, why = B2.depth_of("X", False, {"X"}, set(), set())
    assert d >= 2 and any("真实攻击事件" in w for w in why)


# B2-3：深度 1 的理由必须是"仅结构性"
def test_depth1_reason_mentions_structural_only():
    d, why = B2.depth_of("X", True, set(), set(), set())
    assert d == 1 and any("仅结构性" in w for w in why)


# B2-4：深度 2 的理由必须点出"未验证真的拦住"
def test_depth2_reason_mentions_unverified():
    d, why = B2.depth_of("X", True, {"X"}, set(), set())
    assert d == 2 and any("未验证" in w for w in why)


# B2-5：35 向量全覆盖 + 深度分布自洽
def test_all_vectors_and_depth_distribution():
    a = B2.assess()
    assert a["n_vectors"] == 35
    assert sum(a["by_depth"].values()) == 35
    assert set(a["by_depth"]) == {0, 1, 2, 3, 4}


# B2-6：已知低深度向量必被标（深度 ≤1 清单非空）
def test_low_depth_vectors_flagged():
    a = B2.assess()
    assert len(a["only_structural"]) + len(a["untouched"]) > 0
    ids = {r["id"] for r in a["rows"] if r["depth"] <= 1}
    assert ids == set(a["only_structural"]) | set(a["untouched"])


# B2-7：引用扫描排除定义/汇总类文件（否则所有向量都会被自己"引用"）
def test_reference_index_excludes_definers():
    idx = B2.reference_index(["L1.1", "L4.2", "L8.5"])
    for files in idx.values():
        assert not (set(files) & set(B2.SKIP_REF_FILES))


# B2-8：known_error_rate 无数据结论有据 + 只读自检
def test_no_error_data_and_selftest():
    a = B2.assess()
    assert a["tracker_snapshot"]["n_with_samples"] == 0
    assert a["no_error_data_all"] is True
    assert all(r["no_error_data"] for r in a["rows"])
    assert B2.selftest() == 0
