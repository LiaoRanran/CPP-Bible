"""611 C3 · 论证图碎片化修复影响分析（**只读 what-if** · 不真实落库）。

问题：C1 实测论证图碎片化（11 分量 / 最大覆盖 66.1%）；C2 生成了 98 条跨分量桥接候选。
本工具做 **what-if**：若把 C2 的候选边（作为 low 可信度的 `mis_to_mis` 攻击边）加入图，
碎片化程度是否改善？—— 只产出分析，**不**写权威边文件、**不**改 W2 判决（仓内只留分析文档）。

关键诚实点：
  * 连通性（分量数/覆盖率）只看**图结构**，方向忽略；
  * 候选边两端都是 `low` 可信度 ⇒ 在 W2 里**不构成击败**（同档），故判决 IN/OUT 不变；
    即"补桥"只改善连通性，不改变任何节点的胜负。
  * 若只加 strong/medium（本批为 0）则几乎不改善；改善全部来自 weak（同主题跨分量）候选。

CLI：`--stats`（JSON）/ `--write`（写 `data/fragmentation_repair_analysis_611.md`）/ `--check`。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
CAND_IN = ROOT / "data" / "bridge_edge_candidates_611.jsonl"
REPORT_OUT = ROOT / "data" / "fragmentation_repair_analysis_611.md"

# 611 C3 锁定：把全部 98 候选加入后，连通性的改善幅度（结构冻结前不变）
KNOWN = {"components_after": 7, "largest_after": 97, "coverage_after": 0.8017,
         "components_before": 11, "largest_before": 80, "isolated_before": 4}


def load_candidates(path: Path | None = None) -> list[dict]:
    p = Path(path) if path else CAND_IN
    if not p.is_file():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def _mk_bridge_edge(c: dict):
    import defense_chain as dc  # noqa: E402
    return dc.AttackEdge(edge_id=c["edge_id"], source=c["source"], target=c["target"],
                         kind="mis_to_mis", confidence="low", human_verdict="unreviewed",
                         edge_kind="bridge")


def analyze(edges_path=None, ann_path=None, cands: list[dict] | None = None) -> dict:
    import argument_audit as aa  # noqa: E402
    edges, verdicts, cred = aa.load_state(edges_path, ann_path)
    nodes = aa.all_nodes(verdicts, edges)
    comps_before = aa.detect_isolated_subgraphs(edges, nodes)
    sizes_before = sorted((len(c) for c in comps_before), reverse=True)

    if cands is None:
        cands = load_candidates()
    bridge_edges = [_mk_bridge_edge(c) for c in cands]
    merged = list(edges) + bridge_edges
    nodes_after = aa.all_nodes(verdicts, merged)
    comps_after = aa.detect_isolated_subgraphs(merged, nodes_after)
    sizes_after = sorted((len(c) for c in comps_after), reverse=True)
    isolated_after = sum(1 for c in comps_after if len(c) == 1)

    # 判决是否变化（候选都是 low ⇒ 应不变；显式核对，避免"想当然"）
    from defense_chain import credibilities_of, solve_verdicts  # noqa: E402
    v_before = solve_verdicts(edges, cred)
    v_after = solve_verdicts(merged, credibilities_of(merged))
    verdict_changed = sum(1 for n in v_before if v_before[n] != v_after.get(n))

    return {
        "components_before": len(comps_before),
        "components_after": len(comps_after),
        "largest_before": sizes_before[0],
        "largest_after": sizes_after[0],
        "coverage_before": round(sizes_before[0] / max(len(nodes), 1), 4),
        "coverage_after": round(sizes_after[0] / max(len(nodes_after), 1), 4),
        "isolated_before": sum(1 for c in comps_before if len(c) == 1),
        "isolated_after": isolated_after,
        "candidates_added": len(bridge_edges),
        "verdict_changed": verdict_changed,
        "note": ("候选边两端皆 low ⇒ W2 不构成击败 ⇒ 判决 IN/OUT 不变；"
                 "改善仅来自连通性（分量合并）。"),
    }


def render_report(r: dict, cands: list[dict]) -> str:
    lines = [
        "# 611 C3 · 论证图碎片化修复影响分析（what-if · 只读）", "",
        "> 把 C2 的 98 条桥接候选（作为 low 可信度 `mis_to_mis` 边）加入图，看碎片化是否改善。"
        "**不**写权威边文件、**不**改 W2 判决。", "",
        "## 一、连通性 before → after", "",
        "| 指标 | 加桥前 | 加桥后 | 变化 |",
        "|---|---|---|---|",
        f"| 连通分量 | {r['components_before']} | {r['components_after']} | "
        f"{r['components_after'] - r['components_before']} |",
        f"| 最大分量节点 | {r['largest_before']} | {r['largest_after']} | "
        f"{r['largest_after'] - r['largest_before']} |",
        f"| 最大分量覆盖率 | {r['coverage_before']:.1%} | {r['coverage_after']:.1%} | "
        f"{r['coverage_after'] - r['coverage_before']:+.1%} |",
        f"| 孤立节点 | {r['isolated_before']} | {r['isolated_after']} | "
        f"{r['isolated_after'] - r['isolated_before']} |",
        f"| 加入候选边数 | — | {r['candidates_added']} | — |",
        f"| 判决变化的节点数 | — | {r['verdict_changed']} | （应为 0：候选皆 low，不构成击败） |",
        "", "## 二、结论", "",
    ]
    if r["components_after"] < r["components_before"]:
        lines.append(
            f"- 加入全部 98 条候选后，连通分量从 **{r['components_before']}** 降到 "
            f"**{r['components_after']}**，最大分量覆盖率从 {r['coverage_before']:.1%} 升到 "
            f"{r['coverage_after']:.1%} —— **碎片化显著改善**（仍非单一连通分量，说明补桥是必要非充分）；")
    else:
        lines.append(
            f"- 加入候选后分量数未下降（{r['components_before']}→{r['components_after']}），"
            "说明当前候选无法连通碎片（需更强关联，或人工造真实攻击边）。")
    lines += [
        f"- 判决变化节点 = **{r['verdict_changed']}**（=0 符合预期：候选边两端皆 low，W2 同档不构成击败，"
        "不翻转任何 IN/OUT）；",
'       "- 因此「补桥」对论证**胜负**零影响，只让「谁和谁在同一个论证子图里」更清楚；',
        "- 是否真把候选落库为攻击边、重跑 W2，是**人审权力**（须逐条判断方向 + replay 证据），本工具不改仓。",
        "", "## 三、口径与边界", "",
        "- 连通性用忽略方向的 BFS（与 C1 同源）；",
        "- 候选数据来自 `data/bridge_edge_candidates_611.jsonl`（C2 产物，本工具只读它）；",
        "- 本分析是 **what-if**，仓内只留本 `.md`，不碰 `attack_edges_candidates.jsonl` / `grounded_labels_w2.json`。",
        "",
    ]
    return "\n".join(lines)


def check(r: dict) -> list[str]:
    problems: list[str] = []
    if KNOWN["components_after"] is not None and r["components_after"] != KNOWN["components_after"]:
        problems.append(f"加桥后分量应为 {KNOWN['components_after']}（实测 {r['components_after']}）")
    if KNOWN["largest_after"] is not None and r["largest_after"] != KNOWN["largest_after"]:
        problems.append(f"加桥后最大分量应为 {KNOWN['largest_after']}（实测 {r['largest_after']}）")
    if KNOWN["coverage_after"] is not None and abs(r["coverage_after"] - KNOWN["coverage_after"]) > 0.002:
        problems.append(f"加桥后覆盖率应为≈{KNOWN['coverage_after']}（实测 {r['coverage_after']}）")
    if r["verdict_changed"] != 0:
        problems.append(f"判决变化节点应为 0（实测 {r['verdict_changed']}）——候选不应改变胜负")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="fragmentation_repair_analysis",
                                 description="611 C3 碎片化修复影响分析（只读 what-if）")
    ap.add_argument("--version", action="version", version=f"fragmentation_repair_analysis {VERSION}")
    ap.add_argument("--stats", action="store_true", help="打印 JSON")
    ap.add_argument("--write", action="store_true", help=f"写 {REPORT_OUT.name}")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    cands = load_candidates()
    r = analyze(cands=cands)
    if a.stats:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = check(r)
        if problems:
            for p in problems:
                print(f"[C3] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[C3] ✓ 加桥分析锁定（分量 {r['components_before']}→{r['components_after']} · "
              f"覆盖 {r['coverage_before']:.1%}→{r['coverage_after']:.1%} · 判决变化 {r['verdict_changed']}）")
        return 0
    if a.write:
        REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
        REPORT_OUT.write_text(render_report(r, cands), encoding="utf-8", newline="\n")
        print(f"[C3] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}"
              f"（分量 {r['components_before']}→{r['components_after']} · "
              f"覆盖 {r['coverage_before']:.1%}→{r['coverage_after']:.1%}）")
        return 0
    print(f"分量 {r['components_before']}→{r['components_after']} · "
          f"覆盖 {r['coverage_before']:.1%}→{r['coverage_after']:.1%} · "
          f"判决变化 {r['verdict_changed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
