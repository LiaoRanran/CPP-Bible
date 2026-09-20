"""612 A2 回归测试：桥接边人审执行（append-only 决策日志）。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import bridge_edge_review as a2  # noqa: E402


@pytest.fixture
def tmp_log(tmp_path, monkeypatch):
    p = tmp_path / "rev.jsonl"
    monkeypatch.setattr(a2, "REVIEW_LOG", p)
    return p


def test_list_all_pending(tmp_log, capsys):
    assert a2.main(["list"]) == 0
    out = capsys.readouterr().out
    assert out.count("pending") == 98


def test_approve_updates_stats(tmp_log):
    cid = a2.load_candidate_ids()[0]
    assert a2.main(["approve", cid, "--confidence", "high"]) == 0
    st = a2.stats()
    assert st["approved"] == 1
    assert st["pending"] == 97


def test_reject_updates_stats(tmp_log):
    cid = a2.load_candidate_ids()[1]
    assert a2.main(["reject", cid, "--reason", "论证关系弱"]) == 0
    assert a2.stats()["rejected"] == 1


def test_batch_executes(tmp_log, tmp_path):
    ids = a2.load_candidate_ids()
    f = tmp_path / "ops.txt"
    f.write_text(f"approve {ids[2]} medium\nreject {ids[3]} 伪桥接\n", encoding="utf-8")
    assert a2.main(["batch", "--from-file", str(f)]) == 0
    st = a2.stats()
    assert st["approved"] == 1 and st["rejected"] == 1


def test_check_passes(tmp_log):
    assert a2.main(["--check"]) == 0


def test_append_only_guard(tmp_log):
    ids = a2.load_candidate_ids()
    a2.main(["approve", ids[0]])
    with pytest.raises(PermissionError):
        a2.modify_record()
    a2.main(["approve", ids[0]])          # 再追加一条（不是覆盖）
    assert len(a2.load_reviews()) == 2


def test_unknown_candidate_rejected(tmp_log):
    with pytest.raises(SystemExit):
        a2.main(["approve", "bridge-NOPE->NOPE"])


def test_real_log_empty_or_valid():
    # 真仓决策日志若存在，则每条记录 action 必须合法（不把「零人审」当常量）
    if a2.REVIEW_LOG.is_file():
        for r in a2.load_reviews():
            assert r["action"] in ("approve", "reject", "modify")
