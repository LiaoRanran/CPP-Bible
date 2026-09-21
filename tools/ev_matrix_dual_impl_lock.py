#!/usr/bin/env python3
"""616 B3 · EV-MATRIX 双实现一致性**回归锁**。

目的：未来改 `gate_engine.py`（官方实现）后，**自动**验证它与独立第二实现
（`ev_matrix_unbacked_v2.py`，补全语义 P1+P2）在全部证据卡上的 verdict 是否仍一致。

口径（616 铁律的**明确许可**）：本工具 `import gate_engine` 并调用**单个规则函数**
`gate_engine.check_evidence_matrix_backed()`——这是**对比用途**，**不是**跑 `gate_engine.py --check`（监工门禁）。

产物：`data/ev_matrix_dual_impl_baseline_616.json`（一致性基线）+ `data/ev_matrix_dual_impl_lock_616.md`。
CLI：`--check`（锁逻辑自验证）/ `--baseline`（写基线）/ `--report` / 默认打印。

铁律：不跑 `gate_engine.py --check`；不改 `gate_engine.py`；不改受控目录。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import ev_matrix_unbacked_v2 as v2  # noqa: E402

BASELINE = ROOT / "data" / "ev_matrix_dual_impl_baseline_616.json"
REPORT = ROOT / "data" / "ev_matrix_dual_impl_lock_616.md"
PASS_THRESHOLD = 0.95


def _official_unbacked() -> set[str]:
    """官方实现（`gate_engine` 单规则函数）判为 UNBACKED 的卡（相对路径）。

    注：**只 import 单规则函数**，不跑 `gate_engine.py --check`。
    """
    import gate_engine as ge  # noqa: E402  616 B3 明确许可（对比用途，非监工门禁）
    findings = cast("list[Any]", ge.check_evidence_matrix_backed())
    return {str(getattr(f, "target", "")).replace("\\", "/") for f in findings}


def _applicable_cards() -> list[tuple[str, str]]:
    return [(rel, text) for rel, text in v2._cards() if len(v2.compiler_list(text)) > 1]


def compare() -> dict:
    unbacked = _official_unbacked()
    rows: list[dict] = []
    for rel, text in _applicable_cards():
        j = v2.judge(text, strip_sha=True)
        if j is None:
            continue
        official = "UNBACKED" if rel in unbacked else "BACKED"
        rows.append({"card": rel, "official": official, "v2": j["verdict"]})
    diverge = [r for r in rows if r["official"] != r["v2"]]
    applicable = len(rows)
    agree = applicable - len(diverge)
    rate = agree / applicable if applicable else 0.0
    return {"applicable": applicable, "agree": agree, "rate": round(rate, 4),
            "official_hits": sum(1 for r in rows if r["official"] == "UNBACKED"),
            "diverge": diverge, "status": "pass" if rate >= PASS_THRESHOLD else "fail"}


def write_baseline(c: dict | None = None) -> Path:
    c = c or compare()
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    BASELINE.write_text(json.dumps(
        {"ts": datetime.now().isoformat(timespec="seconds"),
         "official": "gate_engine.check_evidence_matrix_backed (import, 非 --check)",
         "independent": "ev_matrix_unbacked_v2 (P1+P2)",
         "applicable": c["applicable"], "agree": c["agree"], "rate": c["rate"],
         "official_hits": c["official_hits"],
         "diverge": [r["card"] for r in c["diverge"]],
         "status": c["status"],
         "pass_threshold": PASS_THRESHOLD}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return BASELINE


def render(c: dict) -> str:
    L = ["# 616 B3 · EV-MATRIX 双实现一致性回归锁", "",
         "> **用途**：未来改 `gate_engine.py` 后跑本工具，自动验证官方实现与独立第二实现的一致性。",
         "> 官方侧 = `import gate_engine; check_evidence_matrix_backed()`（**单规则函数，非 `--check` 门禁**）。", "",
         "## 一、当前一致性基线", "",
         f"- 适用卡（多编译器）：**{c['applicable']}**；官方 UNBACKED：**{c['official_hits']}**",
         f"- 一致 **{c['agree']}** / 分歧 **{len(c['diverge'])}** ⇒ 一致率 **{c['rate']:.1%}**",
         f"- 状态：**{c['status'].upper()}**（阈值 ≥{PASS_THRESHOLD:.0%}）", "",
         "## 二、分歧卡（如有）", "",
         "| 卡 | 官方 | 第二实现 v2 |", "|---|---|---|",
         *([f"| `{r['card']}` | {r['official']} | {r['v2']} |" for r in c["diverge"]] or ["| （无） | — | — |"]),
         "", "## 三、如何使用", "",
         "1. 每次修改 `gate_engine.py`（尤其 `check_evidence_matrix_backed`）后，跑 `python tools/ev_matrix_dual_impl_lock.py`；",
         f"2. 一致率 < 阈值（{PASS_THRESHOLD:.0%}）⇒ 状态 `fail`，**不一致即告警**；",
         "3. 处理流程：**先分析原因**（是官方实现改了对、还是第二实现漏了预处理），再决定修官方还是修第二实现；",
         "4. 修完重跑本工具 + 更新基线 `data/ev_matrix_dual_impl_baseline_616.json`。", "",
         "## 四、边界", "",
         "- 本工具**只对比**，不改任何实现；未跑 `gate_engine.py --check`。",
         "- `import gate_engine` 只为取单规则函数（对比用途）；其模块级副作用为只读缓存（无写盘）。", ""]
    return "\n".join(L) + "\n"


def check() -> list[str]:
    problems: list[str] = []
    c = compare()
    if c["applicable"] < 1:
        problems.append("适用卡为 0（数据源异常）")
    # 状态与阈值自洽
    expect = "pass" if c["rate"] >= PASS_THRESHOLD else "fail"
    if c["status"] != expect:
        problems.append("status 与阈值不一致")
    # 计数自洽
    if c["agree"] + len(c["diverge"]) != c["applicable"]:
        problems.append("计数不自洽（agree + diverge ≠ applicable）")
    # 官方侧确实被 import 到（函数存在）
    unbacked = _official_unbacked()
    if not isinstance(unbacked, set):
        problems.append("官方侧读数类型异常")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ev_matrix_dual_impl_lock",
                                 description="616 B3 EV-MATRIX 双实现一致性回归锁（import 单规则函数对比）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        problems = check()
        if problems:
            for msg in problems:
                print(f"[B3] ❌ {msg}", file=sys.stderr)
            return 1
        c = compare()
        print(f"[B3] ✅ 回归锁自验证通过：适用 {c['applicable']} / 一致率 {c['rate']:.1%} / "
              f"状态 {c['status'].upper()}")
        return 0
    c = compare()
    if a.baseline:
        p = write_baseline(c)
        print(f"[B3] 已写基线 {p.relative_to(ROOT).as_posix()}（一致率 {c['rate']:.1%}）")
        return 0
    if a.report:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(render(c), encoding="utf-8", newline="\n")
        print(f"[B3] 已写 {REPORT.relative_to(ROOT).as_posix()}（状态 {c['status'].upper()}）")
        return 0
    print(json.dumps(c, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
