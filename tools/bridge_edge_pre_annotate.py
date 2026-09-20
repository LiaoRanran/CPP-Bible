"""612 A1 · 桥接候选人审预标注工具（**只读** · 不执行人审、不实际加边）。

读取 611 C2 的 98 条桥接候选（`data/bridge_edge_candidates_611.jsonl`），对每条基于三维度自动生成
**预标注建议**（主题相关性 / 论证关系强度 / 分量距离）→ 综合建议置信度 + 建议操作（approve/reject/modify）。
复算口径与 611 C2 同源（`bridge_edge_candidates.load_mis_index` + `argument_audit` 分量图）。

⚠️ 三维度说明（均只读、纯词频/结构，不调 LLM）：
  * 主题相关性：候选 `basis.topic_match`（同主题=high，否则=low）
  * 论证关系强度：两 MIS `refutations` 词频 Jaccard（>0.3=high，0.1-0.3=medium，<0.1=low）
  * 分量距离：两分量大小（都大=high，一大一小=medium，都小=low）
综合：置信度 high/medium/low（按三维度得分求和）；操作 modify 仅当三维度全 high（升 high），
否则 confidence≥medium ⇒ approve（升 medium），否则 reject。预标注只是建议，最终由人审决定。

CLI：`--write`（写 `data/bridge_edge_pre_annotation_612.md`）/ `--stats`（JSON）/ `--check`（exit 0=通过）。
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
CAND_IN = ROOT / "data" / "bridge_edge_candidates_611.jsonl"
REPORT_OUT = ROOT / "data" / "bridge_edge_pre_annotation_612.md"

# 611 C2 锁定：98 条候选
KNOWN_TOTAL = 98


def _tokens(text: str) -> set[str]:
    import re
    return {t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text or "")
            if len(t) > 1 and t.lower() not in
            {"main", "printf", "scanf", "malloc", "free", "cout", "cin", "endl", "int",
             "void", "char", "bool", "float", "double", "auto", "const", "static", "return"}}


def component_sizes() -> dict[int, int]:
    import bridge_edge_candidates as c2  # noqa: E402
    cm = c2.component_map()
    sizes: dict[int, int] = {}
    for v in cm.values():
        sizes[v] = sizes.get(v, 0) + 1
    return sizes


def _size_class(n: int) -> str:
    if n >= 40:
        return "large"
    if n < 10:
        return "small"
    return "medium"


def annotate(cands: list[dict] | None = None, sizes: dict[int, int] | None = None) -> list[dict]:
    import bridge_edge_candidates as c2  # noqa: E402
    if cands is None:  # 默认从 611 产物读取（不重算生成）
        cands = [json.loads(line) for line in CAND_IN.read_text(encoding="utf-8").splitlines() if line.strip()]
    if sizes is None:
        sizes = component_sizes()
    mi = c2.load_mis_index()
    out: list[dict] = []
    for c in cands:
        topic_rel = "high" if c["basis"]["topic_match"] else "low"
        a, b = c["source"], c["target"]
        ta = _tokens(" ".join(mi.get(a, {}).get("refutations", [])))
        tb = _tokens(" ".join(mi.get(b, {}).get("refutations", [])))
        j = (len(ta & tb) / len(ta | tb)) if (ta | tb) else 0.0
        arg_str = "high" if j > 0.3 else ("medium" if j >= 0.1 else "low")
        ca = sizes.get(c["components"][0], 0)
        cb = sizes.get(c["components"][1], 0)
        sc = _size_class(min(ca, cb)), _size_class(max(ca, cb))
        dist = "high" if sc == ("large", "large") else ("low" if sc == ("small", "small") else "medium")
        score = {"high": 2, "medium": 1, "low": 0}[topic_rel] \
                + {"high": 2, "medium": 1, "low": 0}[arg_str] \
                + {"high": 2, "medium": 1, "low": 0}[dist]
        conf = "high" if score >= 4 else ("medium" if score >= 2 else "low")
        # 建议操作：三维全 high ⇒ modify（升 high）；论证关系弱（low）=伪桥接 ⇒ reject；
        # 其余（confidence 非 low）⇒ approve（升 medium）。所有候选同主题，故论证强度是区分主轴。
        if topic_rel == arg_str == dist == "high":
            action = "modify"
        elif arg_str == "low":
            action = "reject"
        elif conf != "low":
            action = "approve"
        else:
            action = "reject"
        out.append({**c, "pre_annotation": {
            "topic_relevance": topic_rel, "argument_strength": arg_str,
            "component_distance": dist, "confidence": conf, "action": action,
            "jaccard": round(j, 4), "comp_sizes": [ca, cb]}})
    return out


def summarize(anns: list[dict]) -> dict:
    conf = Counter(a["pre_annotation"]["confidence"] for a in anns)
    act = Counter(a["pre_annotation"]["action"] for a in anns)
    pseudo = [a["edge_id"] for a in anns
              if a["pre_annotation"]["topic_relevance"] == "high"
              and a["pre_annotation"]["argument_strength"] == "low"]
    return {"version": VERSION, "total": len(anns),
            "by_confidence": dict(conf), "by_action": dict(act),
            "pseudo_bridge_count": len(pseudo), "pseudo_bridges": pseudo[:20]}


def render(anns: list[dict], summ: dict) -> str:
    L = ["# 612 A1 · 桥接候选人审预标注（只读 · 建议，不执行人审）", "",
         "> 三维度：主题相关性（同主题=high）/ 论证关系强度（refutations 词频 Jaccard）/ 分量距离（分量大小）。"
         "预标注只是**建议**，最终决策由人审做出；本工具不实际加边、不修数据。", "",
         "## 一、总览", "",
         f"- 候选 **{summ['total']}** 条；建议置信度：high "
         f"{summ['by_confidence'].get('high', 0)} / medium {summ['by_confidence'].get('medium', 0)} "
         f"/ low {summ['by_confidence'].get('low', 0)}",
         f"- 建议操作：approve（升 medium）{summ['by_action'].get('approve', 0)} · "
         f"reject（不采纳）{summ['by_action'].get('reject', 0)} · "
         f"modify（升 high）{summ['by_action'].get('modify', 0)}",
         f"- **伪桥接风险**：{summ['pseudo_bridge_count']} 条（主题相关但论证关系弱，加了也不构成击败）", "",
         "## 二、逐条预标注（节选 Top 30）", "",
         "| 优先级 | 候选边 | 主题 | 论证 | 分量距离 | 置信度 | 建议操作 |",
         "|---|---|---|---|---|---|---|"]
    for a in anns[:30]:
        pa = a["pre_annotation"]
        L.append(f"| {a['priority']} | `{a['edge_id']}` | {pa['topic_relevance']} | "
                 f"{pa['argument_strength']} | {pa['component_distance']} | {pa['confidence']} | {pa['action']} |")
    if len(anns) > 30:
        L.append(f"| … | 其余 {len(anns) - 30} 条见 JSON / 报告 | | | | | |")
    L += ["", "## 三、口径与边界", "",
          "- **只读**：不写 `data/attack_edges_candidates.jsonl`、不修改任何数据文件；",
          "- **不保证成立**：预标注是「可能」的攻击关系，真正成立与否需人审 + replay 证据（见 A2/A3）；",
          "- **伪桥接**：主题相关但论证关系弱的候选，加了也只在结构上连起来，不构成击败（C3 已证加桥判决变化 0）；",
          "- 与 611 C2 同源；论证图一变即须重看。", ""]
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="bridge_edge_pre_annotate", description="612 A1 桥接预标注（只读）")
    ap.add_argument("--version", action="version", version=f"bridge_edge_pre_annotate {VERSION}")
    ap.add_argument("--stats", action="store_true", help="打印 JSON")
    ap.add_argument("--write", action="store_true", help=f"写 {REPORT_OUT.name}")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    anns = annotate()
    summ = summarize(anns)
    if a.stats:
        print(json.dumps({"summary": summ, "annotations": anns}, ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = []
        if summ["total"] != KNOWN_TOTAL:
            problems.append(f"候选总数应为 {KNOWN_TOTAL}（实测 {summ['total']}）")
        # 置信度不应全 high 或全 low
        conf = summ["by_confidence"]
        if len(conf) <= 1:
            problems.append("置信度分布退化（不应全是同一档）")
        if problems:
            for p in problems:
                print(f"[A1] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[A1] ✓ 预标注锁定（{summ['total']} 条；置信度 {summ['by_confidence']}；"
              f"伪桥接 {summ['pseudo_bridge_count']}）")
        return 0
    if a.write:
        REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
        REPORT_OUT.write_text(render(anns, summ), encoding="utf-8", newline="\n")
        print(f"[A1] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}（{summ['total']} 条；"
              f"置信度 {summ['by_confidence']}）")
        return 0
    print(f"候选 {summ['total']} · 置信度 {summ['by_confidence']} · 操作 {summ['by_action']} · "
          f"伪桥接 {summ['pseudo_bridge_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
