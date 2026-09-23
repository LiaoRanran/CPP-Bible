"""629 A2 · 误报注入探针 单测（7 例）。

注意：`measure()` 会计时（镜像 + 约 20 次全库求值 ≈ 20s），故用 module 级 fixture 缓存。
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import autoimmune_probe_629 as P


@pytest.fixture(scope="module")
def measured():
    return P.measure()


def test_perturbations_are_semantics_preserving():
    txt = ('---\nid: ATOM-T-001\nstatus: verified\ntitle: "带引号的标题"\n'
           "history:\n  - {level: draft, at: legacy, by: writer:agent}\n---\n\n正文\n")
    assert len(P.PERTURBATIONS) == 5
    for kind in P.PERTURBATIONS:
        p = P.perturb(kind, txt)
        assert p is not None, f"{kind} 应对合成卡适用"
        assert P.fm_equal(txt, p), f"{kind} 应语义等价（parse_frontmatter 逐键相等）"
        assert p != txt, f"{kind} 必须真的改动了文本"


def test_semantic_change_is_detected():
    txt = "---\nid: ATOM-T-001\nstatus: verified\n---\n\n正文\n"
    changed = txt.replace("status: verified", "status: draft")
    assert not P.fm_equal(txt, changed), "语义改动必须被判不等价（防止把语义改动计成格式过敏）"


def test_no_perturbation_on_non_frontmatter():
    assert P.perturb("trailing_ws", "没有 frontmatter 的正文\n") is None
    assert P.split_frontmatter("no fm") is None


def test_measured_has_sample_and_valid_perturbations(measured):
    assert len(measured["cards"]) == P.SAMPLE_N == 5
    assert measured["measured"] >= 10, "有效扰动应覆盖 5 卡 × 多数扰动种类"
    assert measured["measured"] + measured["na"] + len(measured["non_neutral"]) \
        == len(measured["rows"])


def test_negative_control_holds(measured):
    """真阴性：镜像中原样卡的 warn 集合必须等于真实仓库读数。"""
    assert measured["tn_ok"] is True


def test_false_positive_rate_consistent(measured):
    fp = len(measured["fp_events"])
    assert abs(measured["false_positive_rate"]
               - fp / max(measured["measured"], 1)) < 1e-9
    assert all(e["new_rules"] for e in measured["fp_events"])


def test_report_written_with_confusion_matrix():
    p = P.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("混淆矩阵", "真阴性", "假阳性", "真阳性", "假阴性", "格式过敏率", "局限"):
        assert kw in md, f"报告缺：{kw}"
    assert "124/124" in md and "1/1406" in md      # 引用的 standing baseline 必须标注来源


def test_repo_untouched_by_probe():
    assert P._repo_clean(), f"探针不得改动 atoms/evidence：{P._git_dirty()}"
    assert os.path.exists(os.path.join(P.ROOT, "data", "autoimmune_probe_results.md"))
