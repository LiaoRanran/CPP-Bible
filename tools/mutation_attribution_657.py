#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""mutation_attribution_657.py — 657 C 段：把**剩余存活体逐条归因**（不藏、不编）。

任务书 C3 要求："剩余存活体全部归因（等价变异 / 不可测 / 成本太高）"。
本工具读 `data/656_mutation_report_{core,all}.json`，对每个存活体给出：

1. 它落在哪个函数里（`enclosing_func`，与变异工具同口径）；
2. 归因类别——
   - `equivalent`：**等价变异**，改法不改语义（逐条给"为什么不可区分"）；只对人工核实过的
     条目给出（下方 `KNOWN_EQUIVALENT`，**没有核实过的一律不标**）；
   - `cli_io`：CLI / 报告 / 文件 IO 路径（`main` / `write_report` / `build_checkpoint` /
     `verify_checkpoint_file` / `export_jsonl` / `import_jsonl` / `_sig` / `_leaves_from_ledger`）；
   - `not_in_kill_scope`：杀测试文件（`tests/test_core_pbt_656.py` 的 P1–P14 性质）**不覆盖**
     该路径，补测需另建夹具（如 HMAC checkpoint 文件）。
3. 每条都带 `目标/行/算子/原文`，可逐行回查。

`--check` 只读自检；`--report` 写 `data/657_mutation_attribution.md`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

import mutation_test_656 as mt  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "657_mutation_attribution.md")
REPORTS = {"core": os.path.join(ROOT, "data", "656_mutation_report_core.json"),
           "all": os.path.join(ROOT, "data", "656_mutation_report_all.json")}

#: 人工核对过的**等价变异**：(目标, 行号) → 为什么改了也不可区分。
KNOWN_EQUIVALENT: dict[tuple[str, int], str] = {
    ("four_state_verdict_638", 190):
        "`status == \"verified\" and not m` 改成 `!=`：`_raw_state(\"\")` 本身也判 `pass`，"
        "所以「改写 verdict」与「不改写」在 status=verified 且无显式 falsification 时结果相同；"
        "而一旦有显式 falsification，`not m` 为假使整条条件恒假 ⇒ 两者同样都不改写。",
    ("decision_event_v2_626", 244):
        "`e.supersedes or []` 改成 `and []`：**合法账本**里 `supersedes` 只指向更早的事件，"
        "因此最新一条必然不在 superseded 集合里 ⇒ `alive[-1] == evs[-1]`，两个写法同结果。"
        "（`supersedes` 若指向前方事件——本仓无此产生路径——才可能不同。）",
    ("decision_event_v2_626", 246):
        "`alive[-1] if alive else evs[-1]` 改成 `if not alive`：同上，合法账本下 "
        "`alive[-1] == evs[-1]`，两分支等价。",
}

#: 按函数归因（不在 KNOWN_EQUIVALENT 里的存活体用这张表归类）。
CLI_IO_FUNCS = frozenset({
    "main", "write_report", "compare", "_report", "build_checkpoint",
    "verify_checkpoint_file", "_sig", "_leaves_from_ledger", "export_jsonl",
    "import_jsonl", "load_ledger", "_raises",
})


def _func_of(target: str, line: int) -> str:
    src = open(os.path.join(HERE, f"{target}.py"), encoding="utf-8").read().splitlines(keepends=True)
    return mt.enclosing_func(src, line - 1)


def classify(target: str, line: int) -> tuple[str, str]:
    if (target, line) in KNOWN_EQUIVALENT:
        return "equivalent", KNOWN_EQUIVALENT[(target, line)]
    fn = _func_of(target, line)
    if fn in CLI_IO_FUNCS:
        return "cli_io", f"落点 `{fn}`：CLI / 报告 / 文件 IO 路径，P1–P14 性质测试不覆盖"
    return "not_in_kill_scope", f"落点 `{fn}`：现有杀测试（P1–P14）不含该路径，补测需另建夹具"


def run() -> dict[str, Any]:
    out: dict[str, Any] = {"scope": {}, "rows": {}}
    for scope, path in REPORTS.items():
        rep = json.load(open(path, encoding="utf-8"))
        surv = [r for r in rep["results"] if r["status"] == "survived"]
        rows = []
        for r in surv:
            kind, why = classify(r["target"], r["line"])
            rows.append({"target": r["target"], "line": r["line"], "op": r["op"],
                         "from": r.get("from"), "to": r.get("to"), "text": r.get("text"),
                         "func": _func_of(r["target"], r["line"]), "kind": kind, "why": why})
        out["scope"][scope] = {
            "scored": rep["killed"] + rep["survived"],
            "killed": rep["killed"],
            "survived": rep["survived"],
            "import_error": rep["import_error"],
            "timeout": rep["timeout"],
            "kill_rate_on_scored": rep["kill_rate_on_scored"],
            "by_kind": {k: sum(1 for r in rows if r["kind"] == k)
                        for k in ("equivalent", "cli_io", "not_in_kill_scope")},
        }
        out["rows"][scope] = rows
    return out


def write_report() -> str:
    r = run()
    L = ["# 657 C · 剩余存活体逐条归因", "",
         "> 工具：`tools/mutation_attribution_657.py`（只读；数据源 "
         "`data/656_mutation_report_{core,all}.json`）。", "",
         "## 一、达标对照", "",
         "| 作用域 | 被杀/计分 | 检出率 | 目标 | 判定 | 导入崩 | 超时 | 剩余存活 |",
         "|---|---|---:|---|---|---:|---:|---:|"]
    for scope in ("core", "all"):
        s = r["scope"][scope]
        tgt = 80 if scope == "core" else 60
        L.append(f"| `{scope}` | {s['killed']}/{s['scored']} | **{s['kill_rate_on_scored']}%** | "
                 f"≥{tgt}% | {'达标' if s['kill_rate_on_scored'] >= tgt else '未达标'} | "
                 f"{s['import_error']} | {s['timeout']} | {s['survived']} |")
    L += ["", "> 口径：分母 = 被杀 + 存活（**导入即崩**与**超时**单独统计、不计入分母——"
              "前者不含信息量，后者是「跑飞」而非「没抓到」）。", ""]
    for scope in ("core", "all"):
        s = r["scope"][scope]["by_kind"]
        rows = r["rows"][scope]
        L += [f"## 二、{scope} 存活体归因（{len(rows)} 条）", "",
              f"- 等价变异：**{s['equivalent']}**；CLI/IO 路径：**{s['cli_io']}**；"
              f"现有杀测试未覆盖：**{s['not_in_kill_scope']}**。", "",
              "| 目标 | 行 | 算子 | 改了什么 | 落点函数 | 归因 |", "|---|---:|---|---|---|---|"]
        for x in rows:
            L.append(f"| `{x['target']}` | {x['line']} | {x['op']} | "
                     f"`{str(x['from'])[:10]}`→`{str(x['to'])[:10]}` | `{x['func']}` | "
                     f"{x['kind']} |")
        L.append("")
    L += ["## 三、等价变异的逐条理由（**只有核实过的才标 equivalent**）", ""]
    for (tgt, ln), why in sorted(KNOWN_EQUIVALENT.items()):
        L.append(f"- `{tgt}` L{ln}：{why}")
    L += ["", "## 四、诚实边界", "",
          "1. `equivalent` 只给**人工逐条核过**的 3 条；其余存活体一律按落点归类，"
          "**不为了把数字做好看而标等价**。",
          "2. `cli_io` / `not_in_kill_scope` ≠ 不可测：它们是「本轮杀测试文件没覆盖到」，"
          "补测需另建夹具（CLI 断言 / HMAC checkpoint 文件），成本已如实登记。",
          "3. `超时` 的变异体**是被发现**的（表达式跑飞），只是按工具口径不计入「被杀」，"
          "故不出现在本表。"]
    open(OUT_MD, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}{(' · ' + extra) if extra else ''}")
        ok = ok and cond

    for p in REPORTS.values():
        chk(f"报告存在：{os.path.basename(p)}", os.path.isfile(p))
    if not all(os.path.isfile(p) for p in REPORTS.values()):
        return 1
    r = run()
    for scope in ("core", "all"):
        s = r["scope"][scope]
        chk(f"{scope} 存活体数 == 归因条数",
            s["survived"] == len(r["rows"][scope]), f"{s['survived']}")
        chk(f"{scope} 归因分布和 == 存活数",
            sum(s["by_kind"].values()) == s["survived"], str(s["by_kind"]))
        chk(f"{scope} 每个存活体都有归因理由",
            all(x["why"] for x in r["rows"][scope]))
    chk("equivalent 只覆盖人工核实过的条目",
        all(any((x["target"], x["line"]) == k for k in KNOWN_EQUIVALENT)
            for x in r["rows"]["all"] if x["kind"] == "equivalent"))
    chk("输出落在 data/ 下", OUT_MD.replace("\\", "/").endswith("data/657_mutation_attribution.md"))
    print(f"mutation_attribution_657 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="657 C 存活体归因")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(write_report())
        return 0
    r = run()
    if a.json:
        print(json.dumps(r["scope"], ensure_ascii=False, indent=2))
        return 0
    for scope, s in r["scope"].items():
        print(f"[657attr] {scope}: {s['killed']}/{s['scored']} = {s['kill_rate_on_scored']}%"
              f" | 存活 {s['survived']} {s['by_kind']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
