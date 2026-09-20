#!/usr/bin/env python3
"""613 任务D2 · 论证图碎片化报告（**区分"真实现状"与"加桥投影"**）。

核心诚实口径：611/612 的"加桥 11→7、覆盖 66%→80%"是**假设 98 条候选边全部成立**的投影；
而 613 D1 实测这 98 条**无一经过人审、且全为 weak 无实据** ⇒ **当前真实状态并未被修复**。

本工具同时给出三列：
  * 现状（真实）：未加任何桥 ⇒ 分量 11 / 覆盖 66.1% / 孤立 4；
  * 投影（若全部加桥，611 口径）：分量 7 / 覆盖 80.2%；
  * 已生效（实际）：已人审并落权威边的桥接边条数 ⇒ **0**（人审记录为空）。

CLI：
  python tools/argument_fragmentation_613.py          # 生成 data/argument_fragmentation_613.md
  python tools/argument_fragmentation_613.py --check  # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

OUT = ROOT / "data" / "argument_fragmentation_613.md"
REVIEW = ROOT / "data" / "bridge_edge_review_612.jsonl"
APPLIED = ROOT / "data" / "bridge_edges_applied_613.jsonl"


def projection() -> dict:
    """611 口径的加桥投影（假设候选边全部成立）。"""
    import fragmentation_repair_analysis as fra  # noqa: E402
    return fra.analyze()


def effective_edges() -> tuple[int, int]:
    """返回 (已人审桥接边数, 已 apply 但非权威的边数)。"""
    n_rev = 0
    if REVIEW.is_file():
        n_rev = len([ln for ln in REVIEW.read_text(encoding="utf-8").splitlines() if ln.strip()])
    n_app = 0
    if APPLIED.is_file():
        n_app = len([ln for ln in APPLIED.read_text(encoding="utf-8").splitlines() if ln.strip()])
    return n_rev, n_app


def render(p: dict, n_rev: int, n_app: int) -> str:
    L = ["# 613 · 论证图碎片化报告（D2）", "",
         f"> 生成：`python tools/argument_fragmentation_613.py` ｜ "
         f"时间：{datetime.now().isoformat(timespec='seconds')}",
         "> 口径：**现状＝真实**，**投影＝假设**（611 加桥 what-if），**已生效＝实际落权威边数**。", "",
         "## 一、三态对照", "",
         "| 指标 | 现状（真实） | 投影（若 98 条全加） | 已生效 |", "|---|---|---|---|",
         f"| 连通分量 | **{p['components_before']}** | {p['components_after']} | "
         f"{p['components_before']}（人审 0） |",
         f"| 最大分量节点 | {p['largest_before']} | {p['largest_after']} | "
         f"{p['largest_before']} |",
         f"| 覆盖率 | {p['coverage_before'] * 100:.1f}% | {p['coverage_after'] * 100:.1f}% | "
         f"{p['coverage_before'] * 100:.1f}% |",
         f"| 孤立节点 | {p['isolated_before']} | {p['isolated_after']} | "
         f"{p['isolated_before']} |",
         f"| 桥接边 | 0 | {p['candidates_added']} | **{n_rev}** |", "",
         "## 二、为什么「已生效」是 0", "",
         f"- 人审记录 `data/bridge_edge_review_612.jsonl`：**{n_rev} 条**（空）",
         f"- D1 `--apply` 产出（非权威）`data/bridge_edges_applied_613.jsonl`：**{n_app} 条**",
         "- 权威边文件 `data/attack_edges_candidates.jsonl` **未被本批改动**（人审权，不越权）。",
         "- ⇒ 碎片化**当前并未真正改善**；11 分量 / 66.1% 覆盖是真实基线。", "",
         "## 三、修复路径（交人）", "",
         "1. 人审 98 条候选（方向 + 是否真成立），写入人审记录；",
         "2. 人审通过后写权威边文件（**人执行**，本批不代劳）；",
         "3. 重跑本工具 ⇒ 「已生效」列才会向「投影」列靠拢。", "",
         f"> 611 注：{p.get('note', '')}"]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 D2 · 论证图碎片化报告")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    p = projection()
    n_rev, n_app = effective_edges()

    if a.check:
        errs = []
        if p["components_before"] != 11 or p["components_after"] != 7:
            errs.append(f"分量投影异常: {p['components_before']}→{p['components_after']}")
        if p["candidates_added"] != 98:
            errs.append(f"候选边数应为 98，实测 {p['candidates_added']}")
        if n_rev != 0:
            errs.append(f"人审记录应为 0（本批未人审），实测 {n_rev}")
        page = render(p, n_rev, n_app)
        if "碎片化报告" not in page:
            errs.append("报告标题缺失")
        for e in errs:
            print(f"[D2] ✗ {e}")
        print("[D2] " + ("✅ 自验证通过" if not errs else f"❌ {len(errs)} 项失败"))
        return 0 if not errs else 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(p, n_rev, n_app), encoding="utf-8", newline="\n")
    print(f"[D2] 写入 {OUT.relative_to(ROOT).as_posix()}（现状 {p['components_before']} 分量 / "
          f"投影 {p['components_after']} / 已生效 {n_rev} 条）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
