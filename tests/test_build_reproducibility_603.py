"""603 任务1.3：编译可复现性引擎 `check_build_reproducibility` 回归测试。

纪律：正反毒样例 + 存釂零误伤 + 可证伪（不裸 except）+ 隔离（不污染仓库）。
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

import atom_evidence_replay as replay


def _write_cpp(tmp_path: Path, body: str, name: str = "sample.cpp") -> Path:
    p = tmp_path / name
    p.write_text(body, encoding="utf-8")
    return p


def _gpp() -> str:
    from toolchain import resolve_gpp
    return resolve_gpp()


SIMPLE = "int main(){int s=0;for(int i=0;i<10;++i)s+=i;return s;}\n"


def test_positive_sha_reproducible(tmp_path: Path):
    src = _write_cpp(tmp_path, SIMPLE)
    wd = tmp_path / "wd"
    res = replay.check_build_reproducibility(
        src, ["g++", "-std=c++23", "-O2", "-Wl,--no-insert-timestamp", str(src), "-o", "o.exe"], wd,
        check_level="sha", cwd=str(wd))
    assert res.success is True
    assert res.first_hash == res.second_hash
    assert res.compile_exit_code == 0
    assert res.symbols_match is None and res.sections_match is None


def test_positive_full_symbols_and_sections(tmp_path: Path):
    src = _write_cpp(tmp_path, SIMPLE)
    wd = tmp_path / "wd"
    res = replay.check_build_reproducibility(
        src, ["g++", "-std=c++23", "-O2", "-Wl,--no-insert-timestamp", str(src), "-o", "o.exe"], wd,
        check_level="full", cwd=str(wd))
    assert res.success is True
    assert res.symbols_match is True
    assert res.sections_match is True


def test_positive_date_macro_same_day(tmp_path: Path):
    # __DATE__ 精确到天，同一秒内两次编译 sha 仍一致（短窗口确定）
    body = '#include <cstdio>\nint main(){std::printf("%s", __DATE__);return 0;}\n'
    src = _write_cpp(tmp_path, body)
    wd = tmp_path / "wd"
    res = replay.check_build_reproducibility(
        src, ["g++", "-std=c++23", "-O2", "-Wl,--no-insert-timestamp", str(src), "-o", "o.exe"], wd,
        check_level="sha", cwd=str(wd))
    assert res.success is True, res.diff_detail


def test_negative_compile_failure(tmp_path: Path):
    src = _write_cpp(tmp_path, "int main(){ this is not c++ }\n")
    wd = tmp_path / "wd"
    res = replay.check_build_reproducibility(
        src, ["g++", "-std=c++23", "-O2", "-Wl,--no-insert-timestamp", str(src), "-o", "o.exe"], wd,
        check_level="sha", cwd=str(wd))
    assert res.success is False
    assert res.compile_exit_code != 0
    assert res.compile_stderr.strip() != ""


def test_negative_tampered_binary_detected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    src = _write_cpp(tmp_path, SIMPLE)
    wd = tmp_path / "wd"
    real_run = replay.subprocess.run

    def _flip_run2(cmd, **kw):
        r = real_run(cmd, **kw)
        if isinstance(cmd, (list, tuple)) and "-o" in cmd:
            o = Path(cmd[cmd.index("-o") + 1])
            if "run2" in str(o) and o.is_file():       # 在第二次产物上篡改首字节 ⇒ run1≠run2
                b = bytearray(o.read_bytes())
                b[0] ^= 0xFF
                o.write_bytes(bytes(b))
        return r

    monkeypatch.setattr(replay.subprocess, "run", _flip_run2)
    res = replay.check_build_reproducibility(
        src, ["g++", "-std=c++23", "-O2", "-Wl,--no-insert-timestamp", str(src), "-o", "o.exe"], wd,
        check_level="sha", cwd=str(wd))
    assert res.success is False
    assert res.diff_detail is not None and "run1=" in res.diff_detail


def test_negative_missing_source(tmp_path: Path):
    wd = tmp_path / "wd"
    res = replay.check_build_reproducibility(
        tmp_path / "does_not_exist.cpp",
        ["g++", "-std=c++23", "-O2", "x.cpp", "-o", "o.exe"], wd,
        check_level="sha", cwd=str(wd))
    assert res.compile_exit_code == -1          # 源不存在：明确错误返回，不崩溃
    assert "source" in (res.compile_stderr or res.diff_detail or "")


def test_negative_missing_compiler(tmp_path: Path):
    src = _write_cpp(tmp_path, SIMPLE)
    wd = tmp_path / "wd"
    res = replay.check_build_reproducibility(
        src, ["g++_no_such_binary_xyz", str(src), "-o", "o.exe"], wd,
        check_level="sha", cwd=str(wd))
    assert res.compile_exit_code != 0           # 编译器起不来：返回错误，不抛异常


def test_idempotent(tmp_path: Path):
    src = _write_cpp(tmp_path, SIMPLE)
    wd = tmp_path / "wd"
    args = (src, ["g++", "-std=c++23", "-O2", "-Wl,--no-insert-timestamp", str(src), "-o", "o.exe"], wd)
    kw = dict(check_level="sha", cwd=str(wd))
    r1 = replay.check_build_reproducibility(*args, **kw)
    r2 = replay.check_build_reproducibility(*args, **kw)
    assert (r1.success, r1.first_hash, r1.second_hash, r1.symbols_match,
            r1.sections_match, r1.compile_exit_code, r1.compile_stderr) == \
           (r2.success, r2.first_hash, r2.second_hash, r2.symbols_match,
            r2.sections_match, r2.compile_exit_code, r2.compile_stderr)


def test_isolation_does_not_pollute(tmp_path: Path):
    src = _write_cpp(tmp_path, SIMPLE)
    wd = tmp_path / "wd"
    before = hashlib.sha256(src.read_bytes()).hexdigest()
    replay.check_build_reproducibility(
        src, ["g++", "-std=c++23", "-O2", "-Wl,--no-insert-timestamp", str(src), "-o", "o.exe"], wd,
        check_level="sha", cwd=str(wd))
    after = hashlib.sha256(src.read_bytes()).hexdigest()
    assert before == after                     # 源文件未被改动
    assert (wd / "run1").is_dir() and (wd / "run2").is_dir()
    assert set(p.name for p in wd.iterdir()) == {"run1", "run2"}  # work_dir 顶层无散落文件
