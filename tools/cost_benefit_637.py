"""637 D · 代价评估器（CostBenefit）——给每个候选方案打分排序

输入：CandidateGenerator 的 JSON（默认 `data/637_candidates.json`）。
输出：全部候选按 score 排序 + top 3 建议先做的（含「为什么它排第一」）。

评分公式：`score = 收益(1-3) / 成本(1-3) × 风险系数(0.5-1.5)`；
风险系数：report(只加报告/测量)=0.5、tool(加/改工具)=1.0、core(改 CORE_TOOLS)=1.5。

**纯数学计算，不调 LLM**。`--check` 只读、不写盘、exit 0；`--report` 才落盘。
≥5 例单测（tests/test_cost_benefit_637.py）。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

DEFAULT_IN = os.path.join(ROOT, "data", "637_candidates.json")
OUT_JSON = os.path.join(ROOT, "data", "637_scored.json")
OUT_MD = os.path.join(ROOT, "data", "637_scored.md")

LEVEL = {"低": 1, "中": 2, "高": 3}
RISK_FACTOR = {"report": 0.5, "tool": 1.0, "core": 1.5}
SEV_RANK = {"P0": 3, "P1": 2, "P2": 1}
TOP_N = 3


def score_one(cost: str, benefit: str, risk_class: str) -> float:
    c = LEVEL.get(cost, 2)
    b = LEVEL.get(benefit, 2)
    r = RISK_FACTOR.get(risk_class, 1.0)
    return round(b / c * r, 3)


def flatten(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for it in items:
        a = it.get("anomaly", {}) or {}
        for c in it.get("candidates", []) or []:
            rows.append({
                "anomaly_name": a.get("name", ""),
                "anomaly_severity": a.get("severity", ""),
                "candidate": c.get("name", ""),
                "action": c.get("action", ""),
                "cost": c.get("cost", ""),
                "benefit": c.get("benefit", ""),
                "risk_class": c.get("risk_class", ""),
                "risk_factor": RISK_FACTOR.get(str(c.get("risk_class", "")), 1.0),
                "dependency": c.get("dependency", ""),
                "score": score_one(str(c.get("cost", "")), str(c.get("benefit", "")),
                                   str(c.get("risk_class", ""))),
            })
    return rows


def rank(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda r: (
        -float(r["score"]),
        -LEVEL.get(str(r["benefit"]), 0),
        LEVEL.get(str(r["cost"]), 9),
        -SEV_RANK.get(str(r["anomaly_severity"]), 0),
        str(r["anomaly_name"]),
    ))


def reason(row: dict[str, Any]) -> str:
    return (f"收益{row['benefit']}({LEVEL.get(str(row['benefit']), 2)})/成本{row['cost']}"
            f"({LEVEL.get(str(row['cost']), 2)})×风险系数{row['risk_factor']}"
            f" → score {row['score']}；对应异常「{row['anomaly_name']}」({row['anomaly_severity']})。")


def load(path: str) -> dict[str, Any]:
    try:
        data: Any = json.loads(open(path, encoding="utf-8").read())
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def write_report(in_path: str) -> dict[str, str]:
    cand = load(in_path)
    rows = rank(flatten(list(cand.get("items", []) or [])))
    top = rows[:TOP_N]
    for r in top:
        r["reason"] = reason(r)
    out = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "source": os.path.relpath(in_path, ROOT).replace(os.sep, "/"),
        "n_candidates": len(rows),
        "scored": rows,
        "top3": top,
    }
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    lines = ["# 637 · 候选打分排序（CostBenefit 自动生成）", "",
             f"> 来源：{out['source']}；候选 {len(rows)} 个；公式 score = 收益/成本 × 风险系数。", "",
             "## 一、全量排序", "", "| # | 方案 | 异常 | 成本 | 收益 | 风险类别 | score |",
             "|---|---|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        lines.append(f"| {i} | {r['candidate']} | {r['anomaly_name']} | {r['cost']} | "
                     f"{r['benefit']} | {r['risk_class']} | {r['score']} |")
    lines += ["", "## 二、建议先做的 top 3", ""]
    for i, r in enumerate(top, 1):
        lines += [f"### {i}. {r['candidate']}", f"- 为什么：{r['reason']}",
                  f"- 做什么：{r['action']}", f"- 依赖：{r['dependency']}", ""]
    lines += ["---", "本报告由 cost_benefit_637 自动生成 · 纯数学计算，不改系统。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("低/中/高映射", LEVEL == {"低": 1, "中": 2, "高": 3})
    chk("风险系数 report/tool/core", RISK_FACTOR == {"report": 0.5, "tool": 1.0, "core": 1.5})
    chk("公式 高收益/低成本/report=1.5", score_one("低", "高", "report") == 1.5)
    chk("公式 高收益/高成本/tool=1.0", score_one("高", "高", "tool") == 1.0)
    chk("公式 低收益/高成本/tool=0.333", score_one("高", "低", "tool") == 0.333)
    demo = [{"candidate": "x", "cost": "低", "benefit": "高", "risk_class": "report",
             "anomaly_name": "A", "anomaly_severity": "P1"},
            {"candidate": "y", "cost": "高", "benefit": "低", "risk_class": "core",
             "anomaly_name": "B", "anomaly_severity": "P0"}]
    rows = rank(flatten([{"anomaly": {}, "candidates": []}]))  # 空输入不崩
    chk("空输入不崩", rows == [])
    ranked = rank([dict(demo[0], risk_factor=0.5, action="a", dependency="无",
                        score=score_one("低", "高", "report")),
                   dict(demo[1], risk_factor=1.5, action="b", dependency="无",
                        score=score_one("高", "低", "core"))])
    chk("排序：高分在前", ranked[0]["candidate"] == "x")
    chk("输出路径在 data 下",
        OUT_JSON.startswith(os.path.join(ROOT, "data")) and OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="637 D 代价评估器")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--in", dest="inp", default=DEFAULT_IN)
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        out = write_report(args.inp)
        print(f"written {out['json']} {out['md']}")
        return 0
    rows = rank(flatten(list(load(args.inp).get("items", []) or [])))
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    for r in rows:
        print(f"{r['score']} {r['candidate']} ({r['anomaly_name']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
