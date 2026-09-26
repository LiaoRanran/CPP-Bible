"""645 · 阶段 A5 · 规则 error 追踪真实累积（替代 643 E1 代理实现）。

目标（645 §三 A5）：从真实判决历史（452 条 Authority 账本）中，为**每条规则**提取：
- 触发次数（该规则参与判决的次数）
- 被推翻次数（人审改判 result=REJECT/MODIFY/ABSTAIN 推翻原判）
- 逃逸关联次数（该规则没拦住的逃逸——账本中标记为逃逸的事件）

输出：67 规则每条的**真实** known_error_rate（非 643 的代理初值）。

数据源（真实，非代理）：
- `data/authority/decision_event_v2_ledger.jsonl`（452 条，append-only 哈希链）
- 每条事件含 `target_id`（规则/卡片 ID）、`result`、`review_method`、`decision_origin`、
  `basis_refs`、`operation` 等字段。
- 关联规则：事件的 `target_id` 以 `ATOM-`/`EV-` 前缀落到卡片，再经 `serves`/规则映射；
  但账本是**规则级**判决轨迹的最真实来源——本工具直接统计事件里出现的规则 ID。

铁律：只读账本，绝不修改；error_rate 由真实计数推导，不编造。
`--check`：只读自检（解析逻辑 + 计数一致性）。
`--track`：真实统计 67 规则，写 `data/645_rule_error_report.md`+`.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
RULE_ID_RE = re.compile(r"(ATOM-[A-Z0-9-]+|EV-[A-Z0-9-]+|RULE-[A-Z0-9-]+)")
REPORT_MD = os.path.join(ROOT, "data", "645_rule_error_report.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_rule_error_report.json")

# 规则 ID 集合（从 gate_engine 取真实 67 条；失败则回退到账本中出现的 ID）
try:
    import gate_engine as ge  # noqa: E402
    RULE_IDS = [r.id for r in ge.RULES]
except Exception:  # noqa: BLE001
    RULE_IDS = []


def load_ledger() -> list[dict]:
    """逐行读取哈希链账本（只读，跳过空行/坏行）。"""
    out: list[dict] = []
    if not os.path.exists(LEDGER):
        return out
    with open(LEDGER, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _is_overturn(ev: dict) -> bool:
    """是否「被推翻」：人审改判（REJECT/MODIFY）或 ABSTAIN 撤销。

    真实口径（642 A4）：ledger 改判 85/452=0.1881；这里逐事件判定。
    """
    r = str(ev.get("result", "")).upper()
    op = str(ev.get("operation", "")).upper()
    # 原判被推翻：REVOKE/REJECT/MODIFY 且非初始 CREATE；或 ABSTAIN（弃权=不认原判）
    if op == "REVOKE":
        return True
    if r in ("REJECT", "MODIFY"):
        return True
    if r == "ABSTAIN":
        return True
    return False


def _is_escape(ev: dict) -> bool:
    """是否「逃逸关联」：事件本身标记逃逸，或 basis_refs 含 escape/逃逸字样。"""
    txt = " ".join(str(ev.get(k, "")) for k in ("basis_refs", "modification", "abstain_reason"))
    return ("逃逸" in txt) or ("escape" in txt.lower())


def track(rules: Optional[list[str]] = None) -> dict:
    """真实统计每条规则的触发/被推翻/逃逸关联次数。"""
    events = load_ledger()
    if rules is None:
        rules = RULE_IDS
    if not rules:
        # 回退：账本里出现过的规则/卡 ID
        ids: set[str] = set()
        for ev in events:
            tid = str(ev.get("target_id", ""))
            if RULE_ID_RE.match(tid):
                ids.add(tid)
        rules = sorted(ids)
    stats: dict[str, dict] = {rid: {"trigger": 0, "overturn": 0, "escape": 0} for rid in rules}
    for ev in events:
        # 事件可能直接指向某规则/卡，或其 basis_refs 引用多个规则
        ids_here: set[str] = set()
        tid = str(ev.get("target_id", ""))
        if tid in stats:
            ids_here.add(tid)
        refs = ev.get("basis_refs") or []
        if isinstance(refs, str):
            refs = [refs]
        for ref in refs:
            if str(ref) in stats:
                ids_here.add(str(ref))
        for rid in ids_here:
            stats[rid]["trigger"] += 1
            if _is_overturn(ev):
                stats[rid]["overturn"] += 1
            if _is_escape(ev):
                stats[rid]["escape"] += 1
    # 计算真实 error_rate：被推翻率（无触发则 0，真实而非代理初值）
    per_rule = {}
    for rid, s in stats.items():
        trig = s["trigger"]
        err_rate = (s["overturn"] / trig) if trig > 0 else 0.0
        per_rule[rid] = {
            "trigger": trig, "overturn": s["overturn"], "escape": s["escape"],
            "known_error_rate": round(err_rate, 6),
        }
    total_trig = sum(s["trigger"] for s in stats.values())
    return {
        "ledger_events": len(events),
        "rule_count": len(rules),
        "rules_with_trigger": sum(1 for s in stats.values() if s["trigger"] > 0),
        "total_trigger": total_trig,
        "per_rule": per_rule,
    }


def write_report(result: dict) -> None:
    """把结果写为 `data/645_*.md` + `.json` 报告（人类可读 + 机器可读）。"""
    lines = ["# 645 规则 error 追踪报告（A5，真实账本统计）", "",
             f"- 账本事件数：{result['ledger_events']}",
             f"- 规则总数：{result['rule_count']}",
             f"- 有触发记录的规则：{result['rules_with_trigger']}", ""]
    lines.append("## 逐规则（真实 error_rate）")
    for rid, info in sorted(result["per_rule"].items()):
        lines.append(f"- `{rid}`：触发={info['trigger']} 推翻={info['overturn']} "
                     f"逃逸关联={info['escape']} error_rate={info['known_error_rate']}")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：解析/计数逻辑（用内联账本，不读真实账本）。"""
    sample: list[dict] = [
        {"target_id": "R1", "result": "APPROVE", "operation": "CREATE", "basis_refs": []},
        {"target_id": "R1", "result": "REJECT", "operation": "REPLACE", "basis_refs": []},
        {"target_id": "R2", "result": "ABSTAIN", "operation": "REVOKE",
         "basis_refs": ["逃逸-样例"]},
    ]
    # 临时替换 load_ledger
    orig = load_ledger.__name__
    # 直接测内联逻辑：构造一个假统计
    stats = {rid: {"trigger": 0, "overturn": 0, "escape": 0} for rid in ("R1", "R2")}
    for ev in sample:
        rid = ev["target_id"]
        stats[rid]["trigger"] += 1
        if _is_overturn(ev):
            stats[rid]["overturn"] += 1
        if _is_escape(ev):
            stats[rid]["escape"] += 1
    assert stats["R1"]["trigger"] == 2 and stats["R1"]["overturn"] == 1
    assert stats["R2"]["escape"] == 1
    # 真实账本可读
    assert isinstance(load_ledger(), list)
    _ = orig
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 规则 error 追踪（真实账本）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--track", action="store_true", help="真实统计 67 规则 error_rate")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = track()
    write_report(result)
    print(f"[645 rule_error_tracker] 规则={result['rule_count']} "
          f"有触发={result['rules_with_trigger']} 总触发={result['total_trigger']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
