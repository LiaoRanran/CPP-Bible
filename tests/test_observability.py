"""可观测性 L1 回归锁（508 任务4）。

覆盖：
  * 日志三面与必填字段（JSON Lines 可机读）
  * trace_id：env 优先 / 自动生成 / 写回 env（子进程继承的前提）
  * 轮转：超期文件被删、未超期保留
  * **失败不致命**：非法枚举降级为 WARN + 带 invalid 字段，不抛异常
  * log_query 的过滤语义（trace_id / tool / level 阈值 / grep / since）
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import log_query as lq
import observability as obs
import pytest


@pytest.fixture()
def tmp_logs(tmp_path: Path) -> Path:
    d = tmp_path / "logs"
    d.mkdir()
    return d


def _read(day: str, base: Path) -> list[dict]:
    return obs.read_events(day=day, base=base)


# ── 写入与字段 ────────────────────────────────────────────────────────────
def test_log_writes_required_fields(tmp_logs: Path):
    """必填字段齐全：timestamp / level / tool / trace_id / surface / message。"""
    ev = obs.log("INFO", "gate_engine", "check start EV-X", base=tmp_logs)
    assert ev is not None
    for k in ("timestamp", "level", "tool", "trace_id", "surface", "message"):
        assert k in ev, f"缺必填字段 {k}"
    assert ev["level"] == "INFO" and ev["surface"] == "operation"
    assert ev["trace_id"].startswith("batch-")
    rows = _read(ev["timestamp"][:10], tmp_logs)
    assert len(rows) == 1 and rows[0]["message"] == "check start EV-X"


def test_log_three_surfaces_and_optional_duration(tmp_logs: Path):
    """三面（操作/上下文/认知）都可写；duration_ms 为可选字段，非数值时不出现。"""
    obs.log("INFO", "t", "op", surface="operation", base=tmp_logs)
    obs.context_snapshot("t", ["--check"], base=tmp_logs)
    obs.cognition_note("worklog 摘要", base=tmp_logs)
    obs.log("INFO", "t", "no duration", base=tmp_logs)
    rows = _read(_rows_day(tmp_logs), tmp_logs)
    assert [r["surface"] for r in rows] == ["operation", "context", "cognition", "operation"]
    assert "duration_ms" not in rows[-1]


def test_log_duration_recorded(tmp_logs: Path):
    ev = obs.log("INFO", "t", "timed", duration_ms=12.34, base=tmp_logs)
    assert ev is not None and ev["duration_ms"] == pytest.approx(12.3, abs=0.05)


def _rows_day(base: Path) -> str:
    """取沙箱里那一天的日期串（避免跨午夜 flaky）。"""
    assert base.is_dir()
    files = sorted(base.glob("*.jsonl"))
    assert files, "期望已有日志文件"
    return files[-1].stem


# ── trace_id ──────────────────────────────────────────────────────────────
def test_trace_id_env_wins_and_propagates(monkeypatch: pytest.MonkeyPatch):
    """env TRACE_ID 优先；无则自动生成并**写回 env**（子进程继承的前提）。"""
    monkeypatch.setenv("TRACE_ID", "batch-20260914-000000-aaaa")
    monkeypatch.setattr(obs, "_PROC_TRACE_ID", None)
    assert obs.trace_id() == "batch-20260914-000000-aaaa"
    monkeypatch.delenv("TRACE_ID", raising=False)
    monkeypatch.setattr(obs, "_PROC_TRACE_ID", None)
    tid = obs.trace_id()
    assert tid.startswith("batch-") and os.environ.get("TRACE_ID") == tid


def test_trace_id_generated_shape(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("TRACE_ID", raising=False)
    monkeypatch.setattr(obs, "_PROC_TRACE_ID", None)
    tid = obs.new_trace_id()
    parts = tid.split("-")
    assert parts[0] == "batch" and len(parts) == 4 and len(parts[3]) == 4


# ── 失败不致命 ────────────────────────────────────────────────────────────
def test_invalid_enum_degrades_not_raises(tmp_logs: Path):
    """非法 level/surface 不得抛异常：降级 + 记 invalid（错误不被吞掉）。"""
    ev = obs.log("NOT_A_LEVEL", "t", "m", surface="NOT_A_SURFACE", base=tmp_logs)
    assert ev is not None
    assert ev["level"] == "WARN" and ev["surface"] == "operation"
    assert "level=" in ev["invalid"] and "surface=" in ev["invalid"]


def test_log_survives_unwritable_base(tmp_path: Path):
    """IO 失败（路径被文件占位）⇒ 返回 None，**不抛**（观测不得影响主流程）。"""
    blocker = tmp_path / "blocked"
    blocker.write_text("not a dir", encoding="utf-8")
    assert obs.log("INFO", "t", "m", base=blocker) is None


def test_disabled_switch_short_circuits(tmp_logs: Path, monkeypatch: pytest.MonkeyPatch):
    """CPPBIBLE_OBS=0 ⇒ no-op（量化开销/排障用；这也是 508 实测开销的 A/B 手段）。"""
    monkeypatch.setenv("CPPBIBLE_OBS", "0")
    assert obs.log("INFO", "t", "m", base=tmp_logs) is None
    assert not list(tmp_logs.glob("*.jsonl"))


# ── 轮转 ──────────────────────────────────────────────────────────────────
def test_rotate_deletes_only_expired(tmp_logs: Path):
    old, fresh = "2000-01-01", "2999-12-31"
    (tmp_logs / f"{old}.jsonl").write_text("{}\n", encoding="utf-8")
    (tmp_logs / f"{fresh}.jsonl").write_text("{}\n", encoding="utf-8")
    (tmp_logs / "not-a-date.jsonl").write_text("{}\n", encoding="utf-8")
    n = obs.rotate(keep_days=30, base=tmp_logs)
    assert n == 1
    assert not (tmp_logs / f"{old}.jsonl").exists()
    assert (tmp_logs / f"{fresh}.jsonl").exists()
    assert (tmp_logs / "not-a-date.jsonl").exists(), "非日期文件名不得被误删"


# ── log_query 过滤语义 ────────────────────────────────────────────────────
def test_query_filters(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys):
    """trace_id / tool / level（**阈值**语义）/ grep / since 各过滤一次。"""
    logs = tmp_path / "logs"
    logs.mkdir()
    monkeypatch.setattr(lq, "LOGS", logs)
    day = "2026-09-14"
    rows = [
        {"timestamp": f"{day}T10:00:00", "level": "INFO", "tool": "gate_engine",
         "trace_id": "batch-A", "surface": "operation", "message": "check start EV-X"},
        {"timestamp": f"{day}T10:00:01", "level": "ERROR", "tool": "gate_engine",
         "trace_id": "batch-A", "surface": "operation", "message": "check raised EV-Y"},
        {"timestamp": f"{day}T11:00:00", "level": "INFO", "tool": "replay",
         "trace_id": "batch-B", "surface": "operation", "message": "replay card"},
    ]
    (logs / f"{day}.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")

    def run(*args: str) -> list[dict]:
        capsys.readouterr()
        assert lq.main(["--date", day, "--json", *args]) == 0
        return [json.loads(ln) for ln in capsys.readouterr().out.splitlines() if ln.strip()]

    assert len(run()) == 3
    assert [r["trace_id"] for r in run("--trace-id", "batch-A")] == ["batch-A"] * 2
    assert len(run("--tool", "replay")) == 1
    assert len(run("--level", "ERROR")) == 1, "level 为阈值语义（>=ERROR）"
    assert len(run("--level", "INFO")) == 3
    assert len(run("--grep", "EV-Y")) == 1
    assert len(run("--since", "2026-09-14 10:30")) == 1


def test_query_last_and_colour_off_when_not_tty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys):
    """--last N 截断；非 tty 时不着色（管道/CI 里输出干净）。"""
    logs = tmp_path / "logs"
    logs.mkdir()
    monkeypatch.setattr(lq, "LOGS", logs)
    day = "2026-09-14"
    with (logs / f"{day}.jsonl").open("w", encoding="utf-8") as f:
        for i in range(5):
            f.write(json.dumps({"timestamp": f"{day}T10:00:0{i}", "level": "INFO",
                                "tool": "t", "trace_id": "batch-C",
                                "surface": "operation", "message": f"m{i}"}) + "\n")
    capsys.readouterr()
    assert lq.main(["--date", day, "--last", "2"]) == 0
    out = capsys.readouterr().out
    assert out.count("m") >= 2 and "m0" not in out and "m4" in out
    assert "\033[" not in out, "非 tty 不得输出 ANSI 颜色"
