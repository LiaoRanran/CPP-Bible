"""603 任务1.3：编译可复现性引擎 `check_build_reproducibility` 回归测试。

纪律：正反毒样例 + 存釂零误伤 + 可证伪（不裸 except）+ 隔离（不污染仓库）。
"""
from __future__ import annotations

import hashlib
import subprocess
import time
from pathlib import Path

import atom_evidence_replay as replay
import pytest


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


# ── 603 任务3.2：毒样例 P80–P83（验证引擎的判别力；P80/P81 正例、P82/P83 反例）──────
def test_p80_positive_asm_deterministic(tmp_path: Path):
    """P80 正例：同一命令两次独立编译**汇编**（`-S`，无链接器时间戳）⇒ sha 一致。"""
    src = _write_cpp(tmp_path, SIMPLE)
    wd = tmp_path / "wd"
    res = replay.check_build_reproducibility(
        src, ["g++", "-std=c++23", "-O2", "-S", str(src), "-o", "o.asm"], wd,
        check_level="sha", cwd=str(wd))
    assert res.success is True, res.diff_detail
    assert res.first_hash == res.second_hash


def test_p81_positive_date_macro_same_day(tmp_path: Path):
    """P81 正例：`__DATE__`（精度=天）+ `full` 级比对 ⇒ 同一运行内两次编译仍一致。"""
    body = '#include <cstdio>\nint main(){std::printf("%s", __DATE__);return 0;}\n'
    src = _write_cpp(tmp_path, body)
    wd = tmp_path / "wd"
    res = replay.check_build_reproducibility(
        src, ["g++", "-std=c++23", "-O2", "-Wl,--no-insert-timestamp", str(src), "-o", "o.exe"],
        wd, check_level="full", cwd=str(wd))
    assert res.success is True, res.diff_detail
    assert res.symbols_match is True and res.sections_match is True


def test_p82_negative_time_macro_cross_second_detected(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """P82 反例：`__TIME__` 跨秒 ⇒ 两次编译产物不同 ⇒ 引擎须判**不可复现**。

    判别力要点：`__TIME__` 是否跨秒取决于两次编译是否落在不同秒内——天然不稳定。
    为**确定性**触发，这里在第二次编译（`run2`）前注入 >1s 延迟，强制跨秒边界，
    而非依赖"恰好慢到跨秒"（那会让测试随机跳红）。
    """
    body = '#include <cstdio>\nint main(){std::printf("%s", __TIME__);return 0;}\n'
    src = _write_cpp(tmp_path, body)
    wd = tmp_path / "wd"
    real_run = replay.subprocess.run

    def _delay_run2(cmd, **kw):
        if isinstance(cmd, (list, tuple)) and "-o" in cmd:
            out = Path(cmd[cmd.index("-o") + 1])
            if "run2" in str(out):
                time.sleep(1.1)
        return real_run(cmd, **kw)

    monkeypatch.setattr(replay.subprocess, "run", _delay_run2)
    res = replay.check_build_reproducibility(
        src, ["g++", "-std=c++23", "-O2", "-Wl,--no-insert-timestamp", str(src), "-o", "o.exe"],
        wd, check_level="sha", cwd=str(wd))
    assert res.success is False, "跨秒的 __TIME__ 未被检出 ⇒ 判别力缺失"
    assert res.diff_detail is not None and "run1=" in res.diff_detail


def test_p83_debug_path_boundary(tmp_path: Path):
    """P83 反例（边界）：调试信息里的**编译目录**影响产物 sha，但引擎两次运行共用 cwd。

    如实记录引擎的判别边界（非缺陷）：
      (i) 引擎对两次编译使用**同一 cwd**（设计：隔离 `-o` 目标、固定环境），
          故"同 cwd"的 `-g` 判定为可复现；
      (ii) 但"不同工作目录"确实会让 DWARF 的 `DW_AT_comp_dir` 不同 ⇒ sha 不同，
           这一类非确定性**不在本引擎判别范围**。当前各卡命令均为同 cwd 复算，
           不影响 replay / metrics 口径；若要覆盖需引擎按 run 切 cwd（另议）。
    """
    gpp = _gpp()
    body = "int f(int x){return x*3+1;}\nint main(){return f(2);}\n"
    src = _write_cpp(tmp_path, body)
    wd = tmp_path / "wd"

    # (i) 引擎：同 cwd + -g ⇒ 可复现
    same = replay.check_build_reproducibility(
        src, [gpp, "-std=c++23", "-O2", "-g", "-Wl,--no-insert-timestamp",
              str(src), "-o", "o.exe"], wd, check_level="sha", cwd=str(wd))
    assert same.success is True, same.diff_detail

    # (ii) 直接两次编译（不同 cwd、相对源路径）⇒ 调试信息路径不同 ⇒ sha 不同
    for d in ("ca", "cb"):
        (tmp_path / d).mkdir(exist_ok=True)
        (tmp_path / d / "d.cpp").write_text(body, encoding="utf-8")
    outs = []
    for d in ("ca", "cb"):
        r = subprocess.run([gpp, "-std=c++23", "-O2", "-g", "-Wl,--no-insert-timestamp",
                            "d.cpp", "-o", "o.exe"], cwd=str(tmp_path / d),
                           capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        outs.append(hashlib.sha256((tmp_path / d / "o.exe").read_bytes()).hexdigest())
    assert outs[0] != outs[1], "不同 cwd 的 -g 产物应不同（P83 现象未复现）"
