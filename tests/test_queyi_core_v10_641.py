"""641 A1–A6 · QueYi Core 协议内核 v1.0 回归测试。

锁的是**内核机制本身**（与领域数据无关）：
1. 内容寻址：同内容同 ID（CRLF/LF/路径无关）、不同内容不同 ID（A2）；
2. Evidence/Decision 原语的确定性与四态约束（A3/A4）；
3. VerificationRun 构建→封存→只读→自哈希→篡改检测（A5）；
4. 投影从封存 run 确定性派生；未注册投影 fail-loud（A6）；
5. **内核零领域依赖的 AST 机械证明**（§四.2）+ 端口抽象不可实例化（A1）。
"""
from __future__ import annotations

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import queyi_core_v10_641 as core  # noqa: E402


def _art(content: bytes = b"x = 1\n", kind: str = "text", uri: str = "",
         metadata: dict | None = None) -> core.Artifact:
    return core.Artifact.from_bytes(content, kind, uri=uri, metadata=metadata)


# ── A2：内容寻址 ─────────────────────────────────────────────────────────────
def test_content_addressing_same_content_same_id():
    a_crlf = _art(b"int main(){}\r\n", uri="win\\path\\a.cpp")
    a_lf = _art(b"int main(){}\n", uri="posix/path/b.cpp")
    assert a_crlf.artifact_id == a_lf.artifact_id, "CRLF/LF 与路径不同不得影响内容寻址"
    assert a_crlf.content_digest == a_lf.content_digest


def test_content_addressing_different_content_different_id():
    assert _art(b"a\n").artifact_id != _art(b"b\n").artifact_id
    assert _art(b"a\n").artifact_id != _art(b"a\n\n").artifact_id


def test_uri_normalized_to_posix():
    assert _art(uri="a\\b\\c").uri == "a/b/c"


def test_artifact_roundtrip_dict():
    a = _art(metadata={"k": 1})
    d = a.to_dict()
    assert d["artifact_id"] == a.artifact_id and d["metadata"]["k"] == 1


# ── A3：Evidence ─────────────────────────────────────────────────────────────
def test_evidence_id_is_deterministic_and_order_insensitive():
    e1 = core.Evidence.make(["b", "a"], "replay", {"cmd": "g++"}, "high")
    e2 = core.Evidence.make(["a", "b"], "replay", {"cmd": "g++"}, "high")
    assert e1.evidence_id == e2.evidence_id
    assert set(e1.artifact_ids) == {"a", "b"}


def test_evidence_result_rejects_unknown_state():
    with pytest.raises(ValueError):
        core.EvidenceResult("e1", "maybe")
    assert core.EvidenceResult("e1", "infra").status == "infra"


# ── A4：Decision 四态 ────────────────────────────────────────────────────────
def test_decision_rejects_state_outside_four():
    with pytest.raises(ValueError):
        core.Decision.make("a1", "maybe")
    for s in core.FOUR_STATES:
        assert core.Decision.make("a1", s).state == s


def test_decision_id_deterministic_for_dedup():
    d1 = core.Decision.make("a1", "pass", reasons=["ok"], rule_ids=["R1"])
    d2 = core.Decision.make("a1", "pass", reasons=["ok"], rule_ids=["R1"])
    assert d1.decision_id == d2.decision_id


def test_decision_v2_interop_roundtrip():
    for st in core.FOUR_STATES:
        d = core.Decision.make("a1", st, reasons=["r"], rule_ids=["R1"])
        v2 = d.to_decision_event_v2()
        back = core.Decision.from_decision_event_v2(v2)
        assert back.state == st, f"{st} 往返丢失"
        assert back.artifact_id == d.artifact_id


# ── 通用规则引擎（B2 的引擎侧）───────────────────────────────────────────────
def test_rule_engine_is_deterministic_and_domain_free():
    rules = [core.Rule.make("R-B"), core.Rule.make("R-A", severity="block")]
    eng = core.RuleEngine(rules)
    assert [r.rule_id for r in eng.rules] == ["R-A", "R-B"]
    assert eng.policy_digest == core.RuleEngine(list(reversed(rules))).policy_digest
    a1, a2 = _art(b"1\n"), _art(b"2\n")
    outs = eng.apply([a1, a2], lambda a, r: core.RuleOutcome(
        r.rule_id, "triggered" if a is a2 else "observed", severity=r.severity))
    assert [o.rule_id for o in outs] == ["R-A", "R-B", "R-A", "R-B"]
    assert core.RuleEngine.summarize(outs)["triggered"] == 2


# ── A5：VerificationRun ──────────────────────────────────────────────────────
def _build(domain: str = "t", n: int = 2) -> core.VerificationRunBuilder:
    b = core.VerificationRunBuilder(domain, source_revision="deadbeef")
    for i in range(n):
        b.add_artifact(_art(f"c{i}\n".encode(), uri=f"f{i}"))
    return b.set_result("gate", {"n": n})


def test_run_id_excludes_timestamps():
    r1 = _build().seal()
    r2 = _build().seal()
    assert r1.run_id == r2.run_id, "run_id 不得含时间戳（否则不可复现）"
    assert r1.created_at  # 时间信息另存字段


def test_sealed_run_is_readonly_and_self_verifying():
    run = _build().seal()
    assert run.verify_integrity()
    assert "input_manifest_digest" in run.digests
    with pytest.raises(RuntimeError):
        run.domain = "hacked"          # type: ignore[misc]
    with pytest.raises(RuntimeError):
        run.results = {}               # type: ignore[misc]


def test_tampering_breaks_integrity():
    run = _build().seal()
    d = run.to_dict()
    d["results"] = {"gate": {"n": 999}}
    assert core._run_integrity(d) != run.integrity, "篡改 results 必须被 integrity 检出"


def test_run_binds_digests_and_decisions():
    b = _build()
    b.set_digest("verifier_closure_digest", "abc")
    b.set_digest("policy_digest", "def")
    b.add_decision(core.Decision.make("a1", "fail", rule_ids=["R1"]))
    run = b.seal()
    assert run.digests["verifier_closure_digest"] == "abc"
    assert run.digests["policy_digest"] == "def"
    assert len(run.decisions) == 1
    assert run.project("summary")["decision_states"]["fail"] == 1


# ── A6：投影 ─────────────────────────────────────────────────────────────────
def test_builtin_projections_are_deterministic():
    run = _build().seal()
    for kind in core.BUILTIN_PROJECTORS:
        assert run.project(kind) == run.project(kind)
    s = run.project("summary")
    assert s["n_artifacts"] == 2 and s["kind"] == "summary"
    assert run.project("manifest")["domain"] == "t"
    assert run.project("decisions")["decisions"] == []


def test_unregistered_projection_fails_loud():
    run = _build().seal()
    # 用一个**谁都不会注册**的名字（"w2" 会被 C++ 插件注册，注册表是进程级全局）
    with pytest.raises(KeyError):
        run.project("_never_registered_projection_641")


def test_domain_pack_can_register_projection():
    core.register_projector("_test_p", lambda r: {"kind": "_test_p", "n": len(r.decisions)})
    try:
        run = _build().seal()
        assert run.project("_test_p")["n"] == 0
        assert "_test_p" in core.measure()["registered_projectors"]
    finally:
        core._PROJECTORS.pop("_test_p", None)


# ── A1：依赖方向机械证明 ─────────────────────────────────────────────────────
def test_kernel_has_zero_domain_imports():
    hits = core.verify_no_domain_imports(os.path.join(ROOT, "tools", "queyi_core_v10_641.py"))
    assert hits == [], f"内核不得 import 领域模块：{hits}"


def test_ports_are_abstract():
    for cls in (core.VerifierPort, core.AttackerPort, core.AuthorityPort,
                core.EvidencePort, core.DomainPack):
        with pytest.raises(TypeError):
            cls()  # type: ignore[abstract]


def test_cli_check_passes():
    assert core.main(["--check"]) == 0
    assert core.measure()["version"] == core.SCHEMA_VERSION
