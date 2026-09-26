"""642 B2 · kernel_minimality_audit_642 单测（最小性四判据 + 依赖方向 + 只审计不改）。
编号 B2-1..B2-7。
"""
from __future__ import annotations

import hashlib

import kernel_minimality_audit_642 as K


def _digest() -> str:
    with open(K.KERNEL, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# B2-1：内核零领域依赖（AST 机械证明，与 641 同源口径）
def test_kernel_has_zero_domain_imports():
    a = K.audit()
    assert a["domain_imports"] == []
    assert a["forbidden_blacklist_size"] >= 14


# B2-2：内核零非标准库依赖
def test_kernel_has_zero_non_stdlib_imports():
    assert K.audit()["non_stdlib_imports"] == []


# B2-3：内核零高攻击面能力（无网络/子进程/动态执行/pickle/ctypes）
def test_kernel_has_no_dangerous_capability():
    a = K.audit()
    assert a["dangerous"] == []
    for bad in ("subprocess", "socket", "urllib", "eval", "exec", "pickle", "ctypes"):
        assert bad not in a["imports"]


# B2-4：写盘面收敛（内核只写 data/ 下的两个声明常量）
def test_kernel_write_surface_is_declared():
    a = K.audit()
    assert sorted(a["write_paths"]) == ["OUT_JSON", "OUT_MD"]


# B2-5：依赖方向双向核验（适配器 → 内核 ✅；内核 → 适配器 ❌）
def test_dependency_direction_both_ways():
    a = K.audit()
    assert a["kernel_imports_adapters"] == []
    assert all(a["adapters_import_kernel"].values())


# B2-6：只审计不改（内核源码字节不变）+ 建议移出项确实存在
def test_audit_is_readonly_and_move_out_is_real():
    before = _digest()
    a = K.audit()
    assert _digest() == before, "最小性审计不得改动内核源码"
    present = set(a["symbols"]["classes"]) | set(a["symbols"]["functions"]) \
        | set(a["symbols"]["constants"])
    assert {m["symbol"] for m in a["move_out"]} <= present
    assert len(a["move_out"]) >= 3


# B2-7：--check 自检通过
def test_selftest():
    assert K.selftest() == 0
