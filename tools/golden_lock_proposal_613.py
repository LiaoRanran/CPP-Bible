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

# 上批（612 C1 oracle_verifier）实测的 gate 命中分布；**613 未重测**（铁律：不跑监工 --check）
CURRENT = {"block": 0, "warn": 186, "advice": 5, "source": "612 C1 oracle_verifier 实测，613 未重测"}


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
    locked = cast("dict[str, Any]", snap.get("metrics", {}))
    locked_warn = _as_int(locked.get("warn_findings", 0))
    cur_warn = _as_int(CURRENT["warn"])
    delta = cur_warn - locked_warn
    return {
        "locked_warn": locked_warn,
        "locked_block": _as_int(locked.get("block_findings", 0)),
        "locked_updated": snap.get("updated", "?"),
        "locked_commit": snap.get("commit", "?"),
        "current_warn": cur_warn,
        "current_block": CURRENT["block"],
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
         f"> 当前值来源：{CURRENT['source']}。", "",
         "## 二、归因", "",
         f"warn +{d['delta']} **全部来自 `OBSERVATION-LIVENESS` 规则**（607 引入、612 实测 50 条 "
         "observation 命题缺 `liveness` 活性锚）。", "",
         "- 该规则要求 observation 命题带 `liveness: {kind: fixture_symbol, symbol: <真实符号>}`；",
         "- 50 条命题当前均无锚 ⇒ 规则按设计报 warn（**不是回归、不是误报**，是规则上线后的中间态）；",
         "- 612 B3 what-if 已证明：补全后 warn **50 ⇒ 0**（可清零）。", "",
         "## 三、建议（供人审裁决，三选一）", "",
         "| 方案 | 做法 | 代价 | 推荐度 |", "|---|---|---|---|",
         "| ① 清零（首选） | 落地 A2 补丁（low 9 条）+ 人审 medium/high 41 条锚 | 需人审 41 条 | **高** |",
         "| ② 分类接受（过渡） | `--classify OBSERVATION-LIVENESS=legacy`，约定清零期限 | 快照基线抬到 186 | 中 |",
         "| ③ 整体 accept | `check --accept` 抬基线至 186，不分类 | 违反 warn 会计制度（530 任务5：无分类一律 exit≠0） | **不可行** |", "",
         "## 四、若采纳方案②，建议命令（**人执行**）", "",
         "```bash",
         "python tools/golden_lock.py check --accept \\",
         "    \"613：OBSERVATION-LIVENESS 50 条为 607 规则上线后的活性锚中间态，非回归；",
         "     612 B3 已证补全后 50⇒0，约定 613 线A 完成（含人审 41 条）后清零\" \\",
         "    --classify \"OBSERVATION-LIVENESS=legacy\"",
         "```", "",
         "分类语义（`tools/golden_lock.py` 定义）：",
         "- `real` 真实债务需修 ｜ `false_positive` 误报 ｜ `legacy` 历史遗留（口径迁移期，约定清零期限）",
         "  ｜ `accepted` 已接受长期现状。", "",
         "## 五、现有分类表（快照）", "",
         "```json",
         json.dumps(d["classify_now"], ensure_ascii=False, indent=2)[:1200],
         "```", "",
         "> 注：本提案的任何方案**都不改变** atoms/ 等受控目录；方案①的落卡同样需人审授权。"]
    return "\n".join(L) + "\n"


def check(d: dict) -> list[str]:
    errs = []
    if d["locked_warn"] != 136:
        errs.append(f"锁定 warn 应为 136，实测 {d['locked_warn']}")
    if d["delta"] != 50:
        errs.append(f"warn 增量应归因 50（OBSERVATION-LIVENESS），实测 {d['delta']}")
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
