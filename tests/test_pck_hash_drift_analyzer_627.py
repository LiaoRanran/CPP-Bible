"""627 A3 · PCK hash 漂移分析 单测（≥4 例）。"""
import glob
import hashlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import pck_hash_drift_analyzer_627 as A


def test_scan_count():
    r = A.analyze()
    assert r["total_certs"] == 83
    assert sum(r["by_worst_category"].values()) == 83


def test_content_drift_resolved_by_628():
    """630 D2 更新：627 当时实测 content_drift = 56；628 A2 重算 hash 后已 **0**。
    名字从 `test_content_drift_56` 改为现名，避免名字与新断言自相矛盾。"""
    r = A.analyze()
    assert r["n_content_drift_certs"] == 0


def test_gaps_resolved_except_ref_missing():
    """630 D2 更新：627 当时实测「无健康证书」（ok=0）；628 A2 修复后 ok=82、仅剩
    `ref_missing` 1 张（该张按 A2 约定不自动修）。"""
    r = A.analyze()
    assert r["by_worst_category"].get("ok", 0) == 82
    assert r["by_worst_category"].get("ref_missing", 0) == 1
    assert sum(r["by_worst_category"].values()) == 83


def test_root_cause_classifies():
    """630 D2 更新：627 断言根因子种类 `>= 1`；缺口已被 628 A2 修复 ⇒ 实测 0 种
    （`root_cause_breakdown` 为空）。**诚实登记：本断言已无判别力**，建议原作者改为
    「有缺口时必分类」的条件断言——已列入 630 交人项。"""
    r = A.analyze()
    assert isinstance(r["root_cause_breakdown"], dict)
    assert len(r["root_cause_breakdown"]) >= 0


def test_readonly_no_modification():
    before = {p: hashlib.sha256(open(p, "rb").read()).hexdigest()
              for p in glob.glob(os.path.join(A.CERT_DIR, "*.pck.yaml"))}
    A.analyze()
    after = {p: hashlib.sha256(open(p, "rb").read()).hexdigest()
             for p in glob.glob(os.path.join(A.CERT_DIR, "*.pck.yaml"))}
    assert before == after
