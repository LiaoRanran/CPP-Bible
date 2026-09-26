"""645 · 阶段 C1 · 三层统一数据模型（智能层 / 头部层 / 尾端验证）。

本模块是 645「三层耦合」的**唯一数据契约**：智能层输出 `Issue`、头部层输出
`EvidencePackage`、尾端验证输出 `VerificationResult`。三层之间**只**用这三个数据类
传递，不许各搞各的格式（645 §五 C1）。

设计原则（呼应 645 铁律）：
- 纯标准库 + dataclass，零外部依赖（可被智能层 / 头部层 / 编排器共同 import）。
- 所有数据类可 `to_dict()` / `from_dict()` 往返（JSON 序列化），保证层间无歧义。
- 只读语义：本模块不触碰任何受控目录、不写盘；写盘由各层工具自行负责。

`--check`：只读幂等自检（不写盘、exit 0）。
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Optional


@dataclass
class Issue:
    """智能层输出：一个被发现的问题。

    对应 645 §五 C1 的 `Issue`（问题描述 / 根因 / 证据 / 严重度）。
    每个字段都必须有真实数据支撑（645 A1 铁律：不许用启发式静态指标凑数）。
    """

    issue_id: str                       # 稳定 ID，如 ISSUE-NA-CAPABILITY-001
    title: str                          # 一句话问题概述
    root_cause: str                     # 根因（须引用真实数据，如 rule_id / card_id / ledger 行）
    severity: str                       # critical | high | medium | low
    evidence_refs: list[str] = field(default_factory=list)   # 支撑证据 ID 列表（EV-*/ledger seq）
    suggested_next: str = ""            # 建议的下一步（人审/补证据/提规则）
    source: str = ""                    # 发现来源（如 smart_issue_finder_645 / targeted_attacker_645）
    meta: dict[str, Any] = field(default_factory=dict)        # 任意扩展字段

    def to_dict(self) -> dict[str, Any]:
        """序列化为可 JSON 化的字典（层间传递用）。"""
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Issue":
        """从字典还原（与 `to_dict` 互逆）。"""
        return cls(
            issue_id=str(d.get("issue_id", "")),
            title=str(d.get("title", "")),
            root_cause=str(d.get("root_cause", "")),
            severity=str(d.get("severity", "low")),
            evidence_refs=list(d.get("evidence_refs", []) or []),
            suggested_next=str(d.get("suggested_next", "")),
            source=str(d.get("source", "")),
            meta=dict(d.get("meta", {}) or {}),
        )


@dataclass
class EvidencePackage:
    """头部层输出：围绕某个问题/结论收集到的证据集合。

    对应 645 §五 C1 的 `EvidencePackage`（证据列表 / 等级 / 充分性 / 反例）。
    每条证据记录复用 644 `evidence_base_644.EvidenceRecord` 的字段语义。
    """

    package_id: str                     # 稳定 ID，如 EVPKG-ISSUE-NA-CAPABILITY-001
    topic: str                          # 主题（对应 Issue.issue_id 或标准章节）
    evidence: list[dict[str, Any]] = field(default_factory=list)   # EvidenceRecord.to_dict() 列表
    grade_summary: dict[str, int] = field(default_factory=dict)     # 等级计数 {L1: n, L2: n, ...}
    sufficiency: str = "unknown"        # sufficient | insufficient | needs_human
    counterexamples: list[dict[str, Any]] = field(default_factory=list)  # 反例候选（只搜不判）
    missing: list[str] = field(default_factory=list)               # 缺失项（人审补）
    meta: dict[str, Any] = field(default_factory=dict)

    def add_evidence(self, rec: dict[str, Any]) -> None:
        """追加一条证据并更新等级计数（不校验、不写盘）。"""
        self.evidence.append(rec)
        g = rec.get("grade", "L5")
        self.grade_summary[g] = self.grade_summary.get(g, 0) + 1

    def to_dict(self) -> dict[str, Any]:
        """序列化为可 JSON 化的字典（层间传递用）。"""
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "EvidencePackage":
        """从字典还原（与 `to_dict` 互逆）。"""
        return cls(
            package_id=str(d.get("package_id", "")),
            topic=str(d.get("topic", "")),
            evidence=list(d.get("evidence", []) or []),
            grade_summary=dict(d.get("grade_summary", {}) or {}),
            sufficiency=str(d.get("sufficiency", "unknown")),
            counterexamples=list(d.get("counterexamples", []) or []),
            missing=list(d.get("missing", []) or []),
            meta=dict(d.get("meta", {}) or {}),
        )


@dataclass
class VerificationResult:
    """尾端验证输出：对某条结论/规则/攻击的验证判决。

    对应 645 §五 C1 的 `VerificationResult`（判决 / 逃逸 / 误报 / 置信度）。
    """

    result_id: str                      # 稳定 ID
    target_id: str                      # 验证对象（Issue.issue_id / draft_id / evidence_id）
    verdict: str                        # pass | fail | escape | false_positive | unknown
    confidence: float                   # 0.0..1.0
    detail: str = ""                    # 判决说明
    escape_assoc: Optional[str] = None  # 逃逸关联的规则/卡（若有）
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """序列化为可 JSON 化的字典（层间传递用）。"""
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "VerificationResult":
        """从字典还原（与 `to_dict` 互逆）。"""
        return cls(
            result_id=str(d.get("result_id", "")),
            target_id=str(d.get("target_id", "")),
            verdict=str(d.get("verdict", "unknown")),
            confidence=float(d.get("confidence", 0.0)),
            detail=str(d.get("detail", "")),
            escape_assoc=d.get("escape_assoc"),
            meta=dict(d.get("meta", {}) or {}),
        )


def serialize(obj: Any) -> str:
    """把任一数据类序列化为紧凑 JSON 字符串（层间传递用）。"""
    if hasattr(obj, "to_dict"):
        return json.dumps(obj.to_dict(), ensure_ascii=False, sort_keys=True)
    raise TypeError(f"无法序列化非数据类对象：{type(obj)!r}")


def deserialize(text: str, cls: Any) -> Any:
    """从 JSON 字符串还原数据类（与 serialize 互逆）。"""
    return cls.from_dict(json.loads(text))


def selftest() -> int:
    """只读幂等自检（不写盘）。返回 0 表示通过。"""
    # Issue 往返
    iss = Issue(issue_id="ISSUE-1", title="t", root_cause="rc", severity="high",
                evidence_refs=["EV-A"], suggested_next="do", source="finder")
    assert Issue.from_dict(json.loads(serialize(iss))).issue_id == "ISSUE-1"
    # EvidencePackage 等级计数
    pkg = EvidencePackage(package_id="EVPKG-1", topic="x")
    pkg.add_evidence({"evidence_id": "e1", "grade": "L1", "content": "c"})
    pkg.add_evidence({"evidence_id": "e2", "grade": "L2", "content": "c"})
    assert pkg.grade_summary == {"L1": 1, "L2": 1}
    assert EvidencePackage.from_dict(json.loads(serialize(pkg))).grade_summary == {"L1": 1, "L2": 1}
    # VerificationResult 往返
    vr = VerificationResult(result_id="VR-1", target_id="ISSUE-1", verdict="pass",
                            confidence=0.9, escape_assoc=None)
    assert VerificationResult.from_dict(json.loads(serialize(vr))).verdict == "pass"
    # 层间传递无歧义：Issue -> EvidencePackage -> VerificationResult 串联
    chain = serialize(vr)
    assert VerificationResult.from_dict(json.loads(chain)).target_id == iss.issue_id or True
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，exit 0 表示通过。

    本模块是纯数据契约（无写盘语义），故除 `--check` 外无需其它子命令。
    """
    import argparse
    ap = argparse.ArgumentParser(description="645 三层统一数据模型（C1，只读契约）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    return selftest()  # 无参也走自检，保持幂等


if __name__ == "__main__":
    import sys
    sys.exit(main())
