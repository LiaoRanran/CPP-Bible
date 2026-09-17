"""470 P0-F → 472 P1-1 回归锁（452 E10）：零诊断字段位移 + 夹具 pragma 消音。

472 P1-1：本规则由 warn **升 block**（"零诊断"措辞缺 -Werror ⇒ 判据不可机器判定 ⇒
不可复算判据不得放行；存量 56 卡 0 命中，升格零误伤）。旧断言 `severity == "warn"`
已同步——否则升格后套件长红，反而掩盖真实回归。
"""
from __future__ import annotations

from pathlib import Path

import gate_engine as ge
import pytest


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


def test_field_displacement_blocked(sb: Path):
    """H16a：措辞在 expected（旧版只扫 falsification）→ 检出且 **block**（472 P1-1）。"""
    _card(sb, "EV-Z1", expected="判据：零诊断（编译无警告）", command="g++ -Wall fx.cpp")
    hits = ge.check_evidence_zero_diag_werror()
    assert hits and hits[0].severity == "block"


def test_pragma_suppression_blocked(sb: Path):
    """H16b：夹具 pragma 消音 + 卡声明 -Werror → 检出且 **block**（472 P1-1）。"""
    (sb / "fx.cpp").write_text(
        '#pragma GCC diagnostic ignored "-Wunused-variable"\nint main(){return 0;}\n',
        encoding="utf-8")
    _card(sb, "EV-Z2", command="g++ -Wall -Werror -c fx.cpp")
    hits = ge.check_evidence_zero_diag_werror()
    assert hits and "pragma" in hits[0].message
    assert hits[0].severity == "block", "消音 pragma 使判据退化 ⇒ 不可复算 ⇒ block"


def test_werror_clean_fixture_passes(sb: Path):
    """阴性：-Werror + 夹具无消音 → 不报。"""
    (sb / "fx.cpp").write_text("int main(){return 0;}\n", encoding="utf-8")
    _card(sb, "EV-Z3", command="g++ -Wall -Werror -c fx.cpp")
    assert ge.check_evidence_zero_diag_werror() == []


def test_wording_with_werror_passes(sb: Path):
    """阴性：有措辞但 command 带 -Werror → 合规不报（存量 EV-LANG-001 形态）。"""
    _card(sb, "EV-Z4", expected="零诊断", command="g++ -Wall -Werror -c fx.cpp")
    assert ge.check_evidence_zero_diag_werror() == []
