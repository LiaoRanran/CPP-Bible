"""C2：四工具 --json 输出必须可解析且结构统一（v6.1 schema）。

schema = {tool, version, timestamp, status, summary, findings, infra_errors}
- --json 时 stdout 只输出 JSON，普通日志走 stderr
- exit code 不变（block>0 仍 exit 1）
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PY = sys.executable

# stdout 只含 JSON：取首个以 { 开头的行（可能是多行缩进 JSON）
SCHEMA_KEYS = ("tool", "version", "timestamp", "status", "summary",
               "findings", "infra_errors")


def _run(args):
    return subprocess.run([PY, *args], cwd=REPO, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def _parse_json_only(proc):
    text = proc.stdout
    s, e = text.find("{"), text.rfind("}")
    assert s != -1 and e != -1, f"stdout 无 JSON；stdout={proc.stdout!r} stderr={proc.stderr!r}"
    return json.loads(text[s:e + 1])


def _check_schema(data, tool):
    assert data["tool"] == tool, data.get("tool")
    for k in SCHEMA_KEYS:
        assert k in data, f"缺字段 {k}"
    assert data["status"] in ("pass", "fail")
    assert isinstance(data["findings"], list)
    assert isinstance(data["infra_errors"], list)


def test_gate_engine_json():
    p = _run(["tools/gate_engine.py", "--check", "--json"])
    data = _parse_json_only(p)
    _check_schema(data, "gate_engine")
    assert "rules" in data["summary"]
    assert "block" in data["summary"]


def test_replay_json():
    card = next((REPO / "evidence" / "mem").glob("EV-*.md"))
    p = _run(["tools/atom_evidence_replay.py", "--json", "--card", str(card)])
    data = _parse_json_only(p)
    _check_schema(data, "atom_evidence_replay")
    assert "confirm" in data["summary"]
    assert "refute" in data["summary"]
    assert "infra_error" in data["summary"]


def test_poison_drill_json():
    p = _run(["tools/poison_drill.py", "--json"])
    data = _parse_json_only(p)
    _check_schema(data, "poison_drill")
    assert "passed" in data["summary"]
    assert "total" in data["summary"]


def test_golden_lock_json():
    p = _run(["tools/golden_lock.py", "check", "--json"])
    data = _parse_json_only(p)
    _check_schema(data, "golden_lock")
    # 当前基线已 accept（warn 8→32），check 应无恶化 → status pass
    assert data["status"] == "pass"
