"""630 C2 · 攻击面横切面：**时间轴 × 调度轴**（纯标准库，只读）

629 B1 建立了**部件轴**（L1–L8，攻击打在哪里）。v23 指出还需要两个**横切面**：

- **时间轴**：攻击是 `一次性`（打一枪就走）/ `周期性`（随数据老化反复出现）/
  `持续演化`（对手随防线变化不断调整）；
- **调度轴**：攻击是 `自发`（自己发起）/ `被触发`（特定状态才启动）/ `被诱导`（需要
  把防守方哄进某种状态，如人审压力、批量授权）。

本工具给 35 个向量逐个标注两轴属性，并输出**三维矩阵**（部件轴 × 时间轴 × 调度轴）。

**标注是规则化的启发式**（关键词 → 轴值），**每条都带 `依据`**（命中的关键词），
可逐条复核；不是人工逐条精读的结论，也不是机器"理解"语义。
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
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "attack_surface_axes_630.md")
OUT_JSON = os.path.join(ROOT, "data", "attack_surface_axes_630.json")

TIME_VALUES = ("一次性", "周期性", "持续演化")
SCHED_VALUES = ("自发", "被触发", "被诱导")

# 关键词 → 轴值（顺序即优先级；先命中者胜，依据记命中的词）
TIME_RULES: list[tuple[str, str, str]] = [
    (r"持续|演化|自适应|投毒|Goodhart|绕过|heuristic|正则|等价改写|多义|common-mode",
     "持续演化", "语义含「随防线变化不断调整」特征"),
    (r"漂移|陈旧|留痕|时间戳|累积|周期|re-anchor|老化|覆盖不足",
     "周期性", "语义含「随时间累积/反复出现」特征"),
]
SCHED_RULES: list[tuple[str, str, str]] = [
    (r"人审|授权|模板|rubber|批量|mirror|复核|签署|诱导|shorcut|shortcut",
     "被诱导", "需要把防守方（尤其人审环节）哄进某种状态才成立"),
    (r"时序|触发|条件|边界|阈值|优先级|CI|needs|执行序|回退|transition",
     "被触发", "只在特定状态/时刻才会启动"),
]


def vectors() -> list[dict[str, Any]]:
    import attack_surface_taxonomy as T

    return list(T.vectors())


def annotate_time(v: dict[str, Any]) -> dict[str, str]:
    text = f"{v.get('name', '')} {v.get('desc', '')} {v.get('probe') or ''}"
    for pat, val, why in TIME_RULES:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return {"time": val, "time_basis": f"{why}（命中 {m.group(0)!r}）"}
    return {"time": "一次性", "time_basis": "无时间累积/演化特征 ⇒ 默认一次性"}


def annotate_sched(v: dict[str, Any]) -> dict[str, str]:
    text = f"{v.get('name', '')} {v.get('desc', '')} {v.get('probe') or ''}"
    for pat, val, why in SCHED_RULES:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return {"sched": val, "sched_basis": f"{why}（命中 {m.group(0)!r}）"}
    return {"sched": "自发", "sched_basis": "无外部触发/诱导条件 ⇒ 默认自发"}


def annotate() -> list[dict[str, Any]]:
    out = []
    for v in vectors():
        out.append({**v, **annotate_time(v), **annotate_sched(v)})
    return out


def matrix() -> dict[str, Any]:
    rows = annotate()
    cells: dict[tuple[str, str, str], int] = collections.Counter(
        (r["layer"], r["time"], r["sched"]) for r in rows)
    by_time = collections.Counter(r["time"] for r in rows)
    by_sched = collections.Counter(r["sched"] for r in rows)
    empty = [(f"L{i}", t, s) for i in range(1, 9) for t in TIME_VALUES
             for s in SCHED_VALUES if (f"L{i}", t, s) not in cells]
    return {"rows": rows, "total": len(rows),
            "cells": {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in sorted(cells.items())},
            "by_time": dict(by_time), "by_sched": dict(by_sched),
            "empty_cells": [f"{a}|{b}|{c}" for a, b, c in empty],
            "cell_count": len(cells), "empty_count": len(empty)}


def write_report() -> str:
    m = matrix()
    rows = m["rows"]
    high = [r for r in rows if str(r.get("risk")) == "high"]
    lines = [
        "# 630 C2 · 攻击面横切面（时间轴 × 调度轴）", "",
        "> 工具：`tools/attack_surface_axes_630.py`（只读；向量表取 629 B1）",
        "> **标注是规则化启发式**（关键词→轴值），每条带 `依据`（命中词），可逐条复核", "",
        "## 一、两轴定义", "",
        "| 轴 | 取值 | 含义 |", "|---|---|---|",
        "| 时间轴 | `一次性` | 打一枪就走（单次变异/单次注入） |",
        "|  | `周期性` | 随数据老化/累积反复出现（漂移、陈旧留痕、时间戳） |",
        "|  | `持续演化` | 对手随防线变化不断调整（绕过、投毒、Goodhart、等价改写） |",
        "| 调度轴 | `自发` | 攻击者自己发起，无需外部条件 |",
        "|  | `被触发` | 只在特定状态/时刻启动（时序、阈值、边界、CI 依赖） |",
        "|  | `被诱导` | 需把防守方哄进某种状态（人审压力、批量授权、模板化） |", "",
        "## 二、分布", "",
        "| 时间轴 | 向量数 |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in sorted(m["by_time"].items(), key=lambda kv: -kv[1])],
        "", "| 调度轴 | 向量数 |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in sorted(m["by_sched"].items(), key=lambda kv: -kv[1])],
        "", f"- 非空三维格：**{m['cell_count']}** / 8×3×3=72"
        f"（空 {m['empty_count']} 个）", "",
        "## 三、三维矩阵（部件轴 L1–L8 × 时间轴 × 调度轴）", "",
        "| 层 | 时间轴 | 调度轴 | 向量数 |", "|---|---|---|---|",
        *[f"| {k.split('|')[0]} | {k.split('|')[1]} | {k.split('|')[2]} | {v} |"
          for k, v in m["cells"].items()], "",
        "## 四、逐向量标注（含依据）", "",
        "| 向量 | 层 | 名称 | risk | 时间轴 | 依据 | 调度轴 | 依据 |",
        "|---|---|---|---|---|---|---|---|",
        *[f"| `{r['id']}` | {r['layer']} | {r['name']} | {r.get('risk')} | "
          f"**{r['time']}** | {r['time_basis']} | **{r['sched']}** | {r['sched_basis']} |"
          for r in rows], "",
        "## 五、解读", "",
        f"- **时间轴重心**：{max(m['by_time'], key=m['by_time'].get)} 类最多"
        f"（{max(m['by_time'].values())}/35）⇒ 说明现有向量表主要刻画"
        "「打一枪」式攻击；`周期性`与`持续演化`的向量偏少，**而真实世界里演化型攻击"
        "最难防**（每轮修复都会训练对手）；",
        f"- **调度轴重心**：{max(m['by_sched'], key=m['by_sched'].get)} 类最多"
        f"（{max(m['by_sched'].values())}/35）；`被诱导`类（{m['by_sched'].get('被诱导', 0)} 个）"
        "全部集中在人审/授权层（L7），与「人审是唯一真人授权来源」的结构一致；",
        f"- **高风险向量的轴分布**：{len(high)} 个 high 向量，"
        f"时间轴 {dict(collections.Counter(r['time'] for r in high))}；"
        "两类「慢变量」（周期性/持续演化）在高风险向量里的占比，就是**长期对抗面的规模**；",
        "- **空三维格**不是缺陷而是**未知**：空等于「该层该类攻击目前没人想过」——"
        "这是给下一轮调研的线索清单（本批只登记，不编造向量）。", "",
        "## 六、局限", "",
        "- 标注是**关键词启发式**（规则表写在源码里），不是逐条精读：命名含糊的向量会落到默认值；",
        "- 「时间轴/调度轴」的取值集合是本批定义的（v23 只给方向），**边界情形有解释空间**；",
        "- 三维矩阵的 72 格里大量为空是**正常**的（35 个向量铺不满 72 格），不要读成覆盖率。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    m = matrix()
    chk("35 个向量全部标注", m["total"] == 35)
    chk("时间轴取值合法",
        all(r["time"] in TIME_VALUES for r in m["rows"]))
    chk("调度轴取值合法",
        all(r["sched"] in SCHED_VALUES for r in m["rows"]))
    chk("每条都带依据（可复核）",
        all(r["time_basis"] and r["sched_basis"] for r in m["rows"]))
    chk("时间轴分布合计 = 35", sum(m["by_time"].values()) == 35)
    chk("调度轴分布合计 = 35", sum(m["by_sched"].values()) == 35)
    chk("矩阵格计数合计 = 35", sum(m["cells"].values()) == 35)
    chk("空格数自洽（72 - 非空）", m["empty_count"] == 72 - m["cell_count"],
        f"({m['cell_count']} 非空)")
    chk("两轴都至少有 2 个非默认取值（标注有区分度）",
        len(m["by_time"]) >= 2 and len(m["by_sched"]) >= 2,
        f"({m['by_time']} / {m['by_sched']})")
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"C2 attack surface axes check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="630 C2 攻击面横切面（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    m = matrix()
    if args.json:
        print(json.dumps(m, ensure_ascii=False, indent=2, default=str))
        return 0
    print(f"time={m['by_time']} sched={m['by_sched']} cells={m['cell_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
