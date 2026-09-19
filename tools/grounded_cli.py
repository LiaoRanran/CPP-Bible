"""609 C3 · 论证 CLI：`status` / `proposition` / `mis` / `card` / `defense` / `--check`。

前四个是"看"，`defense` 是"**为什么**"——把一条命题为什么 IN、谁攻击了它、为什么那些
攻击者被打败、谁在给它辩护，**精确到边级**写成 Markdown（边 id 形如 `ae-<source>-><target>`）。

辩护链的四段（缺任何一段都要明写"无"，不许留白让人脑补）：
  * `攻击它的边`（`attackers` 全集，含不构成击败的"有边无击败"）
  * `其中真构成击败的`（`defeated_attackers`：可信度严格大于才成立）
  * `被它打败的攻击者`（`defeated_attackers` 的反向：它对这些攻击者构成击败）
  * `为它辩护的节点`（`defenders`：IN 且攻击它的某个攻击者）

CLI：
    status                                  判决分布总览
    proposition <id>                        单命题详情
    mis <id>                                单误解详情
    card <card>                             按证据卡反查节点
    defense <id>                            辩护链 Markdown（边级）
    --check                                 0 文档结构合法 / 1 破
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import attack_edge_generator as aeg  # noqa: E402

VERSION = "1.0"
DEFAULT_LABELS = ROOT / "data" / "grounded_labels_w2.json"
DEFAULT_EDGES = aeg.DEFAULT_OUT


def load_doc(path: Path | str = DEFAULT_LABELS) -> dict:
    p = Path(path)
    if not p.is_file():
        raise SystemExit(f"[cli] 标注文档不存在：{p}（先跑 weighted_af_solver.py solve）")
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise SystemExit(f"[cli] 标注文档不是合法 JSON：{exc}") from exc
    if not isinstance(doc.get("nodes"), dict) or not doc["nodes"]:
        raise SystemExit("[cli] 标注文档 nodes 为空 ⇒ 拒绝出结论（不许拿空文档糊人）")
    return doc


def load_edges(path: Path | str = DEFAULT_EDGES) -> list[dict]:
    return aeg.load_edges(path)


def edge_ids_for(nodes: dict[str, dict], node_id: str, edges: list[dict]) -> list[str]:
    """某节点涉及的候选边 id（`ae-<source>-><target>` 全集里挑出它当端点/目标的）。"""
    out = []
    for e in edges:
        s, t = str(e["source"]), str(e["target"])
        if s == node_id or t == node_id:
            out.append(str(e["id"]))
    return sorted(out)


def render_status(doc: dict) -> str:
    s = doc["summary"]
    lines = [f"# 论证状态（W2 · {doc.get('model')}）", "",
             f"- 节点 **{s['nodes']}**（命题 {s['IN_propositions']} IN · "
             f"误解 {s['IN_misconceptions']} IN）",
             f"- IN **{s['IN']}** / OUT **{s['OUT']}** / UNDEC **{s['UNDEC']}**",
             f"- 击败边 {doc.get('defeating_edges')}/{doc.get('edges')} · "
             f"{doc.get('rounds')} 轮收敛",
             f"- 可信度档位 {doc.get('credibility_levels')}", ""]
    for nid in sorted(doc["nodes"]):
        v = doc["nodes"][nid]
        lines.append(f"  - `{nid}` [{v['type']}] **{v['label']}**"
                     f"（cred {v['credibility']}, attackers {len(v['attackers'])}, "
                     f"defenders {len(v['defenders'])}）")
    return "\n".join(lines) + "\n"


def _detail(doc: dict, node_id: str, edges: list[dict], *, want_type: str | None = None) -> str:
    v = doc["nodes"].get(node_id)
    if v is None:
        return f"（节点不存在：{node_id}）\n"
    if want_type and v["type"] != want_type:
        return (f"（{node_id} 是 {v['type']}，不是 {want_type} ⇒ 换个 id 或换子命令）\n")
    eids = edge_ids_for(doc["nodes"], node_id, edges)
    lines = [f"# {node_id}", "",
             f"- 类型：{v['type']} · 判决：**{v['label']}** · "
             f"可信度 {v['confidence']}（credibility {v['credibility']}）"]
    if v.get("card"):
        lines.append(f"- 证据卡：`{v['card']}`（claim_type {v.get('claim_type')}）")
    lines += [
        f"- 攻击者 {len(v['attackers'])}：`{', '.join(v['attackers'][:12])}`"
        + ("…" if len(v["attackers"]) > 12 else ""),
        f"- 被它击败的攻击者 {len(v['defeated_attackers'])}："
        f"`{', '.join(v['defeated_attackers'][:12])}`",
        f"- 辩护者 {len(v['defenders'])}：`{', '.join(v['defenders'][:12])}`",
        f"- 涉及候选边 {len(eids)} 条（前 5）：`{', '.join(eids[:5])}`",
    ]
    return "\n".join(lines) + "\n"


def render_card(doc: dict, card: str) -> str:
    hits = [nid for nid, v in sorted(doc["nodes"].items()) if v.get("card") == card]
    if not hits:
        return f"（没有节点挂在证据卡 {card} 上）\n"
    lines = [f"# 证据卡 {card} 的节点", ""]
    for nid in hits:
        v = doc["nodes"][nid]
        lines.append(f"- `{nid}` [{v['type']}] **{v['label']}**"
                     f"（attackers {len(v['attackers'])}, defenders {len(v['defenders'])}）")
    return "\n".join(lines) + "\n"


def render_defense(doc: dict, node_id: str, edges: list[dict]) -> str:
    """辩护链 Markdown：**精确到边级**（每条边都给 `ae-<source>-><target>` id）。"""
    v = doc["nodes"].get(node_id)
    if v is None:
        return f"（节点不存在：{node_id}）\n"
    by_id = {str(e["id"]): e for e in edges}

    def eid(a: str, b: str) -> str:            # 与 attack_edge_generator 的 id 口径一致
        return f"ae-{a}->{b}"
    lines = [f"# 辩护链 · {node_id}", "",
             f"判决：**{v['label']}** · 可信度 {v['confidence']}（credibility "
             f"{v['credibility']}）", "",
             "## 1. 攻击它的边（全部攻击边，含不构成击败的）"]
    if v["attackers"]:
        for a in sorted(v["attackers"]):
            e = by_id.get(eid(a, node_id))
            conf = e.get("confidence") if e else "?"
            lines.append(f"- `{eid(a, node_id)}`：`{a}` → `{node_id}`"
                         f"（源可信度 {conf} ⇒ 比目标 {v['confidence']} "
                         f"{'高 ⇒ 构成击败' if (e and e.get('confidence') and e.get('confidence') != v['confidence']) else '—— 见下条判定'}）")
    else:
        lines.append("- 无攻击者 ⇒ 立即 IN（grounded 最小不动点）")
    lines += ["", "## 2. 其中真构成击败的（`defeated_attackers`：可信度**严格大于**才成立）"]
    lines += [f"- `{eid(a, node_id)}`：`{a}` 真的击败 `{node_id}`" for a in
              sorted(v["defeated_attackers"])] or ["- 无"]
    lines += ["", "## 3. 它反过来击败的攻击者"]
    lines += [f"- `{eid(node_id, a)}`：`{node_id}` 击败 `{a}`" for a in
              sorted(v.get("defeated_attackers", ()))] or ["- 无"]
    lines += ["", "## 4. 为它辩护的节点（IN 且攻击它的某个攻击者）"]
    lines += [f"- `{d}` → 攻击 `{node_id}` 的某个攻击者 ⇒ 为 `{node_id}` 辩护"
              for d in sorted(v["defenders"])] or ["- 无（无人替它挡）"]
    lines += ["", ("⚠️ 注：第 3、4 段来自 `weighted_af_solver` 的 `defenders` / "
                   "`defeated_attackers` 字段；两者都是**在击败关系上**算出来的，"
                   "不构成击败的攻击不算攻击（W2 语义，596 实测踩过坑）。")]
    return "\n".join(lines) + "\n"


def check(path: Path | str = DEFAULT_LABELS) -> list[str]:
    problems: list[str] = []
    if not Path(path).is_file():
        return [f"标注文档不存在：{path}"]
    doc = load_doc(path)
    for nid, v in doc["nodes"].items():
        if v.get("label") not in ("IN", "OUT", "UNDEC"):
            problems.append(f"{nid} 判决非法：{v.get('label')!r}")
        if v.get("type") not in ("proposition", "misconception"):
            problems.append(f"{nid} 类型非法：{v.get('type')!r}")
        if not set(("attackers", "defenders", "defeated_attackers")) <= set(v):
            problems.append(f"{nid} 缺辩护链字段（attackers/defenders/defeated_attackers）")
    s = doc.get("summary", {})
    if s.get("nodes") != len(doc["nodes"]):
        problems.append("summary.nodes 与实际节点数不一致")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="grounded_cli",
                                 description="609 C3 论证 CLI（status/proposition/mis/card/defense）")
    ap.add_argument("--version", action="version", version=f"grounded_cli {VERSION}")
    ap.add_argument("--labels", default=str(DEFAULT_LABELS))
    ap.add_argument("--edges", default=str(DEFAULT_EDGES))
    ap.add_argument("--check", action="store_true")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("status")
    sp = sub.add_parser("proposition")
    sp.add_argument("node_id")
    sp = sub.add_parser("mis")
    sp.add_argument("node_id")
    sp = sub.add_parser("card")
    sp.add_argument("card")
    sp = sub.add_parser("defense")
    sp.add_argument("node_id")
    a = ap.parse_args(argv)

    if a.check:
        problems = check(a.labels)
        if problems:
            print(f"[cli] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        print(f"[cli] --check OK：{Path(a.labels).name} 结构合法"
              f"（节点 {len(load_doc(a.labels)['nodes'])}）")
        return 0

    if a.cmd is None:
        ap.print_help()
        return 2

    doc = load_doc(a.labels)
    edges = load_edges(a.edges)
    if a.cmd == "status":
        print(render_status(doc), end="")
    elif a.cmd == "proposition":
        print(_detail(doc, a.node_id, edges, want_type="proposition"), end="")
    elif a.cmd == "mis":
        print(_detail(doc, a.node_id, edges, want_type="misconception"), end="")
    elif a.cmd == "card":
        print(render_card(doc, a.card), end="")
    else:
        print(render_defense(doc, a.node_id, edges), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
