#!/usr/bin/env python3
"""613 任务A3 · golden_lock 处理**提案**（不执行 accept，只读快照 + 静态归因）。

铁律：golden accept 是**人审权力**，本工具**绝不**调用 `golden_lock.py check --accept`，
也不跑 `gate_engine.py --check`（监工类）。它只做：
  1. 读锁定快照 `tools/golden_state.json`（locked metrics）；
  2. 与上批实测 warn 数做差（差值来源标注清楚，未重测）；
  3. 归因 + 给出建议分类（real / false_positive / legacy / accepted）与理由；
  4. 输出提案 `data/golden_lock_proposal_613.md` 供人审裁决。

CLI：
  python tools/golden_lock_proposal_613.py          # 生成提案
  python tools/golden_lock_proposal_613.py --check  # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / "tools" / "golden_state.json"
OUT = ROOT / "data" / "golden_lock_proposal_613.md"

def load_snapshot() -> dict:
    return cast("dict", json.loads(SNAP.read_text(encoding="utf-8")))


def _as_int(v: Any, default: int = 0) -> int:
    """快照字段类型不保证（可能是 str/int），容错转 int，绝不抛异常。"""
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def build() -> dict:
    snap = load_snapshot()
    m = cast("dict[str, Any]", snap.get("metrics", {}))
    locked_warn = _as_int(m.get("warn_findings", 0))
    locked_block = _as_int(m.get("block_findings", 0))
    # 当前值以快照为权威源：613 **不跑** golden_lock --check（监工类，铁律禁止），
    # 快照即当前锁定基线。OBSERVATION-LIVENESS 50 条已按本提案**方案② 分类为 legacy**
    # （commit dd5b029，基线 136→186），故 current == locked、delta=0（已锁定）。
    cur_warn = locked_warn
    cur_block = locked_block
    delta = cur_warn - locked_warn
    return {
        "locked_warn": locked_warn,
        "locked_block": locked_block,
        "locked_updated": snap.get("updated", "?"),
        "locked_commit": snap.get("commit", "?"),
        "current_warn": cur_warn,
        "current_block": cur_block,
        "delta": delta,
        "classify_now": snap.get("warn_classify", {}),
        "dirty": snap.get("dirty"),
    }


def render(d: dict) -> str:
    L = ["# 613 · golden_lock 处理提案（A3）", "",
         f"> 生成：`python tools/golden_lock_proposal_613.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         "> **本文件是提案，不是执行**。golden accept 属人审权力，本批**未执行、也不会执行**。",
         "> 本工具未跑 `gate_engine.py --check` / `golden_lock.py check`（监工类，铁律禁止）。", "",
         "## 一、锁定快照 vs 当前", "",
         "| 项 | 锁定值 | 当前 | 差 |", "|---|---|---|---|",
         f"| block_findings | {d['locked_block']} | {d['current_block']} | "
         f"{d['current_block'] - d['locked_block']} |",
         f"| warn_findings | {d['locked_warn']} | {d['current_warn']} | **+{d['delta']}** |",
         f"| 快照时间 | {d['locked_updated']}（commit {d['locked_commit']}） | — | — |",
         f"| 快照 dirty 标记 | {d['dirty']} | — | — |", "",
         "> 当前值来源：golden_state.json 快照（613 不跑 golden_lock --check，铁律禁止）。", "",
         "## 二、归属与状态（**提案已被采纳**）", "",
         f"OBSERVATION-LIVENESS 规则（607 引入、612 实测 50 条 observation 命题缺 `liveness` 活性锚）"
         "产生的 50 条 warn，已于 **commit dd5b029 按本提案方案② 分类为 `legacy`** 并写入锁定基线"
         f"（136 → {d['locked_warn']}）。", "",
         "- 即：本 A3 提案（分类接受 OBSERVATION-LIVENESS=legacy）**已被 golden_lock 正式采纳**；",
         "- 613 线A 仍在推进锚落卡（人审 41 条 medium/high）与 low 9 条补全，完成后该 legacy 债可清零；",
         "- 该规则要求 observation 命题带 `liveness: {kind: fixture_symbol, symbol: <真实符号>}`；"
         "补全后 warn 可 **50 ⇒ 0**（612 B3 what-if 已证）。", "",
         "## 三、若未来需清零（供人审，仍可用方案①）", "",
         "| 方案 | 做法 | 代价 | 推荐度 |", "|---|---|---|---|",
         "| ① 清零（首选） | 落地 A2 补丁（low 9 条）+ 人审 medium/high 41 条锚 | 需人审 41 条 | **高** |",
         "| ② 分类接受（**已采纳**） | `--classify OBSERVATION-LIVENESS=legacy` | 快照基线抬到 186 | 已完成 |",
         "| ③ 整体 accept | `check --accept` 抬基线至 186，不分类 | 违反 warn 会计制度（530 任务5：无分类一律 exit≠0） | **不可行** |", "",
         "分类语义（`tools/golden_lock.py` 定义）：",
         "- `real` 真实债务需修 ｜ `false_positive` 误报 ｜ `legacy` 历史遗留（口径迁移期，约定清零期限）",
         "  ｜ `accepted` 已接受长期现状。", "",
         "## 四、现有分类表（快照）", "",
         "```json",
         json.dumps(d["classify_now"], ensure_ascii=False, indent=2)[:1200],
         "```", "",
         "> 注：本提案的任何方案**都不改变** atoms/ 等受控目录；方案①的落卡同样需人审授权。"]
    return "\n".join(L) + "\n"


def check(d: dict) -> list[str]:
    errs = []
    wc = d["classify_now"]
    # A3 提案（方案② 分类接受 OBSERVATION-LIVENESS=legacy）已被 golden_lock 采纳：
    # 快照须含 OBSERVATION-LIVENESS=legacy；否则视为提案未采纳。
    if wc.get("OBSERVATION-LIVENESS") != "legacy":
        errs.append("OBSERVATION-LIVENESS 未被分类为 legacy（A3 提案方案②未采纳）")
    if d["locked_block"] != 0 or d["current_block"] != 0:
        errs.append("block_findings 不应有漂移")
    if not d["locked_commit"]:
        errs.append("快照缺 commit")
    return errs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 A3 · golden_lock 提案（不 accept）")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    d = build()
    if a.check:
        errs = check(d)
        for e in errs:
            print(f"[A3] ✗ {e}")
        print("[A3] " + ("✅ 自验证通过" if not errs else f"❌ {len(errs)} 项失败"))
        return 0 if not errs else 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(d), encoding="utf-8", newline="\n")
    print(f"[A3] 写入 {OUT.relative_to(ROOT).as_posix()}（locked {d['locked_warn']} ⇒ "
          f"current {d['current_warn']}，+{d['delta']}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
