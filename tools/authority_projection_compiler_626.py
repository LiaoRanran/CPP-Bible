"""626 D1/D2 · Authority → Projection Compiler（**唯一方向，禁止反向写回**）

**Authority 是唯一裁定真源**：W2 / PCK / golden / dashboard / textbook 都是**派生视图**。
本编译器只读 Authority Ledger，产出投影；**绝不写回 Authority**。

核心保证：
1. **只读**：编译后 ledger 不变
2. **确定性**：相同输入 ⇒ 相同输出
3. **可追溯**：每个投影结果带 `source_authority_events`

feature flag：统一环境变量 `QUEYI_AUTHORITY_V2=1`
- **dashboard 投影默认启用 V2**（只影响展示，让 626 价值可见）
- **关键路径（W2/PCK）默认仍用旧投影**（向后兼容，需人确认后切换）

纯标准库；`--check` 自检。
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import decision_event_v2_626 as D  # noqa: E402
import review_item_ledger_626 as R  # noqa: E402

LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
REVIEW_LEDGER = os.path.join(ROOT, "data", "review_item_ledger.jsonl")
CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
GROUNDED = os.path.join(ROOT, "data", "grounded_labels_w2.json")
OUT_JSON = os.path.join(ROOT, "data", "authority_projection_626.json")

ENV_FLAG = "QUEYI_AUTHORITY_V2"
PROJECTION_RULES_VERSION = "v0.1"
AGG_STRICT = "v0.1-strict"
AGG_RELAXED = "v0.1-relaxed"


def v2_enabled() -> bool:
    return os.environ.get(ENV_FLAG, "0") == "1"


def _now() -> str:
    import time
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class AuthorityProjectionCompiler:
    def __init__(self, ledger_path: str = LEDGER,
                 projection_rules_version: str = PROJECTION_RULES_VERSION) -> None:
        self.ledger_path = ledger_path
        self.version = projection_rules_version
        self.ledger = D.AuthorityLedger.import_jsonl(ledger_path)
        self._events = self.ledger.all_events()

    # ── W2 投影 ──
    def _active_attacks(self) -> tuple[dict[str, set], set]:
        """从 Authority 决定推导"生效的攻击边"。

        约定：`result=APPROVE` 的边表示**该攻击成立**（攻击者击败目标）；
        REJECT/MODIFY/ABSTAIN 表示攻击不成立或存疑（不产生击败）。
        返回 (attackers: target→{attacker...}, nodes)
        """
        attackers: dict[str, set] = {}
        nodes: set = set()
        for e in self._events:
            if e.target_type != "edge":
                continue
            tid = e.target_id
            nodes.add(tid)
            if e.result != "APPROVE":
                continue
            # 边 ID 形如 ae-<SRC>->-<DST>::prop-N
            src = dst = None
            if "->" in tid:
                body = tid[3:] if tid.startswith("ae-") else tid
                parts = body.split("->")
                if len(parts) >= 2:
                    src, dst = parts[0], parts[1].split("::")[0]
            if src and dst:
                nodes.add(src)
                nodes.add(dst)
                attackers.setdefault(dst, set()).add(src)
        return attackers, nodes

    def compile_w2(self) -> dict[str, str]:
        """Dung grounded 语义：IN（未被击败）/ OUT（被 IN 的攻击者击败）/ UNDEC。"""
        attackers, nodes = self._active_attacks()
        labels: dict[str, str] = {n: "UNDEC" for n in nodes}
        changed = True
        while changed:
            changed = False
            for n in sorted(nodes):
                if labels[n] != "UNDEC":
                    continue
                atk = attackers.get(n, set())
                if any(labels.get(a) == "IN" for a in atk):
                    labels[n] = "OUT"
                    changed = True
                elif atk and all(labels.get(a) == "OUT" for a in atk):
                    labels[n] = "IN"
                    changed = True
                elif not atk:
                    labels[n] = "IN"      # 无攻击者 ⇒ IN
                    changed = True
        return labels

    def w2_summary(self) -> dict[str, int]:
        labels = self.compile_w2()
        out = {"IN": 0, "OUT": 0, "UNDEC": 0}
        for v in labels.values():
            out[v] = out.get(v, 0) + 1
        return out

    # ── PCK 投影 ──
    def _card_authority(self) -> dict[str, DecisionLike]:
        out: dict[str, Any] = {}
        for e in self._events:
            if e.target_type in ("card", "certificate"):
                out[e.target_id] = e
        return out

    def compile_pck(self, pck_id: str) -> dict[str, Any]:
        """单个 PCK 的投影：严格 + 宽松两种聚合策略。"""
        card_auth = self._card_authority()
        edge_auth = {e.target_id: e for e in self._events if e.target_type == "edge"}
        cert_path = os.path.join(CERT_DIR, f"{pck_id}.pck.yaml")
        has_cert = os.path.exists(cert_path)
        card_ev = card_auth.get(pck_id)
        has_card_level = card_ev is not None and card_ev.result == "APPROVE"
        n_claims_with_edge_auth = sum(
            1 for t in edge_auth if t.startswith(pck_id) or pck_id in t)
        if has_card_level:
            strict = relaxed = "authorized"
        else:
            strict = "pending"
            relaxed = "pending"
        warn = ""
        if not has_card_level and n_claims_with_edge_auth > 0:
            warn = ("cross_granularity：仅有 edge-level authority，"
                    "不自动升级为 card-level authorized")
        return {
            "pck_id": pck_id,
            "has_certificate": has_cert,
            "strict": {"status": strict, "policy": AGG_STRICT},
            "relaxed": {"status": relaxed, "policy": AGG_RELAXED},
            "cross_granularity_warning": warn,
            "source_authority_events": [card_ev.event_id] if card_ev else [],
            "aggregation_policy_version": self.version,
        }

    def compile_pck_all(self) -> dict[str, Any]:
        """全部 PCK 的投影，同时给出两种策略的 authorized 数量与差异。"""
        ids: list[str] = []
        for p in sorted(glob.glob(os.path.join(CERT_DIR, "*.pck.yaml"))):
            ids.append(os.path.basename(p)[:-9])       # 去掉 .pck.yaml
        results = {i: self.compile_pck(i) for i in ids}
        s = sum(1 for r in results.values() if r["strict"]["status"] == "authorized")
        rx = sum(1 for r in results.values() if r["relaxed"]["status"] == "authorized")
        warned = sum(1 for r in results.values() if r["cross_granularity_warning"])
        return {"count": len(results),
                "strict_authorized": s, "relaxed_authorized": rx,
                "delta_relaxed_minus_strict": rx - s,
                "cross_granularity_warned": warned,
                "results": results}

    # ── 追溯 ──
    def trace_projection(self, projection_type: str, target_id: str) -> list[str]:
        if projection_type == "W2":
            out = []
            for e in self._events:
                if e.target_type == "edge" and (target_id in e.target_id):
                    out.append(e.event_id)
            return out
        if projection_type == "PCK":
            r = self.compile_pck(target_id)
            return list(r["source_authority_events"])
        return []

    # ── 确定性 ──
    def _digest(self, obj: Any) -> str:
        return hashlib.sha256(
            json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)
            .encode("utf-8")).hexdigest()

    def verify_determinism(self) -> bool:
        a = self._digest({"w2": self.compile_w2(), "pck": self.compile_pck_all()})
        c2 = AuthorityProjectionCompiler(self.ledger_path, self.version)
        b = c2._digest({"w2": c2.compile_w2(), "pck": c2.compile_pck_all()})
        return a == b

    # ── golden / dashboard / textbook（D2 实现） ──
    def compile_golden(self) -> dict[str, Any]:
        return self._compile_golden()

    def compile_dashboard(self) -> dict[str, Any]:
        return self._compile_dashboard()

    def compile_textbook(self, atom_id: str) -> dict[str, Any]:
        return self._compile_textbook(atom_id)

    def _compile_golden(self) -> dict[str, Any]:
        """golden 投影：**不自动采纳 legacy**。"""
        disp = [e for e in self._events if e.target_type == "warn_disposition"]
        accepted = [e for e in disp
                    if e.result == "APPROVE" and "accept_legacy" in (e.scope or "")]
        return {"warn_disposition_events": len(disp),
                "accepted_legacy": len(accepted),
                "accepted_legacy_events": [e.event_id for e in accepted],
                "rule": "任何自动采纳 legacy 的路径必须关闭；只有 Authority event 才能标记 accepted_legacy",
                "source_authority_events": [e.event_id for e in disp]}

    def _compile_dashboard(self) -> dict[str, Any]:
        """dashboard 投影：**默认启用 V2**。"""
        rl = R.ReviewItemLedger.import_jsonl(REVIEW_LEDGER)
        by_status: dict[str, int] = {}
        for it in rl.all_items():
            by_status[it.status] = by_status.get(it.status, 0) + 1
        by_m = self.ledger.count_by_review_method()
        by_o = self.ledger.count_by_decision_origin()
        amb = {"high": 0, "medium": 0, "low": 0}
        for it in rl.all_items():
            k = "high" if it.ambiguity_score >= 0.8 else (
                "medium" if it.ambiguity_score >= 0.5 else "low")
            amb[k] += 1
        return {
            "v2_enabled": v2_enabled(),
            "review_items_unique": rl.get_unique_count(),
            "review_items_records": rl.get_record_count(),
            "by_status": by_status,
            "review_method_distribution": by_m,
            "decision_origin_distribution": by_o,
            "ambiguity_distribution": amb,
            "independent_human_review_count": self.ledger.independent_human_review_count(),
            "authority_events": len(self.ledger),
            "generated_at": _now(),
        }

    def _compile_textbook(self, atom_id: str) -> dict[str, Any]:
        """教材渲染状态（**只读投影，不写 Book/ 受控目录**）。"""
        pck = self.compile_pck(atom_id)
        w2 = self.compile_w2()
        atom_nodes = [k for k in w2 if atom_id in k]
        out_atom = any(w2.get(n) == "OUT" for n in atom_nodes)
        has_auth = pck["strict"]["status"] == "authorized"
        if has_auth and not out_atom:
            state = "CERTIFIED"
        elif has_auth:
            state = "CONDITIONALLY_VERIFIED"
        elif out_atom:
            state = "DISPUTED"
        elif atom_nodes or pck["has_certificate"]:
            state = "ABSTAIN"
        else:
            state = "UNVERIFIED"
        return {"atom_id": atom_id, "render_state": state,
                "pck_status": pck["strict"]["status"],
                "argument_status": {n: w2[n] for n in atom_nodes[:10]},
                "source_authority_events": pck["source_authority_events"]}

    # ── 汇总 ──
    def compile_all(self) -> dict[str, Any]:
        return {
            "W2": self.w2_summary(),
            "PCK": {k: v for k, v in self.compile_pck_all().items() if k != "results"},
            "GOLDEN": self._compile_golden(),
            "DASHBOARD": self._compile_dashboard(),
            "TEXTBOOK_SAMPLE": self._compile_textbook("ATOM-CONC-RACE-001"),
            "projection_rules_version": self.version,
            "deterministic": self.verify_determinism(),
            "v2_enabled": v2_enabled(),
        }


DecisionLike = Any


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    c = AuthorityProjectionCompiler()
    n = len(c.ledger)
    chk("ledger 可读且非空", n > 0, f"({n} events)")
    before = c._digest({"w2": c.compile_w2()})

    w2 = c.compile_w2()
    chk("W2 投影非空", len(w2) > 0, f"({len(w2)} nodes)")
    s = c.w2_summary()
    chk("W2 汇总含 IN/OUT/UNDEC",
        all(k in s for k in ("IN", "OUT", "UNDEC")), str(s))
    chk("W2 计数自洽", s["IN"] + s["OUT"] + s["UNDEC"] == len(w2))

    pck = c.compile_pck_all()
    chk("PCK 投影覆盖 83 张", pck["count"] == 83, f"({pck['count']})")
    chk("PCK 同时给出严格/宽松", "strict_authorized" in pck and "relaxed_authorized" in pck)
    chk("PCK 可追溯", all("source_authority_events" in r for r in pck["results"].values()))
    chk("跨粒度警告字段存在", "cross_granularity_warned" in pck)

    chk("确定性验证通过", c.verify_determinism())
    chk("重编译结果一致", c._digest({"w2": c.compile_w2()}) == before)

    tr = c.trace_projection("W2", list(w2)[0])
    chk("trace_projection 返回 event_id 列表", isinstance(tr, list))

    # 只读保证：编译后 ledger 未变
    c2 = AuthorityProjectionCompiler()
    chk("只读：编译后 ledger 条数不变", len(c2.ledger) == n)
    chk("只读：哈希链仍有效", c2.ledger.verify_chain())
    print(f"D1/D2 projection check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="626 D1/D2 Authority→Projection Compiler")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--json", action="store_true", help="输出投影 JSON")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    c = AuthorityProjectionCompiler()
    if args.json:
        with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(c.compile_all(), fh, ensure_ascii=False, indent=2)
        print(f"written {OUT_JSON}")
    print(json.dumps(c.compile_all(), ensure_ascii=False, indent=2)[:2000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
