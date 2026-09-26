"""pytest 公共配置：把 tools/ 加入 import 路径。

本仓库 80+ 个工具脚本此前**零单元测试**（工具正确性仅靠 CI 跑通间接验证）。
本目录的测试专门锁定**真实发生过的回归**，详见各文件的 docstring。
"""
import os
import subprocess
import sys
import time
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
    "test_poison_coverage_581.py",    # 581 hole A：跑 poison_drill 钻探（行为级 covered）
    "test_poison_exemptions_581.py",  # 581 hole B：含一次钻探做 fail-closed 端到端验证
    "test_build_reproducibility_603.py",   # 603 T1/T3.2：调 g++ 真编译（引擎 + 毒样例 P80–P83）
    "test_recompile_invariant.py",    # 重编译不变量（真编译）
    "test_replay_invariants_603.py",  # 603 T3.1：replay_card 真编译（不变量回归锁）
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
    # 583 任务 0：**断言"真实仓全树指纹/manifest 字节不变"** 的两个模块。
    #   病：它们读 `Examples/atoms/evidence` 全树指纹，而 `-n auto` 全套里**别的 worker 的
    #   合法写盘**（replay 删-重建工件；writer_selfcheck/artifact_version 修工件）会让指纹变
    #   ⇒ 假红（实测：全套红、单模块并行/串行/静默树全套均绿）。
    #   挂 `replay_serial` 只挡 replay 一家 ⇒ 挡不住其余写者，故按本仓既有机制整模块串行。
    "test_mutation_isolation_579.py",   # 579：跑批对真实仓零副作用（Examples 指纹 + manifest 字节）
    "test_mutation_parallel_580.py",    # 580：并行跑批后真实根指纹/真实锁不动
    "test_replay_lock_serial.py",        # 592：整模块操作全局 build/.replay_lock，并发下与 replay 抢锁假红
    # 607 收工门禁暴露：605/606 的 replay 不变量检查**读真实仓可变状态**（`build/.replay_lock`
    #   是否存在、`Examples/` 工件指纹、真实 metrics 的 run_checks 结果）。`-n auto` 跑法下，
    #   别的 worker 合法地持锁（挂了 `replay_serial` 的 **fast** 用例，如
    #   `test_output_snapshots::test_kg_stats_counts`）⇒ `test_lock_no_stale_in_real_repo`
    #   把"别人正持锁"误判成"锁泄漏"、`test_metrics_invariants_all_true` 读到
    #   `lock_consistency=False`（实测：全套 `-n auto` 红、这两例 `-n0` 绿）。
    #   与 592/583 同因同治：整模块移入串行组（`-m slow -n0` 仍完整执行，覆盖率不减）。
    #   注：`test_replay_invariants_603.py` 早在 SLOW_MODULES 里，605/606 属同族漏挂。
    "test_replay_invariants_605.py",     # 607：断言真实 `Examples/` 工件指纹稳定（读真实仓）
    "test_replay_invariants_606.py",     # 607：断言真实锁不存在 + 真实 metrics 的 run_checks 全真
    "test_replay_invariants_608.py",     # 608：I1/I4 真跑 replay_card + T7 改 Examples/ 工件（读真实仓）
    "test_build_reproducibility_608.py", # 608 B2：I2 真编译（符号表/段/跨时间窗口，读真实仓）
    # ── 643 任务0：**实测**并行假红（fast = `-m "not slow" -n auto`）增量移入串行组 ──────
    # 取证：643 首次 fast 跑出 3111 例中 **35 红**；把 35 例逐个**串行复跑**：
    #   32 例串行绿（并行假红）+ 3 例串行仍红（真红，根因 = 643 新工具自身的 mypy
    #   `no-any-return`，已修）。⇒ 32 例是**并行竞争**造成的假红，落在这 24 个模块上。
    #   证据文件：`_auto/_643_parallel_reds.json`（含 valid 闸门：必须真跑到用例才算证据）。
    # 共同特征（与 508/559/583/592/607 同因）：**跑 gate/自检子进程** 或
    #   **读真实仓可变状态**（`data/` 产物、`Examples/` 工件、`build/.replay_lock`），
    #   与别的 worker 的**合法写盘**竞争 ⇒ 读到自己写过的中间态。
    # 为什么整模块移入而不是逐例：本仓机制就是模块级打标（见上），且不增加 slow 组墙钟量级。
    # ⚠️ 该清单是**经验累积（实测到的）**，不声称完备；fast 复跑若再现新红，继续增量登记。
    "test_622_a2.py",
    "test_622_gate.py",
    "test_autoimmune_auto_fill_631.py",
    "test_autoimmune_human_queue_631.py",
    "test_autoimmune_recalc_630.py",
    "test_autoimmune_threshold_630.py",
    "test_baseline_629.py",
    "test_baseline_630.py",
    "test_baseline_631.py",
    "test_coverage_probe_l1_2_631.py",
    "test_guard_hijack_640.py",
    "test_merkle_integrity_601.py",
    "test_merkle_proof_613.py",
    "test_metrics_613.py",
    "test_oracle_gate.py",
    "test_output_snapshots.py",
    "test_pollution_bisect_631.py",
    "test_pre_push_630.py",
    "test_queyi_core_interface_v02_631.py",
    "test_run_624_gate.py",
    "test_run_635_gate.py",
    "test_run_639_gate.py",
    "test_third_party_audit_demo_628.py",
    "test_vsa_attestation_628.py",
    # ── 643 任务0：第二轮 fast 复跑**增量**登记（同一取证方法）───────────────────
    # 第二轮 11 红中：4 例是 643 **自身引入的真缺陷**（已修：① `failed_node_ids`
    # 漏 `.py` ⇒ 选例静默 0 例；② 落盘日志带 ANSI ESC ⇒ 污染 `data/` 的两条
    # "无控制字符"测试），另 6 例是并行假红（串行复跑全绿）。
    "test_autoimmune_dashboard_629.py",
    "test_autoimmune_probe_629.py",
    "test_ci_pytest_triage_631.py",
    "test_learner_twin_gate_628.py",
    "test_prop_graph.py",
    "test_queyi_core_cpp_641.py",
    # ── 643 任务0：**原则性规则**（不再逐例围堵）──────────────────────────────
    # 规则：**门禁脚本测试（`test_run_*_gate*.py`）一律串行**。理由（实测 + 结构）：
    #   它们的断言对象是**真实仓库的当场状态**（受控目录 git 状态、`data/` 产物、
    #   工具 `--check` 返回值），且**自己会起子进程再读同一批状态** ⇒
    #   与别的 worker 的合法写盘/子进程**结构性竞争**，跑多少次都会随机红几例
    #   （643 实测：第一轮 35 红 → 第二轮 11 红 → 逐例围堵无收敛迹象）。
    #   串行运行零成本争议：这些模块本身跑子进程，`-n auto` 的加速被 IO/进程争抢抵消。
    # ⚠️ 仍**不声称完备**：该规则覆盖"门禁类"，其他读真实仓状态的模块继续按实测增量登记。
    "test_run_612_gate.py",
    "test_run_613_gate.py",
    "test_run_614_gate.py",
    "test_run_615_gate.py",
    "test_run_623_gate.py",
    "test_run_625_gate.py",
    "test_run_627_gate.py",
    "test_run_628_gate_628.py",
    "test_run_629_gate.py",
    "test_run_630_gate.py",
    "test_run_632_gate.py",
    "test_run_633_gate.py",
    "test_run_634_gate.py",
    "test_run_636_gate.py",
    "test_run_637_gate.py",
    "test_run_638_gate.py",
    "test_run_641_gate.py",
    "test_run_642_gate.py",
})


# ── 559 Part B：读真实仓库状态的测试，与 replay 用**同一把锁**串行 ─────────────
# 为什么需要：replay 校验一卡是「删旧工件 → 重生成 → 比 sha → 还原」，期间
# `Examples/atoms/*.asm` **瞬时**不存在/内容不同。若另一个 worker 恰在此时读它
# （golden_lock 的门禁扫描、writer_selfcheck 的 WC-01「磁盘 sha == 卡值」）就会假红
# —— 558 验收里"错误地对 slow 用 `-n auto`"正是这么红的（559 实测探针 3/3 复现非 pass）。
# 为什么用**同一把**锁：508 已证 `--dist loadgroup` + `xdist_group` 在本版 xdist **不生效**
# （调度器读不到 marker），所以只能靠"真互斥"：本 fixture 直接复刻 `replay_card` 的取锁
# 逻辑（`build/.replay_lock`）⇒ 持锁期间任何 replay 都被挡在改写动作之前，读到的状态是稳的。
# 拿不到锁（确有 replay 在跑）⇒ **带因 skip**（绝不让测试假失败）；权威两阶段跑法
# （`-m slow -n0`）里锁是空的，故这两例正常执行、不会被 skip。
_REPLAY_LOCK_WAIT = 5.0


@pytest.fixture()
def replay_serial():
    """把"读真实仓库工件状态"的断言包在 replay 的同一把锁里（任意 `-n` 跑法都不假红）。"""
    import atom_evidence_replay as replay

    try:
        replay._acquire_replay_lock(wait_timeout=_REPLAY_LOCK_WAIT)
    except TimeoutError as exc:
        pytest.skip(f"replay 正在改写工件（共享 build/.replay_lock 被占）：{exc}")
    try:
        yield
    finally:
        replay._release_replay_lock()


def pytest_configure(config: pytest.Config) -> None:
    # ── 591 任务 3：测试器配置完整性自检（conftest/pyproject 被篡改 ⇒ 拒绝开跑）──────────
    # 病（590 A2）：conftest.py 在收集前执行，可通过 `pytest_runtest_makereport` 把 failed 改判
    #   passed；而它不在 CORE_TOOLS、无完整性校验 ⇒ 篡改它可让"pytest 全绿"而判决被抽空。
    # 纵深防御边界（如实登记）：钩子本身在 conftest 里，攻击者"改钩子 + 重签基准"仍可绕过
    #   ⇒ 防得住"只改内容不改哈希"，防不住"改钩子并重签"；根治需 conftest 入 CORE_TOOLS 且
    #   enforce() 在 pytest 之外独立校验（会改架构），故本批不做、只上这一层。
    _r = subprocess.run(
        [sys.executable, "tools/tool_integrity.py", "--check-test-config"],
        capture_output=True, text=True,
        cwd=str(Path(__file__).resolve().parent.parent))
    if _r.returncode != 0:
        pytest.exit(
            f"测试器配置完整性校验失败（conftest/pyproject 被篡改）：\n{_r.stderr}",
            returncode=2)
    # ── 559 Part C：把 pytest 临时目录移进仓内（`.pytest_tmp/`，已 .gitignore）──────
    # 病（实测）：默认 tmp 在系统 `%TEMP%\pytest-of-<user>\`，会话收尾要把整批
    # `tmp_path` 一次 rmtree 掉；本环境有一层删除拦截（safe-delete），单次操作子树
    # >500 文件就报 `[SAFE_DELETE_BULK_CONFIRM_REQUIRED]`（实测 count=1053）⇒ 会话收尾
    # 被截断（卡很久、连 pytest 汇总行都打不出来）。
    #
    # 为什么不是 `--basetemp=.pytest_tmp`（提示词的处方，实测**不可用**）：
    #   `--basetemp` 指向固定目录时，pytest 每次启动都会先 **rmtree 掉已存在的 basetemp**
    #   ⇒ 第二次运行必然撞拦截层：实测 `_safe_shutil_rmtree('\\\\?\\C:\\…\\.pytest_tmp')`
    #   抛错误 → 凡是使用 `tmp_path` 的用例整片 fixture ERROR（比原来更坏）。
    #   拦截层的旁路条件是"路径在 **OS 临时目录**下"或"执行上下文已失效"，**仓内路径不旁路**；
    #   且 pytest 传的是 `\\?\` 扩展长度路径，连 `%TEMP%` 那条旁路也比对不上。
    #
    # 故改为：**每次运行给一个全新子目录**（`run-<pid>-<ts>`）。
    #   * 目录不存在 ⇒ pytest 的 `rm_rf` 直接返回，**不触发任何删除** ⇒ 不碰拦截层；
    #   * 不用 `pytest-of-<user>` 编号目录 ⇒ 不再有 `garbage-*` 批量回收；
    #   * 结果：连跑任意轮都无 safe-delete 输出，`git status` 也不出现（已 gitignore）。
    # 代价：`.pytest_tmp/run-*` 会按运行次数堆积（可随时手工清；本环境删除会被拦截层拦，
    #   故留给人工/CI 清理，不影响测试判定）。
    if not config.option.basetemp:
        _repo = Path(__file__).resolve().parent.parent
        (_repo / ".pytest_tmp").mkdir(parents=True, exist_ok=True)
        config.option.basetemp = str(
            _repo / ".pytest_tmp" / f"run-{os.getpid()}-{int(time.time())}")
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
