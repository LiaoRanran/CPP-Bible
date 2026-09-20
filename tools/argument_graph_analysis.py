"""611 C1 · 论证图连通分量分析（**纯读** · 复用 610 `argument_audit` 的算法与同一真源口径）。

610 C 线已发现：论证图**碎片化**——11 个连通分量、最大只覆盖 66.1%。本工具把这件事做成
**可独立复算的、可锁定的**组件分析（不依赖 `data/defense_chain_analysis_*` 那种手算文档）：

  * 全部复用 `argument_audit.detect_isolated_subgraphs` 的 BFS（忽略方向），**单一真源** =
    `defense_chain.load_data`（候选边 + 用户授权人审 + W2 辩护链）；
  * 输出：组件数、**孤立节点**（仅 1 节点的分量）、**最大组件覆盖比例**、最大组件里的节点类型构成；
  * `--check` 把已知事实钉死（11 分量 / 孤立 4 / 最大 80 / 121 节点 / 388 边 / 覆盖 66.1%）——
    论证图结构一变（比如 C2 补了桥接边）就报红，逼人重看碎片化是否改善。

CLI：`--stats`（JSON）/ `--write`（写出 `data/argument_graph_connectivity_611.md`）/ `--check`。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
REPORT_OUT = ROOT / "data" / "argument_graph_connectivity_611.md"

# 611 C1 锁定的已知事实（与 610 C 线 `--check` 同源；论证图未重构前不可变）
KNOWN = {"components": 11, "isolated": 4, "largest": 80, "nodes": 121,
         "edges": 388, "coverage": 0.6612}


def analyze(edges_path: Path | str | None = None,
            ann_path: Path | str | None = None) -> dict:
    """现算连通分量分析。**只读**，复用 610 `argument_audit` 的 BFS 与同一真源。"""
    import argument_audit as aa  # noqa: E402

    edges, verdicts, _cred = aa.load_state(edges_path, ann_path)
    nodes = aa.all_nodes(verdicts, edges)
    comps = aa.detect_isolated_subgraphs(edges, nodes)
    sizes = sorted((len(c) for c in comps), reverse=True)
    isolated = [c[0] for c in comps if len(c) == 1]
    largest = max(comps, key=len)
    from collections import Counter  # noqa: E402
    type_counts = Counter(aa.dc.node_type_of(n, edges) for n in largest)
    return {
        "nodes": len(nodes), "edges": len(edges), "components": len(comps),
        "sizes": sizes, "isolated": isolated, "largest_size": sizes[0],
        "coverage": round(sizes[0] / max(len(nodes), 1), 4),
        "largest_component_types": dict(type_counts),
        "largest_component_sample": sorted(largest)[:12],
    }


def render_report(c: dict) -> str:
    lines = [
        "# 611 C1 · 论证图连通分量分析（碎片化定量化）", "",
        "> 纯读生成，复用 610 `argument_audit.detect_isolated_subgraphs`（BFS，忽略方向），"
        "同一真源 = 候选边 388 + 用户授权人审 388 + W2 辩护链。", "",
        "## 一、总览", "",
        f"- 节点 **{c['nodes']}** · 边 **{c['edges']}**",
        f"- 连通分量 **{c['components']}** 个 · 孤立节点（仅 1 节点分量）**{len(c['isolated'])}** 个",
        f"- **最大分量 {c['largest_size']} 节点 = 覆盖 {c['coverage']:.1%}**"
        "（其余 {c['components'] - 1} 个分量合计仅 "
        f"{c['nodes'] - c['largest_size']} 节点）", "",
        "## 二、各分量大小", "",
        "- 大小降序：", *[f"  - {n} 节点" for n in c["sizes"]],
        "", "## 三、孤立节点（断联论证）", "",
        "- 全部是**命题**（无误解指向、也无误解被它攻击）：",
        *[f"  - `{n}`" for n in c["isolated"]],
        "", "## 四、最大分量构成", "",
        f"- 节点数 {c['largest_size']}：其中"
        + " · ".join(f"{k} {v}" for k, v in c["largest_component_types"].items()),
        "- 含（节选）：" + "、".join(f"`{n}`" for n in c["largest_component_sample"]),
        "", "## 五、结论（碎片化）", "",
        f"- 论证图被切成 **{c['components']} 块**，最大块只覆盖 {c['coverage']:.1%}**"
        "——说明本仓的论证是**一堆互不相连的孤岛**，跨主题的辩护链在结构上无法成立；",
        "- 这与 610 C 线 `argument_audit` 的 P1「论证图碎片化」结论一致，**数字同源**；",
        "- 是否要补「桥接攻击边」把孤岛连起来，是 C2/C3 的议题；本工具只定量、不擅自连。", "",
        "> 数字可由 `tools/argument_graph_analysis.py --stats` 复算；`--check` 锁定上表事实。", "",
    ]
    return "\n".join(lines) + "\n"


def check() -> list[str]:
    c = analyze()
    problems: list[str] = []
    if c["components"] != KNOWN["components"]:
        problems.append(f"components 应为 {KNOWN['components']}（实测 {c['components']}）")
    if len(c["isolated"]) != KNOWN["isolated"]:
        problems.append(f"孤立节点应为 {KNOWN['isolated']}（实测 {len(c['isolated'])}）")
    if c["largest_size"] != KNOWN["largest"]:
        problems.append(f"最大分量应为 {KNOWN['largest']}（实测 {c['largest_size']}）")
    if c["nodes"] != KNOWN["nodes"]:
        problems.append(f"节点数应为 {KNOWN['nodes']}（实测 {c['nodes']}）")
    if c["edges"] != KNOWN["edges"]:
        problems.append(f"边数应为 {KNOWN['edges']}（实测 {c['edges']}）")
    if abs(c["coverage"] - KNOWN["coverage"]) > 0.002:
        problems.append(f"coverage 应为≈{KNOWN['coverage']}（实测 {c['coverage']}）")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="argument_graph_analysis",
                                 description="611 C1 论证图连通分量分析")
    ap.add_argument("--version", action="version", version=f"argument_graph_analysis {VERSION}")
    ap.add_argument("--stats", action="store_true", help="打印 JSON")
    ap.add_argument("--write", action="store_true", help=f"写 {REPORT_OUT.name}")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    c = analyze()
    if a.stats:
        print(json.dumps(c, ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = check()
        if problems:
            for p in problems:
                print(f"[C1] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[C1] ✓ 论证图结构锁定（{KNOWN['components']} 分量 / 孤立 {KNOWN['isolated']} / "
              f"最大 {KNOWN['largest']} / 覆盖 {KNOWN['coverage']:.1%}）")
        return 0
    if a.write:
        REPORT_OUT.write_text(render_report(c), encoding="utf-8", newline="\n")
        print(f"[C1] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}")
        return 0
    print(f"components {c['components']} · isolated {len(c['isolated'])} · "
          f"largest {c['largest_size']} ({c['coverage']:.1%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
