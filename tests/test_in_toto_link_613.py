#!/usr/bin/env python3
"""E2 回归测试：in_toto_link（link 元数据 · HMAC 对称签名，非标准非对称）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import in_toto_link as e2  # noqa: E402

KEY = b"unit-test-key"


def test_scheme_is_explicitly_nonstandard():
    link = e2.build_link("s", [], [], [], {}, KEY)
    assert link["signature"]["scheme"] == e2.SCHEME
    assert "not-in-toto-standard" in e2.SCHEME, "必须显式标注非标准，不得伪装成真签名"


def test_verify_ok_with_right_key():
    link = e2.build_link("s", [__file__], [__file__], ["echo"], {}, KEY)
    ok, errs = e2.verify_link(link, KEY)
    assert ok and not errs


def test_verify_fails_with_wrong_key():
    link = e2.build_link("s", [__file__], [__file__], ["echo"], {}, KEY)
    ok, _ = e2.verify_link(link, b"wrong")
    assert not ok


def test_unsigned_link_is_rejected():
    link = e2.build_link("s", [], [], [], {}, None)
    ok, errs = e2.verify_link(link, None)
    assert not ok and any("未签名" in e for e in errs)


def test_tampered_product_hash_detected():
    link = e2.build_link("s", [], [__file__], [], {}, KEY)
    rel = next(iter(link["products"]))
    link["products"][rel]["sha256"] = "0" * 64
    ok, errs = e2.verify_link(link, KEY)
    assert not ok and any("哈希不符" in e for e in errs)


def test_missing_file_detected():
    link = e2.build_link("s", [], [], [], {}, KEY)
    link["products"] = {"no/such/file.json": {"sha256": "0" * 64}}
    ok, errs = e2.verify_link(link, KEY)
    assert not ok and any("不存在" in e for e in errs)


def test_link_json_shape():
    link = e2.build_link("s", [__file__], [], ["echo", "hi"], {"return-value": 0}, KEY)
    assert link["_type"] == "link"
    assert link["command"] == ["echo", "hi"]
    assert set(link) >= {"materials", "products", "byproducts", "signature"}


def test_check_passes():
    assert e2.main(["--check"]) == 0
