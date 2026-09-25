"""635 1.4 · 术语接地盘点 + 担保类型映射（只加数据，不改判决）

对 67 条 gate 规则逐条盘「术语接地状态」+「证据担保类型」：
- 接地状态：已接地 / 部分接地 / 未接地
- 担保类型（参照 FRE 803 例外逻辑）：即时性（直接实验）/ 系统性（标准·cppreference）/
  常规性（常见实践）/ 权威性（人审·外部审核）

**分类口径（启发式，已登记）**：
- `scope == evidence` ⇒ **已接地 / 即时性**（直接作用于产物/实验证据）；
- `kind ∈ {pedagogy, meta}` ⇒ **未接地 / 权威性**（教学/元规则无外部实验对应）；
- `scope == atom` ⇒ **部分接地 / 系统性**（概念/标准语义）；
- `scope == repo` ⇒ **部分接地 / 常规性**（仓库约定）。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 写
`data/635_grounding_inventory.md`。纯标准库；≥5 例单测（tests/test_grounding_inventory_635.py）。
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

OUT_MD = os.path.join(ROOT, "data", "635_grounding_inventory.md")


def get_rules() -> list[dict[str, str]]:
    try:
        import gate_engine as ge
        return [{"id": r.id, "title": getattr(r, "title", ""), "kind": getattr(r, "kind", ""),
                 "scope": getattr(r, "scope", ""), "basis": getattr(r, "basis", "")}
                for r in ge.RULES]
    except Exception:  # noqa: BLE001
        return []


def classify(rule: dict[str, str]) -> tuple[str, str]:
    scope, kind = rule.get("scope", ""), rule.get("kind", "")
    if scope == "evidence":
        return ("已接地", "即时性")
    if kind in ("pedagogy", "meta"):
        return ("未接地", "权威性")
    if scope == "atom":
        return ("部分接地", "系统性")
    if scope == "repo":
        return ("部分接地", "常规性")
    return ("未接地", "权威性")


def inventory() -> list[dict[str, str]]:
    out = []
    for r in get_rules():
        g, a = classify(r)
        out.append({**r, "grounding": g, "assurance": a})
    return out


def stats() -> dict[str, Any]:
    inv = inventory()
    g: dict[str, int] = {}
    a: dict[str, int] = {}
    for r in inv:
        g[r["grounding"]] = g.get(r["grounding"], 0) + 1
        a[r["assurance"]] = a.get(r["assurance"], 0) + 1
    n = len(inv) or 1
    return {"total": len(inv), "grounding": g, "assurance": a,
            "grounded_pct": round(100.0 * g.get("已接地", 0) / n, 1),
            "ungrounded": [r["id"] for r in inv if r["grounding"] == "未接地"]}


def write_report() -> str:
    inv = inventory()
    s = stats()
    lines = [
        "# 635 1.4 · 术语接地盘点 + 担保类型映射", "",
        f"- 规则数：**{s['total']}**",
        f"- 接地状态分布：`{s['grounding']}`（已接地 {s['grounded_pct']}%）",
        f"- 担保类型分布：`{s['assurance']}`", "",
        "## 一、逐条规则盘点", "",
        "| 规则 | 标题 | scope | kind | 接地状态 | 担保类型 |", "|---|---|---|---|---|---|"]
    for r in inv:
        lines.append(f"| `{r['id']}` | {r['title']} | {r['scope']} | {r['kind']} | "
                     f"{r['grounding']} | {r['assurance']} |")
    lines += ["", "## 二、接地覆盖率", "",
              f"- 已接地 **{s['grounding'].get('已接地', 0)}/{s['total']} = {s['grounded_pct']}%**",
              f"- 部分接地 **{s['grounding'].get('部分接地', 0)}**",
              f"- 未接地 **{s['grounding'].get('未接地', 0)}**", "",
              "## 三、未接地清单（优先级排序：教学/元规则优先补实验）", ""]
    for r in inv:
        if r["grounding"] == "未接地":
            lines.append(f"- `{r['id']}`（{r['title']}，kind={r['kind']}）")
    lines += ["", "## 诚实登记", "",
              "1. 分类为**启发式**（按 scope/kind），非人工逐条判定术语级接地；",
              "2. 「未接地」= kind ∈ {pedagogy, meta}（教学/元规则，无外部实验对应）；"
              "「部分接地」= atom/repo 结构规则（有规范/约定对应但无直接实验）；",
              "3. 本工具**只读**，不改任何规则。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("get_rules = 67", len(get_rules()) == 67)
    chk("evidence → 已接地/即时性", classify({"scope": "evidence", "kind": "fact"}) == ("已接地", "即时性"))
    chk("pedagogy → 未接地/权威性", classify({"scope": "atom", "kind": "pedagogy"}) == ("未接地", "权威性"))
    chk("atom → 部分接地/系统性", classify({"scope": "atom", "kind": "fact"}) == ("部分接地", "系统性"))
    chk("inventory 67 条", len(inventory()) == 67)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="635 1.4 术语接地盘点")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    s = stats()
    if args.json:
        print(json.dumps(s, ensure_ascii=False, indent=2))
        return 0
    print(s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
