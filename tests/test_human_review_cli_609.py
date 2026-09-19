"""609 A1 · 人审 CLI 回归锁（append-only + fail-closed）。

只通过**命令行入口** `main()` 驱动，锁的是人实际会看到的退出码与副作用：

  1. approve 合法 ⇒ 追加 1 行、--check exit 0；
  2. reject 合法 ⇒ 追加 1 行、--check exit 0；
  3. approve 未知 edge_id ⇒ exit 1 且**一行都不写**（fail-closed）；
  4. approve reason<20 ⇒ exit 2 且**一行都不写**（防 rubber-stamp）；
  5. modify --confidence high ⇒ confidence 字段落盘正确；
  6. modify --confidence 非法 ⇒ exit 3 且**一行都不写**；
  7. 同一 edge_id 重复 approve ⇒ **两行**（append-only，不覆盖历史）；
  8. --check 发现 reviewer=machine ⇒ exit 1 且打印行号+原因。

⚠️ 全部用例把通道重定向到 tmp（**绝不写真实 596 人审通道**）。
"""
from __future__ import annotations

import json
from pathlib import Path

import human_review_cli as hrc
import pytest

EDGE = sorted(hrc.load_edge_ids())[0]
REASON = "人审确认：该攻击边的目标命题确实被这条误解反驳，证据充分且可核"   # ≥ 20 字符


@pytest.fixture
def ann(tmp_path: Path) -> Path:
    p = tmp_path / "ann.jsonl"
    p.write_text("", encoding="utf-8", newline="\n")
    return p


def _rows(p: Path) -> list[dict]:
    return [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]


def test_approve_appends_one_record_and_check_ok(ann: Path, capsys):
    assert hrc.main(["--annotations", str(ann), "approve", EDGE,
                     "--reason", REASON]) == 0
    rows = _rows(ann)
    assert len(rows) == 1
    assert rows[0]["edge_id"] == EDGE and rows[0]["kind"] == "approve"
    assert rows[0]["reviewer"] == "human"
    assert len(rows[0]["reason"]) >= hrc.MIN_REASON
    assert "APPROVED: " + EDGE in capsys.readouterr().out
    assert hrc.main(["--annotations", str(ann), "--check"]) == 0


def test_reject_appends_one_record_and_check_ok(ann: Path, capsys):
    assert hrc.main(["--annotations", str(ann), "reject", EDGE,
                     "--reason", REASON]) == 0
    rows = _rows(ann)
    assert len(rows) == 1 and rows[0]["kind"] == "reject"
    assert "REJECTED: " + EDGE in capsys.readouterr().out
    assert hrc.main(["--annotations", str(ann), "--check"]) == 0


def test_approve_unknown_edge_fails_closed(ann: Path, capsys):
    bad = "ae-NO-SUCH-NODE::prop-1->MIS-XXX-999"
    assert hrc.main(["--annotations", str(ann), "approve", bad,
                     "--reason", REASON]) == 1
    assert _rows(ann) == [], "fail-closed 破防：未知 edge_id 竟然写了盘"
    assert "拒写" in capsys.readouterr().err


def test_short_reason_fails_closed(ann: Path, capsys):
    assert hrc.main(["--annotations", str(ann), "approve", EDGE,
                     "--reason", "太短"]) == 2
    assert _rows(ann) == [], "fail-closed 破防：reason<20 竟然写了盘"
    assert "rubber-stamp" in capsys.readouterr().err


def test_modify_high_confidence_record(ann: Path, capsys):
    assert hrc.main(["--annotations", str(ann), "modify", EDGE,
                     "--confidence", "high", "--reason", REASON]) == 0
    rows = _rows(ann)
    assert rows[0]["kind"] == "modify" and rows[0]["confidence"] == "high"
    assert f"MODIFIED: {EDGE} -> high" in capsys.readouterr().out
    assert hrc.main(["--annotations", str(ann), "--check"]) == 0


def test_modify_illegal_confidence_exit3(ann: Path):
    assert hrc.main(["--annotations", str(ann), "modify", EDGE,
                     "--confidence", "ultra", "--reason", REASON]) == 3
    assert _rows(ann) == [], "fail-closed 破防：非法 confidence 竟然写了盘"


def test_append_only_keeps_history(ann: Path):
    assert hrc.main(["--annotations", str(ann), "approve", EDGE,
                     "--reason", REASON]) == 0
    assert hrc.main(["--annotations", str(ann), "approve", EDGE,
                     "--reason", REASON + "（第二轮复核同样成立）"]) == 0
    rows = _rows(ann)
    assert len(rows) == 2, "append-only 破防：历史行被覆盖"
    assert {r["kind"] for r in rows} == {"approve"}
    assert len(hrc.latest_by_edge(rows)) == 1 and hrc.status_of(EDGE, hrc.latest_by_edge(rows)) == "approved"


def test_check_catches_machine_reviewer(ann: Path, capsys):
    rec = hrc.build_record(EDGE, "approve", REASON)
    rec["reviewer"] = "machine"                       # 机器冒充人审
    ann.write_text(json.dumps(rec, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    rc = hrc.main(["--annotations", str(ann), "--check"])
    err = capsys.readouterr().err
    assert rc == 1, "机器冒名竟然通过了 --check"
    assert "第 1 行" in err and "reviewer" in err


def test_default_channel_is_empty_and_checks_green():
    """真实 596 通道必须存在且为空（608 的教训：断言"不存在"会被误删偶然骗过）。"""
    p = hrc.DEFAULT_ANN
    if p.is_file():
        assert hrc.load_annotations(p) == [], "真实人审通道被写入了内容（人审权不容机器代签）"
        assert p.stat().st_size == 0
    assert hrc.check(p) == []
