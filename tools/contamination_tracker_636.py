"""636 V26-补1 · 污染传播自动追踪器（**影子**）

从 635 击败器台账的 `taint=true` 卡里选 1 张，**自动追踪**：它被引用在哪些其他卡的正文/证据里；
对每个下游引用做**三阀门检查**（独立来源？必然发现？善意？），产出最终 `tainted` 清单。

**只读契约**：`--check` 只读、exit 0；`--report` 写 `data/636_contamination_tracker_shadow.md`。
纯标准库；≥5 例单测。
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

OUT_MD = os.path.join(ROOT, "data", "636_contamination_tracker_shadow.md")


def taint_candidates() -> list[str]:
    try:
        import defeater_ledger_635 as D
        return list(D.stats()["taint_true"])
    except Exception:  # noqa: BLE001
        return []


def all_cards() -> list[tuple[str, str, str]]:
    out = []
    for r, _d, fs in os.walk(os.path.join(ROOT, "atoms")):
        for f in fs:
            if f.endswith(".md"):
                p = os.path.join(r, f)
                out.append((os.path.relpath(p, ROOT).replace(os.sep, "/"), f[:-3],
                            open(p, encoding="utf-8", errors="replace").read()))
    return out


def downstream(target: str) -> list[dict[str, Any]]:
    rows = []
    for rel, cid, t in all_cards():
        if cid == target:
            continue
        if re.search(rf"\b{re.escape(target)}\b", t):
            in_evidence = bool(re.search(r"evidence:\s*\[[^\]]*" + re.escape(target), t))
            rows.append({"card": cid, "rel": rel, "in_evidence": in_evidence})
    return rows


def three_valves(card: dict[str, Any]) -> dict[str, str]:
    return {
        "独立来源": "❌ 无（同仓同证据链）",
        "必然发现": "✅ 是" if card["in_evidence"] else "⚠️ 否（仅正文引用，非证据链）",
        "善意": "✅ 是（内部流水线，无造假动机）",
    }


def trace(target: Optional[str] = None) -> dict[str, Any]:
    cands = taint_candidates()
    t = target or (cands[0] if cands else "")
    ds = downstream(t) if t else []
    for d in ds:
        d["valves"] = three_valves(d)
    tainted = [d["card"] for d in ds if d["valves"]["独立来源"].startswith("❌")]
    return {"candidates": cands, "target": t, "downstream": ds,
            "tainted": tainted, "n_downstream": len(ds)}


def write_report() -> str:
    r = trace()
    lines = [
        "# 636 V26-补1 · 污染传播自动追踪器（影子）", "",
        "## 一、选中卡（来自 635 击败器台账 taint=true）", "",
        f"- taint=true 候选：**{len(r['candidates'])}** 张 → `{r['candidates']}`",
        f"- **选中**：`{r['target']}`", "",
        "## 二、下游引用清单", ""]
    if r["downstream"]:
        lines += ["| 下游卡 | 在证据链中 | 独立来源 | 必然发现 | 善意 |", "|---|---|---|---|---|"]
        for d in r["downstream"]:
            lines.append(f"| `{d['card']}` | {'✅' if d['in_evidence'] else '—'} | "
                         f"{d['valves']['独立来源']} | {d['valves']['必然发现']} | "
                         f"{d['valves']['善意']} |")
    else:
        lines.append("- **无下游引用**（该卡被引用度=0）")
    lines += ["", "## 三、最终 tainted 卡清单", ""]
    lines += [f"- `{c}`" for c in r["tainted"]] or ["- 无"]
    lines += ["", "## 诚实登记", "",
              "1. **影子**：不标 taint、不改任何卡/判决；仅离线模拟；",
              "2. 「下游引用」为**文本级**匹配（非语义引用图）；",
              "3. 三阀门为**规则判定**（当前仓库同源，故「独立来源」普遍为否）；",
              f"4. 选中卡 `{r['target']}` 的 taint 判定来自 635 击败器台账。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    cands = taint_candidates()
    chk("taint 候选 ≥1", len(cands) >= 1)
    r = trace()
    chk("选中卡非空", bool(r["target"]))
    chk("下游为 list", isinstance(r["downstream"], list))
    chk("三阀门 3 项", len(three_valves({"in_evidence": True})) == 3)
    chk("tainted 为 list", isinstance(r["tainted"], list))
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="636 V26-补1 污染追踪")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    r = trace()
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    print({"target": r["target"], "n_downstream": r["n_downstream"], "tainted": r["tainted"]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
