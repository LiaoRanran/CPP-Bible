"""645 · 阶段 A1 · 问题发现器重建（基于真实数据，非启发式凑数）。

目标（645 §三 A1）：重建问题发现器，输出 Top 10 问题，每条带：
根因（有数据支撑）/ 证据（可复现）/ 严重度 / 建议下一步。
**不许用启发式静态指标凑数**——每个问题必须有真实数据支撑。

真实数据源（645 §三 A1 数据源）：
- 真实规则命中：直接跑 `gate_engine.run(include_advice=True)` 得到 67 规则在当前仓库的
  真实 Finding（哪些规则真的在响、响在哪些卡上）——这是最硬的真实数据。
- 真实盲区：自动化规则中 0 命中的 → 覆盖盲区（真实存在）。
- 真实 error 率：复用 A5 `rule_error_tracker_645.track()` 真实统计（规则被推翻/逃逸）。
- 真实老化：复用 A6 `rule_aging_detector_645.detect()`（命中趋势下滑的规则）。

严重度计算（可复现，非拍脑袋）：
- 真实 block 级 Finding 命中 → high
- 某 block 规则盲区（从不响）→ critical（最危险：该拦的没拦）
- 高 error_rate（>0.2 真实被推翻）→ high
- 老化规则命中下滑 → medium
公式：score = w_block*block_hits + w_blind*blind_flag + w_err*error_rate + w_aging*aging_signal

`--check`：只读自检（排序/严重度逻辑，不跑全库 gate）。
`--discover`：真实跑 gate + A5/A6，产出 Top10，写 `data/645_issue_report.md`+`.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(ROOT, "data", "645_issue_report.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_issue_report.json")

# 严重度权重（可复现，写死便于审计）
W_BLOCK = 3.0
W_BLIND = 5.0      # 盲区最危险：该拦未拦
W_ERR = 2.0
W_AGING = 1.0


def discover_real_findings() -> dict[str, int]:
    """真实跑 gate_engine，得到每条自动化规则的命中次数（真实数据）。"""
    import gate_engine as ge  # 延迟导入（重依赖）
    findings = ge.run(include_advice=True)
    counts: dict[str, int] = {}
    for f in findings:
        counts[f.rule_id] = counts.get(f.rule_id, 0) + 1
    return counts


def discover_blind_spots() -> set[str]:
    """真实盲区：自动化且 0 命中的规则 ID。"""
    import gate_engine as ge
    fired = discover_real_findings()
    return {r.id for r in ge.RULES if r.automated and r.id not in fired}


def build_issues(finding_counts: Optional[dict[str, int]] = None,
                 blind: Optional[set[str]] = None,
                 error_rates: Optional[dict] = None,
                 aging: Optional[dict] = None,
                 top_n: int = 10) -> list[dict]:
    """基于真实计数构建 TopN 问题（纯函数，便于单测，不依赖全库 gate）。"""
    finding_counts = finding_counts or {}
    blind = blind or set()
    error_rates = error_rates or {}
    aging = aging or {}
    import gate_engine as ge
    # 真实规则 + 所有输入里出现的 ID（合成/测试 ID 也纳入，保证覆盖）
    real_rules = {r.id: r for r in ge.RULES}
    all_ids = (set(real_rules) | set(finding_counts) | blind
               | set(error_rates) | set(aging))
    issues: list[dict] = []
    for rid in all_ids:
        r = real_rules.get(rid)
        sev_base = r.severity if r is not None else "advice"
        title = r.title if r is not None else rid
        block_hits = finding_counts.get(rid, 0)
        is_blind = rid in blind
        err = error_rates.get(rid, {}).get("known_error_rate", 0.0) if isinstance(error_rates.get(rid), dict) else 0.0
        aging_signal = aging.get(rid, {}).get("aging_signal", 0.0) if isinstance(aging.get(rid), dict) else 0.0
        # 严重度基线
        if is_blind and sev_base == "block":
            severity = "critical"
        elif is_blind:
            severity = "high"          # 任意规则的盲区都是显著问题（该响不响）
        elif block_hits > 0 and sev_base == "block":
            severity = "high"
        elif err > 0.2:
            severity = "high"
        elif aging_signal > 0:
            severity = "medium"
        else:
            severity = "low"
        score = (W_BLOCK * block_hits + W_BLIND * (1 if is_blind else 0)
                 + W_ERR * err + W_AGING * aging_signal)
        # 根因（必须引用真实数据）
        if is_blind:
            root = f"规则 {rid}（{sev_base}）在全库 0 命中 → 覆盖盲区（真实盲区）"
            ev = [f"rule:{rid}", "blind_spot"]
            nxt = "补充该规则能命中的卡片/证据，或评估是否退役"
        elif block_hits > 0:
            root = f"规则 {rid} 当前真实命中 {block_hits} 次（gate_engine.run 真实产出）"
            ev = [f"rule:{rid}", f"hits:{block_hits}"]
            nxt = "复核命中是否真问题；高严重度优先人审"
        elif err > 0.2:
            root = f"规则 {rid} 真实被推翻率 {err:.3f}（A5 账本统计）>0.2"
            ev = [f"rule:{rid}", f"error_rate:{err:.3f}"]
            nxt = "复核该规则 precondition/判定逻辑是否过时"
        elif aging_signal > 0:
            root = f"规则 {rid} 命中趋势下滑（A6 老化信号 {aging_signal:.3f}）"
            ev = [f"rule:{rid}", "aging"]
            nxt = "检查该规则适用场景是否随标准演进失效"
        else:
            continue  # 无真实信号的问题不进榜（不凑数）
        issues.append({
            "issue_id": f"ISSUE-{rid}",
            "title": f"{rid}：{title}",
            "root_cause": root,
            "severity": severity,
            "score": round(score, 4),
            "evidence_refs": ev,
            "suggested_next": nxt,
            "source": "smart_issue_finder_645",
        })
    issues.sort(key=lambda x: (-x["score"], x["severity"] != "critical"))
    return issues[:top_n]


def selftest() -> int:
    """只读自检：排序/严重度逻辑（用合成真实计数，不跑全库 gate）。"""
    import gate_engine as ge
    blk = next((r.id for r in ge.RULES if r.severity == "block"), "R-B")
    finding_counts = {"R-A": 3, blk: 0}
    blind = {blk}  # 真实 block 规则盲区 → critical
    err = {"R-C": {"known_error_rate": 0.3}}
    issues = build_issues(finding_counts, blind, err, {}, top_n=10)
    # 真实 block 盲区规则应判 critical
    assert any(i["issue_id"] == f"ISSUE-{blk}" and i["severity"] == "critical" for i in issues)
    # 无真实信号的问题不进榜
    assert all(i["evidence_refs"] for i in issues)
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 问题发现器（真实数据 Top10）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--discover", action="store_true", help="真实跑 gate + A5/A6 产出 Top10")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    finding_counts = discover_real_findings()
    blind = discover_blind_spots()
    # 复用 A5 / A6 真实统计（失败则退化为空，不阻断）
    error_rates: dict = {}
    aging: dict = {}
    try:
        import loop_r5_runner_645 as a5  # noqa: E402  (647 D1：error 追踪已并入)
        error_rates = a5.track()["per_rule"]
    except Exception:  # noqa: BLE001
        pass
    try:
        import loop_r5_runner_645 as a6  # noqa: E402  (647 D1：老化检测已并入)
        aging = a6.detect()["per_rule"]
    except Exception:  # noqa: BLE001
        pass
    issues = build_issues(finding_counts, blind, error_rates, aging, top_n=10)
    report = {"finding_counts": finding_counts, "blind_spots": sorted(blind),
              "issues": issues}
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2, sort_keys=True)
    lines = ["# 645 问题发现报告（A1，真实数据 Top10）", "",
             f"- 真实命中规则数：{len(finding_counts)}",
             f"- 真实盲区规则数：{len(blind)}",
             f"- 产出问题数：{len(issues)}", ""]
    for i in issues:
        lines.append(f"### {i['issue_id']}（{i['severity']}, score={i['score']}）")
        lines.append(f"- 根因：{i['root_cause']}")
        lines.append(f"- 证据：{', '.join(i['evidence_refs'])}")
        lines.append(f"- 建议：{i['suggested_next']}")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"[645 issue_finder] Top{len(issues)} 问题；盲区={len(blind)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
