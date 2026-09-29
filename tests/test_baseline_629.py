# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""629 任务0 · 基线台账 单测（7 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import baseline_629 as B
import counts_659 as counts  # 666 A2：去写死


def test_standing_matches_task_book():
    s = B.STANDING
    assert (s["gate_rules"], s["gate_hits"], s["gate_block"], s["gate_warn"],
            s["gate_advice"]) == (67, 191, 0, 186, 5)
    assert s["escape"].startswith("1/1406") and "0.9062%" in s["escape"]
    assert s["mirror_edges"].endswith("总 194") and s["pck"].endswith("27/83")
    assert set(B.TASK_BOOK_NUMBERS) == {"atoms", "mutation_v7", "tools"}


def test_gate_counts_measured_equals_standing():
    """666 A2 去写死：原断言 `(121,0,116,5)` / `warn_top[0]==(...,77)` / `len==8` 是
    640 时点的**测量快照**——639/658–665 后实测已到 `(231,0,176,55)`，冻结它只会假红。

    改为**可加性 + 事实源**：
      · 总数 == block+warn+advice（分类可加，换了语料也成立）；
      · rules_loaded == `gate_engine.RULES` 实际条数（派生 vs 事实源）；
      · warn_top 是"按规则名降序 top10 且截断到实际 warn 规则数"（结构不变量）；
      · 历史基线仍由 `B.STANDING` 存档承载（那一处**不**改，它是历史）。
    """
    import gate_engine as ge

    g = B.gate_counts()
    assert g["total"] == g["block"] + g["warn"] + g["advice"]
    assert g["rules_loaded"] == len(ge.RULES)
    assert g["automated_rules"] <= g["rules_loaded"]
    assert len(g["warn_top"]) == min(10, g["warn_rule_count"])
    counts_only = [n for _n, n in g["warn_top"]]
    assert counts_only == sorted(counts_only, reverse=True), "warn_top 必须降序"
    assert all(n > 0 for n in counts_only)
    # `ge.RULES` 是 `Rule` 对象列表（不是 dict）⇒ 用属性名对齐，别用 `in RULES`
    rule_ids = {r.id for r in ge.RULES}
    assert all(rname in rule_ids for rname, _n in g["warn_top"])


def test_head_anchor_is_ancestor():
    assert B.is_ancestor(B.STANDING["head"], "HEAD"), "629 开工锚点必须在当前 HEAD 祖先链上"
    assert B.is_ancestor(B.REMOTE_SHA, "HEAD")


def test_git_facts_readable():
    """630 D2 更新（只改数字）：629 当时断言 `ahead >= 62`；**630 B2 完成 push 后 ahead = 0**
    ⇒ 硬编码下限过期。改为 `>= 0`（合法非负整数即可；HEAD/log3 关系仍锁住）。"""
    g = B.git_facts()
    assert g["ahead"] >= 0 and len(g["head"]) >= 7
    assert len(g["log3"]) == 3 and g["log3"][0].startswith(g["head"])


def test_file_counts_measured():
    """666 A2 去写死：`atoms_md==27` / `pck_yaml==83` 是 629 时点快照。

    改为对齐 `counts_659` 事实源：`atoms_md` 走的是"所有 ATOM-*.md 文件"（含
    `atoms/draft650/` 草稿）⇒ 对应 `ATOMS_TOTAL`；PCK 证书目录只含实卡 ⇒ `CARDS_REAL`。
    """
    f = B.file_counts()
    assert f["tools_py"] > 300 and f["tests_py"] > 300
    assert f["atoms_md"] == counts.ATOMS_TOTAL
    assert f["pck_yaml"] == counts.CARDS_REAL


def test_report_sections_written(tmp_path):
    p = B.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("standing baseline", "开工实测", "warn 按规则名 top10",
               "实测 vs 任务书", "既有失败", "recent commits"):
        assert kw in md, f"报告缺章节：{kw}"
    assert "基线漂移" in md or "一致" in md


def test_selftest_and_baseline_failure_freeze():
    """基线为**修正版 11 项**：首测 19 项里 8 项是自伤（工作区里语法未完成的同名新文件）
    或本批真实回归（C2 首版 anchor 非确定性），已在 baseline 注释与验收报告 §四.1 登记。

    631 A3：原用例还断言 `B.selftest() == 0`，而 629 工具的 selftest 断言
    「push 前 ahead ≥ 62」——630 B2 完成 push 后 ahead = 0 ⇒ **工具自检过期**。
    修它要改 629 工具（§零.11 越界）⇒ 本批**只去掉对 selftest 的依赖**（测试侧），
    保留基线计数断言（这才是本用例真正要守的东西）。
    """
    assert len(B.BASELINE_FAILURES) == 11
    assert sum(B.BASELINE_CATEGORIES.values()) == 11
    assert all(n.startswith("tests/") and "::" in n for n in B.BASELINE_FAILURES)
    assert not any(n.startswith("tests/test_") and "629" in n
                   for n in B.BASELINE_FAILURES)
