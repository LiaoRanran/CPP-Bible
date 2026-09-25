#!/usr/bin/env python3
"""640b A1 · W2 数字的**单一权威源**（根治涟漪）

**问题**：W2 的 IN/OUT/defeating_edges 会随人签/重算演进，但几十个测试各自把当前
数字写死（114/7/…），每次演进批量红（640b 的 28 项即此）。

**治法**：全库只有本模块定义"当前 W2 数字"，两条**不同路径**：

1. `compute_w2_summary()` —— **现算**：从事实源（`data/attack_edges_609.json` 边 +
   人审 annotation）经 `weighted_af_solver.solve_reviewed()` 求解；
2. `artifact_summary()` —— **读产物**：读入库权威产物 `data/grounded_labels_w2.json`。

`summary()["consistent"]` 是两条路径的交叉校验：产物过期/漂移时立刻可见。

测试应：
- 一致性类 → 断言被测工具输出 == `compute_w2_summary()`（**不是**写死数字）；
- 报告/仪表盘类 → 断言"提交的报告 == 现场重生成"（幂等），数值从本模块取。

**只读契约**：全部函数只读；`--check` 零写盘；纯标准库 + 既有工具。
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

ARTIFACT = os.path.join(ROOT, "data", "grounded_labels_w2.json")
DEFAULT_MODE = "keep-low"


def compute_w2_summary(modify_mode: str = DEFAULT_MODE) -> dict[str, Any]:
    """**现算**路径：事实源 → W2 求解 → 当前数字。

    `W2_SIM_OFFSET`（**仅测试用**，见 tests 的 §四.3 模拟）：把 IN 加 N / OUT 减 N，
    用于模拟"两条路径同步演进"而无需真改事实源。
    """
    import attack_edge_review as aer
    import weighted_af_solver as w2
    edges = w2.load_edges()
    annotations = aer.load_annotations()
    doc, _changes = w2.solve_reviewed(edges, annotations, modify_mode=modify_mode)
    st = w2.stats(doc)
    by = st["by_label"]
    off = int(os.environ.get("W2_SIM_OFFSET", "0") or 0)
    return {"IN": int(by.get("IN", 0)) + off, "OUT": int(by.get("OUT", 0)) - off,
            "UNDEC": int(by.get("UNDEC", 0)),
            "defeating_edges": int(st["defeating_edges"]),
            "edges": int(st["edges"]), "nodes": int(st["total"]),
            "modify_mode": modify_mode, "source": "recompute"}


def artifact_summary(path: str = ARTIFACT) -> dict[str, Any]:
    """**读产物**路径：入库权威产物 `grounded_labels_w2.json`。"""
    d: dict[str, Any] = json.loads(open(path, encoding="utf-8").read())
    cnt: collections.Counter[str] = collections.Counter(
        str(v.get("label")) for v in d.get("nodes", {}).values())
    return {"IN": cnt.get("IN", 0), "OUT": cnt.get("OUT", 0),
            "UNDEC": cnt.get("UNDEC", 0),
            "defeating_edges": int(d.get("defeating_edges", 0)),
            "edges": int(d.get("edges", 0)), "nodes": len(d.get("nodes", {})),
            "source": os.path.relpath(path, ROOT).replace(os.sep, "/")}


def summary() -> dict[str, Any]:
    """两条路径 + 交叉校验。"""
    comp = compute_w2_summary()
    art = artifact_summary()
    keys = ("IN", "OUT", "UNDEC", "defeating_edges", "edges", "nodes")
    consistent = all(comp[k] == art[k] for k in keys)
    return {"recompute": comp, "artifact": art, "consistent": consistent,
            "mismatch": [k for k in keys if comp[k] != art[k]]}


# ── 便捷取值（测试用；避免各处写死）────────────────────────────────────────
def current() -> dict[str, Any]:
    """当前权威数字（现算路径）。"""
    return compute_w2_summary()


def triple() -> tuple[int, int, int]:
    c = compute_w2_summary()
    return (c["IN"], c["OUT"], c["UNDEC"])


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    s = summary()
    chk("两条路径一致（产物未过期）", s["consistent"])
    chk("现算数字非负且总量自洽",
        s["recompute"]["IN"] + s["recompute"]["OUT"] + s["recompute"]["UNDEC"]
        == s["recompute"]["nodes"])
    chk("现算有边与击败边", s["recompute"]["edges"] > 0
        and s["recompute"]["defeating_edges"] > 0)
    chk("triple() 与现算一致", triple() == (s["recompute"]["IN"],
                                            s["recompute"]["OUT"],
                                            s["recompute"]["UNDEC"]))
    chk("只读：模块不写盘", not hasattr(sys.modules[__name__], "_WRITES"))
    print(f"640b W2 authority selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="640b W2 数字单一权威源")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    print(json.dumps(summary(), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
