#!/usr/bin/env python3
"""613 任务D1 · 桥接边画像 + 提案 + apply（默认 dry-run，人审前不落权威边）。

画像维度（对 98 条候选逐条计算）：
  * 主题（topic）与分量对（components）；
  * 证据重叠：shared_atoms / shared_evidence 是否非空（**非空才是有实据的桥**）；
  * 分量对热度：同一分量对被多少条候选连接（热度高 = 优先修，收益大）；
  * 风险旗标：`NO_SHARED_EVIDENCE`（仅主题匹配，无共享证据/原子）、`SAME_TOPIC_ONLY`。

分级：
  * **A 推荐**：有 shared_evidence 或 shared_atoms（有实据）；
  * **B 需人审**：仅 topic_match（98 条实测**全部**属此档）；
  * **C 暂缓**：既不共享证据也不主题匹配（本批无）。

纪律（沿用 611/612 桥接线口径）：
  * **不写权威边文件** `data/attack_edges_candidates.jsonl`（那是人审权）；
  * `--apply` 只追加到 `data/bridge_edges_applied_613.jsonl`（append-only，可回滚）；
  * 默认 dry-run。

CLI：
  python tools/bridge_edge_proposal_613.py            # 出画像 + 提案（dry-run）
  python tools/bridge_edge_proposal_613.py --apply    # 追加落盘（仍非权威边）
  python tools/bridge_edge_proposal_613.py --check    # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAND = ROOT / "data" / "bridge_edge_candidates_611.jsonl"
APPLIED = ROOT / "data" / "bridge_edges_applied_613.jsonl"
OUT = ROOT / "data" / "bridge_edge_proposal_613.md"
TOP_N = 20


def load_candidates() -> list[dict]:
    if not CAND.is_file():
        return []
    out = []
    for ln in CAND.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln:
            try:
                out.append(json.loads(ln))
            except json.JSONDecodeError:
                pass
    return out


def profile(cands: list[dict]) -> list[dict]:
    pair_hot = Counter(tuple(sorted(c.get("components") or [])) for c in cands)
    rows = []
    for c in cands:
        b = c.get("basis") or {}
        se = b.get("shared_evidence") or []
        sa = b.get("shared_atoms") or []
        comps = tuple(sorted(c.get("components") or []))
        flags = []
        if not se and not sa:
            flags.append("NO_SHARED_EVIDENCE")
        if b.get("topic_match") and not se and not sa:
            flags.append("SAME_TOPIC_ONLY")
        grade = "A" if (se or sa) else ("B" if b.get("topic_match") else "C")
        rows.append({"edge_id": c.get("edge_id"), "source": c.get("source"),
                     "target": c.get("target"), "topic": b.get("topic", ""),
                     "components": list(comps), "priority": c.get("priority"),
                     "direction": c.get("direction"),
                     "n_shared_evidence": len(se), "n_shared_atoms": len(sa),
                     "pair_heat": pair_hot.get(comps, 0), "grade": grade,
                     "flags": flags})
    # 排序：先按分量对热度降序（修一条高热度对收益最大），再按 grade、edge_id
    rows.sort(key=lambda r: (-r["pair_heat"], r["grade"], r["edge_id"] or ""))
    return rows


def render(rows: list[dict]) -> str:
    g = Counter(r["grade"] for r in rows)
    topics = Counter(r["topic"] for r in rows)
    hot = Counter(tuple(r["components"]) for r in rows).most_common(5)
    n_ev = sum(1 for r in rows if r["n_shared_evidence"] or r["n_shared_atoms"])
    L = ["# 613 · 桥接边画像与提案（D1）", "",
         f"> 生成：`python tools/bridge_edge_proposal_613.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         "> 源：`data/bridge_edge_candidates_611.jsonl`（98 条）。**默认 dry-run**；",
         "> `--apply` 只写 `data/bridge_edges_applied_613.jsonl`，**不动权威边文件**。", "",
         "## 一、画像总览", "",
         "| 项 | 值 |", "|---|---|",
         f"| 候选边总数 | {len(rows)} |",
         f"| 有共享证据/原子（A 档） | **{g.get('A', 0)}** |",
         f"| 仅主题匹配（B 档） | **{g.get('B', 0)}** |",
         f"| 两者皆无（C 档） | {g.get('C', 0)} |",
         f"| 带实据（shared_* 非空）条数 | {n_ev} |",
         f"| 主题分布 | {dict(topics)} |", "",
         "## 二、分量对热度 Top5（优先修这些对，单条收益最大）", "",
         "| 分量对 | 候选条数 |", "|---|---|"]
    for pair, n in hot:
        L.append(f"| {list(pair)} | {n} |")
    L += ["", f"## 三、提案清单（前 {TOP_N} 条）", "",
          "| # | edge_id | source → target | 主题 | 分量对 | 热度 | 档 | 旗标 |",
          "|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(rows[:TOP_N], 1):
        L.append(f"| {i} | `{r['edge_id']}` | {r['source']} → {r['target']} | {r['topic']} "
                 f"| {r['components']} | {r['pair_heat']} | {r['grade']} "
                 f"| {'、'.join(r['flags']) or '—'} |")
    L += ["", "## 四、判定与交人", "",
          "- 98 条候选**全部为 weak 优先级、且无共享证据/原子**（仅同主题跨分量）",
          "  ⇒ 机器**无法**断言这些桥接边真实成立，全部需**人审**（方向/是否成立由人裁定）。",
          "- 本工具只做画像与排序，**不代替人审**；`--apply` 也不写权威边文件。"]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 D1 · 桥接边画像/提案/apply")
    ap.add_argument("--apply", action="store_true", help="追加落盘（非权威边）")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    rows = profile(load_candidates())

    if a.check:
        errs = []
        if len(rows) != 98:
            errs.append(f"候选应为 98，实测 {len(rows)}")
        if rows and rows[0]["pair_heat"] < max(r["pair_heat"] for r in rows):
            errs.append("未按热度降序")
        if any(r["grade"] not in ("A", "B", "C") for r in rows):
            errs.append("存在非法档位")
        if rows != profile(load_candidates()):
            errs.append("画像非确定性")
        for e in errs:
            print(f"[D1] ✗ {e}")
        print("[D1] " + ("✅ 自验证通过" if not errs else f"❌ {len(errs)} 项失败"))
        return 0 if not errs else 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(rows), encoding="utf-8", newline="\n")
    print(f"[D1] 写入 {OUT.relative_to(ROOT).as_posix()}（{len(rows)} 条画像）")

    if a.apply:
        existing = set()
        if APPLIED.is_file():
            for ln in APPLIED.read_text(encoding="utf-8").splitlines():
                if ln.strip():
                    try:
                        existing.add(json.loads(ln).get("edge_id"))
                    except json.JSONDecodeError:
                        pass
        new = [r for r in rows if r["edge_id"] not in existing]
        with APPLIED.open("a", encoding="utf-8", newline="\n") as fh:
            for r in new:
                r = dict(r, applied_at=datetime.now().isoformat(timespec="seconds"))
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"[D1] 追加 {len(new)} 条到 {APPLIED.relative_to(ROOT).as_posix()}"
              f"（累计 {len(existing) + len(new)}；**非权威边**）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
