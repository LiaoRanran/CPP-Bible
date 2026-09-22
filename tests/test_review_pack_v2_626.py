"""626 E2 · Review Pack v2 回归测试（≥8 例）。"""
import json
import os
import sys
import tempfile
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import review_pack_v2_626 as RP  # noqa: E402

DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
REVIEW_ZIP = os.path.join(DESKTOP, "阙疑_ReviewPack_v2_20260922.zip")
EVID_ZIP = os.path.join(DESKTOP, "阙疑_EvidencePack_Top10_20260922.zip")


def _g() -> RP.ReviewPackGenerator:
    return RP.ReviewPackGenerator()


def test_selftest_passes():
    assert RP.selftest() == 0


def test_review_pack_generation():
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "rp.zip")
        _g().generate_review_pack(p)
        assert os.path.exists(p)
        with zipfile.ZipFile(p) as z:
            names = z.namelist()
        assert "SNAPSHOT_MANIFEST.json" in names
        assert "01_review_items.json" in names
        assert not any("\\" in n for n in names)


def test_evidence_pack_generation():
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "ep.zip")
        r = _g().generate_evidence_pack(p, top_n=5)
        assert r["items"] == 5
        assert r["html_pages"] == 5
        with zipfile.ZipFile(p) as z:
            names = z.namelist()
        assert any(n.startswith("pages/") and n.endswith(".html") for n in names)


def test_validate_pack_ok_and_bad():
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "rp.zip")
        _g().generate_review_pack(p)
        v = _g().validate_pack(p)
        assert v["ok"] and v["backslash"] == 0 and v["has_manifest"]
        bad = os.path.join(td, "bad.zip")
        with zipfile.ZipFile(bad, "w") as z:
            z.writestr("a.md", "x")
        vb = _g().validate_pack(bad)
        assert not vb["ok"] and not vb["has_manifest"]


def test_control_chars_cleaned():
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "ep.zip")
        _g().generate_evidence_pack(p, top_n=3)
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if n.endswith((".md", ".json", ".html")):
                    assert b"\x08" not in z.read(n) and b"\x0b" not in z.read(n)


def test_snapshot_manifest_binds_git_sha():
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "rp.zip")
        _g().generate_review_pack(p)
        with zipfile.ZipFile(p) as z:
            m = json.loads(z.read("SNAPSHOT_MANIFEST.json"))
        assert m["git_sha"] and m["git_sha"] != "unknown"
        assert m["path_separator"] == "/"
        assert m["unique_review_items"] == 93


def test_filter_by_item_ids():
    g = _g()
    ids = [it.review_item_id for it in g.review.sorted_by_ambiguity()[:3]]
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "ep.zip")
        r = g.generate_evidence_pack(p, review_item_ids=ids)
        assert r["items"] == 3


def test_empty_items_list():
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "ep.zip")
        r = _g().generate_evidence_pack(p, review_item_ids=[])
        assert r["items"] == 0
        assert os.path.exists(p)


def test_desktop_packs_exist_and_valid():
    if os.path.exists(REVIEW_ZIP):
        v = _g().validate_pack(REVIEW_ZIP)
        assert v["ok"], str(v)
    if os.path.exists(EVID_ZIP):
        v = _g().validate_pack(EVID_ZIP)
        assert v["ok"], str(v)
