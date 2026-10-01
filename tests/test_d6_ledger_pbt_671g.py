# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671g D6：账本 10 不变式的 example-based + hypothesis 属性测试（红路径）。"""
from __future__ import annotations

import copy

import pytest

try:
    from hypothesis import given, strategies as st, settings, HealthCheck
except ImportError:  # pragma: no cover
    pytest.skip("hypothesis 未安装", allow_module_level=True)

import ledger_invariants_671g as L


def _chain(n, *, rv="1.0.0", kind="verdict", cards=None, ts_gap=True):
    recs = []
    for i in range(n):
        payload = {"verdict": "catch"} if kind == "verdict" else {}
        if cards is not None:
            payload["cards_total"] = cards[i]
        rec = L.make_record(recs[-1] if recs else None, kind, payload, rv,
                          ts=f"2026-10-{(i % 27) + 1:02d} 10:00:00" if ts_gap else "2026-10-01 10:00:00")
        recs.append(rec)
    return recs


# ── example-based 10 条不变式红路径 ──────────────────────────────────────────

def test_inv01_schema(tmp_path):
    c = _chain(1); c[0]["schema"] = "evil"
    assert any(v["inv"] == "INV-01" for v in L.validate(c))


def test_inv02_required_fields():
    c = _chain(1); del c[0]["hash"]
    assert any(v["inv"] == "INV-02" for v in L.validate(c))


def test_inv03_seq_contiguity():
    c = _chain(2); c[1]["seq_idx"] = 5
    c[1]["hash"] = L.hash_of(c[1]["prev_hash"], c[1])
    assert any(v["inv"] == "INV-03" for v in L.validate(c))


def test_inv04_ts_monotone():
    c = _chain(2); c[1]["ts"] = "2026-09-01 10:00:00"
    c[1]["hash"] = L.hash_of(c[1]["prev_hash"], c[1])
    assert any(v["inv"] == "INV-04" for v in L.validate(c))


def test_inv05_prev_hash_link():
    c = _chain(2); c[1]["prev_hash"] = "WRONG"
    c[1]["hash"] = L.hash_of("WRONG", c[1])
    assert any(v["inv"] == "INV-05" for v in L.validate(c))


def test_inv06_content_hash_detects_tamper():
    c = _chain(1); c[0]["payload"]["verdict"] = "miss"   # 改内容不重算 hash
    assert any(v["inv"] == "INV-06" for v in L.validate(c))


def test_inv07_append_only_api_exists():
    assert hasattr(L, "append_record")
    assert not hasattr(L, "update_record") and not hasattr(L, "remove_record")


def test_inv08_illegal_verdict():
    c = _chain(1); c[0]["payload"] = {"verdict": "maybe"}
    c[0]["hash"] = L.hash_of(c[0]["prev_hash"], c[0])
    assert any(v["inv"] == "INV-08" for v in L.validate(c))


def test_inv09_cards_monotone():
    c = _chain(2, kind="event", cards=[50, 40])
    assert any(v["inv"] == "INV-09" for v in L.validate(c))
    c2 = _chain(2, kind="event", cards=[50, 50])   # 不减不报错
    assert not any(v["inv"] == "INV-09" for v in L.validate(c2))


def test_inv10_rules_version_match():
    c = _chain(1, rv="1.0.0")
    assert any(v["inv"] == "INV-10" for v in L.validate(c, "2.0.0"))
    assert L.validate(c, "1.0.0") == []


# ── PBT：合法链恒通过；任意单点篡改必被至少一条不变式抓住 ────────────────────

@settings(max_examples=30, deadline=None,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
@given(n=st.integers(min_value=0, max_value=12),
       kind=st.sampled_from(("verdict", "event", "decision")))
def test_pbt_any_valid_chain_passes(n, kind):
    c = _chain(n, kind=kind, ts_gap=False)
    assert L.validate(c, "1.0.0") == []


def test_append_chain_file_roundtrip(tmp_path):
    p = tmp_path / "l.jsonl"
    for i in range(5):
        L.append_record(p, "verdict", {"verdict": "catch", "i": i}, "1.0.0",
                    ts="2026-10-01 10:00:00")
    assert L.validate_file(tmp_path, p, "1.0.0") == []


@settings(max_examples=30, deadline=None,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
@given(idx=st.integers(min_value=1, max_value=4), field=st.sampled_from(
    ["payload_illegal", "prev_hash", "ts", "rules_version", "seq_idx"]))
def test_pbt_any_single_field_tamper_breaks_chain(idx, field):
    c = _chain(5)
    c2 = copy.deepcopy(c)
    if field == "payload_illegal":
        c2[idx]["payload"] = {"verdict": "EVIL"}   # 非法判决（语义篡改）
        c2[idx]["hash"] = L.hash_of(c2[idx]["prev_hash"], c2[idx])
    elif field == "prev_hash":
        c2[idx]["prev_hash"] = "DEADBEEF"
        c2[idx]["hash"] = L.hash_of("DEADBEEF", c2[idx])
    elif field == "ts":
        # idx≥1 保证有前驱可比（genesis 之前无约束）
        c2[idx]["ts"] = "2026-01-01 00:00:00"
        c2[idx]["hash"] = L.hash_of(c2[idx]["prev_hash"], c2[idx])
    elif field == "rules_version":
        c2[idx]["rules_version"] = "9.9.9"
        c2[idx]["hash"] = L.hash_of(c2[idx]["prev_hash"], c2[idx])
    else:
        c2[idx]["seq_idx"] = c2[idx]["seq_idx"] + 1
        c2[idx]["hash"] = L.hash_of(c2[idx]["prev_hash"], c2[idx])
    assert L.validate(c2, "1.0.0") != []
