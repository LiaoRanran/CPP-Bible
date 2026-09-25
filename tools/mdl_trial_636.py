"""636 2.5 · MDL 边际判据试运行（**影子，不拦截新规则**）

**判据**（启发式近似，非严格 MDL，§七.4）：
`admit(rule) ⟺ savings > L(rule)`，其中
- `savings = samples_explained × log2(N)`（解释 N 元样本集里若干样本省下的比特）；
- `L(rule) = 8×len(id) + 8×len(title) + 32`（规则自身描述成本）；
- `samples_explained` = 该规则在 VFDR 热力图里被触达的**轮数**（0–6）。

离线重跑 **67 条规则** ⇒ admit/reject 数；并按「早期 vs 近期」统计**豁免率趋势**。

**只读契约**：`--check` 只读、exit 0；`--report` 写 `data/636_mdl_trial_run.md`。
纯标准库；≥5 例单测。
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "636_mdl_trial_run.md")
VFDR = os.path.join(ROOT, "data", "vfdr_report_v2_624.json")
N_SAMPLES = 1593   # mutation 变体数（616 v7）
SAMPLES_PER_ROUND = 50   # 每轮沙箱攻击数（近似；登记）
FIXED_BITS = 32


def rules() -> list[dict[str, str]]:
    try:
        import gate_engine as ge
        return [{"id": r.id, "title": getattr(r, "title", "")} for r in ge.RULES]
    except Exception:  # noqa: BLE001
        return []


def heatmap() -> dict[str, dict[str, bool]]:
    try:
        d = json.loads(open(VFDR, encoding="utf-8").read())
        h = d.get("heatmap", {})
        return h if isinstance(h, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def samples_explained(rule_id: str, hm: dict[str, dict[str, bool]]) -> int:
    """解释的样本数 = 触达轮数 × 每轮样本数（近似）。"""
    rounds = hm.get(rule_id, {})
    touched = sum(1 for v in rounds.values() if v) if isinstance(rounds, dict) else 0
    return touched * SAMPLES_PER_ROUND


def rule_cost(rule: dict[str, str]) -> int:
    return 8 * len(rule["id"]) + 8 * len(rule.get("title", "")) + FIXED_BITS


def admit(rule: dict[str, str], hm: dict[str, dict[str, bool]]) -> dict[str, Any]:
    se = samples_explained(rule["id"], hm)
    savings = se * math.log2(N_SAMPLES)
    cost = rule_cost(rule)
    return {"id": rule["id"], "samples_explained": se, "savings_bits": round(savings, 1),
            "cost_bits": cost, "admit": savings > cost}


def trial() -> dict[str, Any]:
    hm = heatmap()
    rs = rules()
    rows = [admit(r, hm) for r in rs]
    admitted = [r for r in rows if r["admit"]]
    rejected = [r for r in rows if not r["admit"]]
    half = len(rows) // 2
    early = rows[:half]
    recent = rows[half:]
    early_rate = round(100.0 * sum(1 for r in early if r["admit"]) / max(1, len(early)), 1)
    recent_rate = round(100.0 * sum(1 for r in recent if r["admit"]) / max(1, len(recent)), 1)
    return {"total": len(rows), "admitted": len(admitted), "rejected": len(rejected),
            "admit_rate_pct": round(100.0 * len(admitted) / max(1, len(rows)), 1),
            "early_rate_pct": early_rate, "recent_rate_pct": recent_rate,
            "rows": rows}


def write_report() -> str:
    t = trial()
    lines = [
        "# 636 2.5 · MDL 边际判据试运行（影子，未拦截新规则）", "",
        "## 一、判据与编码长度定义（启发式近似）", "",
        f"- `admit(rule) ⟺ savings > L(rule)`；`savings = samples_explained × log2({N_SAMPLES})`；",
        f"- `L(rule) = 8×len(id) + 8×len(title) + {FIXED_BITS}`；",
        f"- `samples_explained` = VFDR 热力图触达轮数 × {SAMPLES_PER_ROUND}（近似样本解释量）。", "",
        "## 二、67 规则模拟结果", "",
        f"- **admit：{t['admitted']}**；**reject：{t['rejected']}**；通过率 **{t['admit_rate_pct']}%**", "",
        "| 规则 | 样本数 | savings(bits) | cost(bits) | admit |", "|---|---|---|---|---|"]
    for r in t["rows"]:
        lines.append(f"| `{r['id']}` | {r['samples_explained']} | {r['savings_bits']} | "
                     f"{r['cost_bits']} | {'✅' if r['admit'] else '❌'} |")
    lines += ["", "## 三、豁免率趋势（早期 vs 近期）", "",
              f"- 早期一半规则通过率：**{t['early_rate_pct']}%**",
              f"- 近期一半规则通过率：**{t['recent_rate_pct']}%**",
              f"- 趋势：{'近期更高（规则更省数据）' if t['recent_rate_pct'] > t['early_rate_pct'] else ('近期更低（规则更冗余）' if t['recent_rate_pct'] < t['early_rate_pct'] else '持平')}", "",
              "## 四、若 MDL 在线会挡多少？", "",
              f"- **{t['rejected']}/{t['total']}** 条规则会被 reject（若在线）；",
              "- **本批为影子**，未拦截任何规则（§零.7）。", "",
              "## 诚实登记", "",
              "1. **编码长度为启发式近似**（非严格 MDL，§七.4）；",
              "2. `samples_explained` 用「VFDR 触达轮数」近似样本解释量；",
              "3. 7 条规则不在 VFDR 热力图（新增）⇒ samples_explained=0 ⇒ 必 reject（如实说明）；",
              "4. **影子**：未拦截、未改判。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("67 规则", len(rules()) == 67)
    a = admit({"id": "X", "title": "T"}, {"X": {"R1": True}})
    chk("触达 1 轮 samples=50", a["samples_explained"] == SAMPLES_PER_ROUND)
    chk("零触达必 reject", admit({"id": "Y", "title": "T"}, {})["admit"] is False)
    t = trial()
    chk("admitted+rejected=total", t["admitted"] + t["rejected"] == t["total"])
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="636 2.5 MDL 试运行")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    t = trial()
    if args.json:
        print(json.dumps({k: v for k, v in t.items() if k != "rows"}, ensure_ascii=False, indent=2))
        return 0
    print({k: v for k, v in t.items() if k != "rows"})
    return 0


if __name__ == "__main__":
    sys.exit(main())
