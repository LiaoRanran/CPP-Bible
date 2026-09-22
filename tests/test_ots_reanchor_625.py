"""625 A2 · OTS re-anchor 回归测试（≥4 例）。

验证：新 anchor digest 与当前信任根一致 / pending 诚实标注 / --check 通过 / 报告口径。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import ots_anchor_613 as e1  # noqa: E402


def test_anchor_digest_matches_current_root():
    a = e1.anchor()
    assert "error" not in a
    assert a["digest_matches"] is True
    assert a["digest_now"] == a["parsed"]["file_digest"]


def test_anchor_is_pending_not_confirmed():
    a = e1.anchor()
    assert a["pending"] is True, "未上链必须 pending（不得伪装 confirmed）"


def test_check_passes():
    assert e1.main(["--check"]) == 0


def test_report_states_pending_and_no_proof():
    txt = open(os.path.join(ROOT, "data", "ots_anchor_613.md"), encoding="utf-8").read()
    assert "pending" in txt.lower()
    assert "不得当作时间戳证明" in txt


def test_ots_file_exists_and_nonempty():
    p = e1.OTS_OUT
    assert p.is_file() and p.stat().st_size > 0
