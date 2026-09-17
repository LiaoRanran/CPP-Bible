"""470 P0-E 回归锁（452 E06）：环境量进断言键 = block；仅留痕 = advice；弱词不误伤。"""
from __future__ import annotations

from pathlib import Path

import gate_engine as ge
import pytest


def _card(tmp: Path, cid: str, keys: str, out_text: str) -> Path:
    (tmp / "e.out").write_text(out_text, encoding="utf-8")
    p = tmp / "evidence" / f"{cid}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        "---\nid: " + cid + "\nserves: []\nhypothesis: h\nkind: run\n"
        "command: g++ fx.cpp -o a.exe\nfixture: fx.cpp\nartifact: a.asm\n"
        "artifact_sha256: " + "0" * 64 + "\nverdict: confirm\nfalsification: f\n"
        f"actual:\n  run_match_file: e.out\n  run_match_keys: {keys}\n---\n",
        encoding="utf-8")
    return p


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ge, "ROOT", tmp_path)
    monkeypatch.setattr(ge, "EVIDENCE", tmp_path / "evidence")
    (tmp_path / "evidence").mkdir()
    return tmp_path


def test_env_key_in_assert_blocked(sb: Path):
    """E06 正例：nproc/date/user 声明进 keys → block（CI 异核必红）。"""
    _card(sb, "EV-E1", "[nproc, result]", "nproc=32\nresult=7\n")
    hits = [f for f in ge.check_env_dependent_key() if f.severity == "block"]
    assert hits and "nproc" in hits[0].message


def test_env_key_out_only_advice(sb: Path):
    """留痕面：.out 含 nproc 但未声明 → advice 不 block（存量 EV-CONC-003 形态）。"""
    _card(sb, "EV-E2", "[result]", "nproc=32\nresult=7\n")
    hits = ge.check_env_dependent_key()
    assert hits and hits[0].severity == "advice"
    assert not any(f.severity == "block" for f in hits)


def test_weak_time_words_not_flagged(sb: Path):
    """弱词不误伤：timestamp/elapsed/random 不作环境量（bench 卡正常记录会命中）。"""
    _card(sb, "EV-E3", "[timestamp, elapsed_ns, randomized_layout]",
          "timestamp=12345\nelapsed_ns=99\nrandomized_layout=1\n")
    assert ge.check_env_dependent_key() == []


def test_exact_env_key_helper():
    assert ge._is_env_key("nproc")
    assert ge._is_env_key("hardware_concurrency_used")
    assert ge._is_env_key("USERNAME")
    assert ge._is_env_key("processor_count")
    assert not ge._is_env_key("timestamp")
    assert not ge._is_env_key("result")
