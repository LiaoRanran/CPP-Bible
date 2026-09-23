"""629 任务0 · 基线台账 单测（7 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import baseline_629 as B


def test_standing_matches_task_book():
    s = B.STANDING
    assert (s["gate_rules"], s["gate_hits"], s["gate_block"], s["gate_warn"],
            s["gate_advice"]) == (67, 191, 0, 186, 5)
    assert s["escape"].startswith("1/1406") and "0.9062%" in s["escape"]
    assert s["mirror_edges"].endswith("总 194") and s["pck"].endswith("27/83")
    assert set(B.TASK_BOOK_NUMBERS) == {"atoms", "mutation_v7", "tools"}


def test_gate_counts_measured_equals_standing():
    g = B.gate_counts()
    assert g["total"] == B.STANDING["gate_hits"]
    assert (g["block"], g["warn"], g["advice"]) == (0, 186, 5)
    assert g["rules_loaded"] == B.STANDING["gate_rules"] == 67
    assert g["automated_rules"] < g["rules_loaded"]      # 有 3 条非程序化规则
    assert len(g["warn_top"]) == min(10, g["warn_rule_count"]) == 9
    assert g["warn_top"][0] == ("ATOM-CLAIM-CONCEPT-NORMALIZED", 77)


def test_head_anchor_is_ancestor():
    assert B.is_ancestor(B.STANDING["head"], "HEAD"), "629 开工锚点必须在当前 HEAD 祖先链上"
    assert B.is_ancestor(B.REMOTE_SHA, "HEAD")


def test_git_facts_readable():
    g = B.git_facts()
    assert g["ahead"] >= 62 and len(g["head"]) >= 7
    assert len(g["log3"]) == 3 and g["log3"][0].startswith(g["head"])


def test_file_counts_measured():
    f = B.file_counts()
    assert f["tools_py"] > 300 and f["tests_py"] > 300
    assert f["atoms_md"] == 27, "任务书说 28 张，实测 27 张（差异已登记）"
    assert f["pck_yaml"] == 83


def test_report_sections_written(tmp_path):
    p = B.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("standing baseline", "开工实测", "warn 按规则名 top10",
               "实测 vs 任务书", "既有失败", "recent commits"):
        assert kw in md, f"报告缺章节：{kw}"
    assert "基线漂移" in md or "一致" in md


def test_selftest_and_baseline_failure_freeze():
    """基线为**修正版 11 项**：首测 19 项里 8 项是自伤（工作区里语法未完成的同名新文件）
    或本批真实回归（C2 首版 anchor 非确定性），已在 baseline 注释与验收报告 §四.1 登记。"""
    assert B.selftest() == 0
    assert len(B.BASELINE_FAILURES) == 11
    assert sum(B.BASELINE_CATEGORIES.values()) == 11
    assert all(n.startswith("tests/") and "::" in n for n in B.BASELINE_FAILURES)
    assert not any(n.startswith("tests/test_") and "629" in n
                   for n in B.BASELINE_FAILURES)
