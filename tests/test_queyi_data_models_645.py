"""645 C1 数据模型单测（纯逻辑，fast 组，不调用编译器）。

锁定：三个数据类的字段、序列化/反序列化往返、等级计数、层间传递无歧义。
对应 645 §五 C1 验收：数据类正确、序列化/反序列化正确、层间传递无歧义。
"""
import json
import sys

sys.path.insert(0, "tools")

from queyi_data_models_645 import (
    EvidencePackage,
    Issue,
    VerificationResult,
    deserialize,
    selftest,
    serialize,
)


def test_selftest_passes():
    assert selftest() == 0


def test_issue_roundtrip():
    iss = Issue(issue_id="ISSUE-X", title="标题", root_cause="根因(引用 EV-1)",
                severity="high", evidence_refs=["EV-1", "EV-2"], suggested_next="补证据",
                source="smart_issue_finder_645", meta={"k": 1})
    back = Issue.from_dict(json.loads(serialize(iss)))
    assert back.issue_id == "ISSUE-X"
    assert back.evidence_refs == ["EV-1", "EV-2"]
    assert back.meta == {"k": 1}


def test_evidence_package_grade_count():
    pkg = EvidencePackage(package_id="EVPKG-X", topic="topic")
    pkg.add_evidence({"evidence_id": "a", "grade": "L1", "content": "x"})
    pkg.add_evidence({"evidence_id": "b", "grade": "L1", "content": "y"})
    pkg.add_evidence({"evidence_id": "c", "grade": "L3", "content": "z"})
    assert pkg.grade_summary == {"L1": 2, "L3": 1}
    back = EvidencePackage.from_dict(json.loads(serialize(pkg)))
    assert back.grade_summary == {"L1": 2, "L3": 1}
    assert len(back.evidence) == 3


def test_verification_result_roundtrip():
    vr = VerificationResult(result_id="VR-1", target_id="ISSUE-X", verdict="escape",
                            confidence=0.7, detail="真逃逸", escape_assoc="ATOM-FOO")
    back = VerificationResult.from_dict(json.loads(serialize(vr)))
    assert back.verdict == "escape"
    assert back.escape_assoc == "ATOM-FOO"
    assert back.confidence == 0.7


def test_three_layer_chain_no_ambiguity():
    """智能层 Issue -> 头部层 EvidencePackage -> 尾端 VerificationResult 串联往返一致。"""
    iss = Issue(issue_id="I1", title="t", root_cause="rc", severity="medium")
    pkg = EvidencePackage(package_id="P1", topic=iss.issue_id)
    pkg.add_evidence({"evidence_id": "e", "grade": "L2", "content": "c"})
    vr = VerificationResult(result_id="V1", target_id=pkg.topic, verdict="pass", confidence=0.8)
    # 三段分别序列化再反序列化，字段均保持
    assert deserialize(serialize(iss), Issue).issue_id == "I1"
    assert deserialize(serialize(pkg), EvidencePackage).grade_summary == {"L2": 1}
    assert deserialize(serialize(vr), VerificationResult).verdict == "pass"
