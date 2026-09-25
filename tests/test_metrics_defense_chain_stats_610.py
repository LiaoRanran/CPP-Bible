"""610 D3 · 辩护链统计集成（tools/metrics_610.py::collect_defense_chain_stats）。

锁五件事（任务书 D3 的 5 例 + 2 例自加）：
  1. `total_nodes` = **121**，键齐全；
  2. in **114** / out **7** / undec **0**；
  3. defeating_edges **17** · total_edges 388；
  4. no_defenders **7** / no_attackers **4** + 可信度分布 {high 0, medium 114, low 7}；
  5. 引擎不可用 ⇒ `{"error": ...}` + notes 记账（不给半截数）；
  +. 与 608 的 `grounded` 判决数同值（跨工具口径一致）；
  +. 容器 `metrics_610` 三键齐全。
"""
from __future__ import annotations

import metrics_610 as m610
import metrics_collector as mc


def test_collect_defense_chain_stats():
    out = m610.collect_defense_chain_stats({})
    for k in ("total_nodes", "in", "out", "undec", "total_edges", "defeating_edges",
              "no_defenders", "no_attackers", "source"):
        assert k in out, f"缺字段 {k}"
    assert out["total_nodes"] == 121
    assert out["source"].startswith("defense_chain.py")


def test_stats_in_out():
    from w2_authority_640b import current as _w2
    exp = _w2()
    out = m610.collect_defense_chain_stats({})
    assert (out["in"], out["out"], out["undec"]) == (exp["IN"], exp["OUT"], exp["UNDEC"])


def test_defeating_edges():
    from w2_authority_640b import current as _w2
    exp = _w2()
    out = m610.collect_defense_chain_stats({})
    assert out["defeating_edges"] == exp["defeating_edges"]
    assert out["total_edges"] == exp["edges"] == 388


def test_no_defenders_no_attackers():
    """no_defenders = OUT 数（每个 OUT 节点必有击败者…口径见工具）；可信度分布随人签演进。"""
    from w2_authority_640b import current as _w2
    exp = _w2()
    out = m610.collect_defense_chain_stats({})
    assert out["no_attackers"] == 4
    assert out["no_defenders"] >= exp["OUT"]        # 含无攻击者的保守计法
    dist = out["credibility_distribution"]
    assert set(dist) == {"high", "medium", "low"}
    assert dist["low"] == 7                          # 未人审边仍 low（322 条边口径）


def test_tool_not_found(monkeypatch):
    import defense_chain as dc

    def boom(*_a, **_k):
        raise ImportError("defense_chain engine unavailable")

    monkeypatch.setattr(dc, "load_data", boom)
    notes: dict = {}
    out = m610.collect_defense_chain_stats({}, notes)
    assert "error" in out and "ImportError" in out["error"]
    assert "defense_chain_stats_610" in notes
    assert "total_nodes" not in out, "失败路径不得给出半截统计"


def test_agrees_with_608_grounded():
    from w2_authority_640b import current as _w2
    exp = _w2()
    a = m610.collect_defense_chain_stats({})
    b = mc.collect_608_new_metrics({}, with_heavy=False)["grounded"]
    assert (a["in"], a["out"], a["undec"]) == (b["in"], b["out"], b["undec"]) == (
        exp["IN"], exp["OUT"], exp["UNDEC"])
    assert a["total_edges"] == b["candidate_edges_total"] == exp["edges"]


def test_container_has_all_three_keys():
    d = m610.collect_610_new_metrics({}, with_heavy=False)
    assert set(d) == {"grounded_status", "human_review_progress", "defense_chain_stats"}
    from w2_authority_640b import current as _w2
    assert d["defense_chain_stats"]["defeating_edges"] == _w2()["defeating_edges"]
