#!/usr/bin/env python3
"""613 任务D3 · 辩护链**深化**：多跳防御深度 + 单点依赖 + 共同依赖（相关失效）风险。

611 的 `defense_chain_deepen.py` 只看了「降级涟漪（demote_ripple）」一步；
本工具在此基础上补充三个**结构性**指标：

  1. **防御深度 depth**：节点 ← 辩护者 ← 辩护者的辩护者 … 的最长链长（环安全、带记忆化）。
     depth=0 表示无辩护者（裸命题，最脆弱）。
  2. **单点依赖 single_point**：辩护者数 == 1 的节点 —— 该唯一辩护者一倒，本节点即失守。
  3. **共同依赖 correlated**：被 ≥N 个节点共同依赖的「承重辩护者」——
     它一倒会引发**相关失效**（多个节点同时失守），是本图最危险的结构。

输入：`data/grounded_labels_w2.json`（nodes：DEFENDERS / ATTACKERS / DEFEATED_ATTACKERS / LABEL）。
输出：`data/defense_chain_deep_613.md`。

CLI：
  python tools/defense_chain_deep_613.py          # 生成报告
  python tools/defense_chain_deep_613.py --check  # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

LABELS = ROOT / "data" / "grounded_labels_w2.json"
OUT = ROOT / "data" / "defense_chain_deep_613.md"
SHARED_MIN = 3


def load_nodes() -> dict[str, dict]:
    g = json.loads(LABELS.read_text(encoding="utf-8"))
    nodes = g.get("nodes", g)
    return {k: v for k, v in nodes.items() if isinstance(v, dict)}


def defenders_of(rec: dict) -> list[str]:
    d = rec.get("DEFENDERS") or rec.get("defenders") or []
    return [x for x in d if isinstance(x, str)]


def compute(nodes: dict[str, dict]) -> dict:
    depth: dict[str, int] = {}
    visiting: set[str] = set()

    def dep(nid: str) -> int:
        if nid in depth:
            return depth[nid]
        if nid in visiting:  # 环：截断，避免无限递归
            return 0
        visiting.add(nid)
        best = 0
        for d in defenders_of(nodes.get(nid, {})):
            if d in nodes:
                best = max(best, 1 + dep(d))
        visiting.discard(nid)
        depth[nid] = best
        return best

    for nid in nodes:
        dep(nid)

    single = [n for n, r in nodes.items() if len(defenders_of(r)) == 1]
    bare = [n for n, r in nodes.items() if not defenders_of(r)]
    load: Counter[str] = Counter()
    for r in nodes.values():
        for d in defenders_of(r):
            load[d] += 1
    shared = {d: c for d, c in load.items() if c >= SHARED_MIN}
    return {"depth": depth, "single_point": sorted(single), "bare": sorted(bare),
            "load": load, "shared": shared,
            "max_depth": max(depth.values()) if depth else 0,
            "n_nodes": len(nodes)}


def render(c: dict) -> str:
    depth_hist = Counter(c["depth"].values())
    top_shared = sorted(c["shared"].items(), key=lambda kv: -kv[1])[:15]
    L = ["# 613 · 辩护链深化报告（D3）", "",
         f"> 生成：`python tools/defense_chain_deep_613.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         "> 输入：`data/grounded_labels_w2.json`；指标＝防御深度 / 单点依赖 / 共同依赖（相关失效）。",
         "", "## 一、总览", "",
         "| 项 | 值 |", "|---|---|",
         f"| 节点总数 | {c['n_nodes']} |",
         f"| **最大防御深度** | **{c['max_depth']}** |",
         f"| 单点依赖节点（辩护者=1） | {len(c['single_point'])} |",
         f"| 裸命题（无辩护者） | {len(c['bare'])} |",
         f"| 承重辩护者（被 ≥{SHARED_MIN} 节点依赖） | {len(c['shared'])} |", "",
         "## 二、防御深度分布", "",
         "| 深度 | 节点数 |", "|---|---|"]
    for d in sorted(depth_hist):
        L.append(f"| {d} | {depth_hist[d]} |")
    L += ["", "## 三、承重辩护者 Top15（相关失效风险源）", "",
          "| 辩护者 | 被依赖次数 |", "|---|---|"]
    if top_shared:
        for d, n in top_shared:
            L.append(f"| `{d}` | {n} |")
    else:
        L.append("| — | — |")
    L += ["", "## 四、单点依赖节点（前 15）", "", "| 节点 | 唯一辩护者 |", "|---|---|"]
    nodes = load_nodes()
    for n in c["single_point"][:15]:
        L.append(f"| `{n}` | `{defenders_of(nodes[n])[0]}` |")
    if not c["single_point"]:
        L.append("| — | — |")
    L += ["", "## 五、读法", "",
          "- **深度 0** = 无辩护者：任何攻击直接奏效，最脆弱。",
          "- **共同依赖**：一个辩护者被多个节点依赖 ⇒ 它失效会**同时**打倒一批（相关失效），"
          "比单点依赖更危险，优先加固。",
          "- 本工具只读，不改动任何权威文件。"]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 D3 · 辩护链深化")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    nodes = load_nodes()
    c = compute(nodes)

    if a.check:
        errs = []
        if c["n_nodes"] != 121:
            errs.append(f"节点数应为 121，实测 {c['n_nodes']}")
        if len(c["depth"]) != c["n_nodes"]:
            errs.append("深度未覆盖全部节点")
        if c["depth"] != compute(load_nodes())["depth"]:
            errs.append("深度计算非确定性")
        if any(v < 0 for v in c["depth"].values()):
            errs.append("出现负深度")
        for e in errs:
            print(f"[D3] ✗ {e}")
        print("[D3] " + ("✅ 自验证通过" if not errs else f"❌ {len(errs)} 项失败"))
        return 0 if not errs else 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(c), encoding="utf-8", newline="\n")
    print(f"[D3] 写入 {OUT.relative_to(ROOT).as_posix()}（节点 {c['n_nodes']} / "
          f"最大深度 {c['max_depth']} / 单点依赖 {len(c['single_point'])} / "
          f"承重 {len(c['shared'])}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
