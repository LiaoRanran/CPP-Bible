"""643 E4 · **闭环扩大（条件触发）**（抗 Goodhart #4）。

**定位**：按 inbox 的**条件**决定是否扩大 `auto_executor` 白名单：
- **条件**：E3 的 R4 校准度 **≥ 60%**；
- 达标 ⇒ 从 642 C1 评估过的 8 个候选里，按 **score 升序**（风险最低优先）安全扩展 **2–3 类**，
  每类**必须**带草栏（护栏）、回滚方案、风险评估；
- 不达标 ⇒ **不扩展**，登记原因，留 644。

**实测**：R4 校准度 **10.0% < 60%** ⇒ **本批不扩展**（结论由 E3 实测数字驱动，不是预设）。

**本工具只做"决定 + 方案"**：即使达标也**不执行**扩展（改 `WHITELIST` 属改 642 批产物 +
改 `test_config` 受控面）⇒ 输出的是**扩展方案**，执行留人。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/643_whitelist_expand.md` + `.json`。
纯标准库；≥6 例单测。
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

import auto_executor_whitelist_eval_642 as W642  # noqa: E402
import loop_runner_643 as E3  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_whitelist_expand.md")
OUT_JSON = os.path.join(ROOT, "data", "643_whitelist_expand.json")
THRESHOLD = 0.60
MIN_ADD, MAX_ADD = 2, 3


def eligible() -> list[dict[str, Any]]:
    """可扩展候选 = 642 C1 里"技术可入选"且**未被拒**的类别，按 score 升序。"""
    r = W642.evaluate()
    out = [row for row in r["rows"]
           if row["verdict"] in ("技术可入选（本批不扩大）", "可入选")]
    out.sort(key=lambda x: (x["score"], x["category"]))
    return out


def decide(calibration: Optional[float] = None) -> dict[str, Any]:
    """条件触发判定（纯函数，可用合成校准度测试）。"""
    if calibration is None:
        calibration = E3.run()["calibration"]
    cands = eligible()
    ok = calibration is not None and calibration >= THRESHOLD
    if not ok:
        return {"calibration": calibration, "threshold": THRESHOLD, "expanded": False,
                "reason": (f"校准度 {calibration} < {THRESHOLD:.0%} ⇒ **不扩展**；"
                           "按 inbox 条件触发，不达标即登记原因、留 644"),
                "candidates_available": [c["category"] for c in cands],
                "plan": [], "executed": False,
                "what_would_be_needed": (
                    f"校准度需 ≥ {THRESHOLD:.0%}；当前口径为「预期兑现率」的可验证子集"
                    f"（{E3.run()['verified_subset']} 条），**样本量远不足** ⇒ "
                    "要么补实测样本，要么由人裁决改用别的口径（不得偷偷换口径）")}
    picked = cands[:MAX_ADD]
    plan = [{"category": c["category"], "score": c["score"],
             "guardrails": c["guardrails"], "rollback": c["rollback"],
             "risk": c["zone"]} for c in picked]
    return {"calibration": calibration, "threshold": THRESHOLD, "expanded": True,
            "reason": f"校准度 {calibration} ≥ {THRESHOLD:.0%} ⇒ 允许扩展 "
                      f"{len(plan)} 类（按 score 升序取最低风险）",
            "candidates_available": [c["category"] for c in cands],
            "plan": plan, "executed": False,
            "what_would_be_needed": "达标后仍需人审执行（改 `WHITELIST` 属改 642 批产物 + "
                                    "`test_config` 受控面 ⇒ 必须重钉台账）"}


def write_report() -> str:
    d = decide()
    lines = [
        "# 643 E4 · 闭环扩大（条件触发）", "",
        f"> 条件：校准度 ≥ **{THRESHOLD:.0%}**；实测 R4 校准度 = **{d['calibration']}**",
        f"> **判定：{'允许扩展' if d['expanded'] else '不扩展'}** —— {d['reason']}",
        f"> 执行状态：**未执行**（`executed={d['executed']}`）—— 即使达标也不代执行。", "",
        "## 一、不扩展时的登记（本批实况）", "",
        f"- 原因：{d['reason']}",
        f"- 补齐条件：{d['what_would_be_needed']}",
        f"- 已备候选（642 C1 评估过、技术可入选）：`{d['candidates_available']}`", "",
        "## 二、若达标的扩展方案（预生成，供 644 直接用）", "",
        "| 类别 | score | 影响面 | 护栏数 | 回滚方案 |", "|---|---|---|---|---|"]
    if d["plan"]:
        for p in d["plan"]:
            lines.append(f"| `{p['category']}` | {p['score']} | {p['risk']} | "
                         f"{len(p['guardrails'])} | {p['rollback']} |")
    else:
        lines.append("| — | — | — | — | **未生成（条件未达）** |")
    lines += ["", "## 三、执行边界（为什么即使达标也不代执行）", "",
              "1. 改 `auto_executor_640.WHITELIST` = 改**642 批已评估并冻结**的产物；",
              "2. 该类改动若触及 `tests/conftest.py`/`pyproject.toml`，属 **`tool_integrity` 的 "
              "`test_config` 受控面** ⇒ 必须**重钉台账**（改哈希），属「改信任根」级别动作；",
              "3. ⇒ 本工具只出**决定与方案**，执行与重钉**留人**。", "",
              "## 诚实登记", "",
              "1. **条件触发是硬条件**：校准度未达 ⇒ 一律不扩展（**不因「想推进」而放宽**）；",
              "2. **校准度口径本身有争议**（R4 用「可验证子集」口径）⇒ 若改口径必须**显式登记 + 人批**，"
              "不得偷偷换（A3 教训 1：先冻结口径再优化）；",
              "3. **预生成的扩展方案在条件未达时也不作数**：它只是「如果」，"
              "不代表可执行；",
              "4. **未改 642 的白名单评估**：候选与 score 全部读自 `auto_executor_whitelist_eval_642`；",
              "5. 本工具**只读 + 只写 data/**：不改 `WHITELIST`、不改台账、不执行任何修复。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    lo = decide(0.10)
    chk("低于门槛 ⇒ 不扩展", lo["expanded"] is False and lo["plan"] == [])
    chk("不扩展也登记原因", bool(lo["reason"]) and "不扩展" in lo["reason"])
    chk("不扩展必给「补齐条件」", "校准度需" in lo["what_would_be_needed"])

    hi = decide(0.65)
    chk("达标 ⇒ 允许扩展", hi["expanded"] is True)
    chk("扩展 2–3 类", MIN_ADD <= len(hi["plan"]) <= MAX_ADD, str(len(hi["plan"])))
    chk("每类都带护栏与回滚",
        all(p["guardrails"] and p["rollback"] for p in hi["plan"]))
    chk("按 score 升序取最低风险",
        [p["score"] for p in hi["plan"]] == sorted(p["score"] for p in hi["plan"]))
    chk("边界：恰好 0.60 ⇒ 达标（>=）", decide(0.60)["expanded"] is True)
    chk("None ⇒ 不扩展（无数据不拍板）", decide(None)["expanded"] is False)
    chk("**即使达标也不代执行**", hi["executed"] is False)
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 E4 白名单条件触发展开")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true", help="打印（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    if x.report:
        print(f"written {write_report()}")
        return 0
    d = decide()
    if x.json:
        print(json.dumps({k: v for k, v in d.items() if k != "plan"},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[whitelist-expand] 校准度 {d['calibration']} vs 门槛 {d['threshold']:.0%} ⇒ "
          f"{'允许扩展' if d['expanded'] else '不扩展'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
