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
    "test_mutation_fuzz.py",          # 539：沙箱内跑整轮门禁 + M1/M7 真跑 replay
})


# 508：除 SLOW_MODULES 外，**读真实仓库可变状态**的模块也必须同组——replay 的校验流程是
# 「删旧工件 → 重生成 → 比 sha → 还原」，期间 `Examples/atoms/*.asm` 会**瞬时不存在/内容不同**；
# 若另一个 worker 恰在此时读它（如 writer_selfcheck 的 WC-01「磁盘 sha == 卡值」、
# gate 的 `EV-ARTIFACT-FILE-EXISTS` 存在性），就会假红。串行组 wall 由
# `test_golden_lock_json`（~125s）主导，把这些模块并进去**不增加 wall**。
SERIAL_EXTRA = frozenset({
    "test_gate_engine.py",       # 真实仓库规则扫描（读工件存在性/内容）
    "test_writer_selfcheck.py",  # WC-01 磁盘 sha == 卡值（对瞬时改写最敏感）
    "test_artifact_version.py",  # 工件版本台账 + 工件事存在性
})


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers", "slow: 调用编译器（g++/cl）/ 跑 replay / 跑 poison 的测试")
    config.addinivalue_line(
        "markers", "fast: 纯字符串 / 数据结构 / 规则判断，不调用编译器")
    config.addinivalue_line(
        "markers", "serial: 必须串行执行（共享文件锁/端口/固定路径）。"
                   "**当前无测试使用**——508 实测 xdist 的 loadgroup 分组在本版本不生效，"
                   "改由 `-m slow` 切分两阶段（见 pyproject 的 addopts 注释）实现同样的隔离；"
                   "保留本标记供未来按测试粒度标注时使用（届时用 `-m serial -n0` 单独跑）")


def pytest_collection_modifyitems(config: pytest.Config, items: list) -> None:
    """按模块归类打标（不删除、不改写任何测试；标记只影响 -m 过滤）。

    508 任务1 的落点是**按模块切 slow/fast 两组**（配合 pyproject 注释里的两阶段命令：
    `pytest -m "not slow" -n auto` 跑纯逻辑，`pytest -m slow -n0` 跑共享真实仓库状态的）。
    这条切分是**不依赖 xdist 分组**的——508 实测 `--dist loadgroup` + `xdist_group` 在
    xdist 3.8 下不生效（同组测试仍散在多个 worker，并发跑 replay 会撞全局锁报
    `replay 锁被占用超时`），故放弃分组、改用标记切分。
    """
    for item in items:
        mod = Path(str(item.fspath)).name
        slow = mod in SLOW_MODULES or mod in SERIAL_EXTRA
        item.add_marker(pytest.mark.slow if slow else pytest.mark.fast)
