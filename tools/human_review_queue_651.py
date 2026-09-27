#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""human_review_queue_651.py — M7 人审接口修复（651 W3）。

为什么（651 W3-M7）：647 A2 的实测洞是"**缺字段被默认放行**"。本工具按 **fail-closed** 重做接口：
- **缺关键字段（item_id/target/reason）⇒ 拒收**（进 `rejected`，附白名单 `reject_reason`），**绝不默认填充**；
- 条目 `reason` 必须在**封闭白名单**内，否则拒收（`unknown_reason`）——**自由文本不算数**；
- 真队列 schema 不一致时，提供**显式可审计的适配器**（字段别名 + 自由文本→枚举规范化，逐条留痕），
  **而不是**在读取时静默塞默认值。

用法
====
    python tools/human_review_queue_651.py --check                 # 合成自检（含 fail-closed）
    python tools/human_review_queue_651.py --build                 # 真队列：raw 严格 vs adapted 适配 对照
    python tools/human_review_queue_651.py --json

诚实边界：本工具**不代签**；三率看板缺数据处报 `None`（不编造）。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "protector", "name": "human_review_queue_651", "entry": "build_queue",
                "description": "M7 人审队列：缺字段 fail-closed + reason 白名单 + 优先级 + 三率看板"}

PENDING = ROOT / "data" / "authority" / "pending_review_621.jsonl"
OUT = ROOT / "data" / "651_m7_queue.json"
M3_OUT = ROOT / "data" / "651_m3_calibration.json"

REQUIRED_FIELDS = ("item_id", "target", "reason")   # created_at 可选（仅用于老化，不做默认填充）
REASON_ENUM = {"conflict", "blind_violation", "calibration_over", "mdl_reject", "aging", "needs_human"}
REJECT_REASONS = {"missing_field", "unknown_reason", "malformed"}

# 真队列字段别名（显式、可审计；仅在 --build 的 adapted 视图用）
ALIASES = {"item_id": ("item_id", "proposal_id"), "target": ("target", "atom_card"),
           "reason": ("reason", "suggested_reason"), "created_at": ("created_at", "review_at", "ts")}

# 自由文本 → 枚举的**显式**规范化规则（无匹配 ⇒ None ⇒ 拒收，不猜）
REASON_PATTERNS = (
    ("需独立判断", "needs_human"), ("rubber-stamp", "needs_human"), ("复核", "needs_human"),
    ("盲", "blind_violation"), ("冲突", "conflict"), ("校准", "calibration_over"),
    ("MDL", "mdl_reject"), ("老化", "aging"),
)

SEVERITY = {"blind_violation": 3.0, "conflict": 2.5, "calibration_over": 2.0,
            "mdl_reject": 1.5, "aging": 1.0, "needs_human": 0.5}
COST = {"blind_violation": 2.0, "conflict": 2.0, "calibration_over": 1.5,
        "mdl_reject": 1.0, "aging": 0.5, "needs_human": 0.5}


def normalize_reason(text: str | None) -> str | None:
    """自由文本 → 枚举（仅显式模式命中；否则 None）。"""
    if not text:
        return None
    if text in REASON_ENUM:
        return text
    for pat, val in REASON_PATTERNS:
        if pat in text:
            return val
    return None


def adapt_item(item: dict) -> tuple[dict, list[str]]:
    """字段别名 + reason 规范化；返回 (适配后对象, 留痕)。**不做默认填充**：缺则保持缺。"""
    if not isinstance(item, dict):
        return {"_raw": str(item)}, ["malformed"]
    out: dict = {}
    log: list[str] = []
    for dst, names in ALIASES.items():
        src_name = None
        for nm in names:
            if nm in item and item[nm] not in (None, ""):
                src_name = nm
                break
        if src_name is not None:
            out[dst] = item[src_name]
            if src_name != names[0]:
                log.append(f"{dst} <= {src_name}")
    if "reason" in out:
        norm = normalize_reason(str(out["reason"]))
        log.append(f"reason: {str(out['reason'])[:24]}… → {norm}")
        if norm is None:
            out.pop("reason")   # 规范化失败 ⇒ 移除 ⇒ fail-closed 拒收（不猜）
        else:
            out["reason"] = norm
    return out, log


def validate_item(item: dict) -> tuple[bool, str | None]:
    if not isinstance(item, dict):
        return False, "malformed"
    for f in REQUIRED_FIELDS:
        v = item.get(f)
        if v is None or (isinstance(v, str) and not v.strip()):
            return False, "missing_field"
    if item["reason"] not in REASON_ENUM:
        return False, "unknown_reason"
    return True, None


def score(item: dict) -> float:
    sev = SEVERITY.get(item["reason"], 1.0)
    imp = float(item.get("impact", 1.0) or 1.0)
    return round(sev * imp / COST.get(item["reason"], 1.0), 4)


def build_queue(items: list[dict], adapt: bool = False) -> dict:
    accepted, rejected = [], []
    for it in items:
        log: list[str] = []
        cur = it
        if adapt:
            cur, log = adapt_item(it)
        ok, why = validate_item(cur)
        if ok:
            accepted.append({**cur, "priority": score(cur), **( {"adapt_log": log} if log else {})})
        else:
            rejected.append({"item": it if isinstance(it, dict) else {"raw": str(it)},
                             "reject_reason": why, **({"adapt_log": log} if log else {})})
    accepted.sort(key=lambda x: x["priority"], reverse=True)
    return {"total": len(items), "accepted": accepted, "rejected": rejected, "rejected_count": len(rejected)}


def three_rate_dashboard(queue: dict, blind_violations: int | None = None,
                         review_total: int | None = None) -> dict:
    total = queue["total"] or 1
    calib_over = None
    if M3_OUT.is_file():
        try:
            m3 = json.loads(M3_OUT.read_text(encoding="utf-8"))
            strata = m3.get("strata") or 0
            calib_over = round(len(m3.get("forced_recalibration", [])) / strata, 4) if strata else None
        except json.JSONDecodeError:
            calib_over = None
    blind = (round(blind_violations / review_total, 4)
             if (blind_violations is not None and review_total) else None)
    return {"blind_violation_rate": blind,
            "calibration_over_rate": calib_over,
            "fail_closed_reject_rate": round(queue["rejected_count"] / total, 4),
            "note": "缺数据处为 None（未编造）。"}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    good = {"item_id": "I1", "target": "T", "reason": "conflict", "impact": 2.0}
    missing = {"item_id": "I2", "reason": "conflict"}
    badreason = {"item_id": "I3", "target": "T", "reason": "wat"}
    q = build_queue([good, missing, badreason])
    chk("合法入队", len(q["accepted"]) == 1)
    chk("缺字段 fail-closed", any(r["reject_reason"] == "missing_field" for r in q["rejected"]))
    chk("非法 reason 拒收", any(r["reject_reason"] == "unknown_reason" for r in q["rejected"]))
    # 规范化
    chk("自由文本→枚举", normalize_reason("复核 approve") == "needs_human")
    chk("无匹配 ⇒ None", normalize_reason("完全无关的话") is None)
    # 适配器：真队列风格对象（proposal_id/atom_card/自由文本 reason）
    raw = {"proposal_id": "prop-1", "atom_card": "ATOM-X", "suggested_reason": "复核 approve"}
    chk("raw 严格 ⇒ 拒收", build_queue([raw])["rejected_count"] == 1)
    ad = build_queue([raw], adapt=True)
    chk("adapted ⇒ 收下", len(ad["accepted"]) == 1 and ad["accepted"][0]["reason"] == "needs_human")
    chk("adapted 留痕", bool(ad["accepted"][0].get("adapt_log")))
    # 优先级
    a = {"item_id": "a", "target": "T", "reason": "blind_violation", "impact": 1.0}
    b = {"item_id": "b", "target": "T", "reason": "needs_human", "impact": 1.0}
    chk("优先级排序", build_queue([b, a])["accepted"][0]["item_id"] == "a")
    chk("盲率缺数据 ⇒ None", three_rate_dashboard(q)["blind_violation_rate"] is None)
    print(f"human_review_queue_651 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="651 M7 人审队列（fail-closed + 适配器 + 三率看板）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--pending", default=str(PENDING))
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    items = []
    p = Path(a.pending)
    if p.is_file():
        for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if ln.strip():
                try:
                    items.append(json.loads(ln))
                except json.JSONDecodeError:
                    items.append({"__raw__": ln[:80]})
    raw = build_queue(items)
    adapted = build_queue(items, adapt=True)
    rep = {"source": str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p),
           "raw": {"total": raw["total"], "accepted": len(raw["accepted"]), "rejected": raw["rejected_count"]},
           "adapted": {"total": adapted["total"], "accepted": len(adapted["accepted"]),
                       "rejected": adapted["rejected_count"],
                       "sample_accept": adapted["accepted"][:2]},
           "raw_reject_reasons": _count(raw["rejected"]),
           "dashboard": three_rate_dashboard(raw)}
    if a.build:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"raw: {raw['total']} 条 → 收 {len(raw['accepted'])} / 拒 {raw['rejected_count']}"
              f"\nadapted: → 收 {len(adapted['accepted'])} / 拒 {adapted['rejected_count']}"
              f"\n{rep['dashboard']}\n→ {OUT.name}")
        return 0
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json else json.dumps(rep["raw"], ensure_ascii=False))
    return 0


def _count(rejected: list[dict]) -> dict:
    c: dict[str, int] = {}
    for r in rejected:
        c[r["reject_reason"]] = c.get(r["reject_reason"], 0) + 1
    return c


if __name__ == "__main__":
    raise SystemExit(main())
