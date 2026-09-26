"""647 A4 · 外部锚接口回归锁（编号 A4-1..A4-9）。

锁定：`publish(hash)->receipt` / `verify(hash,receipt)->bool` 契约；本地 mock 可发布可验证、
篡改必检出；**预留接入点调用即抛**（不静默降级）；**不真连任何外部服务**。
"""
from __future__ import annotations

import json
import os

import external_anchor_647 as A
import pytest

H = "f" * 64


# ── A4-1：契约两条存在且可调用 ──────────────────────────────────────────────────
def test_a4_1_contract_exists():
    assert callable(A.publish) and callable(A.verify)
    spec = A.interface_spec()
    assert spec["contract"]["publish"].startswith("publish(hash")
    assert spec["contract"]["verify"].startswith("verify(hash")


# ── A4-2：mock 可发布、可验证、确定性 ──────────────────────────────────────────
def test_a4_2_mock_publish_and_verify():
    r = A.publish(H, published_at="2026-09-26T00:00:00Z")
    assert r["provider"] == A.MOCK_PROVIDER and r["hash"] == H
    assert len(r["receipt_id"]) == 64 and len(r["receipt_digest"]) == 64
    assert A.verify(H, r) is True
    assert A.publish(H, published_at="2026-09-26T00:00:00Z") == r, "同参必须同凭据（可复算）"


# ── A4-3：篡改任一字段 / 换 hash ⇒ 必检出 ─────────────────────────────────────
@pytest.mark.parametrize("field,bad", [("receipt_id", "0" * 64), ("receipt_digest", "0" * 64),
                                       ("published_at", "1999-01-01T00:00:00Z"),
                                       ("hash", "0" * 64)])
def test_a4_3_tamper_detected(field: str, bad: str):
    r = A.publish(H, published_at="2026-09-26T00:00:00Z")
    t = dict(r)
    t[field] = bad
    assert A.verify(H, t) is False, field
    assert A.verify("e" * 64, r) is False, "换 hash 也必须 False"


# ── A4-4：畸形输入 ⇒ False（不抛）─────────────────────────────────────────────
def test_a4_4_malformed_receipt_is_false():
    assert A.verify(H, {}) is False
    assert A.verify(H, None) is False          # type: ignore[arg-type]
    assert A.verify(H, {"provider": "nope"}) is False
    r = A.publish(H)
    assert A.verify(H, {k: v for k, v in r.items() if k != "receipt_digest"}) is False


# ── A4-5：预留接入点：登记齐、未实现、调用即抛（不静默降级成 mock）───────────────
def test_a4_5_reserved_providers_are_explicitly_unimplemented():
    names = [s["name"] for s in A.RESERVED_PROVIDERS]
    assert set(names) == {"github-gist", "rfc3161-timestamp", "opentimestamps"}
    for n in names:
        p = A.get_provider(n)
        assert p.implemented is False
        with pytest.raises(A.AnchorNotImplemented):
            p.publish(H)
        with pytest.raises(A.AnchorNotImplemented):
            p.verify(H, {})
    # 未实现提供方 ⇒ 门面 `verify()` 返回 False（fail-closed，不伪装成"验过了"）
    assert A.verify(H, {"provider": "github-gist", "hash": H}) is False


# ── A4-6：把当前透明日志 anchor 发布到 mock 并验证可验 ─────────────────────────
def test_a4_6_current_transparency_anchor_roundtrip():
    a = A.transparency_anchor()
    assert a["n_entries"] >= 1 and len(a["anchor"]) == 64
    cur = A.publish_current_anchor(published_at="2026-09-26T00:00:00Z")
    assert cur["published"] is True and cur["verified"] is True
    assert cur["tamper_detected"] is True
    assert cur["receipt"]["hash"] == a["anchor"]


# ── A4-7：**不真连外部服务**（诚实口径可机检）──────────────────────────────────
def test_a4_7_no_real_external_service():
    spec = A.interface_spec()
    assert spec["real_external_service_connected"] is False
    assert spec["implemented"] == [A.MOCK_PROVIDER]
    src = open(os.path.join(A.HERE, "external_anchor_647.py"), encoding="utf-8").read()
    for banned in ("import requests", "import urllib", "import socket", "import http"):
        assert banned not in src, f"不得联网：{banned}"


# ── A4-8：透明日志 / 受控文件零改动（发布只读）────────────────────────────────
def test_a4_8_read_only():
    import hashlib
    log = os.path.join(A.ROOT, "data", "transparency_log.jsonl")
    before = hashlib.sha256(open(log, "rb").read()).hexdigest()
    A.transparency_anchor()
    A.publish_current_anchor(published_at="2026-09-26T00:00:00Z")
    assert hashlib.sha256(open(log, "rb").read()).hexdigest() == before


# ── A4-9：报告与自检 ─────────────────────────────────────────────────────────
def test_a4_9_report_and_selftest():
    assert A.selftest() == 0
    assert A.main(["--report"]) == 0
    assert os.path.isfile(A.OUT_MD) and os.path.isfile(A.OUT_JSON)
    doc = json.load(open(A.OUT_JSON, encoding="utf-8"))
    assert doc["spec"]["real_external_service_connected"] is False
    assert doc["current"]["verified"] is True
