"""627 A1 · W2 投影归一化 / 差异对比 单测（≥4 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import w2_projection_diff_627 as D
import w2_projection_normalizer_627 as N
from w2_authority_640b import current as _w2  # 640b：W2 数字单一权威源


def _exp() -> dict:
    return _w2()


def test_normalizer_node_count_121():
    nodes = N.load_grounded_nodes()
    assert len(nodes) == 121


def test_normalizer_in_out_distribution():
    res = N.compile_w2()
    exp = _exp()
    assert res["summary"]["IN"] == exp["IN"]
    assert res["summary"]["OUT"] == exp["OUT"]
    assert res["summary"]["UNDEC"] == exp["UNDEC"]


def test_normalizer_no_outside_nodes():
    # 归一化封闭性：所有 active 边的 source/target 都在 121 节点内
    nodes = N.load_grounded_nodes()
    edges = N.authority_active_edges()
    outside = [(e["source"], e["target"]) for e in edges
               if e["source"] not in nodes or e["target"] not in nodes]
    assert not outside, f"{len(outside)} 边落在 121 节点之外"


def test_diff_zero_against_grounded():
    d = D.diff()
    exp = _exp()
    assert d["diff_count"] == 0                       # 投影与权威产物零差异
    assert d["projected_summary"]["IN"] == exp["IN"]
    assert d["projected_summary"]["OUT"] == exp["OUT"]
    assert d["cause_breakdown"] == {}


def test_modify_is_required_for_full_out():
    """626 缺陷回归：只认 APPROVE 得到的 OUT 必然少于（计入 MODIFY 的）权威 OUT。"""
    nodes = N.load_grounded_nodes()
    led = N.D.AuthorityLedger.import_jsonl(N.LEDGER)
    only_appr = [(e.target_id, e.result) for e in led.all_events()
                 if e.target_type == "edge" and e.result == "APPROVE"]
    assert any(e.result == "MODIFY" for e in led.all_events()
               if e.target_type == "edge")
    # 仅用 APPROVE 时 OUT 必然 < 7
    import weighted_af_solver as W
    def parse(t):
        b = t[3:] if t.startswith("ae-") else t
        s, d = b.split("->", 1)
        return s, d
    es = []
    seen = set()
    for tid, _ in only_appr:
        s, d = parse(tid)
        if (s, d) in seen:
            continue
        seen.add((s, d))
        es.append({"source": s, "target": d, "direction":
                   "mis_to_prop" if s.startswith("MIS") else "prop_to_mis"})
    defeats = W.defeats_of(es, nodes)
    labels, _ = W.grounded_labels(nodes, defeats)
    out = sum(1 for v in labels.values() if v == "OUT")
    assert out < _exp()["OUT"], "只用 APPROVE 应少于权威 OUT（证明 MODIFY 必计入）"
