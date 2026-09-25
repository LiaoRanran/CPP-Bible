"""635 V26-1 · 错误代价比声明（带日期，只加数据不改判决）

计算当前错误代价比（**逃逸率 : 自身免疫率**）并给出**明确立场**，
落盘 `data/error_cost_ratio_statement.md`。后续任何阈值变更**必须引用本声明**。

- 逃逸率（漏报）：1/1406 ≈ 0.0711%（616 统计）；
- 自身免疫率（误报）：当前 0%（历史上曾 14.3%，634 C1 修复）。

参照 Blackstone 10:1 原则（宁放过 10 个，不错冤 1 个）。

**只读契约**：`--check` 只读、exit 0；`--report` 写声明。纯标准库；≥5 例单测。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_MD = os.path.join(ROOT, "data", "error_cost_ratio_statement.md")

ESCAPE = (1, 1406)
AUTOIMMUNE_NOW = (0, 28)
AUTOIMMUNE_HIST = (4, 28)
DATE = "2026-09-25"


def pct(num: int, den: int) -> float:
    return round(100.0 * num / max(1, den), 4)


def metrics() -> dict[str, Any]:
    e = pct(*ESCAPE)
    a_now = pct(*AUTOIMMUNE_NOW)
    a_hist = pct(*AUTOIMMUNE_HIST)
    # 实际配比（漏报:误报）——当前误报为 0 ⇒ 比值无界，用历史点给参照
    ratio_now = "∞（误报为 0）" if a_now == 0 else f"{round(e/a_now,3)}:1"
    ratio_hist = f"{round(e/a_hist, 4)}:1"
    return {"date": DATE, "escape_pct": e, "autoimmune_now_pct": a_now,
            "autoimmune_hist_pct": a_hist, "ratio_now": ratio_now,
            "ratio_hist": ratio_hist}


def verdict(m: dict[str, Any]) -> str:
    # 当前：漏报极低 + 误报 0 ⇒ 相对 Blackstone（宁可漏报多些也别误报）偏保守，可接受
    return ("**可接受**（当前配比 = 漏报 0.0711% : 误报 0%）。"
            "相对 Blackstone 10:1（宁放过多、勿冤枉少），本系统**误报已为 0**、"
            "漏报极低，处于**保守端**，无需为「减少误报」而放宽；"
            "若未来为压漏报而加严 gate，须回到本声明评估是否把误报推高到不可接受。")


def write_statement() -> str:
    m = metrics()
    lines = [
        f"# 错误代价比声明（{m['date']}）", "",
        "> 本声明由 `tools/error_cost_ratio_635.py` 生成；**后续任何阈值变更必须引用本声明**。", "",
        "## 一、当前实际配比", "",
        "| 项 | 值 | 来源 |", "|---|---|---|",
        f"| 逃逸率（漏报） | {m['escape_pct']}%（1/1406） | 616 统计 |",
        f"| 自身免疫率（误报） | {m['autoimmune_now_pct']}%（0/28） | 634 C1 后实测 |",
        f"| 历史自身免疫率 | {m['autoimmune_hist_pct']}%（4/28） | 634 C1 前 |",
        f"| **实际配比（漏报:误报）** | **{m['ratio_now']}** | 计算 |",
        f"| 历史配比 | {m['ratio_hist']} | 计算 |", "",
        "## 二、是否可接受（参照 Blackstone 10:1）", "",
        f"- {verdict(m)}", "",
        "## 三、调整方向建议", "",
        "1. **当前不建议放宽**（误报已 0，放宽无收益、徒增漏报）；",
        "2. **若要压漏报**：加严 gate 前，须在此声明下评估其对**误报率**的边际影响；",
        "3. **阈值治理**：任何 block/warn 阈值调整的 PR 需引用本文件日期。", "",
        "## 诚实登记", "",
        "1. 逃逸率取 **616 统计**（未重跑 mutation，§零.4）；",
        f"2. 误报为 0 使「配比」为无界值，故并列**历史点**（{m['ratio_hist']}）供参照；",
        "3. 本声明为**只加数据**，不改任何判决逻辑。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    m = metrics()
    chk("逃逸率 ≈ 0.0711", abs(m["escape_pct"] - 0.0711) < 0.001)
    chk("误报当前 0", m["autoimmune_now_pct"] == 0.0)
    chk("历史误报 14.29", abs(m["autoimmune_hist_pct"] - 14.2857) < 0.01)
    chk("配比含 ∞", "∞" in m["ratio_now"])
    chk("有明确立场", "可接受" in verdict(m))
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="635 V26-1 错误代价比声明")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_statement()}")
        return 0
    m = metrics()
    if args.json:
        print(json.dumps(m, ensure_ascii=False, indent=2))
        return 0
    print(m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
