#!/usr/bin/env python3
"""615 C1 回归测试：warn_governance（不增锁机制）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import warn_governance as wg  # noqa: E402


def test_new_warn_not_auto_adopted() -> None:
    fake = {"warn_classify": {"R-NEW": "real"},
            "accepted": [{"ts": "2026-01-01", "reason": "b0"}]}
    assert wg.classify(fake).get("R-NEW") == "new"


def test_observation_period() -> None:
    fake = {"warn_classify": {"R1": "real"},
            "accepted": [{"ts": "2026-01-01", "reason": "b", "classify": {"R1": "real"}},
                         {"ts": "2026-01-02", "reason": "b"}]}
    # age=1 < 观察期 3 ⇒ observation（不可采纳）
    assert wg.classify(fake, observation=3).get("R1") == "observation"
    # 放宽观察期为 1 ⇒ 变可考虑
    assert wg.classify(fake, observation=1).get("R1") == "considerable"


def test_adopted_requires_approval() -> None:
    bad = {"warn_classify": {"R2": "legacy"}, "accepted": [{"ts": "2026-01-01", "reason": "b0"}]}
    assert wg.approvals_ok(bad), "已采纳但无 acceptance classify 记录应报错"
    good = {"warn_classify": {"R2": "legacy"},
            "accepted": [{"ts": "2026-01-01", "reason": "b", "classify": {"R2": "legacy"}}]}
    assert wg.approvals_ok(good) == []


def test_expiry_detection() -> None:
    fake = {"warn_classify": {"R3": "legacy"},
            "accepted": [{"ts": "2026-01-01", "reason": "b", "classify": {"R3": "legacy"}}]
                        + [{"ts": f"2026-02-{i:02d}", "reason": "b"} for i in range(1, 12)]}
    assert wg.classify(fake, expiry=10).get("R3") == "expired_reassess"
