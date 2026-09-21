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
