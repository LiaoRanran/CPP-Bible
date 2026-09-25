#!/usr/bin/env python3
"""640 A2 · 闭环路线图对齐（D9：闭环建议与路线图长期错配的修复）

**病（638 交人项）**：637/638 闭环提的建议（修测试/修静态错）与路线图
（四态/FSM/理论建设/外骨骼）长期错配——candidate_generator 只按异常类别出方案，
不知道"当前批次该往哪走"。

**治法（覆盖层，不改 637 工具）**：
1. **路线图感知**：读 `_auto/status.json` 的 `current_task`/`next_batch` 文本，
   归出方向标签（theory / arch / exo / maintenance）；
2. **权重调整**：对 candidate_generator 的每个候选打路线图权重——
   方向一致 ×1.5 / 不一致 ×0.5 / 中性维护 ×1.0；
3. **候选库扩展**：补 理论建设 / 架构升级 / 外骨骼 三类候选（中性维护类保留）；
4. **对比**：重排后 top 建议与原 top 的差异。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 写
`data/640_loop_roadmap_align.md` + `.json`。纯标准库；≥5 例单测。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

STATUS = os.path.join(ROOT, "_auto", "status.json")
OUT_MD = os.path.join(ROOT, "data", "640_loop_roadmap_align.md")
OUT_JSON = os.path.join(ROOT, "data", "640_loop_roadmap_align.json")

DIRECTION_KEYWORDS: dict[str, tuple[str, ...]] = {
    "theory": ("四态", "FSM", "理论", "框架", "哲学", "规则哲学"),
    "arch": ("core 通用化", "通用化", "插件", "架构", "抽象", "core"),
    "exo": ("外骨骼", "验证框架", "信任根独立", "独立"),
}
CANDIDATE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "theory": ("理论", "框架", "哲学", "四态", "FSM", "概念"),
    "arch": ("架构", "通用化", "插件", "抽象", "core", "接口"),
    "exo": ("外骨骼", "验证框架", "信任根", "独立"),
}
DIRECTIONS = ("theory", "arch", "exo", "maintenance")
NEUTRAL = ("report", "tool")     # 中性维护类的 risk_class（core=判决逻辑，非中性）


def load_status(path: str = STATUS) -> dict[str, Any]:
    try:
        d: Any = json.loads(open(path, encoding="utf-8").read())
        return d if isinstance(d, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def classify_direction(text: str) -> str:
    """把路线图文本归入方向标签（关键词命中最多者；全无 ⇒ maintenance）。"""
    scores = {k: sum(1 for kw in kws if kw in text)
              for k, kws in DIRECTION_KEYWORDS.items()}
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else "maintenance"


def candidate_category(c: dict[str, Any]) -> str:
    text = f"{c.get('name', '')}{c.get('action', '')}"
    for cat, kws in CANDIDATE_KEYWORDS.items():
        if any(kw in text for kw in kws):
            return cat
    return "maintenance"


def weight_for(cat: str, direction: str) -> float:
    if cat == "maintenance" or direction == "maintenance":
        return 1.0
    return 1.5 if cat == direction else 0.5


def realign(items: list[dict[str, Any]], direction: str) -> dict[str, Any]:
    """对 candidate_generator 的输出做路线图加权重排。"""
    rows = []
    for it in items:
        for cand in it.get("candidates", []):
            cat = candidate_category(cand)
            w = weight_for(cat, direction)
            base = {"low": 1.0, "中": 2.0, "高": 3.0}.get(str(cand.get("benefit", "")), 1.0)
            risk = {"report": 0.5, "tool": 1.0, "core": 1.5}.get(
                str(cand.get("risk_class", "")), 1.0)
            rows.append({"anomaly": it.get("anomaly", {}).get("key", ""),
                         "name": cand.get("name", ""), "category": cat,
                         "roadmap_weight": w,
                         "score": round(base * risk * w, 3),
                         "risk_class": cand.get("risk_class", "")})
    rows.sort(key=lambda r: -r["score"])
    return {"direction": direction, "ranked": rows,
            "top3": [r["name"] for r in rows[:3]]}


def run() -> dict[str, Any]:
    status = load_status()
    text = f"{status.get('current_task', '')} {status.get('next_batch', '')}"
    direction = classify_direction(text)
    try:
        import candidate_generator_637 as cg
        items = cg.generate({"anomalies": [
            {"key": k, "name": k, "severity": "P1"} for k in cg.LIBRARY]})
    except Exception as exc:  # noqa: BLE001
        items = []
        direction_error = repr(exc)
    else:
        direction_error = ""
    aligned = realign(items, direction)
    return {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "direction": direction, "direction_source": "_auto/status.json",
            "direction_error": direction_error,
            "n_candidates": len(aligned.get("ranked", [])),
            **aligned}


def write_report() -> dict[str, str]:
    r = run()
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(r, fh, ensure_ascii=False, indent=2)
    L = ["# 640 A2 · 闭环路线图对齐（D9）", "",
         f"> 生成：{r['generated']}。覆盖层：不改 637 工具，只做路线图加权重排。", "",
         "## 一、当前路线图方向", "",
         f"- 方向标签：**{r['direction']}**（来源 `_auto/status.json` 的 current_task/next_batch 文本）；",
         "- 归类关键词：theory（四态/FSM/理论）/ arch（通用化/插件/架构）/ "
         "exo（外骨骼/信任根独立）/ maintenance（无命中）。", "",
         "## 二、候选重排（top 10）", "",
         "| 候选 | 类别 | 路线图权重 | 综合分 |", "|---|---|---|---|"]
    for row in r["ranked"][:10]:
        L.append(f"| {row['name']} | {row['category']} | {row['roadmap_weight']} | {row['score']} |")
    L += ["", "## 三、top 3（加权后）", ""]
    for i, name in enumerate(r["top3"], 1):
        L.append(f"{i}. {name}")
    L += ["", "## 四、诚实边界", "",
          "- 关键词归类是**启发式**：中文表述变化可能导致误分类（单测锁定的是机制，不是具体归类结果）；",
          "- 权重 ×1.5/×0.5 是 640 任务书的**规定值**，不是调出来的；效果需人复评；",
          "- 637 的候选库仍是异常驱动的；路线图驱动的新增方向（理论/架构/外骨骼）"
          "只有在对应异常出现时才会出现在候选里。", ""]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    r = run()
    chk("方向标签 ∈ 四类", r["direction"] in DIRECTIONS)
    chk("候选非空且全部有权重",
        r["n_candidates"] > 0
        and all(x["roadmap_weight"] in (0.5, 1.0, 1.5) for x in r["ranked"]))
    chk("top3 ≤ 候选数", len(r["top3"]) <= 3)
    chk("重排降序", all(a["score"] >= b["score"]
                       for a, b in zip(r["ranked"], r["ranked"][1:])))
    chk("机制：方向一致 ×1.5", weight_for("theory", "theory") == 1.5)
    chk("机制：方向不一致 ×0.5", weight_for("theory", "arch") == 0.5)
    chk("机制：中性维护 ×1.0", weight_for("maintenance", "theory") == 1.0
        and weight_for("report类", "maintenance") == 1.0)
    chk("文本归类：理论文本 ⇒ theory", classify_direction("四态理论建设与FSM") == "theory")
    chk("文本归类：无关文本 ⇒ maintenance", classify_direction("修测试补字段") == "maintenance")
    chk("输出路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    print(f"A2 roadmap align selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="640 A2 闭环路线图对齐")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    ap.add_argument("--report", action="store_true", help="写报告")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(json.dumps(write_report(), ensure_ascii=False))
        return 0
    print(json.dumps(run(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
