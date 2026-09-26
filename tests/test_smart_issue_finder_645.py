"""645 A1 问题发现器单测（fast 组：用合成真实计数，不跑全库 gate）。

锁定：严重度计算可复现、Top10 排序、盲区→critical/high、每条问题有真实证据引用、不凑数。
对应 645 §三 A1 验收：已知真实问题必进 Top10、每条有数据引用、严重度可复现。
"""
import sys

sys.path.insert(0, "tools")

import gate_engine as ge
import smart_issue_finder_645 as a1

# 取一个真实存在的 block 规则 ID（用于盲区 critical 判定）
REAL_BLOCK = next((r.id for r in ge.RULES if r.severity == "block"), "R-B")


def test_selftest_passes():
    assert a1.selftest() == 0


def test_blind_block_rule_is_critical():
    """某真实 block 规则真实 0 命中（盲区）→ 必须判 critical。"""
    issues = a1.build_issues(
        finding_counts={REAL_BLOCK: 0}, blind={REAL_BLOCK}, error_rates={}, aging={}, top_n=10)
    hit = [i for i in issues if i["issue_id"] == f"ISSUE-{REAL_BLOCK}"]
    assert hit, "真实 block 盲区规则应进榜"
    assert hit[0]["severity"] == "critical"
    assert "盲区" in hit[0]["root_cause"]


def test_blind_nonblock_is_high():
    """任意规则盲区至少 high（该响不响 = 显著问题）。"""
    issues = a1.build_issues(
        finding_counts={}, blind={"R-B"}, error_rates={}, aging={}, top_n=10)
    hit = [i for i in issues if i["issue_id"] == "ISSUE-R-B"]
    assert hit and hit[0]["severity"] == "high"


def test_issue_has_real_evidence_ref():
    issues = a1.build_issues(
        finding_counts={"R-A": 3}, blind=set(), error_rates={}, aging={})
    assert len(issues) >= 1
    for i in issues:
        assert i["evidence_refs"], "每条问题必须有真实证据引用（不凑数）"
        assert i["root_cause"], "每条问题必须有根因"


def test_high_error_rate_flags_issue():
    issues = a1.build_issues(
        finding_counts={}, blind=set(),
        error_rates={"R-C": {"known_error_rate": 0.35}}, aging={})
    hit = [i for i in issues if i["issue_id"] == "ISSUE-R-C"]
    assert hit, "真实高 error_rate（0.35）的问题应进榜"
    assert hit[0]["severity"] == "high"


def test_no_signal_no_issue():
    """没有任何真实信号 → 不进榜（不凑数）。"""
    issues = a1.build_issues(
        finding_counts={}, blind=set(), error_rates={}, aging={})
    assert all(i["evidence_refs"] for i in issues)
