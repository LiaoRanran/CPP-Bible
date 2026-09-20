"""612 B2 回归测试：活性锚人审确认（append-only 确认日志）。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import liveness_review as b2  # noqa: E402


@pytest.fixture
def tmp_log(tmp_path, monkeypatch):
    p = tmp_path / "lrev.jsonl"
    monkeypatch.setattr(b2, "REVIEW_LOG", p)
    return p


def _first_prop() -> str:
    return next(iter(b2.load_props()))


def test_list_outputs_pending(tmp_log, capsys):
    assert b2.main(["list"]) == 0
    assert "pending" in capsys.readouterr().out


def test_approve_updates_stats(tmp_log):
    pid = _first_prop()
    assert b2.main(["approve", pid, "--symbol", "some_sym"]) == 0
    assert b2.stats()["by_status"]["approved"] == 1


def test_mark_inference_updates_stats(tmp_log):
    pid = _first_prop()
    assert b2.main(["mark-inference", pid, "--reason", "无单一工件符号"]) == 0
    assert b2.stats()["by_status"]["inference"] == 1


def test_reject_updates_stats(tmp_log):
    pid = _first_prop()
    assert b2.main(["reject", pid, "--reason", "符号不相关"]) == 0
    assert b2.stats()["by_status"]["rejected"] == 1


def test_check_passes(tmp_log):
    assert b2.main(["--check"]) == 0


def test_append_only_guard(tmp_log):
    pid = _first_prop()
    b2.main(["approve", pid, "--symbol", "a"])
    with pytest.raises(PermissionError):
        b2.modify_record()
    b2.main(["approve", pid, "--symbol", "b"])
    assert len(b2.load_reviews()) == 2
