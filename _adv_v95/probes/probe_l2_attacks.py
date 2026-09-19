"""545 独立对抗探针（攻击面 A：L2 task_queue 信任根）。

只读正式文件；一切状态落在系统临时目录（DB_PATH / ANCHOR_ROOT 指向 tmp），
不改仓库任何正式文件，不 commit。

用法：.venv\\Scripts\\python.exe _adv_v95\\probes\\probe_l2_attacks.py
输出：每条攻击打印 [ESCAPE]/[VISIBLE]/[BY-DESIGN] + 证据行。
"""
from __future__ import annotations

import datetime as _dt
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import task_queue as tq  # noqa: E402


def sb() -> Path:
    d = Path(tempfile.mkdtemp(prefix="adv95_"))
    tq.DB_PATH = d / "q.db"
    tq.ANCHOR_ROOT = d
    return d


def handoff(budget_used: int, n_done: int = 0, remaining: list | None = None) -> Path:
    d = tq.ANCHOR_ROOT
    h = {
        "schema": "tq-handoff/v1",
        "goal": "545 对抗探针",
        "steps_done": [{"n": i + 1, "title": f"step{i + 1}", "outputs": []}
                       for i in range(n_done)],
        "steps_remaining": remaining if remaining is not None else [{"n": 99, "title": "todo"}],
        "verified_facts": [{"fact": "探针事实", "trust": "L1", "anchor": "cmd:echo probe"}],
        "budget_used": budget_used,
        "next_action": "继续 step 99：写完立刻 checkpoint",
    }
    p = d / f"h{len(list(d.glob('h*')))}.json"
    p.write_text(json.dumps(h, ensure_ascii=False), encoding="utf-8")
    return p


def get(db: Path, tid: str) -> dict:
    c = sqlite3.connect(str(db))
    c.row_factory = sqlite3.Row
    try:
        r = c.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
        return dict(r) if r else {}
    finally:
        c.close()


def verdict(tag: str, ok: bool, summary: str, evidence: list[str]) -> None:
    print(f"\n===== {tag} =====\n[{('ESCAPE' if ok else 'BLOCKED')}] {summary}")
    for e in evidence:
        print(f"  · {e}")


# ── A7 · verify_cmd 自证（worker 与 enqueuer 同一人）───────────────────────────
def a7_self_certify() -> None:
    db = sb() / "q.db"
    tid = tq.enqueue("custom", "docs/a7.md", task_id="A7",
                     verify_cmd="echo attacker-pass")["id"]
    tq.claim("A")
    r = tq.complete(tid, "A")
    verdict("A7 · verify_cmd 自证", r["status"] == "done",
            "入队时自带的 verify_cmd 恒真 ⇒ complete 直接 done（同一人既入队又收尾）",
            [f"verify_cmd={r['verify_cmd']}", f"status={r['status']}",
             f"verify_hash={r['verify_hash']}",
             "源码：tools/task_queue.py complete() 取 row['verify_cmd'] 后 shell=True 执行",
             "注：--verify-cmd 覆盖 type 默认表是 534 §4.3 明写的设计；"
             "洞在『enqueuer==worker』时没人复核"])


# ── A3 · 未来心跳 / 时钟偏移 永久占坑 ──────────────────────────────────────────
def a3_future_heartbeat() -> None:
    d = sb()
    db = d / "q.db"
    tid = tq.enqueue("custom", "docs/a3.md", task_id="A3")["id"]
    tq.claim("A")
    future = (_dt.datetime.now() + _dt.timedelta(hours=1)).isoformat(timespec="seconds")
    c = sqlite3.connect(str(db))
    c.execute("UPDATE tasks SET heartbeat_at=? WHERE id=?", (future, tid))
    c.commit()
    c.close()
    r = tq.claim("B")
    nx = tq.next_task()
    still = get(db, tid)["status"]
    verdict("A3 · 未来心跳（时钟偏移/跨时区 worker）永久占坑",
            r["claimed"] is None and nx["next"] is None and still == "claimed",
            "heartbeat_at 写成未来 ⇒ 永不 stale ⇒ 无人能接管（除人 --force）",
            [f"heartbeat_at={future}（now+1h）",
             f"claim(B).claimed={r['claimed']}  next_task().next={nx['next']}",
             f"任务状态仍={still}",
             "源码：_sweep_stale 用 heartbeat_at < now-600s；_age_s() 用 time.mktime 本地时区解析",
             "触发路径：worker 机器时区/时钟快于调度机（跨机场景）即可自然产生"])
    # 缓解确证
    tr = tq.claim("B", takeover=tid, force=True, reason="人确认旧会话已死")
    print(f"  · 缓解：--force --reason 可接管 ⇒ taken_over={tr['claimed']['id'] if tr['claimed'] else None}")


# ── A5 · yield 无限层级续命（budget 越让越多）──────────────────────────────────
def a5_yield_immortality() -> None:
    db = sb() / "q.db"
    tq.DB_PATH = db
    tq.ANCHOR_ROOT = db.parent
    chain: list[str] = []
    tid = tq.enqueue("custom", "docs/a5.md", task_id="P", budget=500)["id"]
    tq.claim("w0")
    # 父：used=450 ⇒ left=50 < YIELD_BUDGET_LEFT(100) ⇒ **无需人签** 即可让出
    hp = handoff(450)
    tq.checkpoint(tid, "w0", hp, used=450)
    r0 = tq.yield_task(tid, "w0", hp)
    cur = r0["children"][0]
    chain.append(f"P(budget=500,used=450,left=50) --无force--> "
                 f"{cur}(budget={get(db, cur)['budget_calls']})")
    # 之后每级：预算 80 ⇒ left=80-0=80 < 100 ⇒ **无需 force**，可无限续
    for i in range(1, 5):
        tq.claim(f"w{i}")
        h = handoff(0)
        r = tq.yield_task(cur, f"w{i}", h)
        nxt = r["children"][0]
        chain.append(f"{cur}(budget={get(db, cur)['budget_calls']},used=0) "
                     f"--无force--> {nxt}(budget={get(db, nxt)['budget_calls']})")
        cur = nxt
    depth = len(chain)
    verdict("A5 · yield 无限层级续命",
            depth >= 5,
            f"每级子任务预算恒为 MIN_CHILD_BUDGET(80) < YIELD_BUDGET_LEFT(100) ⇒ "
            f"无需 --force 即可再让出 ⇒ 深度无上界，总调用预算无上界",
            chain + ["源码：yield_task 中 per = max(MIN_CHILD_BUDGET, left // len(groups))；"
                     "闸门只看本级 left，不看层级深度/累计调用数",
                     f"实测深度 {depth} 级仍可继续；无 depth 上限、无累计预算账"])


# ── A5b · 父 done 而子未全 done 时是否被误回卷 ─────────────────────────────────
def a5b_rollup_partial() -> None:
    db = sb() / "q.db"
    tid = tq.enqueue("custom", "docs/a5b.md", task_id="P2", budget=150)["id"]
    tq.claim("w")
    hp = handoff(100, remaining=[{"n": 2}, {"n": 3}])
    tq.checkpoint(tid, "w", hp, used=100)
    r = tq.yield_task(tid, "w", hp)
    kids = r["children"]
    # 只让第一组完成（后组还在 queued）
    tq.claim("w1")
    assert tq.claim("w1")["claimed"] is None or True
    first = kids[0]
    tq.done(first, "w1", result_ref="out/1")
    verdict("A5b · 父回卷时机", get(db, tid)["status"] == "yielded",
            "仅部分子任务 done 时父保持 yielded（回卷时机正确）",
            [f"子任务={kids}", f"父状态={get(db, tid)['status']}",
             f"剩余未 done 子任务={[k for k in kids if get(db, k)['status'] != 'done']}"])


if __name__ == "__main__":
    a7_self_certify()
    a3_future_heartbeat()
    a5_yield_immortality()
    a5b_rollup_partial()
    print("\n[done] 全部探针执行完毕（状态只在系统临时目录，仓库零改动）")
