#!/usr/bin/env python3
"""B2 回归测试：D5 基准源路径解析（库根优先 + `_archive/benchmarks/` 兜底）。

守护：基准源 2026 迁至 `_archive/benchmarks/` 后，两个 D5 门禁曾全红（appendix ERROR=119 /
source_integrity exit 1）。本测试锁定"两处都能解析、且未跟踪判定用相对路径"。
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import d5_appendix_audit as daa  # noqa: E402
import d5_source_integrity as dsi  # noqa: E402


def test_archive_dir_exists_and_has_benches():
    assert dsi.ARCHIVE_BENCH and Path(dsi.ARCHIVE_BENCH).is_dir()
    n = len(list(Path(dsi.ARCHIVE_BENCH).glob("_bench_d5_*.cpp")))
    assert n >= 100, f"归档基准源应 ≥100，实测 {n}"


def test_resolve_bench_finds_archive_file():
    sample = "_bench_d5_04_move.cpp"
    p = daa._resolve_bench(sample)
    assert p is not None, f"{sample} 应能在库根或归档中找到"
    assert p.exists()


def test_resolve_bench_returns_none_for_unknown():
    assert daa._resolve_bench("_bench_d5_ZZZ_not_exist.cpp") is None


def test_collect_disk_files_includes_archive():
    files = dsi.collect_disk_files()
    assert len(files) >= 100
    assert "_bench_d5_04_move.cpp" in files


def test_git_tracked_includes_archive():
    tr = dsi.git_tracked("_bench_d5_*.cpp")
    assert "_bench_d5_04_move.cpp" in tr


def test_appendix_audit_exit_zero():
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "d5_appendix_audit.py")],
                       cwd=str(ROOT), capture_output=True, text=True, timeout=180)
    assert r.returncode == 0, r.stdout[-800:]
    assert "ERROR=0" in r.stdout


def test_source_integrity_exit_zero():
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "d5_source_integrity.py"), "--check"],
                       cwd=str(ROOT), capture_output=True, text=True, timeout=180)
    assert r.returncode == 0, r.stdout[-800:]
