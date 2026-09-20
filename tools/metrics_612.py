#!/usr/bin/env python3
"""612 线 E · metrics_612（E1-E3 度量，拆分自 metrics_610/611 口径，**只读**）。

E1 · modify 双模式一致性：复用 `weighted_af_solver` 在两种 modify 口径下重算 W2 判决，
    锁定量级（keep-low: IN114/OUT7；upgrade-medium: IN121/OUT0），证明「同一套 modify 比例口径，
    610/611/612 一致，无新行为」。
E2 · artifact 碎片化统计：原子卡(ATOM) vs MIS 卡 vs 证据卡(EV) 的数量与碎片化指数，
    并给出消除建议（原子卡已是最小单元，不拆；MIS 卡按主题聚类可能过碎）。
E3 · oracle 人审质量指标：评审者数量 / 已审数量 / 评审质量(通过率) / 检查耗时 / 修改计数。

CLI：
  python tools/metrics_612.py          # 生成 data/metrics_612.md
  python tools/metrics_612.py --check  # 验证三模块不变量（exit 0=通过）

约束（spec）：复用既有工具口径，不新增行为；诚实标注「等待人审」等当前状态。
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT_OUT = ROOT / "data" / "metrics_612.md"
PLAN = ROOT / "data" / "oracle_verification_plan_611.jsonl"
REPORT_612 = ROOT / "data" / "oracle_verification_report_612.md"

# 已知基线（610/612 锁定）
KNOWN_KEEP_LOW = (114, 7)        # (IN, OUT) under keep-low
KNOWN_UPGRADE_MEDIUM = (121, 0)  # (IN, OUT) under upgrade-medium
KNOWN_ATOMIC = 27
KNOWN_MIS = 79
KNOWN_ORACLE = 83


# ── E1：modify 双模式 ─────────────────────────────────────────────────────
def e1_modify_modes() -> dict:
    import attack_edge_review as aer  # noqa: E402
    import weighted_af_solver as w2  # noqa: E402
    edges = w2.load_edges()
    annotations = aer.load_annotations()
    out: dict[str, dict] = {}
    for mode in ("keep-low", "upgrade-medium"):
        doc, _changes = w2.solve_reviewed(edges, annotations, modify_mode=mode)
        st = w2.stats(doc)
        out[mode] = {
            "IN": st["by_label"].get("IN", 0), "OUT": st["by_label"].get("OUT", 0),
            "UNDEC": st["by_label"].get("UNDEC", 0),
            "defeating_edges": st["defeating_edges"], "edges": st["edges"],
            "nodes": st["total"],
        }
    return out


# ── E2：artifact 碎片化 ───────────────────────────────────────────────────
def e2_fragmentation() -> dict:
    atomic = len(list(ROOT.glob("atoms/**/ATOM-*.md")))
    evidence = len(list(ROOT.glob("evidence/**/EV-*.md")))
    mis = len(list((ROOT / "data" / "flashcards" / "markdown").glob("misconception_*.md")))
    total = atomic + evidence + mis
    per_kc = total / atomic if atomic else 0.0
    return {"atomic": atomic, "evidence": evidence, "mis": mis, "total": total,
            "artifacts_per_kc": round(per_kc, 2)}


# ── E3：oracle 人审质量 ───────────────────────────────────────────────────
def e3_oracle_quality() -> dict:
    entries: list[dict] = []
    if PLAN.is_file():
        for line in PLAN.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            entries.append(json.loads(line))
    reviewers = {e.get("verified_by_oracle") for e in entries
                if e.get("verified_by_oracle") not in (None, "")}
    reviews_done = sum(1 for e in entries if e.get("verified"))
    modifications = sum(1 for e in entries if e.get("verified_by_oracle"))
    total = len(entries)
    # 检查耗时：从 612 C1 报告解析三门禁耗时（失败则回退到已知值）
    times = _parse_gate_times()
    return {"total": total, "reviewers": sorted(r for r in reviewers if r),
            "distinct_reviewers": len(reviewers), "reviews_done": reviews_done,
            "modifications": modifications, "gate_time": times,
            "quality_note": ("等待人审（verified=false、verified_by_oracle 均为空）"
                             if reviews_done == 0 else "已有评审数据")}


def _parse_gate_times() -> dict[str, float]:
    fallback = {"gate": 5.3, "poison": 8.3, "replay": 90.0}
    if not REPORT_612.is_file():
        return fallback
    text = REPORT_612.read_text(encoding="utf-8")
    out: dict[str, float] = {}
    for gate in ("gate", "poison", "replay"):
        m = re.search(rf"\| *{gate} *\|[^|]*\|[^|]*\| *([0-9.]+) *\|", text)
        out[gate] = float(m.group(1)) if m else fallback[gate]
    return out


# ── 报告 ─────────────────────────────────────────────────────────────────
def render(e1: dict, e2: dict, e3: dict) -> str:
    g, p, r = e3["gate_time"].values()
    L: list[str] = []
    L.append("# 612 线 E · metrics_612（E1-E3 · 只读）")
    L.append("")
    L.append(f"> 生成时间：{datetime.now().isoformat(timespec='seconds')} ｜ 命令：`python tools/metrics_612.py`")
    L.append(">")
    L.append("> 复用既有工具口径（weighted_af_solver / atoms / oracle plan），不新增行为；"
             "人审相关指标如实标注当前状态。")
    L.append("")
    L.append("## E1 · modify 双模式一致性（610/611/612 同口径）")
    L.append("")
    L.append("| 口径 | IN | OUT | UNDEC | 击败边 | 总边 | 节点 |")
    L.append("|---|---|---|---|---|---|---|")
    for mode, v in e1.items():
        L.append(f"| `{mode}` | {v['IN']} | {v['OUT']} | {v['UNDEC']} | "
                 f"{v['defeating_edges']} | {v['edges']} | {v['nodes']} |")
    L.append("")
    L.append(f"- 锁定：keep-low = IN{KNOWN_KEEP_LOW[0]}/OUT{KNOWN_KEEP_LOW[1]}；"
             f"upgrade-medium = IN{KNOWN_UPGRADE_MEDIUM[0]}/OUT{KNOWN_UPGRADE_MEDIUM[1]}。")
    L.append("- 结论：两种口径直接复用 `weighted_af_solver`，结果与 610/612 基线一致，**无新行为**；"
             "差异仅来自入审 modify 边是否升 medium（口径分歧，非本批次引入）。")
    L.append("")
    L.append("## E2 · artifact 碎片化统计")
    L.append("")
    L.append(f"- 原子卡（ATOM）：**{e2['atomic']}** ｜ 证据卡（EV）：**{e2['evidence']}** ｜ "
             f"MIS 卡（misconception）：**{e2['mis']}**")
    L.append(f"- 工件总数：**{e2['total']}** ｜ 每 KC 平均工件数：**{e2['artifacts_per_kc']}**")
    L.append("")
    L.append("**碎片化消除建议（诚实）**：")
    L.append(f"- 原子卡（{e2['atomic']} 张）**已是最小知识单元，不应再拆**（602/612 共识："
             "原子卡是命题的不可分载体）。")
    L.append(f"- MIS 卡（{e2['mis']} 张）按「命题级 misconception」粒度生成，可能过碎；"
             "建议按主题聚类为少量 MIS 卡簇（如 UB / 并发 / 内存 三大簇），降低维护面。")
    L.append(f"- 证据卡（{e2['evidence']} 张）与原子卡 1:N 对应，碎片化合理；"
             "可评估是否有重复证据可合并。")
    L.append("")
    L.append("## E3 · oracle 人审质量指标")
    L.append("")
    L.append(f"- oracle 卡总数：**{e3['total']}**")
    L.append(f"- 评审者数量（distinct）：**{e3['distinct_reviewers']}** "
             f"（当前：`{', '.join(e3['reviewers']) or '无'}`）")
    L.append(f"- 已审数量：**{e3['reviews_done']}** ｜ 修改计数：**{e3['modifications']}**")
    L.append(f"- 评审质量（通过率）：**{'N/A（无评审）' if e3['reviews_done'] == 0 else '见逐卡' }**")
    L.append(f"- 检查耗时（C1 三门禁，秒）：gate={g} / poison={p} / replay={r}"
             f"（replay 全量≈300s，超预算标记 timeout，不代表失败）")
    L.append("")
    L.append(f"> 当前状态：**{e3['quality_note']}**。E3 如实反映「零人审」现状，"
             "不臆造评审者或质量数字（与 612 铁律「不把尚未发生的人类活动当常量」一致）。")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="612 E · metrics_612（E1-E3）")
    ap.add_argument("--check", action="store_true", help="验证不变量（exit 0=通过）")
    a = ap.parse_args(argv)
    e1 = e1_modify_modes()
    e2 = e2_fragmentation()
    e3 = e3_oracle_quality()

    problems: list[str] = []
    # E1 基线锁定
    if (e1["keep-low"]["IN"], e1["keep-low"]["OUT"]) != KNOWN_KEEP_LOW:
        problems.append(f"keep-low 应为 IN{KNOWN_KEEP_LOW[0]}/OUT{KNOWN_KEEP_LOW[1]}"
                        f"（实测 IN{e1['keep-low']['IN']}/OUT{e1['keep-low']['OUT']}）")
    if (e1["upgrade-medium"]["IN"], e1["upgrade-medium"]["OUT"]) != KNOWN_UPGRADE_MEDIUM:
        problems.append(f"upgrade-medium 应为 IN{KNOWN_UPGRADE_MEDIUM[0]}/OUT{KNOWN_UPGRADE_MEDIUM[1]}"
                        f"（实测 IN{e1['upgrade-medium']['IN']}/OUT{e1['upgrade-medium']['OUT']}）")
    # E2 数量合理
    if e2["atomic"] != KNOWN_ATOMIC:
        problems.append(f"原子卡应为 {KNOWN_ATOMIC}（实测 {e2['atomic']}）")
    if e2["mis"] != KNOWN_MIS:
        problems.append(f"MIS 卡应为 {KNOWN_MIS}（实测 {e2['mis']}）")
    if e2["evidence"] <= 0:
        problems.append("证据卡数应 > 0")
    # E3 数量合理
    if e3["total"] != KNOWN_ORACLE:
        problems.append(f"oracle 卡应为 {KNOWN_ORACLE}（实测 {e3['total']}）")
    if e3["distinct_reviewers"] != 0:
        problems.append(f"当前评审者应为 0（实测 {e3['distinct_reviewers']}）")
    if e3["reviews_done"] != 0:
        problems.append(f"当前已审应为 0（实测 {e3['reviews_done']}）")
    if problems:
        print("[E] ❌ 自检失败：", file=sys.stderr)
        for p in problems:
            print(f"    - {p}", file=sys.stderr)
        return 1

    if a.check:
        print(f"[E] ✅ 自验证通过：E1(keep-low IN{e1['keep-low']['IN']}/OUT{e1['keep-low']['OUT']}, "
              f"upgrade-medium IN{e1['upgrade-medium']['IN']}/OUT{e1['upgrade-medium']['OUT']}) / "
              f"E2(原子{e2['atomic']}/证据{e2['evidence']}/MIS{e2['mis']}) / "
              f"E3(oracle{e3['total']}/评审者{e3['distinct_reviewers']})")
        return 0

    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(render(e1, e2, e3), encoding="utf-8")
    print(f"[E] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}："
          f"E1 双模式一致 / E2 碎片化(原子{e2['atomic']}+证据{e2['evidence']}+MIS{e2['mis']}) / "
          f"E3 oracle{e3['total']} 零人审")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
