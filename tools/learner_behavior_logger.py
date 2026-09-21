#!/usr/bin/env python3
"""614 线B B1：真实学习行为采集 + BKT 递推集成（append-only 行为日志）。

行为事件（每条 = 一次学习交互）：
  * user_id：默认 "default"（单用户场景）
  * kc_id：KC ID（原子卡 ID）
  * action ∈ {correct, incorrect, hint, skip}：hint/skip 缺正确性信号，不参与 BKT 递推（只计数）
  * timestamp：ISO 时间
  * source ∈ {exercise, quiz, review}
  * difficulty：可选 1-5
  * simulated：是否模拟数据（诚实标注，非真实用户数据）

存储：data/learner_behaviors.jsonl（**append-only**；最新掌握度 = 按时间序对该 KC 的
  correct/incorrect 事件做 BKT 递推后的终值）。

CLI：
  log       --kc <id> --action <correct|incorrect|hint|skip> [--source exercise] [--difficulty 1-5]
  import    --file <csv|jsonl>            # 批量导入（CSV 列：kc_id,action,source,difficulty[,timestamp,user_id]）
  stats     [--kc <id>]                   # 统计（总事件/各 action 计数/各 KC 事件数）
  replay    [--kc <id>]                   # 重放行为 → KC 掌握度轨迹（BKT）
  recommend [--threshold 0.5]             # 推荐下一可学 KC（掌握度<阈值 且 前置均已掌握）
  simulate  --kcs 10 --rounds 5 [--seed S] [--acc-start 0.3 --acc-end 0.8]   # 生成 30%→80% 轨迹（simulated）
  --check                                # 自验证（exit 0=通过）

集成：replay() 复用 bkt_solver.BKTModel，对 correct→1 / incorrect→0 做 step 递推；
  绝不臆造 correct（hint/skip 仅计数）。recommend() 复用 kc_inventory 的 prerequisites 做前置门槛。

铁律：单用户 user_id 固定 default；append-only；不调用 LLM；模拟数据标注 simulated=True。
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

DEFAULT_STORE = ROOT / "data" / "learner_behaviors.jsonl"
DEFAULT_USER = "default"
ACTIONS = ("correct", "incorrect", "hint", "skip")
SOURCES = ("exercise", "quiz", "review")
DEFAULT_THRESHOLD = 0.5


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _kc_ids() -> list[str]:
    import kc_inventory as d1  # noqa: E402
    return [k["id"] for k in cast("dict[str, Any]", d1.build())["kcs"]]


def load_all(store: Path) -> list[dict]:
    if not store.is_file():
        return []
    out: list[dict] = []
    for line in store.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(cast("dict[str, Any]", json.loads(line)))
    return out


def record(store: Path, user: str, kc: str, action: str, source: str,
           difficulty: int | None, simulated: bool) -> dict:
    if action not in ACTIONS:
        raise ValueError(f"action 必须 ∈ {ACTIONS}，收到 {action!r}")
    if source not in SOURCES:
        raise ValueError(f"source 必须 ∈ {SOURCES}，收到 {source!r}")
    rec = {"user_id": user, "kc_id": kc, "action": action, "timestamp": _now(),
           "source": source, "simulated": bool(simulated)}
    if difficulty is not None:
        rec["difficulty"] = int(difficulty)
    store.parent.mkdir(parents=True, exist_ok=True)
    with store.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def _import_record(raw: dict, default_user: str) -> dict:
    kc = str(raw.get("kc_id") or raw.get("kc") or "")
    action = str(raw.get("action") or "")
    source = str(raw.get("source") or "exercise")
    difficulty = raw.get("difficulty")
    if difficulty not in (None, ""):
        difficulty = int(difficulty)
    else:
        difficulty = None
    user = str(raw.get("user_id") or raw.get("user") or default_user)
    ts = raw.get("timestamp") or _now()
    rec = {"user_id": user, "kc_id": kc, "action": action, "timestamp": ts,
           "source": source, "simulated": bool(raw.get("simulated", False))}
    if difficulty is not None:
        rec["difficulty"] = difficulty
    if action not in ACTIONS:
        raise ValueError(f"action 必须 ∈ {ACTIONS}，收到 {action!r}")
    if source not in SOURCES:
        raise ValueError(f"source 必须 ∈ {SOURCES}，收到 {source!r}")
    return rec


def import_file(store: Path, path: Path, default_user: str = DEFAULT_USER) -> int:
    recs: list[dict] = []
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                recs.append(_import_record(dict(row), default_user))
    else:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            recs.append(_import_record(cast("dict[str, Any]", json.loads(line)), default_user))
    store.parent.mkdir(parents=True, exist_ok=True)
    with store.open("a", encoding="utf-8") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[logger] import：已追加 {len(recs)} 条行为（来源 {path.name}）。")
    return len(recs)


def replay(store: Path, user: str = DEFAULT_USER) -> dict[str, float]:
    """按时间序对每 KC 的 correct/incorrect 事件做 BKT 递推，返回 KC→终值掌握度。"""
    import bkt_solver as d2  # noqa: E402
    model = d2.BKTModel()
    by_kc: dict[str, list[dict]] = {}
    for r in load_all(store):
        if r.get("user_id") != user:
            continue
        by_kc.setdefault(r["kc_id"], []).append(r)
    out: dict[str, float] = {}
    for kc, evs in by_kc.items():
        evs.sort(key=lambda x: x.get("timestamp", ""))
        mastery = 0.1  # P(L0)
        for e in evs:
            act = e.get("action")
            if act == "correct":
                mastery = model.step(mastery, 1)
            elif act == "incorrect":
                mastery = model.step(mastery, 0)
            # hint / skip：无正确性信号，不参与递推
        out[kc] = mastery
    return out


def stats(store: Path, user: str = DEFAULT_USER, kc: str | None = None) -> dict:
    recs = [r for r in load_all(store) if r.get("user_id") == user]
    if kc:
        recs = [r for r in recs if r.get("kc_id") == kc]
    per_action: dict[str, int] = {a: 0 for a in ACTIONS}
    per_kc: dict[str, int] = {}
    for r in recs:
        per_action[r.get("action", "?")] = per_action.get(r.get("action", "?"), 0) + 1
        per_kc[r.get("kc_id", "?")] = per_kc.get(r.get("kc_id", "?"), 0) + 1
    return {"user": user, "kc_filter": kc, "total": len(recs),
            "per_action": per_action, "per_kc_count": len(per_kc),
            "simulated": sum(1 for r in recs if r.get("simulated"))}


def recommend_next(store: Path, user: str = DEFAULT_USER,
                   threshold: float = DEFAULT_THRESHOLD) -> list[str]:
    """推荐下一可学 KC：掌握度<阈值 且 全部前置 KC 掌握度≥阈值。"""
    import kc_inventory as d1  # noqa: E402
    mastery = replay(store, user)
    kcs = cast("dict[str, Any]", d1.build())["kcs"]
    ids = {k["id"] for k in kcs}
    prereqs = {k["id"]: [p for p in (k.get("prerequisites") or [])
                          if p in ids and p != k["id"]] for k in kcs}
    out: list[str] = []
    for k in kcs:
        kid = k["id"]
        m = mastery.get(kid, 0.1)
        if m >= threshold:
            continue
        if all(mastery.get(p, 0.1) >= threshold for p in prereqs[kid]):
            out.append(kid)
    return out


def simulate(store: Path, kcs_n: int, rounds: int, seed: int = 1234,
             acc_start: float = 0.3, acc_end: float = 0.8,
             user: str = DEFAULT_USER) -> int:
    """生成一条学习轨迹：kcs_n 个 KC × rounds 次练习，准确率从 acc_start 线性升到 acc_end。"""
    import bkt_solver as d2  # noqa: E402
    rng = random.Random(seed)
    kcs = _kc_ids()[:kcs_n]
    model = d2.BKTModel()
    t0 = datetime(2026, 9, 21, 8, 0, 0)
    n = 0
    store.parent.mkdir(parents=True, exist_ok=True)
    with store.open("a", encoding="utf-8") as fh:
        for ki, kc in enumerate(kcs):
            mastery = 0.1
            for r in range(rounds):
                acc = acc_start + (acc_end - acc_start) * (r / max(1, rounds - 1))
                correct = rng.random() < acc
                mastery = model.step(mastery, 1 if correct else 0)
                ts = (t0 + timedelta(minutes=ki * rounds + r)).isoformat(timespec="seconds")
                rec = {"user_id": user, "kc_id": kc, "action": "correct" if correct else "incorrect",
                       "timestamp": ts, "source": "exercise", "simulated": True}
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n += 1
    print(f"[logger] simulate：追加 {n} 条**模拟**作答（{kcs_n} KC × {rounds} 轮，"
          f"准确率 {acc_start}→{acc_end}，seed={seed}）。非真实用户数据。")
    return n


def check(store: Path) -> list[str]:
    problems: list[str] = []
    # 1) schema 校验（若存储非空）
    for r in load_all(store):
        if set(r.keys()) >= {"user_id", "kc_id", "action", "timestamp", "source"}:
            continue
        problems.append(f"事件缺字段：{r}")
        break
    # 2) BKT 性质（直接对 bkt_solver 验证，不依赖存储）
    import bkt_solver as d2  # noqa: E402
    m = d2.BKTModel()
    up = m.run_sequence([1] * 20)["mastery_after"]
    if not all(up[i + 1] >= up[i] for i in range(len(up) - 1)) or not up[-1] > up[0]:
        problems.append("BKT 全对应掌握概率应单调不减且终点高于起点")
    down = m.run_sequence([0] * 20)["mastery_after"]
    if not all(down[i + 1] <= down[i] for i in range(len(down) - 1)) or not down[-1] < down[0]:
        problems.append("BKT 全错应掌握概率应单调不增且终点低于起点")
    # 3) 闭环：simulate → replay 后至少 5 个 KC 掌握度 ≥ 0.5
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "beh.jsonl"
        simulate(tmp, kcs_n=10, rounds=5, seed=7, acc_start=0.3, acc_end=0.8)
        mast = replay(tmp)
        risen = [k for k, v in mast.items() if v >= 0.5]
        if len(risen) < 5:
            problems.append(f"模拟轨迹后 ≥0.5 的 KC 应≥5（实得 {len(risen)}）")
        if not all(v > 0.1 for v in mast.values()):
            problems.append("模拟轨迹后掌握度应全部高于初始 0.1")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="614 B1 学习行为采集 + BKT 集成")
    ap.add_argument("command", nargs="?", default="stats",
                    choices=["log", "import", "stats", "replay", "recommend", "simulate"],
                    help="子命令（默认 stats）")
    ap.add_argument("--kc", default=None)
    ap.add_argument("--action", default=None)
    ap.add_argument("--source", default="exercise")
    ap.add_argument("--difficulty", type=int, default=None)
    ap.add_argument("--user", default=DEFAULT_USER)
    ap.add_argument("--file", default=None)
    ap.add_argument("--kcs", type=int, default=10)
    ap.add_argument("--rounds", type=int, default=5)
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--acc-start", type=float, default=0.3)
    ap.add_argument("--acc-end", type=float, default=0.8)
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    ap.add_argument("--store", default=None, help="测试注入：自定义 jsonl 路径")
    ap.add_argument("--check", action="store_true", help="自验证（exit 0=通过）")
    a = ap.parse_args(argv)
    store = Path(a.store) if a.store else DEFAULT_STORE

    if a.check:
        problems = check(store)
        if problems:
            print("[logger] ❌ 自检失败：", file=sys.stderr)
            for p in problems:
                print(f"    - {p}", file=sys.stderr)
            return 1
        print("[logger] ✅ 自验证通过：schema/BKT 性质/闭环轨迹（≥5 KC→≥0.5）全部一致")
        return 0

    cmd = a.command
    if cmd == "log":
        if not a.kc or not a.action:
            print("[logger] ❌ log 需要 --kc 与 --action", file=sys.stderr)
            return 2
        rec = record(store, a.user, a.kc, a.action, a.source, a.difficulty, simulated=False)
        print(f"[logger] 已记录：{rec}")
        return 0
    if cmd == "import":
        if not a.file:
            print("[logger] ❌ import 需要 --file", file=sys.stderr)
            return 2
        import_file(store, Path(a.file), a.user)
        return 0
    if cmd == "stats":
        print(json.dumps(stats(store, a.user, a.kc), ensure_ascii=False, indent=1))
        return 0
    if cmd == "replay":
        mast = replay(store, a.user)
        if a.kc:
            mast = {a.kc: mast.get(a.kc, 0.1)}
        print(json.dumps(mast, ensure_ascii=False, indent=1))
        return 0
    if cmd == "recommend":
        recs = recommend_next(store, a.user, a.threshold)
        print(json.dumps({"threshold": a.threshold, "recommended_kc": recs,
                          "count": len(recs)}, ensure_ascii=False, indent=1))
        return 0
    if cmd == "simulate":
        simulate(store, a.kcs, a.rounds, a.seed, a.acc_start, a.acc_end, a.user)
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
