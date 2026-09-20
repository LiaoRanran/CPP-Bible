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


def two_mode_verdicts() -> dict:
    """611 B1：两档 modify 口径各现算一遍 W2 判决 + 差值（**纯读**，不改任何文件）。

    返回 `{"modes": {keep-low: {...}, upgrade-medium: {...}}, "default": ...,
    "divergence": bool, "divergence_detail": str}`；任一档算不出来 ⇒ 抛异常（调用方记账）。
    """
    import human_review_cli as hrc
    import weighted_af_solver as w2

    edges = w2.load_edges()
    anns = hrc.load_annotations()
    modes: dict[str, dict] = {}
    for mode in w2.MODIFY_MODES:
        eff, _ch = w2.reviewed_edges(edges, anns, modify_mode=mode)
        d = w2.solve(eff)
        modes[mode] = {"in": d["summary"]["IN"], "out": d["summary"]["OUT"],
                       "undec": d["summary"]["UNDEC"],
                       "defeating_edges": d["defeating_edges"],
                       "caliber": ("modify 保持 low（入库权威口径）" if mode == "keep-low"
                                   else "modify ⇒ new_confidence（609 A3 口径）")}
    lo, up = modes["keep-low"], modes["upgrade-medium"]
    diff = {"in": up["in"] - lo["in"], "out": up["out"] - lo["out"],
            "defeating_edges": up["defeating_edges"] - lo["defeating_edges"]}
    return {"modes": modes, "default": w2.DEFAULT_MODIFY_MODE,
            "divergence": modes["keep-low"] != modes["upgrade-medium"],
            "divergence_detail": {k: v for k, v in diff.items() if v},
            "note": ("两档口径判决不同 ⇒ 口径裁决未定（谁对由人定，工具只呈现）；"
                     "引用 W2 数字必须标明用的哪一档") if modes["keep-low"] != modes["upgrade-medium"]
            else "两档口径判决一致 ⇒ 该冲突对本图不产生影响"}


def collect_modify_mode(metrics: dict, notes: dict | None = None) -> dict:
    """611 B1：modify 口径指标（当前默认档 / 两档判决 / 分歧差值）。

    为什么单列：口径冲突（610 交人项 ①）在裁决前必须**一直可见** —— 把它做成指标，
    每次采集都会把"两档差多少"写进台账，避免"默认值悄悄换掉却没人发现"。
    """
    try:
        out = two_mode_verdicts()
        return {"current_mode": out["default"], "modes": out["modes"],
                "divergence": out["divergence"],
                "divergence_detail": out["divergence_detail"], "note": out["note"],
                "source": "tools/weighted_af_solver.py --modify-mode（611 B1）"}
    except Exception as exc:                     # noqa: BLE001
        if notes is not None:
            notes["modify_mode_611"] = f"采集失败：{type(exc).__name__}: {exc}"
        return {"error": f"{type(exc).__name__}: {exc}"}


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
        try:                                   # 现算**两口径**（分歧显形，不用于覆盖权威值）
            edges = w2.load_edges()
            anns = hrc.load_annotations()
            modes: dict[str, dict] = {}
            for mode in w2.MODIFY_MODES:
                eff, _ch = w2.reviewed_edges(edges, anns, modify_mode=mode)
                d = w2.solve(eff)
                modes[mode] = {"in": d["summary"]["IN"], "out": d["summary"]["OUT"],
                               "undec": d["summary"]["UNDEC"],
                               "defeating_edges": d["defeating_edges"],
                               "caliber": ("modify 保持 low（入库权威口径）" if mode == "keep-low"
                                           else "modify ⇒ new_confidence（609 A3 口径）")}
            out["modes"] = modes
            out["default_modify_mode"] = w2.DEFAULT_MODIFY_MODE
            # 兼容 610 的字段语义：`solver_recompute` = **609 A3 口径**现算（611 B1 起它
            # 不再是默认档 ⇒ 默认档单列在 `solver_recompute_default`，避免"默认"被静默改写）
            out["solver_recompute"] = modes["upgrade-medium"]
            out["solver_recompute_default"] = modes[w2.DEFAULT_MODIFY_MODE]
            up = modes["upgrade-medium"]
            same = (up["in"] == out["in"] and up["out"] == out["out"]
                    and up["defeating_edges"] == out["defeating_edges"])
            # `divergence` = **两口径判决是否不同**（口径冲突信号，与"默认档是否等于权威产物"分开记）
            out["divergence"] = modes["keep-low"] != modes["upgrade-medium"]
            out["default_matches_artifact"] = (
                modes[w2.DEFAULT_MODIFY_MODE]["in"] == out["in"]
                and modes[w2.DEFAULT_MODIFY_MODE]["out"] == out["out"]
                and modes[w2.DEFAULT_MODIFY_MODE]["defeating_edges"] == out["defeating_edges"])
            out["divergence_note"] = (
                "口径分歧（610 A1 实测，611 B1 起**两档并存**）：入库产物用「modify 保持 low」⇒ "
                f"IN{out['in']}/OUT{out['out']}/击败 {out['defeating_edges']}；"
                f"「modify ⇒ new_confidence」⇒ IN{up['in']}/OUT{up['out']}/击败 "
                f"{up['defeating_edges']}。当前默认档 `{w2.DEFAULT_MODIFY_MODE}` 与入库产物"
                f"{'一致' if out['default_matches_artifact'] else '**不一致**'}；"
                "需监工裁决，本采集不擅自统一。")
            if not same:
                out["divergence_detail"] = (
                    f"两档差 {up['in'] - out['in']} 个 IN / {up['out'] - out['out']} 个 OUT / "
                    f"{up['defeating_edges'] - out['defeating_edges']} 条击败边")
        except Exception as exc:                 # noqa: BLE001
            out["solver_recompute"] = {"error": f"{type(exc).__name__}: {exc}"}
            out["divergence"] = None
        return out
    except Exception as exc:                     # noqa: BLE001
        if notes is not None:
            notes["grounded_status_610"] = f"采集失败：{type(exc).__name__}: {exc}"
        return {"error": f"{type(exc).__name__}: {exc}"}


def collect_human_review_progress(metrics: dict, notes: dict | None = None) -> dict:
    """D2：人审进度（读 388 条授权人审）。

    * 计数走 610 A2 的报告统计（与"人审质量报告"**同一函数** ⇒ 跨工具单一真源）；
    * `total_edges` 取候选边文件长度（不写死 388）；`progress_percent` = reviewed/total；
    * `top_modify_mis` = modify 比例最高的前 5 个 MIS（歧义集中区）；
    * 失败 ⇒ `{"error": ...}` + notes 记账，不中断其它采集器。
    """
    try:
        import attack_edge_generator as aeg
        import human_review_report as hrr
        anns = hrr.load_annotations()
        v = hrr.summarize_by_verdict(anns)
        by_mis = hrr.summarize_by_mis(anns)
        total = len(aeg.load_edges())
        reviewed = len({str(a.get("edge_id")) for a in anns})
        return {
            "total_edges": total, "reviewed": reviewed, "unreviewed": total - reviewed,
            "approve": v["approve"]["count"], "modify": v["modify"]["count"],
            "reject": v["reject"]["count"],
            "progress_percent": round(reviewed / total * 100, 2) if total else None,
            "top_modify_mis": [r["mis_id"] for r in by_mis[:5]],
            "mis_groups": len(by_mis),
            "source": "data/human_attack_edge_annotations.jsonl（用户授权人审）",
        }
    except Exception as exc:                         # noqa: BLE001
        if notes is not None:
            notes["human_review_progress_610"] = f"采集失败：{type(exc).__name__}: {exc}"
        return {"error": f"{type(exc).__name__}: {exc}"}


def collect_defense_chain_stats(metrics: dict, notes: dict | None = None) -> dict:
    """D3：辩护链统计（调 610 B1 引擎 `defense_chain.stats`，同一口径 ⇒ 与 `--check` 同数）。

    * 引擎缺失/异常 ⇒ `{"error": ...}` + notes 记账，不中断其它采集器；
    * 额外带上可信度分布（`high/medium/low`）——它是 C 线 P0 漏洞的判据。
    """
    try:
        import defense_chain as dc
        edges, verdicts, cred = dc.load_data()
        st = dc.stats(edges, verdicts, cred)
        return {"total_nodes": st["total_nodes"], "in": st["in"], "out": st["out"],
                "undec": st["undec"], "total_edges": st["total_edges"],
                "defeating_edges": st["defeating_edges"], "no_defenders": st["no_defenders"],
                "no_attackers": st["no_attackers"],
                "credibility_distribution": st["credibility_distribution"],
                "source": "defense_chain.py（610 B1 引擎）"}
    except Exception as exc:                         # noqa: BLE001
        if notes is not None:
            notes["defense_chain_stats_610"] = f"采集失败：{type(exc).__name__}: {exc}"
        return {"error": f"{type(exc).__name__}: {exc}"}


def collect_610_new_metrics(notes: dict, *, with_heavy: bool = True) -> dict:
    """610 新增指标容器（挂 `metrics_610`，与 608 的 `metrics_608` 同级，**不动扁平 27 项**）。"""
    return {"grounded_status": collect_grounded_status({}, notes),
            "human_review_progress": collect_human_review_progress({}, notes),
            "defense_chain_stats": collect_defense_chain_stats({}, notes)}
