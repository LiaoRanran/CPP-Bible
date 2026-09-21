#!/usr/bin/env python3
"""614 C3 回归测试：trust_root_status_check（信任根状态诚实标注）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import trust_root_status_check as t3  # noqa: E402


def test_scheme_standard() -> None:
    assert t3.scheme_standard("ed25519") is True
    assert t3.scheme_standard("rsa") is True
    assert t3.scheme_standard("hmac-sha256-not-in-toto-standard") is False
    assert t3.scheme_standard(None) is False


def test_ots_pending() -> None:
    assert t3.ots_pending({"attestation_pending": True}) is True
    assert t3.ots_pending({"attestation_pending": False}) is False


def test_overall_verdict() -> None:
    sec = {"merkle_root": {"exists": True}, "tool_integrity": {"exists": True},
           "golden_lock": {"exists": True}, "governance": {"exists": True},
           "ots": {"exists": True, "pending": True},
           "in_toto_link": {"exists": True, "standard": False}}
    assert t3.overall(sec) == "partially_anchored"
    sec["ots"]["pending"] = False
    sec["in_toto_link"]["standard"] = True
    assert t3.overall(sec) == "fully_anchored"
    sec["governance"]["exists"] = False
    assert t3.overall(sec) == "untrusted"


def test_collect_real_repo_consistency() -> None:
    """真实仓：collect 应能读到 merkle 根，且 overall 与当前证据一致。"""
    sec = t3.collect()
    assert sec["merkle_root"]["exists"] is True
    assert sec["tool_integrity"]["exists"] is True
    verdict = t3.overall(sec)
    # 当前为 pending + HMAC ⇒ 不应判 fully_anchored
    assert verdict in ("partially_anchored", "untrusted")
