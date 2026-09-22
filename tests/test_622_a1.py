"""622 A1 · 沙箱 apply API 单测"""
from __future__ import annotations

import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import sandbox_apply_622 as SA  # noqa: E402

CARD_TEXT = (
    "---\n"
    "id: ATOM-X-001\n"
    "artifact: Examples/atoms/_x.asm\n"
    "artifact_sha256: abcdef1234567890\n"
    "status: verified\n"
    "run_match_keys:\n"
    " - k1\n"
    " - k2\n"
    "---\n"
    "\n"
    "body\n"
)


def _mkroot(td):
    os.makedirs(os.path.join(td, "atoms", "conc"), exist_ok=True)
    p = os.path.join(td, "atoms", "conc", "ATOM-X-001.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(CARD_TEXT)
    return p, SA.Sandbox(root=td, lock_path=os.path.join(td, ".lock"))


def test_whitelist():
    assert SA.is_allowed("atoms/conc/ATOM-X.md")
    assert SA.is_allowed("evidence/conc/EV-X.md")
    assert not SA.is_allowed("tools/x.py")
    assert not SA.is_allowed("Book/x.md")
    assert not SA.is_allowed("Examples/x.cpp")


def test_plan_edit_all_ops():
    t = CARD_TEXT
    assert SA.plan_edit({"op": "M1", "target_rule": "EV-FM-REQUIRED"}, t)[0] != t
    assert SA.plan_edit({"op": "M6", "target_rule": "EV-FM-REQUIRED"}, t)[0] != t
    assert SA.plan_edit({"op": "M7", "target_rule": "EV-ARTIFACT-FILE-EXISTS"}, t)[0] != t
    assert SA.plan_edit({"op": "M2", "target_rule": "CARD-PATH-NOT-CANONICAL"}, t)[0] != t
    assert SA.plan_edit({"op": "M3", "target_rule": "EV-FALSIFICATION"}, t)[0] != t
    assert SA.plan_edit({"op": "M4", "target_rule": "EV-MATRIX-UNBACKED"}, t)[0] != t
    assert SA.plan_edit({"op": "M5", "target_rule": "ATOM-STATUS-VALUE"}, t)[0] != t


def test_plan_edit_unknown_op_returns_none():
    assert SA.plan_edit({"op": "M9"}, CARD_TEXT) is None


def test_plan_edit_missing_field_returns_none():
    assert SA.plan_edit({"op": "M1", "target_rule": "NOPE"}, "---\nfoo: 1\n---\n") is None


def test_plan_edit_M3_keeps_other_lines():
    new, _desc = SA.plan_edit({"op": "M3", "target_rule": "EV-FALSIFICATION"}, CARD_TEXT)
    assert "- k1" in new and "- k2" not in new
    assert "body" in new


def test_apply_mutation_changes_content():
    with tempfile.TemporaryDirectory() as td:
        p, sb = _mkroot(td)
        before = open(p, encoding="utf-8").read()
        r = sb.apply_mutation({"content": json.dumps({"op": "M1",
                                                     "target_rule": "EV-FM-REQUIRED"})},
                              "atoms/conc/ATOM-X-001.md")
        assert r["applied"] is True
        assert open(p, encoding="utf-8").read() != before


def test_restore_recovers_original():
    with tempfile.TemporaryDirectory() as td:
        p, sb = _mkroot(td)
        before = open(p, "rb").read()
        r = sb.apply_mutation({"content": json.dumps({"op": "M5",
                                                     "target_rule": "ATOM-STATUS-VALUE"})},
                              "atoms/conc/ATOM-X-001.md")
        rst = sb.restore("atoms/conc/ATOM-X-001.md", r)
        assert rst["restored"] is True
        assert open(p, "rb").read() == before


def test_apply_and_run_restores_on_exception():
    with tempfile.TemporaryDirectory() as td:
        p, sb = _mkroot(td)
        before = open(p, "rb").read()

        def boom(_card):
            raise RuntimeError("gate 炸了")

        sb.run_gate = boom  # type: ignore[method-assign]
        try:
            sb.apply_and_run({"mutation_id": "m1",
                              "content": json.dumps({"op": "M1",
                                                     "target_rule": "EV-FM-REQUIRED"})},
                             "atoms/conc/ATOM-X-001.md")
            raised = False
        except RuntimeError:
            raised = True
        assert raised is True
        assert open(p, "rb").read() == before  # finally 已还原


def test_empty_mutation_is_infra_error():
    with tempfile.TemporaryDirectory() as td:
        _p, sb = _mkroot(td)
        r = sb.apply_and_run({}, "atoms/conc/ATOM-X-001.md")
        assert r["verdict"] == "infra_error"


def test_invalid_card_path_rejected():
    with tempfile.TemporaryDirectory() as td:
        _p, sb = _mkroot(td)
        r = sb.apply_mutation({"content": json.dumps({"op": "M1"})}, "tools/x.py")
        assert r["applied"] is False
        r2 = sb.apply_mutation({"content": json.dumps({"op": "M1"})},
                               "atoms/conc/MISSING.md")
        assert r2["applied"] is False


def test_concurrency_lock_blocks_second():
    with tempfile.TemporaryDirectory() as td:
        sb1 = SA.Sandbox(root=td, lock_path=os.path.join(td, ".lock"))
        sb2 = SA.Sandbox(root=td, lock_path=os.path.join(td, ".lock"))
        sb1.acquire()
        try:
            try:
                sb2.acquire()
                blocked = False
            except RuntimeError:
                blocked = True
            assert blocked is True
        finally:
            sb1.release()
        sb2.acquire()
        sb2.release()


def test_findings_for_filters_by_card():
    gj = {"findings": [{"file": "atoms/a.md", "rule": "R1", "severity": "warn"},
                       {"file": "evidence/b.md", "rule": "R2", "severity": "block"}]}
    assert len(SA.Sandbox.findings_for(gj, "atoms/a.md")) == 1
    assert SA.Sandbox.findings_for(gj, "evidence/b.md")[0]["rule"] == "R2"
    assert SA.Sandbox.findings_for(gj, "atoms/zzz.md") == []


def test_real_gate_end_to_end_and_clean():
    """真实跑一次 apply_and_run：判决格式正确、卡还原、受控目录零污染。"""
    card = "atoms/conc/ATOM-CONC-FENCE-001.md"
    if not os.path.exists(os.path.join(ROOT, card)):
        return
    import subprocess
    before = open(os.path.join(ROOT, card), "rb").read()
    sb = SA.Sandbox()
    base = sb.gate_all()
    assert base.get("findings") is not None
    mut = {"mutation_id": "smoke", "attack_type": "rule_blind_spot",
           "content": json.dumps({"op": "M1", "target_rule": "EV-FM-REQUIRED"})}
    with sb:
        res = sb.apply_and_run(mut, card, SA.Sandbox.findings_for(base, card))
    assert res["verdict"] in ("blocked", "escaped", "neutral", "infra_error")
    assert "elapsed_ms" in res
    assert open(os.path.join(ROOT, card), "rb").read() == before
    st = subprocess.run(["git", "status", "--porcelain", "--", "atoms", "evidence"],
                        cwd=ROOT, capture_output=True, text=True)
    assert st.stdout.strip() == ""


def test_selftest_passes():
    assert SA.selftest() == 0
