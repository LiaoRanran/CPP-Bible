# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""645 阶段 C3 · 耦合效果评估单测（fast）。"""
import os
import sys
from pathlib import Path

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import three_layer_orchestrator_645 as c3  # noqa: E402  (647 D1：C3 已并入三层耦合套件)


def _kernel_repo_available() -> bool:
    """兄弟仓 `queyi-verifier/tools/queyi_core_v10_641.py` 是否可探测到。

    与 `tests/conftest.py::_kernel_canonical_available` **逐字对齐**（自 `tools/` 起向上
    8 级找 `queyi-verifier/tools/<同名文件>`），避免两处判据分叉。
    """
    d = Path(ROOT) / "tools"
    for _ in range(8):
        if (d / "queyi-verifier" / "tools" / "queyi_core_v10_641.py").is_file():
            return True
        d = d.parent
    return False


# 674d：`c3.evaluate()` 内部经 `queyi_data_models_645` 读拆仓内核 ⇒ 单仓检出/CI 上必然
# RuntimeError（只在**运行期**触发，故 conftest 的 collect_ignore 挡不住）。这里显式 skip；
# 双仓布局下行为完全不变、仍真跑。不改工具（内核 wrapper 的 fail-loud 是设计）。
_NEEDS_KERNEL_REPO = pytest.mark.skipif(
    not _kernel_repo_available(),
    reason="拆仓 queyi-verifier 未检出 ⇒ c3.evaluate() 内部走 queyi_data_models_645 会 fail-loud",
)


@pytest.mark.parametrize("sev,expect", [("critical", "fail"), ("high", "fail"),
                                        ("medium", "needs_human"), ("low", "needs_human")])
def test_heuristic_verdict(sev, expect):
    """无耦合基线：仅按严重度启发式。"""
    assert c3._heuristic_verdict(sev) == expect


def test_selftest_passes():
    """--check 只读自检必须通过。"""
    assert c3.effect_selftest() == 0


@_NEEDS_KERNEL_REPO
def test_evaluate_real_runs_and_shapes():
    """真实评估跑通且指标完整（每项都有 with/without）。"""
    res = c3.evaluate()
    m = res["metrics"]
    for key in ("attribution_accuracy", "evidence_fetch_success", "verdict_pass_rate"):
        assert "with_coupling" in m[key] and "without_coupling" in m[key]
    assert 0.0 <= m["attribution_accuracy"]["with_coupling"] <= 1.0
    assert m["attribution_accuracy"]["without_coupling"] == 0.0
    assert res["issues_total"] >= 1


def test_write_report(tmp_path, monkeypatch):
    """报告写入到临时路径（不污染仓库 data/）。"""
    md = tmp_path / "out.md"
    js = tmp_path / "out.json"
    monkeypatch.setattr(c3, "EFFECT_REPORT_MD", str(md))
    monkeypatch.setattr(c3, "EFFECT_REPORT_JSON", str(js))
    res = {"issues_total": 1, "chain_count": 1, "verdicts": {"pass": 1},
           "metrics": {
               "attribution_accuracy": {"with_coupling": 1.0, "without_coupling": 0.0,
                                        "note": "x"},
               "evidence_fetch_success": {"with_coupling": 0.9, "without_coupling": 0.0,
                                          "note": "x"},
               "verdict_pass_rate": {"with_coupling": 1.0, "without_coupling": 0.0, "note": "x"},
               "feedback_effectiveness": {"needs_evidence": 0, "needs_human": 0,
                                          "verified_ok": 1, "head_layer_priority": "medium"},
           }}
    c3.write_effect_report(res)
    assert md.exists() and "有证据" in md.read_text(encoding="utf-8")
    assert js.exists()
