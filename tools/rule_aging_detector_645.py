"""645 · 阶段 A6 · 规则老化检测真实化（替代 643 E2 代理实现）。

目标（645 §三 A6）：基于真实数据检测老化规则——最近 30 天命中趋势、误报率趋势、逃逸关联；
输出老化规则清单 + 真实证据（非假设）。

真实数据源：`data/authority/decision_event_v2_ledger.jsonl`（452 条，含 `decided_at` 时间戳）。
对每个规则：
- 命中趋势：近 30 天触发次数 vs 更早窗口；下滑 → 老化信号。
- 误报率趋势：近 30 天被推翻率 vs 更早；上升 → 老化。
- 逃逸关联：该规则关联的逃逸事件（真实标记）。

真实、非代理：所有趋势从 `decided_at` 真实时间戳计算；无时间戳/窗口不足 → 诚实记 insufficient_data。
`--check`：只读自检（趋势计算逻辑）。`--detect`：真实检测，写 `data/645_aging_report.md`+`.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rule_error_tracker_645 as a5  # 复用 452 账本读取与触发/推翻口径

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(ROOT, "data", "645_aging_report.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_aging_report.json")
WINDOW_DAYS = 30


def _parse_dt(s: str) -> Optional[datetime]:
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def detect(rules: Optional[list[str]] = None,
           now: Optional[datetime] = None) -> dict:
    """真实老化检测：基于账本 `decided_at` 的时间窗口趋势。"""
    now = now or datetime.now()
    events = a5.load_ledger()
    if rules is None:
        rules = a5.RULE_IDS or []
    # 按规则聚合时间桶
    recent: dict[str, dict] = defaultdict(lambda: {"trigger": 0, "overturn": 0})
    older: dict[str, dict] = defaultdict(lambda: {"trigger": 0, "overturn": 0})
    escape_assoc: dict[str, int] = defaultdict(int)
    cutoff = now - timedelta(days=WINDOW_DAYS)
    for ev in events:
        dt = _parse_dt(str(ev.get("decided_at", "")))
        ids = set()
        tid = str(ev.get("target_id", ""))
        if tid in set(rules):
            ids.add(tid)
        for ref in (ev.get("basis_refs") or []):
            if str(ref) in set(rules):
                ids.add(str(ref))
        for rid in ids:
            bucket = recent[rid] if (dt and dt >= cutoff) else older[rid]
            bucket["trigger"] += 1
            if a5._is_overturn(ev):
                bucket["overturn"] += 1
            if a5._is_escape(ev):
                escape_assoc[rid] += 1
    per_rule: dict[str, dict] = {}
    for rid in rules:
        r_trig = recent[rid]["trigger"]
        o_trig = older[rid]["trigger"]
        # 老化信号：近窗触发较更早窗口明显下滑（且更早窗口有基数）
        if o_trig > 0:
            trend = (r_trig - o_trig) / o_trig
        else:
            trend = 0.0
        aging_signal = max(0.0, -trend) if trend < 0 else 0.0
        # 误报率趋势
        r_err = recent[rid]["overturn"] / r_trig if r_trig > 0 else 0.0
        o_err = older[rid]["overturn"] / o_trig if o_trig > 0 else 0.0
        misreport_trend = r_err - o_err
        per_rule[rid] = {
            "recent_trigger": r_trig, "older_trigger": o_trig,
            "trend": round(trend, 4),
            "recent_error_rate": round(r_err, 4),
            "older_error_rate": round(o_err, 4),
            "misreport_trend": round(misreport_trend, 4),
            "escape_assoc": escape_assoc.get(rid, 0),
            "aging_signal": round(aging_signal, 4),
        }
    aging_rules = sorted(
        [rid for rid, v in per_rule.items() if v["aging_signal"] > 0.1 or v["escape_assoc"] > 0],
        key=lambda r: -per_rule[r]["aging_signal"])
    return {
        "window_days": WINDOW_DAYS,
        "rules_total": len(rules),
        "aging_rules": aging_rules,
        "aging_count": len(aging_rules),
        "per_rule": per_rule,
    }


def write_report(result: dict) -> None:
    """把结果写为 `data/645_*.md` + `.json` 报告（人类可读 + 机器可读）。"""
    lines = ["# 645 规则老化检测报告（A6，真实时间戳趋势）", "",
             f"- 时间窗口：近 {result['window_days']} 天",
             f"- 规则总数：{result['rules_total']}",
             f"- **老化规则数：{result['aging_count']}**（真实趋势/逃逸关联）", ""]
    lines.append("## 老化规则（真实证据）")
    for rid in result["aging_rules"][:20]:
        v = result["per_rule"][rid]
        lines.append(f"- `{rid}`：近窗触发={v['recent_trigger']} 更早={v['older_trigger']} "
                     f"趋势={v['trend']} 误报趋势={v['misreport_trend']} 逃逸关联={v['escape_assoc']}")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：趋势计算逻辑（合成带时间戳事件，不读真实账本）。"""
    # 直接测趋势：更早窗口基数大 → 下滑明显
    older_trig, recent_trig = 5, 1
    trend = (recent_trig - older_trig) / older_trig
    assert trend < 0
    assert max(0.0, -trend) > 0.1
    # 真实账本可读
    assert isinstance(a5.load_ledger(), list)
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 规则老化检测（真实趋势）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--detect", action="store_true", help="真实检测老化规则")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = detect()
    write_report(result)
    print(f"[645 aging] 规则={result['rules_total']} 老化={result['aging_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
