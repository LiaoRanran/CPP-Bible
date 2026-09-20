"""611 D1 · OUT 的 7 个 MIS 复核工具支持（**只读** · 不执行人审）。

问题：W2 把 7 个 MIS 判为 OUT（IN114/OUT7），且这 7 个的全部攻击边都是 `modify`（保持 low）
⇒ 它们被命题辩护链击败。是否该把某些 `modify` 改 `approve`（升 medium）是人审权力。
本工具**不裁决**，只把"复核所需的全部事实"结构化地摆出来，支持人逐条复核：

  * 每个 OUT MIS 的攻击者（边 id / 人审 action / 是否构成击败 / 方向）；
  * 它的辩护者（谁在替它挡刀）；
  * **决策支撑**：若把它的全部攻击边升到 approve（medium），它的判决会怎么变
    （`defense_chain.what_if` 全量重算，不改仓）——供人判断"改 approve 的后果"。

⚠️ 只读：不写 `human_attack_edge_annotations.jsonl`、不调人审接口、不落库任何判决。

CLI：`--stats`（JSON）/ `--write`（写 `data/out_mis_review_support_611.md`）/ `--check`。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
REPORT_OUT = ROOT / "data" / "out_mis_review_support_611.md"

# 611 D1 锁定的 7 个 OUT MIS（与 data/grounded_labels_w2.json + 610 实测一致）
KNOWN_OUT_MIS = ["MIS-LANG-001", "MIS-MEM-001", "MIS-MEM-003", "MIS-UB-001",
                 "MIS-UB-004", "MIS-UB-008", "MIS-UB-014"]


def analyze(edges_path=None, ann_path=None) -> dict:
    import defense_chain as dc  # noqa: E402
    edges, verdicts, cred = dc.load_data(edges_path, ann_path)
    out_nodes = sorted(n for n, v in verdicts.items() if v == "OUT")
    rows: list[dict] = []
    for n in KNOWN_OUT_MIS:
        if n not in verdicts or verdicts[n] != "OUT":
            rows.append({"mis_id": n, "present": False})
            continue
        ch = dc.get_defense_chain(n, edges, verdicts, cred)
        attackers = []
        for e in sorted(ch.attackers, key=lambda x: x.source):
            attackers.append({
                "edge_id": e.edge_id, "source": e.source, "target": e.target,
                "human_verdict": e.human_verdict, "is_defeating": e.is_defeating,
                "kind": e.kind,
            })
        # 决策支撑：把它的全部攻击边升到 medium 后，它的判决如何变
        cred2 = dict(cred)
        for e in ch.attackers:
            mis_end = e.source if e.kind == "mis_to_prop" else e.target
            cred2[mis_end] = "medium"
        # 仅改这条 MIS 相关端点即可（升它自己 + 它攻击的命题？这里升攻击者 MIS 端点）
        # 更稳妥：用 what_if 对"每条攻击边对应攻击者 MIS"分别升 —— 但整组升更能反映"全 approve"后果
        v2 = dc.solve_verdicts(edges, cred2)
        rows.append({
            "mis_id": n, "present": True, "credibility": ch.credibility,
            "verdict": ch.verdict, "attackers": attackers,
            "defenders": sorted(ch.defenders, key=lambda x: x.source),
            "defeated_by": ch.defeated_by, "w2_defenders": ch.w2_defenders,
            "n_attackers": len(attackers),
            "n_modify": sum(1 for e in attackers if e["human_verdict"] == "modify"),
            "n_approve": sum(1 for e in attackers if e["human_verdict"] == "approve"),
            "if_all_approve_verdict": v2.get(n),
        })
    return {"out_mis_count": len([r for r in rows if r.get("present")]),
            "out_nodes_total": len(out_nodes), "rows": rows,
            "note": "只读：不裁决、不写人审、不落库；if_all_approve_verdict 为 what-if 重算（不改仓）"}


def render_report(a: dict) -> str:
    lines = [
        "# 611 D1 · OUT 的 7 个 MIS 复核支撑（只读）", "",
        "> 仅把「复核所需事实」结构化摆出，不裁决、不写人审、不落库判决。"
        "每行的 `if_all_approve_verdict` 是 what-if 重算（把该 MIS 全部攻击边升 medium），供人判断后果。", "",
        "## 一、总览", "",
        f"- OUT MIS（本工具锁定）**{a['out_mis_count']}** 个；全图 OUT 节点共 {a['out_nodes_total']} 个；",
        "- 这 7 个的全部攻击边都是 `modify`（保持 low）⇒ 被命题辩护链击败；", "",
        "## 二、逐 MIS 复核明细", "",
    ]
    for r in a["rows"]:
        if not r.get("present"):
            lines.append(f"### `{r['mis_id']}` ⚠️ 不在 OUT 判决中（口径漂移？）")
            continue
        lines.append(f"### `{r['mis_id']}`（cred {r['credibility']} · 现 OUT）")
        lines.append("")
        lines.append(f"- 攻击者 **{r['n_attackers']}** 条：approve {r['n_approve']} / "
                     f"modify **{r['n_modify']}** / reject 0")
        lines.append(f"- 被击败者（决定它 OUT）：`{', '.join(r['defeated_by']) or '—'}`")
        lines.append(f"- W2 辩护者：`{', '.join(r['w2_defenders']) or '—'}`")
        lines.append(f"- **若把全部攻击边升 approve（medium）⇒ 判决变为 `{r['if_all_approve_verdict']}`**")
        lines.append("")
        lines.append("| 边 id | 攻击者→目标 | 人审 | 构成击败 | 方向 |")
        lines.append("|---|---|---|---|---|")
        for e in r["attackers"]:
            lines.append(f"| `{e['edge_id']}` | `{e['source']}`→`{e['target']}` | "
                         f"{e['human_verdict']} | {'✅' if e['is_defeating'] else '—'} | {e['kind']} |")
        lines.append("")
    lines += ["## 三、口径与边界", "",
              "- **不改仓**：本工具是复核「看板」，所有判决变化仅存在于 what-if 重算的内存里；",
              "- **人审权力**：是否把 `modify` 改为 `approve` 由用户逐条裁定（可能翻盘 OUT→IN）；",
              "- 与 610 P0 口径冲突（keep-low vs upgrade-medium）无关：本工具按入库权威 keep-low 口径读现状。",
              ""]
    return "\n".join(lines)


def check(a: dict) -> list[str]:
    problems: list[str] = []
    if a["out_mis_count"] != len(KNOWN_OUT_MIS):
        problems.append(f"OUT MIS 应为 {len(KNOWN_OUT_MIS)}（实测 {a['out_mis_count']}）")
    missing = [r["mis_id"] for r in a["rows"] if not r.get("present")]
    if missing:
        problems.append(f"锁定的 OUT MIS 不在 OUT 判决中：{missing}（口径漂移）")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="out_mis_review_support",
                                 description="611 D1 OUT MIS 复核支撑（只读）")
    ap.add_argument("--version", action="version", version=f"out_mis_review_support {VERSION}")
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
                print(f"[D1] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[D1] ✓ OUT MIS 复核支撑锁定（{res['out_mis_count']} 个 OUT MIS 全部在位）")
        return 0
    if a.write:
        REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
        REPORT_OUT.write_text(render_report(res), encoding="utf-8", newline="\n")
        print(f"[D1] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}"
              f"（{res['out_mis_count']} 个 OUT MIS 复核明细）")
        return 0
    print(f"OUT MIS {res['out_mis_count']} 个 · 全图 OUT {res['out_nodes_total']} 个")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
