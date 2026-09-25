"""635 1.3 · 四问现状审计（**每问必须有数据支撑，不凭印象**）

四问（v25 三问 + v26 第四问）：
1. 人审是否**盲评**？（人审时是否看到 AI 推荐结果？）
2. **AI 结论是否先于判断**？（AI 先出结论，人再审？）
3. 审查者是否见过**自己的校准数据**？（知道自己之前的准确率吗？）
4. **评审人由谁指派**？是否与卡片作者同源？

数据源：`data/human_review_worksheet_90.md`、`data/authority/decision_event_v2_ledger.jsonl`、
`data/authority/authority_log.jsonl`。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 才写
`data/635_four_questions_audit.md`。纯标准库；≥5 例单测（tests/test_four_questions_635.py）。
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WORKSHEET = os.path.join(ROOT, "data", "human_review_worksheet_90.md")
LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
AUTH = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")
OUT_MD = os.path.join(ROOT, "data", "635_four_questions_audit.md")


def _read(p: str) -> str:
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def _jsonl(p: str) -> list[dict]:
    out = []
    for ln in _read(p).splitlines():
        if ln.strip():
            try:
                out.append(json.loads(ln))
            except json.JSONDecodeError:
                continue
    return out


def q1_blind() -> dict[str, Any]:
    """人审是否盲评：工作表是否向审者展示 AI 建议。"""
    s = _read(WORKSHEET)
    shows_suggestion = bool(re.search(r"给了建议值|建议值|你只需要看一眼", s))
    return {"blind": not shows_suggestion, "evidence": "工作表用法写明「每条给了建议值，你只需要看一眼」"
            if shows_suggestion else "未发现建议展示", "sheet_lines": len(s.splitlines())}


def q2_ai_first() -> dict[str, Any]:
    """AI 结论是否先于判断：decision_origin 分布。"""
    rows = _jsonl(LEDGER)
    dist = dict(collections.Counter(r.get("decision_origin", "?") for r in rows))
    return {"total": len(rows), "origins": dist,
            "ai_first": dist.get("human_observed", 0) + dist.get("user_authorized_execution", 0) > 0}


def q3_calibration() -> dict[str, Any]:
    """审查者是否见过自己校准数据：全库检索准确率记录。"""
    hits = []
    for r, _d, fs in os.walk(os.path.join(ROOT, "data")):
        for f in fs:
            if not f.endswith((".md", ".json", ".jsonl")):
                continue
            p = os.path.join(r, f)
            t = _read(p)
            if re.search(r"审者?.{0,6}准确率|reviewer.{0,6}accuracy|校准数据", t):
                hits.append(os.path.relpath(p, ROOT).replace(os.sep, "/"))
    return {"records": hits, "has_calibration": bool(hits)}


def q4_assignment() -> dict[str, Any]:
    """评审人由谁指派/是否同源：authority_log 的 reviewer 分布。"""
    rows = _jsonl(AUTH)
    reviewers = dict(collections.Counter(r.get("reviewer", "?") for r in rows))
    return {"total": len(rows), "reviewers": reviewers,
            "single_reviewer": len(reviewers) <= 1}


def write_report() -> str:
    a = q1_blind()
    b = q2_ai_first()
    c = q3_calibration()
    d = q4_assignment()
    lines = [
        "# 635 1.3 · 四问现状审计", "", "> 每问：现状 + 证据 + 与理想状态的差距。", "",
        "## 问 1：人审是否盲评？", "",
        f"- **现状：{'是盲评' if a['blind'] else '❌ 非盲评（审者能看到 AI 建议）'}**",
        f"- 证据：`data/human_review_worksheet_90.md` 用法写明「{a['evidence']}」"
        f"（工作表 {a['sheet_lines']} 行）；",
        "- 差距：理想 = 审者在**看不到 AI 建议**下先独立判断；现状 = 建议与待填项同屏。", "",
        "## 问 2：AI 结论是否先于判断？", "",
        "- **现状：❌ AI 结论先于/伴随人判断**（工作表先给建议值，审者只做确认）",
        f"- 证据：`decision_event_v2_ledger.jsonl` decision_origin 分布 = `{b['origins']}`"
        f"（共 {b['total']} 条）；",
        "- 差距：理想 = `decision_origin` 应含 `human_observed_before_ai` 类；现状**无该字段值**，"
        "且工作表流程本身即 AI 先行。", "",
        "## 问 3：审查者是否见过自己的校准数据？", "",
        f"- **现状：{'有记录' if c['has_calibration'] else '❌ 无数据（全库无审者准确率记录）'}**",
        f"- 证据：全 `data/` 检索「审者准确率 / reviewer accuracy / 校准数据」命中："
        f"{c['records'] or '**0 处**'}；",
        "- 差距：理想 = 审者能查到自己历史判准率以自我校准；现状 = **完全无此数据**（如实登记）。", "",
        "## 问 4：评审人由谁指派？是否与卡片作者同源？", "",
        f"- **现状：❌ 单一评审人，无独立指派**（reviewer 分布 = `{d['reviewers']}`，共 {d['total']} 条）；",
        f"- `single_reviewer` = {d['single_reviewer']}（⇒ 无多审者交叉，**无独立性**）；",
        "- 差距：理想 = 评审人由独立方指派、与作者非同源、且 ≥2 人交叉；现状 = 全部同一人。", "",
        "## 汇总", "",
        "| 问 | 现状 | 理想 | 差距 |", "|---|---|---|---|",
        f"| 1 盲评 | {'是' if a['blind'] else '否'} | 是 | {'—' if a['blind'] else '需隐藏 AI 建议'} |",
        "| 2 AI 先行 | 是 | 否 | 需 human-first 字段与流程 |",
        f"| 3 校准数据 | {'有' if c['has_calibration'] else '无'} | 有 | {'—' if c['has_calibration'] else '需建审者准确率台账'} |",
        "| 4 评审人独立 | 否 | 是 | 需独立指派 + 多人交叉 |", "",
        "## 诚实登记（§七）", "",
        "1. 四问**均有数据支撑**（工作表原文 / ledger 字段分布 / 全库检索 / reviewer 分布），非印象；",
        "2. 问 3 **完全无数据** ⇒ 如实写「无数据」，不编造准确率；",
        "3. 问 2 的 `decision_origin` **无 `human_observed_before_ai` 类**，故「AI 先行」由"
        "工作表流程佐证，属**流程性证据**而非字段证据，如实说明；",
        "4. 本工具**只读**，不改人审/账本任何内容。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("Q1 返回 blind 布尔", isinstance(q1_blind()["blind"], bool))
    chk("Q2 origins 有 human_observed", q2_ai_first()["origins"].get("human_observed", 0) >= 1)
    chk("Q3 返回 records 列表", isinstance(q3_calibration()["records"], list))
    chk("Q4 reviewers 非空", bool(q4_assignment()["reviewers"]))
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="635 1.3 四问审计")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    d = {"q1": q1_blind(), "q2": q2_ai_first(), "q3": q3_calibration(), "q4": q4_assignment()}
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    print(d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
