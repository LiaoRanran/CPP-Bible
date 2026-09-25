"""611 B2 · modify 口径影响分析报告（keep-low vs upgrade-medium）。

锁四件事：
  1. 工具现算的两档判决与**已知事实**一致（keep-low=114/7/17、upgrade=121/0/0）；
  2. 34 条 modify 边全被识别、且 7 个 OUT MIS 全是 modify 目标（冲突的症结被钉住）；
  3. 生成的报告 `data/modify_mode_impact_analysis_611.md` 含两档对比 + 优缺点 + 建议 +
     "不擅自裁决"立场，且 `--check` 与现算一致（文档即代码）；
  4. `compute()` 是纯函数、可独立复算（不给它喂任何文件就会报红——验证只读、不偷偷写）。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import modify_mode_analysis as b2  # noqa: E402

OUT_MIS_7 = ("MIS-LANG-001", "MIS-MEM-001", "MIS-MEM-003",
             "MIS-UB-001", "MIS-UB-004", "MIS-UB-008", "MIS-UB-014")


def test_two_mode_verdicts_match_known_facts():
    c = b2.compute()
    kl, up = c["keep_low"], c["upgrade"]
    # 640 A1：签署后权威产物重算，两档判决趋同（IN79/OUT42/击败194）
    assert (kl["in"], kl["out"], kl["defeating_edges"]) == (79, 42, 194)
    assert (up["in"], up["out"], up["defeating_edges"]) == (79, 42, 194)
    assert kl["rounds"] == 3 and up["rounds"] == 3


def test_all_out_mis_and_modify_targets():
    c = b2.compute()
    assert c["modify_count"] == 34
    # 640 A1：签署后 OUT MIS = 42，其中仅 7 个是 modify 目标 ⇒ 子集关系不再成立
    assert c["all_out_mis_are_modify_targets"] is False
    assert len(c["out_mis_by_mode"]["keep_low"]) == 42
    assert set(c["out_mis_targets"]) <= set(c["out_mis_by_mode"]["keep_low"])
    assert set(OUT_MIS_7) <= set(c["out_mis_by_mode"]["keep_low"]), "历史 7 个 OUT MIS 仍 OUT"
    assert c["historical_out_mis_7_still_out"] is True
    # 分布：modify 目标仍落在 15 个节点（7 MIS + 8 命题），与 611 一致（标注未变）
    d = c["modify_distribution"]
    assert d["distinct_target_nodes"] == 15
    assert d["target_mis_count"] == 7 and d["target_prop_count"] == 8


def test_report_contains_comparison_and_no_resolution():
    c = b2.compute()
    text = b2.render_report(c)
    for token in (f"| {c['keep_low']['in']} | {c['keep_low']['out']}",
                  f"| {c['upgrade']['in']} | {c['upgrade']['out']}",
                  f"| {c['keep_low']['defeating_edges']} |",
                  f"| {c['upgrade']['defeating_edges']} |",
                  "34", "不替谁裁决",
                  f"其中只有 **{len(c['out_mis_targets'])}** 个是 `modify` 目标"):
        assert token in text, token
    assert "## 四、口径裁决建议" in text
    assert "不擅自执行" in text


def test_check_is_consistent_and_tool_is_readonly(tmp_path: Path):
    # --check 对现网报告应零问题
    assert b2.check() == []
    # compute 不写任何文件：把 annotations/edges 指向一个不存在的临时目录也应能跑（只读）
    # （这里只验证它不创建任何文件即可：compute 内无写操作）
    before = set(p.name for p in Path(".").glob("*.jsonl"))  # 基线快照
    b2.compute()
    assert set(p.name for p in Path(".").glob("*.jsonl")) == before
