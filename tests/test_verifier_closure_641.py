"""641 D1–D3 · Verifier Closure（信任根闭包）回归测试。

锁的是**闭包完整 + 缺失即 FAIL + run 可自述版本**：
1. 闭包覆盖内核 / 适配器 / 5 个 CORE_TOOLS / 配置信任根，且 digest 确定；
2. **缺失即 FAIL**（不是 warning）：假装缺失与"读不到"两条路径都必须 FAIL；
3. run 绑定 `verifier_closure_digest` / `policy_digest` / `source_revision`；
4. 攻击测试**不真删**任何信任根文件（受控/信任根零破坏）。
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import queyi_core_v10_641 as core  # noqa: E402
import verifier_closure_641 as vc  # noqa: E402


def test_closure_covers_kernel_adapter_and_core_tools():
    cl = vc.build_closure()
    paths = [e["path"] for e in cl["files"]]
    assert "tools/queyi_core_v10_641.py" in paths
    assert "tools/queyi_core_cpp_641.py" in paths
    for t in vc.CORE_TOOLS:
        assert f"tools/{t}.py" in paths, f"CORE_TOOL {t} 必须在闭包里"
    assert "pyproject.toml" in paths and "tools/.tool_checksums" in paths


def test_closure_is_ok_and_deterministic_on_real_repo():
    cl = vc.build_closure()
    assert cl["status"] == "OK" and cl["n_missing"] == 0
    assert vc.build_closure()["digest"] == cl["digest"]
    assert len(cl["digest"]) == 64


def test_missing_trust_root_is_fail_not_warning():
    """D2：缺失即 FAIL（攻击测试，**不真删**文件）。"""
    att = vc.simulate_missing(["pyproject.toml"])
    assert att["status"] == "FAIL"
    assert att["missing"] == ["pyproject.toml"]
    assert att["digest"] != vc.build_closure()["digest"]


def test_unreadable_file_counts_as_missing(monkeypatch):
    """另一条路径：文件在但**读不到**（等价删除）⇒ 同样 FAIL。"""
    orig = vc.sha256_file
    monkeypatch.setattr(vc, "sha256_file",
                        lambda p: None if p.endswith("pyproject.toml") else orig(p))
    cl = vc.build_closure()
    assert cl["status"] == "FAIL" and "pyproject.toml" in cl["missing"]


def test_annotate_binds_all_three_digests():
    b = vc.annotate(core.VerificationRunBuilder("cpp", source_revision="x"),
                    policy_digest="p1")
    run = b.seal()
    assert run.digests["verifier_closure_digest"] == vc.closure_digest()
    assert run.digests["policy_digest"] == "p1"
    assert run.digests["source_revision"] == vc.source_revision()
    assert run.verify_integrity()
    assert run.results["closure"]["status"] == "OK"


def test_closure_change_changes_closure_digest():
    """改任一闭包成员 ⇒ digest 变（run 能检测"用哪版内核/规则跑的"）。"""
    base = vc.build_closure()["digest"]
    att = vc.simulate_missing(["tools/.tool_checksums"])
    assert att["digest"] != base


def test_cli_check_and_simulate_missing():
    assert vc.main(["--check"]) == 0
    assert vc.main(["--simulate-missing", "pyproject.toml"]) == 0      # FAIL ⇒ 退出 0（判定生效）
    assert vc.main(["--simulate-missing", "no_such_file_here.txt"]) == 1  # 无缺失 ⇒ 不该 FAIL
