#!/usr/bin/env python3
"""616 C3 回归测试：Goodhart 监控接入 metrics。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import goodhart_monitor as gh  # noqa: E402
import metrics_collector as mc  # noqa: E402


def test_new_goodhart_fields_exist() -> None:
    g = mc.collect_curves()["goodhart"]
    for k in ("goodhart_score", "goodhart_warn_growth_rate", "goodhart_legacy_growth_rate",
              "goodhart_block_rate", "goodhart_rule_coverage", "goodhart_human_reject_rate"):
        assert k in g, f"缺字段 {k}"
    assert 0.0 <= g["goodhart_score"] <= 100.0


def test_score_matches_independent_computation() -> None:
    g = mc.collect_curves()["goodhart"]
    assert g["goodhart_score"] == gh.compute()["score"]


def test_metrics_collector_runs_and_schema_intact() -> None:
    snap = mc.collect(with_heavy=False, with_gate=False)
    assert set(snap["metrics"]) == set(mc.ALL_METRICS)     # 27 项扁平 schema 未动
    assert len(mc.ALL_METRICS) == 27
