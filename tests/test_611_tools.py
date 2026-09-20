"""611 新工具回归测试（锁定冻结数据与图结构的已知数字）。

这些测试是 611 收工门禁的一部分：任何一个数对不上（图结构/卡数据漂移）都会让对应 --check 或本测试红，
逼人重看"碎片化是否改善 / 口径是否被改"。

运行：`python -m pytest tests/test_611_tools.py -q`
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import bridge_edge_candidates as c2   # noqa: E402
import fragmentation_repair_analysis as c3  # noqa: E402
import out_mis_review_support as d1   # noqa: E402
import liveness_completion_plan as d2  # noqa: E402
import oracle_verification_plan as d3  # noqa: E402
import metrics_611 as e1              # noqa: E402
import human_review_quality_deepen as e2  # noqa: E402
import defense_chain_deepen as e3     # noqa: E402


def test_c2_bridge_candidates():
    cands = c2.generate_candidates(c2.load_mis_index(), c2.component_map())
    s = c2.summarize(cands)
    assert s["total"] == 98
    assert s["by_priority"] == {"strong": 0, "medium": 0, "weak": 98}
    assert c2.check(cands) == []  # --check 锁定


def test_c3_fragmentation_repair():
    r = c3.analyze(cands=c3.load_candidates())
    assert r["components_before"] == 11
    assert r["components_after"] == 7
    assert r["largest_after"] == 97
    assert r["coverage_after"] == 0.8017
    assert r["verdict_changed"] == 0  # 候选皆 low，不应翻转胜负
    assert c3.check(r) == []


def test_d1_out_mis_review():
    a = d1.analyze()
    assert a["out_mis_count"] == 7
    assert d1.check(a) == []


def test_d2_liveness_plan():
    p = d2.build_plan()
    assert p["total_missing"] == 50
    assert d2.check(p) == []


def test_d3_oracle_plan():
    p = d3.build_plan()
    assert p["cards_total"] == 83
    assert p["by_kind"].get("evidence") == 56
    assert p["by_kind"].get("atom") == 27
    assert p["verified"] == 0
    assert d3.check(p) == []


def test_e1_metrics_611():
    notes: dict = {}
    m = e1.collect_611_new_metrics(notes)
    assert notes == {}  # 全部采集器成功，无错误记账
    assert m["argument_graph_fragmentation"]["components"] == 11
    assert m["bridge_candidates"]["total"] == 98
    assert m["out_mis_review"]["out_mis_count"] == 7
    assert m["liveness_missing"]["missing_observation"] == 50
    assert m["oracle_verification"]["cards_total"] == 83
    assert m["oracle_verification"]["verified"] == 0


def test_e2_human_review_quality_deepen():
    a = e2.analyze()
    assert a["records"] == 388
    assert a["reviewer_diversity"]["distinct_reviewers"] == 1
    assert a["mis_consistency"]["modify_only_count"] == 7
    assert e2.check(a) == []


def test_e3_defense_chain_deepen():
    a = e3.analyze()
    assert a["total_nodes"] == 121
    assert a["nodes_whose_demote_changes_something"] == 107
    assert a["max_ripple"] == 1
    assert e3.check(a) == []
