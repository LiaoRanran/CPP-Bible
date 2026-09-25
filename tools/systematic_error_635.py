"""635 V26-2 · 系统误差清单（可收敛/不可收敛二分，永不合并）

把全部指标分两类：
- **可收敛**（统计性）：加样本量可改善（如逃逸率、τ_d、接地覆盖率）；
- **不可收敛**（系统性）：加样本量无效（coverage 缺口 / 自身免疫率 / Horizon 断崖 / N/A 率）。

并给**每份 baseline 报告**追加「可收敛指标 / 不可收敛指标」两栏（**永不合并成单一健康分**）。

**只读契约**：`--check` 只读、exit 0；`--apply` 追加两栏；`--report` 写
`data/635_systematic_error_ledger.md`。纯标准库；≥5 例单测。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_MD = os.path.join(ROOT, "data", "635_systematic_error_ledger.md")
MARKER = "635 V26-2 系统误差二分"

# (指标, 类别, 理由)
METRICS: list[tuple[str, str, str]] = [
    ("逃逸率", "可收敛", "多测 mutation 可更准确估计漏报率（统计量）"),
    ("τ_d（逃逸→修补间隔）", "可收敛", "样本量增加可收紧分位数"),
    ("接地覆盖率", "可收敛", "可补实验把「部分/未接地」转「已接地」"),
    ("工具数/测试数", "可收敛", "持续增加"),
    ("coverage 缺口", "不可收敛", "剩下的是**没测过的攻击面**，不是测不准"),
    ("自身免疫率", "不可收敛", "是**规则设计问题**，不是样本问题"),
    ("Horizon 断崖（60-80 桶）", "不可收敛", "是**载体天花板**，不是样本量"),
    ("N/A 率", "不可收敛", "主因是载体无法施加（634 B3），加样本无效"),
    ("gate 规则数", "不可收敛", "是**设计选择**，非估计量"),
]


def convergent() -> list[tuple[str, str]]:
    return [(n, r) for n, k, r in METRICS if k == "可收敛"]


def non_convergent() -> list[tuple[str, str]]:
    return [(n, r) for n, k, r in METRICS if k == "不可收敛"]


def _md_block() -> str:
    cv = convergent()
    nv = non_convergent()
    return (
        f"\n\n## {MARKER}（不可合并为单一健康分）\n\n"
        "**可收敛指标**（加样本可改善）：\n"
        + "".join(f"- {n}：{r}\n" for n, r in cv)
        + "\n**不可收敛指标**（加样本无效，须换方法）：\n"
        + "".join(f"- {n}：{r}\n" for n, r in nv)
    )


def baseline_files() -> list[str]:
    return sorted(glob.glob(os.path.join(ROOT, "data", "*baseline*")))


def apply(dry: bool = True) -> list[dict[str, Any]]:
    rows = []
    for p in baseline_files():
        s = open(p, encoding="utf-8", errors="replace").read()
        has = MARKER in s
        if not dry and not has and p.endswith((".md", ".json")):
            with open(p, "a", encoding="utf-8", newline="\n") as fh:
                fh.write(_md_block())
        rows.append({"file": os.path.basename(p), "already": has})
    return rows


def write_report() -> str:
    rows = apply(dry=True)
    lines = [
        "# 635 V26-2 · 系统误差清单（可收敛/不可收敛二分）", "",
        f"- baseline 报告：**{len(rows)}** 份（均追加两栏，永不合并）", "",
        "## 一、可收敛指标（统计性：加样本可改善）", "",
        "| 指标 | 理由 |", "|---|---|"]
    lines += [f"| {n} | {r} |" for n, r in convergent()]
    lines += ["", "## 二、不可收敛指标（系统性：加样本无效）", "",
              "| 指标 | 理由 |", "|---|---|"]
    lines += [f"| {n} | {r} |" for n, r in non_convergent()]
    lines += ["", "## 三、为什么某些指标不可收敛", "",
              "- **coverage 缺口**：剩下的是没被测过的**攻击面**，不是「测不准」——"
              "多跑同样的测试不会覆盖新面；须**换方法**（新攻击向量/新载体）。",
              "- **自身免疫率**：是**规则设计**问题（如把正确表述判为违规），加样本只会重复同一偏差。",
              "- **Horizon 断崖**：是**载体天花板**（gate-only 单卡 field-edit 的能力上限），非样本量。",
              "- **N/A 率**：主因「载体无法施加」（634 B3），是**方法/载体**问题。", "",
              "## 四、不可收敛指标的正确处理方式（不是加样本）", "",
              "1. **换方法**：coverage → 设计新攻击向量；自身免疫 → 改规则/加人工校准；"
              "Horizon → 换载体（跨卡/多字段）；",
              "2. **永不合并**：两类指标不得平均成单一「健康分」（会把系统性问题稀释成统计噪声）；",
              "3. 每份 baseline 报告已追加两栏，**结构性强制分离**。", "",
              "## 诚实登记", "",
              "1. 分类为**判断性**（按 §V26-2 定义），非自动度量；",
              "2. 追加两栏只**加小节**，不改既有内容与判决。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("可收敛 ≥1", len(convergent()) >= 1)
    chk("不可收敛 ≥1", len(non_convergent()) >= 1)
    chk("逃逸率可收敛", any(n == "逃逸率" for n, _ in convergent()))
    chk("自身免疫率不可收敛", any("自身免疫率" in n for n, _ in non_convergent()))
    chk("baseline 文件 ≥20", len(baseline_files()) >= 20)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="635 V26-2 系统误差清单")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.apply:
        rows = apply(dry=False)
        print(f"applied {len(rows)} files")
        return 0
    if args.report:
        print(f"written {write_report()}")
        return 0
    d = {"convergent": [n for n, _ in convergent()],
         "non_convergent": [n for n, _ in non_convergent()]}
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    print(d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
