# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""628 A2 · PCK hash 重算 单测（7 例）。"""
import glob
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import pck_hash_renewal_628 as P

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERT_DIR = os.path.join(HERE, "data", "pck", "certificates")
# 670a 去写死 + 诚实登记：证书 ↔ 卡 差集登记在 `data/670a_cert_gap.json`（known-gap 惯例）。
_GAP_FILE = os.path.join(HERE, "data", "670a_cert_gap.json")


def _documented_gap() -> frozenset:
    with open(_GAP_FILE, encoding="utf-8") as fh:
        return frozenset(json.load(fh)["gap_cards"])


def _cert_ids() -> set[str]:
    # 证书文件名为 `<CARD_ID>.pck.yaml` ⇒ 去掉整个后缀（`splitext` 只去 `.yaml`）
    return {os.path.basename(p)[:-len(".pck.yaml")]
            for p in glob.glob(os.path.join(CERT_DIR, "*.pck.yaml"))}


def _card_ids() -> set[str]:
    import gate_engine as ge  # noqa: E402
    out: set[str] = set()
    for pat, base in (("ATOM-*.md", ge.ATOMS), ("EV-*.md", ge.EVIDENCE)):
        for p in base.rglob(pat):
            if "README" in p.name or p.parent.name == "draft650":
                continue
            m = ge._meta(p)
            out.add(str(m.get("id") or p.stem))
    return out


def test_cert_set_matches_fact_source_except_documented_gap():
    """670a 去写死：证书数不再冻结 `counts.CARDS_REAL`（=卡口径，两者本就不同）。

    改锁：证书集 == 事实源卡集 − **登记差集**（差集变化即红）；且无幽灵证书。
    """
    certs, cards = _cert_ids(), _card_ids()
    gap = _documented_gap()
    assert not (certs - cards), "幽灵证书：引用了事实源中不存在的卡"
    assert cards - certs == set(gap), sorted(cards - certs)
    assert len(certs) == len(cards) - len(gap)


def test_hash_matches_current_file():
    v = P.verify()
    assert v["hash_ok"] >= 82 and v["bad_count"] == 0


def test_ref_missing_not_auto_fixed():
    v = P.verify()
    assert 1 <= v["needs_human"] <= 2
    # 需人审条目必须有 hash_status 标记且不伪造 hash
    for p in glob.glob(os.path.join(CERT_DIR, "*.yaml")):
        data = yaml.safe_load(open(p, encoding="utf-8"))
        for ev in data.get("evidence", []) or []:
            if ev.get("hash_status") == P.NEEDS_HUMAN:
                assert not os.path.exists(ev["ref"])


def test_semantic_fields_untouched():
    assert P.semantic_fields_untouched()


def test_backup_exists_with_83():
    assert os.path.isdir(P.BACKUP_DIR)
    assert len(glob.glob(os.path.join(P.BACKUP_DIR, "*.yaml"))) == 83


def test_hash_format_preserved():
    # hash 保持 sha256:<hex> 前缀格式
    for p in glob.glob(os.path.join(CERT_DIR, "*.yaml")):
        data = yaml.safe_load(open(p, encoding="utf-8"))
        for ev in data.get("evidence", []) or []:
            h = ev.get("hash")
            if h:
                assert h.startswith("sha256:") and len(h) == 7 + 64
        break


def test_renewal_idempotent():
    # 再跑一次 apply：全部 already_ok，不新增改动
    before = P.verify()
    r = P.renew(apply_changes=True)
    after = P.verify()
    assert before == after
    assert r["stats"]["renewed"] == 0 and r["stats"]["added"] == 0
