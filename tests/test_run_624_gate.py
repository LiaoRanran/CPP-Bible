"""624 F1 收工门禁 · 单元测试（≥3 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import run_624_gate as g  # noqa: E402


def test_batch_624_files_enumerated():
    files = g.batch_624_files()
    assert len(files) >= 5
    assert all("_624" in os.path.basename(p) for p in files)


def test_ci_yml_ok():
    assert g.ci_yml_ok() is True


def test_selftest_passes():
    assert g.selftest() == 0


def test_gate_passes():
    # 完整收工门禁（整目录 ruff + 本批 ruff + 工具 --check + ci.yml + 零污染）
    assert g.main([]) == 0
