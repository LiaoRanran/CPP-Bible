"""pytest 公共配置：把 tools/ 加入 import 路径。

本仓库 80+ 个工具脚本此前**零单元测试**（工具正确性仅靠 CI 跑通间接验证）。
本目录的测试专门锁定**真实发生过的回归**，详见各文件的 docstring。
"""
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))


# ── 500 任务 6：快慢标记分离 ────────────────────────────────────────────────
# 分类依据是**语义**（任务 6 定义）：模块内测试是否**实际调用编译器**（g++/cl）、
# **跑 replay** 或 **跑 poison**，而不是墙钟时长。
# 为何不按时长切：500 实测逐模块耗时（`_mod_times.txt`）显示热 ccache 下多数编译类
# 模块只有 1–3s（recompile_invariant 1.24s / p0g_lock 2.09s / toolchain_regressions
# 1.17s），唯二大头是 test_json_output.py（125.5s）与 test_atom_evidence_replay.py
# （12.9s）——按时长切会把"是否碰编译器"这一维度切丢。
# 默认跑全部（不加 -m 时标记不影响结果）；`-m fast` 只跑纯逻辑，`-m slow` 只跑编译类。
SLOW_MODULES = frozenset({
    "test_artifact_snapshot.py",      # replay 工件快照
    "test_atom_evidence_replay.py",   # replay 真编译
    "test_ccache_prefix.py",          # replay 编译器包装
    "test_ci_local_precheck.py",      # 调 replay
    "test_discriminative.py",         # replay 判别力
    "test_incremental_replay.py",     # 增量 replay
    "test_json_output.py",            # golden_lock / poison_drill / replay 子进程
    "test_p02_discriminative.py",     # replay 判别力
    "test_p0g_lock.py",               # replay 并发锁
    "test_patch_blocks.py",           # compile_all
    "test_poison_attack_type.py",     # poison_drill
    "test_recompile_invariant.py",    # 重编译不变量（真编译）
    "test_s1_s6.py",                  # poison_drill + golden_lock
    "test_toolchain_regressions.py",  # 真实 g++ 解析
})


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers", "slow: 调用编译器（g++/cl）/ 跑 replay / 跑 poison 的测试")
    config.addinivalue_line(
        "markers", "fast: 纯字符串 / 数据结构 / 规则判断，不调用编译器")


def pytest_collection_modifyitems(config: pytest.Config, items: list) -> None:
    """按模块归类打标（不删除、不改写任何测试；标记只影响 -m 过滤）。"""
    for item in items:
        mod = Path(str(item.fspath)).name
        item.add_marker(pytest.mark.slow if mod in SLOW_MODULES
                        else pytest.mark.fast)
