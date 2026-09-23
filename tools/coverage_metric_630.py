"""630 C1 · coverage（送审覆盖率）**第四元指标**（纯标准库，只读）

前三元（629 D3）盯的是 gate 的**判决质量**（逃逸率 = 漏报、自身免疫率 = 误报、触达率 = 沙箱
能打到多少规则）。它们都回答不了第四个问题：**我们到底有没有把攻击面送进去试**？

- **coverage（送审覆盖率）** = **实际跑过探针的攻击向量数 ÷ 总攻击向量数（35）**。

三个口径并列（避免混淆）：
| 口径 | 定义 | 数据源 |
|---|---|---|
| **有探针**（probe-ready） | 向量表里写了可执行探针 | 629 B1 `VECTORS[].covered` |
| **真实发生过**（real-event） | 历史真实攻击事件命中的向量 | 629 B2 `events()` |
| **本批送审过**（exercised） | 629/630 本批实跑探针所覆盖的向量（**显式映射表**，逐条给理由） |

`coverage` 取「real-event ∪ exercised」的并集 ÷ 35（两个口径都是"确实跑过"，只是来源不同）。

**诚实点**：`exercised` 的映射是**人工判断**（写在 `EXERCISED_NOTE` 里逐条给理由），
不是机器自动推出；且 630 D2 的 `M1 删字段` 在 35 向量表里**找不到对应向量**——
这本身就是一个 coverage 缺口发现。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "coverage_metric_630.md")
OUT_JSON = os.path.join(ROOT, "data", "coverage_metric_630.json")

# 本批实际送审的向量（人工映射，逐条给理由）
EXERCISED_NOTE = {
    "L3.2": "630 A2 跑 20 次语义等价格式微扰（该向量的 probe 正是 autoimmune_probe_629）",
    "L2.1": "630 D2 第八轮 20 条含 10 条 M7 sha256 篡改，直接打在证据内容漂移面",
}
# 本批实跑但**在 35 向量表里没有对应项**的算子（缺口发现）
UNMAPPED_OPS = {
    "M1 删字段": "630 D2 跑了 10 条「删 artifact_sha256/字段」，向量表无「必需字段被删除」向量",
}

ESCAPE = "1/1406（0.0711%，CS 上界 0.9062%）"
AUTOIMMUNE = "100%（23/23，其中 22 张口径级）"
TOUCHED = "36/67（53.7%，盲区 31）"


def vectors() -> list[dict[str, Any]]:
    import attack_surface_taxonomy as T

    return list(T.vectors())


def real_event_ids() -> set[str]:
    import attack_mapping_629 as M

    return {str(e.get("vector")) for e in M.events()}


def measure() -> dict[str, Any]:
    vs = vectors()
    total = len(vs)
    probe_ready = sorted(v["id"] for v in vs if v.get("covered"))
    no_probe = sorted(v["id"] for v in vs if not v.get("covered"))
    real = sorted(real_event_ids())
    exercised = sorted(EXERCISED_NOTE)
    ran = sorted(set(real) | set(exercised))
    never = sorted(set(v["id"] for v in vs) - set(ran))
    return {"total": total, "probe_ready": probe_ready,
            "probe_ready_count": len(probe_ready),
            "no_probe": no_probe, "no_probe_count": len(no_probe),
            "real_event": real, "real_event_count": len(real),
            "exercised_by_630": exercised,
            "exercised_note": EXERCISED_NOTE, "unmapped_ops": UNMAPPED_OPS,
            "ran": ran, "ran_count": len(ran),
            "coverage": round(len(ran) / total, 4),
            "coverage_pct": round(len(ran) / total * 100, 1),
            "never_run": never, "never_run_count": len(never),
            "four_metrics": {"逃逸率（漏报）": ESCAPE,
                             "自身免疫率（误报）": AUTOIMMUNE,
                             "触达率（沙箱覆盖规则）": TOUCHED,
                             "coverage（送审覆盖率）": f"{len(ran)}/{total} "
                                                      f"({len(ran) / total * 100:.1f}%)"}}


def write_report() -> str:
    m = measure()
    lines = [
        "# 630 C1 · coverage（送审覆盖率）第四元指标", "",
        "> 工具：`tools/coverage_metric_630.py`（只读；向量表取 629 B1，真实事件取 629 B2）",
        "", "## 一、定义与口径", "",
        "```",
        "coverage = (真实发生过 ∪ 本批送审过) 的攻击向量数 ÷ 总攻击向量数(35)",
        "```", "",
        "三个口径并列（避免混淆）：", "",
        "| 口径 | 含义 | 数 |", "|---|---|---|",
        f"| 有探针（probe-ready） | 向量表里写了可执行探针 | {m['probe_ready_count']}/{m['total']} |",
        f"| 真实发生过（real-event） | 历史真实攻击命中的向量（629 B2） | "
        f"{m['real_event_count']}/{m['total']} |",
        f"| **本批送审过（exercised）** | 629/630 本批实跑探针覆盖的向量 | "
        f"{len(m['exercised_by_630'])}/{m['total']} |",
        f"| **coverage（并集）** | real-event ∪ exercised | **{m['ran_count']}/{m['total']}"
        f" = {m['coverage_pct']}%** |", "",
        "## 二、本批送审映射（人工判断，逐条理由）", "",
        "| 向量 | 理由 |", "|---|---|",
        *[f"| `{k}` | {v} |" for k, v in EXERCISED_NOTE.items()], "",
        "## 三、从未跑过的向量（coverage 缺口）", "",
        f"共 **{m['never_run_count']}** 个：", "",
        "| 向量 | 名称 | 有探针 |", "|---|---|---|",
        *[f"| `{v['id']}` | {v['name']} | "
          f"{'有' if v.get('covered') else '**无**'} |"
          for v in vectors() if v["id"] in m["never_run"]], "",
        "## 四、本批实跑但**向量表无对应项**的算子（缺口发现）", "",
        *[f"- **{k}**：{v}" for k, v in UNMAPPED_OPS.items()],
        "", "## 五、四元组联合报告", "",
        "| 维度 | 方向 | 值 |", "|---|---|---|",
        *[f"| {k} | {'漏报' if '逃逸' in k else ('误报' if '自身免疫' in k else '覆盖')} | "
          f"{v} |" for k, v in m["four_metrics"].items()], "",
        "**四元组一起看才有意义**（诚实解读）：", "",
        f"1. **判决质量不差**：逃逸率 {ESCAPE.split('（')[0]}（极低）、硬开火率 0%（见 630 A3）；",
        "2. **误报在软层高**：自身免疫率 100%（v23 软阈值 20%/疲劳线 40%）；",
        f"3. **规则触达不到一半**：触达率 {TOUCHED}；",
        f"4. **送审覆盖率只有 {m['coverage_pct']}%**：35 个已识别向量里，"
        f"**{m['never_run_count']} 个从未跑过**（其中 "
        f"{sum(1 for v in vectors() if v['id'] in m['never_run'] and not v.get('covered'))} 个"
        f"连探针都没有）⇒ **「我们没测过的东西」仍然是最大盲区**，"
        f"比「gate 判错」更根本。", "",
        "## 六、局限与诚实登记", "",
        "- `exercised` 是**人工映射**（机器无法从「跑了 20 条微扰」自动推出「覆盖哪个向量」）；",
        f"- 629 B1 报告曾写「已有探针覆盖 24/35」，而本工具按 `VECTORS[].covered` 旗标实测 "
        f"**{m['probe_ready_count']}/35** —— 两者口径不同（B1 的 24 可能额外要求"
        "「探针建成且被单测锁定」），本报告按旗标口径，差异如实登记；",
        "- coverage **不衡量判决质量**：跑过的向量也可能（且确实）判错；它是「是否送审」的窗口；",
        "- 35 个向量本身可能不完备（见 §四 的 M1 缺口）⇒ coverage 高不等于攻击面全。",
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

    m = measure()
    chk("向量总数 = 35", m["total"] == 35, f"({m['total']})")
    chk("有探针 + 无探针 = 35",
        m["probe_ready_count"] + m["no_probe_count"] == 35)
    chk("真实事件向量 ⊆ 35 向量", set(m["real_event"]) <= {v["id"] for v in vectors()},
        f"({m['real_event']})")
    chk("本批送审映射的向量都真实存在",
        set(m["exercised_by_630"]) <= {v["id"] for v in vectors()})
    chk("coverage = ran ÷ 35（四舍五入到 4 位）",
        m["coverage"] == round(m["ran_count"] / 35, 4),
        f"({m['coverage_pct']}%)")
    chk("ran + never = 35", m["ran_count"] + m["never_run_count"] == 35)
    chk("四元组齐全", len(m["four_metrics"]) == 4)
    chk("缺口发现已登记（M1 无对应向量）", bool(m["unmapped_ops"]))
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"C1 coverage metric check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="630 C1 coverage 第四元指标（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    m = measure()
    if args.json:
        print(json.dumps(m, ensure_ascii=False, indent=2))
        return 0
    print(f"coverage={m['ran_count']}/{m['total']} ({m['coverage_pct']}%) "
          f"probe_ready={m['probe_ready_count']} never_run={m['never_run_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
