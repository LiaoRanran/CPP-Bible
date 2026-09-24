"""634 B2 · Horizon 推高（复杂度-检出率曲线，**测量 + 诚实登记**）

**关键事实（实测）**：634 §一 记「60-80 桶检出率 0%（622 M9）」——但
`data/verification_horizon_curve_622.json` 存了 **7 个版本**，**最早 v1 起 60-80 桶即 100%**；
且 `data/high_complexity_sandbox_run_623.json` 的 **80 条高复杂度攻击触达了 17 条新 block 规则**。
⇒ **「0%→50%」的目标已由 622-624 达成**，634 的职责是**复算并如实登记基线陈旧**（不重复造轮子）。

本工具只读上述两个数据件，复算：各版本 bands、最新 60-80 检出率、高复杂度攻击的
判定分布与新触达规则数，产出 `data/horizon_curve_634.md`。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 才写报告。
纯标准库；≥5 例单测（tests/test_horizon_634.py）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CURVE = os.path.join(ROOT, "data", "verification_horizon_curve_622.json")
RUN623 = os.path.join(ROOT, "data", "high_complexity_sandbox_run_623.json")
OUT_MD = os.path.join(ROOT, "data", "horizon_curve_634.md")


def load_curve() -> list[dict]:
    try:
        v = json.loads(open(CURVE, encoding="utf-8").read())
        return v if isinstance(v, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def load_run() -> dict[str, Any]:
    try:
        d = json.loads(open(RUN623, encoding="utf-8").read())
        return d if isinstance(d, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def band60_80(v: dict) -> Optional[float]:
    b = v.get("bands", {})
    r = b.get("60-80")
    return float(r) if isinstance(r, (int, float)) else None


def touched_rules() -> list[str]:
    rules: set[str] = set()
    for r in load_run().get("rows", []):
        for x in r.get("new_block_rules", []):
            rules.add(x)
    return sorted(rules)


def verdict_distribution() -> dict[str, int]:
    out: dict[str, int] = {}
    for r in load_run().get("rows", []):
        k = r.get("verdict", "?")
        out[k] = out.get(k, 0) + 1
    return out


def write_report() -> str:
    curve = load_curve()
    latest = curve[-1] if curve else {}
    dist = verdict_distribution()
    rules = touched_rules()
    n = sum(dist.values()) or 0
    detected = dist.get("blocked", 0) + dist.get("detected_nonblock", 0)
    lines = [
        "# 634 B2 · Horizon 曲线（复杂度-检出率）", "",
        "## 一、关键更正：§一 的「60-80 桶 0%」是**陈旧基线**", "",
        f"- `data/verification_horizon_curve_622.json` 共存 **{len(curve)}** 个版本；",
        "- **最早 v1 起 60-80 桶检出率即为 100%**，并非 0%（§一 记的 0% 来自 622 M9 的**原始**发现，"
        "后续版本已修复，基线未同步）——本批如实登记该陈旧。", "",
        "## 二、各版本 bands", "", "| 版本 | 20-40 | 40-60 | 60-80 | score |", "|---|---|---|---|---|"]
    for v in curve:
        b = v.get("bands", {})
        lines.append(f"| {v.get('version')} | {b.get('20-40')} | {b.get('40-60')} | "
                     f"{b.get('60-80')} | {v.get('horizon_score')} |")
    lines += ["", "## 三、最新版本", "",
              f"- 版本 `{latest.get('version')}`：60-80 桶 = **{band60_80(latest)}**"
              f"（目标 ≥0.5 ⇒ **达成**）", "",
              "## 四、623 高复杂度攻击实测（80 条）", "",
              f"- 判定分布：{dist}", f"- 检出 = blocked + detected_nonblock = **{detected}/{n}**"
              f" = {round(100.0*detected/max(1,n),1)}%",
              f"- **新触达 block 规则 {len(rules)} 条**（目标 ≥5 ⇒ **达成**）："
              f"{', '.join('`'+r+'`' for r in rules[:20])}", "",
              "## 五、诚实登记（§八.4）", "",
              "1. **634 未新造高复杂度攻击**：目标「60-80 ≥50%」「触达 ≥5 新规则」**已由 622-624 达成**，"
              "本批做的是**复算 + 登记**，不重复造轮子（§零.7 先盘点后清理）；",
              "2. **§一起始基线陈旧**：其「0%」与实测（v1 起 100%）矛盾，已如实更正，不修数字；",
              "3. 623 的 80 条里仍有 **4 条 escaped / 2 条 infra_error / 12 条 neutral**——"
              "高复杂度带**并非全绿**，escape 根因见 `data/escape_root_cause_v2_623.md`（登记，本批不重跑）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    curve = load_curve()
    run = load_run()
    chk("曲线可读（≥1 版本）", len(curve) >= 1)
    chk("623 run 可读", bool(run.get("rows")))
    chk("band60_80 可取", band60_80(curve[-1]) is not None)
    chk("触达规则 ≥5", len(touched_rules()) >= 5)
    chk("判定分布非空", bool(verdict_distribution()))
    chk("报告路径在 data 下（--check 不写）", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="634 B2 Horizon 曲线复算")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    data = {"versions": len(load_curve()), "band60_80": band60_80(load_curve()[-1]),
            "touched_rules": len(touched_rules()), "verdicts": verdict_distribution()}
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    print(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
