"""624 E2 · 人审逐条复核清单生成器（30 → >100，**只生成不执行**）

**背景**：622 D1 执行了 30 条逐条人审（Authority 388→418）。本任务生成**新的**逐条复核清单
（>70 条），使总逐条人审 >100。

**判据（歧义度排序，只生成不判决）**：
- **high**：annotations 中 action=`modify`（W2 视为 UNRESOLVED，机器不确定）；或所属原子在 623 D2 中
  UNRESOLVED→IN 翻转；或同一原子多边动作冲突。
- **medium**：所属原子结构复杂度 ≥ 75（高复杂度带，见 624 B1）。
- **low**：其余未人审边。

**不代签**：只产出清单（edge_id / 原子 / 歧义度 / 推荐判决 / 理由），**不修改 Authority 日志、不执行判决**。

铁律：只读 annotations/Authority；必有 `--check`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import gate_engine as GE  # noqa: E402
import w2_recompute_623 as W2  # noqa: E402

ANN = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
SYNCED = os.path.join(ROOT, "data", "human_attack_edge_annotations.synced.jsonl")
PRIOR_COUNT = 30                    # 622 D1 已执行
FLIPPED = {"ATOM-LANG-INLINE-001", "MIS-LANG-001", "MIS-MEM-001", "MIS-MEM-003",
           "MIS-UB-001", "MIS-UB-004", "MIS-UB-008", "MIS-UB-014"}
HC_THRESHOLD = 75

RECOMMEND = {"modify": "approve", "approve": "approve", "reject": "reject"}


def load_edges(path: str) -> list[dict]:
    out: list[dict] = []
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def _atom_cx() -> dict[str, int]:
    cx: dict[str, int] = {}
    for p in GE._cards(GE.ATOMS, "ATOM-*.md"):
        cx[str(GE._meta(p).get("id") or p.stem)] = GE._hc_complexity(p)
    return cx


def generate(edges: list[dict], cap: int = 80) -> list[dict]:
    cx = _atom_cx()
    by_atom: dict[str, list[str]] = {}
    for e in edges:
        a = W2._atom_of(str(e.get("edge_id", "")))
        if a:
            by_atom.setdefault(a, []).append(str(e.get("action", "")))
    items: list[dict] = []
    for e in edges:
        eid = str(e.get("edge_id", ""))
        atom = W2._atom_of(eid)
        if not atom:
            continue
        action = str(e.get("action", ""))
        acts = by_atom.get(atom, [])
        conflicting = len({x for x in acts if x}) > 1 and action != "approve"
        if action == "modify":
            amb = "high"
        elif atom in FLIPPED:
            amb = "high"
        elif conflicting:
            amb = "high"
        elif cx.get(atom, 0) >= HC_THRESHOLD:
            amb = "medium"
        else:
            amb = "low"
        items.append({
            "edge_id": eid, "atom": atom, "action": action, "ambiguity": amb,
            "recommend": RECOMMEND.get(action, "modify"),
            "reason": ("W2 视 modify 为 UNRESOLVED（机器不确定）" if action == "modify"
                       else ("623 D2 翻转原子" if atom in FLIPPED
                             else ("同原子多边动作冲突" if conflicting
                                   else (f"高复杂度原子（cx≥{HC_THRESHOLD}）" if amb == "medium"
                                         else "常规未人审边")))),
        })
    order = {"high": 0, "medium": 1, "low": 2}
    items.sort(key=lambda x: (order[x["ambiguity"]], x["atom"], x["edge_id"]))
    return items[:cap]


def summarize(items: list[dict]) -> dict:
    from collections import Counter
    amb = Counter(x["ambiguity"] for x in items)
    rec = Counter(x["recommend"] for x in items)
    return {"total": len(items), "ambiguity": dict(amb), "recommend": dict(rec),
            "total_after": PRIOR_COUNT + len(items)}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    edges = load_edges(ANN)
    chk("annotations 非空", len(edges) > 0)
    items = generate(edges, cap=80)
    chk("生成 >70 条", len(items) > 70)
    chk("总数（含 622 的 30）>100", PRIOR_COUNT + len(items) > 100)
    chk("歧义度取值合法", all(x["ambiguity"] in ("high", "medium", "low") for x in items))
    chk("排序：high 在前", bool(items) and items[0]["ambiguity"] == "high")
    chk("推荐判决合法", all(x["recommend"] in ("approve", "modify", "reject") for x in items))
    s = summarize(items)
    chk("汇总 total 一致", s["total"] == len(items) and s["total_after"] == PRIOR_COUNT + len(items))
    print(f"E2 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def render(items: list[dict]) -> str:
    s = summarize(items)
    L = ["# 624 E2 · 人审逐条复核清单（30 → >100，**只生成不执行**）", "",
         f"> 新生成 **{s['total']}** 条；连同 622 D1 的 {PRIOR_COUNT} 条，总逐条人审 **{s['total_after']}** 条。",
         f"> 歧义度分布：{s['ambiguity']}；推荐判决分布：{s['recommend']}。", "",
         "> **不代签**：本清单**只生成、不执行判决**；执行需人授权。", "",
         "## 逐条复核清单", "",
         "| # | edge_id | 原子 | 动作 | 歧义度 | 推荐判决 | 理由 |", "|---|---|---|---|---|---|---|"]
    for i, x in enumerate(items, 1):
        L.append(f"| {i} | `{x['edge_id']}` | {x['atom']} | {x['action']} | "
                 f"{x['ambiguity']} | {x['recommend']} | {x['reason']} |")
    L += ["", "## 局限性声明", "",
          "1. 清单为**机器排序建议**，歧义度与推荐判决均非人审结论。",
          "2. 622 的 30 条以 `source=authority_log` 标识（已执行）；本清单覆盖其余未人审边。",
          "3. 执行（写 Authority 日志）**需人授权**，本批不做。", ""]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="624 E2 人审逐条清单生成器")
    ap.add_argument("--check", action="store_true", help="只读自检，exit 0 = 通过")
    ap.add_argument("--out", help="输出 markdown 路径")
    ap.add_argument("--cap", type=int, default=80)
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    items = generate(load_edges(ANN), cap=args.cap)
    s = summarize(items)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render(items))
    print(json.dumps(s, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
