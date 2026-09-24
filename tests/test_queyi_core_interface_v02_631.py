"""631 F1 · Core 接口 v0.2 单测（6 例）。"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import queyi_core_interface_v02_631 as T


def test_five_interfaces_present():
    m = T.measure()
    assert m["n_interfaces"] == 5
    assert set(T.INTERFACES) == {"Claim", "Evidence", "Verifier",
                                 "Authority", "Attacker"}


def test_each_interface_has_methods_and_docstrings():
    m = T.measure()
    for r in m["rows"]:
        assert r["n_methods"] >= 4, r["interface"]
        assert r["methods_with_doc"] == r["n_methods"], \
            f"{r['interface']} 有方法缺 docstring"
        # 全部方法的 docstring 非空
        for meth in r["methods"]:
            assert T.doc_of(T.INTERFACES[r["interface"]]["cls"], meth)


def test_all_methods_unimplemented():
    """§十 F1.2：只定义不实现，方法体必须 raise NotImplementedError。"""
    for meta in T.INTERFACES.values():
        for meth in T.public_methods(meta["cls"]):
            assert T._raises(meta["cls"], meth), f"{meta['cls'].__name__}.{meth} 已实现"


def test_verifier_and_attacker_new_capabilities():
    vm = T.public_methods(T.Verifier)
    am = T.public_methods(T.Attacker)
    assert "independent_hook" in vm, "Verifier 需含独立验证者钩子"
    assert "attest" in vm
    assert "objective" in am, "Attacker 需含目标函数"
    assert "revert" in am, "Attacker 需含 revert 契约"


def test_authority_append_only_semantics():
    am = T.public_methods(T.Authority)
    assert "append" in am and "chain_verify" in am
    assert "transparency_log" in am and "human_decision" in am


def test_readonly_and_report():
    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain"], cwd=T.ROOT,
                           capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    T.measure()
    T.write_report()
    assert snap() == before, "只读：不实例化业务、不改工作区"
    text = open(T.OUT_MD, encoding="utf-8").read()
    for kw in ("接口清单与实现状态映射", "v0.1 → v0.2 的差异",
               "雷1 剥离触发标准推进情况", "诚实登记"):
        assert kw in text, f"报告缺：{kw}"
    payload = json.load(open(T.OUT_JSON, encoding="utf-8"))
    assert payload["version"] == "v0.2"
    assert payload["implemented"] == 0, "必须 0 个已实现"
    assert T.selftest() == 0
