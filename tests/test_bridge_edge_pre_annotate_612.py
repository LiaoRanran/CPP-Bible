"""612 A1 回归测试：桥接候选人审预标注（锁死已知数字）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import bridge_edge_pre_annotate as a1  # noqa: E402


def test_annotate_total():
    anns = a1.annotate()
    assert len(anns) == 98


def test_all_have_pre_annotation():
    anns = a1.annotate()
    for a in anns:
        pa = a["pre_annotation"]
        assert set(pa) >= {"topic_relevance", "argument_strength",
                           "component_distance", "confidence", "action"}


def test_confidence_distribution_not_degenerate():
    anns = a1.annotate()
    summ = a1.summarize(anns)
    # 置信度不应全 high 或全 low（至少两档）
    assert len(summ["by_confidence"]) >= 2


def test_pseudo_bridge_exists():
    anns = a1.annotate()
    summ = a1.summarize(anns)
    assert summ["pseudo_bridge_count"] > 0


def test_action_mix_has_reject():
    anns = a1.annotate()
    summ = a1.summarize(anns)
    # 论证关系弱的伪桥接应被建议 reject（动作分布非单一）
    assert summ["by_action"].get("reject", 0) > 0
    assert summ["by_action"].get("approve", 0) > 0


def test_check_passes():
    # --check 通过（exit 0）
    assert a1.main(["--check"]) == 0
