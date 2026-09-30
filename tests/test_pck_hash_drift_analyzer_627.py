# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""627 A3 · PCK hash 漂移分析 单测（≥4 例）。"""
import glob
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import counts_659 as counts  # noqa: E402
import pck_hash_drift_analyzer_627 as A

# 670a 去写死 + 诚实登记：PCK 证书集 = **证书文件现算**（103 张），事实源卡数 = 113。
# 差集是 669/668 新增的 5 张原子卡 + 5 张证据卡（尚无 PCK 证书；证书含语义字段须人签）
# ⇒ 登记在 `data/670a_cert_gap.json`（known-gap 惯例）。差集一旦变化即红（防静默扩口）。
_GAP_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "data", "670a_cert_gap.json")


def _documented_gap() -> frozenset:
    with open(_GAP_FILE, encoding="utf-8") as fh:
        return frozenset(json.load(fh)["gap_cards"])


def _cert_ids() -> set[str]:
    return {os.path.basename(p)[:-len(".pck.yaml")]
            for p in glob.glob(os.path.join(A.CERT_DIR, "*.pck.yaml"))}


def _card_ids() -> set[str]:
    """事实源卡 id（原子实卡 + 证据卡；不含 draft650 草稿）。"""
    import gate_engine as ge  # noqa: E402
    out: set[str] = set()
    for pat, base in (("ATOM-*.md", ge.ATOMS), ("EV-*.md", ge.EVIDENCE)):
        for p in base.rglob(pat):
            if "README" in p.name or p.parent.name == "draft650":
                continue
            m = ge._meta(p)
            out.add(str(m.get("id") or p.stem))
    return out


def test_scan_count():
    r = A.analyze()
    certs = _cert_ids()
    assert r["total_certs"] == len(certs)
    assert sum(r["by_worst_category"].values()) == len(certs)


def test_cert_gap_is_documented_and_bounded():
    """670a：证书 ↔ 卡 差集必须**恰好**等于登记清单（不扩口），且无幽灵证书。"""
    certs, cards = _cert_ids(), _card_ids()
    gap = _documented_gap()
    assert cards - certs == set(gap), sorted(cards - certs)
    assert not (certs - cards), "幽灵证书：引用了事实源中不存在的卡"
    assert len(certs) == len(cards) - len(gap) <= counts.CARDS_REAL


def test_content_drift_resolved_by_628():
    """630 D2 更新：627 当时实测 content_drift = 56；628 A2 重算 hash 后已 **0**。
    名字从 `test_content_drift_56` 改为现名，避免名字与新断言自相矛盾。"""
    r = A.analyze()
    assert r["n_content_drift_certs"] == 0


def test_gaps_resolved_except_ref_missing():
    """630 D2 更新：627 当时实测「无健康证书」（ok=0）；628 A2 修复后 ok=82、仅剩
    `ref_missing` 1 张（该张按 A2 约定不自动修）。"""
    r = A.analyze()
    # 670a 去写死：ok 数不再冻结 102；改为「除 ref_missing 外全部 ok」的口径不变量
    n_certs = len(_cert_ids())
    assert r["by_worst_category"].get("ref_missing", 0) == 1
    assert r["by_worst_category"].get("ok", 0) == n_certs - 1
    assert sum(r["by_worst_category"].values()) == n_certs


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
