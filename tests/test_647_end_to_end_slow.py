"""647 F · 端到端（slow）：**四块硬骨头 + 打靶准备**一次性串起来验（-m slow 跑）。

这是 647 的"收工级"慢用例：把每条硬骨头的**最小可证断言**串成一条链，
任何一块退化都会在这里红（而不是散落在各单测里各红一半）。
"""
from __future__ import annotations

import os

import decision_event_v2_626 as de
import external_anchor_647 as ext
import interface_verify_647 as iv
import protector_mode_647 as pmode
import protector_rollout_647 as rollout
import pytest
import targeting_prep_647 as targeting
import tool_integrity as ti
import verifier_closure_647 as vc

pytestmark = pytest.mark.slow


def test_slow_a1_a2_trust_root_fail_closed():
    """A1：缺信任根文件 ⇒ FAIL（strict）/ 不红（lenient）；A2：不完整事件 ⇒ 拒。"""
    a1 = ti.verify_supply_chain(strict=True)
    assert a1[2] == 0, "真实仓库信任根必须齐备"
    with pytest.raises(de.StrictEventError):
        de.DecisionEvent.from_dict_strict({})
    assert de.DecisionEvent.from_dict({}).result == "APPROVE", "历史宽容通道保留"


def test_slow_a3_closure_and_a4_anchor():
    cl = vc.build_closure()
    assert cl["status"] == "OK" and cl["n_rules"] == 67
    assert vc.consistency_with_tool_integrity(cl)["consistent"] is True
    assert vc.build_closure(missing=["tools/gate_engine.py"])["status"] == "FAIL"
    cur = ext.publish_current_anchor(published_at="2026-09-26T00:00:00Z")
    assert cur["published"] and cur["verified"] and cur["tamper_detected"]


def test_slow_b_protectors_enforce_and_rollback():
    """五个保护器 enforce 上岗 + 一键回滚到 shadow ⇒ 强制量归零 + 生产工件零漂移。"""
    saved = os.environ.get(pmode.ENV)
    try:
        os.environ[pmode.ENV] = "enforce"
        r = rollout.rollout()
        assert r["zero_drift"] is True, r["drift"]
        assert r["layer_check"]["keys_disjoint"] and r["layer_check"]["layers_distinct"]
    finally:
        if saved is None:
            os.environ.pop(pmode.ENV, None)
        else:
            os.environ[pmode.ENV] = saved
    rb = rollout.rollback_and_verify()
    assert rb["zero_enforcement"] is True and rb["wrote_mode_file"] is False


def test_slow_d_tools_merged_and_interface_ok():
    """15 → 10：成员已删、入口仍在；10 个核心工具接口合规。"""
    loss = iv.merge_loss_check()
    assert all(x["ok"] for x in loss)
    present = [n for n in iv.CORE_10 if os.path.isfile(os.path.join(iv.HERE, n + ".py"))]
    assert len(present) == 10


def test_slow_e_targeting_docs_ready():
    res = targeting.audit()
    assert res["all_ok"] is True and res["n"] == 3
    for r in res["docs"]:
        assert r["missing_sections"] == [] and r["declares_no_cards"] is True
