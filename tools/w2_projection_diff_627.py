"""627 A1 · W2 投影逐节点差异对比（V2 归一化投影 vs grounded_labels）

对比 `w2_projection_normalizer_627.compile_w2()` 的输出与 `grounded_labels_w2.json`
的**逐节点**标签，输出差异报告（哪些节点状态不同 + 差异原因归类）。

差异原因归类：
- `missing_from_authority`：grounded_labels 有攻击者，但 Authority 无对应生效边
- `extra_in_authority`：Authority 有生效边，但 grounded_labels 未记录该攻击者
- `credibility_flattened`：双方都有边，但 Authority 侧可信度不足以构成击败
- `unknown`：其他

`--check`：归一化后节点数 = 121 且 IN/OUT 分布与 grounded_labels 一致。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import w2_projection_normalizer_627 as N  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "w2_projection_diff_627.md")


def diff(ledger_path: str = N.LEDGER) -> dict[str, Any]:
    nodes = N.load_grounded_nodes()
    res = N.compile_w2(ledger_path, nodes=nodes)
    got = res["labels"]
    expected = {k: v["label"] for k, v in nodes.items()}

    edges = N.authority_active_edges(ledger_path)
    auth_atk: dict[str, set] = {}
    for e in edges:
        auth_atk.setdefault(e["target"], set()).add(e["source"])
    gl_atk = {k: set(v.get("attackers") or []) for k, v in nodes.items()}

    rows: list[dict] = []
    for k in sorted(expected):
        if got.get(k) == expected[k]:
            continue
        a, g = auth_atk.get(k, set()), gl_atk.get(k, set())
        if g and not a:
            cause = "missing_from_authority"
        elif a and not g:
            cause = "extra_in_authority"
        elif a != g:
            cause = "attacker_set_mismatch"
        else:
            cause = "credibility_flattened"
        rows.append({"node": k, "projected": got.get(k), "expected": expected[k],
                     "cause": cause, "auth_attackers": sorted(a),
                     "gl_attackers": sorted(g)})
    return {"nodes": len(nodes),
            "projected_summary": res["summary"],
            "expected_summary": dict(Counter(expected.values())),
            "diff_count": len(rows), "rows": rows,
            "active_edges": res["active_edges"], "defeats": res["defeats"],
            "cause_breakdown": dict(Counter(r["cause"] for r in rows))}


def render(d: dict) -> str:
    L = ["# 627 A1 · W2 投影归一化逐节点差异报告", "",
         "| 项 | 值 |", "|---|---|",
         f"| 节点数 | {d['nodes']} |",
         f"| 投影结果 | `{d['projected_summary']}` |",
         f"| grounded_labels | `{d['expected_summary']}` |",
         f"| **差异节点数** | **{d['diff_count']}** |",
         f"| 活跃边 / 击败 | {d['active_edges']} / {d['defeats']} |", ""]
    if d["rows"]:
        L += ["| 节点 | 投影 | 期望 | 原因 |", "|---|---|---|---|"]
        for r in d["rows"][:50]:
            L.append(f"| `{r['node']}` | {r['projected']} | {r['expected']} | {r['cause']} |")
    else:
        L += ["✅ **逐节点完全一致（diff = 0）**"]
    return "\n".join(L) + "\n"


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    d = diff()
    chk("节点数 121", d["nodes"] == 121, f"({d['nodes']})")
    chk("投影 IN = 114", d["projected_summary"].get("IN") == 114)
    chk("投影 OUT = 7", d["projected_summary"].get("OUT") == 7)
    chk("期望 IN = 114", d["expected_summary"].get("IN") == 114)
    chk("期望 OUT = 7", d["expected_summary"].get("OUT") == 7)
    chk("逐节点 diff = 0", d["diff_count"] == 0, f"({d['diff_count']})")
    chk("差异原因可归类", isinstance(d["cause_breakdown"], dict))
    # diff 函数在有差异时能正确归类（用空 ledger 制造差异）
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "empty.jsonl")
        open(p, "w").close()
        d2 = diff(p)
    chk("空 ledger 时产生差异且可归类",
        d2["diff_count"] > 0 and all(r["cause"] for r in d2["rows"]),
        f"(diff {d2['diff_count']})")
    print(f"A1 diff check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="627 A1 W2 投影逐节点差异对比")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--report", action="store_true", help="输出差异报告 MD")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    d = diff()
    if args.report:
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render(d))
        print(f"written {OUT_MD}")
    print(json.dumps({k: v for k, v in d.items() if k != "rows"},
                     ensure_ascii=False, indent=2))
    return 0 if d["diff_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
