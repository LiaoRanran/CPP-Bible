"""635 1.5 · 种子击败器台账 + taint 标记（只加数据，不改判决）

为**全部 verified 卡**生成 ≥1 条**击败器（defeater）**：
- 类型：`rebutting`（直接反驳）/ `undercutting`（削弱理由）；
- 内容：**什么新证据出现会推翻这条卡**（模板 + 卡内 prop 摘要，非空话）；
- `taint_propagation`：该卡被判错时是否影响下游 ≥3 条卡（按**跨卡引用计数**判定）。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 写 `data/635_defeater_ledger.md`。
纯标准库；≥5 例单测（tests/test_defeater_ledger_635.py）。
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
OUT_MD = os.path.join(ROOT, "data", "635_defeater_ledger.md")
TAINT_THRESHOLD = 3


def _cards() -> list[tuple[str, str, str]]:
    """返回 (rel, id, text) 列表。"""
    out = []
    for r, _d, fs in os.walk(os.path.join(ROOT, "atoms")):
        for f in fs:
            if f.endswith(".md"):
                p = os.path.join(r, f)
                out.append((os.path.relpath(p, ROOT).replace(os.sep, "/"), f[:-3],
                            open(p, encoding="utf-8", errors="replace").read()))
    return out


def verified_cards() -> list[dict[str, str]]:
    return [{"rel": rel, "id": cid, "text": t} for rel, cid, t in _cards()
            if re.search(r"^status:\s*verified", t, re.MULTILINE)]


def first_prop(text: str) -> str:
    m = re.search(r"-\s*id:\s*(prop-\d+)(.*?)(?=\n\s*-\s*id:|\Z)", text, re.DOTALL)
    if not m:
        return ""
    sm = re.search(r"statement:\s*(.+)", m.group(2))
    return (sm.group(1).strip()[:80] if sm else "")


def reference_count(cid: str, all_cards: list[tuple[str, str, str]]) -> int:
    n = 0
    for _rel, other, text in all_cards:
        if other == cid:
            continue
        if re.search(rf"\b{re.escape(cid)}\b", text):
            n += 1
    return n


def defeater_for(card: dict[str, str], refs: int) -> dict[str, Any]:
    stmt = first_prop(card["text"]) or card["id"]
    has_evidence = bool(re.search(r"evidence:\s*\[", card["text"]))
    dtype = "undercutting" if has_evidence else "rebutting"
    if has_evidence:
        content = (f"若「{stmt}」所依赖的实验/产物在新编译器或平台上得到相反观测"
                   "（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。")
    else:
        content = (f"若出现权威标准条文/一手实验直接否定「{stmt}」，则本卡结论被**直接反驳**。")
    return {"card": card["id"], "rel": card["rel"], "type": dtype, "content": content,
            "refs": refs, "taint_propagation": refs >= TAINT_THRESHOLD}


def ledger() -> list[dict[str, Any]]:
    allc = _cards()
    return [defeater_for(c, reference_count(c["id"], allc)) for c in verified_cards()]


def stats() -> dict[str, Any]:
    rows = ledger()
    tainted = [r["card"] for r in rows if r["taint_propagation"]]
    return {"verified_cards": len(rows), "covered": len(rows),
            "coverage_pct": 100.0 if rows else 0.0,
            "taint_true": tainted, "n_taint": len(tainted),
            "by_type": {"rebutting": sum(1 for r in rows if r["type"] == "rebutting"),
                        "undercutting": sum(1 for r in rows if r["type"] == "undercutting")}}


def write_report() -> str:
    rows = ledger()
    s = stats()
    lines = [
        "# 635 1.5 · 种子击败器台账 + taint 标记", "",
        f"- verified 卡：**{s['verified_cards']}**；覆盖率：**{s['coverage_pct']}%**（每卡 ≥1 击败器）",
        f"- 类型分布：{s['by_type']}",
        f"- `taint_propagation=true`（引用于 ≥{TAINT_THRESHOLD} 条下游卡）：**{s['n_taint']}** 张", "",
        "## 一、击败器清单", "",
        "| 卡 | 类型 | taint | 引用数 | 击败器内容 |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| `{r['card']}` | {r['type']} | {str(r['taint_propagation']).lower()} | "
                     f"{r['refs']} | {r['content']} |")
    lines += ["", "## 二、taint=true 高风险卡清单", ""]
    lines += [f"- `{c}`" for c in s["taint_true"]] or ["_无_"]
    lines += ["", "## 诚实登记", "",
              "1. 击败器内容为**模板 + 卡内 prop 摘要**生成（非人工逐条撰写），真实可用但需人审润色；",
              f"2. `taint_propagation` 按**跨卡引用计数 ≥{TAINT_THRESHOLD}** 判定（启发式）；",
              "3. 本工具**只读**，不改任何卡与判决。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    vc = verified_cards()
    chk("verified 卡 ≥1", len(vc) >= 1)
    rows = ledger()
    chk("覆盖率 100%", len(rows) == len(vc) and len(rows) > 0)
    chk("每条有 type + content", all(r["type"] and r["content"] for r in rows))
    chk("type ∈ {rebutting,undercutting}",
        all(r["type"] in ("rebutting", "undercutting") for r in rows))
    chk("taint 为布尔", all(isinstance(r["taint_propagation"], bool) for r in rows))
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="635 1.5 击败器台账")
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
        print(json.dumps(stats(), ensure_ascii=False, indent=2))
        return 0
    print(stats())
    return 0


if __name__ == "__main__":
    sys.exit(main())
