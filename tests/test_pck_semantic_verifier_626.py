"""626 E1 · PCK semantic verifier 回归测试（≥10 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import pck_semantic_verifier_626 as P  # noqa: E402

GOOD = {"schema_version": "1.0",
        "claim": {"id": "C1", "statement": "data race is undefined behavior"},
        "evidence": [{"type": "replay", "ref": "data/grounded_labels_w2.json"}],
        "verifiers": [{"name": "gate_engine", "result": "pass"}],
        "uncertainty": {"cs_upper_bound": 0.001},
        "provenance": {"commit": "abc123"},
        "human_authority": {"status": "pending"}}


def _v() -> P.PCKSemanticVerifier:
    return P.PCKSemanticVerifier()


def test_selftest_passes():
    assert P.selftest() == 0


def test_b2s_schema_pass_and_fail():
    v = _v()
    assert v.check_schema(GOOD)["status"] == "pass"
    bad = {"claim": {}, "evidence": [], "uncertainty": {}, "provenance": {}}
    assert v.check_schema(bad)["status"] == "fail"


def test_b2s_accepts_verifiers_plural():
    """实测字段名为 `verifiers`（复数）。"""
    v = _v()
    assert v.check_schema(GOOD)["status"] == "pass"
    single = dict(GOOD)
    single.pop("verifiers")
    single["verifier"] = "v1"
    assert v.check_schema(single)["status"] == "pass"
    none = dict(GOOD)
    none.pop("verifiers")
    assert v.check_schema(none)["status"] == "fail"


def test_b2r_referential_resolvable():
    v = _v()
    r = v.check_referential(GOOD, "X")
    assert r["status"] == "pass"


def test_b2r_hash_mismatch_detected():
    """真实发现：56 张 PCK 的 evidence.hash 与当前文件不匹配。"""
    v = _v()
    bad = {"evidence": [{"type": "replay", "ref": "data/grounded_labels_w2.json",
                         "hash": "sha256:" + "0" * 64}]}
    r = v.check_referential(bad, "X")
    assert r["status"] == "fail"
    assert any("hash" in e for e in r["errors"])


def test_b2e_evidence_semantics():
    v = _v()
    assert v.check_evidence_semantics(GOOD)["status"] == "pass"
    assert v.check_evidence_semantics({"evidence": [], "claim": {}})["status"] == "fail"


def test_b2a_authority_semantics():
    v = _v()
    assert v.check_authority(GOOD, "X")["status"] == "pass"
    auth = dict(GOOD, human_authority={"status": "authorized"})
    r = v.check_authority(auth, "X")
    assert r["status"] == "fail"      # authorized 但无 card-level Authority event


def test_global_vs_local_uncertainty():
    v = _v()
    g = v.check_uncertainty({"uncertainty": {"cs_upper_bound": P.GLOBAL_CS_UPPER}})
    assert "global_uncertainty_ref" in " ".join(g["notes"])
    loc = v.check_uncertainty({"uncertainty": {"cs_upper_bound": 0.001}})
    assert "local" in " ".join(loc["notes"]).lower()


def test_verify_single_and_all():
    v = _v()
    allr = v.verify_all()
    assert allr["count"] == 83
    assert len(allr["by_layer_pass"]) == 4


def test_all_four_layers_present():
    v = _v()
    allr = v.verify_all()
    first = next(iter(allr["results"].values()))
    layers = {layer["layer"] for layer in first["layers"]}
    assert layers == {"B2-S", "B2-R", "B2-E", "B2-A"}


def test_report_generated_and_does_not_modify_pcks():
    assert os.path.exists(P.OUT_MD)
    n = len([f for f in os.listdir(P.CERT_DIR) if f.endswith(".pck.yaml")])
    _v().verify_all()
    assert len([f for f in os.listdir(P.CERT_DIR) if f.endswith(".pck.yaml")]) == n
