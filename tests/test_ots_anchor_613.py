#!/usr/bin/env python3
"""E1 回归测试：ots_anchor_613（信任根 OTS 凭据 · 不 submit，pending 必须诚实）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import opentimestamps_anchor as ots  # noqa: E402
import ots_anchor_613 as e1  # noqa: E402


def test_target_is_the_trust_root():
    assert e1.TARGET.is_file()
    assert e1.TARGET.name == "merkle_roots.json"


def test_anchor_produces_pending_ots(tmp_path, monkeypatch):
    tgt = tmp_path / "roots.json"
    tgt.write_text('{"root": "abc"}', encoding="utf-8")
    monkeypatch.setattr(e1, "TARGET", tgt)
    monkeypatch.setattr(e1, "OTS_OUT", tgt.with_suffix(tgt.suffix + ".ots"))
    a = e1.anchor()
    assert a["digest_matches"] is True
    assert a["pending"] is True, "不 submit ⇒ attestation 必须 pending（609 铁律）"
    assert a["parsed"]["ops"], "OTS 操作序列不得为空"


def test_report_marks_not_yet_anchored(tmp_path, monkeypatch):
    tgt = tmp_path / "roots.json"
    tgt.write_text('{"root": "abc"}', encoding="utf-8")
    monkeypatch.setattr(e1, "TARGET", tgt)
    monkeypatch.setattr(e1, "OTS_OUT", tgt.with_suffix(tgt.suffix + ".ots"))
    page = e1.render(e1.anchor())
    assert "pending" in page and "不得当作时间戳证明" in page


def test_digest_mismatch_detected_by_check(tmp_path, monkeypatch):
    """anchor() 每次都会重新 stamp（故 digest 恒一致）；不一致**只在 --check 路径**检出。"""
    tgt = tmp_path / "roots.json"
    tgt.write_text('{"root": "abc"}', encoding="utf-8")
    monkeypatch.setattr(e1, "TARGET", tgt)
    monkeypatch.setattr(e1, "OTS_OUT", tgt.with_suffix(tgt.suffix + ".ots"))
    e1.anchor()                                            # 锚定旧内容
    assert e1.main(["--check"]) == 0
    tgt.write_text('{"root": "xyz"}', encoding="utf-8")    # 再改内容
    assert e1.main(["--check"]) == 1, "信任根变更后 --check 必须变红"


def test_missing_target_reports_error(tmp_path, monkeypatch):
    monkeypatch.setattr(e1, "TARGET", tmp_path / "nope.json")
    assert "error" in e1.anchor()


def test_ots_roundtrip_parse():
    p = tmp_file = None  # noqa: F841
    raw = ots.build_ots(b"\x00" * 32)
    parsed = ots.parse_ots(raw)
    assert parsed["file_digest"] == "00" * 32


def test_check_passes():
    assert e1.main(["--check"]) == 0
