"""641 A1–A6 · QueYi Core **协议内核 v1.0**（领域无关 · 纯标准库 · 只读自检）

从 625/631/632 的"5 接口 OO 框架"收敛为**层次清晰的协议内核**：

| 层 | 内容 |
|---|---|
| 数据原语（内核定义，领域无关） | `Artifact`（**内容寻址**）/ `Evidence` / `Decision`（**四态**） |
| 运行协议（本轮最关键） | `VerificationRun`：一次完整验证的**自包含、可复现、可外部审计**记录；所有报告/指标都只是它的**投影** |
| 角色端口（ABC，领域适配器实现） | `VerifierPort` / `AttackerPort` / `AuthorityPort` / `EvidencePort` + 插件契约 `DomainPack` |
| 投影层 | 内核只提供 `summary`/`manifest`/`decisions` 三种**领域无关**投影；W2/PCK/dashboard/textbook 由**领域插件注册**（内核不认识它们） |

铁律（§二.3 / §四.2）：本模块**不 import 任何领域专用模块**（gate_engine / poison_drill /
atom_evidence_replay / toolchain / cppbible / authority_v2 …），依赖方向**内核 ← 适配器**，
由 `verify_no_domain_imports()` 做 **AST 机械证明**（不是口头声称）。

与旧版的关系：625/631/632 的 `queyi_core_interface_*` 是"5 接口 25 方法"的**抽象清单**，
本模块是**可运行的协议内核**（原语有实现、run 可封存、投影可派生）。旧文件保持不动，
本模块不 import 它们（避免把抽象清单变成运行时依赖）。

CLI：`--check`（只读自检）/ `--json`（measure）/ `--report`（写 `data/queyi_core_v10_641.md`）
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Iterable, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_MD = os.path.join(ROOT, "data", "queyi_core_v10_641.md")
OUT_JSON = os.path.join(ROOT, "data", "queyi_core_v10_641.json")

SCHEMA_VERSION = "1.0"
#: 四态（与 638 四态 schema 一致：pass / pass_with_exception / fail / unknown）
FOUR_STATES = ("pass", "pass_with_exception", "fail", "unknown")
#: 领域模块黑名单（内核不得 import；适配器可以）
FORBIDDEN_DOMAIN_MODULES = frozenset({
    "gate_engine", "poison_drill", "atom_evidence_replay", "atom_evidence_sandbox",
    "toolchain", "cppbible", "authority_v2_627", "decision_event_v2_626",
    "defense_chain", "weighted_af_solver", "argument_audit", "card_schema",
    "compile_all", "replay",
})
#: 证据复验状态（与 628/635 三态口径同源，此处内核化）
EVIDENCE_STATES = ("confirm", "refute", "infra", "unknown")


# ── 规范化与内容寻址 ──────────────────────────────────────────────────────────
def canonical_json(obj: Any) -> str:
    """确定性序列化（sort_keys + 紧凑分隔 + 非 ASCII 直出），跨平台同字节。"""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, default=str)


def digest_of(obj: Any) -> str:
    """任意可序列化对象的 sha256（先做确定性序列化）。"""
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def digest_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def kernel_self_digest() -> str:
    """内核**自身文件**的 sha256 —— **通用性证明的锚**（C3）。

    两个领域各自把 `kernel_digest` 记进自己的 run；只要内核没为某个领域改过，
    两个 run 里的这个值就必然相同（否则"同一内核零改动跨领域"不成立）。
    """
    try:
        with open(os.path.abspath(__file__), "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return ""


def canonicalize_content(content: bytes) -> bytes:
    """跨平台内容规范化：CRLF→LF；非空内容确保以单个 LF 结尾。

    **不做编码猜测**（调用方给字节）；不裁剪空白——那是领域插件的职责（§二.4）。
    """
    b = content.replace(b"\r\n", b"\n")
    if b and not b.endswith(b"\n"):
        b = b + b"\n"
    return b


def _uri_norm(uri: str) -> str:
    return uri.replace(os.sep, "/") if uri else ""


def _pairs(d: dict[str, Any] | None) -> tuple[tuple[str, str], ...]:
    """dict → 确定性（键排序后的 (k, canonical_json(v))）元组，保证可哈希 + 可比较。"""
    if not d:
        return ()
    return tuple(sorted((str(k), canonical_json(v)) for k, v in d.items()))


def _unpairs(p: Iterable[tuple[str, str]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in p:
        try:
            out[k] = json.loads(v)
        except (ValueError, TypeError):
            out[k] = v
    return out


# ── 原语 1：Artifact（内容寻址）──────────────────────────────────────────────
@dataclass(frozen=True)
class ArtifactRef:
    """`VerificationRun.inputs.artifacts` 里的引用（§五 schema）。"""
    artifact_id: str
    kind: str
    uri: str
    content_digest: str

    def to_dict(self) -> dict[str, Any]:
        return {"artifact_id": self.artifact_id, "kind": self.kind,
                "uri": self.uri, "content_digest": self.content_digest}


@dataclass(frozen=True)
class Artifact:
    """任何被验证对象的统一抽象。**内容寻址**：`artifact_id = sha256(规范化内容)`。

    同内容（无论路径/CRLF/到达方式）⇒ 同 ID。路径只作为**提示**保存在 `uri`，
    不参与 ID（否则同一内容换个文件名就是两个对象）。
    """
    artifact_id: str
    kind: str
    content_digest: str
    size: int
    uri: str = ""
    claims: tuple[str, ...] = ()
    metadata: tuple[tuple[str, str], ...] = ()

    @classmethod
    def from_bytes(cls, content: bytes, kind: str, uri: str = "",
                   claims: Iterable[str] = (), metadata: dict[str, Any] | None = None) -> "Artifact":
        c = canonicalize_content(content)
        return cls(artifact_id=digest_bytes(b"artifact\n" + c),
                   kind=kind,
                   content_digest=digest_bytes(c),
                   size=len(c),
                   uri=_uri_norm(uri),
                   claims=tuple(claims),
                   metadata=_pairs(metadata))

    def ref(self) -> ArtifactRef:
        return ArtifactRef(self.artifact_id, self.kind, self.uri, self.content_digest)

    def to_dict(self) -> dict[str, Any]:
        return {"artifact_id": self.artifact_id, "kind": self.kind,
                "content_digest": self.content_digest, "size": self.size,
                "uri": self.uri, "claims": list(self.claims),
                "metadata": _unpairs(self.metadata)}


# ── 原语 2：Evidence ─────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Evidence:
    """支撑断言的证据：可独立复验、带来源与置信。**不绑定任何卡片格式**（A3）。"""
    evidence_id: str
    artifact_ids: tuple[str, ...]
    method: str
    provenance: tuple[tuple[str, str], ...]
    confidence: str = "unspecified"

    @classmethod
    def make(cls, artifact_ids: Iterable[str], method: str,
             provenance: dict[str, Any] | None = None,
             confidence: str = "unspecified") -> "Evidence":
        ids = tuple(sorted(set(artifact_ids)))
        prov = _pairs(provenance)
        return cls(evidence_id=digest_of({"a": list(ids), "m": method, "p": list(prov)}),
                   artifact_ids=ids, method=method, provenance=prov, confidence=confidence)

    def to_dict(self) -> dict[str, Any]:
        return {"evidence_id": self.evidence_id, "artifact_ids": list(self.artifact_ids),
                "method": self.method, "provenance": _unpairs(self.provenance),
                "confidence": self.confidence}


@dataclass(frozen=True)
class EvidenceResult:
    """证据复验结果（状态取自 `EVIDENCE_STATES`），由 `EvidencePort` 产出。"""
    evidence_id: str
    status: str
    detail: str = ""

    def __post_init__(self) -> None:
        if self.status not in EVIDENCE_STATES:
            raise ValueError(f"非法证据状态 {self.status!r}（应为 {EVIDENCE_STATES}）")


# ── 原语 3：Decision（四态）──────────────────────────────────────────────────
@dataclass(frozen=True)
class Decision:
    """一次判定的结果。**四态** + 依据 + 证据引用；可序列化、可与 DecisionEvent v2 互转（A4）。

    `decision_id` 确定性（不含时间戳）⇒ 同一 (artifact, state, reasons, rules, policy)
    的决策 ID 相同，重复写入权威账本可去重。
    """
    decision_id: str
    artifact_id: str
    state: str
    reasons: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    rule_ids: tuple[str, ...] = ()
    policy_ref: str = ""
    exceptions: tuple[str, ...] = ()
    abstained: bool = False
    decided_at: str = ""

    def __post_init__(self) -> None:
        if self.state not in FOUR_STATES:
            raise ValueError(f"非法判决态 {self.state!r}（应为 {FOUR_STATES}）")

    @classmethod
    def make(cls, artifact_id: str, state: str, reasons: Iterable[str] = (),
             evidence_ids: Iterable[str] = (), rule_ids: Iterable[str] = (),
             policy_ref: str = "", exceptions: Iterable[str] = (),
             abstained: bool = False, decided_at: str = "") -> "Decision":
        rs, es, rids, exs = (tuple(reasons), tuple(sorted(set(evidence_ids))),
                             tuple(sorted(set(rule_ids))), tuple(exceptions))
        return cls(decision_id=digest_of({"a": artifact_id, "s": state, "r": list(rs),
                                          "rid": list(rids), "p": policy_ref}),
                   artifact_id=artifact_id, state=state, reasons=rs, evidence_ids=es,
                   rule_ids=rids, policy_ref=policy_ref, exceptions=exs,
                   abstained=abstained,
                   decided_at=decided_at or datetime.now().isoformat(timespec="seconds"))

    def to_dict(self) -> dict[str, Any]:
        return {"decision_id": self.decision_id, "artifact_id": self.artifact_id,
                "state": self.state, "reasons": list(self.reasons),
                "evidence_ids": list(self.evidence_ids), "rule_ids": list(self.rule_ids),
                "policy_ref": self.policy_ref, "exceptions": list(self.exceptions),
                "abstained": self.abstained, "decided_at": self.decided_at}

    # ── 与 626 DecisionEvent v2 的互转（最小字段映射，诚实：非全字段）──
    V2_STATE_MAP = {"pass": "PASS", "pass_with_exception": "PASS_WITH_EXCEPTION",
                    "fail": "FAIL", "unknown": "UNKNOWN"}

    def to_decision_event_v2(self) -> dict[str, Any]:
        """映射为 DecisionEvent v2 的**核心字段**（v2 共 26 字段，此处只填内核能填的）。"""
        return {"event_id": self.decision_id,
                "target_type": "artifact",
                "target_id": self.artifact_id,
                "result": self.V2_STATE_MAP[self.state],
                "rule_ids": list(self.rule_ids),
                "reason": "; ".join(self.reasons),
                "evidence_refs": list(self.evidence_ids),
                "decided_at": self.decided_at}

    @classmethod
    def from_decision_event_v2(cls, d: dict[str, Any]) -> "Decision":
        inv = {v: k for k, v in cls.V2_STATE_MAP.items()}
        state = inv.get(str(d.get("result", "")).upper(), "unknown")
        return cls(decision_id=str(d.get("event_id", "")),
                   artifact_id=str(d.get("target_id", "")),
                   state=state,
                   reasons=tuple([d["reason"]] if d.get("reason") else []),
                   evidence_ids=tuple(str(x) for x in d.get("evidence_refs", []) or []),
                   rule_ids=tuple(str(x) for x in d.get("rule_ids", []) or []),
                   decided_at=str(d.get("decided_at", "")))


# ── 端口与插件契约 ───────────────────────────────────────────────────────────
@dataclass(frozen=True)
class PolicyRef:
    """规则/政策版本引用（可声明、可版本化；§二.4）。"""
    policy_id: str
    version: str = "1"
    digest: str = ""
    source: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"policy_id": self.policy_id, "version": self.version,
                "digest": self.digest, "source": self.source}


class VerifierPort(ABC):
    """给定 artifact + policy，产出判定（C++ 侧接 `gate_engine`）。"""

    @abstractmethod
    def verify(self, artifact: Artifact, policy: PolicyRef) -> Decision:
        raise NotImplementedError


class AttackerPort(ABC):
    """生成/施加变异、沙箱执行、可还原（C++ 侧接 poison_drill/沙箱）。"""

    @abstractmethod
    def attack(self, artifacts: list[Artifact], mutations: list[dict[str, Any]]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def restore(self) -> bool:
        raise NotImplementedError


class AuthorityPort(ABC):
    """append-only 决策账本 + 透明日志 + 人审入口（C++ 侧接 Authority V2）。"""

    @abstractmethod
    def append(self, decision: Decision) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_chain(self) -> bool:
        raise NotImplementedError


class EvidencePort(ABC):
    """证据复验（C++ 侧接 `atom_evidence_replay`）。"""

    @abstractmethod
    def verify(self, evidence: Evidence) -> EvidenceResult:
        raise NotImplementedError


class DomainPack(ABC):
    """领域插件契约（§二.4）：一个领域至少声明 canonicalize / 证据复验 / 规则集 / 环境。"""

    domain_id: str = ""

    @abstractmethod
    def canonicalize(self, content: bytes) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def load_rules(self) -> list["Rule"]:
        raise NotImplementedError

    @abstractmethod
    def environment(self) -> dict[str, Any]:
        raise NotImplementedError


# ── 通用规则引擎（引擎通用，规则外置）────────────────────────────────────────
@dataclass(frozen=True)
class Rule:
    """**声明式**规则：内核只认识 id/severity/kind/参数，如何判定由领域 evaluator 给。"""
    rule_id: str
    severity: str = "warn"
    kind: str = ""
    description: str = ""
    params: tuple[tuple[str, str], ...] = ()

    @classmethod
    def make(cls, rule_id: str, severity: str = "warn", kind: str = "",
             description: str = "", params: dict[str, Any] | None = None) -> "Rule":
        return cls(rule_id=rule_id, severity=severity, kind=kind,
                   description=description, params=_pairs(params))

    def to_dict(self) -> dict[str, Any]:
        return {"rule_id": self.rule_id, "severity": self.severity, "kind": self.kind,
                "description": self.description, "params": _unpairs(self.params)}


@dataclass(frozen=True)
class RuleOutcome:
    rule_id: str
    outcome: str            # triggered | observed | na | error
    message: str = ""
    severity: str = "warn"


class RuleEngine:
    """**领域无关**的规则执行器：只负责确定性遍历与汇总，判定逻辑由 `evaluator` 注入。

    B2 用它加载 C++ 的 67 条规则（外置），内核不硬编码任何 C++ 规则。
    """

    def __init__(self, rules: Iterable[Rule]) -> None:
        self.rules: tuple[Rule, ...] = tuple(sorted(rules, key=lambda r: r.rule_id))

    @property
    def policy_digest(self) -> str:
        return digest_of([r.to_dict() for r in self.rules])

    def apply(self, artifacts: Iterable[Artifact],
              evaluator: Callable[[Artifact, Rule], RuleOutcome]) -> list[RuleOutcome]:
        """按 (artifact_id, rule_id) 确定性排序遍历。"""
        outs: list[RuleOutcome] = []
        for a in sorted(artifacts, key=lambda x: x.artifact_id):
            for r in self.rules:
                outs.append(evaluator(a, r))
        return outs

    @staticmethod
    def summarize(outcomes: Iterable[RuleOutcome]) -> dict[str, int]:
        c = {"triggered": 0, "observed": 0, "na": 0, "error": 0}
        for o in outcomes:
            c[o.outcome] = c.get(o.outcome, 0) + 1
        return c


# ── 运行协议：VerificationRun（本轮最关键对象）────────────────────────────────
class VerificationRun:
    """一次完整验证的**自包含、可复现、可外部审计**记录（§五 schema）。

    * 构建期可变（`VerificationRunBuilder`）；`seal()` 后**只读**（再赋值抛 `RuntimeError`）；
    * `run_id` **确定性**（只由 schema/domain/revision/输入/digest 决定，不含时间戳）
      ⇒ 同样的输入与内核再跑一次得到同一个 run_id，可外部复现比对；
    * `integrity` = 封存内容自哈希，`verify_integrity()` 可检测任何事后篡改；
    * 所有报告/指标都是它的**投影**（`project()`）——不允许"报告另算"（§四.6）。
    """

    def __init__(self, run_id: str, domain: str, source_revision: str,
                 execution_mode: str, random_seed: Optional[int],
                 digests: dict[str, str], inputs: dict[str, Any],
                 results: dict[str, Any], decisions: list[Decision],
                 external_attestations: list[dict[str, Any]],
                 exceptions: list[dict[str, Any]], abstentions: list[dict[str, Any]],
                 created_at: str, started_at: str, ended_at: str,
                 integrity: str) -> None:
        self.schema_version = SCHEMA_VERSION
        self.run_id = run_id
        self.domain = domain
        self.source_revision = source_revision
        self.execution_mode = execution_mode
        self.random_seed = random_seed
        self.digests = dict(digests)
        self.inputs = dict(inputs)
        self.results = dict(results)
        self.decisions = list(decisions)
        self.external_attestations = list(external_attestations)
        self.exceptions = list(exceptions)
        self.abstentions = list(abstentions)
        self.created_at = created_at
        self.started_at = started_at
        self.ended_at = ended_at
        self.integrity = integrity
        object.__setattr__(self, "_sealed", True)   # 构造完成才封存

    # ── 封存后只读 ──
    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_sealed", False):
            raise RuntimeError(f"VerificationRun 已封存，不可修改字段 {name!r}（§四.6）")
        object.__setattr__(self, name, value)

    def to_dict(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, "run_id": self.run_id,
                "domain": self.domain, "source_revision": self.source_revision,
                "execution_mode": self.execution_mode, "random_seed": self.random_seed,
                "digests": self.digests, "inputs": self.inputs, "results": self.results,
                "decisions": [d.to_dict() for d in self.decisions],
                "external_attestations": self.external_attestations,
                "exceptions": self.exceptions, "abstentions": self.abstentions,
                "created_at": self.created_at, "started_at": self.started_at,
                "ended_at": self.ended_at, "integrity": self.integrity}

    def verify_integrity(self) -> bool:
        d = self.to_dict()
        return bool(d.pop("integrity") == _run_integrity(d))

    def project(self, kind: str) -> dict[str, Any]:
        return project(self, kind)


def _run_integrity(d: dict[str, Any]) -> str:
    return digest_of({k: v for k, v in d.items() if k != "integrity"})


def _run_id(domain: str, source_revision: str, execution_mode: str,
            random_seed: Optional[int], inputs: dict[str, Any],
            digests: dict[str, str]) -> str:
    """确定性 run_id：不含任何时间戳（否则不可复现）。"""
    return digest_of({"schema": SCHEMA_VERSION, "domain": domain,
                      "revision": source_revision, "mode": execution_mode,
                      "seed": random_seed, "inputs": inputs, "digests": digests})


class VerificationRunBuilder:
    """构建期（`seal()` 之前）唯一允许改动 run 的地方。"""

    def __init__(self, domain: str, source_revision: str = "",
                 execution_mode: str = "normal",
                 random_seed: Optional[int] = None) -> None:
        self.domain = domain
        self.source_revision = source_revision
        self.execution_mode = execution_mode
        self.random_seed = random_seed
        self._artifacts: list[ArtifactRef] = []
        self._mutation_population: dict[str, Any] = {}
        self._digests: dict[str, str] = {}
        self._results: dict[str, Any] = {}
        self._decisions: list[Decision] = []
        self._attestations: list[dict[str, Any]] = []
        self._exceptions: list[dict[str, Any]] = []
        self._abstentions: list[dict[str, Any]] = []
        self._started = datetime.now().isoformat(timespec="seconds")

    def add_artifact(self, a: Artifact) -> "VerificationRunBuilder":
        self._artifacts.append(a.ref())
        return self

    def set_mutation_population(self, desc: dict[str, Any]) -> "VerificationRunBuilder":
        self._mutation_population = dict(desc)
        return self

    def set_digest(self, name: str, value: str) -> "VerificationRunBuilder":
        self._digests[str(name)] = str(value)
        return self

    def set_result(self, section: str, data: Any) -> "VerificationRunBuilder":
        self._results[str(section)] = data
        return self

    def add_decision(self, d: Decision) -> "VerificationRunBuilder":
        self._decisions.append(d)
        return self

    def add_attestation(self, a: dict[str, Any]) -> "VerificationRunBuilder":
        self._attestations.append(a)
        return self

    def add_exception(self, e: dict[str, Any]) -> "VerificationRunBuilder":
        self._exceptions.append(e)
        return self

    def add_abstention(self, a: dict[str, Any]) -> "VerificationRunBuilder":
        self._abstentions.append(a)
        return self

    def seal(self) -> VerificationRun:
        inputs = {"artifacts": [a.to_dict() for a in self._artifacts],
                  "mutation_population": self._mutation_population}
        if "input_manifest_digest" not in self._digests:
            self._digests["input_manifest_digest"] = digest_of(inputs)
        now = datetime.now().isoformat(timespec="seconds")
        body: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "run_id": _run_id(self.domain, self.source_revision, self.execution_mode,
                              self.random_seed, inputs, self._digests),
            "domain": self.domain, "source_revision": self.source_revision,
            "execution_mode": self.execution_mode, "random_seed": self.random_seed,
            "digests": dict(self._digests), "inputs": inputs, "results": dict(self._results),
            "decisions": [d.to_dict() for d in self._decisions],
            "external_attestations": list(self._attestations),
            "exceptions": list(self._exceptions), "abstentions": list(self._abstentions),
            "created_at": now, "started_at": self._started, "ended_at": now,
        }
        body["integrity"] = _run_integrity(body)
        run = VerificationRun(
            run_id=body["run_id"], domain=self.domain, source_revision=self.source_revision,
            execution_mode=self.execution_mode, random_seed=self.random_seed,
            digests=body["digests"], inputs=body["inputs"], results=body["results"],
            decisions=list(self._decisions), external_attestations=body["external_attestations"],
            exceptions=body["exceptions"], abstentions=body["abstentions"],
            created_at=body["created_at"], started_at=body["started_at"],
            ended_at=body["ended_at"], integrity=body["integrity"])
        # 封存自检：建出来就必须自洽（防止"封存了但哈希算错"）
        if not run.verify_integrity():
            raise RuntimeError("VerificationRun 封存自检失败：integrity 不匹配")
        return run


# ── 投影层（A6）：报告 = run 的确定性函数 ─────────────────────────────────────
_PROJECTORS: dict[str, Callable[[VerificationRun], dict[str, Any]]] = {}


def register_projector(name: str, fn: Callable[[VerificationRun], dict[str, Any]]) -> None:
    """注册一个投影。**领域插件**用它注册 W2/PCK/dashboard/textbook 等（内核不认识它们）。"""
    _PROJECTORS[name] = fn


def project(run: VerificationRun, kind: str) -> dict[str, Any]:
    """从封存 run **确定性**派生投影。未注册的 kind ⇒ `KeyError`（fail-loud，不静默兜底）。"""
    if kind not in _PROJECTORS:
        raise KeyError(f"未注册的投影 {kind!r}（已注册：{sorted(_PROJECTORS)}）")
    return _PROJECTORS[kind](run)


def _p_summary(run: VerificationRun) -> dict[str, Any]:
    states = {s: 0 for s in FOUR_STATES}
    for d in run.decisions:
        states[d.state] = states.get(d.state, 0) + 1
    return {"kind": "summary", "run_id": run.run_id, "domain": run.domain,
            "n_artifacts": len(run.inputs.get("artifacts", [])),
            "n_decisions": len(run.decisions), "decision_states": states,
            "n_exceptions": len(run.exceptions), "n_abstentions": len(run.abstentions),
            "result_sections": sorted(run.results)}


def _p_manifest(run: VerificationRun) -> dict[str, Any]:
    return {"kind": "manifest", "run_id": run.run_id, "schema_version": run.schema_version,
            "domain": run.domain, "source_revision": run.source_revision,
            "execution_mode": run.execution_mode, "random_seed": run.random_seed,
            "digests": dict(run.digests), "inputs": run.inputs}


def _p_decisions(run: VerificationRun) -> dict[str, Any]:
    return {"kind": "decisions", "run_id": run.run_id,
            "decisions": sorted((d.to_dict() for d in run.decisions),
                                key=lambda x: str(x["decision_id"]))}


register_projector("summary", _p_summary)
register_projector("manifest", _p_manifest)
register_projector("decisions", _p_decisions)
BUILTIN_PROJECTORS = ("decisions", "manifest", "summary")


# ── 依赖方向机械证明（§四.2）─────────────────────────────────────────────────
def module_imports(path: str) -> list[str]:
    """AST 取一个模块**顶层与函数内**所有 import 的模块名（不含相对导入）。"""
    try:
        src = open(path, encoding="utf-8", errors="replace").read()
        tree = ast.parse(src)
    except (OSError, SyntaxError):
        return []
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                names.append(node.module.split(".")[0])
    return sorted(set(names))


def verify_no_domain_imports(path: str, forbidden: Iterable[str] = FORBIDDEN_DOMAIN_MODULES) -> list[str]:
    """返回 `path` **命中**的领域模块（空 = 机械证明零领域依赖）。"""
    forb = set(forbidden)
    return sorted(set(module_imports(path)) & forb)


def measure() -> dict[str, Any]:
    return {"version": SCHEMA_VERSION,
            "module": os.path.basename(__file__),
            "primitives": ["Artifact", "Evidence", "Decision"],
            "four_states": list(FOUR_STATES),
            "evidence_states": list(EVIDENCE_STATES),
            "ports": ["VerifierPort", "AttackerPort", "AuthorityPort", "EvidencePort",
                      "DomainPack"],
            "builtin_projectors": list(BUILTIN_PROJECTORS),
            "registered_projectors": sorted(_PROJECTORS),
            "domain_imports_in_kernel": verify_no_domain_imports(os.path.abspath(__file__)),
            "forbidden_domain_modules": sorted(FORBIDDEN_DOMAIN_MODULES)}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 1) 内容寻址
    a1 = Artifact.from_bytes(b"x = 1\n", "text", uri="a\\b\\c.txt")
    a2 = Artifact.from_bytes(b"x = 1\r\n", "text", uri="d.txt")
    a3 = Artifact.from_bytes(b"x = 2\n", "text")
    chk("同内容（CRLF/LF、不同路径）⇒ 同 artifact_id", a1.artifact_id == a2.artifact_id)
    chk("不同内容 ⇒ 不同 artifact_id", a1.artifact_id != a3.artifact_id)
    chk("uri 规范化为正斜杠", a1.uri == "a/b/c.txt", a1.uri)
    chk("size 记的是规范化后字节", a1.size == len(b"x = 1\n"))

    # 2) Evidence
    e1 = Evidence.make([a1.artifact_id], "replay", {"command": "echo"}, "high")
    e2 = Evidence.make([a1.artifact_id], "replay", {"command": "echo"}, "high")
    chk("Evidence id 确定性", e1.evidence_id == e2.evidence_id)
    chk("EvidenceResult 拒绝非法状态",
        _raises(lambda: EvidenceResult(e1.evidence_id, "bogus")))
    chk("EvidenceResult 接受合法状态",
        EvidenceResult(e1.evidence_id, "confirm").status == "confirm")

    # 3) Decision 四态
    chk("非法判决态被拒", _raises(lambda: Decision.make(a1.artifact_id, "maybe")))
    d_pass = Decision.make(a1.artifact_id, "pass", reasons=["ok"], rule_ids=["R1"])
    d_fail = Decision.make(a3.artifact_id, "fail", reasons=["bad"], rule_ids=["R1"])
    chk("同参数 ⇒ 同 decision_id（可去重）",
        d_pass.decision_id == Decision.make(a1.artifact_id, "pass",
                                            reasons=["ok"], rule_ids=["R1"]).decision_id)
    # v2 互转往返
    v2 = d_fail.to_decision_event_v2()
    back = Decision.from_decision_event_v2(v2)
    chk("Decision ↔ DecisionEvent v2 往返一致（result=" + str(v2["result"]) + "）",
        back.decision_id == d_fail.decision_id and back.state == "fail")

    # 4) 规则引擎（通用 + 外置）
    rules = [Rule.make("R-B", severity="warn"), Rule.make("R-A", severity="block")]
    eng = RuleEngine(rules)
    chk("规则按 id 排序（确定性）", [r.rule_id for r in eng.rules] == ["R-A", "R-B"])
    d1 = eng.policy_digest
    chk("policy_digest 稳定", d1 == RuleEngine(list(reversed(rules))).policy_digest)
    outs = eng.apply([a1, a3], lambda a, r: RuleOutcome(
        r.rule_id, "triggered" if a.artifact_id == a3.artifact_id else "observed",
        severity=r.severity))
    chk("规则引擎遍历数 = 规则数 × artifact 数", len(outs) == 4)
    chk("汇总计数正确", RuleEngine.summarize(outs) == {"triggered": 2, "observed": 2,
                                                       "na": 0, "error": 0})

    # 5) VerificationRun
    b = (VerificationRunBuilder("selftest", source_revision="deadbeef")
         .add_artifact(a1).add_artifact(a3)
         .set_digest("policy_digest", d1)
         .set_result("gate", {"n": 2})
         .add_decision(d_pass).add_decision(d_fail))
    run = b.seal()
    chk("run_id 确定性（不含时间戳）",
        run.run_id == VerificationRunBuilder(
            "selftest", source_revision="deadbeef").add_artifact(a1).add_artifact(a3)
        .set_digest("policy_digest", d1).set_result("gate", {"n": 2})
        .add_decision(d_pass).add_decision(d_fail).seal().run_id)
    chk("input_manifest_digest 自动补齐", "input_manifest_digest" in run.digests)
    chk("integrity 自校验通过", run.verify_integrity())
    chk("封存后只读（改字段抛错）",
        _raises(lambda: setattr(run, "domain", "hacked")))
    # 篡改检测：伪造一个同结构但 results 不同的 run
    forged = VerificationRunBuilder("selftest", source_revision="deadbeef") \
        .add_artifact(a1).add_artifact(a3).set_digest("policy_digest", d1) \
        .set_result("gate", {"n": 999}).add_decision(d_pass).add_decision(d_fail).seal()
    forged_dict = forged.to_dict()
    forged_dict["results"] = {"gate": {"n": 2}}
    chk("篡改 results ⇒ integrity 失效",
        _run_integrity(forged_dict) != forged.integrity)

    # 6) 投影
    s = run.project("summary")
    chk("summary 投影计数正确",
        s["n_artifacts"] == 2 and s["n_decisions"] == 2
        and s["decision_states"]["pass"] == 1 and s["decision_states"]["fail"] == 1)
    chk("投影确定性", run.project("summary") == s)
    chk("manifest 投影含 digests", "policy_digest" in run.project("manifest")["digests"])
    # 注意：必须用**谁都不会注册**的名字。"w2" 会被 C++ 领域适配器注册
    # （投影注册表是进程级全局），同进程内先跑 cpp 测试再跑本 selftest 时
    # run.project("w2") 会成功 ⇒ 断言假失败。fail-loud 本身是设计行为。
    chk("未注册投影 ⇒ KeyError（fail-loud）",
        _raises(lambda: run.project("_never_registered_projection_641")))
    chk("内置投影 3 个", sorted(BUILTIN_PROJECTORS) == ["decisions", "manifest", "summary"])

    # 7) 内核零领域依赖（AST 自证）
    hits = verify_no_domain_imports(os.path.abspath(__file__))
    chk("内核 AST 扫描零领域 import", hits == [], str(hits))

    print(f"v1.0 core selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _raises(fn: Callable[[], Any]) -> bool:
    try:
        fn()
    except Exception:  # noqa: BLE001
        return True
    return False


def write_report() -> str:
    m = measure()
    lines = [
        "# 641 · QueYi Core 协议内核 v1.0", "",
        f"- 版本：**{m['version']}** · 模块 `{m['module']}`",
        f"- 数据原语：**{len(m['primitives'])}** 个（{', '.join(m['primitives'])}）",
        f"- 判决四态：{', '.join(m['four_states'])}",
        f"- 端口：{', '.join(m['ports'])}",
        f"- 投影：内置 {len(m['builtin_projectors'])} 个（{', '.join(m['builtin_projectors'])}）"
        f"；已注册合计 {len(m['registered_projectors'])} 个（领域插件注册的在其中）",
        f"- **内核领域依赖（AST 机械证明）：{m['domain_imports_in_kernel'] or '零'}**",
        f"- 领域模块黑名单：{len(m['forbidden_domain_modules'])} 个", "",
        "## 一、与 631/632 的关系", "",
        "| 项 | v0.2/v0.3（631/632） | v1.0（641） |", "|---|---|---|",
        "| 形态 | 5 接口 25 方法**抽象清单** | **可运行协议内核**（原语有实现） |",
        "| 真实适配 | 仅 Evidence 1/5 | 内核无关；适配器由领域插件实现 |",
        "| run 协议 | 无 | **VerificationRun**（构建/封存/投影） |",
        "| 依赖方向证明 | 口头 | **AST 机械证明** |", "",
        "## 二、诚实登记", "",
        "1. `Decision ↔ DecisionEvent v2` 是**最小字段映射**（v2 共 26 字段，内核只填能填的 8 个），"
        "不是全字段等价；",
        "2. `run_id` 不含时间戳 ⇒ 同输入必然同 ID（利于复现），但**不表达「第几次跑」**，"
        "需要时序请用 `created_at`；",
        "3. 内核的规则引擎只做**确定性遍历与汇总**，判定逻辑必须外部注入（否则内核就被领域污染）；",
        "4. 投影只内置 3 个**领域无关**项；W2/PCK/dashboard/textbook 由领域插件注册，"
        "内核不认识它们。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="641 QueYi Core 协议内核 v1.0")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写内核报告 + JSON")
    ap.add_argument("--json", action="store_true", help="打印 measure(JSON)")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(f"written {write_report()}")
        return 0
    if a.json:
        print(json.dumps(measure(), ensure_ascii=False, indent=2))
        return 0
    m = measure()
    print(f"version={m['version']} primitives={len(m['primitives'])} "
          f"domain_imports={len(m['domain_imports_in_kernel'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
