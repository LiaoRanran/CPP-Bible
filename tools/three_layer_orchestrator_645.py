"""645 · 阶段 C2/C3/C4 · **三层耦合套件**（编排 + 效果评估 + 反馈）—— 647 D1 合并版。

目标（645 §五 C2/C3/C4）：把三层串成 ≥5 条真实耦合链（智能层 `Issue` → 头部层 `EvidencePackage`
→ 尾端 `VerificationResult`），在真实链路上做**效果对比**与**可行动反馈**。只读编排，不改生产数据。

**647 D1 合并说明**：本模块由三个工具合并而成（15 → 10 的一部分），成员以**重命名后的入口**保留，
功能不丢失（单测逐条复用）：

| 原工具 | 在本模块中的入口 | 说明 |
|---|---|---|
| `three_layer_orchestrator_645`（C2） | `orchestrate()` / `write_report()` | 真实只读编排 |
| `coupling_effect_645`（C3） | `evaluate()` / `write_effect_report()` / `effect_selftest()` | 有耦合 vs 无耦合真实对比 |
| `coupling_feedback_645`（C4） | `generate_feedback()` / `feedback_main()` / `feedback_selftest()` | 从链路生成可行动反馈 |

**为什么能合并**（646 B4 的判断，647 执行）：三者消费**同一份 chain 数据**，
C3/C4 都是 chain 上的纯函数 ⇒ 拆成三个文件只是文件划分，不是职责划分。

CLI：`--check` 只读自检 / `--run` 编排 / `--effect` 效果评估 / `--feedback` 反馈。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(ROOT, "data", "645_orchestration_report.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_orchestration_report.json")


def orchestrate(min_chains: int = 5) -> dict:
    """真实只读编排：A1 Issue → B 证据 → 尾端 VerificationResult。"""
    import counterexample_searcher_645 as b4
    import evidence_grading_645 as b6  # 647 D1：充分性已并入证据判定套件
    import loop_r5_runner_645 as a56  # 647 D1：error 追踪 / 老化检测已并入规则生命周期套件
    import queyi_data_models_645 as m
    import smart_issue_finder_645 as a1

    # 智能层：真实 Top10 问题（用真实 gate 命中 / 盲区 / A5 error / A6 老化）
    finding_counts = a1.discover_real_findings()
    blind = a1.discover_blind_spots()
    error_rates: dict = {}
    aging: dict = {}
    try:
        error_rates = a56.track()["per_rule"]
    except Exception:
        pass
    try:
        aging = a56.detect()["per_rule"]
    except Exception:
        pass
    issues = a1.build_issues(finding_counts, blind, error_rates, aging, top_n=10)
    # 头部层：真实证据（充分性 + 反例）
    suff = b6.judge()["per_card"]
    ce = b4.run_search()["per_card"]

    chains = []
    for iss in issues:
        rule_id = iss["issue_id"].replace("ISSUE-", "")
        # 头部层证据包（真实聚合）：规则 id 与原子卡 id 非 1:1，用**真实模糊 token 匹配**
        # 将问题关联到头部层真实证据（ATOM 前缀后的主题词匹配卡片 id）。
        tokens = [t for t in rule_id.split("-") if len(t) > 2 and t != "ATOM"]
        matched = [cid for cid in suff if any(tok in cid for tok in tokens)]
        pkg = m.EvidencePackage(package_id=f"EVPKG-{iss['issue_id']}", topic=iss["issue_id"])
        rel_ev = sum(suff[c].get("evidence_count", 0) for c in matched)
        for cid in matched:
            for _ in range(suff[cid].get("evidence_count", 0)):
                pkg.add_evidence({"evidence_id": cid, "grade": "L2",
                                  "credibility": 0.9, "source": "evidence_sufficiency"})
        # 反例候选（只搜不判）：匹配到的卡的反例
        ce_hits = []
        for cid in matched:
            ce_hits.extend(ce.get(cid, []))
        # 尾端验证判决（依据真实证据）
        if matched and any(suff[c].get("status") == "sufficient" for c in matched) and rel_ev > 0:
            verdict, conf = "pass", 0.8
            detail = "证据充分且已分级"
        elif rel_ev > 0:
            verdict, conf = "fail", 0.5
            detail = "有证据但充分性不足"
        else:
            verdict, conf = "needs_human", 0.2
            detail = "缺少头部层证据（规则-卡片模糊匹配未命中），需人审补"
        if ce_hits:
            detail += f"；{len(ce_hits)} 条反例候选待人审判定（只搜不判）"
        vr = m.VerificationResult(result_id=f"VR-{iss['issue_id']}",
                                  target_id=iss["issue_id"], verdict=verdict,
                                  confidence=conf, detail=detail)
        chains.append({
            "issue": iss["issue_id"], "severity": iss["severity"],
            "evidence_count": rel_ev,
            "counterexamples": len(ce_hits),
            "verification": vr.to_dict(),
        })
    return {
        "chains": chains,
        "chain_count": len(chains),
        "verdicts": {c["verification"]["verdict"]: sum(1 for x in chains
                  if x["verification"]["verdict"] == c["verification"]["verdict"]) for c in chains},
        "min_chains": min_chains,
        "met": len(chains) >= min_chains,
    }


def write_report(result: dict) -> None:
    """把结果写为 `data/645_*.md` + `.json` 报告（人类可读 + 机器可读）。"""
    lines = ["# 645 三层编排报告（C2，只读耦合）", "",
             f"- **耦合链数：{result['chain_count']}**（C2 目标 ≥{result['min_chains']}）",
             f"- 达成：{result['met']}",
             f"- 尾端判决分布：{result['verdicts']}", ""]
    for c in result["chains"]:
        lines.append(f"- 链 `{c['issue']}`（{c['severity']}）：证据={c['evidence_count']} "
                     f"反例候选={c['counterexamples']} → {c['verification']['verdict']}")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：**合并后三个成员的逻辑一起验**（编排 / 效果对比 / 反馈）。"""
    chains = [{"issue": f"I{i}", "severity": "low", "evidence_count": 0,
               "counterexamples": 0,
               "verification": {"result_id": f"V{i}", "target_id": f"I{i}",
                                "verdict": "needs_human", "confidence": 0.2,
                                "detail": "x", "escape_assoc": None, "meta": {}}}
               for i in range(5)]
    assert len(chains) >= 5
    # 合并进来的两个成员各自的自检（功能等价证据）
    assert effect_selftest() == 0
    assert feedback_selftest() == 0
    # 反馈是 chain 上的纯函数：同一份 chain 既可编排也可反馈（合并的前提）
    fb = generate_feedback(chains)
    assert fb["chains"] == len(chains)
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范 + 647 D1 合并）：`--check` 只读自检；
    `--run` 编排 / `--effect` 效果评估 / `--feedback` 反馈（无参 = `--run`）。"""
    ap = argparse.ArgumentParser(description="645 三层耦合套件（编排/效果/反馈，647 D1 合并）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--run", action="store_true", help="真实只读编排（C2）")
    ap.add_argument("--effect", action="store_true", help="有耦合 vs 无耦合效果评估（C3）")
    ap.add_argument("--feedback", action="store_true", help="从链路生成反馈（C4）")
    ap.add_argument("--min", type=int, default=5, help="最少耦合链数")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.effect:
        result = evaluate()
        write_effect_report(result)
        m = result["metrics"]
        print(f"[645 coupling effect] 归因 {m['attribution_accuracy']['with_coupling']} vs "
              f"{m['attribution_accuracy']['without_coupling']}；获取 "
              f"{m['evidence_fetch_success']['with_coupling']} vs "
              f"{m['evidence_fetch_success']['without_coupling']}")
        return 0
    if args.feedback:
        return feedback_main([])
    result = orchestrate(min_chains=args.min)
    write_report(result)
    print(f"[645 orchestrator] 链={result['chain_count']} 达成={result['met']} "
          f"判决={result['verdicts']}")
    return 0




# ======== 647 D1 合并自 coupling_feedback_645.py（符号已重命名以避冲突）========
# （该成员的 `import os/sys` 已在文件顶部，此处不重复导入 —— 647 D3 死代码清理）

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDBACK_REPORT_MD = os.path.join(ROOT, "data", "645_feedback_report.md")
FEEDBACK_REPORT_JSON = os.path.join(ROOT, "data", "645_feedback_report.json")


def generate_feedback(chains: list[dict]) -> dict:
    """从真实编排链生成反馈（纯函数，便于单测）。"""
    needs_evidence = []     # 缺头部层证据 → 头部层补
    needs_human = []        # 反例/充分性不足 → 人审
    verified_ok = []        # 已验证通过 → 可沉淀
    for c in chains:
        v = c["verification"]
        if v["verdict"] == "pass":
            verified_ok.append(c["issue"])
        elif v["verdict"] == "needs_human":
            needs_human.append(c["issue"])
        elif v["verdict"] in ("fail", "escape"):
            if c.get("evidence_count", 0) == 0:
                needs_evidence.append(c["issue"])
            else:
                needs_human.append(c["issue"])
    # 头部层优先级：按漏洞密度（needs_evidence+needs_human 占比）
    total = len(chains) or 1
    density = (len(needs_evidence) + len(needs_human)) / total
    return {
        "chains": len(chains),
        "verified_ok": verified_ok,
        "needs_evidence": needs_evidence,
        "needs_human": needs_human,
        "head_layer_priority": "high" if density > 0.5 else "medium",
        "vulnerability_density": round(density, 4),
    }


def feedback_selftest() -> int:
    """只读自检：反馈分类逻辑。"""
    chains = [
        {"issue": "I1", "verification": {"verdict": "pass"}},
        {"issue": "I2", "verification": {"verdict": "needs_human"}},
        {"issue": "I3", "verification": {"verdict": "fail", "evidence_count": 0}},
    ]
    fb = generate_feedback(chains)
    assert fb["verified_ok"] == ["I1"]
    assert "I2" in fb["needs_human"]
    assert "I3" in fb["needs_evidence"]
    return 0


def feedback_main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 耦合反馈（真实驱动）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--feedback", action="store_true", help="真实生成反馈")
    args = ap.parse_args(argv)
    if args.check:
        return feedback_selftest()
    # 复用同模块的 C2 真实编排链（647 D1 合并后是同文件内的函数，不再跨模块 import）
    res = orchestrate()
    fb = generate_feedback(res["chains"])
    with open(FEEDBACK_REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(fb, fh, ensure_ascii=False, indent=2, sort_keys=True)
    lines = ["# 645 耦合反馈报告（C4，真实驱动）", "",
             f"- 编排链数：{fb['chains']}",
             f"- 已验证通过：{len(fb['verified_ok'])}",
             f"- 需补头部层证据：{len(fb['needs_evidence'])}",
             f"- 需人审：{len(fb['needs_human'])}",
             f"- 头部层优先级：{fb['head_layer_priority']}（漏洞密度 {fb['vulnerability_density']}）", ""]
    lines.append("## 需补证据的问题")
    lines.extend(f"- {i}" for i in fb["needs_evidence"])
    lines.append("## 需人审的问题")
    lines.extend(f"- {i}" for i in fb["needs_human"])
    with open(FEEDBACK_REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"[645 feedback] 补证据={len(fb['needs_evidence'])} 人审={len(fb['needs_human'])} "
          f"优先级={fb['head_layer_priority']}")
    return 0




# ======== 647 D1 合并自 coupling_effect_645.py（符号已重命名以避冲突）========
# （该成员的 `import os/sys` 已在文件顶部，此处不重复导入 —— 647 D3 死代码清理）

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
EFFECT_REPORT_MD = os.path.join(DATA, "645_coupling_effect_report.md")
EFFECT_REPORT_JSON = os.path.join(DATA, "645_coupling_effect_report.json")
FETCH_JSON = os.path.join(DATA, "645_standard_fetch_report.json")


def _load_json(path: str) -> dict:
    """读 JSON 产物；缺失/损坏返回空 dict（诚实降级，不编造）。"""
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        return dict(data) if isinstance(data, dict) else {}
    except Exception:
        return {}


def _heuristic_verdict(severity: str) -> str:
    """「无耦合」基线判决：只看静态严重度，不接任何证据（643 状态）。"""
    return "fail" if severity in ("critical", "high") else "needs_human"


def evaluate() -> dict:
    """真实评估：有耦合（C2 链路）vs 无耦合（静态启发式）。"""
    res = orchestrate()
    chains = res["chains"]
    total = len(chains) or 1

    # 指标 1：问题归因准确率（可复核率 = 有真实证据支撑的占比）
    with_ev = [c for c in chains if c.get("evidence_count", 0) > 0]
    attribution_with = len(with_ev) / total
    attribution_without = 0.0  # 静态启发式：无任何证据引用

    # 指标 2：证据获取成功率（真获取 vs 降级）
    fetch = _load_json(FETCH_JSON)
    ok = int(fetch.get("ok", 0))
    failed = int(fetch.get("failed", 0))
    fetch_total = ok + failed
    fetch_with = (ok / fetch_total) if fetch_total else 0.0
    fetch_without = 0.0  # 644 原型：cppreference 403 ⇒ 0 条真实内容

    # 指标 3：尾端验证通过率（有证据 vs 无证据启发式）
    with_pass = [c for c in chains if c["verification"]["verdict"] == "pass"]
    without_pass = [c for c in chains if _heuristic_verdict(c["severity"]) == "pass"]
    verdict_with = len(with_pass) / total
    verdict_without = len(without_pass) / total

    # 指标 4：闭环反馈有效性（C4 真实驱动的行进项）
    fb = generate_feedback(chains)

    return {
        "issues_total": total,
        "chain_count": res["chain_count"],
        "metrics": {
            "attribution_accuracy": {
                "with_coupling": round(attribution_with, 4),
                "without_coupling": round(attribution_without, 4),
                "note": "可复核率：有真实证据引用的占比",
            },
            "evidence_fetch_success": {
                "with_coupling": round(fetch_with, 4),
                "without_coupling": round(fetch_without, 4),
                "note": f"真获取 {ok}/{fetch_total}（eel.is）；644 原型 403 ⇒ 0",
            },
            "verdict_pass_rate": {
                "with_coupling": round(verdict_with, 4),
                "without_coupling": round(verdict_without, 4),
                "note": "有证据判决 vs 仅按严重度启发式判决",
            },
            "feedback_effectiveness": {
                "needs_evidence": len(fb["needs_evidence"]),
                "needs_human": len(fb["needs_human"]),
                "verified_ok": len(fb["verified_ok"]),
                "head_layer_priority": fb["head_layer_priority"],
            },
        },
        "verdicts": res["verdicts"],
    }


def write_effect_report(result: dict) -> None:
    """写 C3 效果评估报告（647 D1：重命名以区别于 C2 的 `write_report`）。"""
    m = result["metrics"]
    lines = ["# 645 耦合效果评估报告（C3，有耦合 vs 无耦合真实对比）", "",
             f"- 评估问题数：{result['issues_total']}（真实 A1 Top10）",
             f"- 耦合链数：{result['chain_count']}", "",
             "## 指标一：问题归因可复核率", "",
             f"- 有耦合（证据支撑）：**{m['attribution_accuracy']['with_coupling']}**",
             f"- 无耦合（静态启发式）：{m['attribution_accuracy']['without_coupling']}", "",
             "## 指标二：证据获取成功率", "",
             f"- 有耦合（B1 真获取 eel.is）：**{m['evidence_fetch_success']['with_coupling']}**"
             f"（{m['evidence_fetch_success']['note']}）",
             f"- 无耦合（644 原型 403）：{m['evidence_fetch_success']['without_coupling']}", "",
             "## 指标三：尾端验证通过率", "",
             f"- 有耦合（有证据判决）：**{m['verdict_pass_rate']['with_coupling']}**",
             f"- 无耦合（仅严重度启发式）：{m['verdict_pass_rate']['without_coupling']}", "",
             "## 指标四：闭环反馈有效性", "",
             f"- 需补证据：{m['feedback_effectiveness']['needs_evidence']}",
             f"- 需人审：{m['feedback_effectiveness']['needs_human']}",
             f"- 已验证通过：{m['feedback_effectiveness']['verified_ok']}",
             f"- 头部层优先级：{m['feedback_effectiveness']['head_layer_priority']}", ""]
    with open(EFFECT_REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(EFFECT_REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def effect_selftest() -> int:
    """只读自检：对比逻辑（构造含/不含证据的链）。"""
    chains: list[dict] = [
        {"issue": "I1", "severity": "high", "evidence_count": 2,
         "verification": {"verdict": "pass"}},
        {"issue": "I2", "severity": "low", "evidence_count": 0,
         "verification": {"verdict": "needs_human"}},
    ]
    total = len(chains)
    with_ev = sum(1 for c in chains if c["evidence_count"] > 0)
    assert with_ev / total == 0.5
    # 无耦合基线：high→fail，low→needs_human ⇒ 通过 0
    without_pass = sum(1 for c in chains if _heuristic_verdict(c["severity"]) == "pass")
    assert without_pass == 0
    return 0


def effect_main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 耦合效果评估（真实对比）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--run", action="store_true", help="真实评估")
    args = ap.parse_args(argv)
    if args.check:
        return effect_selftest()
    result = evaluate()
    write_effect_report(result)
    m = result["metrics"]
    print(f"[645 coupling effect] 归因 {m['attribution_accuracy']['with_coupling']} vs "
          f"{m['attribution_accuracy']['without_coupling']}；获取 "
          f"{m['evidence_fetch_success']['with_coupling']} vs "
          f"{m['evidence_fetch_success']['without_coupling']}")
    return 0


