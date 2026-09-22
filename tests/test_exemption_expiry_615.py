#!/usr/bin/env python3
"""615 C2 回归测试：exemption_expiry（legacy 豁免到期制）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import exemption_expiry as ex  # noqa: E402


def test_expiry_equals_created_plus_10() -> None:
    rows = ex.assign()
    assert len(rows) == len(ex.load_exemptions())     # 624 D3：动态口径（legacy 27 + 624 新增）
    for r in rows:
        assert r["expiry_batch"] == r["created_batch"] + ex.EXPIRY_BATCHES


def test_due_soon_and_expired_detection() -> None:
    # 构造：7 批(09-11) 创建批次=7 ⇒ 到期 17（只在 legacy 豁免上验证状态机）
    due_tl = ["2026-09-11"] * 7 + ["2026-09-20"] * 8     # current=15 ⇒ 17-15=2 ≤3 ⇒ due_soon
    rows = [r for r in ex.assign(due_tl) if r["redteam_seen"] == "legacy"]
    assert rows and all(r["status"] == "due_soon" for r in rows)
    exp_tl = ["2026-09-11"] * 7 + ["2026-09-20"] * 10    # current=17 ⇒ 17<=17 ⇒ expired
    rows2 = [r for r in ex.assign(exp_tl) if r["redteam_seen"] == "legacy"]
    assert rows2 and all(r["status"] == "expired" for r in rows2)


def test_check_consistency() -> None:
    assert ex.check() == []
