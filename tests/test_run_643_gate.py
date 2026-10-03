# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""643 F1 · 收工门禁 单测（验证门禁自身的判定逻辑；不重跑整库 mypy/ruff）。

编号 F1-1..F1-7。本测试刻意**不**调用 `build()` 的 ruff/mypy/643-tests 分支
（那会在 pytest 里再起 pytest/mypy，既慢又会被并发批次 644 污染）；
只验证：工具清单无拼写错、643 工具 --check 全绿、642 收尾确认、内核纯性、保护器灰度。
"""
from __future__ import annotations

import os
import sys

import run_643_gate as G
import pytest  # noqa: E402  672h：slow 标记

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))


def _kernel_repo_available() -> bool:
    """兄弟仓 `queyi-verifier/tools/queyi_core_v10_641.py` 是否可探测到。

    与 `tests/conftest.py::_kernel_canonical_available` **逐字对齐**（自 `tools/` 起向上
    8 级找 `queyi-verifier/tools/<同名文件>`）——两处判据必须同源，否则白名单会分叉
    （674d 已因分叉漏掉 9 个收集期失败文件）。
    """
    d = os.path.join(ROOT, "tools")
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "queyi-verifier", "tools", "queyi_core_v10_641.py")):
            return True
        d = os.path.dirname(d)
    return False


# F1-1：清单里的每个工具文件真实存在（无拼写错）
def test_tool_lists_match_disk():
    for name in G.NEW_TOOLS_643:
        p = os.path.join(ROOT, "tools", f"{name}.py")
        assert os.path.exists(p), f"缺失 643 工具：{name}"
    for name in G.TOOLS_642:
        p = os.path.join(ROOT, "tools", f"{name}.py")
        assert os.path.exists(p), f"缺失 642 工具：{name}"


# F1-2：每个 643 工具都有 --check 入口（门禁依赖它）
def test_new_tools_have_check_entry():
    for name in G.NEW_TOOLS_643:
        src = open(os.path.join(ROOT, "tools", f"{name}.py"), encoding="utf-8").read()
        assert '--check' in src, f"{name} 无 --check"


# F1-3：643 新工具 --check 全绿（轻量子进程）
@pytest.mark.slow
def test_new_tools_check_green():
    r = G.check_new_tools()
    assert r["ok"], r["detail"]
    assert r["gate"] is True
    assert r["detail"].startswith(f"{len(G.NEW_TOOLS_643)}/{len(G.NEW_TOOLS_643)}")


# F1-4：642 收尾确认（status + 642 工具 --check）
@pytest.mark.slow
def test_642_closure():
    r = G.check_642_closure()
    assert r["ok"], r["detail"]
    assert r["gate"] is False


# F1-5：内核零领域 import（AST 机械证明）
def test_kernel_purity():
    # 674d：`check_kernel_purity()` 需读拆仓内核 canonical ⇒ 单仓检出/CI 上必然
    # RuntimeError（工具 fail-loud 是设计，不改工具）。显式条件 skip；双仓布局下行为不变。
    if not _kernel_repo_available():
        pytest.skip("拆仓 queyi-verifier 未检出 ⇒ 内核纯度检查需 canonical 内核（fail-loud）")
    r = G.check_kernel_purity()
    assert r["ok"], r["detail"]
    assert r["detail"] == "领域 import：零"


# F1-6：642 保护器灰度验证（零漂移/零改判/可回滚）
def test_protector_rollout():
    if not _kernel_repo_available():
        pytest.skip("拆仓 queyi-verifier 未检出 ⇒ 保护器灰度验证需 canonical 内核（fail-loud）")
    r = G.check_protector_rollout()
    assert r["ok"], r["detail"]
    assert r["gate"] is False


# F1-7：受控目录检查返回结构正确（不要求一定干净——644 可能并发写入）
def test_controlled_check_shape():
    r = G.check_controlled()
    assert "detail" in r and "ok" in r
    assert r["gate"] is False


# F1-8：两阶段终验检查可调用且结构正确（证据由收工序列真跑，测试不强制绿）
def test_two_phase_check_shape():
    r = G.check_two_phase()
    assert set(r) >= {"ok", "gate", "detail"}
    assert r["gate"] is True


# F1-9：644 污染登记项是整库静态检查（node id 形如 tests/....py::test_...）
def test_polluted_registry_shape():
    assert G.POLLUTED_644
    for nid in G.POLLUTED_644:
        assert nid.startswith("tests/") and "::" in nid
