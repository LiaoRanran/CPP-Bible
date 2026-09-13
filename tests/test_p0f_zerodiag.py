"""470 P0-F 回归锁（452 E10）：零诊断字段位移 + 夹具 pragma 消音。"""
from __future__ import annotations

from pathlib import Path

import pytest

import gate_engine as ge


def _card(tmp: Path, cid: str, *, expected: str = "", command: str,
          fixture: str = "fx.cpp") -> None:
    p = tmp / "evidence" / f"{cid}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        "---\nid: " + cid + "\nserves: []\nhypothesis: h\nkind: run\n"
        f"command: {command}\nfixture: {fixture}\nartifact: a.asm\n"
        "artifact_sha256: " + "0" * 64 + "\nverdict: confirm\nfalsification: f\n"
        f"expected: '{expected}'\n---\n", encoding="utf-8")


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ge, "ROOT", tmp_path)
    monkeypatch.setattr(ge, "EVIDENCE", tmp_path / "evidence")
    (tmp_path / "evidence").mkdir()
    return tmp_path


def test_field_displacement_warned(sb: Path):
    """H16a：措辞在 expected（旧版只扫 falsification）→ 检出。"""
    _card(sb, "EV-Z1", expected="判据：零诊断（编译无警告）", command="g++ -Wall fx.cpp")
    hits = ge.check_evidence_zero_diag_werror()
    assert hits and hits[0].severity == "warn"


def test_pragma_suppression_warned(sb: Path):
    """H16b：夹具 pragma 消音 + 卡声明 -Werror → 检出。"""
    (sb / "fx.cpp").write_text(
        '#pragma GCC diagnostic ignored "-Wunused-variable"\nint main(){return 0;}\n',
        encoding="utf-8")
    _card(sb, "EV-Z2", command="g++ -Wall -Werror -c fx.cpp")
    hits = ge.check_evidence_zero_diag_werror()
    assert hits and "pragma" in hits[0].message


def test_werror_clean_fixture_passes(sb: Path):
    """阴性：-Werror + 夹具无消音 → 不报。"""
    (sb / "fx.cpp").write_text("int main(){return 0;}\n", encoding="utf-8")
    _card(sb, "EV-Z3", command="g++ -Wall -Werror -c fx.cpp")
    assert ge.check_evidence_zero_diag_werror() == []


def test_wording_with_werror_passes(sb: Path):
    """阴性：有措辞但 command 带 -Werror → 合规不报（存量 EV-LANG-001 形态）。"""
    _card(sb, "EV-Z4", expected="零诊断", command="g++ -Wall -Werror -c fx.cpp")
    assert ge.check_evidence_zero_diag_werror() == []
