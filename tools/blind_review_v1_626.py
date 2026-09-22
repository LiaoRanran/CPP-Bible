"""626 C1 · Blind Review v1（Pass A 盲审 + Pass B 解盲）

**根治 P0-C**：禁止 AI 推荐结果出现在「独立人审」的第一视图。

- **Pass A（盲审）**：`ai_recommendation_shown` **必须为 False**，否则**拒绝提交**。
- **Pass B（解盲）**：揭示 AI 推荐，记录人是否改变决定、人机一致性、automation bias 风险。

与 Authority Ledger 的集成：Pass A 决定可作为 Authority event 的输入
（`review_method=ITEM_BLIND`），但**本批只提供接口，不自动写入**（需人确认，不代签）。

纯标准库；`--check` 自检。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

EXAMPLE_PATH = os.path.join(ROOT, "data", "blind_review_example_626.jsonl")

DECISIONS = ("APPROVE", "REJECT", "MODIFY", "ABSTAIN")


@dataclass
class PassADecision:
    decision: str = "APPROVE"
    reason: str = ""
    view_digest: str = ""          # 看到的视图哈希（验证无 AI 推荐）
    evidence_shown: list = field(default_factory=list)
    ai_recommendation_shown: bool = False   # **必须 False**
    elapsed_ms: int = 0
    decided_at: str = ""


@dataclass
class PassBResult:
    ai_recommendation: str = ""
    ai_reason: str = ""
    human_decision: str = ""
    changed_after_reveal: bool = False
    change_reason: str = ""
    consistency: str = ""          # agree / disagree / changed
    automation_bias_risk: str = ""  # high / medium / low
    elapsed_ms: int = 0
    decided_at: str = ""


@dataclass
class BlindReviewSession:
    blind_review_id: str = ""
    review_item_id: str = ""
    status: str = "pass_a_pending"   # pass_a_pending|pass_a_done|pass_b_done
    pass_a: Optional[PassADecision] = None
    pass_b: Optional[PassBResult] = None
    created_at: str = ""
    completed_at: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    @staticmethod
    def from_dict(d: dict) -> "BlindReviewSession":
        s = BlindReviewSession(
            blind_review_id=d.get("blind_review_id", ""),
            review_item_id=d.get("review_item_id", ""),
            status=d.get("status", "pass_a_pending"),
            created_at=d.get("created_at", ""),
            completed_at=d.get("completed_at", ""),
        )
        if d.get("pass_a"):
            s.pass_a = PassADecision(**d["pass_a"])
        if d.get("pass_b"):
            s.pass_b = PassBResult(**d["pass_b"])
        return s


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _digest(parts: list[str]) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def _risk(changed: bool, consistent: bool) -> str:
    if changed:
        return "high"
    return "low" if consistent else "medium"


class BlindReviewManager:
    def __init__(self) -> None:
        self._sessions: list[BlindReviewSession] = []

    # ── Pass A ──
    def start_session(self, review_item_id: str,
                      evidence: list) -> BlindReviewSession:
        s = BlindReviewSession(
            blind_review_id=f"BR-{len(self._sessions) + 1:04d}-"
                            f"{_digest([review_item_id, _now()])[:8]}",
            review_item_id=review_item_id,
            status="pass_a_pending",
            created_at=_now(),
        )
        s._evidence = list(evidence)   # type: ignore[attr-defined]
        self._sessions.append(s)
        return s

    def submit_pass_a(self, session_id: str, decision: str, reason: str,
                      evidence_shown: Optional[list] = None,
                      ai_recommendation_shown: bool = False,
                      elapsed_ms: int = 0) -> BlindReviewSession:
        """提交 Pass A。**若 ai_recommendation_shown=True ⇒ 拒绝提交**。"""
        s = self.get_session(session_id)
        if s is None:
            raise ValueError(f"session 不存在：{session_id}")
        if ai_recommendation_shown:
            raise ValueError("Pass A 禁止展示 AI 推荐（P0-C）：ai_recommendation_shown 必须为 False")
        if decision not in DECISIONS:
            raise ValueError(f"decision 非法：{decision}")
        ev = list(evidence_shown if evidence_shown is not None
                  else getattr(s, "_evidence", []))
        s.pass_a = PassADecision(
            decision=decision, reason=reason,
            view_digest=_digest([s.review_item_id, *map(str, ev)]),
            evidence_shown=ev,
            ai_recommendation_shown=False,
            elapsed_ms=elapsed_ms, decided_at=_now(),
        )
        s.status = "pass_a_done"
        return s

    # ── Pass B ──
    def reveal_ai_recommendation(self, session_id: str, ai_rec: str,
                                 ai_reason: str) -> BlindReviewSession:
        s = self.get_session(session_id)
        if s is None:
            raise ValueError(f"session 不存在：{session_id}")
        if s.pass_a is None:
            raise ValueError("须先完成 Pass A 才能解盲")
        s.pass_b = PassBResult(ai_recommendation=ai_rec, ai_reason=ai_reason,
                               human_decision=s.pass_a.decision)
        return s

    def submit_pass_b(self, session_id: str, final_decision: str,
                      changed: bool, change_reason: str = "",
                      elapsed_ms: int = 0) -> BlindReviewSession:
        s = self.get_session(session_id)
        if s is None:
            raise ValueError(f"session 不存在：{session_id}")
        if s.pass_a is None or s.pass_b is None:
            raise ValueError("须先完成 Pass A 并解盲")
        s.pass_b.human_decision = final_decision
        s.pass_b.changed_after_reveal = changed
        s.pass_b.change_reason = change_reason
        agree = (s.pass_a.decision == s.pass_b.ai_recommendation)
        s.pass_b.consistency = "changed" if changed else ("agree" if agree else "disagree")
        s.pass_b.automation_bias_risk = _risk(changed, agree)
        s.pass_b.elapsed_ms = elapsed_ms
        s.pass_b.decided_at = _now()
        s.status = "pass_b_done"
        s.completed_at = _now()
        return s

    # ── 读 ──
    def get_session(self, session_id: str) -> Optional[BlindReviewSession]:
        for s in self._sessions:
            if s.blind_review_id == session_id:
                return s
        return None

    def get_all_sessions(self, status: Optional[str] = None) -> list[BlindReviewSession]:
        return [s for s in self._sessions if status is None or s.status == status]

    def get_consistency_stats(self) -> dict[str, int]:
        out = {"agree": 0, "disagree": 0, "changed": 0}
        for s in self._sessions:
            if s.pass_b and s.pass_b.consistency in out:
                out[s.pass_b.consistency] += 1
        return out

    def automation_bias_risk_stats(self) -> dict[str, int]:
        out = {"high": 0, "medium": 0, "low": 0}
        for s in self._sessions:
            if s.pass_b and s.pass_b.automation_bias_risk in out:
                out[s.pass_b.automation_bias_risk] += 1
        return out

    # ── 与 Authority Ledger 的接口（**不自动写入**） ──
    def to_authority_event_kwargs(self, session_id: str) -> dict:
        """为 Pass A 决定生成 Authority event 的参数（**需人确认后才写入**）。"""
        s = self.get_session(session_id)
        if s is None or s.pass_a is None:
            raise ValueError("Pass A 未完成")
        return {
            "review_method": "ITEM_BLIND",
            "decision_origin": "human_observed",
            "result": s.pass_a.decision,
            "blind_review_id": s.blind_review_id,
            "view_digest": s.pass_a.view_digest,
            "target_type": "edge",
            "target_id": s.review_item_id,
        }

    # ── IO ──
    def export_jsonl(self, path: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            for s in self._sessions:
                fh.write(json.dumps(s.to_dict(), ensure_ascii=False) + "\n")
        return path

    @classmethod
    def import_jsonl(cls, path: str) -> "BlindReviewManager":
        m = cls()
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        m._sessions.append(BlindReviewSession.from_dict(json.loads(line)))
        return m


def build_example() -> BlindReviewManager:
    """示例 session（**模拟数据，非真实人审**，仅供演示/测试）。"""
    m = BlindReviewManager()
    s1 = m.start_session("RI-edge-ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-1",
                         ["evidence/ATOM-MEM-MOVE-002/replay.md"])
    m.submit_pass_a(s1.blind_review_id, "APPROVE", "证据可复现，无明显反例",
                    elapsed_ms=42000)
    m.reveal_ai_recommendation(s1.blind_review_id, "APPROVE", "AI 预标注 approve")
    m.submit_pass_b(s1.blind_review_id, "APPROVE", changed=False)

    s2 = m.start_session("RI-edge-ae-MIS-UB-001->ATOM-UB-GRAY-001::prop-2",
                         ["evidence/ATOM-UB-GRAY-001/replay.md"])
    m.submit_pass_a(s2.blind_review_id, "REJECT", " UB 边界证据不足", elapsed_ms=61000)
    m.reveal_ai_recommendation(s2.blind_review_id, "MODIFY", "AI 建议降级为 modify")
    m.submit_pass_b(s2.blind_review_id, "MODIFY", changed=True,
                    change_reason="解盲后接受 AI 的部分修改建议")

    s3 = m.start_session("RI-edge-ae-MIS-CONC-002->ATOM-CONC-RACE-001::prop-1",
                         ["evidence/ATOM-CONC-RACE-001/replay.md"])
    m.submit_pass_a(s3.blind_review_id, "ABSTAIN", "需补 TSan 反例", elapsed_ms=30000)
    m.reveal_ai_recommendation(s3.blind_review_id, "APPROVE", "AI 预标注 approve")
    m.submit_pass_b(s3.blind_review_id, "ABSTAIN", changed=False)
    return m


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    m = BlindReviewManager()
    s = m.start_session("RI-edge-ae-x", ["ev1", "ev2"])
    chk("session id 形如 BR-0001-xxxxxxxx", s.blind_review_id.startswith("BR-0001-"))
    chk("初始状态 pass_a_pending", s.status == "pass_a_pending")

    # Pass A 禁止 AI 推荐
    try:
        m.submit_pass_a(s.blind_review_id, "APPROVE", "r", ai_recommendation_shown=True)
        chk("Pass A 展示 AI 推荐被拒（P0-C）", False)
    except ValueError:
        chk("Pass A 展示 AI 推荐被拒（P0-C）", True)

    m.submit_pass_a(s.blind_review_id, "APPROVE", "证据充分", elapsed_ms=1000)
    chk("Pass A 提交后状态 pass_a_done", s.status == "pass_a_done")
    chk("ai_recommendation_shown 恒 False",
        s.pass_a is not None and s.pass_a.ai_recommendation_shown is False)
    chk("view_digest 已生成", bool(s.pass_a and s.pass_a.view_digest))

    m.reveal_ai_recommendation(s.blind_review_id, "APPROVE", "AI 同意")
    m.submit_pass_b(s.blind_review_id, "APPROVE", changed=False)
    chk("Pass B 后状态 pass_b_done", s.status == "pass_b_done")
    chk("一致性 agree", s.pass_b is not None and s.pass_b.consistency == "agree")
    chk("automation_bias_risk = low",
        s.pass_b is not None and s.pass_b.automation_bias_risk == "low")

    # changed 场景
    s2 = m.start_session("RI-edge-ae-y", ["ev"])
    m.submit_pass_a(s2.blind_review_id, "REJECT", "不足")
    m.reveal_ai_recommendation(s2.blind_review_id, "APPROVE", "AI 认为足够")
    m.submit_pass_b(s2.blind_review_id, "APPROVE", changed=True, change_reason="被 AI 说服")
    chk("changed → consistency=changed",
        s2.pass_b is not None and s2.pass_b.consistency == "changed")
    chk("changed → automation_bias_risk=high",
        s2.pass_b is not None and s2.pass_b.automation_bias_risk == "high")

    st = m.get_consistency_stats()
    chk("一致性统计", st["agree"] == 1 and st["changed"] == 1, str(st))
    chk("风险统计", m.automation_bias_risk_stats()["high"] == 1)

    # Authority 接口（不自动写入）
    kw = m.to_authority_event_kwargs(s.blind_review_id)
    chk("Authority 接口 review_method=ITEM_BLIND", kw["review_method"] == "ITEM_BLIND")
    chk("Authority 接口 decision_origin=human_observed",
        kw["decision_origin"] == "human_observed")

    # 导出/导入往返
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "b.jsonl")
        m.export_jsonl(p)
        m2 = BlindReviewManager.import_jsonl(p)
    chk("导出/导入条数一致", len(m2.get_all_sessions()) == len(m.get_all_sessions()))
    print(f"C1 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="626 C1 Blind Review v1")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--example", action="store_true", help="生成示例 session（标注为示例）")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.example:
        m = build_example()
        m.export_jsonl(EXAMPLE_PATH)
        print(f"example -> {EXAMPLE_PATH} ({len(m.get_all_sessions())} sessions, 模拟数据非真实人审)")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
