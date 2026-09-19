"""609 A2 · 人审质量控制回归锁（automation bias 检测）。

锁六件事（任务书 6 例 + 2 例自加）：
  1. inject-trap 合法 edge + expected ⇒ 台账写入且字段齐全；
  2. review_seconds=3s（<5s）⇒ `short_time`；
  3. reason_len=10（<20）⇒ `short_reason`；
  4. 全 approve + 短理由 ⇒ agree_rate=1.0 ⇒ `rubber_stamp`；
  5. 陷阱题 expected=reject 却判 approve ⇒ `trap_caught=false` + `trap_failed`；
  6. report 含陷阱题捕获率/平均耗时/agree_rate/风险等级；
  +. 缺失 review_seconds ⇒ **不伪造** 0.0：`measured=false` 且不判 short_time；
  +. 默认台账缺件时 --check exit 0（不celebrate数据缺失）。

所有用例走 tmp 路径，**不写真实 data/** 下的人审/质量/陷阱题台账。
"""
from __future__ import annotations

import json
from pathlib import Path

import human_review_cli as hrc
import human_review_quality as hrq
import pytest

EDGE = sorted(hrc.load_edge_ids())[0]
EDGE2 = sorted(hrc.load_edge_ids())[1]
LONG_REASON = "人审确认：攻击关系成立，反驳证据可核据==>" + "x" * 30   # ≥20 字符
SHORT_REASON = "理由太短了"          # 6 字符 < 20


def _write_ann(p: Path, rows: list[dict]) -> Path:
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                 encoding="utf-8", newline="\n")
    return p


def _rec(edge_id: str, kind: str = "approve", *, reason: str = LONG_REASON,
         **extra) -> dict:
    return {"edge_id": edge_id, "kind": kind, "reviewer": "human",
            "timestamp": "2026-09-19T10:00:00+08:00", "reason": reason, **extra}


@pytest.fixture
def paths(tmp_path: Path):
    class P:
        ann = tmp_path / "ann.jsonl"
        traps = tmp_path / "traps.json"
        quality = tmp_path / "quality.jsonl"
    return P()


def _detect(paths) -> list[dict]:
    assert hrq.main(["--annotations", str(paths.ann), "--traps", str(paths.traps),
                     "--quality", str(paths.quality), "detect"]) == 0
    return [json.loads(ln) for ln in paths.quality.read_text(encoding="utf-8").splitlines()
            if ln.strip()]


# ── 1. 陷阱题注入 ─────────────────────────────────────────────────────────────
def test_inject_trap_writes_register(paths, capsys):
    assert hrq.main(["--traps", str(paths.traps), "inject-trap", EDGE,
                     "--expected", "reject"]) == 0
    out = capsys.readouterr().out
    assert f"TRAP INJECTED: {hrq.TRAP_PREFIX}{EDGE}" in out
    t = hrq.load_traps(paths.traps)[EDGE]
    assert t["expected"] == "reject" and t["original_edge_id"] == EDGE
    assert hrq.check(quality_path=paths.quality, traps_path=paths.traps) == []


def test_inject_trap_unknown_edge_exit1(paths):
    assert hrq.main(["--traps", str(paths.traps), "inject-trap",
                     "ae-NOPE::prop-1->MIS-NOPE-000", "--expected", "reject"]) == 1
    assert not paths.traps.exists()


# ── 2-4. 三类复核标记 ─────────────────────────────────────────────────────────
def test_short_time_flag(paths):
    _write_ann(paths.ann, [_rec(EDGE, review_seconds=3.0)])
    rows = _detect(paths)
    assert rows[0]["review_flag"] == "short_time"
    assert rows[0]["review_seconds"] == 3.0


def test_short_reason_flag(paths):
    # 用 reject（agree_rate=0.0）隔离出 short_reason：单条 approve 会同时构成
    # agree_rate==1.0 ⇒ 优先级更高的 rubber_stamp（见 test_rubber_stamp_flag）。
    _write_ann(paths.ann, [_rec(EDGE, "reject", reason=SHORT_REASON, review_seconds=60.0)])
    rows = _detect(paths)
    assert rows[0]["review_flag"] == "short_reason"
    assert rows[0]["reason_len"] == len(SHORT_REASON)


def test_rubber_stamp_flag(paths):
    _write_ann(paths.ann, [_rec(EDGE, reason=SHORT_REASON, review_seconds=60.0),
                           _rec(EDGE2, reason=SHORT_REASON, review_seconds=60.0)])
    rows = _detect(paths)
    assert all(r["agree_rate"] == 1.0 for r in rows)
    assert rows[-1]["review_flag"] == "rubber_stamp"


# ── 5. 陷阱题未捕获 ───────────────────────────────────────────────────────────
def test_trap_failed_flag(paths):
    assert hrq.main(["--traps", str(paths.traps), "inject-trap", EDGE,
                     "--expected", "reject"]) == 0
    _write_ann(paths.ann, [_rec(EDGE, "approve", review_seconds=60.0)])
    rows = _detect(paths)
    assert rows[0]["is_trap"] is True and rows[0]["trap_expected"] == "reject"
    assert rows[0]["trap_caught"] is False
    assert rows[0]["review_flag"] == "trap_failed"


# ── 6. 报告 ───────────────────────────────────────────────────────────────────
def test_report_contains_key_metrics(paths, capsys):
    assert hrq.main(["--traps", str(paths.traps), "inject-trap", EDGE,
                     "--expected", "approve"]) == 0
    _write_ann(paths.ann, [_rec(EDGE, "approve", review_seconds=42.0),
                           _rec(EDGE2, "reject", review_seconds=18.0)])
    assert hrq.main(["--annotations", str(paths.ann), "--traps", str(paths.traps),
                     "--quality", str(paths.quality), "report"]) == 0
    out = capsys.readouterr().out
    for key in ("捕获率", "平均耗时", "平均理由长度", "agree_rate", "automation bias 风险等级"):
        assert key in out, f"报告缺 {key}"
    rows = [json.loads(ln) for ln in paths.quality.read_text(encoding="utf-8").splitlines()
            if ln.strip()]
    s = hrq.summarize(rows)
    assert s["traps_total"] == 1 and s["traps_caught"] == 1 and s["trap_capture_rate"] == 1.0
    assert s["avg_review_seconds"] == 30.0
    # EDGE 是陷阱题 ⇒ 不入 agree_rate 分母；非陷阱题只有 EDGE2(reject) ⇒ 0/1 = 0.0
    assert s["agree_rate"] == 0.0
    assert s["bias_risk"] == "low"


# ── +2 诚实口径 ───────────────────────────────────────────────────────────────
def test_missing_review_seconds_is_not_fabricated(paths):
    """A1 schema 没有 review_seconds ⇒ 不可回溯测量 ⇒ 不得伪造成 0.0/short_time。"""
    _write_ann(paths.ann, [_rec(EDGE)])
    rows = _detect(paths)
    assert rows[0]["review_seconds"] is None
    assert rows[0]["review_seconds_measured"] is False
    assert rows[0]["review_flag"] == "none"
    s = hrq.summarize(rows)
    assert s["avg_review_seconds"] is None
    assert s["review_seconds_unmeasurable"] == 1


def test_default_state_check_is_green(tmp_path: Path):
    assert hrq.main(["--quality", str(tmp_path / "q.jsonl"),
                     "--traps", str(tmp_path / "t.json"), "--check"]) == 0
    _write_ann(tmp_path / "a.jsonl", [])
    rows = hrq.detect_records([], {})
    assert hrq.summarize(rows)["insufficient_evidence"] is True
    assert hrq.summarize(rows)["bias_risk"] == "insufficient evidence"
