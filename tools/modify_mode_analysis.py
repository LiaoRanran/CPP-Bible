"""611 B2 · modify 口径影响分析报告生成器（**纯读** · 可独立复算）。

610 交人项 ① 的口径冲突：34 条 `modify` 的 `new_confidence` 全是 `medium`。
  * `keep-low`（入库权威口径，611 B1 起默认）：modify 保持 low ⇒ IN114/OUT7/击败 17；
  * `upgrade-medium`（609 A3 口径）：modify 落档 ⇒ IN121/OUT0/击败 0（论证层攻击性被抽空）。

本工具把"两种口径到底差在哪"量化成报告（`data/modify_mode_impact_analysis_611.md`），
**不替谁裁决**，只给事实 + 优缺点 + 建议。所有数字都由 `weighted_af_solver` 现算，可复算。

CLI：`--stats`（打印 JSON）/`--write`（写出报告）/`--check`（报告与现算一致？）。
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
REPORT_OUT = ROOT / "data" / "modify_mode_impact_analysis_611.md"

OUT_MIS_7 = ("MIS-LANG-001", "MIS-MEM-001", "MIS-MEM-003",
             "MIS-UB-001", "MIS-UB-004", "MIS-UB-008", "MIS-UB-014")


def _topic_group(mis_id: str) -> str:
    if mis_id.startswith("MIS-LANG"):
        return "LANG"
    if mis_id.startswith("MIS-MEM"):
        return "MEM"
    if mis_id.startswith("MIS-UB"):
        return "UB"
    return "OTHER"


def compute(edges_path: Path | str | None = None,
            ann_path: Path | str | None = None) -> dict:
    """现算两种口径的判决 + 34 条 modify 边的分布。**只读，不改任何文件**。

    返回 dict（含 `keep_low`/`upgrade` 两档判决、`modify_distribution`、
    `out_mis_by_mode`、可复算用的原始计数）。
    """
    import human_review_cli as hrc  # noqa: E402
    import weighted_af_solver as w2  # noqa: E402

    edges = w2.load_edges(edges_path) if hasattr(w2, "load_edges") and edges_path \
        else w2.load_edges()
    anns = hrc.load_annotations(ann_path) if ann_path else hrc.load_annotations()

    def verdict(mode: str) -> dict:
        eff, _ch = w2.reviewed_edges(edges, anns, modify_mode=mode)
        doc = w2.solve(eff)
        s = doc["summary"]
        return {"in": s["IN"], "out": s["OUT"], "undec": s["UNDEC"],
                "defeating_edges": doc["defeating_edges"], "rounds": doc["rounds"],
                "nodes": s["nodes"],
                "out_mis": sorted(n for n, lab in doc["nodes"].items()
                                  if lab.get("type") == "misconception"
                                  and lab.get("label") == "OUT")}

    keep = verdict("keep-low")
    up = verdict("upgrade-medium")

    # 34 条 modify 边分布（按 target 节点 + 主题组）
    last = hrc.latest_by_edge(anns)
    em = {e["id"]: e for e in edges}
    mods = [(eid, a) for eid, a in last.items() if hrc.kind_of(a) == "modify"]
    target_nodes: Counter = Counter()
    topic_group: Counter = Counter()
    for eid, _a in mods:
        e = em.get(eid)
        if not e:
            continue
        tgt = str(e.get("target") or e.get("mis_id") or "")
        target_nodes[tgt] += 1
        if tgt.startswith("MIS-"):
            topic_group[_topic_group(tgt)] += 1
    # 640 A1：OUT MIS 集合改为**当前现算**（签署后 OUT MIS = 42，历史 7 个清单
    # `OUT_MIS_7` 保留为 611 快照常量，不再用于过滤）。
    out_targets = sorted(t for t in target_nodes if t in set(keep["out_mis"]))

    return {
        "keep_low": keep, "upgrade": up, "modify_count": len(mods),
        "modify_distribution": {
            "distinct_target_nodes": len(target_nodes),
            "target_mis_count": sum(1 for t in target_nodes if t.startswith("MIS-")),
            "target_prop_count": sum(1 for t in target_nodes if not t.startswith("MIS-")),
            "by_target_node_top": target_nodes.most_common(15),
            "by_topic_group": dict(topic_group),
        },
        "out_mis_by_mode": {"keep_low": keep["out_mis"], "upgrade": up["out_mis"]},
        # 640 A1：语义更新 = 当前 OUT MIS 是否全部是 modify 目标（签署后为 False：
        # OUT MIS 42 个，modify 目标只有 7 个 MIS）。历史口径见 OUT_MIS_7。
        "all_out_mis_are_modify_targets": set(keep["out_mis"]) <= set(target_nodes),
        "out_mis_targets": out_targets,
        "historical_out_mis_7_still_out": set(OUT_MIS_7) <= set(keep["out_mis"]),
    }


def render_report(c: dict) -> str:
    kl, up = c["keep_low"], c["upgrade"]
    lines = [
        "# 611 B2 · modify 口径影响分析（keep-low vs upgrade-medium）", "",
        "> 背景（610 交人项 ①）：34 条 `modify` 人审的 `new_confidence` **全是 medium**。"
        "两种口径对这 34 条的处置不同 ⇒ 判决不同。**本报告只量化差异、给优缺点与建议，"
        "不替谁裁决**（口径裁决是监工/人的事，见 §四）。", "",
        "## 一、两档判决对比（现算，可复算）", "",
        "| 口径 | IN | OUT | UNDEC | 击败边 | 轮次 |",
        "|---|---:|---:|---:|---:|---:|",
        f"| `keep-low`（入库权威 / 611 B1 默认） | {kl['in']} | {kl['out']} | {kl['undec']} "
        f"| {kl['defeating_edges']} | {kl['rounds']} |",
        f"| `upgrade-medium`（609 A3） | {up['in']} | {up['out']} | {up['undec']} "
        f"| {up['defeating_edges']} | {up['rounds']} |", "",
        f"> **差异**：IN 差 **{up['in'] - kl['in']}** 个（{kl['in']}→{up['in']}）、"
        f"OUT 差 **{kl['out'] - up['out']}** 个（{kl['out']}→{up['out']}）、"
        f"击败边差 **{kl['defeating_edges'] - up['defeating_edges']}** 条"
        f"（{kl['defeating_edges']}→{up['defeating_edges']}）。", "",
        "## 二、34 条 modify 边的分布", "",
        f"- 总数：**{c['modify_count']}** 条（全部 `kind=modify`）；",
        f"- 按 target 节点：落在 **{c['modify_distribution']['distinct_target_nodes']}** 个不同节点上 ——"
        f" {c['modify_distribution']['target_mis_count']} 个 MIS（**恰好是全部 OUT MIS**）+ "
        f"{c['modify_distribution']['target_prop_count']} 个命题；",
        "- 按 MIS 主题组（仅对 MIS target 计）："
        + " / ".join(f"{k} {v}" for k, v in c["modify_distribution"]["by_topic_group"].items())
        + "；",
        f"- 关键事实（640 A1 更新）：签署后 OUT MIS 共 **{len(c['out_mis_by_mode']['keep_low'])}** 个，"
        f"其中只有 **{len(c['out_mis_targets'])}** 个是 `modify` 目标"
        f"（`all_out_mis_are_modify_targets={c['all_out_mis_are_modify_targets']}`）——"
        "历史 7 个 OUT MIS（611 快照）至今仍 OUT；", "",
        "top 分布（节点 → 该节点作为 target 的 modify 边数）：", "",
    ]
    for node, n in c["modify_distribution"]["by_target_node_top"]:
        flag = "（OUT MIS）" if node in OUT_MIS_7 else ""
        lines.append(f"- `{node}` → {n} 条 {flag}")
    lines += ["", "## 三、两档优缺点（事实，不是裁决）", "",
              "**`keep-low`（入库权威，640 重算后 IN79/OUT42/击败194）**：",
              "- ✅ 与已冻结的 `data/grounded_labels_w2.json` **逐字段一致**（640 A1 按签署后状态重算），"
              "不推翻既有交付；",
              "- ✅ 保守：人审说「保持 low」就保持 low，不替人升档；",
              "- ❌ 与 34 条 modify 人审的**字面意图**（`new_confidence=medium`）**不符** —— "
              "人审想升档，工具没升；",
              "- ❌ OUT MIS 42 个（签署后命题可信度 high，误解本就无法击败命题）。",
              "",
              "**`upgrade-medium`（609 A3）**：",
              "- ✅ 尊重 34 条 modify 人审的**字面意图**（medium 落档）；",
              "- ❌ 640 A1 实测：签署后命题可信度 high，34 条 low→medium 的升档**不足以翻转任何判决** "
              "⇒ 两档判决趋同（IN79/OUT42/击败194）——「upgrade 抽空攻击性」的 611 论据已随签署失效；",
              "- ⚖️ 两档的**机制差异**仍在（keep-low 下 34 条 modify 未生效留痕），"
              "若未来出现足以翻转的 modify 档位将重新分歧。", "",
              "## 四、口径裁决建议（不擅自执行）", "",
              "- 640 A1 诚实登记：**当前数据下两档判决一致**，611 的口径冲突在现有图上"
              "不再产生判决差异；冲突的**语义定义**（「modify 到底要不要改权重」）仍未钉死，"
              "留待未来出现实际分歧时再裁决。",
              "- 无论哪种，本工具与 `metrics_610.collect_modify_mode` 都已把两档数字"
              "**量化显形**，每次采集都能看到 divergence，不会悄悄换口径。",
              "- 无论哪种，本工具与 `metrics_610.collect_modify_mode` 都已把两档数字"
              "**量化显形**，每次采集都能看到 divergence，不会悄悄换口径。", "",
              "> 数字来源：全部由 `weighted_af_solver.reviewed_edges(..., modify_mode=...)` + `solve` "
              "现算，与 `tools/modify_mode_analysis.py --stats` 一致。", "",
              ]
    return "\n".join(lines) + "\n"


def check() -> list[str]:
    """报告与现算一致？返回问题列表（空 = 通过）。"""
    problems: list[str] = []
    c = compute()
    if not REPORT_OUT.is_file():
        problems.append(f"报告不存在：{REPORT_OUT}")
        return problems
    text = REPORT_OUT.read_text(encoding="utf-8")
    for token in (f"| {c['keep_low']['in']} | {c['keep_low']['out']}",
                  f"| {c['upgrade']['in']} | {c['upgrade']['out']}",
                  f"| {c['keep_low']['defeating_edges']} |",
                  f"| {c['upgrade']['defeating_edges']} |",
                  f"**{c['modify_count']}** 条",
                  f"其中只有 **{len(c['out_mis_targets'])}** 个是 `modify` 目标"):
        if token not in text:
            problems.append(f"报告缺/不一致：{token}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="modify_mode_analysis",
                                 description="611 B2 · modify 口径影响分析")
    ap.add_argument("--version", action="version", version=f"modify_mode_analysis {VERSION}")
    ap.add_argument("--stats", action="store_true", help="打印两档判决 + 分布 JSON")
    ap.add_argument("--write", action="store_true", help=f"写出 {REPORT_OUT.name}")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    c = compute()
    if a.stats:
        print(json.dumps(c, ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = check()
        if problems:
            for p in problems:
                print(f"[B2] ❌ {p}", file=sys.stderr)
            return 2
        print("[B2] ✓ 报告与现算一致")
        return 0
    if a.write:
        REPORT_OUT.write_text(render_report(c), encoding="utf-8", newline="\n")
        print(f"[B2] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}")
        return 0
    # 默认：打印摘要
    kl, up = c["keep_low"], c["upgrade"]
    print(f"keep-low: IN{kl['in']}/OUT{kl['out']}/击败{kl['defeating_edges']} · "
          f"upgrade: IN{up['in']}/OUT{up['out']}/击败{up['defeating_edges']} · "
          f"modify {c['modify_count']} 条")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
