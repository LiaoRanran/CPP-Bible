"""637 C · 候选生成器（CandidateGenerator）——为 top 5 问题各想 2-3 个方案

输入：ErrorDetector 的 JSON（默认 `data/637_errors.json`）。
输出：每个异常 2-3 个候选方案，含 动作/成本/收益/前置依赖/风险类别。

**纯规则匹配，不调 LLM**。`--check` 只读、不写盘、exit 0；`--report` 才落盘。
≥5 例单测（tests/test_candidate_generator_637.py）。
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

DEFAULT_IN = os.path.join(ROOT, "data", "637_errors.json")
OUT_JSON = os.path.join(ROOT, "data", "637_candidates.json")
OUT_MD = os.path.join(ROOT, "data", "637_candidates.md")

OK_LEVELS = {"低", "中", "高"}
RISK_CLASSES = {"report", "tool", "core"}


def _c(name: str, action: str, cost: str, benefit: str, dependency: str,
       risk_class: str) -> dict[str, str]:
    return {"name": name, "action": action, "cost": cost, "benefit": benefit,
            "dependency": dependency, "risk_class": risk_class}


# 方案库（异常 key → 2-3 个候选）；risk_class: report=只加报告/测量(0.5)、
# tool=加/改工具(1.0)、core=改 CORE_TOOLS 判决逻辑(1.5)
LIBRARY: dict[str, list[dict[str, str]]] = {
    "grounding_pct": [
        _c("补实验接地", "为 24 条未接地规则各补 1 个可观测实验/标准条文锚点", "高", "高", "需实验环境", "tool"),
        _c("未接地降级", "把未接地规则从 block 降为 warn（判决逻辑变更）", "中", "中", "需人审", "core"),
        _c("标记暂不使用", "把未接地规则标为「暂不使用」并登记清单", "低", "中", "无", "report"),
    ],
    "observation_pct": [
        _c("收历史错误率", "为 67 条观察态规则采集 known_error_rate 历史数据", "中", "高", "需运行记录", "report"),
        _c("观察态降级", "把观察态规则从 block 降为 warn（判决逻辑变更）", "中", "中", "需人审", "core"),
        _c("人工逐条审", "人工逐条复核观察态规则是否成熟可转正", "高", "中", "人力", "report"),
    ],
    "pytest_failures": [
        _c("修失败测试", "定位并修复失败用例，恢复回归绿灯", "中", "高", "无", "tool"),
        _c("标已知失败+skip", "对已知失败加 skip 标记并登记原因", "低", "低", "无", "tool"),
        _c("分析失败根因", "对失败做根因分类，输出报告而非立即改码", "低", "中", "无", "report"),
    ],
    "static_errors": [
        _c("自动修静态错", "用 ruff --fix / 手工按提示修可安全自动修项", "低", "中", "无", "tool"),
        _c("人工修静态错", "人工逐条修复剩余 ruff/mypy 报错", "中", "中", "人力", "report"),
    ],
    "taint_cards": [
        _c("追踪下游影响", "为每张 taint=true 卡列出下游引用清单", "低", "中", "无", "report"),
        _c("优先修高 taint", "优先复核引用数最多的 tainted 卡", "中", "高", "无", "tool"),
        _c("自动污染追踪", "加自动污染传播追踪器（影子）", "中", "高", "依赖 636 追踪器", "tool"),
    ],
    "exception_clauses": [
        _c("复审例外有效性", "逐条复审 227 条例外是否仍然成立", "中", "中", "人力", "report"),
        _c("合并相似例外", "合并同源相似例外，减少条款总数", "中", "中", "需人审", "core"),
        _c("为例外设过期", "为每条例外设过期时间（+180 天复审）", "低", "中", "无", "tool"),
    ],
    "ahead": [
        _c("push 未推提交", "把 ahead 的 commit push 到远端", "低", "中", "需联网", "report"),
        _c("拆分 commit", "把大 commit 拆成原子提交便于 review", "中", "低", "无", "report"),
        _c("排查不 push 原因", "检查为何长期不 push（阻塞/评审/网络）", "低", "低", "无", "report"),
    ],
    "tools_per_test": [
        _c("补测试", "为缺测试的新工具补回归用例", "中", "高", "无", "tool"),
        _c("删重复工具", "合并/删除功能重复的工具", "中", "中", "需人审", "tool"),
        _c("放慢工具增长", "冻结新增工具，先补测试再扩功能", "低", "低", "无", "report"),
    ],
}

FALLBACK = [
    _c("补报告/测量", "先做只读测量，把该问题量化后再决定方案", "低", "低", "无", "report"),
]


def candidates_for(key: str) -> list[dict[str, str]]:
    return [dict(c) for c in LIBRARY.get(key, FALLBACK)]


def generate(errors: dict[str, Any]) -> list[dict[str, Any]]:
    items = []
    for a in errors.get("anomalies", []) or []:
        items.append({"anomaly": a, "candidates": candidates_for(str(a.get("key", "")))})
    return items


def load_errors(path: str) -> dict[str, Any]:
    try:
        data: Any = json.loads(open(path, encoding="utf-8").read())
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def write_report(in_path: str) -> dict[str, str]:
    errs = load_errors(in_path)
    items = generate(errs)
    n = sum(len(it["candidates"]) for it in items)
    out = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "source": os.path.relpath(in_path, ROOT).replace(os.sep, "/"),
        "n_anomalies": len(items),
        "n_candidates": n,
        "items": items,
    }
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    lines = ["# 637 · 候选方案（CandidateGenerator 自动生成）", "",
             f"> 来源：{out['source']}；异常 {len(items)} 个，候选方案 {n} 个。", ""]
    for it in items:
        a = it["anomaly"]
        lines += [f"## {a.get('name')}（{a.get('severity')}）", "",
                  "| 方案 | 做什么 | 成本 | 收益 | 依赖 |", "|---|---|---|---|---|"]
        for c in it["candidates"]:
            lines.append(f"| {c['name']} | {c['action']} | {c['cost']} | {c['benefit']} | {c['dependency']} |")
        lines.append("")
    lines += ["---", "本报告由 candidate_generator_637 自动生成 · 纯规则匹配，不改系统。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("8 类异常都有方案库", all(len(LIBRARY[k]) >= 2 for k in LIBRARY))
    for k, cs in LIBRARY.items():
        chk(f"{k} 方案字段合法",
            all(c["cost"] in OK_LEVELS and c["benefit"] in OK_LEVELS
                and c["risk_class"] in RISK_CLASSES and c["name"] and c["action"] for c in cs))
    chk("未知异常走兜底", len(candidates_for("__unknown__")) >= 1)
    demo = {"anomalies": [{"key": "grounding_pct", "name": "接地率低", "severity": "P1"}]}
    chk("generate 结构正确", generate(demo)[0]["candidates"][0]["risk_class"] in RISK_CLASSES)
    chk("每个异常 ≥2 方案", all(len(v) >= 2 for v in LIBRARY.values()))
    chk("输出路径在 data 下",
        OUT_JSON.startswith(os.path.join(ROOT, "data")) and OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="637 C 候选生成器")
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
    items = generate(load_errors(args.inp))
    if args.json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return 0
    for it in items:
        print(f"{it['anomaly'].get('name')}: {len(it['candidates'])} 个候选")
    return 0


if __name__ == "__main__":
    sys.exit(main())
