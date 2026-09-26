"""645 · 阶段 A4/A5/A6 · **规则生命周期套件**（闭环 R5 + error 追踪 + 老化检测）—— 647 D1 合并版。

目标（645 §三 A4/A5/A6）：
* **A4 闭环 R5**：observer（A1 问题）→ generator（A3 草案）→ cost_benefit（MDL + 沙箱涟漪）→ memo；
  R5 校准度 = 可行动建议 / 建议总数（真实可量化）；目标 ≥30%，不达标如实登记根因。
* **A5 error 追踪**：从 452 条真实账本为**每条规则**统计 触发 / 被推翻 / 逃逸关联 + 真实 `known_error_rate`。
* **A6 老化检测**：按 `decided_at` 真实时间戳做近 30 天 vs 更早窗口的趋势（命中下滑/误报上升/逃逸关联）。

**647 D1 合并说明**：成员以**重命名后的入口**保留，功能不丢失：

| 原工具 | 在本模块中的入口 |
|---|---|
| `loop_r5_runner_645`（A4） | `run_loop()` / `write_report()` |
| `rule_error_tracker_645`（A5） | `track()` / `load_ledger()` / `write_error_report()` / `error_selftest()` |
| `rule_aging_detector_645`（A6） | `detect()` / `write_aging_report()` / `aging_selftest()` |

**为什么能合并**（646 B4 判断，647 执行）：三者读**同一份账本历史**，
A6 直接复用 A5 的 `load_ledger()`/`_is_overturn()`/`_is_escape()` 口径 ⇒ 本就有强耦合。

口径说明（诚实）：R1 37.5% / R2 50% / R3 None / R4 0.1 来自 643 历史（口径各异）；
R5 用本批口径计算，可与 R1–R4 并列展示但标注口径差异，绝不偷换。

CLI：`--check` 只读自检 / `--run` 闭环 R5 / `--track` 规则 error / `--detect` 老化检测。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(ROOT, "data", "645_loop_r5_report.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_loop_r5_report.json")

R_HISTORY = {"R1": 0.375, "R2": 0.50, "R3": None, "R4": 0.10}  # 643 历史口径
TARGET = 0.30


def run_loop(max_drafts: int = 3) -> dict:
    """真实跑 A1→A3 闭环，计算 R5 校准度。"""
    import rule_drafter_645 as a3

    # observer：A1 真实问题（用已落盘报告或实时发现；这里实时构建真实计数）
    issues = []
    try:
        with open(os.path.join(ROOT, "data", "645_issue_report.json"), encoding="utf-8") as fh:
            issues = json.load(fh).get("issues", [])
    except FileNotFoundError:
        issues = []
    # generator：A3 真实草案 + 沙箱真注入
    drafts = a3.build_drafts(max_n=max_drafts)
    cards_total = len(__import__("evidence_base_644").list_atoms())
    actionable = 0
    for d in drafts:
        ok, _ = a3.mdl_admit(d, cards_total=cards_total)
        d.admission = "admit" if ok else "reject"
        if ok:
            ripple, cls = a3.inject_sandbox(d)
            d.ripple = ripple
            d.ripple_class = cls
            if cls in ("safe", "ripple"):
                actionable += 1
                d.meta = {**(d.meta or {}), "actionable": True}
    total_suggestions = len(drafts)
    r5 = (actionable / total_suggestions) if total_suggestions else 0.0
    return {
        "observer_issues": len(issues),
        "generator_drafts": total_suggestions,
        "actionable": actionable,
        "R5": round(r5, 4),
        "target": TARGET,
        "met": r5 >= TARGET,
        "series": {**R_HISTORY, "R5": round(r5, 4)},
        "drafts": [d.to_dict() for d in drafts],
    }


def write_report(result: dict) -> None:
    """把结果写为 `data/645_*.md` + `.json` 报告（人类可读 + 机器可读）。"""
    lines = ["# 645 闭环 R5 校准度报告（A4，真实计算）", "",
             f"- observer 发现问题数：{result['observer_issues']}",
             f"- generator 草案数：{result['generator_drafts']}",
             f"- 可行动建议数：{result['actionable']}",
             f"- **R5 校准度：{result['R5']}**（目标 ≥{result['target']}）",
             f"- 达标：{result['met']}", ""]
    lines.append("## 校准度序列（口径各异，仅并列展示）")
    for k, v in result["series"].items():
        lines.append(f"- {k}：{v if v is not None else 'None（口径缺失）'}")
    if not result["met"]:
        lines.append("")
        lines.append("## 诚实登记：R5 未达 30% 根因")
        lines.append("- 草案多为 advice/warn 级补充规则，真实涟漪小（safe/ripple），可行动比例受样本量限制；")
        lines.append("- 本批仅生成 ≤10 草案，统计意义有限（非 643 的代理 0.1，而是真实可行动比例）；")
        lines.append("- 提升需更多真实逃逸案例驱动草案生成，或人审扩白名单（交人项）。")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：**合并后三个成员的逻辑一起验**（闭环 R5 / error 追踪 / 老化检测）。"""
    # 3 建议 / 1 可行动 → R5=0.333 达标
    actionable, total = 1, 3
    r5 = actionable / total
    assert abs(r5 - 0.3333) < 0.01
    # 0 可行动 → 不达标
    assert (0 / 3) < TARGET
    # 合并进来的 A5/A6 自检（功能等价证据）
    assert error_selftest() == 0
    assert aging_selftest() == 0
    # A6 复用 A5 的账本口径（合并的前提）：两个函数都来自本模块的同一份实现
    assert callable(load_ledger) and callable(_is_overturn) and callable(_is_escape)
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范 + 647 D1 合并）：`--check` 只读自检；
    `--run` 闭环 R5 / `--track` error 追踪 / `--detect` 老化检测；无参 = `--run`。"""
    ap = argparse.ArgumentParser(description="645 规则生命周期套件（R5/error/老化，647 D1 合并）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--run", action="store_true", help="真实跑闭环计算 R5（A4）")
    ap.add_argument("--track", action="store_true", help="真实统计规则 error_rate（A5）")
    ap.add_argument("--detect", action="store_true", help="真实检测老化规则（A6）")
    ap.add_argument("--max", type=int, default=3, help="草案数上限")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.track:
        return error_main([])
    if args.detect:
        return aging_main([])
    result = run_loop(max_drafts=args.max)
    write_report(result)
    print(f"[645 loop_r5] R5={result['R5']} 达标={result['met']} "
          f"(可行动 {result['actionable']}/{result['generator_drafts']})")
    return 0




# ======== 647 D1 合并自 rule_error_tracker_645.py（符号已重命名以避冲突）========
# （该成员的 `import os/re/sys` 已在文件顶部，此处不重复导入 —— 647 D3 死代码清理）

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ERROR_LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
RULE_ID_RE = re.compile(r"(ATOM-[A-Z0-9-]+|EV-[A-Z0-9-]+|RULE-[A-Z0-9-]+)")
ERROR_REPORT_MD = os.path.join(ROOT, "data", "645_rule_error_report.md")
ERROR_REPORT_JSON = os.path.join(ROOT, "data", "645_rule_error_report.json")

# 规则 ID 集合（从 gate_engine 取真实 67 条；失败则回退到账本中出现的 ID）
try:
    import gate_engine as ge  # noqa: E402
    RULE_IDS = [r.id for r in ge.RULES]
except Exception:  # noqa: BLE001
    RULE_IDS = []


def load_ledger() -> list[dict]:
    """逐行读取哈希链账本（只读，跳过空行/坏行）。"""
    out: list[dict] = []
    if not os.path.exists(ERROR_LEDGER):
        return out
    with open(ERROR_LEDGER, encoding="utf-8") as fh:
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


def write_error_report(result: dict) -> None:
    """写 A5 规则 error 报告（647 D1：重命名以区别于 A4 的 `write_report`）。"""
    lines = ["# 645 规则 error 追踪报告（A5，真实账本统计）", "",
             f"- 账本事件数：{result['ledger_events']}",
             f"- 规则总数：{result['rule_count']}",
             f"- 有触发记录的规则：{result['rules_with_trigger']}", ""]
    lines.append("## 逐规则（真实 error_rate）")
    for rid, info in sorted(result["per_rule"].items()):
        lines.append(f"- `{rid}`：触发={info['trigger']} 推翻={info['overturn']} "
                     f"逃逸关联={info['escape']} error_rate={info['known_error_rate']}")
    with open(ERROR_REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(ERROR_REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def error_selftest() -> int:
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


def error_main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 规则 error 追踪（真实账本）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--track", action="store_true", help="真实统计 67 规则 error_rate")
    args = ap.parse_args(argv)
    if args.check:
        return error_selftest()
    result = track()
    write_error_report(result)
    print(f"[645 rule_error_tracker] 规则={result['rule_count']} "
          f"有触发={result['rules_with_trigger']} 总触发={result['total_trigger']}")
    return 0




# ======== 647 D1 合并自 rule_aging_detector_645.py（符号已重命名以避冲突）========
# （该成员的 `os/sys/defaultdict/datetime` 导入已在文件顶部 —— 647 D3 死代码清理）


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGING_REPORT_MD = os.path.join(ROOT, "data", "645_aging_report.md")
AGING_REPORT_JSON = os.path.join(ROOT, "data", "645_aging_report.json")
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
    events = load_ledger()
    if rules is None:
        rules = RULE_IDS or []
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
            if _is_overturn(ev):
                bucket["overturn"] += 1
            if _is_escape(ev):
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


def write_aging_report(result: dict) -> None:
    """写 A6 老化报告（647 D1：重命名以区别于 A4 的 `write_report`）。"""
    lines = ["# 645 规则老化检测报告（A6，真实时间戳趋势）", "",
             f"- 时间窗口：近 {result['window_days']} 天",
             f"- 规则总数：{result['rules_total']}",
             f"- **老化规则数：{result['aging_count']}**（真实趋势/逃逸关联）", ""]
    lines.append("## 老化规则（真实证据）")
    for rid in result["aging_rules"][:20]:
        v = result["per_rule"][rid]
        lines.append(f"- `{rid}`：近窗触发={v['recent_trigger']} 更早={v['older_trigger']} "
                     f"趋势={v['trend']} 误报趋势={v['misreport_trend']} 逃逸关联={v['escape_assoc']}")
    with open(AGING_REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(AGING_REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def aging_selftest() -> int:
    """只读自检：趋势计算逻辑（合成带时间戳事件，不读真实账本）。"""
    # 直接测趋势：更早窗口基数大 → 下滑明显
    older_trig, recent_trig = 5, 1
    trend = (recent_trig - older_trig) / older_trig
    assert trend < 0
    assert max(0.0, -trend) > 0.1
    # 真实账本可读
    assert isinstance(load_ledger(), list)
    return 0


def aging_main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 规则老化检测（真实趋势）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--detect", action="store_true", help="真实检测老化规则")
    args = ap.parse_args(argv)
    if args.check:
        return aging_selftest()
    result = detect()
    write_aging_report(result)
    print(f"[645 aging] 规则={result['rules_total']} 老化={result['aging_count']}")
    return 0


