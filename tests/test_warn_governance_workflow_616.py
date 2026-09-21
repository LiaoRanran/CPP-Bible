#!/usr/bin/env python3
"""616 C1 回归测试：warn 治理完整工作流。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import warn_governance as wg  # noqa: E402


def test_observation_tracking() -> None:
    tr = wg.observation_tracking()
    wc = wg.load_state().get("warn_classify") or {}
    assert set(tr) == set(wc)
    for v in tr.values():
        assert v["age_batches"] >= 0 and v["first_seen_batch"] >= 0


def test_adoption_suggestions() -> None:
    sug = wg.adoption_suggestions()
    buckets = wg.classify()
    assert len(sug) == sum(1 for v in buckets.values() if v == "considerable")
    for x in sug:
        assert x["action"] == "suggest_only"        # 只建议，不自动采纳
        assert "人审" in x["suggestion"]


def test_expiry_reminders() -> None:
    rem = wg.expiry_reminders()
    buckets = wg.classify()
    assert len(rem) == sum(1 for v in buckets.values() if v == "expired_reassess")
    for x in rem:
        assert x["action"] == "remind_only"          # 只提醒，不自动删除


def test_workflow_report_written() -> None:
    p = ROOT / "data" / "warn_governance_workflow_616.md"
    assert p.is_file() and p.stat().st_size > 0
    text = p.read_text(encoding="utf-8")
    assert "不自动采纳" in text and "观察期" in text and "到期重评估" in text
