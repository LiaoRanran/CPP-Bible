"""621 C1 · ABSTAIN 六态分类器（雷6：未知检测 / 弃权三态）

六态：SUPPORTED / REFUTED / UNDECIDED / INSUFFICIENT_EVIDENCE / CONFLICTED / STALE
其中后四者是**弃权态** —— ABSTAIN 不是失败，是系统能力。

判定优先级见 `data/abstain_state_definition_621.md` §三：
    INSUFFICIENT_EVIDENCE → CONFLICTED → STALE → REFUTED → SUPPORTED → UNDECIDED

**硬边界**：只读卡 frontmatter，不改卡；不代签任何决策。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

STATES = ("SUPPORTED", "REFUTED", "UNDECIDED",
          "INSUFFICIENT_EVIDENCE", "CONFLICTED", "STALE")
ABSTAIN_STATES = ("UNDECIDED", "INSUFFICIENT_EVIDENCE", "CONFLICTED", "STALE")
STALE_DAYS = 90

DEFAULT_OUT = os.path.join(ROOT, "data", "abstain_classification_621.jsonl")


def _days_since(verified_at: object, now: datetime | None = None) -> int | None:
    if not verified_at:
        return None
    s = str(verified_at).strip()
    if not s or s.lower() == "unknown":
        return None
    try:
        d = datetime.fromisoformat(s[:10])
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return max(0, ((now or datetime.now(timezone.utc)) - d).days)


def classify(state: dict, now: datetime | None = None) -> dict:
    """输入 card_state，输出 {state, reason, is_abstain}。"""
    ev = int(state.get("evidence_count") or 0)
    if ev <= 0:
        return {"state": "INSUFFICIENT_EVIDENCE",
                "reason": "无任何证据锚（claim_structured.evidence / artifact_sha256 皆空）",
                "is_abstain": True}
    if state.get("conflicted"):
        return {"state": "CONFLICTED", "reason": "relations 含 contradicts（证据互相矛盾）",
                "is_abstain": True}
    days = state.get("days_since_verify")
    if days is None:
        days = _days_since(state.get("verified_at"), now)
    if days is not None and days > STALE_DAYS:
        return {"state": "STALE", "reason": f"距上次验证 {days} 天 > {STALE_DAYS} 天",
                "is_abstain": True}
    verdict = str(state.get("verdict") or "").strip().lower()
    if verdict == "refute":
        return {"state": "REFUTED", "reason": "verdict=refute 且证据充分、未过期",
                "is_abstain": False}
    if verdict == "confirm":
        return {"state": "SUPPORTED", "reason": "verdict=confirm 且证据充分、未过期",
                "is_abstain": False}
    return {"state": "UNDECIDED",
            "reason": f"verdict={verdict or '缺失'}，证据不足以判定（含 infra_error 情形）",
            "is_abstain": True}


# ── 622 C1：分类器 v2（verdict 识别 + Authority 交叉验证 + 证据充分性）──────────
# 升级动因（621 C2 实测）：ABSTAIN 与 Authority **完全反相关**
#   （SUPPORTED×pending 56、UNDECIDED×approved 27），
# 根因是 v1 只看「卡上有没有 verdict 字段」，而 Authority 看「人是否批准」。
#
# v2 的判定顺序（在 v1 的 4 个硬前置之后，把"verdict 缺失"从死路改为**多源交叉**）：
#   ① 证据数 0            → INSUFFICIENT_EVIDENCE
#   ② relations 矛盾      → CONFLICTED
#   ③ 超过 90 天          → STALE
#   ④ 卡上 verdict=refute → REFUTED
#   ⑤ 卡上 verdict=confirm→ SUPPORTED
#   ⑥ **提取的 verdict**（C2）→ REFUTED / SUPPORTED
#   ⑦ **Authority=approved** → SUPPORTED ；=rejected → REFUTED
#   ⑧ 其余                → UNDECIDED
#
# 每条结论都带 `basis`，明确"是谁判的"，避免"机器说支持"与"人已批准"混为一谈。
AUTHORITY_LOG = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")


def load_authority_entries(path: str = AUTHORITY_LOG) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [json.loads(ln) for ln in fh if ln.strip()]


def authority_status_for(card_id: str, entries: list[dict]) -> str | None:
    """按 620 C3 的同一规则（子串匹配 target.id）取该卡的 Authority 状态。"""
    if not card_id:
        return None
    hits = [e for e in entries if card_id in str((e.get("target") or {}).get("id", ""))]
    if not hits:
        return None
    power = str(hits[-1].get("power") or "")
    return {"ACCEPT": "approved", "OVERRIDE": "approved",
            "REJECT": "rejected", "ABSTAIN": "abstained"}.get(power)


def classify_v2(state: dict, authority: str | None = None,
                extracted_verdict: str | None = None,
                now: datetime | None = None) -> dict:
    """分类器 v2：与 Authority 判定标准对齐。"""
    ev = int(state.get("evidence_count") or 0)
    if ev <= 0:
        return {"state": "INSUFFICIENT_EVIDENCE", "is_abstain": True,
                "basis": "evidence_count=0", "reason": "无任何证据锚"}
    if state.get("conflicted"):
        return {"state": "CONFLICTED", "is_abstain": True,
                "basis": "relations", "reason": "relations 含 contradicts"}
    days = state.get("days_since_verify")
    if days is None:
        days = _days_since(state.get("verified_at"), now)
    if days is not None and days > STALE_DAYS:
        return {"state": "STALE", "is_abstain": True, "basis": "verified_at",
                "reason": f"距上次验证 {days} 天 > {STALE_DAYS} 天"}

    v = str(state.get("verdict") or "").strip().lower()
    if v == "refute":
        return {"state": "REFUTED", "is_abstain": False, "basis": "card_verdict",
                "reason": "卡面 verdict=refute"}
    if v == "confirm":
        return {"state": "SUPPORTED", "is_abstain": False, "basis": "card_verdict",
                "reason": "卡面 verdict=confirm"}

    ex = str(extracted_verdict or "").strip().lower()
    if ex in ("supported", "confirm"):
        return {"state": "SUPPORTED", "is_abstain": False, "basis": "extracted_verdict",
                "reason": "由卡面内容提取出的 verdict=SUPPORTED"}
    if ex in ("refuted", "refute"):
        return {"state": "REFUTED", "is_abstain": False, "basis": "extracted_verdict",
                "reason": "由卡面内容提取出的 verdict=REFUTED"}

    a = str(authority or "").strip().lower()
    if a == "approved":
        return {"state": "SUPPORTED", "is_abstain": False, "basis": "authority_approved",
                "reason": "卡面无 verdict，但 Authority 已批准（人审交叉验证）"}
    if a == "rejected":
        return {"state": "REFUTED", "is_abstain": False, "basis": "authority_rejected",
                "reason": "卡面无 verdict，但 Authority 已否决"}

    return {"state": "UNDECIDED", "is_abstain": True, "basis": "no_signal",
            "reason": f"无 verdict（卡面/提取）且 Authority={a or 'none'}"}


def pck_authority_map(cert_dir: str | None = None) -> dict[str, str]:
    """从 PCK 证书读 `human_authority.status`（622 C3 规定的权威口径）。

    注：PCK 证书是 620 C3 由「Authority 决策日志 + 卡面 status」派生出的**投影**，
    覆盖面比决策日志广（决策日志只覆盖 25 张原子卡，PCK 覆盖全部 83 张）。
    """
    import glob as _glob  # noqa: PLC0415
    try:
        import yaml  # noqa: PLC0415
    except ImportError:
        return {}
    d = cert_dir or os.path.join(ROOT, "data", "pck", "certificates")
    out: dict[str, str] = {}
    for p in sorted(_glob.glob(os.path.join(d, "*.pck.yaml"))):
        try:
            with open(p, encoding="utf-8") as fh:
                cert = yaml.safe_load(fh.read())
        except Exception:  # noqa: BLE001
            continue
        cid = str((cert.get("claim") or {}).get("id") or "")
        st = (cert.get("human_authority") or {}).get("status")
        if cid and st:
            out[cid] = str(st)
    return out


def classify_card_v2(card_rel: str, authority_entries: list[dict] | None = None,
                     extracted: dict[str, str] | None = None,
                     authority_map: dict[str, str] | None = None,
                     now: datetime | None = None) -> dict:
    """按卡分类（v2）：自动取 Authority 状态与（可选的）C2 提取 verdict。

    `authority_map` 优先（PCK 投影口径）；未提供时回退到决策日志子串匹配。
    """
    sys.path.insert(0, HERE)
    import pck_batch_migrator_620 as M  # noqa: PLC0415
    fm = M.read_frontmatter(os.path.join(ROOT, card_rel))
    st = build_state(fm, card_rel, now)
    card_id = fm.get("id") or os.path.basename(card_rel).replace(".md", "")
    if authority_map is not None:
        auth = authority_map.get(card_id)
        auth_source = "pck_human_authority"
    else:
        entries = (authority_entries if authority_entries is not None
                   else load_authority_entries())
        auth = authority_status_for(card_id, entries)
        auth_source = "authority_decision_log"
    res = classify_v2(st, authority=auth,
                      extracted_verdict=(extracted or {}).get(card_id), now=now)
    return {"card": card_rel, "card_id": card_id,
            "kind": "atom" if card_rel.startswith("atoms/") else "evidence",
            "domain": card_rel.split("/")[1] if card_rel.count("/") > 1 else "unknown",
            "authority": auth, "authority_source": auth_source,
            "extracted_verdict": (extracted or {}).get(card_id),
            "input": st, **res}


def classify_all_v2(cards: list[str], extracted: dict[str, str] | None = None,
                    authority_entries: list[dict] | None = None,
                    authority_map: dict[str, str] | None = None,
                    now: datetime | None = None) -> list[dict]:
    """对一批卡跑 v2 分类（只读）。

    `authority_map`（PCK 口径）优先；否则回退决策日志。
    """
    amap = authority_map if authority_map is not None else pck_authority_map()
    return [classify_card_v2(c, extracted=extracted, authority_map=amap, now=now)
            for c in cards]


# 对齐口径：机器判定 vs 人审授权
ALIGNED_PAIRS = {("SUPPORTED", "approved"), ("REFUTED", "rejected")}
MACHINE_ABSTAIN_STATES = ("UNDECIDED", "INSUFFICIENT_EVIDENCE", "CONFLICTED", "STALE")


def alignment_crosstab(rows: list[dict]) -> dict:
    """ABSTAIN × Authority 交叉表 + 对齐分析（622 C3）。"""
    cross: dict[tuple, int] = {}
    for r in rows:
        cross[(r["state"], str(r.get("authority")))] = \
            cross.get((r["state"], str(r.get("authority"))), 0) + 1
    aligned = sum(n for (st, au), n in cross.items() if (st, au) in ALIGNED_PAIRS)
    # 「机器说支持、人没批」与「机器弃权、人却批了」两类缺口
    machine_supported_human_pending = sum(
        n for (st, au), n in cross.items() if st == "SUPPORTED" and au == "pending")
    machine_abstain_human_approved = sum(
        n for (st, au), n in cross.items() if st in MACHINE_ABSTAIN_STATES and au == "approved")
    total = len(rows)
    return {
        "cross": {f"{k[0]}×{k[1]}": v for k, v in sorted(cross.items())},
        "total": total,
        "aligned": aligned,
        "aligned_rate": round(aligned / total, 4) if total else None,
        "machine_supported_human_pending": machine_supported_human_pending,
        "machine_abstain_human_approved": machine_abstain_human_approved,
        "abstain_count": sum(n for (st, _au), n in cross.items()
                             if st in MACHINE_ABSTAIN_STATES),
    }


def build_state(fm: dict, card_rel: str, now: datetime | None = None) -> dict:
    """从 frontmatter 构造 card_state（只读派生）。"""
    is_atom = card_rel.startswith("atoms/")
    cs = fm.get("claim_structured") or []
    if is_atom:
        ev: list = []
        for c in cs:
            if isinstance(c, dict):
                ev.extend([e for e in (c.get("evidence") or []) if isinstance(e, str)])
        evidence_count = len(ev)
    else:
        evidence_count = 1 if fm.get("artifact_sha256") else 0
    relations = fm.get("relations") or []
    conflicted = any(isinstance(r, dict)
                     and str(r.get("type", "")).lower().startswith("contradict")
                     for r in relations)
    # yaml 会把 verified_at 解析成 datetime.date ⇒ 统一转成字符串，保证 JSON 可序列化
    va = fm.get("verified_at")
    va_str = str(va)[:10] if va else None
    return {
        "evidence_count": evidence_count,
        "conflicted": conflicted,
        "verdict": fm.get("verdict"),
        "status": fm.get("status"),
        "verified_at": va_str,
        "days_since_verify": _days_since(va_str, now),
    }


def classify_card(card_rel: str, now: datetime | None = None) -> dict:
    sys.path.insert(0, HERE)
    import pck_batch_migrator_620 as M  # noqa: PLC0415
    fm = M.read_frontmatter(os.path.join(ROOT, card_rel))
    st = build_state(fm, card_rel, now)
    res = classify(st, now)
    return {
        "card": card_rel,
        "card_id": fm.get("id") or os.path.basename(card_rel).replace(".md", ""),
        "kind": "atom" if card_rel.startswith("atoms/") else "evidence",
        "domain": card_rel.split("/")[1] if card_rel.count("/") > 1 else "unknown",
        "input": st,
        **res,
    }


def classify_all(cards: list[str], now: datetime | None = None) -> list[dict]:
    return [classify_card(c, now) for c in cards]


def write_jsonl(rows: list[dict], path: str = DEFAULT_OUT) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    return path


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    now = datetime(2026, 9, 22, tzinfo=timezone.utc)
    chk("SUPPORTED：confirm + 有证据",
        classify({"evidence_count": 2, "verdict": "confirm"}, now)["state"] == "SUPPORTED")
    chk("REFUTED：refute + 有证据",
        classify({"evidence_count": 2, "verdict": "refute"}, now)["state"] == "REFUTED")
    chk("UNDECIDED：verdict 缺失",
        classify({"evidence_count": 2, "verdict": None}, now)["state"] == "UNDECIDED")
    chk("UNDECIDED：infra_error 也算弃权",
        classify({"evidence_count": 2, "verdict": "infra_error"}, now)["is_abstain"] is True)
    chk("INSUFFICIENT_EVIDENCE：证据数 0",
        classify({"evidence_count": 0, "verdict": "confirm"}, now)["state"]
        == "INSUFFICIENT_EVIDENCE")
    chk("CONFLICTED：relations 矛盾",
        classify({"evidence_count": 2, "verdict": "confirm", "conflicted": True}, now)["state"]
        == "CONFLICTED")
    chk("STALE：超过 90 天",
        classify({"evidence_count": 2, "verdict": "confirm",
                  "verified_at": "2026-01-01"}, now)["state"] == "STALE")
    chk("非 STALE：90 天内",
        classify({"evidence_count": 2, "verdict": "confirm",
                  "verified_at": "2026-09-01"}, now)["state"] == "SUPPORTED")
    chk("六态集合完整", set(STATES) == {"SUPPORTED", "REFUTED", "UNDECIDED",
                                    "INSUFFICIENT_EVIDENCE", "CONFLICTED", "STALE"})
    chk("弃权态 4 个", len(ABSTAIN_STATES) == 4)
    chk("days_since 解析", _days_since("2026-09-01", now) == 21)
    chk("unknown 日期不解析", _days_since("unknown", now) is None)

    # ── 622 C1：v2 升级项 ──
    chk("v2：无 verdict 但 Authority 批准 ⇒ SUPPORTED",
        classify_v2({"evidence_count": 3, "verdict": None}, authority="approved",
                    now=now)["state"] == "SUPPORTED")
    chk("v2：无 verdict 且 Authority 未批 ⇒ UNDECIDED",
        classify_v2({"evidence_count": 3, "verdict": None}, authority="pending",
                    now=now)["state"] == "UNDECIDED")
    chk("v2：提取 verdict 优先于 Authority",
        classify_v2({"evidence_count": 3, "verdict": None}, authority="approved",
                    extracted_verdict="refuted", now=now)["state"] == "REFUTED")
    chk("v2：卡面 verdict 优先于提取与 Authority",
        classify_v2({"evidence_count": 3, "verdict": "refute"}, authority="approved",
                    extracted_verdict="supported", now=now)["state"] == "REFUTED")
    chk("v2：硬前置（无证据）仍优先",
        classify_v2({"evidence_count": 0, "verdict": "confirm"}, authority="approved",
                    now=now)["state"] == "INSUFFICIENT_EVIDENCE")
    chk("v2：每态带 basis",
        all(classify_v2(s, now=now).get("basis")
            for s in ({"evidence_count": 0}, {"evidence_count": 1, "conflicted": True},
                      {"evidence_count": 1, "verified_at": "2020-01-01"},
                      {"evidence_count": 1, "verdict": "confirm"},
                      {"evidence_count": 1, "verdict": "refute"},
                      {"evidence_count": 1, "verdict": None})))
    chk("v2：Authority 子串匹配",
        authority_status_for("ATOM-MEM-PERF-003",
                             [{"target": {"id": "ae-X->ATOM-MEM-PERF-003::prop-1"},
                               "power": "ACCEPT"}]) == "approved")
    print(f"C1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="621 C1 ABSTAIN 六态分类器")
    ap.add_argument("--all", action="store_true", help="对全量 83 张卡分类")
    ap.add_argument("--card", action="append", help="指定卡（可多次）")
    ap.add_argument("--output", default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    if args.card:
        cards = args.card
    elif args.all:
        sys.path.insert(0, HERE)
        import pck_batch_migrator_620 as M  # noqa: PLC0415
        cards = M.discover_cards()
    else:
        ap.print_help()
        return 0

    rows = classify_all(cards)
    if args.output and args.all:
        write_jsonl(rows, args.output)
        dist: dict[str, int] = {}
        for r in rows:
            dist[r["state"]] = dist.get(r["state"], 0) + 1
        print(json.dumps({"total": len(rows), "distribution": dist}, ensure_ascii=False))
    else:
        for r in rows:
            print(json.dumps(r, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
