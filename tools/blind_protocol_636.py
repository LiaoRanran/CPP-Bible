"""636 2.3 · blind_protocol 影子设计 + 注入式盲化原型（**影子，不执行**）

**五步流程**（影子）：预登记 → 隐藏 AI 推荐 → 人判决 → 提交后揭盲 → 分歧分析。
**注入式盲化原型**（v26 补充）：`masked = value + sign × offset`（offset 隐藏、sign 随机），
评审期只显示 `residual`，评审通过后揭盲（恢复 offset/sign）。

**离线模拟**（用历史人审数据）：若当时是盲评，**违规次数**（AI 推荐可见下做的判决）= 多少？
**分歧率**：无盲评基线 ⇒ 如实登记「无法计算」，不编造。

**只读契约**：`--check` 只读、exit 0；`--report` 写 `data/636_blind_protocol_design.md`。
纯标准库；≥5 例单测。
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_MD = os.path.join(ROOT, "data", "636_blind_protocol_design.md")

LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
WORKSHEET = os.path.join(ROOT, "data", "human_review_worksheet_90.md")
SEED = 636

STEPS = [
    "Step 1 候选卡预登记：冻结 claim/evidence（哈希锁定）",
    "Step 2 隐藏 AI 推荐结果（审者不可见）",
    "Step 3 人做判决（独立填写）",
    "Step 4 提交后揭盲（显示 AI 推荐）",
    "Step 5 分歧分析（人 vs AI，逐条归档）",
]


def _jsonl(p: str) -> list[dict]:
    out = []
    if not os.path.exists(p):
        return out
    for ln in open(p, encoding="utf-8"):
        if ln.strip():
            try:
                out.append(json.loads(ln))
            except json.JSONDecodeError:
                continue
    return out


def inject(value: float, seed: int = SEED) -> dict[str, float]:
    """注入式盲化：隐藏 offset + 随机 sign。返回 masked/offset/sign/residual。"""
    rng = random.Random(f"{seed}:{value}")
    offset = round(abs(value) * 0.25 + 1.0, 3)      # 隐藏偏移量（>0）
    sign = rng.choice([-1, 1])
    masked = round(value + sign * offset, 3)
    return {"value": value, "offset": offset, "sign": sign, "masked": masked,
            "residual": round(masked - value, 3)}


def reveal(masked: dict[str, float]) -> float:
    return round(masked["masked"] - masked["sign"] * masked["offset"], 3)


def violations() -> dict[str, Any]:
    """违规 = AI 推荐可见下做的判决（历史人审）。"""
    rows = _jsonl(LEDGER)
    total = len(rows)
    visible = sum(1 for r in rows if r.get("decision_origin") in
                  ("human_observed", "user_authorized_execution"))
    sheet = open(WORKSHEET, encoding="utf-8", errors="replace").read() if os.path.exists(
        WORKSHEET) else ""
    sheet_shows_ai = bool(re.search(r"给了建议值|建议值", sheet))
    return {"decisions": total, "ai_visible_decisions": visible,
            "worksheet_shows_ai": sheet_shows_ai,
            "violations": visible if sheet_shows_ai else 0}


def disagreement() -> dict[str, Any]:
    return {"rate": None, "note": "无盲评基线 ⇒ 分歧率无法计算（不编造）"}


def write_report() -> str:
    v = violations()
    d = disagreement()
    demo = inject(35.8)   # 用接地率做注入演示
    lines = [
        "# 636 2.3 · blind_protocol 影子设计 + 注入式盲化原型", "",
        "## 一、blind_protocol 五步流程（影子，不执行）", ""]
    lines += [f"{i}. {s}" for i, s in enumerate(STEPS, 1)]
    lines += ["", "## 二、注入式盲化原型（v26）", "",
              "- **算法**：`masked = value + sign × offset`；`offset` 隐藏、`sign ∈ {-1,+1}` 随机；",
              "- **评审期**：看板只显示 `residual = masked - value`；",
              "- **揭盲**：`value = masked - sign × offset`（评审通过后恢复）；",
              f"- **演示**（value=35.8 接地率）：masked={demo['masked']}，sign={demo['sign']}，"
              f"offset={demo['offset']}，residual={demo['residual']}；揭盲回 {reveal(demo)} ✅", "",
              "## 三、离线模拟（历史人审数据）", "",
              f"- 判决总数：**{v['decisions']}**；其中 **AI 推荐可见**下做的：**{v['ai_visible_decisions']}**",
              f"- 工作表是否展示 AI 建议：**{v['worksheet_shows_ai']}**",
              f"- **违规次数**（若当时是盲评，这些本不该看到 AI 推荐）：**{v['violations']}**",
              f"- **分歧率**：{d['rate']}（{d['note']}）", "",
              "## 四、实施成本与前置条件", "",
              "1. **成本**：需改造人审前端（隐藏 AI 建议 + 提交后揭盲）+ 盲化指标看板；",
              "2. **前置**：审者须**独立来源**（当前单一评审人，635 Q4）；须记录**揭盲前后**判决；",
              "3. **风险**：盲评会降低吞吐（无 AI 提示），需与 anti-windup 预算联动。", "",
              "## 诚实登记", "",
              "1. **影子设计**：本批不执行盲评、不改任何人审流程；",
              "2. **分歧率无法计算**（无盲评基线）——**如实写「无法计算」**，不编造；",
              "3. 违规次数用「AI 可见判决数」近似（启发式）；",
              "4. 注入原型用**确定性种子**（可复现），offset 规则为启发式（非密码学盲化）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("五步流程", len(STEPS) == 5)
    m = inject(10.0)
    chk("注入 masked ≠ value", m["masked"] != m["value"])
    chk("揭盲可还原", reveal(m) == 10.0)
    chk("sign ∈ {-1,1}", m["sign"] in (-1, 1))
    v = violations()
    chk("违规数 ≥0", v["violations"] >= 0)
    chk("分歧率登记为 None", disagreement()["rate"] is None)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="636 2.3 blind protocol")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    d = {"violations": violations(), "disagreement": disagreement(), "demo": inject(35.8)}
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    print(d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
