"""612 C1 回归测试：oracle 验证执行工具（stub 三门禁，避免真跑 300s 的 replay）。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import oracle_verifier as c1  # noqa: E402

_CANNED = {
    "gate": {"name": "gate", "status": "pass", "exit": 0, "seconds": 0.1,
             "stdout": "  [WARN  ] OBSERVATION-LIVENESS  evidence/conc/EV-CONC-001.md\n",
             "stderr": ""},
    "poison": {"name": "poison", "status": "pass", "exit": 0, "seconds": 0.1,
               "stdout": "[poison] 诚实覆盖率: 60 规则 / 63\n", "stderr": ""},
    "replay": {"name": "replay", "status": "pass", "exit": 0, "seconds": 0.1,
               "stdout": "[replay] confirm=56 refute=0 infra_error=0\n", "stderr": ""},
}


@pytest.fixture
def stub(monkeypatch):
    monkeypatch.setattr(c1, "_run_check", lambda name, timeout: _CANNED[name])
    return monkeypatch


def test_single_card_success(stub):
    doc = c1.verify(card_id="EV-CONC-001")
    assert len(doc["cards"]) == 1
    assert doc["cards"][0]["id"] == "EV-CONC-001"
    assert doc["cards"][0]["gate_warn"] == 1        # 归因到该卡的 warn
    assert doc["cards"][0]["status"] == "pass"


def test_nonexistent_card_errors(stub):
    with pytest.raises(SystemExit):
        c1.verify(card_id="NO-SUCH-CARD")


def test_report_format(stub):
    doc = c1.verify(top=5)
    text = c1.render(doc)
    assert "三门禁结果" in text and "逐卡清单" in text
    assert len(doc["cards"]) == 5


def test_key_numbers(stub):
    doc = c1.verify(card_id="EV-CONC-001")
    assert doc["key_numbers"]["poison_total"] == 63
    assert doc["key_numbers"]["replay_confirm"] == 56


def test_check_passes(stub):
    assert c1.main(["--check"]) == 0
