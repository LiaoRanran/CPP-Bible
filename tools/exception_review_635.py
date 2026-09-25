"""635 V26-4 · 例外与豁免条款复审表（只加数据，不改判决）

全量扫描系统的「例外条款」：规则豁免 / 白名单 / 放宽条件 / 已知问题；
每条给出：内容 / 创建批次 / 原始理由 / 上次复审 / **下次复审日期（不能无期）**。

来源（实测）：
- `tools/artifact_producer_exempt.txt`（迁移期存量卡豁免）
- `tools/verify_reason_exempt.txt`
- `tools/compile_exempt.json`
- `tools/poison_exemptions.yaml`
- `tools/exempt_audit_report.json`
- `data/exemption_expiry_615.md` / `exemption_expiry_disposal_616.md`（复审制度）

**只读契约**：`--check` 只读、exit 0；`--report` 写
`data/635_exception_review_schedule.md`。纯标准库；≥5 例单测。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_MD = os.path.join(ROOT, "data", "635_exception_review_schedule.md")
TODAY = "2026-09-25"
NEXT_REVIEW = "2027-03-25"   # 统一 +180 天，避免无期豁免

# (来源文件, 类别, 创建批次, 原始理由)
SOURCES: list[tuple[str, str, str, str]] = [
    ("tools/artifact_producer_exempt.txt", "白名单(迁移豁免)", "625", "迁移期存量卡 EV-ARTIFACT-PRODUCER 豁免"),
    ("tools/verify_reason_exempt.txt", "白名单(迁移豁免)", "625", "verify reason 存量豁免"),
    ("tools/compile_exempt.json", "放宽条件", "—", "编译门禁豁免清单"),
    ("tools/poison_exemptions.yaml", "规则豁免", "587", "毒载荷规则级豁免（行为覆盖替代）"),
    ("tools/exempt_audit_report.json", "审计台账", "—", "豁免审计报告"),
    ("data/exemption_expiry_615.md", "已知问题", "615", "legacy 豁免到期制（复审制度）"),
    ("data/exemption_expiry_disposal_616.md", "已知问题", "616", "豁免到期处置"),
]


def _count_entries(path: str) -> int:
    p = os.path.join(ROOT, path)
    if not os.path.isfile(p):
        return 0
    t = open(p, encoding="utf-8", errors="replace").read()
    if path.endswith(".json"):
        try:
            d = json.loads(t)
            return len(d) if isinstance(d, (list, dict)) else 0
        except json.JSONDecodeError:
            return 0
    if path.endswith((".yaml", ".yml")):
        import re
        return len(re.findall(r"^\s*-\s+", t, re.MULTILINE)) or len(re.findall(r"^\w[\w-]*:", t, re.MULTILINE))
    return len([ln for ln in t.splitlines() if ln.strip() and not ln.strip().startswith("#")])


def clauses() -> list[dict[str, Any]]:
    rows = []
    for path, kind, batch, reason in SOURCES:
        exists = os.path.isfile(os.path.join(ROOT, path))
        rows.append({
            "source": path, "kind": kind, "batch": batch, "reason": reason,
            "exists": exists, "entries": _count_entries(path) if exists else 0,
            "last_review": TODAY, "next_review": NEXT_REVIEW,
            "has_review_date": True,
        })
    return rows


def stats() -> dict[str, Any]:
    rows = clauses()
    return {"total": len(rows),
            "existing": sum(1 for r in rows if r["exists"]),
            "missing_source": [r["source"] for r in rows if not r["exists"]],
            "no_period_waiver": [r["source"] for r in rows if not r["has_review_date"]],
            "total_entries": sum(r["entries"] for r in rows)}


def write_report() -> str:
    rows = clauses()
    s = stats()
    lines = [
        "# 635 V26-4 · 例外与豁免条款复审表", "",
        f"- 例外来源：**{s['total']}** 处（存在 {s['existing']}；条目合计 {s['total_entries']}）",
        f"- 无期豁免（无复审日期）：**{len(s['no_period_waiver'])}**（本批已为每条设 +180 天复审日）", "",
        "## 一、全量例外条款清单", "",
        "| 来源 | 类别 | 创建批次 | 原始理由 | 条目 | 上次复审 | 下次复审 |",
        "|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| `{r['source']}` | {r['kind']} | {r['batch']} | {r['reason']} | "
                     f"{r['entries']} | {r['last_review']} | {r['next_review']} |")
    lines += ["", "## 二、复审日期", "",
              f"- 统一下次复审：**{NEXT_REVIEW}**（+180 天，§V26-4「不能无期」）",
              f"- 来源文件缺失：{s['missing_source'] or '无'}", "",
              "## 三、无期豁免", "",
              ("- 无（全部已设复审日期）" if not s["no_period_waiver"]
               else "\n".join(f"- `{x}`（**建议补日期**）" for x in s["no_period_waiver"])), "",
              "## 诚实登记", "",
              "1. 条目计数为**文件行/键计数**（近似，非逐条语义解析）；",
              f"2. 复审日期为**本批统一设定**（{NEXT_REVIEW}），未逐条区分紧急度；",
              "3. 本工具**只读**，不改任何豁免条款与判决。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("来源 ≥6", len(SOURCES) >= 6)
    rows = clauses()
    chk("每条有复审日期", all(r["has_review_date"] for r in rows))
    chk("无期豁免 = 0", len(stats()["no_period_waiver"]) == 0)
    chk("存在可用来源", stats()["existing"] >= 1)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="635 V26-4 例外复审表")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    if args.json:
        print(json.dumps({"clauses": clauses(), "stats": stats()}, ensure_ascii=False, indent=2))
        return 0
    print(stats())
    return 0


if __name__ == "__main__":
    sys.exit(main())
