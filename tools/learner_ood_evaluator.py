#!/usr/bin/env python3
"""614 线B B3：学习效果验证（OOD 题测试 + 跃迁触发条件）。

OOD（Out-of-Distribution）题：不在 Examples/ 中的新题，测试**迁移能力**（脱离例题后能否独立运用）。
跃迁触发条件（_arch_v18 调研定义）：用户完成一个 KC 的学习（掌握度 ≥ 0.8）→ 做 OOD 题 →
  正确率 ≥ 80% ⇒ 判定「跃迁」（mastery jump）。

OOD 题库：内置 EXAMPLE 题库（每 KC 1 道示例题，source=generated，由 atomic 卡 title 模板生成；
  **结构性示例，需人手工精修**——本批只建框架，不做全量手搓）。
记录：data/learner_mastery_jumps.jsonl（append-only：{user,kc,jump_time,pre_mastery,ood_score,post_mastery,verdict}）。

CLI：
  bank      [--kc <id>]                         # 查看 OOD 示例题
  evaluate  --kc <id> --ood-score <0-1> [--user default]   # 跃迁判定（读 B1 行为日志掌握度）
  stats     [--kc <id>]                          # 跃迁统计
  --check                                      # 自验证（exit 0=通过）

铁律：记录 append-only，不可篡改；单用户 default；模拟数据标注 simulated（仅影响统计口径）。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

DEFAULT_JUMPS = ROOT / "data" / "learner_mastery_jumps.jsonl"
USER = "default"
JUMP_MASTERY = 0.8
JUMP_OOD = 0.8


def _kc_list() -> list[dict]:
    import kc_inventory as d1  # noqa: E402
    return cast("list[dict[str, Any]]", cast("dict[str, Any]", d1.build())["kcs"])


def example_bank() -> list[dict]:
    """内置 EXAMPLE OOD 题库：每 KC 1 道结构性示例题（生成式模板，需人精修）。"""
    out: list[dict] = []
    for k in _kc_list():
        kid = k["id"]
        title = k.get("title", kid)
        out.append({
            "kc_id": kid,
            "question": (f"脱离 Examples/ 中的现成例题，独立说明：{title}。"
                         f"请用自己的话重述该结论，并指出一个反例或边界情形。"),
            "answer": (f"应覆盖：{title}（见原子卡 {kid}）；并能举出至少 1 个反例/边界，"
                       f"证明不是死记硬背。"),
            "difficulty": k.get("difficulty", 2),
            "source": "generated",
        })
    return out


def bank(kc: str | None = None) -> list[dict]:
    b = example_bank()
    return [q for q in b if q["kc_id"] == kc] if kc else b


def load_jumps(store: Path) -> list[dict]:
    if not store.is_file():
        return []
    out: list[dict] = []
    for line in store.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(cast("dict[str, Any]", json.loads(line)))
    return out


def evaluate(learner_store: Path, jumps_store: Path, kc: str, ood_score: float,
             user: str = USER) -> dict:
    import learner_behavior_logger as b1  # noqa: E402
    mastery = b1.replay(learner_store, user)
    pre = mastery.get(kc, 0.1)
    jumped = (pre >= JUMP_MASTERY) and (ood_score >= JUMP_OOD)
    verdict = "jump" if jumped else "no_jump"
    rec = {"user_id": user, "kc_id": kc, "jump_time": _now(), "pre_mastery": round(pre, 4),
           "ood_score": round(float(ood_score), 4), "post_mastery": round(pre, 4),
           "verdict": verdict}
    if jumped:
        jumps_store.parent.mkdir(parents=True, exist_ok=True)
        with jumps_store.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def stats(jumps_store: Path, kc: str | None = None) -> dict:
    recs = load_jumps(jumps_store)
    if kc:
        recs = [r for r in recs if r.get("kc_id") == kc]
    jumps = sum(1 for r in recs if r.get("verdict") == "jump")
    return {"total_records": len(recs), "jumps": jumps,
            "kc_filter": kc, "users": sorted({r.get("user_id") for r in recs})}


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def check(learner_store: Path, jumps_store: Path) -> list[str]:
    problems: list[str] = []
    # 1) 至少 5 个 KC 有示例 OOD 题
    if len(bank()) < 5:
        problems.append("示例 OOD 题库应覆盖 ≥5 KC")
    # 2) 跃迁判定逻辑
    import tempfile

    import learner_behavior_logger as b1  # noqa: E402
    with tempfile.TemporaryDirectory() as td:
        lstore = Path(td) / "beh.jsonl"
        jstore = Path(td) / "jumps.jsonl"
        # 把一个 KC 推到 ≥0.8
        kc = b1._kc_ids()[0]
        for _ in range(10):
            b1.record(lstore, USER, kc, "correct", "exercise", None, False)
        ok_jump = evaluate(lstore, jstore, kc, 0.9)
        if ok_jump["verdict"] != "jump":
            problems.append("掌握度≥0.8 且 OOD≥0.8 应判跃迁")
        no_jump = evaluate(lstore, jstore, kc, 0.5)
        if no_jump["verdict"] != "no_jump":
            problems.append("OOD<0.8 不应判跃迁")
        # 掌握度不足也应 no_jump
        kc2 = b1._kc_ids()[1]
        low = evaluate(lstore, jstore, kc2, 1.0)
        if low["verdict"] != "no_jump":
            problems.append("掌握度<0.8 不应判跃迁")
        # 3) append-only：记录应可累积
        if len(load_jumps(jstore)) != 1:  # 只有第一次 jump 写入
            problems.append("跃迁记录应 append-only（仅 jump 写入）")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="614 B3 OOD 效果验证 + 跃迁判定")
    ap.add_argument("command", nargs="?", default="stats",
                    choices=["bank", "evaluate", "stats"], help="子命令（默认 stats）")
    ap.add_argument("--kc", default=None)
    ap.add_argument("--ood-score", type=float, default=None)
    ap.add_argument("--user", default=USER)
    ap.add_argument("--learner-store", default=None, help="B1 行为日志（默认同 B1）")
    ap.add_argument("--jumps-store", default=None)
    ap.add_argument("--check", action="store_true", help="自验证（exit 0=通过）")
    a = ap.parse_args(argv)
    learner_store = Path(a.learner_store) if a.learner_store else None
    jumps_store = Path(a.jumps_store) if a.jumps_store else DEFAULT_JUMPS
    if learner_store is None:
        import learner_behavior_logger as b1  # noqa: E402
        learner_store = b1.DEFAULT_STORE

    if a.check:
        if learner_store is None:
            learner_store = Path(__file__).resolve().parent.parent / "data" / "learner_behaviors.jsonl"
        problems = check(learner_store, jumps_store)
        if problems:
            print("[ood] ❌ 自检失败：", file=sys.stderr)
            for p in problems:
                print(f"    - {p}", file=sys.stderr)
            return 1
        print("[ood] ✅ 自验证通过：题库≥5KC / 跃迁判定 / append-only 均一致")
        return 0

    cmd = a.command
    if cmd == "bank":
        qs = bank(a.kc)
        print(json.dumps(qs, ensure_ascii=False, indent=1))
        return 0
    if cmd == "evaluate":
        if not a.kc or a.ood_score is None:
            print("[ood] ❌ evaluate 需要 --kc 与 --ood-score", file=sys.stderr)
            return 2
        rec = evaluate(learner_store, jumps_store, a.kc, a.ood_score, a.user)
        print(json.dumps(rec, ensure_ascii=False, indent=1))
        return 0
    # stats
    print(json.dumps(stats(jumps_store, a.kc), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
