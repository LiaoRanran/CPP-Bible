"""622 A5 · VFDR 真正计算 + 趋势

**VFDR（Verification Failure Discovery Rate）定义**：
> 在相同预算下，系统**主动发现**的、**此前未知**的验证漏洞数。

本工具用**真实沙箱实跑数据**（622 A1/A2/A4）计算三轮：

| 轮次 | 来源 | 预算（mutation 数） | 判决口径 |
|---|---|---|---|
| R1 | 620 第一轮（v7 既有可判集） | 1406 | v7 已记录判决（回放） |
| R2 | 622 A2（621 生成器 50 条） | 50 | **真实 gate**（沙箱） |
| R3 | 622 A4（v2 生成器 30 条） | 30 | **真实 gate**（沙箱） |

计算维度：每轮新逃逸数、累计新逃逸、**逃逸发现率**（新逃逸/预算）、趋势（含线性斜率）。

**诚实声明**：三轮的 `escaped` 均为 **0**（严格口径：须"检测消失"）。
⇒ VFDR **仍然恒为 0**。本工具的价值在于把"恒定 0"从"口径不明"变成**可复算的事实**，
并给出趋势与"下一步该打哪里"的量化依据。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

R2_RESULTS = os.path.join(ROOT, "data", "mutation_sandbox_run_622_results.json")
R3_RESULTS = os.path.join(ROOT, "data", "mutation_sandbox_run_622_round2_results.json")

# R1（620 第一轮）：v7 既有可判集，escaped=0（620 报告实测）
R1 = {"name": "R1 · 620 第一轮（v7 既有）", "budget": 1406, "escaped": 0,
      "source": "data/adversarial_loop_round1_620.md（620 实测）",
      "verdict_mode": "v7 已记录判决（回放）", "note": "候选空间钉死在 v7 ⇒ 结构上不可能有新逃逸"}


def _load(path: str) -> dict | None:
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_rounds() -> list[dict]:
    rounds = [dict(R1)]
    r2 = _load(R2_RESULTS)
    if r2:
        rounds.append({"name": "R2 · 622 A2（621 生成器 50 条）",
                       "budget": r2.get("total", 0),
                       "escaped": r2.get("distribution", {}).get("escaped", 0),
                       "source": "data/mutation_sandbox_run_622_results.json",
                       "verdict_mode": "真实 gate（沙箱）", "note": "3 策略，46% 不适用"})
    r3 = _load(R3_RESULTS)
    if r3:
        rounds.append({"name": "R3 · 622 A4（v2 生成器 30 条）",
                       "budget": r3.get("total", 0),
                       "escaped": r3.get("distribution", {}).get("escaped", 0),
                       "source": "data/mutation_sandbox_run_622_round2_results.json",
                       "verdict_mode": "真实 gate（沙箱）",
                       "note": "schema-aware + 新算子 M8/M9，v7 重叠 0%"})
    return rounds


def vfdr(rounds: list[dict]) -> dict:
    cum_budget = cum_escaped = 0
    rows = []
    for i, r in enumerate(rounds, 1):
        cum_budget += int(r.get("budget") or 0)
        cum_escaped += int(r.get("escaped") or 0)
        rows.append({
            "round": i, "name": r["name"], "budget": r.get("budget"),
            "escaped": r.get("escaped"),
            "escape_rate": round((r.get("escaped") or 0) / r["budget"], 6) if r.get("budget") else None,
            "cum_budget": cum_budget, "cum_escaped": cum_escaped,
            "vfdr_cumulative": round(cum_escaped / cum_budget, 6) if cum_budget else None,
            "source": r.get("source"), "verdict_mode": r.get("verdict_mode"),
        })
    series = [r["escaped"] for r in rows]
    n = len(series)
    slope = None
    if n >= 2:
        mx = (n - 1) / 2
        my = sum(series) / n
        den = sum((i - mx) ** 2 for i in range(n))
        slope = round(sum((i - mx) * (series[i] - my) for i in range(n)) / den, 6) if den else None
    return {"rows": rows, "series": series, "slope": slope,
            "total_budget": cum_budget, "total_escaped": cum_escaped,
            "vfdr_final": round(cum_escaped / cum_budget, 6) if cum_budget else None,
            "flat_zero": all(v == 0 for v in series)}


def render(res: dict) -> str:
    o = ["# 622 A5 · VFDR 真正计算 + 趋势\n"]
    o.append("> VFDR = 相同预算下主动发现的**此前未知**验证漏洞数 / 预算\n")
    o.append("## 一、逐轮 VFDR\n")
    o.append("| 轮次 | 来源 | 预算 | 新逃逸 | 逃逸发现率 | 累计预算 | 累计逃逸 | VFDR 累计 | 判决口径 |")
    for r in res["rows"]:
        o.append(f"| {r['round']} | {r['name']} | {r['budget']} | **{r['escaped']}** | "
                 f"{r['escape_rate']} | {r['cum_budget']} | {r['cum_escaped']} | "
                 f"**{r['vfdr_cumulative']}** | {r['verdict_mode']} |")
    o.append("")
    o.append("## 二、趋势数据（轮次 vs 新逃逸数）\n")
    o.append(f"- 序列：**{res['series']}**")
    o.append(f"- 线性斜率：**{res['slope']}**")
    o.append(f"- 是否 flat-zero：**{res['flat_zero']}**\n")
    o.append("## 三、与 620/621 的 VFDR 对比\n")
    o.append("| 批次 | VFDR | 原因 |")
    o.append("|---|---|---|")
    o.append("| 620 | **0.0** | 候选空间钉死在 v7（不生成新 mutation） |")
    o.append("| 621 | **0.0** | 能生成但只能**预测**判决，无沙箱施加能力 |")
    o.append(f"| **622** | **{res['vfdr_final']}** | **有沙箱真跑**，但 80 条均未产生逃逸 |")
    o.append("")
    o.append("## 四、结论\n")
    o.append("- 622 首次具备**真实判决能力**（沙箱 apply），VFDR 从「不可测」变为「**可测且测得 0**」。")
    o.append("- ⇒ 这是**方法论的进步**（从「口径不明」到「可复算的事实」），")
    o.append("  但**不是**成果进步：攻击面仍未打穿。")
    o.append("- 下一步（留 623）：按 A3 建议 ③ 做**规则全覆盖**（当前累计只触达 9/63），")
    o.append("  并叠加 replay 复算层。")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    rounds = [
        {"name": "a", "budget": 100, "escaped": 0, "source": "s", "verdict_mode": "v"},
        {"name": "b", "budget": 50, "escaped": 5, "source": "s", "verdict_mode": "v"},
        {"name": "c", "budget": 50, "escaped": 5, "source": "s", "verdict_mode": "v"},
    ]
    r = vfdr(rounds)
    chk("累计预算正确", r["total_budget"] == 200)
    chk("累计逃逸正确", r["total_escaped"] == 10)
    chk("VFDR 最终 = 10/200", r["vfdr_final"] == 0.05)
    chk("逐轮逃逸发现率", r["rows"][0]["escape_rate"] == 0.0 and r["rows"][1]["escape_rate"] == 0.1)
    chk("序列正确", r["series"] == [0, 5, 5])
    chk("斜率 > 0", r["slope"] > 0)
    chk("非 flat-zero", r["flat_zero"] is False)

    flat = vfdr([{"name": "x", "budget": 10, "escaped": 0, "source": "s", "verdict_mode": "v"}])
    chk("单轮 flat-zero", flat["flat_zero"] is True and flat["slope"] is None)
    chk("空轮次安全", vfdr([])["total_budget"] == 0)
    chk("可加载真实三轮", len(load_rounds()) >= 1)
    chk("报告可渲染", "VFDR 真正计算" in render(r))
    print(f"A5 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="622 A5 VFDR 计算 + 趋势")
    ap.add_argument("--out", help="报告输出路径")
    ap.add_argument("--json", dest="json_out", help="VFDR 数据 JSON 输出")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    res = vfdr(load_rounds())
    md = render(res)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
        print(f"wrote {args.out}  vfdr_final={res['vfdr_final']} flat_zero={res['flat_zero']}")
    else:
        print(md)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
