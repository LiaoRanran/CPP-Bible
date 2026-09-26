"""626 B1 · DecisionEvent v2 + AuthorityLedger（Authority 单一真源的核心数据结构）

**只有 Authority Ledger 有「人决定了什么」的权力**；W2/PCK/golden 都是派生视图（626 D 线 Projection Compiler）。

设计要点：
- `operation`（CREATE/REPLACE/REVOKE）与 `result`（APPROVE/REJECT/MODIFY/ABSTAIN）**拆开**（P0-D）
- `review_method`（五级）+ `decision_origin`（四级）区分「怎么审」与「决定来自谁」（P0-A）
- **append-only**：不提供修改/删除方法
- **哈希链**：`self_hash = SHA256(除 self_hash 外所有字段的 JSON 序列化 + prev_hash)`
- `supersedes` 链：`REPLACE` 事件指向被取代的 event_id

纯标准库；`--check` 验证 schema 完整性与 Ledger 基本功能。

647 A2（**fail-open 修复 2**，硬骨头）
====================================
病（642 B3 审计 FO-B，实测）：`DecisionEvent.from_dict({})` 把空/残 JSON **静默补成**
`result=APPROVE` + `review_method=BATCH_AUTH` + `decision_origin=human_observed` ——
恰好是最"信任假设"的组合（不完整事件被自动解释成"人观察过"）；且**未知字段被静默丢弃**
（字段名拼错 = 没写）。

修法（**两个显式入口**，不动历史数据）：

* `from_dict()` / `from_dict_lenient()`：**宽容**（历史语义，缺字段补默认、未知字段丢弃）——
  **历史 452 条专用**，保证既有账本能原样导入（哈希链重算不变）；
* `from_dict_strict()`：**严格**（**新事件专用**）—— 未知字段 ⇒ `StrictEventError`；
  `REQUIRED_FIELDS` 缺任一 ⇒ `StrictEventError`；`validate()` 不过 ⇒ `StrictEventError`。
  即**不再存在"缺字段自动变成 human_observed"这条路径**。

**诚实边界**：dataclass 的字段默认值**仍然保留**（`decision_origin="human_observed"`）——
因为 642 B3 的 FO-B 复现与 `from_dict({})` 的宽容语义依赖它，历史账本也必须能 lenient 导入。
"不再默认成 human_observed"落在**新事件的入口**上（strict），而不是把默认值删掉把历史一起判死。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import authority_schema_v2_626 as SCH  # noqa: E402

LEDGER_PATH = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
GENESIS = "GENESIS"

OPERATIONS = SCH.OPERATIONS
RESULTS = SCH.RESULTS
REVIEW_METHODS = SCH.REVIEW_METHODS
DECISION_ORIGINS = SCH.DECISION_ORIGINS


class StrictEventError(ValueError):
    """647 A2：strict 入口的失败（未知字段 / 缺必填字段 / 校验不过）。**不静默降级**。"""


@dataclass
class DecisionEvent:
    event_id: str = ""                  # AE-<seq>-<short_hash>
    seq: int = 0                        # 单调递增
    operation: str = "CREATE"           # CREATE | REPLACE | REVOKE
    result: str = "APPROVE"             # APPROVE | REJECT | MODIFY | ABSTAIN
    supersedes: list = field(default_factory=list)
    target_type: str = "edge"           # edge|card|certificate|rule|golden_policy|warn_disposition
    target_id: str = ""
    target_revision: str = ""
    scope: str = "single_edge"          # single_edge|card_all_claims|certificate_full
    confidence: str = "medium"          # low|medium|high
    modification: str = ""              # result=MODIFY 时的修改内容
    abstain_reason: str = ""            # result=ABSTAIN 时的原因
    review_method: str = "BATCH_AUTH"
    decision_origin: str = "human_observed"
    blind_review_id: str = ""
    basis_refs: list = field(default_factory=list)
    view_digest: str = ""
    source_digest: str = ""
    reviewer: str = ""
    decided_at: str = ""
    elapsed_ms: int = 0
    aggregation_policy_ref: str = ""
    cross_granularity_warning: str = ""
    # 639 D2：规则归属增量字段（known_error_rate 的 rule 级样本依赖它）。
    # 历史 452 条事件无此字段（默认 ""）——**空值不参与哈希**，保证
    # append-only 链重算哈希与历史完全一致（见 _payload 注释）。
    rule_id: str = ""                   # 命中的 gate 规则 id（如 ATOM-REL-TARGET）
    rule_version: str = ""              # 规则版本（规则变更时由人填写）
    prev_hash: str = GENESIS
    self_hash: str = ""

    # ── 哈希 ──
    def _payload(self) -> str:
        # 注意：`event_id` 由 self_hash 派生 ⇒ 必须排除，否则构成循环依赖，
        # 且导出/导入往返后重算哈希会不一致（event_id 在 finalize 后才写入）。
        # 639 D2：`rule_id`/`rule_version` 为增量字段，空值同样排除——
        # 旧事件（无规则归属）重算哈希不变，新事件（有归属）纳入防篡改。
        d = asdict(self)
        d.pop("self_hash", None)
        d.pop("event_id", None)
        for k in ("rule_id", "rule_version"):
            if not d.get(k):
                d.pop(k, None)
        return json.dumps(d, ensure_ascii=False, sort_keys=True, default=str)

    def compute_self_hash(self) -> str:
        return hashlib.sha256(
            f"{self.prev_hash}|{self._payload()}".encode("utf-8")).hexdigest()

    def finalize(self, prev_hash: str, seq: int) -> "DecisionEvent":
        """分配 seq / prev_hash / event_id / self_hash（幂等前置：调用一次即可）。"""
        self.seq = seq
        self.prev_hash = prev_hash
        self.self_hash = self.compute_self_hash()
        self.event_id = f"AE-{seq:06d}-{self.self_hash[:8]}"
        return self

    def validate(self) -> list[str]:
        errs: list[str] = []
        errs += SCH.validate_event(self.review_method, self.decision_origin,
                                   self.operation, self.result)
        if not self.target_id:
            errs.append("target_id 必填")
        if self.result == "MODIFY" and not self.modification:
            errs.append("result=MODIFY 时 modification 必填")
        if self.result == "ABSTAIN" and not self.abstain_reason:
            errs.append("result=ABSTAIN 时 abstain_reason 必填")
        if self.operation == "REPLACE" and not self.supersedes:
            errs.append("operation=REPLACE 时 supersedes 必填（P0-D）")
        return errs

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "DecisionEvent":
        """宽容导入（= `from_dict_lenient()`，**历史语义保留**）。新事件请用 `from_dict_strict()`。"""
        known = {f for f in DecisionEvent.__dataclass_fields__}  # type: ignore[attr-defined]
        return DecisionEvent(**{k: v for k, v in d.items() if k in known})

    @staticmethod
    def from_dict_lenient(d: dict) -> "DecisionEvent":
        """**宽容**入口（647 A2）：缺字段用默认、未知字段丢弃 —— **历史 452 条专用**。

        保留它的理由：既有账本是按宽容口径钉进哈希链的，必须原样能导入（重算哈希不变）。
        """
        return DecisionEvent.from_dict(d)

    @staticmethod
    def from_dict_strict(d: dict) -> "DecisionEvent":
        """**严格**入口（647 A2，**新事件专用**）：未知字段 / 缺必填字段 / 校验不过 ⇒ 抛错。

        与宽容路径的三个差别（逐条对应 642 B3 FO-B 的修复建议）：
        ① 未知字段 ⇒ 抛错（**不再静默丢弃**：字段名拼错 = 必须报错）；
        ② `REQUIRED_FIELDS` 缺任一 ⇒ 抛错（**不再用默认值补全**，
           尤其 `decision_origin` 不会再被默认成 `human_observed`）；
        ③ `validate()` 不过（枚举非法 / MODIFY 缺 modification / REPLACE 缺 supersedes…）⇒ 抛错。
        """
        if not isinstance(d, dict):
            raise StrictEventError(f"strict 导入要求 dict，得到 {type(d).__name__}")
        unknown = sorted(set(d) - KNOWN_FIELDS)
        if unknown:
            raise StrictEventError(f"未知字段 ⇒ 拒绝（拼错字段名等于没写）：{unknown}")
        missing = [f for f in REQUIRED_FIELDS if not d.get(f)]
        if missing:
            raise StrictEventError(
                f"缺必填字段 ⇒ 拒绝（不允许用默认值补全）：{missing}；"
                f"必填集合 = {list(REQUIRED_FIELDS)}")
        event = DecisionEvent(**d)
        errs = event.validate()
        if errs:
            raise StrictEventError("事件校验不过：" + "; ".join(errs))
        return event


#: 647 A2：DecisionEvent 的**全部**合法字段（strict 用它判"未知字段"）。
KNOWN_FIELDS: frozenset[str] = frozenset(DecisionEvent.__dataclass_fields__)  # type: ignore[attr-defined]
#: 647 A2：strict 导入**必须显式出现且非空**的字段。
#: 口径 = "一条可追溯到人的判决至少要说清：做了什么/结论/对象/怎么审/来自谁/谁签/何时"。
#: `decision_origin` 在列 ⇒ **新事件不再可能被默认成 `human_observed`**。
REQUIRED_FIELDS: tuple[str, ...] = (
    "operation", "result", "target_type", "target_id",
    "review_method", "decision_origin", "reviewer", "decided_at",
)


class AuthorityLedger:
    """append-only 的 Authority 事件账本（哈希链）。"""

    def __init__(self) -> None:
        self._events: list[DecisionEvent] = []

    # ── 写 ──
    def append(self, event: DecisionEvent) -> str:
        errs = event.validate()
        if errs:
            raise ValueError("事件非法：" + "; ".join(errs))
        prev = self._events[-1].self_hash if self._events else GENESIS
        event.finalize(prev_hash=prev, seq=len(self._events) + 1)
        self._events.append(event)
        return event.self_hash

    # 刻意**不提供** update / delete —— append-only

    # ── 读 ──
    def __len__(self) -> int:
        return len(self._events)

    def get(self, event_id: str) -> Optional[DecisionEvent]:
        for e in self._events:
            if e.event_id == event_id:
                return e
        return None

    def _by_target(self, target_type: str, target_id: str) -> list[DecisionEvent]:
        return [e for e in self._events
                if e.target_type == target_type and e.target_id == target_id]

    def get_all(self, target_type: str, target_id: str) -> list[DecisionEvent]:
        return self._by_target(target_type, target_id)

    def get_current(self, target_type: str, target_id: str) -> Optional[DecisionEvent]:
        """当前有效决定：未被任何后续事件 supersede 的最后一条。"""
        evs = self._by_target(target_type, target_id)
        if not evs:
            return None
        superseded = set()
        for e in evs:
            superseded.update(e.supersedes or [])
        alive = [e for e in evs if e.event_id not in superseded]
        return alive[-1] if alive else evs[-1]

    def all_events(self) -> list[DecisionEvent]:
        return list(self._events)

    # ── 校验 ──
    def verify_chain(self) -> bool:
        prev = GENESIS
        for e in self._events:
            if e.prev_hash != prev:
                return False
            if e.compute_self_hash() != e.self_hash:
                return False
            prev = e.self_hash
        return True

    # ── 统计 ──
    def count_by_review_method(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for e in self._events:
            out[e.review_method] = out.get(e.review_method, 0) + 1
        return out

    def count_by_decision_origin(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for e in self._events:
            out[e.decision_origin] = out.get(e.decision_origin, 0) + 1
        return out

    def independent_human_review_count(self) -> int:
        """独立人类确认强度：ITEM_BLIND/ITEM_SECOND_REVIEW + human_observed。"""
        return sum(1 for e in self._events
                   if SCH.is_independent_human_review(e.review_method, e.decision_origin))

    # ── IO ──
    def export_jsonl(self, path: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            for e in self._events:
                fh.write(json.dumps(e.to_dict(), ensure_ascii=False) + "\n")
        return path

    @classmethod
    def import_jsonl(cls, path: str, strict: bool = False) -> "AuthorityLedger":
        """导入 JSONL。`strict=False`（默认）= 宽容（**历史 452 条专用**）。

        `strict=True` ⇒ 逐条走 `from_dict_strict()`，任一不完整/未知字段即抛
        `StrictEventError`（**新批次导入用**）。
        """
        led = cls()
        if not os.path.exists(path):
            return led
        with open(path, encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                if strict:
                    try:
                        led._events.append(DecisionEvent.from_dict_strict(d))
                    except StrictEventError as exc:
                        raise StrictEventError(f"{path}:{lineno} ⇒ {exc}") from None
                else:
                    led._events.append(DecisionEvent.from_dict_lenient(d))
        return led

    def append_strict(self, d: dict) -> str:
        """**新事件**入口（647 A2）：先 `from_dict_strict()` 校验，再走正常 append（哈希链）。"""
        return self.append(DecisionEvent.from_dict_strict(d))


def load_ledger(path: str = LEDGER_PATH, strict: bool = False) -> AuthorityLedger:
    """读取账本：**历史用 `strict=False`（宽容，保证 452 条原样可导入）**；

    新批次/新文件用 `strict=True`（缺字段/未知字段即抛）。
    """
    return AuthorityLedger.import_jsonl(path, strict=strict)


# ── 便利构造 ──
def make_event(target_type: str, target_id: str, result: str,
               reviewer: str = "", decided_at: str = "",
               operation: str = "CREATE",
               review_method: str = "BATCH_AUTH",
               decision_origin: str = "human_observed",
               supersedes: Optional[list] = None,
               modification: str = "", abstain_reason: str = "",
               **kw: Any) -> DecisionEvent:
    e = DecisionEvent(
        operation=operation, result=result, target_type=target_type, target_id=target_id,
        review_method=review_method, decision_origin=decision_origin,
        reviewer=reviewer, decided_at=decided_at,
        supersedes=list(supersedes or []),
        modification=modification, abstain_reason=abstain_reason,
    )
    for k, v in kw.items():
        if hasattr(e, k):
            setattr(e, k, v)
    return e


def _raises(fn) -> bool:
    """`fn()` 抛 `StrictEventError` ⇒ True（自检辅助，不改任何状态）。"""
    try:
        fn()
        return False
    except StrictEventError:
        return True


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # schema 字段完整性
    fields = list(DecisionEvent.__dataclass_fields__)  # type: ignore[attr-defined]
    chk("DecisionEvent 字段 ≥24", len(fields) >= 24, f"({len(fields)})")
    for must in ("operation", "result", "review_method", "decision_origin",
                 "supersedes", "prev_hash", "self_hash", "cross_granularity_warning"):
        chk(f"含字段 {must}", must in fields)

    led = AuthorityLedger()
    chk("空 ledger 链有效", led.verify_chain())
    e1 = make_event("edge", "ae-1", "APPROVE", reviewer="A", decided_at="2026-01-01")
    h1 = led.append(e1)
    chk("append 返回 self_hash", len(h1) == 64)
    chk("seq 从 1 开始", e1.seq == 1)
    chk("event_id 形如 AE-000001-xxxxxxxx", e1.event_id.startswith("AE-000001-"))
    e2 = make_event("edge", "ae-1", "REJECT", reviewer="A", decided_at="2026-01-02",
                    operation="REPLACE", supersedes=[e1.event_id])
    led.append(e2)
    chk("链有效（2 条）", led.verify_chain())
    chk("prev_hash 串联", e2.prev_hash == e1.self_hash)
    cur = led.get_current("edge", "ae-1")
    chk("get_current 返回未被取代者", cur is not None and cur.event_id == e2.event_id)
    chk("get_all 返回 2 条", len(led.get_all("edge", "ae-1")) == 2)
    chk("get 按 id 查询", led.get(e1.event_id) is e1)

    # 校验规则
    bad = make_event("edge", "ae-2", "MODIFY")     # MODIFY 缺 modification
    chk("MODIFY 缺 modification 被拒", bool(bad.validate()))
    bad2 = make_event("edge", "ae-2", "APPROVE", operation="REPLACE")  # REPLACE 缺 supersedes
    chk("REPLACE 缺 supersedes 被拒（P0-D）", bool(bad2.validate()))
    try:
        led.append(bad2)
        chk("非法事件 append 抛错", False)
    except ValueError:
        chk("非法事件 append 抛错", True)

    # 统计
    chk("count_by_review_method", led.count_by_review_method().get("BATCH_AUTH") == 2)
    chk("count_by_decision_origin",
        led.count_by_decision_origin().get("human_observed") == 2)
    chk("independent_human_review_count = 0（无 BLIND）",
        led.independent_human_review_count() == 0)

    # 导出/导入往返
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "l.jsonl")
        led.export_jsonl(p)
        led2 = AuthorityLedger.import_jsonl(p)
        chk("导出/导入条数一致", len(led2) == len(led))
        chk("导入后链有效", led2.verify_chain())
        chk("导入后哈希一致",
            led2.all_events()[0].self_hash == led.all_events()[0].self_hash)

    # append-only：无 update/delete
    chk("无 update 方法", not hasattr(led, "update"))
    chk("无 delete 方法", not hasattr(led, "delete"))

    # ── 647 A2：strict / lenient 两个显式入口 ──
    full = {"operation": "CREATE", "result": "APPROVE", "target_type": "edge",
            "target_id": "ae-9", "review_method": "ITEM_BLIND",
            "decision_origin": "human_observed", "reviewer": "A", "decided_at": "2026-09-26"}
    chk("strict：完整事件通过", DecisionEvent.from_dict_strict(full).target_id == "ae-9")
    for miss in REQUIRED_FIELDS:
        d = {k: v for k, v in full.items() if k != miss}
        try:
            DecisionEvent.from_dict_strict(d)
            chk(f"strict：缺 {miss} 必抛", False)
        except StrictEventError:
            chk(f"strict：缺 {miss} 必抛", True)
    try:
        DecisionEvent.from_dict_strict({**full, "bogus": 1})
        chk("strict：未知字段必抛", False)
    except StrictEventError:
        chk("strict：未知字段必抛", True)
    try:
        DecisionEvent.from_dict_strict({})
        chk("strict：空 dict 必抛（FO-B 修复）", False)
    except StrictEventError:
        chk("strict：空 dict 必抛（FO-B 修复）", True)
    chk("strict：非 dict 必抛",
        _raises(lambda: DecisionEvent.from_dict_strict([])))  # type: ignore[arg-type]
    chk("strict：枚举非法必抛",
        _raises(lambda: DecisionEvent.from_dict_strict({**full, "result": "BOGUS"})))
    # 宽容路径**保持历史语义**（642 B3 FO-B 复现路径仍成立，历史账本必须能读）
    e_legacy = DecisionEvent.from_dict({})
    chk("lenient：空 dict 仍补默认（历史语义保留）",
        e_legacy.result == "APPROVE" and e_legacy.decision_origin == "human_observed")
    chk("from_dict == from_dict_lenient（别名）",
        DecisionEvent.from_dict({"target_id": "x"}).target_id
        == DecisionEvent.from_dict_lenient({"target_id": "x"}).target_id)
    hist = load_ledger()
    chk("历史账本 lenient 可导入且链有效（452 条）",
        len(hist) == 452 and hist.verify_chain(), str(len(hist)))
    print(f"B1 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="626 B1 DecisionEvent v2 / AuthorityLedger")
    ap.add_argument("--check", action="store_true", help="schema + ledger 自检")
    args = ap.parse_args(argv)
    return selftest() if args.check else selftest()


if __name__ == "__main__":
    sys.exit(main())
