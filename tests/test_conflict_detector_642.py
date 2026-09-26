"""642 A1 · conflict_detector_642 单测（灰度上岗：flag 只加标记不改判决）。编号 A1-1..A1-8。"""
from __future__ import annotations

import conflict_detector_636 as shadow
import conflict_detector_642 as C
import queyi_core_v10_641 as core

_RULES = [{"id": "A", "severity": "block", "scope": "atom"},
          {"id": "B", "severity": "warn", "scope": "atom"}]
_GOOD17 = {"EV-T-%03d" % i for i in range(17)}
_GOOD18 = {"EV-T-%03d" % i for i in range(18)}
_CONFLICT_TEXT = ("status: verified\nevidence: ["
                  + ", ".join("EV-T-%03d" % i for i in range(20)) + "]\n")


def _det(text: str, idx) -> dict:
    return shadow.detect(text, _RULES, ev_index=idx)


# A1-1：flag 不改判决（state / decision_id 逐字保留）
def test_flag_does_not_change_verdict():
    dec = core.Decision.make("a1", "pass", reasons=["r"], rule_ids=["R1"])
    flagged = C.flag_decision(dec, _det(_CONFLICT_TEXT, _GOOD17))
    assert flagged["state"] == dec.state
    assert flagged["decision_id"] == dec.decision_id
    assert C.verdict_unchanged(dec.to_dict(), flagged) is True


# A1-2：已知冲突卡必标记（20 引用 / 3 悬挂 ⇒ ee=1，C=0.3 恰在阈值上）
def test_known_conflict_card_is_marked():
    d = _det(_CONFLICT_TEXT, _GOOD17)
    assert (d["C"], d["exceeds_theta"]) == (0.3, True)
    assert "EE" in d["types"]


# A1-3：已知无冲突卡不标记（引用全存在 ⇒ agreement=1 ⇒ C=0）
def test_known_clean_card_is_not_marked():
    text = ("status: verified\nevidence: ["
            + ", ".join("EV-T-%03d" % i for i in range(7)) + "]\n")
    d = _det(text, _GOOD17)
    assert d["C"] == 0.0 and d["exceeds_theta"] is False
    assert d["types"] == ["RR"] or d["types"] == []


# A1-4：阈值边界（C == θ 记标记；C < θ 不标记）
def test_theta_boundary():
    at = _det(_CONFLICT_TEXT, _GOOD17)
    below = _det(_CONFLICT_TEXT, _GOOD18)
    assert at["C"] == shadow.THETA and at["exceeds_theta"] is True
    assert below["C"] < shadow.THETA and below["exceeds_theta"] is False


# A1-5：flag 幂等（重复 flag 不叠加冲突字段，字段集恒定）
def test_flag_is_idempotent():
    dec = core.Decision.make("a1", "pass")
    det = _det(_CONFLICT_TEXT, _GOOD17)
    once = C.flag_decision(dec, det)
    twice = C.flag_decision(dec, det)
    assert set(once) == set(twice)
    assert once["conflict_types"] == twice["conflict_types"]


# A1-6：block 模式明确未实现（显式拒绝，exit 2；不静默降级为 flag）
def test_block_mode_is_refused():
    assert C.BLOCK_IMPLEMENTED is False
    assert C.main(["--mode", "block"]) == 2


# A1-7：全量实跑 ⇒ 零判决被改变，且标记数与 636 影子超阈数一致（单一真源）
def test_run_flag_matches_shadow_and_changes_nothing():
    s = C.run_flag()
    sh = shadow.run_shadow()
    assert s["n_cards"] == sh["n_cards"]
    assert s["n_marked"] == sh["over_theta"]
    assert s["n_verdict_changed"] == 0
    assert all(r["unchanged"] for r in s["rows"])


# A1-8：--check 自检通过
def test_selftest():
    assert C.selftest() == 0
