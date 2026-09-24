"""632 A2 · ci_pytest_final_clear_632 单测（≥5 例，全只读）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import ci_pytest_final_clear_632 as clr  # noqa: E402


def test_load_remaining_items_five(tmp_path):
    md = tmp_path / "ci.md"
    md.write_text(
        "# t\n- `tests/a.py::test_x`\n- `tests/b.py::test_y`\n"
        "- `tests/a.py::test_x`\n- `tests/c.py::test_z`\n"
        "- `tests/d.py::test_w`\n- `tests/e.py::test_v`\n",
        encoding="utf-8")
    items = clr.load_remaining_items(md)
    assert len(items) == 5, items


def test_load_remaining_items_missing_returns_empty():
    assert clr.load_remaining_items(Path("/nope.md")) == []


def test_residue_present_true_when_dir_exists(tmp_path):
    assert clr.residue_present(tmp_path) is False
    (tmp_path / "_arch_v21").mkdir()
    assert clr.residue_present(tmp_path) is True


def test_residue_present_false_on_empty_tree(tmp_path):
    assert clr.residue_present(tmp_path) is False


def test_read_text_robust_utf8(tmp_path):
    p = tmp_path / "u.txt"
    p.write_text("正常 UTF-8 文本\n", encoding="utf-8")
    assert "UTF-8" in clr.read_text_robust(p)


def test_read_text_robust_utf16(tmp_path):
    p = tmp_path / "u.txt"
    p.write_bytes("正常 UTF-16 文本\n".encode("utf-16"))
    assert "UTF-16" in clr.read_text_robust(p)


def test_check_exit_zero():
    assert clr.main(["--check"]) == 0
