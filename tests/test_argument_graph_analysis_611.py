"""611 C1 · 论证图连通分量分析（碎片化定量化）。

锁五件事：
  1. 工具现算与**已知事实**一致（11 分量 / 孤立 4 / 最大 80 / 121 节点 / 388 边 / 覆盖 ≈66.1%）；
  2. 4 个孤立节点**全是命题**（断联论证）；
  3. `--check` 锁定上述结构（论证图未重构前不可变）；
  4. 复用 610 `argument_audit` 的同一 BFS 算法（single source of truth，不另起一套）；
  5. 报告含总览 + 各分量大小 + 孤立节点 + 结论（碎片化），且可独立复算。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import argument_graph_analysis as c1  # noqa: E402

KNOWN = {"components": 11, "isolated": 4, "largest": 80, "nodes": 121,
         "edges": 388, "coverage": 0.6612}


def test_components_match_known_facts():
    c = c1.analyze()
    assert c["components"] == KNOWN["components"]
    assert c["largest_size"] == KNOWN["largest"]
    assert c["nodes"] == KNOWN["nodes"]
    assert c["edges"] == KNOWN["edges"]
    assert abs(c["coverage"] - KNOWN["coverage"]) <= 0.002
    assert len(c["sizes"]) == KNOWN["components"]
    assert c["sizes"][0] == KNOWN["largest"]


def test_isolated_nodes_are_all_propositions():
    import argument_audit as aa  # noqa: E402
    c = c1.analyze()
    assert len(c["isolated"]) == KNOWN["isolated"]
    edges, verdicts, _ = aa.load_state()
    for n in c["isolated"]:
        assert aa.dc.node_type_of(n, edges) == "proposition"
    # 最大分量类型构成合理（命题 + 误解）
    assert c["largest_component_types"]["proposition"] > 0
    assert c["largest_component_types"]["misconception"] > 0


def test_check_locks_structure_and_report_is_reproducible():
    assert c1.check() == []
    c = c1.analyze()
    text = c1.render_report(c)
    for token in (f"连通分量 **{KNOWN['components']}**",
                  f"孤立节点（仅 1 节点分量）**{KNOWN['isolated']}**",
                  f"最大分量 {KNOWN['largest']} 节点 = 覆盖 {KNOWN['coverage']:.1%}",
                  "论证图碎片化", "11 块"):
        assert token in text, token
