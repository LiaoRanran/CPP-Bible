"""641 C1–C3 · 第二领域（toy_math）与通用性证明回归测试。

锁的是"**同一个内核、换领域插件就能跑**"：
1. toy 领域语义（解析/求值/逆运算交叉验算）与 4 条外置规则真的会开火；
2. toy 的 run 与 C++ 的 run 走**同一套** `VerificationRun` 机制（封存/自哈希/投影）；
3. **kernel_digest 两领域相同** ⇒ 内核为跨领域零改动（C3 的核心断言）；
4. toy 插件**不 import** 任何 C++ 领域模块（领域插件彼此独立）。
"""
from __future__ import annotations

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import queyi_core_cpp_641 as cpp  # noqa: E402
import queyi_core_toy_641 as toy  # noqa: E402
import queyi_core_v10_641 as core  # noqa: E402


def test_parse_and_evaluate():
    assert toy.parse("2+3=5") == (2, "+", 3, 5)
    assert toy.parse("hello") is None
    assert toy.evaluate("6*7=42")[0] == "ok"
    assert toy.evaluate("2+2=5")[0] == "wrong"
    assert toy.evaluate("9/0=0")[0] == "div0"
    assert toy.evaluate("hello")[0] == "syntax"


def test_cross_check_is_an_independent_second_method():
    assert toy.cross_check("2+3=5") == "confirm"
    assert toy.cross_check("2+2=5") == "refute"
    assert toy.cross_check("hello") == "unknown"


def test_toy_domain_contract():
    d = toy.ToyDomain()
    assert d.domain_id == "toy_math"
    assert d.canonicalize(b"a\r\n") == b"a\n"
    assert len(d.load_rules()) == 4
    assert d.environment()["domain"] == "toy_math"


def test_toy_run_states():
    run = toy.run_verification()
    st = run.results["toy"]["decision_states"]
    assert st["fail"] == 3 and st["pass"] == 5, str(st)
    assert run.verify_integrity()


def test_kernel_digest_is_the_same_for_both_domains():
    """C3 核心断言：同一内核零改动 ⇒ 两个领域的 `kernel_digest` 必然相同。"""
    cpp_run = cpp.run_verification(limit=5)
    toy_run = toy.run_verification()
    assert cpp_run.digests["kernel_digest"] == toy_run.digests["kernel_digest"]
    assert cpp_run.digests["kernel_digest"] == core.kernel_self_digest()


def test_toy_uses_the_same_kernel_mechanisms():
    run = toy.run_verification()
    assert run.schema_version == core.SCHEMA_VERSION
    assert run.project("summary")["kind"] == "summary"      # 内核内置投影同样可用
    assert run.project("toy")["n_statements"] == len(toy.DEFAULT_CORPUS)
    assert all(d.state in core.FOUR_STATES for d in run.decisions)


def test_run_id_differs_between_domains_but_mechanism_is_shared():
    cpp_run = cpp.run_verification(limit=5)
    toy_run = toy.run_verification()
    assert cpp_run.run_id != toy_run.run_id          # 领域/输入不同 ⇒ run 不同
    assert cpp_run.schema_version == toy_run.schema_version


def test_toy_pack_does_not_import_cpp_domain():
    imports = core.module_imports(os.path.join(ROOT, "tools", "queyi_core_toy_641.py"))
    assert "queyi_core_cpp_641" not in imports
    assert "gate_engine" not in imports


def test_unregistered_projection_still_fails_loud_on_toy():
    run = toy.run_verification()
    # 注意：投影注册表是**进程级全局**（领域插件注册进去），故这里用一个**谁都不会注册**的名字
    with pytest.raises(KeyError):
        run.project("_never_registered_projection_641")


def test_cli_check_passes():
    assert toy.main(["--check"]) == 0
