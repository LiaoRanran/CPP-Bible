#!/usr/bin/env python3
"""615 D3 · 跃迁触发条件**机器判定**（新建工具；**只判定，不自动触发任何跃迁**）。

目标：让系统能自动检测「**门是否在开启**」（不是替人开门）。

判定：
  * 每 KC 状态：`triggered`（掌握度≥0.8 **且** OOD 正确率≥80%）/ `ready`（掌握度≥0.8 但 OOD 未达标）
    / `not_ready`（掌握度<0.8）。
  * 门状态：`triggered` 数 **≥5 ⇒ open**；**≥1 ⇒ opening**；否则 `closed`。
  * 开门数字：**真实学习事件 ≥50** 才谈"门开"（进度 current/50；模拟数据不计入真实事件）。

输入（只读）：`data/learner_state.json`（若不存在，退回 `learner_behaviors.jsonl` 经 BKT 递推）
+ `data/learner_mastery_jumps.jsonl`（OOD 记录）。
CLI：`--check` / `--report` / 默认打印。
铁律：**不自动触发任何跃迁**；不改 `learner_state.json`；不采集真实学习行为。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

STATE_JSON = ROOT / "data" / "learner_state.json"
BEHAVIORS = ROOT / "data" / "learner_behaviors.jsonl"
JUMPS = ROOT / "data" / "learner_mastery_jumps.jsonl"
REPORT = ROOT / "data" / "learner_transition_615.md"

MASTERY_GATE = 0.8
OOD_GATE = 0.8
OPEN_KC = 5
OPENING_KC = 1
OPEN_EVENTS = 50


def _kc_ids() -> list[str]:
    import kc_inventory as d1  # noqa: E402
    return [k["id"] for k in d1.build()["kcs"]]


def load_mastery() -> dict[str, float]:
    """掌握度：优先 learner_state.json；缺失则退回 behaviors 经 BKT 递推。"""
    if STATE_JSON.is_file():
        try:
            d = cast("dict[str, Any]", json.loads(STATE_JSON.read_text(encoding="utf-8")))
            return {str(k): float(v) for k, v in (d.get("mastery") or d).items()
                    if isinstance(v, (int, float))}
        except (ValueError, TypeError):
            pass
    import learner_behavior_logger as b1  # noqa: E402
    return b1.replay(BEHAVIORS)


def load_ood() -> dict[str, float]:
    if not JUMPS.is_file():
        return {}
    out: dict[str, float] = {}
    for ln in JUMPS.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            r = cast("dict[str, Any]", json.loads(ln))
        except ValueError:
            continue
        out[str(r.get("kc_id"))] = float(r.get("ood_score") or 0.0)
    return out


def real_event_count() -> int:
    """真实（非模拟）学习事件数。"""
    if not BEHAVIORS.is_file():
        return 0
    n = 0
    for ln in BEHAVIORS.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            r = cast("dict[str, Any]", json.loads(ln))
        except ValueError:
            continue
        if not r.get("simulated"):
            n += 1
    return n


def status_of(mastery: float, ood: float) -> str:
    if mastery >= MASTERY_GATE and ood >= OOD_GATE:
        return "triggered"
    if mastery >= MASTERY_GATE:
        return "ready"
    return "not_ready"


def gate_status(triggered: int) -> str:
    if triggered >= OPEN_KC:
        return "open"
    if triggered >= OPENING_KC:
        return "opening"
    return "closed"


def detect() -> dict:
    mastery = load_mastery()
    ood = load_ood()
    per: dict[str, dict] = {}
    for kc in _kc_ids():
        m = float(mastery.get(kc, 0.1))
        o = float(ood.get(kc, 0.0))
        per[kc] = {"mastery": round(m, 4), "ood": round(o, 4), "status": status_of(m, o)}
    trig = sum(1 for v in per.values() if v["status"] == "triggered")
    ev = real_event_count()
    return {"kcs": per, "triggered": trig,
            "ready": sum(1 for v in per.values() if v["status"] == "ready"),
            "not_ready": sum(1 for v in per.values() if v["status"] == "not_ready"),
            "gate": gate_status(trig), "real_events": ev, "open_events": OPEN_EVENTS,
            "events_progress": f"{ev}/{OPEN_EVENTS}",
            "events_ready": ev >= OPEN_EVENTS}


def render(d: dict) -> str:
    L = ["# 615 D3 · 跃迁触发条件机器判定（门是否在开启）", "",
         f"> 触发条件：掌握度≥{MASTERY_GATE} **且** OOD≥{OOD_GATE}。**只判定，不自动触发任何跃迁**。", "",
         "## 一、门状态", "",
         f"- **门状态 = `{d['gate']}`**（triggered {d['triggered']} / ready {d['ready']} / "
         f"not_ready {d['not_ready']}）",
         f"- 开门数字：真实学习事件 **{d['events_progress']}**"
         f"（{'✅ 达标' if d['events_ready'] else '未达标'}，模拟数据不计入）", "",
         "## 二、27 KC 跃迁状态", "",
         "| KC | 掌握度 | OOD | 状态 |", "|---|---|---|---|",
         *[f"| `{k}` | {v['mastery']} | {v['ood']} | {v['status']} |" for k, v in d["kcs"].items()],
         "", "## 三、诚实声明", "",
         f"- 当前真实学习事件 = **{d['real_events']}**，门状态 = **`{d['gate']}`**，学习者闭环**尚未开启**。",
         "- 跃迁检测器**只做判定，不自动触发任何跃迁**；开门需真实学习事件 + 人审。", "", ""]
    return "\n".join(L) + "\n"


def check() -> list[str]:
    problems: list[str] = []
    # 判定逻辑（合成）
    if status_of(0.9, 0.9) != "triggered":
        problems.append("≥0.8 且 OOD≥0.8 应 triggered")
    if status_of(0.9, 0.5) != "ready":
        problems.append("≥0.8 但 OOD<0.8 应 ready")
    if status_of(0.5, 0.9) != "not_ready":
        problems.append("<0.8 应 not_ready")
    if gate_status(0) != "closed" or gate_status(1) != "opening" or gate_status(5) != "open":
        problems.append("门状态阈值错误（0=closed/1=opening/5=open）")
    d = detect()
    if len(d["kcs"]) != 27:
        problems.append(f"KC 应 27（实测 {len(d['kcs'])}）")
    if d["triggered"] + d["ready"] + d["not_ready"] != 27:
        problems.append("状态计数不等于 27")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="learner_transition_detector",
                                 description="615 D3 跃迁触发条件机器判定（只判定不触发）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        problems = check()
        if problems:
            for p in problems:
                print(f"[D3] ❌ {p}", file=sys.stderr)
            return 1
        d = detect()
        print(f"[D3] ✅ 自验证通过：门状态 {d['gate']} / 27 KC / 真实事件 {d['real_events']}")
        return 0
    d = detect()
    if a.report:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(render(d), encoding="utf-8", newline="\n")
        print(f"[D3] 已写 {REPORT.relative_to(ROOT).as_posix()}（门 {d['gate']}）")
        return 0
    print(json.dumps({k: v for k, v in d.items() if k != "kcs"}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
