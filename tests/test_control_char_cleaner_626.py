"""626 A2 · 控制字符清洗器回归测试（≥5 例）。"""
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import control_char_cleaner as C  # noqa: E402


def test_selftest_passes():
    assert C.selftest() == 0


def test_scan_detects_control_chars():
    with tempfile.TemporaryDirectory() as td:
        with open(os.path.join(td, "a.md"), "wb") as fh:
            fh.write(b"ok\x08text")
        found = C.scan(td)
        assert len(found) == 1
        assert "0x8" in found[0][1]


def test_scan_clean_dir_returns_empty():
    with tempfile.TemporaryDirectory() as td:
        open(os.path.join(td, "a.md"), "w", encoding="utf-8").write("clean\n")
        assert C.scan(td) == []


def test_fix_removes_only_control_chars():
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "a.md")
        with open(p, "wb") as fh:
            fh.write(b"line1\nverifier\x08x\x0b\nline2\n")
        n = C.clean_file(p)
        assert n == 2
        data = open(p, "rb").read()
        assert b"\x08" not in data and b"\x0b" not in data
        assert data.count(b"\n") == 3      # 换行保留


def test_fix_idempotent():
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "a.md")
        with open(p, "wb") as fh:
            fh.write(b"x\x08y")
        C.clean_file(p)
        assert C.clean_file(p) == 0


def test_repo_data_has_no_control_chars_now():
    # 626 A2 已清洗：data/ 应无残留
    found = C.scan(os.path.join(ROOT, "data"))
    assert found == [], f"仍有控制字符文件: {found}"
