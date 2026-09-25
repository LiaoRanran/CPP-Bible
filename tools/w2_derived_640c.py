#!/usr/bin/env python3
"""w2_derived_640c.py — **派生量的单一权威源**（640b 的 `w2_authority_640b` 的并列扩展）。

**为什么（640c §三）**：640b 把 W2 的 IN/OUT/defeating_edges 收进了权威源，但
**派生量**（可信度分布 high/medium/low、OUT MIS 数、无辩护者数、连通分量、2-环…）
仍散落在 610/611 的测试与工具里各写一份 ⇒ 人签/重算一变就批量红（640c 的 19 项即此）。

**治法**：全库只有本模块定义"这些派生量当前是多少"，且**两条路径**：

1. `live()` —— **现算**：事实源（边 + 人审 annotation）经 `defense_chain`（610 B1 引擎，
   自身又复用 W2 判决内核）现算；
2. `pinned()` —— **读产物**：入库权威产物 `data/grounded_labels_w2.json`。

`derived()["consistent"]` 是两条路径的交叉校验：产物过期/漂移立刻可见。

**防自我证明（§三.4）——如实标注**：
* `credibility_distribution` / `out_mis` / W2 汇总：**两条独立路径**（现算 vs 磁盘产物），
  断言相等有真实验证力；
* `no_defender_*` / `components` / `cycles` / `high_modify_mis`：产物里**没有**对应字段，
  权威源只能现算 ⇒ 用它做 expected 的断言是**一致性锁（弱验证）**，
  真正的验证力来自各测试里的**夹具测试**（已知输入 → 已知输出，人造图/人造 CRED）。

**只读契约**：全部函数只读；`--check` 零写盘。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import argument_audit as aa  # noqa: E402
import defense_chain as dc  # noqa: E402
import w2_authority_640b as auth  # noqa: E402

VERSION = "1.0"
LABELS = dc.DEFAULT_LABELS
#: 两条路径都能给的键（`mismatch` = 漂移告警）
_KEYS = ("nodes", "in", "out", "undec", "edges", "defeating_edges",
         "credibility_distribution", "out_mis")


# ── 路径 2：读产物 ────────────────────────────────────────────────────────────
def pinned(labels_path: Path | str | None = None) -> dict[str, Any]:
    """读入库权威产物 `data/grounded_labels_w2.json` ⇒ 派生量（磁盘一路）。

    口径**复用** `defense_chain.pinned_summary`（产物侧唯一取数入口），避免两套映射漂移。
    """
    p = Path(labels_path) if labels_path else LABELS
    s = dc.pinned_summary(p)
    return {**{k: s[k] for k in _KEYS if k in s},
            "rounds": s["rounds"],
            "source": os.path.relpath(p, ROOT).replace(os.sep, "/")}


# ── 路径 1：现算 ──────────────────────────────────────────────────────────────
def live(edges_path: Path | str | None = None,
         ann_path: Path | str | None = None) -> dict[str, Any]:
    """事实源 → 610 B1 引擎现算 ⇒ 派生量（同一批口径，**不读产物**）。

    图派生量（无辩护者/分量/2-环）复用 610 的探测器实现（`argument_audit`）——
    **单一实现**，避免两套口径各自漂移；其"弱验证"性质见模块 docstring。
    """
    edges, verdicts, cred = dc.load_data(edges_path, ann_path)
    s = dc.solve_summary(edges, cred)
    nodes = aa.all_nodes(verdicts, edges)
    comps = aa.detect_isolated_subgraphs(edges, nodes)
    sizes = sorted((len(c) for c in comps), reverse=True)
    anns = dc.load_annotations(ann_path)
    high_mod = aa.detect_high_modify_ratio_mis(anns)
    out_mis = [n for n in sorted(verdicts)
               if verdicts[n] == "OUT" and dc.node_type_of(n, edges) == "misconception"]
    return {"nodes": s["nodes"], "in": s["in"], "out": s["out"], "undec": s["undec"],
            "edges": s["edges"], "defeating_edges": s["defeating_edges"],
            "rounds": s["rounds"],
            "credibility_distribution": aa.detect_credibility_gaps(cred)["distribution"],
            "out_mis": len(out_mis),
            "no_defender_mis": aa.detect_no_defender_mis(edges, verdicts, cred),
            "no_defender_nodes": aa.detect_no_defender_nodes(edges, verdicts, cred),
            "no_attacker_propositions": aa.detect_no_attacker_propositions(
                edges, [n for n in verdicts if dc.node_type_of(n, edges) == "proposition"]),
            "components": {"count": len(comps),
                           "isolated": sum(1 for c in comps if len(c) == 1),
                           "largest": sizes[0] if sizes else 0},
            "cycles": len(aa.detect_cycle_arguments(edges)),
            "high_modify_mis": [r["mis_id"] for r in high_mod],
            "unreviewed_edges": len(aa.detect_unreviewed_edges(edges)),
            "source": "recompute（事实源 → defense_chain 610 B1）"}


def derived(edges_path: Path | str | None = None,
            ann_path: Path | str | None = None) -> dict[str, Any]:
    """两条路径 + 交叉校验（`mismatch` 即"漂移告警"）。"""
    lv = live(edges_path, ann_path)
    pn = pinned()
    mismatch = [k for k in _KEYS if lv.get(k) != pn.get(k)]
    return {"live": lv, "pinned": pn, "consistent": not mismatch, "mismatch": mismatch}


# ── 便捷取值（测试/工具用；避免各处写死）───────────────────────────────────────
def w2() -> dict[str, Any]:
    """W2 汇总（委托 640b 的两路权威源；含 IN/OUT/UNDEC/边/击败边））。"""
    return auth.summary()


def credibility_distribution(*, pinned_source: bool = False) -> dict[str, int]:
    """可信度分布。`pinned_source=True` ⇒ 取**入库产物**（独立路径）。"""
    return dict(pinned()["credibility_distribution"] if pinned_source
                else live()["credibility_distribution"])


def out_mis(*, pinned_source: bool = False) -> int:
    """OUT 的 MIS 数。`pinned_source=True` ⇒ 取入库产物。"""
    return int((pinned() if pinned_source else live())["out_mis"])


def out_mis_no_defender() -> list[str]:
    """OUT 且无 W2 辩护者的 MIS（现算）。"""
    return list(live()["no_defender_mis"])


def no_defender_nodes() -> list[str]:
    """W2 辩护者为空的全部节点（现算）。"""
    return list(live()["no_defender_nodes"])


def no_attacker_propositions() -> list[str]:
    """无任何攻击者的命题（现算）。"""
    return list(live()["no_attacker_propositions"])


def components() -> dict[str, int]:
    """连通分量 {count, isolated, largest}（现算）。"""
    return dict(live()["components"])


def cycles() -> int:
    """2-环数（现算）。"""
    return int(live()["cycles"])


def high_modify_mis() -> list[str]:
    """modify 比例 > 0.5 的 MIS（现算）。"""
    return list(live()["high_modify_mis"])


def defeating_edge_count() -> int:
    """击败边数（取 640b 权威源；两路不一致 ⇒ 抛错，避免拿漂移值当预期）。"""
    s = w2()
    if not s["consistent"]:
        raise RuntimeError(f"W2 权威源两路不一致：{s['mismatch']} ⇒ 先查产物/事实源漂移")
    return int(s["recompute"]["defeating_edges"])


# ── 自检 ──────────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}{('：' + extra) if extra and not cond else ''}")
        ok = ok and cond

    d = derived()
    chk("两条路径一致（产物未过期）", d["consistent"], str(d["mismatch"]))
    lv = d["live"]
    chk("可信度分布之和 == 节点数", sum(lv["credibility_distribution"].values()) == lv["nodes"])
    chk("判决之和 == 节点数", lv["in"] + lv["out"] + lv["undec"] == lv["nodes"])
    chk("OUT 无辩护者 MIS ⊆ 无辩护者节点",
        set(lv["no_defender_mis"]) <= set(lv["no_defender_nodes"]))
    chk("连通分量是对节点全集的划分",
        lv["components"]["count"] >= 1 and lv["components"]["isolated"] <= lv["components"]["count"])
    chk("未审边 0（人审完整，结论可用）", lv["unreviewed_edges"] == 0)
    chk("640b 权威源两路一致", w2()["consistent"], str(w2()["mismatch"]))
    print(f"640c W2 derived selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="640c 派生量单一权威源")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    print(json.dumps(derived(), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
