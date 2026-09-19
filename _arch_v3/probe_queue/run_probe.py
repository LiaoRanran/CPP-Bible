#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_probe.py — 534 任务4/5 沙箱实测编排（全部真实子进程，kill 用 taskkill /F）。

场景：S1 并发 next 争抢  S2 touch_set 冲突  MAIN kill-9 续跑  S4 yield 切子任务
      S5 verify 失败回退/上限 blocked  S6 毫秒开销  S7 WAL 多进程写
      S8 冒名/deps 环/僵尸心跳/租约过期接管
输出：probe_report.json + 控制台摘要。
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import statistics
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable
FIX = HERE / "fixtures"
REPORT: dict = {"scenarios": {}}


def fresh_root(name: str, *, lease: int = 600, max_attempts: int = 3) -> tuple[Path, dict]:
    root = HERE / "sandbox" / name
    if root.exists():
        shutil.rmtree(root)
    (root / "work").mkdir(parents=True)
    env = dict(os.environ, TQ_DB=str(root / "queue.db"), TQ_ROOT=str(root),
               TQ_WORKDIR=str(root / "work"), TQ_LEASE=str(lease),
               TQ_MAX_ATTEMPTS=str(max_attempts), TQ_STEP_SLEEP="0.8")
    # 独立 git 仓库：让 complete 的 touch_set 事后审计（git status）在沙箱内真实可测，
    # 不被宿主仓库的并行会话改动污染
    subprocess.run(["git", "init", "-q"], cwd=str(root), capture_output=True)
    subprocess.run(["git", "-c", "user.email=tq@probe", "-c", "user.name=tq",
                    "commit", "-q", "--allow-empty", "-m", "baseline"],
                   cwd=str(root), capture_output=True)
    subprocess.run([PY, str(HERE / "tq.py"), "init", "--worker", "harness"],
                   env=env, capture_output=True, text=True)
    return root, env


def tq(env: dict, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(HERE / "tq.py"), *args], env=env,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def enqueue_pipeline(env: dict, tid: str, *, steps: int = 5, fail: bool = False,
                     deps: str = "", touch_suffix: str = "") -> None:
    verify = (f'"{PY}" "{FIX / ("verify_fail.py" if fail else "verify_checker.py")}"'
              + (f' "{env["TQ_ROOT"]}"' if not fail else ""))
    touch = ",".join(f"work/step{n}{touch_suffix}.txt" for n in range(1, steps + 1))
    r = tq(env, "enqueue", "--type", "atom_produce", "--id", tid,
           "--goal", f"{tid} 五步流水线", "--steps", str(steps),
           "--deps", deps, "--touch", touch, "--verify-cmd", verify,
           "--budget", "500", "--worker", "harness")
    assert r.returncode == 0, r.stderr


def worker(env: dict, worker_id: str, *, extra: dict | None = None) -> subprocess.Popen:
    e = dict(env, TQ_WORKER=worker_id)
    if extra:
        e.update(extra)
    return subprocess.Popen([PY, str(HERE / "worker_sim.py")], env=e,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, encoding="utf-8", errors="replace")


def db_env(root: Path) -> dict:
    # autocommit：否则 SELECT 持有 deferred 事务快照（WAL 下永远看不到 worker 的新提交）
    con = sqlite3.connect(str(root / "queue.db"), isolation_level=None)
    con.row_factory = sqlite3.Row
    return con


def wait_step(root: Path, n: int, timeout: float = 20.0) -> None:
    t0 = time.time()
    con = db_env(root)
    while time.time() - t0 < timeout:
        v = con.execute("SELECT steps_done FROM tasks WHERE steps_done>=?", (n,)).fetchone()
        step_next = root / "work" / f"step{n + 1}.txt"
        if v and not step_next.is_file():
            con.close()
            return
        time.sleep(0.05)
    con.close()
    raise TimeoutError(f"等待 steps_done>={n} 超时")


def journal(root: Path) -> list[str]:
    return (root / "work" / "journal.log").read_text(encoding="utf-8").splitlines()


# ── S1 并发 claim ─────────────────────────────────────────────────────────────
def s1_concurrency() -> dict:
    root, env = fresh_root("s1")
    wins, double_claim, gaps = [], [], []
    for i in range(10):
        tid = f"race-{i}"
        enqueue_pipeline(env, tid, steps=1, touch_suffix=f"-{i}")
        ts0 = time.perf_counter()
        ps = [subprocess.Popen([PY, str(HERE / "tq.py"), "next", "--worker", f"w{k}",
                                "--id", tid], env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, encoding="utf-8")
              for k in (1, 2)]
        gap = None
        outs = [p.communicate() for p in ps]
        rcs = [p.returncode for p in ps]
        con = db_env(root)
        row = con.execute("SELECT attempts,claimed_by FROM tasks WHERE id=?", (tid,)).fetchone()
        con.close()
        ok = rcs.count(0) == 1 and row["attempts"] == 1
        wins.append(ok)
        if not ok:
            double_claim.append((tid, rcs, dict(row)))
    # 自动选择版本（无 --id）3 轮
    auto = []
    for i in range(3):
        tid = f"autorace-{i}"
        enqueue_pipeline(env, tid, steps=1, touch_suffix=f"-a{i}")
        ps = [subprocess.Popen([PY, str(HERE / "tq.py"), "next", "--worker", f"a{k}"],
                               env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, encoding="utf-8") for k in (1, 2)]
        rcs = [p.wait() for p in ps]
        con = db_env(root)
        row = con.execute("SELECT attempts FROM tasks WHERE id=?", (tid,)).fetchone()
        con.close()
        auto.append(rcs.count(0) == 1 and row["attempts"] == 1)
    return {"explicit_id_rounds": len(wins), "explicit_ok": sum(wins),
            "auto_rounds": len(auto), "auto_ok": sum(auto),
            "double_claims": double_claim}


# ── S2 touch_set 冲突 ──────────────────────────────────────────────────────────
def s2_touch() -> dict:
    root, env = fresh_root("s2")
    tq(env, "enqueue", "--type", "custom", "--id", "TA", "--goal", "A",
       "--touch", "work/shared.txt", "--worker", "h")
    tq(env, "enqueue", "--type", "custom", "--id", "TB", "--goal", "B",
       "--touch", "work/shared.txt", "--worker", "h")
    tq(env, "enqueue", "--type", "custom", "--id", "TC", "--goal", "C",
       "--touch", "work/c.txt", "--worker", "h")
    a = tq(env, "next", "--worker", "wA", "--id", "TA")
    b_blocked = tq(env, "next", "--worker", "wB", "--id", "TB")
    b_auto = tq(env, "next", "--worker", "wB")
    got = json.loads(b_auto.stdout)
    return {"TA_rc": a.returncode,
            "TB_rc": b_blocked.returncode,
            "TB_stderr": b_blocked.stderr.strip()[:220],
            "B_auto_picked": got.get("task_id"),
            "correctly_skipped_to_TC": got.get("task_id") == "TC"}


# ── MAIN：做到第 3 步被强杀，零上下文新 worker 从第 4 步接上 ──────────────────
def main_kill() -> dict:
    root, env = fresh_root("main")
    enqueue_pipeline(env, "TMAIN", steps=5)
    t0 = time.perf_counter()
    pa = worker(env, "A")
    wait_step(root, 3)
    # step3 已 checkpoint、step4 尚未开始（每步间隔 0.8s）→ 此刻强杀
    time.sleep(0.15)
    kill = subprocess.run(["taskkill", "/F", "/PID", str(pa.pid)], capture_output=True,
                          text=True, encoding="gbk", errors="replace")
    pa.wait(timeout=10)
    killed_at = time.perf_counter() - t0
    time.sleep(0.3)
    alive = pa.poll() is not None
    j_after_a = journal(root)
    # 全新进程 B：只有 env 里的 db/root 位置（等价"人开新会话并跑 next"）
    pb = worker(env, "B")
    rc_b = pb.wait(timeout=60)
    ob, eb = pb.communicate() if rc_b is not None else ("", "")
    j = journal(root)
    con = db_env(root)
    row = con.execute("SELECT status,attempts,steps_done,verify_hash,claimed_by FROM tasks"
                      " WHERE id='TMAIN'").fetchone()
    ev = [dict(x) for x in con.execute(
        "SELECT actor,event FROM events WHERE task_id='TMAIN' ORDER BY seq").fetchall()]
    con.close()
    a_did = sorted(int(x.split("DID step ")[1].split("/")[0])
                   for x in j if " A DID step" in x)
    b_did = sorted(int(x.split("DID step ")[1].split("/")[0])
                   for x in j if " B DID step" in x)
    b_trust = sorted(int(x.split("TRUST step ")[1].split(" ")[0])
                     for x in j if " B TRUST step" in x)
    overlap = sorted(set(a_did) & set(b_did))
    return {"kill_rc": kill.returncode, "kill_msg": kill.stdout.strip() or kill.stderr.strip(),
            "killed_after_s": round(killed_at, 2), "A_dead": alive,
            "A_did": a_did, "B_trusted_inherited": b_trust, "B_did": b_did,
            "redo_overlap": overlap,
            "final": dict(row), "B_exit": rc_b, "events": ev,
            "zero_context_ok": (a_did == [1, 2, 3] and b_trust == [1, 2, 3]
                                and b_did == [4, 5] and not overlap
                                and dict(row)["status"] == "done")}


# ── S4 yield 切子任务 + 父任务回卷 ─────────────────────────────────────────────
def s4_yield() -> dict:
    root, env = fresh_root("s4")
    enqueue_pipeline(env, "TY", steps=5)
    pa = worker(env, "A", {"TQ_YIELD_AFTER": "2"})
    ra = pa.wait(timeout=40)
    con = db_env(root)
    parent = con.execute("SELECT status,result_ref FROM tasks WHERE id='TY'").fetchone()
    children = [dict(x) for x in con.execute(
        "SELECT id,status,parent_task,steps_remaining FROM tasks WHERE parent_task='TY'")]
    con.close()
    pb = worker(env, "B")
    rb = pb.wait(timeout=60)
    con = db_env(root)
    fin = {r["id"]: r["status"] for r in con.execute(
        "SELECT id,status FROM tasks WHERE id IN ('TY','TY.c1')")}
    con.close()
    j = journal(root)
    return {"A_exit": ra, "parent_after_yield": dict(parent), "children": children,
            "B_exit": rb, "final": fin,
            "a_did": [x for x in j if " A " in x],
            "b_lines": [x for x in j if " B " in x],
            "rollup_ok": fin.get("TY") == "done" and fin.get("TY.c1") == "done"}


# ── S5 verify 失败 → 回退重试 → 超上限 blocked ─────────────────────────────────
def s5_verify_fail() -> dict:
    root, env = fresh_root("s5", max_attempts=2)
    enqueue_pipeline(env, "TF", steps=1, fail=True)
    seq = []
    for wid in ("A", "B", "C"):
        p = worker(env, wid)
        rc = p.wait(timeout=30)
        con = db_env(root)
        row = con.execute("SELECT status,attempts FROM tasks WHERE id='TF'").fetchone()
        con.close()
        seq.append({"worker": wid, "exit": rc, "status": row["status"],
                    "attempts": row["attempts"]})
        if row["status"] == "blocked":
            break
    con = db_env(root)
    ev = [x["event"] for x in con.execute(
        "SELECT event FROM events WHERE task_id='TF' ORDER BY seq")]
    con.close()
    return {"sequence": seq, "events": ev,
            "blocked_ok": seq[-1]["status"] == "blocked"}


# ── S6 毫秒级开销（库内事务）──────────────────────────────────────────────────
def s6_timing() -> dict:
    root, env = fresh_root("s6")
    sys.path.insert(0, str(HERE))
    import tq as T
    db = T.DB(Path(env["TQ_DB"]))
    N = 50

    def t(fn):
        ts = []
        for _ in range(N):
            t0 = time.perf_counter(); fn(); ts.append((time.perf_counter() - t0) * 1000)
        return round(statistics.median(ts), 2)

    enq = t(lambda: db.con.execute(
        "INSERT INTO tasks(id,type,status,priority,deps,touch_set,created_at,updated_at,"
        "enqueued_seq) VALUES('tm'||hex(randomblob(3)),'custom','pending',100,'[]','[]',?,?,"
        "(SELECT COALESCE(MAX(enqueued_seq),0)+1 FROM tasks))", (T.now(), T.now())))
    db.con.commit()
    hb = t(lambda: (db.con.execute("BEGIN IMMEDIATE"),
                    db.con.execute("UPDATE tasks SET heartbeat_at=? WHERE id='TF'", (T.now(),)),
                    db.con.commit()))
    db.close()
    # CLI 进程墙钟（含 Python 启动）
    cli = []
    for _ in range(7):
        t0 = time.perf_counter()
        subprocess.run([PY, str(HERE / "tq.py"), "list"], env=env, capture_output=True)
        cli.append((time.perf_counter() - t0) * 1000)
    return {"inproc_enqueue_ms_median": enq, "inproc_heartbeat_tx_ms_median": hb,
            "cli_list_wall_ms_median": round(statistics.median(cli), 1), "n": N}


# ── S7 WAL + 双进程并发写 ─────────────────────────────────────────────────────
def s7_wal() -> dict:
    root, env = fresh_root("s7")
    con = sqlite3.connect(str(root / "queue.db"))
    mode = con.execute("PRAGMA journal_mode").fetchone()[0]
    con.close()
    ps = [subprocess.Popen([PY, str(HERE / "load_gen.py"), "20", tag], env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True, encoding="utf-8", errors="replace")
          for tag in ("X", "Y")]
    outs = [p.communicate() + (p.returncode,) for p in ps]
    con = sqlite3.connect(str(root / "queue.db"))
    n_tasks = con.execute("SELECT COUNT(*) FROM tasks WHERE id LIKE 'load-%'").fetchone()[0]
    con.close()
    return {"journal_mode": mode,
            "loads": [{"rc": o[2], "stdout": o[0].strip()} for o in outs],
            "rows": n_tasks, "no_locked": all(o[2] == 0 for o in outs)}


# ── S8 自攻：冒名 / 环 / 僵尸 / 租约接管 ───────────────────────────────────────
def s8_attacks() -> dict:
    root, env = fresh_root("s8")
    tq(env, "enqueue", "--type", "custom", "--id", "SEC", "--goal", "g",
       "--touch", "work/sec.txt", "--steps", "2", "--worker", "h")
    claim = tq(env, "next", "--worker", "alice", "--id", "SEC")
    bogus_yield = (HERE / "sandbox" / "s8" / "bogus.json")
    hp = root / "sec.handoff.json"
    good_h = {"schema": "tq-handoff/v1", "task_id": "SEC", "goal": "g",
              "steps_done": [{"n": 1, "title": "s1", "outputs": []}],
              "steps_remaining": [{"n": 2, "title": "s2"}],
              "verified_facts": [{"fact": "x", "trust": "L1", "anchor": "work"}],
              "next_action": "do 2", "budget_used": 480}
    hp.write_text(json.dumps(good_h), encoding="utf-8")
    bogus_yield.parent.mkdir(parents=True, exist_ok=True)
    imp_hb = tq(env, "heartbeat", "SEC", "--worker", "bob", "--used", "10")
    imp_yield = tq(env, "yield", "SEC", "--worker", "bob", "--handoff", str(hp), "--force")
    imp_done = tq(env, "complete", "SEC", "--worker", "bob",
                  "--verify-cmd", f'"{PY}" -c "import sys;sys.exit(0)"')
    # deps 环
    tq(env, "enqueue", "--type", "custom", "--id", "CYCX", "--goal", "x", "--worker", "h")
    cyc = tq(env, "enqueue", "--type", "custom", "--id", "CYCY", "--goal", "y",
             "--deps", "CYCX", "--worker", "h")
    cyc2 = tq(env, "enqueue", "--type", "custom", "--id", "CYCX2", "--goal", "z",
              "--deps", "CYCY,CYCX", "--worker", "h")
    # 僵尸：同一 handoff 两次心跳
    z1 = tq(env, "heartbeat", "SEC", "--worker", "alice", "--used", "100",
            "--handoff-file", str(hp))
    z2 = tq(env, "heartbeat", "SEC", "--worker", "alice", "--used", "101",
            "--handoff-file", str(hp))
    # 租约过期接管（独立短租约库）
    r2, e2 = fresh_root("s8lease", lease=1)
    tq(e2, "enqueue", "--type", "custom", "--id", "LZ", "--goal", "z", "--steps", "1",
       "--worker", "h")
    tq(e2, "next", "--worker", "slow", "--id", "LZ")
    time.sleep(1.6)
    takeover = tq(e2, "next", "--worker", "fast", "--id", "LZ")
    con = db_env(r2)
    lz = dict(con.execute("SELECT claimed_by,attempts FROM tasks WHERE id='LZ'").fetchone())
    con.close()
    return {"impersonation": {"hb_rc": imp_hb.returncode, "yield_rc": imp_yield.returncode,
                              "complete_rc": imp_done.returncode,
                              "hb_msg": imp_hb.stderr.strip()[:100]},
            "deps_cycle_rc": cyc2.returncode,
            "deps_cycle_msg": cyc2.stderr.strip()[:140],
            "zombie": {"first": z1.stdout.strip(), "second": z2.stdout.strip()},
            "lease_takeover": {"rc": takeover.returncode, "row": lz,
                               "out": takeover.stdout.strip()[:120]}}


def main() -> int:
    R = REPORT["scenarios"]
    print("== S1 并发 claim ==")
    R["S1_concurrency"] = s1_concurrency(); print(R["S1_concurrency"])
    print("== S2 touch_set 冲突 ==")
    R["S2_touch"] = s2_touch(); print(R["S2_touch"])
    print("== MAIN kill -9 续跑 ==")
    R["MAIN_kill_resume"] = main_kill(); print(json.dumps(R["MAIN_kill_resume"], ensure_ascii=False))
    print("== S4 yield ==")
    R["S4_yield"] = s4_yield(); print(R["S4_yield"]["final"], R["S4_yield"]["rollup_ok"])
    print("== S5 verify 失败回退 ==")
    R["S5_verify_fail"] = s5_verify_fail(); print(R["S5_verify_fail"]["sequence"])
    print("== S6 开销 ==")
    R["S6_timing"] = s6_timing(); print(R["S6_timing"])
    print("== S7 WAL ==")
    R["S7_wal"] = s7_wal(); print(R["S7_wal"]["journal_mode"], R["S7_wal"]["rows"])
    print("== S8 自攻 ==")
    R["S8_attacks"] = s8_attacks(); print(json.dumps(R["S8_attacks"], ensure_ascii=False))
    (HERE / "probe_report.json").write_text(
        json.dumps(REPORT, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = (R["S1_concurrency"]["explicit_ok"] == 10 and R["S1_concurrency"]["auto_ok"] == 3
          and R["S2_touch"]["correctly_skipped_to_TC"]
          and R["MAIN_kill_resume"]["zero_context_ok"]
          and R["S4_yield"]["rollup_ok"] and R["S5_verify_fail"]["blocked_ok"]
          and R["S7_wal"]["no_locked"])
    print("\nALL_CORE_ASSERTIONS =", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
