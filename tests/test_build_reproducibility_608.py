"""608 B2 · I2 编译可复现深化回归锁（7+ 用例）。

覆盖：
  * 时间宏漂移判定 `_only_time_macro_diff`（单元，不编译）
  * `--no-symtab` 正确映射 check_level（sha vs full）
  * 跨时间窗口只对前 3 张卡做（调用次数）
  * 真实卡可复现 + 跨时间窗口真编译（慢组，编译真实卡）

本模块已入 `tests/conftest.py::SERIAL_EXTRA`（编译真实卡 + 读真实仓可变状态 ⇒ 慢组串行），
不进 fast 门禁（`-m "not slow"`）；由监工在 `-m slow -n0` 阶段跑。
"""
from __future__ import annotations

from pathlib import Path

import atom_evidence_replay as aer
import pytest
import replay_invariants as ri


# ── 时间宏漂移判定（单元，不编译）────────────────────────────────────────────────
def test_only_time_macro_diff_identical():
    b = b"hello world\x00\x00"
    assert ri._only_time_macro_diff(b, b) is True


def test_only_time_macro_diff_ascii_only():
    # 差异仅落在可打印 ASCII（__TIME__/__DATE__ 串）⇒ 视为时间宏漂移
    a = b"build at 12:00:00\x00\x00"
    b = b"build at 12:00:01\x00\x00"
    assert ri._only_time_macro_diff(a, b) is True


def test_only_time_macro_diff_binary_region():
    # 差异落在非打印二进制区 ⇒ 真不可复现
    a = b"\x00\x01\x02\x03"
    b = b"\x00\x01\x02\xff"
    assert ri._only_time_macro_diff(a, b) is False


def test_only_time_macro_diff_pe_timestamp():
    # PE 头 TimeDateStamp 4 字节差异（即便已关插时间戳也兜底）⇒ 视为时间相关
    # 构造最小 MZ + PE 签名 + 4 字节时间戳差
    base = bytearray(b"MZ" + b"\x00" * 0x3A)
    base[0x3C:0x40] = b"\x80\x00\x00\x00"   # DOS 头 e_lfanew @0x3C → PE 签名在 0x80
    base += b"\x00" * (0x80 - len(base))    # 填洞到 0x80
    base += b"PE\x00\x00"
    base += b"\x00\x00\x00\x00"             # COFF 头 machine（4 字节）
    ts_off = 0x80 + 8                        # COFF 头 +4 后为 TimeDateStamp
    a = bytearray(base)
    a[ts_off:ts_off + 4] = b"\x00\x00\x00\x01"
    b = bytearray(base)
    b[ts_off:ts_off + 4] = b"\x00\x00\x00\x02"
    # 其余字节一致，仅时间戳区域不同
    assert ri._only_time_macro_diff(bytes(a), bytes(b)) is True


# ── check_level 映射（monkeypatch，不编译）──────────────────────────────────────
def _fake_result(success=True, symbols_match=None, sections_match=None,
                 first_hash="aaa", second_hash="aaa"):
    return aer.BuildReproResult(
        success=success, first_hash=first_hash, second_hash=second_hash,
        symbols_match=symbols_match, sections_match=sections_match,
        diff_detail=None, compile_exit_code=0, compile_stderr="", duration_ms=0)


def _fake_engine_factory(result, log: dict | None = None):
    """返回假引擎：除返回 result 外，还在 work_dir/run1/ 写占位二进制，
    以免真函数里 `bin_a = ...read_bytes()` 因文件不存在而崩（不真正编译）。"""

    def _eng(*, source_path, compile_cmd, work_dir, output_name=None,
             ccaches_disable=True, check_level="sha", cwd=None):
        if log is not None:
            log.setdefault("levels", []).append(check_level)
            log["engine"] = log.get("engine", 0) + 1
        bin_name = Path(source_path).name
        p = Path(work_dir) / "run1"
        p.mkdir(parents=True, exist_ok=True)
        (p / bin_name).write_bytes(b"\x00" * 64)
        return result

    return _eng


def test_no_symtab_maps_check_level(monkeypatch: pytest.MonkeyPatch):
    seen: dict = {}
    monkeypatch.setattr(aer, "check_build_reproducibility",
                        _fake_engine_factory(_fake_result(), seen))
    monkeypatch.setattr(aer, "_recompile_invariant", lambda *a, **k: ("ok", "x"))

    ri.check_build_reproducibility(n_cards=1, no_symtab=True)
    ri.check_build_reproducibility(n_cards=1, no_symtab=False)
    assert seen["levels"].count("sha") == 1
    assert seen["levels"].count("full") == 1


def test_symbol_section_not_false(monkeypatch: pytest.MonkeyPatch):
    # nm/objdump 不可用（返回 None）时不应误判 fail
    monkeypatch.setattr(aer, "check_build_reproducibility",
                        _fake_engine_factory(_fake_result(symbols_match=None,
                                                         sections_match=None)))
    monkeypatch.setattr(aer, "_recompile_invariant", lambda *a, **k: ("ok", "x"))
    res = ri.check_build_reproducibility(n_cards=1)
    assert res["passed"] is True
    # 符号/段为 None（不可检）时该卡仍通过，不会 False 误杀


def test_cross_time_only_first_three(monkeypatch: pytest.MonkeyPatch):
    seen: dict = {}
    monkeypatch.setattr(aer, "check_build_reproducibility",
                        _fake_engine_factory(_fake_result(first_hash="aaa",
                                                         second_hash="aaa"), seen))
    monkeypatch.setattr(aer, "_recompile_invariant", lambda *a, **k: ("ok", "x"))
    # n_cards=3, cross_time=True ⇒ 每张卡 2 次引擎调用（短窗口 + 跨时间）= 6
    res = ri.check_build_reproducibility(n_cards=3, cross_time=True)
    assert seen["engine"] == 6
    assert all(c["cross"] != "真不可复现（fail）" for c in res["cards"])


# ── 真实卡（慢组，真编译）──────────────────────────────────────────────────────
def test_real_card_reproducible():
    res = ri.check_build_reproducibility(n_cards=1)
    assert res["passed"] is True
    assert res["cards"][0]["match"] is True


def test_real_card_cross_time():
    res = ri.check_build_reproducibility(n_cards=1, cross_time=True)
    assert res["passed"] is True
    assert res["cards"][0]["cross"] != "真不可复现（fail）"
