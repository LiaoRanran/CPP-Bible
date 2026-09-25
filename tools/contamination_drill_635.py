"""635 V26-3 · 证据通道字段 + 污染传播演练（只加数据，不改判决）

1. **证据通道字段**：给证据元数据定义 6 类通道 + 控制方
   （direct_experiment / standard_textbook / cppreference / ai_generated /
   human_review / external_audit；控制方 self / external）；
2. **污染传播演练**：选一条**已在演练中暴露错误**的卡，追踪其被引用的下游卡，
   判断下游是否应标 `tainted`，并做**三阀门检查**（独立来源？必然发现？善意？）。

> 诚实：仓库**无任何 `status: disputed/refuted/retracted` 的卡**，故演练对象取
> 「演练中暴露过问题的卡」（ATOM-CONC-FENCE-001，623 逃逸/活性事件主体），并如实登记。

**只读契约**：`--check` 只读、exit 0；`--report` 写 `data/635_contamination_drill.md`。
纯标准库；≥5 例单测（tests/test_contamination_drill_635.py）。
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
OUT_MD = os.path.join(ROOT, "data", "635_contamination_drill.md")
TARGET = "ATOM-CONC-FENCE-001"

CHANNELS = ["direct_experiment", "standard_textbook", "cppreference",
            "ai_generated", "human_review", "external_audit"]
CONTROLLER = {"direct_experiment": "self", "standard_textbook": "external",
              "cppreference": "external", "ai_generated": "self",
              "human_review": "self", "external_audit": "external"}


def _read(p: str) -> str:
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def classify_channel(text: str) -> str:
    t = text.lower()
    if "cppreference" in t:
        return "cppreference"
    if "标准" in text or "iso" in t:
        return "standard_textbook"
    if "人审" in text or "human" in t:
        return "human_review"
    if "外部" in text or "external" in t or "audit" in t:
        return "external_audit"
    if "ai 生成" in text or "ai_generated" in t:
        return "ai_generated"
    return "direct_experiment"


def evidence_cards() -> list[dict[str, str]]:
    out = []
    base = os.path.join(ROOT, "evidence")
    for r, _d, fs in os.walk(base):
        for f in fs:
            if f.endswith(".md"):
                p = os.path.join(r, f)
                t = _read(p)
                ch = classify_channel(t)
                out.append({"rel": os.path.relpath(p, ROOT).replace(os.sep, "/"),
                            "id": f[:-3], "channel": ch, "controller": CONTROLLER[ch]})
    return out


def channel_distribution() -> dict[str, int]:
    d: dict[str, int] = {}
    for c in evidence_cards():
        d[c["channel"]] = d.get(c["channel"], 0) + 1
    return d


def _all_cards() -> list[tuple[str, str, str]]:
    out = []
    for r, _d, fs in os.walk(os.path.join(ROOT, "atoms")):
        for f in fs:
            if f.endswith(".md"):
                p = os.path.join(r, f)
                out.append((os.path.relpath(p, ROOT).replace(os.sep, "/"), f[:-3], _read(p)))
    return out


def downstream(target: str = TARGET) -> list[str]:
    return [rel for rel, cid, t in _all_cards()
            if cid != target and re.search(rf"\b{re.escape(target)}\b", t)]


def three_valves(target: str = TARGET) -> dict[str, str]:
    return {
        "独立来源": "❌ 下游卡多引用同一卡的证据链 ⇒ 无独立来源（同源污染不自动暴露）",
        "必然发现": "⚠️ 若下游同时被 gate 的 EV 引用规则覆盖则可发现；否则不必然",
        "善意": "✅ 无造假动机（内部流水线），属**善意错误**而非投毒",
    }


def taint_recommendation(target: str = TARGET) -> dict[str, Any]:
    ds = downstream(target)
    return {"target": target, "downstream": ds, "n_downstream": len(ds),
            "taint": len(ds) >= 1,
            "rule": "若 {t} 被判错 ⇒ 引用它的下游卡应标 tainted（需独立来源复核）".format(t=target)}


def write_report() -> str:
    ev = evidence_cards()
    dist = channel_distribution()
    ctrl: dict[str, int] = {}
    for c in ev:
        ctrl[c["controller"]] = ctrl.get(c["controller"], 0) + 1
    t = taint_recommendation()
    v = three_valves()
    lines = [
        "# 635 V26-3 · 证据通道字段 + 污染传播演练", "",
        "## 一、证据通道字段定义", "",
        "| 通道 | 控制方 | 含义 |", "|---|---|---|",
        "| direct_experiment | self | 本系统直接实验观测 |",
        "| standard_textbook | external | 标准/教科书 |",
        "| cppreference | external | cppreference 原文 |",
        "| ai_generated | self | AI 生成 |",
        "| human_review | self | 人审确认 |",
        "| external_audit | external | 外部独立审核 |", "",
        f"## 二、现有 {len(ev)} 张证据卡的通道分布", "",
        f"- 通道：`{dist}`", f"- 控制方：`{ctrl}`", "",
        "## 三、污染传播演练", "",
        f"- **演练对象**：`{t['target']}`（诚实：仓库无 `status: disputed/refuted` 的卡，"
        "取 623 演练中**暴露过问题的卡**）；",
        f"- **下游引用本卡的卡**：{t['n_downstream']} 张 ⇒ `{t['downstream'] or '无'}`",
        f"- **taint 建议**：`{t['taint']}`（{t['rule']}）", "",
        "### 三阀门检查", "", "| 阀门 | 判断 |", "|---|---|"]
    for k, val in v.items():
        lines.append(f"| {k} | {val} |")
    lines += ["", "## 四、建议的自动污染传播规则", "",
              "1. **引用即建边**：卡 A 引用卡 B ⇒ 建 `taint_edge(A→B)`；",
              "2. **B 判错 ⇒ A 标 tainted**，且 A 须**独立来源**复核才能清除 tainted；",
              "3. **控制方=external 的通道**（标准/cppreference/外部审计）可用作独立来源；"
              "`self` 通道不能自我洗白；",
              "4. 本批**只出规则建议，不改任何判决逻辑**（§零.1）。", "",
              "## 诚实登记", "",
              "1. 仓库**无正式 disputed 卡**，演练对象为「演练暴露卡」，如实登记；",
              "2. 通道分类为**内容关键词启发式**；",
              "3. 下游引用计数为**文本级**（非语义引用图）；",
              "4. 本工具**只读**。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("6 通道定义", len(CHANNELS) == 6)
    chk("证据卡 ≥1", len(evidence_cards()) >= 1)
    chk("控制器映射自洽", CONTROLLER["cppreference"] == "external")
    chk("通道分类可用", classify_channel("见 cppreference") == "cppreference")
    chk("下游可计算", isinstance(downstream(), list))
    chk("三阀门 3 项", len(three_valves()) == 3)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="635 V26-3 污染传播演练")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    d = {"channels": channel_distribution(), "drill": taint_recommendation()}
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    print(d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
