"""647 E1–E3 · **打靶准备交付物校验**（调研文档完整性 + 可执行性，只读）。

647 §七 E 线的交付物是**三份文档**（不建卡、不写规则）：
`docs/c_domain_adaptation_647.md`（E1）· `docs/embedded_adaptation_647.md`（E2）·
`docs/targeting_plan_647.md`（E3）。

本工具把它们变成**可机检**的交付物（不是"写了就算"）：

| 检查 | 判据 |
|---|---|
| 文档存在且非空 | 三份都在，且 ≥ 1500 字符 |
| E1 适配点完整 | 含「规则层复用结论」「Domain Pack」「编译器/标准源」「工作量估计」 |
| E2 嵌入式特有问题覆盖 | 含「交叉编译」「资源约束/栈」「实时性/ISR」「编译器扩展」四类 |
| E3 计划可执行 | 含「第一批/第二批」「验收标准」「风险预案」 |
| 工作量可量化 | 三份里都出现"人日"量化的数字 |
| **不越界** | 文档**明确声明本批不建卡**（含"不建卡"或"只调研"字样） |

CLI：`--check` 只读自检 / `--json` / `--report`（写 `data/647_targeting_check.md`）。纯标准库。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

OUT_MD = os.path.join(ROOT, "data", "647_targeting_check.md")

DOCS: dict[str, dict[str, Any]] = {
    "docs/c_domain_adaptation_647.md": {
        "task": "E1 · C 语言适配",
        "sections": ("规则层", "Domain Pack", "编译", "标准", "工作量", "人日"),
    },
    "docs/embedded_adaptation_647.md": {
        "task": "E2 · 嵌入式适配",
        "sections": ("交叉编译", "栈", "实时", "ISR", "attribute", "人日"),
    },
    "docs/targeting_plan_647.md": {
        "task": "E3 · 打靶计划",
        "sections": ("第一批", "第二批", "验收标准", "风险预案", "人日"),
    },
}
#: 三份都必须**明确声明不越界**（只调研不建卡）
BOUNDARY_MARKERS = ("不建卡", "只调研", "不产出任何卡片", "本批不执行")


def check_doc(rel: str, spec: dict[str, Any]) -> dict[str, Any]:
    p = os.path.join(ROOT, rel)
    if not os.path.isfile(p):
        return {"doc": rel, "task": spec["task"], "exists": False, "ok": False,
                "why": "文件不存在"}
    text = open(p, encoding="utf-8").read()
    missing = [s for s in spec["sections"] if s not in text]
    boundary = [m for m in BOUNDARY_MARKERS if m in text]
    return {"doc": rel, "task": spec["task"], "exists": True, "chars": len(text),
            "missing_sections": missing, "boundary_markers": boundary,
            "has_workload": "人日" in text,
            "declares_no_cards": bool(boundary),
            "ok": (len(text) >= 1500 and not missing and bool(boundary))}


def audit() -> dict[str, Any]:
    rows = [check_doc(rel, spec) for rel, spec in DOCS.items()]
    return {"docs": rows, "n": len(rows), "all_ok": all(r["ok"] for r in rows),
            "note": "E 线只交调研文档（不建卡、不写规则、不改代码）"}


def write_report(res: Optional[dict[str, Any]] = None) -> str:
    res = res or audit()
    lines = ["# 647 E 线交付物校验（调研文档）", "",
             f"- 文档数：**{res['n']}**；全部合格：**{res['all_ok']}**", "",
             "| 任务 | 文档 | 字符数 | 缺章节 | 声明不建卡 | 合格 |", "|---|---|---|---|---|---|"]
    for r in res["docs"]:
        lines.append(f"| {r['task']} | `{r['doc']}` | {r.get('chars', 0)} | "
                     f"{r.get('missing_sections') or '—'} | {r.get('declares_no_cards')} | "
                     f"{'✅' if r['ok'] else '❌'} |")
    lines += ["", "## 诚实登记", "",
              "1. **E 线是调研**：本批**不建 C/嵌入式卡片、不写规则、不改代码**（§十二.5）；",
              "2. 校验只查**章节存在性与边界声明**，不判断内容对不对（那要人读）；",
              "3. 工作量是**估计值**，未做试点校准。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    res = audit()
    chk("三份文档都在", all(r["exists"] for r in res["docs"]))
    for r in res["docs"]:
        chk(f"{r['task']} 章节完整", not r.get("missing_sections"), str(r.get("missing_sections")))
        chk(f"{r['task']} 声明不建卡", r.get("declares_no_cards") is True)
        chk(f"{r['task']} 工作量可量化（人日）", r.get("has_workload") is True)
    chk("全部合格", res["all_ok"] is True)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    print(f"E targeting-prep selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 E 线打靶准备交付物校验")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写校验报告")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    res = audit()
    if a.report:
        print(f"written {write_report(res)}")
        return 0 if res["all_ok"] else 1
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    print(f"[647 targeting] 文档 {res['n']} 全部合格={res['all_ok']}")
    return 0 if res["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
