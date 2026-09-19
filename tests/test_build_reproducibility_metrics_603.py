"""603 任务2.3：编译可复现性度量 collect_build_reproducibility 测试。

快路径：monkeypatch `check_build_reproducibility` 注入受控结果，验证聚合口径与字段齐全；
不真编译（任务1 已覆盖引擎本身）。
"""
from __future__ import annotations

import sys

import pytest

sys.path.insert(0, "tools")

import atom_evidence_replay as replay
import metrics_collector as mc


def test_collect_fields_and_aggregation(monkeypatch: pytest.MonkeyPatch) -> None:  # noqa: F821
    cards = [
        {"card": "EV-A", "command": "g++ a.cpp -o a.asm", "artifact": "a.asm"},
        {"card": "EV-B", "command": "g++ b.cpp -o b.asm", "artifact": "b.asm"},
        {"card": "EV-C", "command": "g++ c.cpp -o c.asm", "artifact": "c.asm"},
        {"card": "EV-D", "command": "echo no-compile", "artifact": "d.asm"},  # 提不出编译行 ⇒ unavailable
    ]
    seq = [
        replay.BuildReproResult(True, "h", "h", None, None, None, 0, "", 1),    # reproducible
        replay.BuildReproResult(False, "", "", None, None, None, 1, "err", 2),  # compile_failed
        replay.BuildReproResult(False, "x", "y", None, None, "diff", 0, "", 3),  # not_reproducible
    ]
    calls = {"i": 0}

    def _fake(*args, **kwargs):
        r = seq[calls["i"]]
        calls["i"] += 1
        return r

    monkeypatch.setattr(replay, "check_build_reproducibility", _fake)
    res = mc.collect_build_reproducibility(sample=10, cards=cards)
    d = res.to_dict()
    for k in ("total", "sampled", "reproducible", "compile_failed",
              "not_reproducible", "unavailable", "notes", "sampled_cards"):
        assert k in d, f"缺字段 {k}"
    # EV-D 提不出编译行 ⇒ 不计入 total；其余 3 张分属三类
    assert res.total == 3
    assert res.reproducible == 1
    assert res.compile_failed == 1
    assert res.not_reproducible == 1
    assert res.unavailable == 1
    assert set(res.sampled_cards) == {"EV-A", "EV-B", "EV-C"}
    assert d["notes"]["sample_requested"] == 10
    assert d["notes"]["sample_actual"] == 3


def test_collect_empty_cards(monkeypatch: pytest.MonkeyPatch) -> None:  # noqa: F821
    monkeypatch.setattr(replay, "check_build_reproducibility",
                        lambda *a, **k: replay.BuildReproResult(False, "", "", None, None, None, 1, "", 0))
    res = mc.collect_build_reproducibility(cards=[])
    assert res.total == 0
    assert res.reproducible == res.compile_failed == res.not_reproducible == 0
    assert res.unavailable == 0
