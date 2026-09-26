"""647 B5 · MDL 准入真上岗回归锁（编号 B5-1..B5-7）。"""
from __future__ import annotations

import json
import os

import mdl_gate_647 as G
import protector_mode_647 as M


def _hm():
    hm = dict(G.base.shadow.heatmap())
    hm.update(G.base.SYNTH_HEATMAP)
    return hm


def test_b5_1_enforce_blocks_rejects(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    hm, ex = _hm(), G.base.existing_rule_ids()
    assert G.publish_new_rule("CAND-SHORT-001", "短标题", 0.1, hm=hm, existing=ex)["published"] is True
    long_r = G.publish_new_rule("CAND-LONG-001", "冗长" * 400, 0.1, hm=hm, existing=ex)
    assert long_r["published"] is False and long_r["decision"].startswith("REJECT")
    assert G.publish_new_rule("CAND-NODATA-001", "T", None, hm=hm,
                              existing=ex)["published"] is False
    assert G.publish_new_rule("ATOM-REL-TARGET-HC", "已在册", 0.0, hm=hm,
                              existing=ex)["published"] is False


def test_b5_2_shadow_publishes_everything(monkeypatch):
    monkeypatch.setenv(M.ENV, "shadow")
    hm, ex = _hm(), G.base.existing_rule_ids()
    r = G.publish_new_rule("CAND-LONG-001", "冗长" * 400, 0.1, hm=hm, existing=ex)
    assert r["published"] is True and r["decision"].startswith("REJECT")


def test_b5_3_pending_human_is_not_a_pass(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    r = G.publish_new_rule("CAND-NODATA-001", "T", None, hm=_hm(),
                           existing=G.base.existing_rule_ids())
    assert r["decision"] == "PENDING_HUMAN" and r["published"] is False


def test_b5_4_existing_67_untouched():
    assert len(G.base.existing_rule_ids()) == 67
    src = open(os.path.join(G.HERE, "mdl_gate_647.py"), encoding="utf-8").read()
    for banned in ("gate_engine.RULES.append", "RULES.remove", "open(gate_engine"):
        assert banned not in src


def test_b5_5_rejected_candidates_are_kept():
    g = G.run_gate()
    assert all("detail" in r for r in g["rows"])
    assert g["n"] == g["n_published"] + g["n_blocked"]


def test_b5_6_publish_keeps_rejections():
    path = G.write_published()
    doc = json.load(open(path, encoding="utf-8"))
    assert doc["existing_67_rules_untouched"] is True
    assert any(not c["published"] for c in doc["candidates"])


def test_b5_7_report_and_selftest():
    assert G.selftest() == 0
    assert G.main(["--report"]) == 0
    doc = json.load(open(G.OUT_JSON, encoding="utf-8"))
    assert all(s["ok"] for s in doc["synthetic"])
    assert os.path.isfile(G.OUT_MD)
