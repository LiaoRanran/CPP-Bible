#!/usr/bin/env python3
"""E3 回归测试：merkle_proof_613（单文件 Merkle 包含证明）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import merkle_proof_613 as e3  # noqa: E402


def test_roots_exist():
    doc = e3.load_roots()
    assert doc and "dirs" in doc
    assert set(doc["dirs"]) >= {"atoms", "evidence"}


def test_sample_files_returns_paths():
    # iter_files 返回 (rel, abs) 元组 ⇒ sample_files 必须解出绝对路径
    files = e3.sample_files("atoms", 2)
    assert files and all(isinstance(p, Path) and p.is_file() for p in files)


def test_all_proofs_verify():
    rows = e3.build_proofs(2)
    assert rows, "至少要能生成证明"
    bad = [r for r in rows if not r["verified"]]
    assert not bad, f"存在验证失败的证明：{bad[:2]}"


def test_proofs_cover_multiple_dirs():
    rows = e3.build_proofs(2)
    assert len({r["dir"] for r in rows}) >= 3


def test_proof_has_steps_and_root():
    rows = e3.build_proofs(1)
    assert rows and all(r["steps"] >= 0 for r in rows)
    assert all(r["root"].endswith("…") for r in rows)


def test_render_sections():
    page = e3.render(e3.build_proofs(1), e3.load_roots())
    assert "Merkle 包含证明" in page
    assert "逐条证明" in page and "不能证明" in page


def test_check_passes():
    assert e3.main(["--check"]) == 0
