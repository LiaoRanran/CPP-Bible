"""611 · metrics_collector 的新增采集器（**独立模块** ⇒ 逐任务可独立提交，主采集器只挂一行）。

把 611 各线（C 线论证图碎片化 / C2 桥接候选 / D1 OUT MIS / D2 活性锚 / D3 oracle）的**只读**事实
聚合成 `metrics_611` 嵌套指标，挂到快照里（与 `metrics_608` / `metrics_610` 同级，不动扁平 27 项）。

每个采集器**独立 try/except**：任一项失败 ⇒ 该键记 `{"error": ...}` + notes 记账，
不影响其余采集器（与 610 同纪律）。所有数字来自 611 各工具的同源口径。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
BRIDGE_CAND = ROOT / "data" / "bridge_edge_candidates_611.jsonl"


def collect_argument_graph_fragmentation(notes: dict | None = None) -> dict:
    """C1：论证图碎片化（与 `argument_graph_analysis --check` 同源口径）。"""
    try:
        import argument_graph_analysis as aga
        c = aga.analyze()
        return {"components": c["components"], "isolated": len(c["isolated"]),
                "largest_size": c["largest_size"], "coverage": c["coverage"],
                "nodes": c["nodes"], "edges": c["edges"],
                "source": "tools/argument_graph_analysis.py（C1，复用 610 argument_audit BFS）"}
    except Exception as exc:                         # noqa: BLE001
        if notes is not None:
            notes["arg_graph_frag_611"] = f"采集失败：{type(exc).__name__}: {exc}"
        return {"error": f"{type(exc).__name__}: {exc}"}


def collect_bridge_candidates(notes: dict | None = None) -> dict:
    """C2：桥接攻击边候选数（读 C2 产物 jsonl，绝对不重算生成）。"""
    try:
        if not BRIDGE_CAND.is_file():
            return {"error": "C2 产物缺失：data/bridge_edge_candidates_611.jsonl（先跑 C2）"}
        rows = [json.loads(line) for line in BRIDGE_CAND.read_text(encoding="utf-8").splitlines() if line.strip()]
        from collections import Counter as _C  # noqa: E402
        pc = _C(r["priority"] for r in rows)
        return {"total": len(rows),
                "by_priority": {"strong": pc.get("strong", 0), "medium": pc.get("medium", 0),
                                "weak": pc.get("weak", 0)},
                "source": "data/bridge_edge_candidates_611.jsonl（C2 产物）"}
    except Exception as exc:                         # noqa: BLE001
        if notes is not None:
            notes["bridge_candidates_611"] = f"采集失败：{type(exc).__name__}: {exc}"
        return {"error": f"{type(exc).__name__}: {exc}"}


def collect_out_mis(notes: dict | None = None) -> dict:
    """D1：OUT 的 7 个 MIS 复核支撑状态（与 `out_mis_review_support --check` 同源）。"""
    try:
        import defense_chain as dc
        edges, verdicts, cred = dc.load_data()
        out_nodes = [n for n, v in verdicts.items() if v == "OUT"]
        return {"out_mis_count": len(out_nodes),
                "out_nodes_total": len(out_nodes),
                "known_out_mis": ["MIS-LANG-001", "MIS-MEM-001", "MIS-MEM-003", "MIS-UB-001",
                                  "MIS-UB-004", "MIS-UB-008", "MIS-UB-014"],
                "source": "defense_chain.load_data（610 B1 引擎）"}
    except Exception as exc:                         # noqa: BLE001
        if notes is not None:
            notes["out_mis_611"] = f"采集失败：{type(exc).__name__}: {exc}"
        return {"error": f"{type(exc).__name__}: {exc}"}


def collect_liveness_missing(notes: dict | None = None) -> dict:
    """D2：缺活性锚的 observation 命题数（与 `proposition_liveness_audit` 同源）。"""
    try:
        import proposition_liveness_audit as pla
        res = pla.audit()
        st = res["observation_status"]
        return {"missing_observation": st.get("missing", 0),
                "needs_review": st.get("needs_review", 0),
                "ok": st.get("ok", 0),
                "total_observation": res["propositions"]["observation"],
                "source": "tools/proposition_liveness_audit.py（607）"}
    except Exception as exc:                         # noqa: BLE001
        if notes is not None:
            notes["liveness_missing_611"] = f"采集失败：{type(exc).__name__}: {exc}"
        return {"error": f"{type(exc).__name__}: {exc}"}


def collect_oracle(notes: dict | None = None) -> dict:
    """D3：oracle 验证覆盖（83 卡 / 已验 0；与 `oracle_rotation._load_cards` 同源）。"""
    try:
        import oracle_rotation as orot
        cards = orot._load_cards()
        verified = sum(1 for c in cards if c.get("verified_by_oracle"))
        from collections import Counter as _C  # noqa: E402
        kind = _C("evidence" if c["id"].startswith("EV-") else
                  ("atom" if c["id"].startswith("ATOM-") else "other") for c in cards)
        return {"cards_total": len(cards), "verified": verified, "unverified": len(cards) - verified,
                "by_kind": dict(kind),
                "source": "oracle_rotation._load_cards（583/610 同源）"}
    except Exception as exc:                         # noqa: BLE001
        if notes is not None:
            notes["oracle_611"] = f"采集失败：{type(exc).__name__}: {exc}"
        return {"error": f"{type(exc).__name__}: {exc}"}


def collect_611_new_metrics(notes: dict, *, with_heavy: bool = True) -> dict:
    """611 新增指标容器（挂 `metrics_611`，与 608/610 同级，**不动扁平 schema**）。"""
    return {
        "version": VERSION,
        "argument_graph_fragmentation": collect_argument_graph_fragmentation(notes),
        "bridge_candidates": collect_bridge_candidates(notes),
        "out_mis_review": collect_out_mis(notes),
        "liveness_missing": collect_liveness_missing(notes),
        "oracle_verification": collect_oracle(notes),
    }
