"""639 D2 单测：ledger 规则归属回填（≥5 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import decision_event_v2_626 as de  # noqa: E402
import ledger_rule_backfill_639 as LB  # noqa: E402


def test_chain_unchanged_after_schema_extension():
    """452 条历史事件自哈希全吻合（空 rule 字段不参与哈希）。"""
    ch = LB.verify_chain_unchanged()
    assert ch["n"] == 452
    assert ch["hash_ok"] == 452
    assert ch["chain_links_ok"]


def test_new_event_with_rule_id_is_hashed():
    """rule_id 非空 ⇒ 纳入哈希（防篡改生效）。"""
    e = de.DecisionEvent(operation="CREATE", result="APPROVE", target_id="X")
    e.finalize(de.GENESIS, 1)
    h0 = e.self_hash
    e.rule_id = "ATOM-REL-TARGET"
    assert e.compute_self_hash() != h0


def test_old_style_event_hash_stable():
    """rule_id 为空 ⇒ 哈希与 626 时代一致（往返兼容）。"""
    e = de.DecisionEvent(operation="CREATE", result="APPROVE", target_id="X")
    e.finalize(de.GENESIS, 1)
    d = e.to_dict()
    d.pop("rule_id"), d.pop("rule_version")
    e2 = de.DecisionEvent.from_dict(d)
    assert e2.compute_self_hash() == e.self_hash


def test_attribution_no_fabrication():
    """undetermined 事件绝不携带编造 rule_id。"""
    r = LB.run()
    for x in r["rows"]:
        if x["status"] == "undetermined":
            assert x["rule_id"] == ""


def test_distribution_sums_to_events():
    r = LB.run()
    assert sum(r["dist"].values()) == r["n_events"] == 452


def test_attribution_exact_match_positive_case():
    """构造含真实规则 id 的事件文本 ⇒ 能归属（机制有效）。"""
    ev = {"event_id": "X", "modification": "由规则 ATOM-REL-TARGET 判定"}
    rules = LB.load_rules()
    assert "ATOM-REL-TARGET" in rules
    res = LB.attribute(ev, rules)
    assert res["status"] == "attributed" and res["rule_id"] == "ATOM-REL-TARGET"
