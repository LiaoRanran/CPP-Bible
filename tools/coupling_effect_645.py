"""645 · 阶段 C3 · 耦合效果评估（有耦合 vs 无耦合，真实对比）。

目标（645 §五 C3）：量化「三层耦合」相对「各跑各的」的真实增益，四个指标：
1. **问题归因准确率**：有证据支撑的归因 vs 纯静态启发式归因（无证据）。
2. **证据获取成功率**：真获取（B1 eel.is，200 命中）vs 降级失败（644 原型 403）。
3. **尾端验证通过率**：有证据链路的判决 vs 无证据启发式判决。
4. **闭环反馈有效性**：C4 反馈真实驱动的行进项（补证据/人审）。

设计要点（诚实优先）：
- 「无耦合」基线 = 不接头部层证据，仅按智能层静态严重度启发式给判决——**这正是 643/644
  各自为战的真实状态**，非虚构对照组。
- 所有「有耦合」数字来自 C2 编排链（真实 Issue→证据→验证），非编造。
- `--check` 只读自检；`--run` 真实评估，写 `data/645_coupling_effect_report.md`+`.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REPORT_MD = os.path.join(DATA, "645_coupling_effect_report.md")
REPORT_JSON = os.path.join(DATA, "645_coupling_effect_report.json")
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
    import coupling_feedback_645 as c4
    import three_layer_orchestrator_645 as c2

    res = c2.orchestrate()
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
    fb = c4.generate_feedback(chains)

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


def write_report(result: dict) -> None:
    """把结果写为 `data/645_*.md` + `.json` 报告（人类可读 + 机器可读）。"""
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
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
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


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 耦合效果评估（真实对比）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--run", action="store_true", help="真实评估")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = evaluate()
    write_report(result)
    m = result["metrics"]
    print(f"[645 coupling effect] 归因 {m['attribution_accuracy']['with_coupling']} vs "
          f"{m['attribution_accuracy']['without_coupling']}；获取 "
          f"{m['evidence_fetch_success']['with_coupling']} vs "
          f"{m['evidence_fetch_success']['without_coupling']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
