# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671g B1/B3：率三元组一致性 + 分母完整性的红绿路径测试。

红路径纪律：每个测试都**先制造它声称能抓的问题，确认红，再恢复确认绿**——
不制造问题就没有"门禁真的有射程"的证据。
"""
from __future__ import annotations

import number_consistency_scan_671g as S


# ── B1 算术自洽 ─────────────────────────────────────────────────────────────

def test_arithmetic_inconsistency_flagged(tmp_path):
    d = tmp_path / "docs"
    d.mkdir()
    (d / "x.md").write_text("holdout 检出率 **80.0%（14/16）**\n", encoding="utf-8")
    rep = S.scan(tmp_path)
    assert rep["inconsistency_count"] >= 1
    assert rep["arithmetic_inconsistencies"][0]["file"] == "docs/x.md"
    # 恢复成自洽值 ⇒ 绿
    (d / "x.md").write_text("holdout 检出率 **87.5%（14/16）**\n", encoding="utf-8")
    assert S.scan(tmp_path)["inconsistency_count"] == 0


def test_same_kn_different_pct_flagged(tmp_path):
    d = tmp_path / "docs"
    d.mkdir()
    (d / "a.md").write_text("率 50.0%（1/2）\n", encoding="utf-8")
    (d / "b.md").write_text("率 60.0%（1/2）\n", encoding="utf-8")
    rep = S.scan(tmp_path)
    assert rep["conflicting_calibers"], "同一 (1,2) 两个率必须报冲突"
    # 统一后绿
    (d / "b.md").write_text("率 50.0%（1/2）\n", encoding="utf-8")
    assert S.scan(tmp_path)["inconsistency_count"] == 0


def test_different_caliber_not_flagged():
    """盲测 14/16=87.5 与累计 17/21=81.0 是**不同口径**，不得判不一致。"""
    triples = {(pct, k, n) for _, pct, k, n in S.citations_in(
        (S.ROOT / "data/671g_数字真实性核查.md").read_text(encoding="utf-8"))}
    assert (87.5, 14, 16) in triples and (81.0, 17, 21) in triples
    rep = S.scan(S.ROOT)
    assert not any((c["k"], c["n"]) in ((14, 16), (17, 21)) for c in rep["conflicting_calibers"])


def test_code_fences_excluded(tmp_path):
    d = tmp_path / "docs"
    d.mkdir()
    (d / "c.md").write_text("正文率 87.5%（14/16）\n\n```\n99.9%（1/2）\n```\n",
                            encoding="utf-8")
    # 代码块里的 99.9% 不参与扫描
    rep = S.scan(tmp_path)
    assert all("99.9" not in str(a) for a in rep["arithmetic_inconsistencies"])


def test_writing_precision_tolerance(tmp_path):
    d = tmp_path / "docs"
    d.mkdir()
    # 87% 是整数精度，14/16=87.5 四舍五入到整数=88 ⇒ 用更宽容差，不误报
    (d / "p.md").write_text("率约 88%（14/16）\n", encoding="utf-8")
    assert S.scan(tmp_path)["inconsistency_count"] == 0


def test_scan_ignore_marker(tmp_path):
    d = tmp_path / "docs"
    d.mkdir()
    (d / "m.md").write_text("红路径示例：率 50.0%（2/3）<!-- 671g:scan-ignore -->\n",
                            encoding="utf-8")
    assert S.scan(tmp_path)["inconsistency_count"] == 0


def test_real_repo_zero_inconsistency():
    rep = S.scan(S.ROOT)
    assert rep["scanned_files"] >= 10
    assert rep["inconsistency_count"] == 0


# ── B3 分母完整性（红路径）────────────────────────────────────────────

def test_denominator_missing_flags(tmp_path):
    d = tmp_path / "docs" / "discipline"
    d.mkdir(parents=True)
    (d / "y.md").write_text("holdout 检出率为 80.0%，表现很好。\n", encoding="utf-8")
    f = S.check_denominator_complete(tmp_path)
    assert any(x["rule"] == "G-DENOMINATOR-COMPLETE" for x in f)
    # 补 k/n + 口径 ⇒ 绿
    (d / "y.md").write_text("holdout 盲测检出率为 81.0%（17/21，可测口径，CP95 另列）。\n",
                            encoding="utf-8")
    assert S.check_denominator_complete(tmp_path) == []


def test_denominator_threshold_not_flagged(tmp_path):
    d = tmp_path / "docs" / "discipline"
    d.mkdir(parents=True)
    (d / "t.md").write_text("新规则误报率阈值 <5% 才能发布。\n", encoding="utf-8")
    assert S.check_denominator_complete(tmp_path) == []


def test_denominator_baseline_json_requires_kn(tmp_path):
    exp = tmp_path / "data" / "experiments"
    exp.mkdir(parents=True)
    import json
    (exp / "baseline_fd.json").write_text(json.dumps(
        {"holdout": {"measurable": {"point": 0.875}}, "corpus": {"measurable": {}}}),
        encoding="utf-8")
    f = S.check_denominator_complete(tmp_path)
    assert any("baseline_fd.json" in x["target"] for x in f)
    # 补 k/n ⇒ 绿
    (exp / "baseline_fd.json").write_text(json.dumps(
        {"holdout": {"measurable": {"point": 0.875, "numerator": 14, "denominator": 16}},
         "corpus": {"measurable": {}}}), encoding="utf-8")
    assert S.check_denominator_complete(tmp_path) == []


def test_denominator_code_fence_excluded(tmp_path):
    d = tmp_path / "docs" / "discipline"
    d.mkdir(parents=True)
    (d / "z.md").write_text("说明：\n\n```\nholdout 检出率 99.0%\n```\n", encoding="utf-8")
    assert S.check_denominator_complete(tmp_path) == []


def test_denominator_real_repo_clean():
    assert S.check_denominator_complete(S.ROOT) == []
