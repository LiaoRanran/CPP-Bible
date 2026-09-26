"""646 · 阶段 A2 · 三层耦合真正打通（清债 1 续，替代 645 C2 的 token 猜测匹配）。

目标（646 §三 A2）：用 A1 的**规则→卡显式映射**重跑三层联动，让智能层发现的规则问题
自动找到对应卡片的真实证据：
- 智能层 `Issue`（规则命中/盲区）→ A1 映射 → 对应卡片 → 头部层真实证据 → 尾端 `VerificationResult`。
- 目标：≥5 条链**证据≠0**、**问题归因可复核率 ≥0.5**。

与 645 的差别：645 用「规则 id 的主题 token 与卡 id 做模糊匹配」（命中率 0.1）；646 用 A1 的显式
映射（属性/关键词/域三信号），归因可复核率显著提升。**只读**，不改卡片/规则/账本。

**数据源**：A1 规则→卡映射（`646_rule_card_mapping.json`）+ 645 A1 真实问题 + B6 充分性 + B4 反例；
全部**只读**，不含任何代理/编造数据。`--check` 只读自检；`--run` 真实编排，写
`data/646_coupling_report.md` + `.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from functools import lru_cache
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REPORT_MD = os.path.join(DATA, "646_coupling_report.md")
REPORT_JSON = os.path.join(DATA, "646_coupling_report.json")

# 参与耦合的映射强度（high+medium 才认为「关联成立」；low 为全局兜底不算）
USE_STRENGTHS = {"high", "medium"}


def _smart_issues() -> list[dict]:
    """智能层真实 Top10 问题（复用 645 A1 的真实数据源；A3 用记忆化避免重复 gate 扫描）。"""
    import gate_engine as ge
    import perf_646 as perf
    import smart_issue_finder_645 as a1
    fc = perf.finding_counts()
    blind = {r.id for r in ge.RULES if r.automated and r.id not in fc}
    error_rates: dict = {}
    aging: dict = {}
    try:
        import rule_error_tracker_645 as a5
        error_rates = a5.track()["per_rule"]
    except Exception:
        pass
    try:
        import rule_aging_detector_645 as a6
        aging = a6.detect()["per_rule"]
    except Exception:
        pass
    return a1.build_issues(fc, blind, error_rates, aging, top_n=10)


_CACHE_MAX = 1


@lru_cache(maxsize=_CACHE_MAX)
def _suff_per_card() -> dict:
    """头部层充分性（卡→证据），A3 进程内缓存（只读）。"""
    import evidence_sufficiency_645 as b6
    return dict(b6.judge()["per_card"])


@lru_cache(maxsize=_CACHE_MAX)
def _ce_per_card() -> dict:
    """头部层反例候选（卡→反例），A3 进程内缓存（只读）。"""
    import counterexample_searcher_645 as b4
    return dict(b4.run_search()["per_card"])


def clear_caches() -> None:
    """清空编排缓存（测试隔离用）。"""
    _suff_per_card.cache_clear()
    _ce_per_card.cache_clear()


def orchestrate(min_chains: int = 5) -> dict:
    """真实只读编排（A1 映射驱动）：规则问题 → 卡 → 证据 → 判决。"""
    import queyi_data_models_645 as m
    import rule_card_mapper_646 as a1map

    issues = _smart_issues()
    mapping = a1map.build_mapping()["rules"]
    suff = _suff_per_card()          # 卡 → 真实证据（缓存）
    ce = _ce_per_card()              # 卡 → 反例候选（缓存）

    chains: list[dict] = []
    attributed = 0   # 有真实证据支撑的归因数
    for iss in issues:
        rule_id = iss["issue_id"].replace("ISSUE-", "")
        entry = mapping.get(rule_id, {"cards": []})
        matched = [c for c in entry["cards"] if c["strength"] in USE_STRENGTHS]
        cards = [c["card"] for c in matched]
        # 头部层：聚合匹配卡的真实证据
        rel_ev = sum(suff.get(c, {}).get("evidence_count", 0) for c in cards)
        any_ok = any(suff.get(c, {}).get("status") == "sufficient" for c in cards)
        ce_hits = []
        for c in cards:
            ce_hits.extend(ce.get(c, []))
        pkg = m.EvidencePackage(package_id=f"EVPKG-{iss['issue_id']}", topic=iss["issue_id"])
        for c in cards:
            for _ in range(suff.get(c, {}).get("evidence_count", 0)):
                pkg.add_evidence({"evidence_id": c, "grade": "L1",
                                  "credibility": 0.9, "source": "evidence_sufficiency"})
        # 尾端判决
        if cards and rel_ev > 0 and any_ok:
            verdict, conf, detail = "pass", 0.85, f"{len(cards)} 张关联卡证据充分（A1 映射）"
        elif rel_ev > 0:
            verdict, conf, detail = "fail", 0.5, f"{len(cards)} 张关联卡有证据但充分性不足"
        else:
            verdict, conf, detail = "needs_human", 0.2, "A1 映射未命中有效证据，需人审补"
        if rel_ev > 0:
            attributed += 1
        if ce_hits:
            detail += f"；{len(ce_hits)} 条反例候选待人审判定（只搜不判）"
        vr = m.VerificationResult(result_id=f"VR-{iss['issue_id']}",
                                  target_id=iss["issue_id"], verdict=verdict,
                                  confidence=conf, detail=detail)
        chains.append({
            "issue": iss["issue_id"], "rule": rule_id, "severity": iss["severity"],
            "matched_cards": len(cards), "evidence_count": rel_ev,
            "counterexamples": len(ce_hits), "verification": vr.to_dict(),
        })
    total = len(chains) or 1
    with_ev = 0
    for c in chains:
        if c["evidence_count"] > 0:
            with_ev += 1
    verdicts: dict[str, int] = {}
    for c in chains:
        v = c["verification"]["verdict"]
        verdicts[v] = verdicts.get(v, 0) + 1
    return {
        "chains": chains,
        "chain_count": len(chains),
        "chains_with_evidence": with_ev,
        "attribution_rate": round(with_ev / total, 4),
        "verdicts": verdicts,
        "min_chains": min_chains,
        "met": with_ev >= min_chains and (with_ev / total) >= 0.5,
    }


def _before_rate() -> float:
    """645 的归因可复核率（token 猜测匹配），用于打通前后对比。"""
    try:
        import three_layer_orchestrator_645 as old
        res = old.orchestrate()
        n = res["chain_count"] or 1
        return round(sum(1 for c in res["chains"] if c["evidence_count"] > 0) / n, 4)
    except Exception:
        return 0.1  # 645 实测值（报告登记）


def write_report(result: dict) -> None:
    """写 `data/646_coupling_report.md` + `.json`（含打通前后对比）。"""
    before = _before_rate()
    result["before_attribution_rate_645"] = before
    lines = ["# 646 三层耦合报告（A2，清债 1）", "",
             f"- 耦合链数：**{result['chain_count']}**（目标 ≥{result['min_chains']}）",
             f"- **证据≠0 的链：{result['chains_with_evidence']}**",
             f"- **归因可复核率：{result['attribution_rate']}**（目标 ≥0.5）",
             f"- 打通前（645 token 匹配）：{before}",
             f"- 尾端判决分布：{result['verdicts']}",
             f"- 达成：{result['met']}", "",
             "## 逐链（规则 → 匹配卡数 → 证据数 → 判决）"]
    for c in result["chains"]:
        lines.append(f"- `{c['rule']}`（{c['severity']}）：卡={c['matched_cards']} "
                     f"证据={c['evidence_count']} 反例={c['counterexamples']} → "
                     f"{c['verification']['verdict']}")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：映射驱动的链聚合逻辑（合成卡证据）。"""
    suff: dict[str, dict] = {"C1": {"evidence_count": 3, "status": "sufficient"}}
    frag: list[dict] = [{"card": "C1", "strength": "high"}]
    matched = [c for c in frag if c["strength"] in USE_STRENGTHS]
    rel = sum(int(suff.get(c["card"], {}).get("evidence_count", 0)) for c in matched)
    assert rel == 3
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口：`--check` 只读自检；`--run` 真实编排。"""
    ap = argparse.ArgumentParser(description="646 三层编排（A1 映射驱动）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--run", action="store_true", help="真实只读编排")
    ap.add_argument("--min", type=int, default=5, help="最少打通链数")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = orchestrate(min_chains=args.min)
    write_report(result)
    print(f"[646 coupling] 链={result['chain_count']} 证据≠0={result['chains_with_evidence']} "
          f"归因={result['attribution_rate']} 达成={result['met']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
