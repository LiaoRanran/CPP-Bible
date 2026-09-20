"""612 B3 · 活性锚补全 what-if 分析（**只读** · 不跑 gate、不改任何文件）。

**what-if**：假设 50 条活性锚全部补全，模拟 gate `OBSERVATION-LIVENESS`（warn）会消掉多少。
**不跑 gate**（那是监工的事），而是基于规则逻辑**静态分析**：
  * A/B 类（补 `liveness.kind=fixture_symbol` + 合格符号）⇒ warn 消除；
  * C 类（改标 inference）⇒ 不再是 observation ⇒ warn 消除；
  * 每条已处理的缺锚命题，恰消除 **1** 条 OBSERVATION-LIVENESS warn（该规则对命题单点告警）。

诚实边界：本工具**只**分析 OBSERVATION-LIVENESS 这一条规则；不声称「补全后 gate 一定全绿」，
也不声称 poison 覆盖率会变（该规则不是 poison 攻击面上的攻击类型）。所有数字标「假设」。

CLI：`[--partial N]`（只补前 N 条，按 A→B→C 优先级）/ `--stats` / `--check`（exit 0=通过）。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
REPORT_OUT = ROOT / "data" / "liveness_impact_612.md"

_WARN_STATUSES = ("missing", "missing_symbol", "unknown_kind", "needs_review")


def current_warn_count() -> int:
    """gate `OBSERVATION-LIVENESS` 当前会报的 warn 数（= 缺命题级合格锚的 observation 数）。"""
    import proposition_liveness_audit as pla  # noqa: E402
    st = pla.audit()["observation_status"]
    return sum(st.get(s, 0) for s in _WARN_STATUSES)


def priority_ordered() -> list[dict]:
    """缺锚命题按 A→B→C 优先级排序（A 高置信可自动补，B 需人审选，C 建议改标 inference）。"""
    import liveness_review as lrev  # noqa: E402
    props = lrev.load_props()
    order = {"A": 0, "B": 1, "C": 2}
    return [{"proposition_id": pid, "class": p["class"]}
            for pid, p in sorted(props.items(),
                                 key=lambda kv: (order.get(kv[1]["class"], 9), kv[0]))]


def analyze(partial: int | None = None) -> dict:
    before = current_warn_count()
    ordered = priority_ordered()
    n = len(ordered) if partial is None else max(0, min(partial, len(ordered)))
    addressed = ordered[:n]
    by_class: dict[str, int] = {}
    for a in addressed:
        by_class[a["class"]] = by_class.get(a["class"], 0) + 1
    after = before - n
    return {"mode": "all" if partial is None else f"partial:{partial}",
            "warn_before": before, "addressed": n, "warn_after": after,
            "by_class": by_class, "total_props": len(ordered),
            "class_totals": {c: sum(1 for o in ordered if o["class"] == c)
                             for c in ("A", "B", "C")}}


def render(all_r: dict, partial_r: dict) -> str:
    L = ["# 612 B3 · 活性锚补全 what-if（只读 · 假设，不跑 gate）", "",
         "> **假设**：50 条缺锚 observation 全部补全（A/B 补合格符号 / C 改标 inference）。"
         "本工具按规则逻辑静态分析，**不跑 gate**、不改任何文件。", "",
         "## 一、OBSERVATION-LIVENESS warn 消除预测", "",
         "| 场景 | 处理条数 | warn 前 | warn 后 | 按类 |",
         "|---|---|---|---|---|",
         f"| 全量补全 | {all_r['addressed']} | {all_r['warn_before']} | {all_r['warn_after']} | {all_r['by_class']} |",
         f"| --partial {partial_r['addressed']} | {partial_r['addressed']} | {partial_r['warn_before']} | "
         f"{partial_r['warn_after']} | {partial_r['by_class']} |",
         "", f"- 缺锚命题总数 **{all_r['total_props']}**（A {all_r['class_totals']['A']} / "
             f"B {all_r['class_totals']['B']} / C {all_r['class_totals']['C']}）；优先级 A→B→C。",
         "- 每条已处理命题恰消除 1 条 OBSERVATION-LIVENESS warn（该规则对命题单点告警）。", "",
         "## 二、边界（诚实）", "",
         "- **只分析 OBSERVATION-LIVENESS 一条规则**：不声称「补全后 gate 一定全绿」；",
         "  C 类改标 inference 后仍可能触发 inference 相关规则（需 gate 实测，本工具不跑）；",
         "- **覆盖率**：OBSERVATION-LIVENESS 非 poison 攻击面上的攻击类型 ⇒ **诚实覆盖率口径不变**（假设，非实测）；",
         "- A/B 类补的符号须真正出现在引用卡的工件断言中，否则 gate 仍报（本工具按「补对」假设）。", ""]
    return "\n".join(L)


def check(all_r: dict, partial_r: dict) -> list[str]:
    problems: list[str] = []
    if all_r["warn_before"] != 50:
        problems.append(f"当前 OBSERVATION-LIVENESS warn 应为 50（实测 {all_r['warn_before']}）")
    if all_r["warn_after"] != 0:
        problems.append(f"全量补全后 warn 应为 0（实测 {all_r['warn_after']}）")
    if partial_r["addressed"] != 0 and partial_r["warn_after"] != partial_r["warn_before"]:
        problems.append("--partial 0 时 warn 应与基线一致")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="liveness_impact", description="612 B3 活性锚补全 what-if（只读）")
    ap.add_argument("--version", action="version", version=f"liveness_impact {VERSION}")
    ap.add_argument("--partial", type=int, default=0, help="只补前 N 条（按 A→B→C）")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    all_r = analyze(None)
    partial_r = analyze(a.partial)
    if a.stats:
        print(json.dumps({"all": all_r, "partial": partial_r}, ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = check(all_r, partial_r)
        if problems:
            for p in problems:
                print(f"[B3] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[B3] ✓ what-if 锁定（warn {all_r['warn_before']} ⇒ {all_r['warn_after']}；"
              f"partial {partial_r['addressed']} ⇒ {partial_r['warn_after']}）")
        return 0
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(render(all_r, partial_r), encoding="utf-8", newline="\n")
    print(f"[B3] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}（warn {all_r['warn_before']} ⇒ "
          f"{all_r['warn_after']}；partial {partial_r['addressed']} ⇒ {partial_r['warn_after']}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
