"""611 新工具回归测试（**图结构/口径不变量** + 派生量走权威源）。

**640c A1/A2**：原版把 W2 派生量写死（`out_mis_count == 7`、承重 107、最大级联 1），
632/634 人签重算后过期（640c 的 2 项）。现在：
* 图/W2 派生量取 `tools/w2_derived_640c.py`（现算 vs 入库产物两路）；
* 工具的"摘要 vs 逐项明细"一致性由各工具自己的 `check()` 锁（真不变量）；
* E3 另加**夹具测试**（已知输入 → 已知输出），不依赖真库当前数字。

运行：`python -m pytest tests/test_611_tools.py -q`
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import bridge_edge_candidates as c2  # noqa: E402
import defense_chain as dc  # noqa: E402
import defense_chain_deepen as e3  # noqa: E402
import fragmentation_repair_analysis as c3  # noqa: E402
import human_review_quality_deepen as e2  # noqa: E402
import liveness_completion_plan as d2  # noqa: E402
import metrics_611 as e1  # noqa: E402
import oracle_verification_plan as d3  # noqa: E402
import out_mis_review_support as d1  # noqa: E402
import w2_derived_640c as wd  # noqa: E402

PIN = wd.pinned()


def test_c2_bridge_candidates():
    cands = c2.generate_candidates(c2.load_mis_index(), c2.component_map())
    s = c2.summarize(cands)
    assert s["total"] == 98
    assert s["by_priority"] == {"strong": 0, "medium": 0, "weak": 98}
    assert c2.check(cands) == []  # --check 锁定


def test_c3_fragmentation_repair():
    r = c3.analyze(cands=c3.load_candidates())
    assert r["components_before"] == 11
    assert r["components_after"] == 7
    assert r["largest_after"] == 97
    assert r["coverage_after"] == 0.8017
    assert r["verdict_changed"] == 0  # 候选皆 low，不应翻转胜负
    assert c3.check(r) == []


def test_d1_out_mis_review():
    """611 锁定的**复核范围**（7 个具名 MIS，冻结里程碑）全部仍在 OUT ⇒ check 绿。"""
    a = d1.analyze()
    assert a["out_mis_count"] == len(d1.KNOWN_OUT_MIS), "锁定目标应全部在位"
    assert a["out_nodes_total"] == PIN["out"], "全图 OUT 节点数应与权威产物一致"
    assert d1.check(a) == []


def test_d2_liveness_plan():
    p = d2.build_plan()
    assert p["total_missing"] == 50
    assert d2.check(p) == []


def test_d3_oracle_plan():
    p = d3.build_plan()
    assert p["cards_total"] == 83
    assert p["by_kind"].get("evidence") == 56
    assert p["by_kind"].get("atom") == 27
    assert p["verified"] == 0
    assert d3.check(p) == []


def test_e1_metrics_611():
    notes: dict = {}
    m = e1.collect_611_new_metrics(notes)
    assert notes == {}  # 全部采集器成功，无错误记账
    assert m["argument_graph_fragmentation"]["components"] == wd.components()["count"]
    assert m["bridge_candidates"]["total"] == 98       # C2 产物件数（数据产物，非 W2 派生量）
    assert m["out_mis_review"]["out_mis_count"] == PIN["out_mis"], "OUT MIS 数取权威产物"
    assert m["out_mis_review"]["out_nodes_total"] == PIN["out"]
    assert m["liveness_missing"]["missing_observation"] == 50
    assert m["oracle_verification"]["cards_total"] == 83
    assert m["oracle_verification"]["verified"] == 0


def test_e2_human_review_quality_deepen():
    a = e2.analyze()
    assert a["records"] == 388
    assert a["reviewer_diversity"]["distinct_reviewers"] == 1
    assert a["mis_consistency"]["modify_only_count"] == 7
    assert e2.check(a) == []


def test_e3_defense_chain_deepen():
    """真实库：只断言**不变量与内部一致**（承重/最大级联是随人签演进的派生量）。

    640c 现状：`nodes_whose_demote_changes_something == 0`、`max_ripple == 0` ——
    因为每条 MIS 都被 **≥2 个** `high` 命题击败（实测最少 2 个），单独压垮一个命题不改变任何判决。
    这是**正确行为**（不是坏了），故改断言内部一致性而非旧快照 107/1。
    """
    a = e3.analyze()
    assert a["total_nodes"] == len(a["demote_ripple"]) == len(a["escalate_ripple"]) == PIN["nodes"]
    assert a["nodes_whose_demote_changes_something"] \
        == sum(1 for c in a["demote_ripple"].values() if c > 0)
    assert a["max_ripple"] == max(a["demote_ripple"].values(), default=0)
    assert e3.check(a) == []


def _e3_fixture():
    """人造图：`P(high)` 同时击败 `M1(low)`、`M2(low)`（各 1 条边），`P` 自身无有效攻击者。

    现算：P IN / M1 OUT / M2 OUT。
    demote(P) ⇒ 两条击败边消失 ⇒ M1、M2 双双翻 IN（级联 2）；demote(M1/M2) ⇒ 本来就 low ⇒ 0。
    """
    p, m1, m2 = "ATOM-X-001::prop-1", "MIS-X-001", "MIS-Y-001"

    def e(i: str, s: str, t: str, kind: str) -> dc.AttackEdge:
        return dc.AttackEdge(edge_id=i, source=s, target=t, kind=kind,
                             confidence="medium", human_verdict="approve")

    edges = [e("E1", m1, p, "mis_to_prop"), e("E2", p, m1, "prop_to_mis"),
             e("E3", m2, p, "mis_to_prop"), e("E4", p, m2, "prop_to_mis")]
    cred = {p: "high", m1: "low", m2: "low"}
    return p, m1, m2, edges, dc.solve_verdicts(edges, cred), cred


def test_e3_analyze_fixture(monkeypatch):
    """夹具（真验证力）：已知输入 → 已知级联规模，不依赖真库当前数字。"""
    p, m1, m2, edges, verdicts, cred = _e3_fixture()
    assert verdicts == {p: "IN", m1: "OUT", m2: "OUT"}, "夹具前提：P IN、两个 MIS OUT"
    monkeypatch.setattr(dc, "load_data", lambda *_a, **_k: (edges, verdicts, cred))
    a = e3.analyze()
    assert a["total_nodes"] == 3
    assert a["demote_ripple"] == {p: 2, m1: 0, m2: 0}
    assert a["nodes_whose_demote_changes_something"] == 1
    assert a["max_ripple"] == 2
    assert e3.check(a) == []
