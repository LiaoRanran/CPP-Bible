"""611 E3 · 辩护链推理深化（**只读** · 不裁决、不改仓）。

在 610 B1 `defense_chain` 的"单点 what-if"之上**深化**为"全图敏感性"：对每个节点分别做两种压力测试，
量化它在论证图里的**承重程度**（load-bearing）：

  * **demote**（压到 low）：模拟"这条证据/误解被推翻" ⇒ 多少其它节点的判决随之翻转；
  * **escalate**（升到 high）：模拟"这条被提升到高可信" ⇒ 多少节点翻转。

输出：承重 Top 节点（两种方向）、级联规模分布、以及"7 个 OUT MIS 若升到 medium"的聚合影响
（即 D1 的全局版）。这些数字揭示**论证图对哪些节点最脆弱**，供人决定优先复核/加固。

⚠️ 只读：所有翻转只存在于内存重算里，**不改仓、不落库、不自动裁决**。

CLI：`--stats`（JSON）/ `--write`（写 `data/defense_chain_deepen_611.md`）/ `--check`。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
REPORT_OUT = ROOT / "data" / "defense_chain_deepen_611.md"
KNOWN_OUT_MIS = ["MIS-LANG-001", "MIS-MEM-001", "MIS-MEM-003", "MIS-UB-001",
                 "MIS-UB-004", "MIS-UB-008", "MIS-UB-014"]


def analyze(edges_path=None, ann_path=None) -> dict:
    import defense_chain as dc
    edges, verdicts, cred = dc.load_data(edges_path, ann_path)
    nodes = sorted(verdicts)
    demote, escalate = {}, {}
    for n in nodes:
        d = dc.what_if(n, "low", edges, verdicts, cred)
        demote[n] = len(d["changed_nodes"])
        if cred.get(n) != "high":
            e = dc.what_if(n, "high", edges, verdicts, cred)
            escalate[n] = len(e["changed_nodes"])
        else:
            escalate[n] = 0
    # 承重 Top（按两种方向的最大翻转数）
    def top(d: dict, k=10):
        return sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
    # 7 个 OUT MIS 若升到 medium 的聚合影响
    cred2 = dict(cred)
    for m in KNOWN_OUT_MIS:
        cred2[m] = "medium"
    v2 = dc.solve_verdicts(edges, cred2)
    flipped = sorted(n for n in verdicts if verdicts[n] != v2.get(n))
    return {
        "total_nodes": len(nodes),
        "demote_ripple": demote, "escalate_ripple": escalate,
        "load_bearing_demote": [{"node": n, "changed": c} for n, c in top(demote)],
        "load_bearing_escalate": [{"node": n, "changed": c} for n, c in top(escalate)],
        "nodes_whose_demote_changes_something": sum(1 for c in demote.values() if c > 0),
        "max_ripple": max(demote.values()) if demote else 0,
        "out_mis_escalate_medium": {
            "targets": KNOWN_OUT_MIS,
            "flipped_nodes": flipped,
            "flipped_count": len(flipped),
            "note": "把 7 个 OUT MIS 全部升到 medium（approve）后，翻转的节点集合",
        },
        "note": "只读敏感性：每个节点 demote/escalate 的判决级联规模；不改仓、不裁决",
    }


def render_report(a: dict) -> str:
    lines = [
        "# 611 E3 · 辩护链推理深化（全图敏感性 · 只读）", "",
        "> 对每个节点做 demote(压 low) / escalate(升 high) 压力测试，量化其「承重程度」。"
        "所有翻转只存在于内存重算，不改仓、不裁决。", "",
        "## 一、总览", "",
        f"- 节点 **{a['total_nodes']}** 个；有 {a['nodes_whose_demote_changes_something']} 个节点"
        f"被推翻时会引起其它判决翻转；最大级联 **{a['max_ripple']}** 个节点。",
        f"- OUT MIS 升 medium 的聚合影响：翻转 **{a['out_mis_escalate_medium']['flipped_count']}** 个节点"
        f"（详见 §三）。", "",
        "## 二、承重 Top 10", "",
        "### demote（压到 low 后翻转的节点数）", "",
        "| 节点 | 翻转数 |",
        "|---|---|",
        *[f"| `{r['node']}` | {r['changed']} |" for r in a["load_bearing_demote"]],
        "",
        "### escalate（升到 high 后翻转的节点数）", "",
        "| 节点 | 翻转数 |",
        "|---|---|",
        *[f"| `{r['node']}` | {r['changed']} |" for r in a["load_bearing_escalate"]],
        "",
        "## 三、OUT MIS 升 medium 的聚合影响（D1 全局版）", "",
        f"- 目标 7 个：`{', '.join(a['out_mis_escalate_medium']['targets'])}`",
        f"- 翻转节点 **{a['out_mis_escalate_medium']['flipped_count']}** 个："
        f"`{', '.join(a['out_mis_escalate_medium']['flipped_nodes'][:20]) or '—'}`",
        "- 含义：若人审把这些 MIS 的 modify 全部改 approve（升 medium），论证图会按此规模重排；"
        "是否采纳是**人审权力**（工具只呈现后果）。", "",
        "## 四、口径与边界", "",
        "- 复用 610 B1 `defense_chain.what_if` 全量重算内核（节点级可信度 + W2 grounded）；",
        "- 承重 = 单点压力测试下的级联规模，是「脆弱性」指标而非「重要性」判决；",
        "- **不改仓**：本分析不写 `human_attack_edge_annotations.jsonl` / `grounded_labels_w2.json`。", "",
    ]
    return "\n".join(lines)


def check(a: dict) -> list[str]:
    problems: list[str] = []
    if a["total_nodes"] != 121:
        problems.append(f"节点数应为 121（实测 {a['total_nodes']}）")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="defense_chain_deepen",
                                 description="611 E3 辩护链推理深化（全图敏感性）")
    ap.add_argument("--version", action="version", version=f"defense_chain_deepen {VERSION}")
    ap.add_argument("--stats", action="store_true", help="打印 JSON")
    ap.add_argument("--write", action="store_true", help=f"写 {REPORT_OUT.name}")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    res = analyze()
    if a.stats:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = check(res)
        if problems:
            for p in problems:
                print(f"[E3] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[E3] ✓ 辩护链深化锁定（节点 {res['total_nodes']} · "
              f"承重 {res['nodes_whose_demote_changes_something']} · "
              f"最大级联 {res['max_ripple']}）")
        return 0
    if a.write:
        REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
        REPORT_OUT.write_text(render_report(res), encoding="utf-8", newline="\n")
        print(f"[E3] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}"
              f"（节点 {res['total_nodes']} · 最大级联 {res['max_ripple']}）")
        return 0
    print(f"节点 {res['total_nodes']} · 承重 {res['nodes_whose_demote_changes_something']} · "
          f"最大级联 {res['max_ripple']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
