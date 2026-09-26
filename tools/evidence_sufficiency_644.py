"""644 阶段 B · B2 证据充分性判定器。

对每张卡片，依 A1 调研结论（B1 等级 + GRADE「多源/升级」）判定证据是否充分：
1. 至少 1 条 L1 或 L2 证据？           2. 至少 3 条独立证据？
3. 反例是否已被处理？                   4. 证据是否过期？
5. 证据 hash 是否与文件一致（artifact_sha256 齐备）？

输出：充分 / 不足 / 需人审，并附缺失项清单（设计输入 2）。
只读：不修改受控目录。`--check` 只读幂等；`--report` 写全量充分性报告。
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base

OUT_MD = os.path.join(base.ROOT, "data", "644_sufficiency_report.md")
MIN_INDEPENDENT = 3
FRESHNESS_TTL_DAYS = 365 * 5  # 现有证据无时间戳，按「历史取证」宽限，不轻易判过期


def judge(card_id: str, ev_list: list[dict[str, Any]]) -> dict[str, Any]:
    """纯函数：对一组证据判定某卡的充分性。"""
    n = len(ev_list)
    has_strong = any(e["grade"] in ("L1", "L2") for e in ev_list)
    independent_count = len({e["id"] for e in ev_list})
    has_refute = any(str(e.get("verdict", "")).lower() == "refute" for e in ev_list)
    # 反例已处理：没有反例，或所有 refute 证据都带有 falsification 分析
    refute_handled = (not has_refute) or all(
        (str(e.get("verdict", "")).lower() != "refute") or bool(e.get("falsification"))
        for e in ev_list
    )
    expired = _any_expired(ev_list)
    hash_consistent = (n == 0) or all(bool(e.get("artifact_sha256_present")) for e in ev_list)

    missing: list[str] = []
    if n == 0:
        missing.append("无任何证据")
    if not has_strong:
        missing.append("缺少 L1/L2 权威证据")
    if independent_count < MIN_INDEPENDENT:
        missing.append(f"独立证据不足（{independent_count}/{MIN_INDEPENDENT}）")
    if not refute_handled:
        missing.append("存在反例但未处理（需人审）")
    if expired:
        missing.append("存在过期证据")
    if not hash_consistent:
        missing.append("证据 artifact_sha256 缺失/不一致")

    if not missing:
        verdict = "充分"
    elif (not refute_handled) or (not hash_consistent):
        verdict = "需人审"
    else:
        verdict = "不足"

    return {
        "card": card_id, "n_evidence": n, "has_strong": has_strong,
        "independent_count": independent_count, "has_refute": has_refute,
        "refute_handled": refute_handled, "expired": expired,
        "hash_consistent": hash_consistent, "verdict": verdict,
        "missing": missing,
    }


def _has_falsification(e: dict[str, Any]) -> bool:
    # evidence 记录里若有 falsification 标记（由 card_evidence_map 注入）
    return bool(e.get("falsification"))


def _any_expired(ev_list: list[dict[str, Any]]) -> bool:
    # 现有证据无 acquired_at；头部层获取的证据带时间戳，超 TTL 判过期。
    for e in ev_list:
        at = e.get("acquired_at")
        if at and _age_days(at) > FRESHNESS_TTL_DAYS:
            return True
    return False


def _age_days(iso: str) -> int:
    try:
        from datetime import date
        y, m, d = (int(x) for x in iso.split("-")[:3])
        return (date.today() - date(y, m, d)).days
    except (ValueError, TypeError):
        return 0


def judge_all() -> list[dict[str, Any]]:
    """对全量卡片判定（只读）。"""
    m = base.card_evidence_map()
    fal_by_id = {e["id"]: bool(e["meta"].get("falsification"))
                 for e in base.list_existing_evidence()}
    results = []
    for card in base.list_atoms():
        cid = card["id"]
        evs = [dict(e, falsification=fal_by_id.get(e["id"], False))
               for e in m.get(cid, [])]
        results.append(judge(cid, evs))
    return results


def render_md(results: list[dict[str, Any]]) -> str:
    counts = {"充分": 0, "不足": 0, "需人审": 0}
    for r in results:
        counts[r["verdict"]] += 1
    weak = sorted(results, key=lambda r: (r["verdict"] != "不足", -r["n_evidence"]))[:10]
    lines = ["# 644 B2 · 证据充分性全量报告", "",
             f"- 充分：**{counts['充分']}**  不足：**{counts['不足']}**  需人审：**{counts['需人审']}**",
             "", "| 卡片 | 证据数 | 强证据 | 独立数 | 反例已处理 | 过期 | hash一致 | 判定 | 缺失 |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(results, key=lambda x: x["card"]):
        lines.append(f"| {r['card']} | {r['n_evidence']} | {'✅' if r['has_strong'] else '❌'} | "
                     f"{r['independent_count']} | {'✅' if r['refute_handled'] else '❌'} | "
                     f"{'❌' if r['expired'] else '✅'} | {'✅' if r['hash_consistent'] else '❌'} | "
                     f"{r['verdict']} | {'; '.join(r['missing']) or '—'} |")
    lines += ["", "## Top 10 证据最薄弱的卡片", "", "| 卡片 | 判定 | 证据数 | 缺失 |", "|---|---|---|---|"]
    for r in weak:
        lines.append(f"| {r['card']} | {r['verdict']} | {r['n_evidence']} | {'; '.join(r['missing']) or '—'} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_report() -> str:
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_md(judge_all()))
    return OUT_MD


def selftest() -> int:
    # 已知充分卡：3 条 L1/L2、无反例、hash 齐备
    good = [{"id": f"E{i}", "grade": "L1", "verdict": "confirm", "acquired_at": None,
             "artifact_sha256_present": True, "falsification": False} for i in range(3)]
    r = judge("C-good", good)
    assert r["verdict"] == "充分" and r["missing"] == []
    # 已知不足卡：无 L1/L2 且只有 1 条
    bad = [{"id": "E1", "grade": "L4", "verdict": "confirm", "acquired_at": None,
            "artifact_sha256_present": True, "falsification": False}]
    r2 = judge("C-bad", bad)
    assert r2["verdict"] in ("不足", "需人审")
    miss2 = "".join(r2["missing"])
    assert "缺少 L1/L2 权威证据" in miss2
    assert "独立证据不足" in miss2
    # 反例未处理 → 需人审
    ref = good + [{"id": "E9", "grade": "L2", "verdict": "refute", "acquired_at": None,
                   "artifact_sha256_present": True, "falsification": False}]
    r3 = judge("C-ref", ref)
    assert r3["verdict"] == "需人审" and "存在反例但未处理" in "".join(r3["missing"])
    # hash 缺失 → 需人审
    hbad = [dict(good[0], artifact_sha256_present=False)]
    r4 = judge("C-hash", hbad)
    assert r4["verdict"] == "需人审" and "artifact_sha256" in "".join(r4["missing"])
    # 全量判定可跑且不抛错
    allr = judge_all()
    assert len(allr) == len(base.list_atoms())
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 B2 证据充分性判定器")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--report", action="store_true", help="写全量报告")
    a = ap.parse_args(argv)
    if a.report:
        print(f"written {write_report()}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
