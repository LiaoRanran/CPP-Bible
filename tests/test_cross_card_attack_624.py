"""624 A1 跨卡一致性攻击 · 单元测试（≥8 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import cross_card_attack_624 as cc  # noqa: E402


def _muts():
    return cc.generate_mutations(cc.load_inventory(), per_strategy=15)


def test_generate_60():
    muts = _muts()
    assert len(muts) == 60
    by = {}
    for m in muts:
        by.setdefault(m["strategy"], []).append(m)
    assert {k: len(v) for k, v in by.items()} == {"X1": 15, "X2": 15, "X3": 15, "X4": 15}


def test_x1_dangling_multicard():
    xs = [m for m in _muts() if m["strategy"] == "X1"]
    assert xs and all(len(m["edits"]) >= 1 for m in xs)
    assert any(len(m["edits"]) >= 2 for m in xs)


def test_x2_cycle_two_cards():
    xs = [m for m in _muts() if m["strategy"] == "X2"]
    assert xs
    for m in xs:
        assert len(m["edits"]) == 2
        # 双向互指
        targets = {e["target"] for e in m["edits"]}
        assert len(targets) == 2


def test_x3_contradiction():
    xs = [m for m in _muts() if m["strategy"] == "X3"]
    assert xs
    for m in xs:
        assert {e["rtype"] for e in m["edits"]} == {"supports", "contradicts"}


def test_x4_orphan_reference():
    xs = [m for m in _muts() if m["strategy"] == "X4"]
    assert xs
    assert any(any(e["op"] == "SET_SERVES" for e in m["edits"]) for m in xs)
    assert any(any(e["op"] == "SET_MIS" for e in m["edits"]) for m in xs)


def test_complexity_above_60():
    assert all(m["complexity"] > 60 for m in _muts())


def test_plan_edit_primitives():
    text = "---\nid: ATOM-X\nrelations: []\nmisconceptions: [MIS-A]\n---\nbody\n"
    rel = cc.plan_edit_624({"op": "APPEND_REL", "rtype": "supports", "target": "ATOM-Y"}, text)
    assert rel is not None and "target: ATOM-Y" in rel[0]
    mis = cc.plan_edit_624({"op": "SET_MIS", "value": "MIS-NOPE-999"}, text)
    assert mis is not None and "MIS-NOPE-999" in mis[0]
    serv = cc.plan_edit_624({"op": "SET_SERVES", "value": "ATOM-NOPE-999"},
                            "---\nid: EV-X\nserves: [ATOM-A]\n---\nx\n")
    assert serv is not None and "ATOM-NOPE-999" in serv[0]
    assert cc.plan_edit_624({"op": "SET_ID", "value": ""}, text) is None


def test_whitelist_and_multicard_roundtrip():
    assert cc.base.is_allowed("atoms/conc/ATOM-CONC-FENCE-001.md")
    assert not cc.base.is_allowed("tools/x.py")
    inv = cc.load_inventory()
    target = inv["atoms"][0]["card"]
    sb = cc.CrossCardSandbox()
    sha_before = cc.base._sha256_bytes(open(sb._abs(target), "rb").read())
    applied = sb.apply_multi([{"card": target, "op": "APPEND_REL",
                               "rtype": "supports", "target": "ATOM-SELFTEST-999"}])
    assert applied["applied"] and applied["n_edits"] == 1
    rst = sb.restore_multi(applied["backups"])
    sha_after = cc.base._sha256_bytes(open(sb._abs(target), "rb").read())
    assert rst["restored"] and sha_before == sha_after


def test_selftest_passes():
    assert cc.selftest() == 0
