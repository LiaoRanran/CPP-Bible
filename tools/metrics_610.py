"""610 · metrics_collector 的新增采集器（**独立模块** ⇒ 逐任务可独立提交，主采集器只挂一行）。

D1 `collect_grounded_status`：W2 判决状态（人审全量后）。
  * **权威值**取入库产物 `data/grounded_labels_w2.json`（监工验收的 W2 口径：IN114/OUT7/击败边 17）；
  * 同时用 `weighted_af_solver` **现算一遍**并登记两者是否一致 —— 610 实测发现**口径分歧**：
    产物口径（**modify 保持 low**）⇒ IN114/OUT7/击败边 17；
    求解器口径（`modify` 取 `new_confidence`，609 A3）⇒ **IN121/OUT0/击败边 0**。
    分歧以 `divergence` + `divergence_note` **显形**，不掩盖、不擅自统一（改判决口径需授权）；
  * 任何一步失败 ⇒ `{"error": ...}` + notes 记账，**不影响**其它采集器。

口径分离纪律：本模块**只读**，不写任何判决/标注数据；新旧指标并存时以"同一事实源、可交叉核对"为准。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"


def collect_grounded_status(metrics: dict, notes: dict | None = None) -> dict:
    """D1：W2 判决状态（产物权威值 + 求解器现算值 + 分歧标记）。"""
    try:
        import human_review_cli as hrc
        import weighted_af_solver as w2
        art_path = ROOT / "data" / "grounded_labels_w2.json"
        art = json.loads(art_path.read_text(encoding="utf-8"))
        s = art.get("summary", {})
        out = {
            "in": s.get("IN"), "out": s.get("OUT"), "undec": s.get("UNDEC"),
            "in_propositions": s.get("IN_propositions"),
            "in_misconceptions": s.get("IN_misconceptions"),
            "defeating_edges": art.get("defeating_edges"),
            "nodes": s.get("nodes"),
            "include_human_reviewed": bool(hrc.load_annotations() or []),
            "source": "data/grounded_labels_w2.json（入库 W2 产物）",
            "artifact_path": str(art_path.relative_to(ROOT).as_posix()),
        }
        try:                                   # 现算一遍（分歧显形，不用于覆盖权威值）
            edges = w2.load_edges()
            anns = hrc.load_annotations()
            eff, _changes = w2.reviewed_edges(edges, anns)
            doc = w2.solve(eff)
            recompute = {"in": doc["summary"]["IN"], "out": doc["summary"]["OUT"],
                         "undec": doc["summary"]["UNDEC"],
                         "defeating_edges": doc["defeating_edges"],
                         "caliber": "modify ⇒ new_confidence（609 A3 口径）"}
            out["solver_recompute"] = recompute
            same = (recompute["in"] == out["in"] and recompute["out"] == out["out"]
                    and recompute["defeating_edges"] == out["defeating_edges"])
            out["divergence"] = not same
            if not same:
                out["divergence_note"] = (
                    "口径分歧（610 A1 实测）：入库产物用「modify 保持 low」⇒ "
                    f"IN{out['in']}/OUT{out['out']}/击败 {out['defeating_edges']}；"
                    f"weighted_af_solver.reviewed_edges 用「modify ⇒ new_confidence」⇒ "
                    f"IN{recompute['in']}/OUT{recompute['out']}/击败 "
                    f"{recompute['defeating_edges']}。需监工裁决，本采集不擅自统一。")
        except Exception as exc:                 # noqa: BLE001
            out["solver_recompute"] = {"error": f"{type(exc).__name__}: {exc}"}
            out["divergence"] = None
        return out
    except Exception as exc:                     # noqa: BLE001
        if notes is not None:
            notes["grounded_status_610"] = f"采集失败：{type(exc).__name__}: {exc}"
        return {"error": f"{type(exc).__name__}: {exc}"}


def collect_610_new_metrics(notes: dict, *, with_heavy: bool = True) -> dict:
    """610 新增指标容器（挂 `metrics_610`，与 608 的 `metrics_608` 同级，**不动扁平 27 项**）。"""
    return {"grounded_status": collect_grounded_status({}, notes)}
