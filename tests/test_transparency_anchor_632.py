"""632 B1 · transparency_anchor_632 单测（≥5 例，全只读/纯标准库）。"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import transparency_anchor_632 as ta  # noqa: E402


def _make_log(tmp_path: Path, text: str) -> Path:
    p = tmp_path / "transparency_log.jsonl"
    p.write_text(text, encoding="utf-8")
    return p


def test_compute_log_hash_matches_sha256(tmp_path):
    p = _make_log(tmp_path, '{"a":1}\n{"b":2}\n')
    assert ta.compute_log_hash(p) == hashlib.sha256(p.read_bytes()).hexdigest()


def test_write_anchor_creates_file_with_hash(tmp_path):
    log = _make_log(tmp_path, '{"x":1}\n')
    vsa = tmp_path / "vsa"
    vsa.mkdir()
    out = ta.write_anchor(log, vsa)
    assert out.exists() and out.name.startswith("anchor_")
    rec = json.loads(out.read_text(encoding="utf-8"))
    assert rec["log_sha256"] == ta.compute_log_hash(log)
    assert rec["entry_count"] == 1
    assert rec["external"]["status"] == "LOCAL_ONLY"


def test_latest_anchor_picks_newest(tmp_path):
    vsa = tmp_path / "vsa"
    vsa.mkdir()
    (vsa / "anchor_20260101.json").write_text("{}", encoding="utf-8")
    (vsa / "anchor_20260924.json").write_text('{"log_sha256":"abc"}', encoding="utf-8")
    latest = ta.latest_anchor(vsa)
    assert latest.name == "anchor_20260924.json"


def test_verify_anchor_true_when_match(tmp_path):
    log = _make_log(tmp_path, '{"y":9}\n')
    vsa = tmp_path / "vsa"
    vsa.mkdir()
    ta.write_anchor(log, vsa)
    assert ta.verify_anchor(log, vsa) is True


def test_verify_anchor_false_when_log_changed(tmp_path):
    log = _make_log(tmp_path, '{"y":9}\n')
    vsa = tmp_path / "vsa"
    vsa.mkdir()
    ta.write_anchor(log, vsa)
    log.write_text('{"y":9}\n{"z":0}\n', encoding="utf-8")  # 日志变动
    assert ta.verify_anchor(log, vsa) is False


def test_main_check_exit_codes(tmp_path):
    log = _make_log(tmp_path, '{"k":1}\n')
    vsa = tmp_path / "vsa"
    vsa.mkdir()
    ta.write_anchor(log, vsa)
    assert ta.main(["--check", "--log", str(log), "--vsa-dir", str(vsa)]) == 0
    log.write_text('{"k":1}\n{"extra":1}\n', encoding="utf-8")
    assert ta.main(["--check", "--log", str(log), "--vsa-dir", str(vsa)]) == 1
