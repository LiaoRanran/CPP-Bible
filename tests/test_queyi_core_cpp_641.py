"""641 B1–B5 · C++ 领域插件与适配器回归测试。

锁的是"**内核 + C++ 适配器 == legacy**"这一对账关系，以及适配器的**安全边界**：
1. B1 canonicalize / 内容寻址（BOM、CRLF、路径无关）；
2. B2 规则**外置**加载（67 条）与 legacy 规则清单一致、policy_digest 稳定；
3. B3 VerifierPort 产出四态，且不改 `gate_engine`；
4. B4 Attacker **绝不真变异**（dry-run + 受控零污染）、Authority **不代签**；
5. B5 run 封存自洽、投影从 run 派生、对账差异可归因；
6. **依赖方向**：适配器 import 内核，内核**不** import 适配器（AST 机械证明）。
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import queyi_core_cpp_641 as cpp  # noqa: E402
import queyi_core_v10_641 as core  # noqa: E402


def test_canonicalize_strips_bom_and_crlf():
    assert cpp.canonicalize(b"\xef\xbb\xbfa\r\nb") == b"a\nb\n"
    assert cpp.canonicalize(b"a\nb") == b"a\nb\n"


def test_artifacts_are_content_addressed():
    arts = cpp.build_artifacts(limit=6)
    assert len(arts) == 6
    assert len({a.artifact_id for a in arts}) == 6
    assert all(a.uri and "\\" not in a.uri for a in arts)


def test_rule_loading_matches_legacy_inventory():
    """B2：外置加载的规则清单必须与 `gate_engine.RULES` **逐条一致**。"""
    import gate_engine as ge
    rules = cpp.load_rules()
    assert len(rules) == len(ge.RULES) == 67
    assert sorted(r.rule_id for r in rules) == sorted(r.id for r in ge.RULES)
    assert {r.severity for r in rules} <= {"block", "warn", "advice"}


def test_policy_digest_is_stable():
    assert cpp.policy_digest() == core.RuleEngine(cpp.load_rules()).policy_digest
    assert len(cpp.policy_digest()) == 64


def test_verifier_port_yields_four_state_decision():
    arts = cpp.build_artifacts(limit=3)
    pol = core.PolicyRef("cpp_gate_rules", digest=cpp.policy_digest())
    d = cpp.CppVerifier().verify(arts[0], pol)
    assert d.state in core.FOUR_STATES
    assert d.policy_ref == pol.digest


def test_attacker_never_mutates_and_restore_proves_clean():
    """B4 安全边界：dry-run 施加 0 变异；`restore()` 实证受控目录零污染。"""
    at = cpp.CppAttacker()
    r = at.attack(cpp.build_artifacts(limit=3), [])
    assert r["applied"] == 0 and r["mode"] == "dry_run"
    assert at.restore() is True


def test_authority_append_is_staged_only():
    au = cpp.CppAuthority()
    ev = au.append(core.Decision.make("a1", "pass"))
    assert ev.startswith("staged:")        # 不代签、不落库
    assert isinstance(au.verify_chain(), bool)


def test_run_is_sealed_and_binds_digests():
    run = cpp.run_verification(limit=5)
    assert run.verify_integrity()
    assert run.domain == "cpp"
    assert "policy_digest" in run.digests
    assert "kernel_digest" in run.digests          # 通用性证明的锚
    assert run.digests["kernel_digest"] == core.kernel_self_digest()
    assert run.results["controlled_clean"] is True


def test_projections_derive_from_sealed_run():
    run = cpp.run_verification(limit=5)
    for kind in ("w2", "gate", "inventory", "pck", "textbook", "dashboard"):
        assert run.project(kind)["run_id"] == run.run_id
    assert run.project("inventory")["n_cards"] == run.results["inventory"]["n_cards"]


def test_reconcile_reports_zero_unattributed_diff_on_rules():
    run = cpp.run_verification(limit=5)
    rec = cpp.reconcile(run)
    by_metric = {r["metric"]: r for r in rec["rows"]}
    assert by_metric["规则条数"]["kernel"] == by_metric["规则条数"]["legacy"]
    assert by_metric["规则 ID 集合"]["kernel"] == "same"
    assert by_metric["W2 节点数"]["kernel"] == by_metric["W2 节点数"]["legacy"]


def test_kernel_does_not_import_adapter():
    """§四.2 依赖方向：**内核 ← 适配器**，不能反向（AST 机械证明）。"""
    kernel_imports = core.module_imports(os.path.join(ROOT, "tools", "queyi_core_v10_641.py"))
    assert "queyi_core_cpp_641" not in kernel_imports
    assert "gate_engine" not in kernel_imports
    adapter_imports = core.module_imports(os.path.join(ROOT, "tools", "queyi_core_cpp_641.py"))
    assert "queyi_core_v10_641" in adapter_imports


def test_cli_check_passes():
    assert cpp.main(["--check"]) == 0
