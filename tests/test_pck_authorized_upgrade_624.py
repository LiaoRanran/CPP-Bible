"""624 E1 PCK authorized 提升 · 单元测试（≥4 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import pck_authorized_upgrade_624 as m  # noqa: E402


def test_certs_and_baseline():
    certs = m.load_certs()
    assert len(certs) == 83
    st = m.stats(certs)
    assert st["authorized"] == 27


def test_w2_in_nonempty():
    ina = m.w2_in_atoms()
    assert isinstance(ina, set) and len(ina) > 0


def test_candidates_identifies_pending_atom():
    fake = [("ATOM-FAKE-999.pck.yaml", {"human_authority": {"status": "pending"}})]
    assert m.candidates(fake, {"ATOM-FAKE-999"}) == ["ATOM-FAKE-999"]


def test_candidates_excludes_approved_and_evidence():
    assert m.candidates(
        [("ATOM-X.pck.yaml", {"human_authority": {"status": "approved"}})], {"ATOM-X"}) == []
    assert m.candidates(
        [("EV-X.pck.yaml", {"human_authority": {"status": "pending"}})], {"EV-X"}) == []


def test_no_machine_candidates_currently():
    # 诚实登记：真实语料下候选为 0（不代签）
    assert m.candidates(m.load_certs(), m.w2_in_atoms()) == []


def test_selftest_passes():
    assert m.selftest() == 0
