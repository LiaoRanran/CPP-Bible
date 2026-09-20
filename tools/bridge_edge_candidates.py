"""611 C2 · 桥接攻击边候选生成（**只读** · 不执行人审）。

问题：611 C1 实测论证图**碎片化**——11 个连通分量、最大只覆盖 66.1%。碎片之间彼此孤立，
跨主题的辩护链在结构上无法成立。本工具为"补桥"提供**候选集**（哪些不同分量的节点可能该有攻击边），
依据三路关联：

  * **MIS related_atoms 关联**：两个 MIS 的 `related_atoms` 有交集（同领域原子卡）⇒ 可能互相攻击；
  * **主题相似度**：两 MIS 同主题（id 第二前缀，如 `MIS-MEM-*`）；
  * **证据卡关联**：两 MIS 的 `refutations` 文本都提到同一张 `ATOM-*` / `EV-*` 卡。

⚠️ 硬边界（本工具价值全在"不做"上）：
  1. **只读**：不写权威边文件 `data/attack_edges_candidates.jsonl`、不执行人审（人审权在用户）；
  2. 候选只是"补边提示"，方向/是否真成立由人裁定；落库须另行开批；
  3. 复算口径与 C1 同源（`argument_audit` 的 BFS + `defense_chain` 的同一真源），结构一变即重看。

CLI：`--stats`（JSON）/ `--write`（写 `data/bridge_edge_candidates_611.jsonl` + `.md`）/ `--check`。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
CAND_OUT = ROOT / "data" / "bridge_edge_candidates_611.jsonl"
REPORT_OUT = ROOT / "data" / "bridge_edge_candidates_611.md"

# 611 C2 锁定已知事实（候选数由静态卡数据 + 冻结图结构决定，论证图未重构前不变）
KNOWN = {"total": 98, "strong": 0, "medium": 0, "weak": 98,
         "components_before": 11, "largest_before": 80}

_EVID_RX = re.compile(r"(?:ATOM|EV)-[A-Za-z0-9][A-Za-z0-9-]*")
_PROP_RX = re.compile(r"::prop-\d+")
_MIS_SEP = re.compile(r"-")


def topic_of(mis_id: str) -> str:
    """MIS 主题 = id 第二前缀（如 `MIS-MEM-001` → `MEM`）。"""
    parts = mis_id.split("-")
    return parts[1] if len(parts) >= 2 else mis_id


def evidence_tokens(refutations: list[str]) -> set[str]:
    """从 refutations 文本里抽取提到的 `ATOM-*` / `EV-*` 卡号。"""
    out: set[str] = set()
    for text in refutations:
        if not text:
            continue
        out.update(_EVID_RX.findall(text))
    return out


def load_mis_index() -> dict[str, dict]:
    """→ {mis_id: {related_atoms, refutations, topic, evidence}}。复用 596/攻击边生成器的读取面。"""
    import attack_edge_generator as aeg  # noqa: E402
    mis = aeg.read_mis()
    out: dict[str, dict] = {}
    for mid, info in mis.items():
        out[mid] = {
            "related_atoms": list(info.get("related_atoms") or []),
            "refutations": list(info.get("refutations") or []),
            "topic": topic_of(mid),
            "evidence": sorted(evidence_tokens(info.get("refutations") or [])),
        }
    return out


def component_map(edges_path=None, ann_path=None) -> dict[str, int]:
    """→ {node: 分量下标}（忽略方向 BFS，与 C1 同源）。"""
    import argument_audit as aa  # noqa: E402
    edges, verdicts, _cred = aa.load_state(edges_path, ann_path)
    nodes = aa.all_nodes(verdicts, edges)
    comps = aa.detect_isolated_subgraphs(edges, nodes)
    m: dict[str, int] = {}
    for i, c in enumerate(comps):
        for n in c:
            m[n] = i
    return m


def generate_candidates(mis_index: dict[str, dict], comp_map: dict[str, int]) -> list[dict]:
    """为跨分量 MIS 对生成桥接候选（排序确定）。

    关联打分：shared_atoms*2 + shared_evidence*1 + (1 if topic_match else 0)；
    候选条件 = 跨分量 且（shared_atoms≥1 或 shared_evidence≥1 或 topic_match）。
    优先级：strong(有共享原子) / medium(仅共享证据) / weak(仅同主题)。
    """
    mis_ids = sorted(mid for mid in mis_index if mid in comp_map)
    seen: set[tuple[str, str]] = set()
    cands: list[dict] = []
    for i in range(len(mis_ids)):
        a = mis_ids[i]
        ia = mis_index[a]
        for j in range(i + 1, len(mis_ids)):
            b = mis_ids[j]
            ib = mis_index[b]
            ca, cb = comp_map[a], comp_map[b]
            if ca == cb:
                continue                      # 同分量无需桥接
            shared_atoms = sorted(set(ia["related_atoms"]) & set(ib["related_atoms"]))
            shared_ev = sorted(set(ia["evidence"]) & set(ib["evidence"]))
            topic_match = ia["topic"] == ib["topic"]
            if not (shared_atoms or shared_ev or topic_match):
                continue
            key = (a, b) if a < b else (b, a)
            if key in seen:
                continue
            seen.add(key)
            priority = "strong" if shared_atoms else ("medium" if shared_ev else "weak")
            cands.append({
                "edge_id": f"bridge-{key[0]}->{key[1]}",
                "source": key[0], "target": key[1],
                "kind": "bridge", "direction": "mis_to_mis",
                "priority": priority,
                "components": sorted([ca, cb]),
                "basis": {
                    "shared_atoms": shared_atoms,
                    "shared_evidence": shared_ev,
                    "topic_match": topic_match,
                    "topic": ia["topic"],
                },
                "note": "候选桥接边（跨分量）；方向/是否真成立由人裁定，不执行人审",
            })
    cands.sort(key=lambda c: ({"strong": 0, "medium": 1, "weak": 2}[c["priority"]],
                              c["source"], c["target"]))
    return cands


def summarize(cands: list[dict]) -> dict:
    cnt = Counter(c["priority"] for c in cands)
    comp_pairs = Counter(tuple(c["components"]) for c in cands)
    return {
        "version": VERSION,
        "total": len(cands),
        "by_priority": {"strong": cnt.get("strong", 0), "medium": cnt.get("medium", 0),
                        "weak": cnt.get("weak", 0)},
        "distinct_component_pairs": len(comp_pairs),
        "top_component_pairs": [{"pair": list(k), "bridges": v}
                                for k, v in comp_pairs.most_common(8)],
    }


def render_report(cands: list[dict], summ: dict, comp_map: dict[str, int]) -> str:
    ncomp = len({v for v in comp_map.values()})
    lines = [
        "# 611 C2 · 桥接攻击边候选（只读 · 不执行人审）", "",
        "> 候选生成依据：MIS `related_atoms` 关联 + 主题相似度 + 证据卡关联。"
        "候选**只作补边提示**，不写权威边文件、不执行人审。", "",
        "## 一、总览", "",
        f"- 候选桥接边 **{summ['total']}** 条："
        f"strong（共享原子）**{summ['by_priority']['strong']}** · "
        f"medium（共享证据）{summ['by_priority']['medium']} · "
        f"weak（同主题）{summ['by_priority']['weak']}",
        f"- 涉及 **{summ['distinct_component_pairs']}** 对跨分量节点 · "
        f"当前图 {ncomp} 个连通分量（C1 锁定：11 / 最大 80 / 覆盖 66.1%）",
        "- 生成命令：`tools/bridge_edge_candidates.py --write`", "",
        "## 二、候选明细（节选 Top 30）", "",
        "| 优先级 | 候选边 | 连接分量 | 共享原子 | 共享证据 | 同主题 |",
        "|---|---|---|---|---|---|",
    ]
    for c in cands[:30]:
        b = c["basis"]
        lines.append(
            f"| {c['priority']} | `{c['edge_id']}` | "
            f"{c['components'][0]}↔{c['components'][1]} | "
            f"{', '.join(b['shared_atoms'][:4]) or '—'} | "
            f"{', '.join(b['shared_evidence'][:4]) or '—'} | "
            f"{'是' if b['topic_match'] else '否'} |")
    if len(cands) > 30:
        lines.append(f"| … | 其余 {len(cands) - 30} 条见 `data/bridge_edge_candidates_611.jsonl` | | | | |")
    lines += ["", "## 三、口径与边界", "",
              "- **只读**：不写 `data/attack_edges_candidates.jsonl`、不执行人审；候选落库须另行开批；",
              "- **方向未定**：`mis_to_mis` 候选的可能攻击方向（谁攻谁）由人裁定；",
              "- **不保证成立**：关联只说明「可能」有攻击关系，真正成立与否需人审 + replay 证据；",
              "- 与 C1 同源（`argument_audit.detect_isolated_subgraphs` + `defense_chain` 真源）；"
              "论证图一变（如真补了桥）即须重看碎片化是否改善（C3）。", ""]
    return "\n".join(lines)


def check(cands: list[dict]) -> list[str]:
    problems: list[str] = []
    summ = summarize(cands)
    if KNOWN["total"] is not None and summ["total"] != KNOWN["total"]:
        problems.append(f"候选总数应为 {KNOWN['total']}（实测 {summ['total']}）")
    if KNOWN["strong"] is not None and summ["by_priority"]["strong"] != KNOWN["strong"]:
        problems.append(f"strong 候选应为 {KNOWN['strong']}（实测 {summ['by_priority']['strong']}）")
    if KNOWN["medium"] is not None and summ["by_priority"]["medium"] != KNOWN["medium"]:
        problems.append(f"medium 候选应为 {KNOWN['medium']}（实测 {summ['by_priority']['medium']}）")
    if KNOWN["weak"] is not None and summ["by_priority"]["weak"] != KNOWN["weak"]:
        problems.append(f"weak 候选应为 {KNOWN['weak']}（实测 {summ['by_priority']['weak']}）")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="bridge_edge_candidates",
                                 description="611 C2 桥接攻击边候选生成（只读）")
    ap.add_argument("--version", action="version", version=f"bridge_edge_candidates {VERSION}")
    ap.add_argument("--stats", action="store_true", help="打印 JSON 摘要")
    ap.add_argument("--write", action="store_true", help=f"写 {CAND_OUT.name} + {REPORT_OUT.name}")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    mis_index = load_mis_index()
    comp_map = component_map()
    cands = generate_candidates(mis_index, comp_map)
    summ = summarize(cands)
    if a.stats:
        print(json.dumps({"summary": summ, "candidates": cands}, ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = check(cands)
        if problems:
            for p in problems:
                print(f"[C2] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[C2] ✓ 桥接候选锁定（{summ['total']} 条："
              f"strong {summ['by_priority']['strong']} / "
              f"medium {summ['by_priority']['medium']} / "
              f"weak {summ['by_priority']['weak']}）")
        return 0
    if a.write:
        CAND_OUT.parent.mkdir(parents=True, exist_ok=True)
        CAND_OUT.write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in cands) + "\n",
                            encoding="utf-8", newline="\n")
        REPORT_OUT.write_text(render_report(cands, summ, comp_map), encoding="utf-8", newline="\n")
        print(f"[C2] 已写 {CAND_OUT.relative_to(ROOT).as_posix()}（{summ['total']} 条）"
              f" + {REPORT_OUT.relative_to(ROOT).as_posix()}")
        return 0
    print(f"候选 {summ['total']} · strong {summ['by_priority']['strong']} · "
          f"medium {summ['by_priority']['medium']} · weak {summ['by_priority']['weak']} · "
          f"跨分量对 {summ['distinct_component_pairs']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
