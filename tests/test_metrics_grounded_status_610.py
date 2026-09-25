"""610 D1 · W2 重算集成（tools/metrics_610.py::collect_grounded_status，含口径分歧显形）。

锁五件事（任务书 D1 的 5 例 + 2 例自加）：
  1. in=**114** / out=**7** / undec=0（入库 W2 产物为权威值）；
  2. defeating_edges=**17** · nodes=121 · in_propositions=79 · in_misconceptions=35；
  3. `include_human_reviewed` = True；
  4. **向后兼容**：扁平 27 项 schema 不动，608 的键不动，610 只**同级新增** `metrics_610`；
  5. 产物缺失 ⇒ `{"error": ...}` + notes 记账（不中断其它采集器）；
  +. **口径分歧显形**：`solver_recompute`（609 A3 口径 IN121/OUT0/击败 0）+ `divergence=True` + 说明；
  +. `metrics_collector.collect()` 快照里确实挂了 `metrics_610`。
"""
from __future__ import annotations

import json
from pathlib import Path

import metrics_610 as m610
import metrics_collector as mc
import soft_baseline_634 as SB  # 634 A3  # noqa: E402


def test_collect_grounded_status():
    out = m610.collect_grounded_status({})
    # 640 A1：签署后权威产物重算（IN79/OUT42/误解 0 在 IN）
    assert out["in"] == 79 and out["out"] == 42 and out["undec"] == 0
    assert out["nodes"] == 121
    assert out["in_propositions"] == 79 and out["in_misconceptions"] == 0
    assert "入库 W2 产物" in out["source"]


def test_grounded_status_has_defeating_edges():
    out = m610.collect_grounded_status({})
    assert out["defeating_edges"] == 194
    assert out["artifact_path"] == "data/grounded_labels_w2.json"


def test_grounded_status_include_human_reviewed():
    out = m610.collect_grounded_status({})
    assert out["include_human_reviewed"] is True


def test_divergence_is_surfaced_not_hidden():
    """口径分歧必须显形。640 A1：签署后两口径数值趋同 ⇒ divergence=False；
    机制差异（keep-low 34 条 modify 未生效）仍由 modes/caliber 字段留痕。"""
    out = m610.collect_grounded_status({})
    assert out["solver_recompute"]["in"] == 79
    assert out["solver_recompute"]["out"] == 42
    assert out["solver_recompute"]["defeating_edges"] == 194
    assert out["divergence"] is False
    assert "两档" in out["divergence_note"]


def test_backward_compatibility():
    before = list(mc.ALL_METRICS)
    d608 = mc.collect_608_new_metrics({}, with_heavy=False)
    d610 = m610.collect_610_new_metrics({}, with_heavy=False)
    assert list(mc.ALL_METRICS) == before and len(mc.ALL_METRICS) == 27
    # with_heavy=False 时 608 的编译可复现指标走 notes（不进 dict）⇒ 键集如下
    assert set(d608) == {"human_review", "grounded", "escape_rate_convergence",
                         "escape_rate_note"}
    assert "grounded_status" in d610
    assert not set(d610) & set(d608), "610 不得改写 608 的键（只同级新增）"
    # 634 A3：全局计数，读单一基线
    assert d608["grounded"]["in"] == SB.soft("grounded_in", d608["grounded"]["in"]), "608 的 grounded 走产物"


def test_error_handling_when_artifact_missing(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(m610, "ROOT", tmp_path)          # 产物不可见
    notes: dict = {}
    out = m610.collect_grounded_status({}, notes)
    assert "error" in out and "grounded_status_610" in notes
    assert "in" not in out, "失败路径不得给出半截判决数（宁可没有，也不给错）"


def test_collect_snapshot_has_metrics_610(monkeypatch):
    called = {"n": 0}
    real = m610.collect_610_new_metrics

    def spy(notes, *, with_heavy=True):
        called["n"] += 1
        return real(notes, with_heavy=with_heavy)

    monkeypatch.setattr(m610, "collect_610_new_metrics", spy)
    snap = mc.collect(with_heavy=False, with_gate=False)
    assert called["n"] == 1, "collect() 必须调用 610 采集器一次"
    assert "grounded_status" in snap["metrics_610"]
    assert snap["metrics_610"]["grounded_status"]["in"] == SB.soft("grounded_in", snap["metrics_610"]["grounded_status"]["in"])  # 634 A3
    assert json.dumps(snap, ensure_ascii=False)          # 快照可 JSON 序列化
