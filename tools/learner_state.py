#!/usr/bin/env python3
"""612 线 D · D3：用户掌握度数据结构 + 存储（**append-only** + BKT 递推 + 模拟数据）。

掌握度状态（每个 (user_id, kc_id) 一条最新记录）：
  * user_id：默认 `default`（单用户场景）
  * kc_id：KC ID（对应原子卡 ID）
  * mastery_prob：当前掌握概率（0-1）
  * last_updated：最后更新时间
  * correct：本次作答是否答对（仅 update 记录有；init 记录无）

存储：`data/learner_state_612.jsonl`（**只追加不修改**；最新状态 = 同一 (user,kc) 的最后一条记录）。
每次 `update` 基于 BKT 递推（复用 `bkt_solver.BKTModel`）从「上一条掌握度」算出新掌握度再追加。

CLI：
  python tools/learner_state.py init [--initial-prob 0.1]          # 为缺失的 KC 补 init 记录（P(L0)）
  python tools/learner_state.py update --kc <kc_id> --correct 0|1  # 追加一条 update 记录
  python tools/learner_state.py query [--kc <kc_id>]               # 查当前掌握度
  python tools/learner_state.py stats                              # 平均掌握度/已掌握数/总练习数
  python tools/learner_state.py simulate --sessions <N> [--seed S] # 模拟 N 会话演示数据（标注模拟）
  python tools/learner_state.py --check                            # 验证存储与 BKT 递推一致

约束（spec）：只追加，不修改已有记录；不调用 LLM；单用户 user_id 固定 `default`；
模拟数据明确标注「模拟，非真实用户数据」。

用法备注：KC 清单来自 `kc_inventory.build()`（27 张原子卡），只读、不依赖其写盘。
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STORE = ROOT / "data" / "learner_state_612.jsonl"
DEFAULT_USER = "default"
DEFAULT_L0 = 0.1

_KC_CACHE: list[str] | None = None


def _kc_ids() -> list[str]:
    global _KC_CACHE
    if _KC_CACHE is None:
        import kc_inventory as d1  # noqa: E402  （延迟导入，避免循环/重导入开销）
        _KC_CACHE = [k["id"] for k in d1.build()["kcs"]]
    return _KC_CACHE


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def load_all(store: Path) -> list[dict]:
    if not store.is_file():
        return []
    out: list[dict] = []
    for line in store.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        out.append(json.loads(line))
    return out


def latest_by(store: Path) -> dict[tuple[str, str], dict]:
    latest: dict[tuple[str, str], dict] = {}
    for r in load_all(store):
        latest[(r["user_id"], r["kc_id"])] = r
    return latest


def init(store: Path, initial_prob: float = DEFAULT_L0, user: str = DEFAULT_USER) -> int:
    existing = {(r["user_id"], r["kc_id"]) for r in load_all(store)}
    n_added = 0
    store.parent.mkdir(parents=True, exist_ok=True)
    with store.open("a", encoding="utf-8") as fh:
        for kc in _kc_ids():
            if (user, kc) in existing:
                continue
            rec = {"user_id": user, "kc_id": kc, "mastery_prob": initial_prob,
                   "correct": None, "kind": "init", "timestamp": _now(), "simulated": False}
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n_added += 1
    print(f"[D3] init：新增 {n_added} 条 init 记录（P(L0)={initial_prob}）；"
          f"已存在则跳过（append-only）。")
    return n_added


def update(store: Path, kc_id: str, correct: bool, user: str = DEFAULT_USER) -> dict:
    import bkt_solver as d2  # noqa: E402
    model = d2.BKTModel()
    cur = latest_by(store).get((user, kc_id))
    prev = cur["mastery_prob"] if cur else DEFAULT_L0
    new_prob = model.step(prev, 1 if correct else 0)
    rec = {"user_id": user, "kc_id": kc_id, "mastery_prob": new_prob,
           "correct": bool(correct), "kind": "update", "timestamp": _now(), "simulated": False}
    store.parent.mkdir(parents=True, exist_ok=True)
    with store.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"[D3] update {kc_id}：{prev:.4f} --{'+' if correct else '-'}--> {new_prob:.4f}")
    return rec


def query(store: Path, kc_id: str | None = None, user: str = DEFAULT_USER) -> list[dict]:
    latest = latest_by(store)
    if kc_id:
        rec = latest.get((user, kc_id))
        return [rec] if rec else []
    return [latest[k] for k in sorted(latest) if k[0] == user]


def stats(store: Path, user: str = DEFAULT_USER) -> dict:
    recs = query(store, user=user)
    if not recs:
        return {"user": user, "kc_count": 0, "avg_mastery": 0.0, "mastered": 0,
                "total_updates": 0}
    avg = sum(r["mastery_prob"] for r in recs) / len(recs)
    mastered = sum(1 for r in recs if r["mastery_prob"] >= 0.9)
    total_updates = sum(1 for r in load_all(store) if r.get("kind") == "update" and r["user_id"] == user)
    return {"user": user, "kc_count": len(recs), "avg_mastery": round(avg, 4),
            "mastered": mastered, "total_updates": total_updates}


def simulate(store: Path, sessions: int, seed: int = 1234, user: str = DEFAULT_USER) -> int:
    import bkt_solver as d2  # noqa: E402
    rng = random.Random(seed)
    model = d2.BKTModel()
    kcs = _kc_ids()
    latest = latest_by(store)
    n = 0
    store.parent.mkdir(parents=True, exist_ok=True)
    with store.open("a", encoding="utf-8") as fh:
        for _ in range(sessions):
            kc = rng.choice(kcs)
            cur = latest.get((user, kc))
            prev = cur["mastery_prob"] if cur else DEFAULT_L0
            # 真实掌握度决定答对概率（演示用）：以当前掌握度预测答对
            p_cor = model.predict_correct(prev)
            correct = rng.random() < p_cor
            new_prob = model.step(prev, 1 if correct else 0)
            rec = {"user_id": user, "kc_id": kc, "mastery_prob": new_prob,
                   "correct": bool(correct), "kind": "update", "timestamp": _now(),
                   "simulated": True}
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            latest[(user, kc)] = rec
            n += 1
    print(f"[D3] simulate：已追加 {n} 条**模拟**作答（seed={seed}，标注 simulated=True）。"
          "非真实用户数据。")
    return n


def check(store: Path) -> list[str]:
    import bkt_solver as d2  # noqa: E402
    problems: list[str] = []
    model = d2.BKTModel()
    all_recs = load_all(store)
    if not all_recs:
        problems.append("存储为空（应至少 init 过）")
        return problems
    # 1) 27 KC 都应至少有一条记录
    seen = {(r["user_id"], r["kc_id"]) for r in all_recs}
    for kc in _kc_ids():
        if (DEFAULT_USER, kc) not in seen:
            problems.append(f"KC {kc} 无掌握度记录（应已 init）")
    # 2) 每条 (user,kc) 的终态掌握度应与 BKT 递推其作答历史一致
    by_key: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in all_recs:
        by_key[(r["user_id"], r["kc_id"])].append(r)
    for key, recs in by_key.items():
        recs.sort(key=lambda x: x.get("timestamp", ""))
        mastery = DEFAULT_L0
        for r in recs:
            if r.get("kind") == "init":
                mastery = r["mastery_prob"]
                continue
            if r.get("correct") is None:
                continue
            recomputed = model.step(mastery, 1 if r["correct"] else 0)
            if abs(recomputed - r["mastery_prob"]) > 1e-9:
                problems.append(f"{key} 的掌握度递推不一致（BKT 得 {recomputed:.6f}，"
                                f"存 {r['mastery_prob']:.6f}）")
                break
            mastery = r["mastery_prob"]
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="612 D3 · 用户掌握度存储（append-only + BKT）")
    ap.add_argument("command", nargs="?", default="query",
                    choices=["init", "update", "query", "stats", "simulate"],
                    help="init/update/query/stats/simulate（默认 query）")
    ap.add_argument("--kc", default=None, help="KC id")
    ap.add_argument("--correct", type=int, default=None, help="0|1（update 用）")
    ap.add_argument("--initial-prob", type=float, default=DEFAULT_L0, help="init 的初始掌握度")
    ap.add_argument("--sessions", type=int, default=10, help="simulate 会话数")
    ap.add_argument("--seed", type=int, default=1234, help="simulate 随机种子")
    ap.add_argument("--store", default=None, help="测试注入：自定义 jsonl 路径")
    ap.add_argument("--check", action="store_true", help="自验证（exit 0=通过）")
    a = ap.parse_args(argv)
    store = Path(a.store) if a.store else DEFAULT_STORE

    if a.check:
        problems = check(store)
        if problems:
            print("[D3] ❌ 自检失败：", file=sys.stderr)
            for p in problems:
                print(f"    - {p}", file=sys.stderr)
            return 1
        s = stats(store)
        print(f"[D3] ✅ 自验证通过：KC={s['kc_count']} / 平均掌握度={s['avg_mastery']} / "
              f"已掌握={s['mastered']} / 总练习={s['total_updates']}")
        return 0

    cmd = a.command
    if cmd == "init":
        init(store, a.initial_prob)
        return 0
    if cmd == "update":
        if not a.kc or a.correct is None:
            print("[D3] ❌ update 需要 --kc 与 --correct", file=sys.stderr)
            return 2
        update(store, a.kc, bool(a.correct))
        return 0
    if cmd == "simulate":
        simulate(store, a.sessions, a.seed)
        return 0
    if cmd == "stats":
        print(json.dumps(stats(store), ensure_ascii=False, indent=1))
        return 0
    # query（默认）
    recs = query(store, a.kc)
    print(json.dumps(recs, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
