"""trace_logger 回归锁（498 任务 4）。

锁：①JSONL 行格式与字段齐全 ②seq 当日递增 ③read 过滤（action / fail-only）
④非法枚举与非法 details **报错不静默**。全部走 tmp_path（不写真实 data/traces/）。
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import trace_logger as tl


def test_log_writes_jsonl_with_fields(tmp_path: Path):
    tl.log_event("writer", "compile", "fx.cpp", "pass",
                 {"opt": "-O2"}, base=tmp_path)      # 568 任务4：去未用赋值（调用本身有写日志副作用，保留）
    p = tl.trace_file(base=tmp_path)          # 避免手拼日期（跨日边界更稳）
    assert p.is_file()
    line = p.read_text(encoding="utf-8").strip()
    data = json.loads(line)
    for k in ("timestamp", "seq", "pid", "actor", "action", "target", "result"):
        assert k in data, f"缺字段 {k}"
    assert data["details"] == {"opt": "-O2"}
    assert data["seq"] == 1


def test_seq_increments(tmp_path: Path):
    seqs = [tl.log_event("coolie", "gate_check", "repo", "pass", base=tmp_path)["seq"]
            for _ in range(3)]
    assert seqs == [1, 2, 3], seqs


def test_read_filters(tmp_path: Path):
    tl.log_event("coolie", "gate_check", "repo", "fail", {"rule": "EV-X"}, base=tmp_path)
    tl.log_event("coolie", "replay", "EV-A", "pass", base=tmp_path)
    tl.log_event("redteam", "gate_check", "repo", "fail", base=tmp_path)
    fails = tl.read_events(fail_only=True, base=tmp_path)
    assert len(fails) == 2 and all(e["result"] == "fail" for e in fails)
    gate = tl.read_events(action="gate_check", base=tmp_path)
    assert len(gate) == 2 and all(e["action"] == "gate_check" for e in gate)


def test_invalid_enum_raises(tmp_path: Path):
    with pytest.raises(ValueError):
        tl.log_event("nobody", "gate_check", "repo", "pass", base=tmp_path)
    with pytest.raises(ValueError):
        tl.log_event("coolie", "dance", "repo", "pass", base=tmp_path)
    with pytest.raises(ValueError):
        tl.log_event("coolie", "gate_check", "repo", "maybe", base=tmp_path)


def test_invalid_details_rejected(tmp_path: Path):
    """details 非对象 ⇒ ValueError（不静默写坏数据）。"""
    with pytest.raises(ValueError):
        tl.log_event("coolie", "gate_check", "repo", "pass", ["not", "a", "dict"],
                     base=tmp_path)


def test_cli_bad_details_exit2(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """CLI 路径：非法 JSON details ⇒ exit 2（且不写日志）。"""
    monkeypatch.setattr(tl, "TRACES", tmp_path)
    assert tl.main(["log", "--actor", "coolie", "--action", "gate_check",
                    "--target", "repo", "--result", "pass", "--details", "{坏"]) == 2
    assert tl.main(["log", "--actor", "coolie", "--action", "gate_check",
                    "--target", "repo", "--result", "pass", "--details", "[1,2]"]) == 2
    assert not list(tmp_path.glob("*.jsonl")), "非法输入不得落盘"


def test_read_missing_file_returns_empty(tmp_path: Path):
    assert tl.read_events(base=tmp_path) == []
