"""647 C1 · 仓库拆分沙箱验证回归锁（编号 C1-1..C1-7）。

沙箱整体**很重**（clone + fast-export/import + 收集），故用 **module 级 fixture 跑一次**复用。
所有产物都在 `tmp_path` / `tempfile` 里 ⇒ **原仓库零改动**。
"""
from __future__ import annotations

import os

import pytest
import repo_split_sandbox_647 as S


@pytest.fixture(scope="module")
def sandbox():
    return S.sandbox_run()


# ── C1-1：core 清单是「种子 ∪ import 闭包」，且不含受控目录 ────────────────────
def test_c1_1_core_file_list():
    files = S.core_files()
    assert files == sorted(set(files)) and len(files) > 50
    assert S.STANDALONE_ENTRY in files
    assert "tools/conflict_detector_647.py" in files
    # 闭包补全：前身模块（647 保护器 import 的 642 灰度 / 636 影子）必须进清单
    assert "tools/conflict_detector_636.py" in files
    assert "tools/calibration_tracker_642.py" in files
    assert not any(f.startswith(("atoms/", "evidence/", "Examples/", "Book/")) for f in files)
    # 仓库集成配置**明确不迁移**（实测它们强耦合整仓）
    for rel in S.NOT_MIGRATED:
        assert rel not in files, rel


# ── C1-2：拆分成功且保留历史（提交数 > 0）───────────────────────────────────────
def test_c1_2_split_succeeds(sandbox):
    s = sandbox.get("split", {})
    assert s.get("ok") is True, sandbox.get("why")
    assert s["n_commits"] > 0
    assert len(s["head"]) >= 7


# ── C1-3：独立可跑（内核 import + selftest）────────────────────────────────────
def test_c1_3_standalone_runs(sandbox):
    st = sandbox["standalone"]
    assert st["import_ok"] is True, st["import_tail"]
    assert st["kernel_check_rc"] == 0, st["kernel_check_tail"]


# ── C1-4：测试能跑（最小 conftest 下收集零错误）───────────────────────────────
def test_c1_4_tests_collect(sandbox):
    t = sandbox["tests"]
    assert t.get("collect_rc") == 0, t.get("tail")
    assert t.get("n_error_files") == 0, t.get("error_files")


# ── C1-5：历史保留（探针文件在两侧提交数相同）────────────────────────────────
def test_c1_5_history_preserved(sandbox):
    h = sandbox["history"]
    assert h["same"] is True, h


# ── C1-6：沙箱整体通过 + **原仓库零改动** ─────────────────────────────────────
def test_c1_6_no_origin_change(sandbox):
    assert sandbox["ok"] is True
    # 受控目录与非 core 文件都没被动过（沙箱在 tempfile 里）
    assert os.path.isdir(os.path.join(S.ROOT, "tools"))
    assert os.path.isfile(os.path.join(S.ROOT, S.STANDALONE_ENTRY))
    assert not os.path.exists(os.path.join(S.ROOT, "queyi-core")), "拆分产物不得落进原仓库"


# ── C1-7：自检 + 报告落盘 ────────────────────────────────────────────────────
def test_c1_7_selftest_and_report(sandbox):
    assert S.selftest() == 0
    assert S.write_report(sandbox) == S.OUT_MD
    assert os.path.isfile(S.OUT_MD) and os.path.isfile(S.OUT_JSON)
    text = open(S.OUT_MD, encoding="utf-8").read()
    assert "沙箱" in text and "fast-export" in text
