"""629 B3 · 未覆盖攻击面清单与优先级 单测（7 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import attack_mapping_629 as M
import attack_surface_taxonomy as T
import uncovered_attack_surfaces as U


def test_list_matches_zero_event_vectors():
    zero = set(M.stats()["zero_hit_vectors"])
    assert {i["id"] for i in U.uncovered()} == zero
    assert len(zero) > 0, "应存在零命中向量（否则分类学无意义）"


def test_scoring_is_reproducible():
    for i in U.uncovered():
        assert i["score"] == U.score(i, True) == (
            U.RISK_WEIGHT[i["risk"]] + (0 if i["covered"] else 2) + 2)
        assert i["priority"] == U.priority(i["score"])


def test_priority_thresholds():
    for i in U.uncovered():
        if i["score"] >= 7:
            assert i["priority"] == "P0"
        elif i["score"] >= 5:
            assert i["priority"] == "P1"
        else:
            assert i["priority"] == "P2"


def test_p0_are_high_risk_without_probe():
    p0 = [i for i in U.uncovered() if i["priority"] == "P0"]
    assert p0, "至少应有 1 个 P0（高危 + 零探针 + 零命中）"
    assert all(i["risk"] == "high" and not i["covered"] for i in p0)


def test_every_uncovered_has_design_and_mode():
    modes = {"可自动化", "人机结合", "需人审"}
    for i in U.uncovered():
        assert i["design"] and "未登记设计" not in i["design"], i["id"]
        assert i["mode"] in modes, i["id"]


def test_design_keys_are_valid_vectors():
    known = {v["id"] for v in T.vectors()}
    assert set(U.DESIGN) <= known, f"设计表含未知向量：{set(U.DESIGN) - known}"


def test_report_and_selftest():
    p = U.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("P0", "P1", "P2", "建议探针设计", "需人审"):
        assert kw in md
    assert U.selftest() == 0
