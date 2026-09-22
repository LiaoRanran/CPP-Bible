"""624 B1 高复杂度带 block 规则接线 · 单元测试（≥5 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import gate_engine as ge  # noqa: E402

HC_IDS = ("EV-SERVES-EXIST-HC", "ATOM-REL-TARGET-HC",
          "ATOM-REL-UNKNOWN-HC", "CARD-PATH-NOT-CANONICAL-HC")


def test_rule_count_67():
    assert len(ge.RULES) == 67
    ids = {r.id for r in ge.RULES}
    for rid in HC_IDS:
        assert rid in ids


def test_hc_rules_are_block_and_automated():
    for rid in HC_IDS:
        r = next(r for r in ge.RULES if r.id == rid)
        assert r.severity == "block"
        assert r.automated is True
        assert r.kind == "fact"


def test_hc_complexity_ordering():
    # 证据卡复杂度全部 < 阈值（EV-SERVES-EXIST-HC 对证据卡不误伤）
    ev_scores = [ge._hc_complexity(p) for p in ge._cards(ge.EVIDENCE, "EV-*.md")]
    assert ev_scores and max(ev_scores) < ge.HC_COMPLEXITY_THRESHOLD
    # 至少存在高复杂度原子卡（≥ 阈值）⇒ 规则可触发
    atom_scores = [ge._hc_complexity(p) for p in ge._cards(ge.ATOMS, "ATOM-*.md")]
    assert max(atom_scores) >= ge.HC_COMPLEXITY_THRESHOLD


def test_hc_reemit_promotes_complex_card():
    complex_rel = None
    for p in ge._cards(ge.ATOMS, "ATOM-*.md"):
        if ge._hc_complexity(p) >= ge.HC_COMPLEXITY_THRESHOLD:
            complex_rel = ge._rel(p)
            break
    assert complex_rel is not None

    def stub():
        return [ge.Finding("ATOM-REL-TARGET", "warn", complex_rel, "msg", "fix")]

    out = ge._hc_reemit(stub, "ATOM-REL-TARGET", "ATOM-REL-TARGET-HC")
    assert len(out) == 1
    assert out[0].severity == "block" and out[0].rule_id == "ATOM-REL-TARGET-HC"


def test_hc_no_false_positive_on_baseline():
    # 存量语的 walk 债卡复杂度均 < 阈值 ⇒ 4 条 HC 规则在基线上 0 命中（无误报）
    assert ge.check_evidence_serves_exist_hc() == []
    assert ge.check_relations_target_exists_hc() == []
    assert ge.check_relations_unknown_type_hc() == []
    assert ge.check_card_path_canonical_hc() == []


def test_hc_reemit_only_matching_base_rule():
    def stub():
        return [ge.Finding("SOMETHING-ELSE", "warn", "atoms/x.md", "m", "f")]

    assert ge._hc_reemit(stub, "ATOM-REL-TARGET", "ATOM-REL-TARGET-HC") == []
