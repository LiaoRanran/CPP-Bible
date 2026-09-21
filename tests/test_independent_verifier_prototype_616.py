#!/usr/bin/env python3
"""616 D2 回归测试：独立复核原型（HMAC VSA 凭证）。"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import independent_verifier_prototype as ivp  # noqa: E402

CARD = "evidence/conc/EV-CONC-001.md"


def test_vsa_generation() -> None:
    vsa = ivp.make_vsa(CARD)
    for k in ("vsa_version", "verifier_id", "verified_at", "input", "result", "signature"):
        assert k in vsa
    assert vsa["result"]["rule"] == "EV-MATRIX-UNBACKED"
    assert vsa["input"]["path"] == CARD and len(vsa["input"]["sha256"]) == 64


def test_signature_verifies() -> None:
    vsa = ivp.make_vsa(CARD)
    ok, why = ivp.verify_vsa(vsa)
    assert ok, why


def test_tamper_detected() -> None:
    vsa = json.loads(json.dumps(ivp.make_vsa(CARD)))
    vsa["result"]["verdict"] = "BACKED" if vsa["result"]["verdict"] != "BACKED" else "UNBACKED"
    ok, _ = ivp.verify_vsa(vsa)
    assert not ok
    # 换密钥亦失败
    ok2, _ = ivp.verify_vsa(ivp.make_vsa(CARD), key=b"other")
    assert not ok2


def test_check_passes_and_samples() -> None:
    assert ivp.check() == []
    assert (ROOT / "data" / "independent_verifier_samples_616").is_dir()
