"""645 B2/B3 编译器实测单测（slow 组：真实调用 g++/clang++）。

锁定：编译器可检测、真实编译可读退出码、双编译器对比、等级判定、聚合覆盖 ≥15 卡。
对应 645 §四 B2/B3 验收：批量跑不超时、≥15 条证据、等级 L1、沙箱不污染。
"""
import os
import sys

import pytest

sys.path.insert(0, "tools")

from compiler_probe_645 import (
    CLANG_CANDIDATES,
    GPP_CANDIDATES,
    _which,
    compile_once,
    iter_ev_fixtures,
    run_probe,
    selftest,
)

pytestmark = pytest.mark.slow


def test_selftest_passes():
    assert selftest() == 0


def test_compilers_detectable():
    gpp = _which(GPP_CANDIDATES)
    assert gpp is not None, "本环境应有 g++"
    # clang 可能无；若有则为真路径
    clang = _which(CLANG_CANDIDATES)
    if clang is not None:
        assert os.path.exists(clang)


def test_iter_ev_fixtures_reads_real_data():
    fx = iter_ev_fixtures()
    assert len(fx) > 0, "应读到真实 EV fixture"
    # 每条都有存在的 fixture 文件与 serves 目标
    for f in fx[:5]:
        assert os.path.exists(f["fixture_abs"])
        assert isinstance(f["serves"], list)


def test_single_real_compile_records_exit_code():
    gpp = _which(GPP_CANDIDATES)
    clang = _which(CLANG_CANDIDATES)
    fx = iter_ev_fixtures()
    tmp = __import__("tempfile").mkdtemp(prefix="645t_")
    try:
        rec = compile_once(gpp, clang, fx[0]["fixture_abs"], "g++", "c++17", "-O2", tmp)
        # 退出码必须是真实进程返回（0/1/非 0），绝不编造
        assert rec.exit_code is not None
        assert isinstance(rec.output, str)
        assert rec.compiler == "g++"
    finally:
        __import__("shutil").rmtree(tmp, ignore_errors=True)


def test_limited_probe_aggregates_real():
    gpp = _which(GPP_CANDIDATES)
    clang = _which(CLANG_CANDIDATES)
    result = run_probe(gpp, clang, limit=3)
    # 真实编译记录非空，且每张被探测卡都有 g++ 结果
    assert result["compile_runs"] > 0
    assert result["fixtures_probed"] >= 1
    # 等级只能是 L1/L2/L5（真实判定）
    for info in result["per_card"].values():
        assert info["grade"] in ("L1", "L2", "L5")
    # 双编译器信息如实反映环境
    assert result["clang_available"] == (clang is not None)


def test_probe_reaches_target_card_count():
    """全量探测应覆盖足够多的卡（B2 目标 ≥15 张卡有 L1/L2 证据）。

    注：受 CI 时长限制，本测试跑全量（约百次真实编译），标记 slow 串行执行。
    """
    gpp = _which(GPP_CANDIDATES)
    clang = _which(CLANG_CANDIDATES)
    result = run_probe(gpp, clang)
    # 至少有 15 张卡拿到真实编译证据（g++ 通过即计）
    assert result["cards_with_l1"] >= 15, (
        f"有证据卡仅 {result['cards_with_l1']} 张，未达 B2 ≥15 目标")
