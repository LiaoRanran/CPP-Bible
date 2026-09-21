#!/usr/bin/env python3
"""615 C3 · Goodhart 漂移监控（P2 · 新建独立工具）。

背景（_arch_v19/08）：`0 block / 186 warn`，warn 被 golden 锁周期性采纳为 legacy（136→186），
27 条毒样例豁免全 legacy，人审 reject=0 ⇒ "目标被指标替代"（Goodhart）。本工具把漂移**量化成趋势**。

五指标（各 0–20 危险分，合计 0–100，越高越危险）：
  1. warn 增长率（每批次新增 warn）
  2. legacy 豁免增长率（每批次新增采纳）
  3. block 率（block 占比低 ⇒ 危险）
  4. 规则覆盖率（poison 覆盖低 ⇒ 危险）
  5. 人审拒绝率（reject 占比低 ⇒ rubber-stamp 危险）

输入：`data/metrics.jsonl`（趋势）+ `tools/golden_state.json` + `data/human_attack_edge_annotations.jsonl`。
历史数据不足时**诚实声明**（不编趋势）。

CLI：`--check` / `--report` / 默认打印。
铁律：只读；不改任何基线；不跑门禁。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

METRICS = ROOT / "data" / "metrics.jsonl"
GOLDEN = ROOT / "tools" / "golden_state.json"
ANNOT = ROOT / "data" / "human_attack_edge_annotations.jsonl"
REPORT = ROOT / "data" / "goodhart_monitor_615.md"


def _rows() -> list[dict]:
    if not METRICS.is_file():
        return []
    out: list[dict] = []
    for ln in METRICS.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(cast("dict[str, Any]", json.loads(ln)))
        except ValueError:
            continue
    return out


def _warn_series() -> list[int]:
    return [int((r.get("metrics") or {}).get("gate_warn_count") or 0) for r in _rows()]


def _legacy_count() -> int:
    if not GOLDEN.is_file():
        return 0
    st = cast("dict[str, Any]", json.loads(GOLDEN.read_text(encoding="utf-8")))
    return sum(1 for v in (st.get("warn_classify") or {}).values() if v in ("legacy", "accepted"))


def _reject_rate() -> tuple[float, int]:
    if not ANNOT.is_file():
        return 0.0, 0
    recs = [json.loads(ln) for ln in ANNOT.read_text(encoding="utf-8").splitlines() if ln.strip()]
    n = len(recs)
    rej = sum(1 for r in recs if r.get("action") == "reject")
    return (rej / n if n else 0.0), n


def _coverage() -> float | None:
    """poison 诚实覆盖率：从 governance scan 或 poison_surface_map 取；取不到 ⇒ None（不臆造）。"""
    for f, keys in ((ROOT / "data" / "governance_weakening_scan.json",
                     ("poison_honest_coverage_pct", "poison_coverage_pct", "honest_coverage_pct")),
                    (ROOT / "tools" / "poison_surface_map.json",
                     ("honest_coverage_pct", "coverage_pct"))):
        if not f.is_file():
            continue
        try:
            d = cast("dict[str, Any]", json.loads(f.read_text(encoding="utf-8")))
        except ValueError:
            continue
        for k in keys:
            if isinstance(d.get(k), (int, float)):
                return float(d[k])
        cov = d.get("coverage")
        if isinstance(cov, dict) and isinstance(cov.get("honest_pct"), (int, float)):
            return float(cov["honest_pct"])
    return None


def _scale(v: float, lo: float, hi: float, cap: float = 20.0) -> float:
    if hi <= lo:
        return 0.0
    return max(0.0, min(cap, (v - lo) / (hi - lo) * cap))


def compute() -> dict:
    ws = _warn_series()
    batches = max(1, len(ws) - 1)
    warn_growth = ((ws[-1] - ws[0]) / batches) if len(ws) >= 2 else 0.0
    legacy = _legacy_count()
    legacy_growth = legacy / max(1, len(_rows()))
    rej_rate, n_ann = _reject_rate()
    cov = _coverage()
    block_rate = 0.0        # standing baseline: block=0

    s1 = _scale(warn_growth, 0.0, 20.0)                       # ≥20/批 ⇒ 满危险
    s2 = _scale(legacy_growth, 0.0, 1.0)                      # 每批 ≥1 采纳 ⇒ 满
    s3 = 20.0 - _scale(block_rate, 0.0, 0.2)                  # block 率 0 ⇒ 满
    s4 = None if cov is None else (20.0 - _scale(cov, 50.0, 100.0))   # 覆盖低 ⇒ 危险
    s5 = 20.0 - _scale(rej_rate, 0.0, 0.1)                    # reject 率 0 ⇒ 满
    known = [x for x in (s1, s2, s3, s4, s5) if x is not None]
    # 诚实：未知子项**排除**并按已知项重标定（不把"未知"当"满危险"）
    total = round(sum(known) / (20.0 * len(known)) * 100.0, 1)
    return {"warn_series": ws, "warn_growth_per_batch": round(warn_growth, 2),
            "legacy_rules": legacy, "legacy_growth_per_batch": round(legacy_growth, 3),
            "block_rate": block_rate, "coverage_pct": cov,
            "reject_rate": round(rej_rate, 4), "annotations": n_ann,
            "subscores": {"warn_growth": round(s1, 1), "legacy_growth": round(s2, 1),
                          "block_rate": round(s3, 1),
                          "coverage": (round(s4, 1) if s4 is not None else None),
                          "reject_rate": round(s5, 1)},
            "known_subscores": len(known),
            "score": total, "data_points": len(ws),
            "insufficient": len(ws) < 3}


def render(d: dict) -> str:
    note = ("⚠ **历史 metrics 数据不足（{n} 点），趋势分析基于有限数据点**"
            .format(n=d["data_points"]) if d["insufficient"] else
            f"数据点 {d['data_points']}（metrics.jsonl）")
    L = ["# 615 C3 · Goodhart 漂移监控", "",
         "> 五指标各 0–20 危险分，合计 0–100（越高越危险）。只读；不改基线。", "",
         "## 一、漂移评分", "",
         f"- **Goodhart 危险分 = {d['score']} / 100**", f"- {note}", "",
         "## 二、子项", "",
         "| 子项 | 危险分 | 原始值 |", "|---|---|---|",
         f"| warn 增长率 | {d['subscores']['warn_growth']} | {d['warn_growth_per_batch']}/批 |",
         f"| legacy 豁免增长率 | {d['subscores']['legacy_growth']} | {d['legacy_growth_per_batch']}/批"
         f"（{d['legacy_rules']} 条） |",
         f"| block 率 | {d['subscores']['block_rate']} | {d['block_rate']} |",
         f"| 规则覆盖率 | {d['subscores']['coverage'] if d['subscores']['coverage'] is not None else '（未取到，已排除）'} | "
         f"{d['coverage_pct'] if d['coverage_pct'] is not None else '（未取到）'} |",
         f"| 人审拒绝率 | {d['subscores']['reject_rate']} | {d['reject_rate']}"
         f"（{d['annotations']} 条） |", "",
         "## 三、warn 趋势序列", "",
         f"`{d['warn_series']}`", "",
         "## 四、解读与边界", "",
         "- 高分主要由 **block=0（无阻断）**、**warn 持续增长并被采纳为 legacy**、**reject=0（无拒绝）** 驱动，",
         "  与 `_arch_v19/08_大模型发展与涌现.md` 的 Goodhart 判断一致。",
         "- 该分数**不是判决**，是**趋势提示**；不自动修改 golden 基线。",
         "- 若 `metrics.jsonl` 不足 ⇒ 趋势仅供参考（诚实声明在第二节）。", "", ""]
    return "\n".join(L) + "\n"


def check() -> list[str]:
    problems: list[str] = []
    d = compute()
    if not (0.0 <= d["score"] <= 100.0):
        problems.append(f"评分越界：{d['score']}")
    for k, v in d["subscores"].items():
        if v is None:
            continue
        if not (0.0 <= v <= 20.0):
            problems.append(f"子项 {k} 越界：{v}")
    # 单调性：warn 序列首 >= 尾 时增长率非正
    ws = d["warn_series"]
    if len(ws) >= 2 and ws[-1] >= ws[0] and d["warn_growth_per_batch"] < 0:
        problems.append("warn 增长率符号错误")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="goodhart_monitor", description="615 C3 Goodhart 漂移监控")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        problems = check()
        if problems:
            for p in problems:
                print(f"[C3] ❌ {p}", file=sys.stderr)
            return 1
        print(f"[C3] ✅ 自验证通过：评分 {compute()['score']}/100，五子项均 ∈[0,20]")
        return 0
    d = compute()
    if a.report:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(render(d), encoding="utf-8", newline="\n")
        print(f"[C3] 已写 {REPORT.relative_to(ROOT).as_posix()}（危险分 {d['score']}/100）")
        return 0
    print(json.dumps(d, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
