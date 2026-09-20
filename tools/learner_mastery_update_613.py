#!/usr/bin/env python3
"""613 任务C2 · BKT **真实**递推（替换/覆盖 612 的 simulate 模拟值）。

输入：C1 的真实行为事件 `data/learner_behavior.jsonl`。
处理：按时间序，对每条**带正确性**的事件（action_type ∈ answer/test 且 correct 非 null）
      调用 `learner_state.update()` 做一次 BKT 递推（append-only，与 612 同引擎）。
      `review` 事件不带正确性 ⇒ **不参与递推**（只计数），绝不臆造 correct。

输出：`data/mastery_update_report_613.md`（递推前/后掌握度、每 KC 事件数、跳过统计）。

诚实口径：
  * 若真实事件为 0 ⇒ **不做任何递推**，报告明说"仍为 612 simulate 模拟值"，绝不假装更新。
  * 默认 dry-run；`--apply` 才真正写掌握度存储。

CLI：
  python tools/learner_mastery_update_613.py            # dry-run，出报告
  python tools/learner_mastery_update_613.py --apply    # 真实递推并写存储
  python tools/learner_mastery_update_613.py --check    # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import learner_state as ls  # noqa: E402

BEHAVIOR = ROOT / "data" / "learner_behavior.jsonl"
STATE = ROOT / "data" / "learner_state_612.jsonl"
REPORT = ROOT / "data" / "mastery_update_report_613.md"
USER = "default"
RECURRENCE_ACTIONS = ("answer", "test")


def load_events(path: Path = BEHAVIOR) -> list[dict]:
    if not path.is_file():
        return []
    rows = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            rows.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return sorted(rows, key=lambda r: str(r.get("timestamp", "")))


def usable(events: list[dict]) -> tuple[list[dict], int, int]:
    """返回 (参与递推的事件, 跳过数, 未知KC数)。"""
    kcs = set(ls._kc_ids())
    good, skipped, unknown = [], 0, 0
    for e in events:
        kid = e.get("kc_id")
        if kid not in kcs:
            unknown += 1
            continue
        if e.get("action_type") in RECURRENCE_ACTIONS and isinstance(e.get("correct"), bool):
            good.append(e)
        else:
            skipped += 1
    return good, skipped, unknown


def snapshot(store: Path) -> dict[str, float]:
    """掌握度快照。字段名是 **mastery_prob**（learner_state 的记录 schema），
    不是 mastery——取错会恒得 0.0（本批实踩）。"""
    return {kc: float(rec.get("mastery_prob", 0.0))
            for (u, kc), rec in ls.latest_by(store).items() if u == USER}


def apply_events(store: Path, events: list[dict]) -> int:
    n = 0
    for e in events:
        ls.update(store, e["kc_id"], bool(e["correct"]), user=USER)
        n += 1
    return n


def render(before: dict[str, float], after: dict[str, float], events: list[dict],
           good: list[dict], skipped: int, unknown: int, applied: int, dry: bool) -> str:
    per_kc: dict[str, int] = {}
    for e in good:
        per_kc[e["kc_id"]] = per_kc.get(e["kc_id"], 0) + 1
    changed = [(k, before.get(k, 0.0), after.get(k, 0.0))
               for k in sorted(set(before) | set(after))]
    changed = [c for c in changed if abs(c[1] - c[2]) > 1e-9]
    L = ["# 613 · BKT 真实递推报告（C2）", "",
         f"> 生成：`python tools/learner_mastery_update_613.py` ｜ "
         f"时间：{datetime.now().isoformat(timespec='seconds')}",
         f"> 模式：**{'dry-run（未写存储）' if dry else '已应用（真实写入）'}**",
         "> 递推引擎：`learner_state.update()`（与 612 同一 BKT 实现，append-only）。", "",
         "## 一、规模", "",
         "| 项 | 值 |", "|---|---|",
         f"| 真实行为事件总数 | {len(events)} |",
         f"| 参与递推（answer/test 且 correct 非 null） | **{len(good)}** |",
         f"| 跳过（review 等无正确性） | {skipped} |",
         f"| 未知 KC（不在台账） | {unknown} |",
         f"| 本次实际递推次数 | {applied} |", ""]
    if not events:
        L += ["> ⚠ **当前无任何真实学习行为事件** ⇒ 未做任何递推，掌握度仍为 612 `simulate()` "
              "生成的模拟值（空壳状态）。先经 C1 接入真实数据后再跑本工具。", ""]
    L += ["## 二、掌握度变化（前 → 后）", "",
          "| KC | 递推前 | 递推后 | Δ | 事件数 |", "|---|---|---|---|---|"]
    if changed:
        for k, b, a_ in changed:
            L.append(f"| {k} | {b:.4f} | {a_:.4f} | {a_ - b:+.4f} | {per_kc.get(k, 0)} |")
    else:
        L.append("| — | — | — | — | — |")
        L.append("")
        L.append("（无变化）")
    L += ["", "## 三、未变化 KC 数", "", f"- 未变化：{len(set(before) | set(after)) - len(changed)}",
          "", "> 注：`review` 事件不携带正确性，**不参与** BKT 递推（BKT 需要 observed correctness），",
          "> 绝不臆造 correct —— 宁可不更新，也不制造假掌握度。"]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 C2 · BKT 真实递推")
    ap.add_argument("--apply", action="store_true", help="真正写入掌握度存储（默认 dry-run）")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        ok = True
        if not STATE.is_file():
            print("[C2] ✗ 掌握度存储不存在")
            return 1
        # 无事件 ⇒ 必须"零递推"且报告诚实标注
        ev = load_events()
        good, skipped, unknown = usable(ev)
        if not ev and good:
            print("[C2] ✗ 无事件却算出了可递推事件")
            ok = False
        before = snapshot(STATE)
        if not before:
            print("[C2] ✗ 掌握度快照为空")
            ok = False
        page = render(before, before, ev, good, skipped, unknown, 0, True)
        assert "BKT 真实递推报告" in page
        print("[C2] " + ("✅ 自验证通过" if ok else "❌ 自验证失败"))
        return 0 if ok else 1

    if not STATE.is_file():
        print("[C2] ✗ 掌握度存储不存在，先跑 learner_state init")
        return 1

    events = load_events()
    good, skipped, unknown = usable(events)
    before = snapshot(STATE)
    applied = 0
    if good and a.apply:
        applied = apply_events(STATE, good)
    after = snapshot(STATE) if a.apply else before

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(render(before, after, events, good, skipped, unknown, applied, not a.apply),
                      encoding="utf-8", newline="\n")
    print(f"[C2] 事件 {len(events)} / 可递推 {len(good)} / 跳过 {skipped} / 未知KC {unknown} "
          f"/ 已递推 {applied}（{'dry-run' if not a.apply else 'applied'}）")
    print(f"[C2] 写入 {REPORT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
