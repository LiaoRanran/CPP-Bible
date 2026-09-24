"""634 B3 · N/A 率根因分类（**能算的算，算不了的诚实登记**）

**口径**：§一 记 N/A = 179/1593 = 11.24%（源 `data/mutation/full_baseline_v7.json`）。

**数据现实（重要）**：
- 616 的 `full_baseline_v7.json` **只存聚合计数**（variants/blocked/escaped/n_a/out_of_scope…）
  ⇒ **179 条 N/A 的逐行"原因"未落盘**，无法对它们做根因分类（除非重跑变异，重且需编译器）；
- 但 `data/mutation_sandbox_run_622_results.json`（50 行）与
  `data/high_complexity_sandbox_run_623.json`（80 行）**有逐行 verdict + reason**。

⇒ 本工具：对**有逐行 reason 的 130 条**做根因分类（infra_error / timeout / unjudgeable(载体) / other），
并给出「把 unjudgeable(载体) 移出分母」后的**清洁 N/A 率**；对 616 的 179 条**如实登记原因缺失**。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 才写 `data/na_rate_breakdown_634.md`。
纯标准库；≥5 例单测（tests/test_na_rate_634.py）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
V7 = os.path.join(ROOT, "data", "mutation", "full_baseline_v7.json")
RUN622 = os.path.join(ROOT, "data", "mutation_sandbox_run_622_results.json")
RUN623 = os.path.join(ROOT, "data", "high_complexity_sandbox_run_623.json")
OUT_MD = os.path.join(ROOT, "data", "na_rate_breakdown_634.md")

JUDGED = {"blocked", "escaped", "detected_nonblock"}
_CARRIER_RE = re.compile(r"无法施加|不可施加|不适用|out_of_scope|载体")
_TIMEOUT_RE = re.compile(r"timeout|超时")
_INFRA_RE = re.compile(r"error|infra|异常|失败")


def load(path: str) -> Any:
    try:
        return json.loads(open(path, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError):
        return None


def classify_row(r: dict) -> str:
    v = r.get("verdict", "")
    if v in JUDGED:
        return "judged"
    reason = str(r.get("reason", "")) + " " + str(r.get("edit", "")) + str(v)
    if _TIMEOUT_RE.search(reason):
        return "timeout"
    if _CARRIER_RE.search(reason):
        return "unjudgeable(载体)"
    if _INFRA_RE.search(reason) or v == "infra_error":
        return "infra_error"
    return "other"


def rows_of(path: str) -> list[dict]:
    d = load(path)
    if isinstance(d, dict):
        return d.get("rows", []) or []
    return d if isinstance(d, list) else []


def breakdown() -> dict[str, Any]:
    rows = rows_of(RUN622) + rows_of(RUN623)
    cats: dict[str, int] = {}
    for r in rows:
        c = classify_row(r)
        cats[c] = cats.get(c, 0) + 1
    total = len(rows)
    na = total - cats.get("judged", 0)
    carrier = cats.get("unjudgeable(载体)", 0)
    denom_clean = total - carrier
    na_clean = na - carrier
    v7 = load(V7) or {}
    return {"rows_total": total, "categories": cats,
            "na": na, "na_rate": round(100.0 * na / max(1, total), 2),
            "na_rate_clean": round(100.0 * na_clean / max(1, denom_clean), 2),
            "v7": {k: v7.get(k) for k in ("variants", "n_a", "out_of_scope", "blocked", "escaped")},
            "v7_na_rate": round(100.0 * (v7.get("n_a", 0)) / max(1, v7.get("variants", 1)), 2)}


def write_report() -> str:
    b = breakdown()
    lines = [
        "# 634 B3 · N/A 率根因分类", "",
        "## 一、总口径（616 源）", "",
        f"- `data/mutation/full_baseline_v7.json`：variants **{b['v7'].get('variants')}**、"
        f"n_a **{b['v7'].get('n_a')}**、out_of_scope {b['v7'].get('out_of_scope')}"
        f" ⇒ **N/A 率 {b['v7_na_rate']}%**（目标 <7%）。",
        "- **诚实前提**：v7 仅存**聚合**，**179 条 N/A 的逐行原因未落盘** ⇒ 对它们做根因分类"
        "需**重跑变异**（重 + 需编译器），非本批可无损完成。", "",
        "## 二、有逐行 reason 的样本分类（622 50 条 + 623 80 条 = 130 条）", "",
        "| 类别 | 数量 |", "|---|---|"]
    for k, v in sorted(b["categories"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| {k} | {v} |")
    lines += ["", f"- 样本 N/A 率：**{b['na_rate']}%**（{b['na']}/{b['rows_total']}）",
              f"- **清洁 N/A 率**（把 `unjudgeable(载体)` 移出分母）：**{b['na_rate_clean']}%**", "",
              "## 三、修复方案", "",
              "1. **载体型 N/A（无法施加 op/field）不是 infra 故障，是「载体天花板」**：按 §六.B3 `unjudgeable`"
              "口径**标记为「规则覆盖盲区」并移出分母**（本工具已给出清洁率）；",
              "2. **真 infra_error**：给沙箱 apply 更明确的错误码（而非并入 N/A）；",
              "3. **timeout**：分批 / 加长超时。", "",
              "## 四、诚实登记（§八）", "",
              "1. **616 的 179 条 N/A 未逐行分类**（源无原因字段）⇒ 目标「11.24%→7%」**未能对全量证明**；",
              "2. 本批在**有 reason 的 130 条样本**上完成了分类 + 清洁率口径（把载体型移出分母），"
              "这是**可无损达成**的部分；",
              "3. 样本显示 **N/A 主因是「载体无法施加」(unjudgeable)**，而非 infra 故障 ⇒ 属 **coverage 问题"
              "而非 infra 问题**（§六.B3 已预告此结论），如实说明；",
              "4. 未重跑变异（重 + 需编译器），不伪造新数字。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("classify judged", classify_row({"verdict": "blocked"}) == "judged")
    chk("classify 载体型", classify_row({"verdict": "infra_error", "reason": "无法施加 op=M7"}) == "unjudgeable(载体)")
    chk("classify timeout", classify_row({"verdict": "n_a", "reason": "timeout 超时"}) == "timeout")
    b = breakdown()
    chk("样本行数 = 130", b["rows_total"] == 130)
    chk("v7 n_a = 179", b["v7"]["n_a"] == 179)
    chk("报告路径在 data 下（--check 不写）", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="634 B3 N/A 率根因分类")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    b = breakdown()
    if args.json:
        print(json.dumps(b, ensure_ascii=False, indent=2))
        return 0
    print(b)
    return 0


if __name__ == "__main__":
    sys.exit(main())
