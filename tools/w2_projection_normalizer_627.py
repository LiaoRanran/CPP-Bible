"""627 A1 · W2 投影节点归一化（519 → 121，与 grounded_labels 对齐）

**背景**：626 D1 的 `compile_w2()` 以 **`edge_id`** 为节点 ⇒ 519 节点，
与 `grounded_labels_w2.json` 的 121 节点（`prop_id` + `MIS_id`）粒度不同，无法对比。

**归一化规则（627 实测确立）**：
1. **节点宇宙** = `grounded_labels_w2.json` 的 121 个节点（自带 `credibility`）。
   实测：Authority 的 452 条边事件中 **所有 source 与 target 都落在 121 节点内（0 例外）**
   ⇒ 归一化不产生孤立节点。
2. **边的解析**：`ae-<SRC>-><DST>` ⇒ `(source=SRC, target=DST)`，
   按 `(source, target)` 去重。
3. **生效攻击** = `result ∈ {APPROVE, MODIFY}`。
   🔑 **626 的关键缺陷**：只认 APPROVE。实测 7 个 OUT 的 MIS 节点（cred=1）
   正是被 `result=MODIFY` 的边攻击的 —— 漏掉 MODIFY 就永远算不出 OUT=7。
4. **击败关系**沿用权威 solver：`weighted_af_solver.defeats_of()`
   ⇔ `cred(A) > cred(B)`（**严格大于**）。
5. **标签**：`weighted_af_solver.grounded_labels()` 在击败关系上求最小不动点。

**实测结果**：388 条活跃边 / 17 条击败 ⇒ **IN 114 / OUT 7 / UNDEC 0，与 grounded_labels 逐节点 diff = 0**。

本工具**不修改** 626 的 `authority_projection_compiler_626.py`（627 全部新建）。
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

import decision_event_v2_626 as D  # noqa: E402
import weighted_af_solver as W  # noqa: E402

LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
GROUNDED = os.path.join(ROOT, "data", "grounded_labels_w2.json")
OUT_JSON = os.path.join(ROOT, "data", "w2_projection_normalized_627.json")

ACTIVE_RESULTS = ("APPROVE", "MODIFY")


def load_grounded_nodes() -> dict[str, dict]:
    """121 个基准节点（含 credibility）。"""
    g = json.load(open(GROUNDED, encoding="utf-8"))
    nodes: dict[str, dict] = g["nodes"]
    return nodes


def parse_edge(target_id: str) -> tuple[Optional[str], Optional[str]]:
    """`ae-<SRC>-><DST>` ⇒ (SRC, DST)。"""
    body = target_id[3:] if target_id.startswith("ae-") else target_id
    if "->" not in body:
        return None, None
    src, dst = body.split("->", 1)
    return src, dst


def authority_active_edges(ledger_path: str = LEDGER,
                           active: tuple = ACTIVE_RESULTS) -> list[dict]:
    """从 Authority Ledger 读取**生效攻击边**（去重）。"""
    led = D.AuthorityLedger.import_jsonl(ledger_path)
    seen: set = set()
    out: list[dict] = []
    for e in led.all_events():
        if e.target_type != "edge":
            continue
        if e.result not in active:
            continue
        s, d = parse_edge(e.target_id)
        if not s or not d:
            continue
        if (s, d) in seen:
            continue
        seen.add((s, d))
        out.append({"source": s, "target": d, "id": e.target_id,
                    "direction": "mis_to_prop" if s.startswith("MIS") else "prop_to_mis",
                    "confidence": "medium"})
    return out


def compile_w2(ledger_path: str = LEDGER,
               nodes: Optional[dict] = None) -> dict[str, Any]:
    """归一化后的 W2 投影：121 节点 + grounded 标签。"""
    nodes = nodes if nodes is not None else load_grounded_nodes()
    edges = authority_active_edges(ledger_path)
    defeats = W.defeats_of(edges, nodes)
    labels, rounds = W.grounded_labels(nodes, defeats)
    from collections import Counter
    summary = dict(Counter(labels.values()))
    summary.setdefault("UNDEC", 0)
    return {"nodes": len(nodes), "labels": labels, "summary": summary,
            "active_edges": len(edges), "defeats": len(defeats),
            "rounds": rounds, "node_universe": "grounded_labels_w2.json(121)"}


def summarize(res: dict) -> str:
    s = res["summary"]
    return (f"nodes={res['nodes']} IN={s.get('IN',0)} OUT={s.get('OUT',0)} "
            f"UNDEC={s.get('UNDEC',0)} | active_edges={res['active_edges']} "
            f"defeats={res['defeats']} rounds={res['rounds']}")


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    nodes = load_grounded_nodes()
    chk("基准节点 121", len(nodes) == 121, f"({len(nodes)})")
    edges = authority_active_edges()
    chk("活跃边解析成功", len(edges) > 0, f"({len(edges)})")

    # 归一化：所有 source/target 都在 121 节点内
    outside = [(e["source"], e["target"]) for e in edges
               if e["source"] not in nodes or e["target"] not in nodes]
    chk("无 121 之外的节点（归一化封闭）", not outside, f"({len(outside)})")

    res = compile_w2(nodes=nodes)
    chk("归一化后节点数 = 121", res["nodes"] == 121, f"({res['nodes']})")
    s = res["summary"]
    chk("IN = 114", s.get("IN") == 114, f"({s.get('IN')})")
    chk("OUT = 7", s.get("OUT") == 7, f"({s.get('OUT')})")
    chk("UNDEC = 0", s.get("UNDEC") == 0, f"({s.get('UNDEC')})")

    # 与 grounded_labels 逐节点一致
    expected = {k: v["label"] for k, v in nodes.items()}
    diff = [k for k in expected if res["labels"].get(k) != expected[k]]
    chk("逐节点与 grounded_labels 一致", not diff, f"(diff {len(diff)})")

    # MODIFY 必须计入（626 的缺陷回归）
    led = D.AuthorityLedger.import_jsonl(LEDGER)
    appr = [e for e in led.all_events()
            if e.target_type == "edge" and e.result == "APPROVE"]
    chk("MODIFY 边确实存在（否则 OUT=7 无法得出）",
        any(e.result == "MODIFY" for e in led.all_events()),
        f"(APPROVE {len(appr)})")
    print(f"A1 normalizer check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="627 A1 W2 投影节点归一化")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--json", action="store_true", help="输出归一化投影 JSON")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    res = compile_w2()
    if args.json:
        with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)
        print(f"written {OUT_JSON}")
    print(summarize(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
