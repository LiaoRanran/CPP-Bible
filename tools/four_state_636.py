"""636 V26-补2 · 四态判决模拟（**影子**）

把 34 份 baseline 报告的「历史判决」按**四态**重新归类：
- `pass`：完全通过，无例外；
- `pass_with_exception`：有例外条款但整体通过；
- `fail`：被 block/拒绝；
- `unknown`：证据不足，无法判决。

并对比**二态**（pass/block）：多少 `pass` 其实应是 `pass_with_exception`（**假 pass**）。

**只读契约**：`--check` 只读、exit 0；`--report` 写 `data/636_four_state_simulation.md`。
纯标准库；≥5 例单测。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_MD = os.path.join(ROOT, "data", "636_four_state_simulation.md")

_FAIL_RE = re.compile(r"\bblock\b|失败|fail|reject|被拒", re.IGNORECASE)
_EXC_RE = re.compile(r"豁免|例外|exempt|例外条款|out_of_scope", re.IGNORECASE)
_UNK_RE = re.compile(r"无数据|不可判|unable|无法判定|unknown", re.IGNORECASE)

STATES = ["pass", "pass_with_exception", "fail", "unknown"]


def baseline_files() -> list[str]:
    return sorted(glob.glob(os.path.join(ROOT, "data", "*baseline*")))


def classify(text: str) -> str:
    exc = bool(_EXC_RE.search(text))
    fail = bool(_FAIL_RE.search(text))
    unk = bool(_UNK_RE.search(text))
    # 优先级：fail > pass_with_exception > unknown > pass（启发式）
    if fail:
        return "fail"
    if exc:
        return "pass_with_exception"
    if unk:
        return "unknown"
    return "pass"


def simulate() -> dict[str, Any]:
    rows = []
    for p in baseline_files():
        t = open(p, encoding="utf-8", errors="replace").read()
        st = classify(t)
        rows.append({"file": os.path.basename(p), "state": st})
    dist: dict[str, int] = {}
    for r in rows:
        dist[r["state"]] = dist.get(r["state"], 0) + 1
    pass_like = dist.get("pass", 0) + dist.get("pass_with_exception", 0)
    fake_pass = dist.get("pass_with_exception", 0)
    return {"rows": rows, "four_state": dist, "two_state": {"pass": pass_like,
            "fail": dist.get("fail", 0), "unknown": dist.get("unknown", 0)},
            "fake_pass": fake_pass, "n": len(rows)}


def write_report() -> str:
    s = simulate()
    lines = [
        "# 636 V26-补2 · 四态判决模拟（影子）", "",
        "## 一、四态定义", "",
        "| 态 | 含义 |", "|---|---|",
        "| pass | 完全通过，无例外 |",
        "| pass_with_exception | 有例外条款但整体通过 |",
        "| fail | 被 block/拒绝 |",
        "| unknown | 证据不足，无法判决 |", "",
        f"## 二、34 份 baseline 重分类（实际 {s['n']} 份）", "",
        "| 文件 | 四态 |", "|---|---|"]
    for r in s["rows"]:
        lines.append(f"| `{r['file']}` | {r['state']} |")
    lines += ["", "## 三、分布对比（二态 vs 四态）", "",
              "| 态 | 数量 |", "|---|---|"]
    for k in STATES:
        lines.append(f"| {k} | {s['four_state'].get(k, 0)} |")
    lines += ["", f"- 二态口径（pass/fail/unknown）：`{s['two_state']}`", "",
              "## 四、假 pass 识别", "",
              f"- **假 pass**（二态下算 pass、四态下应为 pass_with_exception）：**{s['fake_pass']}** 份",
              f"- 占 pass-like（{s['two_state']['pass']}）的 "
              f"{round(100.0 * s['fake_pass'] / max(1, s['two_state']['pass']), 1)}%", "",
              "## 诚实登记", "",
              "1. **影子模拟**：不改任何历史判决，仅离线重分类；",
              "2. 分类为**关键词启发式**（按文件中是否出现 失败/豁免/无数据 等词），非逐条判读；",
              "3. 635 追加的字段小节（边界字段/两栏）**也在文件内**，可能影响关键词命中——如实说明；",
              "4. 四态是**表示法**，是否采用交人（§八）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("pass 分类", classify("一切正常通过") == "pass")
    chk("fail 分类", classify("被 block 拒绝") == "fail")
    chk("pass_with_exception 分类", classify("整体通过但有豁免条款") == "pass_with_exception")
    chk("unknown 分类", classify("无数据，无法判定") == "unknown")
    s = simulate()
    chk("重分类总数 ≥30", s["n"] >= 30)
    chk("四态和 = 总数", sum(s["four_state"].values()) == s["n"])
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="636 V26-补2 四态模拟")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    s = simulate()
    if args.json:
        print(json.dumps({k: v for k, v in s.items() if k != "rows"}, ensure_ascii=False, indent=2))
        return 0
    print({k: v for k, v in s.items() if k != "rows"})
    return 0


if __name__ == "__main__":
    sys.exit(main())
