"""631 D2 · 探针 #1：向量 **L1.2 命题多义指代**（P0，此前无探针）

向量定义（629 B1）：命题含模糊指代（「它」「该值」）⇒ 复核者各自解读不同。

本探针只做一件事：**扫描原子卡的命题，把"含模糊指代"的命题找出来并计数**
（不判定命题对错、不改卡）。它是 L1.2 的**存在性测量**：
「有多少命题可能被多义解读」，为后续人工消歧提供清单。

**只读**：`--check` 不写盘；`--report` 只写 `data/coverage_probe_l1_2_631.md`。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "coverage_probe_l1_2_631.md")
OUT_JSON = os.path.join(ROOT, "data", "coverage_probe_l1_2_631.json")

# 模糊指代：代词/指示词 + 无先行词的"该/此 + 类指名词"
AMBIGUOUS_TERMS = (
    "它", "它们", "他", "她", "该值", "该对象", "该指针", "该引用", "该变量",
    "该操作", "该行为", "该函数", "该类型", "该表达式", "此值", "此对象",
    "上述", "前者", "后者", "同样", "以此类推",
)
# 排除："其它"（不是指代）
NEGATIVE = re.compile(r"其它|其他")

AMBIG_RE = re.compile("|".join(re.escape(t) for t in AMBIGUOUS_TERMS))


def _ge():
    import gate_engine

    return gate_engine


def scan_text(text: str) -> list[str]:
    """返回文本里命中的模糊指代词（去重、保序；排除"其它/其他"）。"""
    hits = []
    for m in AMBIG_RE.finditer(text or ""):
        term = m.group(0)
        s = max(0, m.start() - 1)
        if NEGATIVE.search((text or "")[s:m.end() + 1]):
            continue
        if term not in hits:
            hits.append(term)
    return hits


def scan_props(card_text: str) -> list[dict[str, Any]]:
    """扫一张卡里每条命题的 subject/predicate/object/statement 字段。"""
    import yaml

    head = card_text.split("\n---", 1)[0].replace("---\n", "", 1)
    try:
        fm = yaml.safe_load(head) or {}
    except Exception:                                          # noqa: BLE001
        return []
    out = []
    for p in (fm.get("claim_structured") or []):
        if not isinstance(p, dict):
            continue
        joined = " ".join(str(p.get(k, "")) for k in
                          ("subject", "predicate", "object", "statement"))
        hits = scan_text(joined)
        if hits:
            out.append({"prop_id": p.get("id"), "hits": hits,
                        "object": str(p.get("object", ""))[:40]})
    return out


def measure() -> dict[str, Any]:
    cards = []
    for base, _d, files in os.walk(os.path.join(ROOT, "atoms")):
        for f in sorted(files):
            if f.endswith(".md"):
                cards.append(os.path.join(base, f))
    rows = []
    for p in sorted(cards):
        text = open(p, encoding="utf-8", errors="replace").read()
        props = scan_props(text)
        if props:
            rows.append({"card": os.path.relpath(p, ROOT).replace(os.sep, "/"),
                         "props": props})
    total_hits = sum(len(list(pr["hits"])) for r in rows
                     for pr in r["props"])
    return {"vector": "L1.2", "name": "命题多义指代",
            "cards_scanned": len(cards), "cards_hit": len(rows),
            "props_hit": sum(len(r["props"]) for r in rows),
            "hits_total": total_hits, "rows": rows}


def write_report() -> str:
    m = measure()
    lines = [
        "# 631 D2 · 探针 #1：L1.2 命题多义指代", "",
        f"- 扫描原子卡：**{m['cards_scanned']}** 张；命中卡 **{m['cards_hit']}** 张",
        f"- 命中命题 **{m['props_hit']}** 条 · 指代命中 **{m['hits_total']}** 处",
        "", "| # | 卡 | 命题 | 命中的模糊词 | object 片段 |", "|---|---|---|---|---|",
    ]
    i = 0
    for r in m["rows"]:
        for pr in r["props"]:
            i += 1
            lines.append(f"| {i} | `{r['card']}` | {pr['prop_id']} | "
                         f"{'、'.join(pr['hits'])} | {pr['object']} |")
    if not m["rows"]:
        lines.append("| — | （无命中） | | | |")
    lines += [
        "", "## 诚实登记", "",
        "1. **这是关键词启发式**：能抓「它 / 该值 / 前者 / 后者」这类显式指代，"
        "抓不到「省略主语」或「跨句指代」等隐性多义 ⇒ 命中数是**下界**；",
        "2. 命中 ≠ 命题错：只是「存在被多义解读的可能」，需人复核（列后续交人）；",
        "3. 本探针**只测存在性**，不做消歧、不改卡（`--check` 只读）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("检测器：显式指代能抓到", scan_text("返回它的值") == ["它"])
    chk("检测器：不误报『其它/其他』", scan_text("其它情况") == [])
    chk("检测器：多个词去重保序",
        scan_text("该值 与 它 和 该值") == ["该值", "它"])
    m = measure()
    chk("扫描了原子卡", m["cards_scanned"] > 0, f"({m['cards_scanned']})")
    chk("统计自洽", m["props_hit"] == sum(len(r["props"]) for r in m["rows"]))

    import subprocess

    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                           capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    measure()
    chk("只读：--check 路径不写盘", snap() == before)
    chk("报告存在", os.path.exists(OUT_MD))
    print(f"D2 probe L1.2 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="631 D2 探针 L1.2 命题多义指代")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写探针报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    m = measure()
    if args.json:
        print(json.dumps(m, ensure_ascii=False, indent=2))
        return 0
    print(f"cards={m['cards_scanned']} hit_cards={m['cards_hit']} "
          f"props={m['props_hit']} hits={m['hits_total']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
