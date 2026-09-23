"""629 B2 · 历史攻击映射 单测（6 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import attack_mapping_629 as M
import attack_surface_taxonomy as T


def test_event_scale_and_uniqueness():
    ev = M.events()
    assert len(ev) >= 15, "任务书要求至少 15 条历史事件"
    assert len({e["id"] for e in ev}) == len(ev)


def test_every_event_maps_to_known_vector():
    known = {v["id"] for v in T.vectors()}
    bad = [e["vector"] for e in M.events() if e["vector"] not in known]
    assert not bad, f"未知向量：{bad}"
    assert all(e["layer"] == e["vector"].split(".")[0] for e in M.events())


def test_event_fields_complete():
    for e in M.events():
        assert e["status"] in M.VALID_STATUS, e["id"]
        assert e["name"] and e["batch"] and e["source"], e["id"]
        assert e["risk"] in T.VALID_RISK and isinstance(e["has_probe"], bool)


def test_layer_stats_reconcile():
    st = M.stats()
    ev = M.events()
    assert st["events"] == len(ev)
    assert sum(st["by_layer"].values()) == len(ev)
    assert sum(st["by_status"].values()) == len(ev)
    assert len(st["by_layer"]) >= 5, "历史事件不应集中在单层"
    hit = {e["vector"] for e in ev}
    assert st["hit_vectors"] == len(hit)
    assert set(st["zero_hit_vectors"]) == {v["id"] for v in T.vectors()} - hit


def test_report_written_with_stats():
    p = M.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("事件 → 攻击面向量", "按层统计", "零命中", "局限"):
        assert kw in md, f"报告缺：{kw}"
    assert "`L4.1`" in md and "EV-MATRIX" in md


def test_selftest_passes():
    assert M.selftest() == 0
