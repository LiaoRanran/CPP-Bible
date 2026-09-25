"""636 2.2 · anti-windup + 告警预算设计（**影子，不拦截**）

定义「人审队列饱和」（三阈值 A/B/C）+ 三档 anti-windup 策略（影子模拟），
并给**告警预算速率**（每周新增告警上限）。**不真的拦截/降级**（§零.7）。

- A：队列长度 > 100；B：平均等待 > 7 天；C：周新增 > 周处理能力。
- 策略：**饱和** → 新告警降级 warn（不新增 block）；**半饱和** → 冷却期 3 天延迟入队；**正常** → 照常。

**只读契约**：`--check` 只读、exit 0；`--report` 写 `data/636_anti_windup_design.md`。
纯标准库；≥5 例单测。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_MD = os.path.join(ROOT, "data", "636_anti_windup_design.md")

QUEUE = os.path.join(ROOT, "data", "autoimmune_human_queue_631.jsonl")
AUTH = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")

THRESHOLD_A = 100      # 队列长度
THRESHOLD_B_DAYS = 7   # 平均等待天数
CAPACITY_PER_WEEK = 20  # 周处理能力（假设，登记）
OBSERVE_DAYS = 30      # 模拟窗口


def queue_len() -> int:
    try:
        return len([ln for ln in open(QUEUE, encoding="utf-8") if ln.strip()])
    except OSError:
        return 0


def weekly_new() -> int:
    """周新增告警（由权威账本全量 / 观测周数近似；登记为启发式）。"""
    try:
        n = len([ln for ln in open(AUTH, encoding="utf-8") if ln.strip()])
    except OSError:
        n = 0
    weeks = max(1, OBSERVE_DAYS // 7)
    return round(n / max(1, weeks))


def saturation() -> dict[str, Any]:
    q = queue_len()
    wn = weekly_new()
    avg_wait = round(q / max(1, CAPACITY_PER_WEEK) * 7, 1)  # 队列积压 → 等待天数近似
    a = q > THRESHOLD_A
    b = avg_wait > THRESHOLD_B_DAYS
    c = wn > CAPACITY_PER_WEEK
    level = "饱和" if (a and b) or (a and c) else ("半饱和" if (a or c) else "正常")
    return {"queue_len": q, "weekly_new": wn, "avg_wait_days": avg_wait,
            "A": a, "B": b, "C": c, "level": level}


def simulate(days: int = OBSERVE_DAYS) -> dict[str, Any]:
    """过去 N 天的影子模拟：多少告警会被冻结/降级。"""
    s = saturation()
    alerts = round(s["weekly_new"] * days / 7)
    if s["level"] == "饱和":
        frozen = alerts          # 全部降级
    elif s["level"] == "半饱和":
        frozen = round(alerts * 0.5)
    else:
        frozen = 0
    return {"window_days": days, "alerts": alerts, "frozen_or_downgraded": frozen,
            "level": s["level"]}


def budget() -> dict[str, Any]:
    return {"weekly_cap": CAPACITY_PER_WEEK, "unit": "告警/周",
            "rule": "周新增告警超过该上限即触发半饱和（冷却期 3 天）"}


def write_report() -> str:
    s = saturation()
    sim = simulate()
    b = budget()
    lines = [
        "# 636 2.2 · anti-windup + 告警预算设计（影子，未拦截）", "",
        "## 一、饱和定义（三阈值）", "",
        "| 阈值 | 定义 | 当前值 | 触发 |", "|---|---|---|---|",
        f"| A | 队列长度 > {THRESHOLD_A} | {s['queue_len']} | {'✅是' if s['A'] else '否'} |",
        f"| B | 平均等待 > {THRESHOLD_B_DAYS} 天 | {s['avg_wait_days']} | {'✅是' if s['B'] else '否'} |",
        f"| C | 周新增 > 周处理能力({CAPACITY_PER_WEEK}) | {s['weekly_new']} | "
        f"{'✅是' if s['C'] else '否'} |",
        f"| **综合等级** | — | **{s['level']}** | — |", "",
        "## 二、anti-windup 三档策略", "",
        "| 档 | 触发 | 行为 |", "|---|---|---|",
        "| 饱和 | A∧B 或 A∧C | 新告警**降级为 warn**（不新增 block） |",
        "| 半饱和 | A∨C | 新告警**延迟入队**（冷却期 3 天） |",
        "| 正常 | 其余 | 照常 |", "",
        f"## 三、历史模拟（过去 {sim['window_days']} 天，影子）", "",
        f"- 窗口内告警：**{sim['alerts']}** 条",
        f"- 会被**冻结/降级**：**{sim['frozen_or_downgraded']}** 条（等级={sim['level']}）", "",
        "## 四、告警预算速率", "",
        f"- **每周新增告警上限 = {b['weekly_cap']}**（超限触发半饱和）；",
        f"- 规则：{b['rule']}。", "",
        "## 诚实登记", "",
        "1. **影子模式**：不真的降级/延迟任何告警（§零.7）；",
        "2. `avg_wait_days` 用「队列积压/CAPACITY×7」**近似**；`weekly_new` 由账本/观测周数近似；",
        f"3. 周处理能力 {CAPACITY_PER_WEEK} 为**假设值**（无历史吞吐台账）——如实登记；",
        "4. 阈值 A/B/C 与策略仅为**设计**，是否启用交人（§八）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    s = saturation()
    chk("queue_len ≥ 0", s["queue_len"] >= 0)
    chk("level ∈ {正常,半饱和,饱和}", s["level"] in ("正常", "半饱和", "饱和"))
    chk("三阈值均为 bool", all(isinstance(s[k], bool) for k in ("A", "B", "C")))
    chk("simulate 有数字", simulate()["alerts"] >= 0)
    chk("budget 有上限", budget()["weekly_cap"] > 0)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="636 2.2 anti-windup 设计")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    d = {"saturation": saturation(), "simulate": simulate(), "budget": budget()}
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    print(d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
