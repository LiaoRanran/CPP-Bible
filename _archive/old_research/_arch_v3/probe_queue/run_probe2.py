#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_probe2.py — 534 任务4 沙箱实测（驱动苦力落地版 tools/task_queue.py d976170 + 增量 tq_ext）。

场景：S1 并发 claim  S2 touch_set 冲突  MAIN kill-9→人工 takeover 零上下文续跑
      S4 yield 切子任务+父回卷  S5 verify 失败回退→blocked  S6 毫秒开销
      S7 WAL 双进程并发 enqueue  S8 冒名/自引用环/僵尸心跳/新鲜接管拒绝/stale 回收
"""
from __future__ import annotations

import json
import os
import shutil
import stat
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


def _force_rmtree(root: Path) -> None:
    """Windows：git objects 只读位 + WAL 句柄延迟释放，chmod+短暂重试。"""
    import time as _t

    def onexc(func, p, exc):
        os.chmod(p, stat.S_IWRITE)
        try:
            func(p)
        except PermissionError:
            _t.sleep(0.3)
            func(p)
    shutil.rmtree(root, onexc=onexc)


def fresh_root(name: str, *, max_attempts: int | None = None) -> tuple[Path, dict]:
    root = HERE / "sandbox2" / name
    if root.exists():
        _force_rmtree(root)
    (root / "work").mkdir(parents=True)
    env = dict(os.environ, TQ_ROOT=str(root),
               TQ_MAX_ATTEMPTS=str(max_attempts) if max_attempts else "")
    env["TQ_TAKEOVER_GRACE"] = "120"
    env["TQ_STEP_SLEEP"] = "0.8"
    # touch 审计的真实 git 边界（complete 内跑 git status --porcelain）
    subprocess.run(["git", "init", "-q"], cwd=str(root), capture_output=True)
    subprocess.run(["git", "-c", "user.email=tq@probe", "-c", "user.name=tq",
                    "commit", "-q", "--allow-empty", "-m", "baseline"],
                   cwd=str(root), capture_output=True)
    return root, env


def db_of(root: Path) -> Path:
    return root / "queue.db"


def tqext(root: Path, env: dict, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(HERE / "tq_ext.py"), "--db", str(db_of(root)), *args],
                          env=env, cwd=str(root), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def tqbase(root: Path, env: dict, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(HERE.parent.parent / "tools" / "task_queue.py"),
                           "--db", str(db_of(root)), *args],
                          env=env, cwd=str(root), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def enqueue(root: Path, env: dict, tid: str, *, steps: int = 5, fail: bool = False,
            touch_suffix: str = "", deps: str = "", vtype: str = "atom_produce") -> None:
    checker = FIX / ("verify_fail.py" if fail else "verify_checker.py")
    verify = f'"{PY}" "{checker}"' + ("" if fail else f' "{root}"')
    touch = ",".join(f"work/step{n}{touch_suffix}.txt" for n in range(1, steps + 1))
    r = tqext(root, env, "--json", "enqueue", "--type", vtype, "--id", tid,
              "--payload-ref", f"docs/{tid}.md", "--steps", str(steps),
              "--deps", deps, "--touch", touch, "--verify-cmd", verify,
              "--budget", "500", "--goal", f"{tid} 五步流水线", "--worker", "harness")
    assert r.returncode == 0, f"enqueue {tid} failed: {r.stderr}"


def worker(root: Path, env: dict, wid: str, *, extra: dict | None = None) -> subprocess.Popen:
    e = dict(env, TQEXT_DB=str(db_of(root)), TQEXT_ROOT=str(root),
             TQEXT_WORKDIR=str(root / "work"), TQEXT_WORKER=wid)
    if extra:
        e.update({k: str(v) for k, v in extra.items()})
    return subprocess.Popen([PY, str(HERE / "worker_ext.py")], env=e, cwd=str(root),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, encoding="utf-8", errors="replace")


def dbcon(root: Path):
    con = sqlite3.connect(str(db_of(root)), isolation_level=None)
    con.row_factory = sqlite3.Row
    return con


def wait_step(root: Path, n: int, timeout: float = 25.0) -> None:
    """等"第 n 步已 checkpoint、第 n+1 步未 checkpoint"的真实窗口。

    注意不能用 stepN+1.txt 是否存在判据：worker 先写文件后 sleep，该文件在
    n 步 checkpoint 后几毫秒就出现；checkpoint 列才是"进度已落盘"的权威，
    其窗口 = 第 n 步 checkpoint 提交 → 第 n+1 步 checkpoint 提交（约 0.9s）。
    """
    t0 = time.time()
    while time.time() - t0 < timeout:
        con = dbcon(root)
        v = con.execute("SELECT steps_done FROM tasks WHERE id='TMAIN'").fetchone()
        con.close()
        if v and int(v[0]) == n:
            time.sleep(0.05)      # 让 kill 落在第 n+1 步的工作中途
            return
        time.sleep(0.03)
    raise TimeoutError(f"等待 steps_done=={n} 超时")


def journal(root: Path) -> list[str]:
    p = root / "work" / "journal.log"
    return p.read_text(encoding="utf-8").splitlines() if p.is_file() else []


# ── S1 并发 claim（落地版原子性 + 增量表共存回归）──────────────────────────────
def s1() -> dict:
    root, env = fresh_root("s1")
    rounds, fails = 0, []
    for i in range(10):
        enqueue(root, env, f"race-{i}", steps=1, touch_suffix=f"-{i}")
        ps = [subprocess.Popen([PY, str(HERE / "tq_ext.py"), "--db", str(db_of(root)),
                                "--json", "claim", "--worker", f"w{k}"],
                               env=env, cwd=str(root), stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, encoding="utf-8")
              for k in (1, 2)]
        outs = [p.communicate() for p in ps]
        rcs = [p.returncode for p in ps]
        con = dbcon(root)
        row = con.execute("SELECT attempts,claimed_by FROM tasks WHERE id=?",
                          (f"race-{i}",)).fetchone()
        con.close()
        rounds += 1
        if not (rcs.count(0) == 2 and row["attempts"] == 1):
            fails.append({"tid": f"race-{i}", "rcs": rcs,
                          "attempts": row["attempts"], "outs": [o[0][:80] for o in outs]})
    return {"rounds": rounds, "double_claim_fails": fails,
            "atomic_ok": not fails}


# ── S2 touch_set 冲突：返回"等谁"，可自动跳到不冲突任务 ─────────────────────────
def s2() -> dict:
    root, env = fresh_root("s2")
    tqext(root, env, "--json", "enqueue", "--type", "custom", "--id", "TA",
          "--payload-ref", "docs/ta.md", "--touch", "work/shared.txt")
    tqext(root, env, "--json", "enqueue", "--type", "custom", "--id", "TB",
          "--payload-ref", "docs/tb.md", "--touch", "work/shared.txt")
    tqext(root, env, "--json", "enqueue", "--type", "custom", "--id", "TC",
          "--payload-ref", "docs/tc.md", "--touch", "work/c.txt")
    a = tqext(root, env, "--json", "claim", "--worker", "wA", "--types", "custom")
    b = tqext(root, env, "--json", "claim", "--worker", "wB", "--types", "custom")
    bj = json.loads(b.stdout)
    # 语义：候选 TB 与在领任务 TA 的 touch_set 相交 ⇒ 跳过 TB（返回体点名"等谁"），
    # 继续挑到不冲突的 TC 领走。
    skip = bj["blocked_by_touch"]
    return {"TA_rc": a.returncode,
            "B_claim": bj,
            "blocked_then_picked_TC": (
                bj["claimed"] is not None and bj["claimed"]["id"] == "TC"
                and skip and skip[0]["id"] == "TB"
                and skip[0]["blocked_by"][0]["task"] == "TA"
                and skip[0]["blocked_by"][0]["files"] == ["work/shared.txt"])}


# ── MAIN：kill -9 后人工 takeover，零上下文新 worker 从第 4 步接上 ──────────────
def main_kill() -> dict:
    root, env = fresh_root("main")
    enqueue(root, env, "TMAIN", steps=5)
    t0 = time.perf_counter()
    pa = worker(root, env, "A")
    wait_step(root, 3)
    time.sleep(0.15)
    kill = subprocess.run(["taskkill", "/F", "/PID", str(pa.pid)], capture_output=True,
                          text=True, encoding="gbk", errors="replace")
    pa.wait(timeout=10)
    killed_after = time.perf_counter() - t0
    time.sleep(0.3)
    # ① 裸 claim：心跳仍新 → 拿不到（租约语义，防顶活人）
    naked = tqext(root, env, "--json", "claim", "--worker", "B")
    naked_j = json.loads(naked.stdout)
    # ② 不带 --force 的 takeover：心跳 <120s → 拒绝
    soft = tqext(root, env, "--json", "claim", "--worker", "B",
                 "--takeover", "TMAIN")
    # ③ 人确认旧会话死 → force + reason 接管；新 worker 零上下文启动
    pb = worker(root, env, "B", extra={"TQEXT_TAKEOVER": "TMAIN", "TQEXT_FORCE": "1",
                                       "TQEXT_REASON": "A 会话工具调用到顶被 kill，人开新会话"})
    rc_b = pb.wait(timeout=60)
    j = journal(root)
    con = dbcon(root)
    row = dict(con.execute("SELECT * FROM tasks WHERE id='TMAIN'").fetchone())
    ev = [dict(x) for x in con.execute(
        "SELECT actor,event FROM events WHERE task_id='TMAIN' ORDER BY seq").fetchall()]
    con.close()
    import re as _re
    a_did = sorted(int(m.group(1)) for x in j for m in [_re.search(r"A DID step (\d+)", x)] if m)
    b_did = sorted(int(m.group(1)) for x in j for m in [_re.search(r"B DID step (\d+)", x)] if m)
    b_trust = sorted(int(m.group(1)) for x in j
                     for m in [_re.search(r"B TRUST step (\d+)", x)] if m)
    return {"kill_msg": (kill.stdout or kill.stderr).strip(), "killed_after_s": round(killed_after, 2),
            "naked_claim_got": naked_j["claimed"] is not None,
            "soft_takeover_rc": soft.returncode,
            "soft_takeover_msg": json.loads(soft.stderr)["error"][:110],
            "A_did": a_did, "B_trusted": b_trust, "B_did": b_did,
            "redo_overlap": sorted(set(a_did) & set(b_did)),
            "B_exit": rc_b,
            "final_status": row["status"], "attempts": row["attempts"],
            "verify_record": (row.get("error") or "")[:120],
            "events": ev,
            "zero_context_ok": (naked_j["claimed"] is None
                                and soft.returncode == 2
                                and a_did == [1, 2, 3] and b_trust == [1, 2, 3]
                                and b_did == [4, 5] and not set(a_did) & set(b_did)
                                and row["status"] == "done")}


# ── S4 yield 切子任务，新会话普通 claim 领到子任务，父任务回卷 done ─────────────
def s4() -> dict:
    root, env = fresh_root("s4")
    enqueue(root, env, "TY", steps=5)
    pa = worker(root, env, "A", extra={"TQEXT_YIELD_AFTER": "2"})
    ra = pa.wait(timeout=40)
    con = dbcon(root)
    parent = dict(con.execute("SELECT status FROM tasks WHERE id='TY'").fetchone())
    child = dict(con.execute(
        "SELECT id,status,parent_task,steps_total,handoff_path FROM tasks "
        "WHERE parent_task='TY'").fetchone())
    con.close()
    pb = worker(root, env, "B")
    rb = pb.wait(timeout=60)
    con = dbcon(root)
    fin = {r["id"]: r["status"] for r in con.execute(
        "SELECT id,status FROM tasks WHERE id IN ('TY','TY.c1')").fetchall()}
    con.close()
    j = journal(root)
    import re as _re
    b_trust = sorted(int(m.group(1)) for x in j
                     for m in [_re.search(r"B TRUST step (\d+)", x)] if m)
    b_did = sorted(int(m.group(1)) for x in j
                   for m in [_re.search(r"B DID step (\d+)", x)] if m)
    return {"A_exit": ra, "parent_after_yield": parent["status"],
            "child": child,
            "B_exit": rb, "final": fin,
            "B_trust": b_trust, "B_did": b_did,
            "rollup_ok": fin == {"TY": "done", "TY.c1": "done"}}


# ── S5 verify 失败：回 queued 重试，超 attempts 上限 blocked ───────────────────
def s5() -> dict:
    root, env = fresh_root("s5", max_attempts=2)
    enqueue(root, env, "TF", steps=1, fail=True)
    seq = []
    for wid in ("A", "B", "C"):
        p = worker(root, env, wid)
        rc = p.wait(timeout=30)
        con = dbcon(root)
        row = con.execute("SELECT status,attempts FROM tasks WHERE id='TF'").fetchone()
        con.close()
        seq.append({"worker": wid, "exit": rc, "status": row["status"],
                    "attempts": row["attempts"]})
        if row["status"] == "blocked":
            break
    con = dbcon(root)
    ev = [x["event"] for x in con.execute(
        "SELECT event FROM events WHERE task_id='TF' ORDER BY seq")]
    con.close()
    return {"sequence": seq, "events": ev, "blocked_ok": seq[-1]["status"] == "blocked"}


# ── S6 毫秒开销 ─────────────────────────────────────────────────────────────────
def s6() -> dict:
    root, env = fresh_root("s6")
    sys.path.insert(0, str(HERE))
    import tq_ext as X
    db = db_of(root)

    def bench(fn, n=40):
        ts = []
        for _ in range(n):
            t0 = time.perf_counter(); fn(); ts.append((time.perf_counter() - t0) * 1000)
        return round(statistics.median(ts), 2)

    def enq():
        X.enqueue_ext(db, task_type="custom", payload_ref=f"p{time.perf_counter_ns()}",
                      task_id=f"tm-{time.perf_counter_ns()}", touch=["x"])

    enq_ms = bench(enq)

    X.enqueue_ext(db, task_type="custom", payload_ref="hb", task_id="HB",
                  touch=["h"], priority=1)
    X.claim_ext(db, "w")
    hp = root / "work" / "hb.json"
    hp.parent.mkdir(exist_ok=True)
    hp.write_text(json.dumps({"goal": "g", "next_action": "do",
                              "steps_done": [{"n": 1, "title": "t", "outputs": []}],
                              "steps_remaining": [],
                              "verified_facts": [{"fact": "f", "trust": "L1",
                                                  "anchor": "work"}]}), encoding="utf-8")
    hb_ms = bench(lambda: X.heartbeat_ext(db, "HB", "w", used=1, handoff_path=hp))
    cli = []
    for _ in range(7):
        t0 = time.perf_counter()
        tqbase(root, env, "list", "--json")
        cli.append((time.perf_counter() - t0) * 1000)
    return {"enqueue_ext_inproc_ms_median": enq_ms,
            "heartbeat_inproc_ms_median": hb_ms,
            "cli_list_wall_ms_median": round(statistics.median(cli), 1)}


# ── S7 WAL 双进程并发 enqueue ──────────────────────────────────────────────────
def s7() -> dict:
    root, env = fresh_root("s7")
    # 先串行建库：双进程同时在不存在的库上跑首个连接会争用（落地版 _connect 的
    # journal_mode PRAGMA 早于 busy_timeout 生效）——冷启动建库必须串行（规格 C1 修）。
    tqext(root, env, "--json", "enqueue", "--type", "custom", "--id", "seed",
          "--payload-ref", "docs/seed.md", "--touch", "w/seed.txt")

    def loadproc(tag: str) -> subprocess.Popen:
        return subprocess.Popen([PY, str(HERE / "load_gen2.py"), str(db_of(root)),
                                 "20", tag], env=env, cwd=str(root),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    ps = [loadproc("X"), loadproc("Y")]
    outs = [(p.communicate() + (p.returncode,)) for p in ps]
    # 模式必须在首个 tq_ext 连接建库之后查（裸连接先于建库只会读到新建空库的默认 delete）
    con = sqlite3.connect(str(db_of(root)))
    mode = con.execute("PRAGMA journal_mode").fetchone()[0]
    n = con.execute("SELECT COUNT(*) FROM tasks WHERE id LIKE 'load-%'").fetchone()[0]
    con.close()
    wal_files = [p.name for p in db_of(root).parent.glob("queue.db-*")]
    return {"journal_mode": mode, "rows": n, "all_rc0": all(o[2] == 0 for o in outs),
            "wal_sidecars": wal_files,
            "proc_out": [o[0].strip() for o in outs]}


# ── S8 自攻：冒名 / 自引用环 / 僵尸 / 新鲜拒绝 / stale 回收 ─────────────────────
def s8() -> dict:
    root, env = fresh_root("s8")
    tqext(root, env, "--json", "enqueue", "--type", "custom", "--id", "SEC",
          "--payload-ref", "docs/sec.md", "--steps", "2", "--touch", "work/sec.txt")
    tqext(root, env, "--json", "claim", "--worker", "alice")
    hp = root / "sec.handoff.json"
    good = {"schema": "tq-handoff/v1", "task_id": "SEC", "goal": "g",
            "next_action": "do 2", "budget_used": 100,
            "steps_done": [{"n": 1, "title": "s1", "outputs": []}],
            "steps_remaining": [{"n": 2, "title": "s2"}],
            "verified_facts": [{"fact": "x", "trust": "L1", "anchor": "work"}]}
    hp.write_text(json.dumps(good), encoding="utf-8")
    bob_hb = tqext(root, env, "--json", "heartbeat", "SEC", "--worker", "bob", "--used", "10")
    bob_done = tqext(root, env, "--json", "complete", "SEC", "--worker", "bob",
                     "--result-ref", "x")
    # 自引用环（在"缺依赖即拒+id幂等"下，这是新节点唯一能构造的环）
    selfcyc = tqext(root, env, "--json", "enqueue", "--type", "custom", "--id", "LOOP",
                    "--payload-ref", "docs/loop.md", "--deps", "LOOP")
    # 缺失依赖（落地版语义回归）
    ghost = tqext(root, env, "--json", "enqueue", "--type", "custom", "--id", "GH",
                  "--payload-ref", "docs/gh.md", "--deps", "no-such")
    # 僵尸：先 checkpoint 把指纹落库，再带**同一指纹**连续两次心跳
    # （checkpoint 推进不算；心跳间指纹不动才是"心跳在但不推进"）
    tqext(root, env, "--json", "checkpoint", "SEC", "--worker", "alice",
          "--handoff", str(hp))
    z1 = tqext(root, env, "--json", "heartbeat", "SEC", "--worker", "alice",
               "--used", "100", "--handoff", str(hp))
    z2 = tqext(root, env, "--json", "heartbeat", "SEC", "--worker", "alice",
               "--used", "101", "--handoff", str(hp))
    # 指纹推进（先 checkpoint 再心跳）→ 计数清零，复活
    good2 = dict(good, steps_done=[{"n": 1, "title": "s1", "outputs": []},
                                   {"n": 2, "title": "s2", "outputs": []}],
                 steps_remaining=[])
    hp.write_text(json.dumps(good2), encoding="utf-8")
    tqext(root, env, "--json", "checkpoint", "SEC", "--worker", "alice",
          "--handoff", str(hp))
    z3 = tqext(root, env, "--json", "heartbeat", "SEC", "--worker", "alice",
               "--used", "120", "--handoff", str(hp))
    # stale 回收（落地版路径回归）：推陈旧心跳 → bob 普通 claim
    con = dbcon(root)
    con.execute("UPDATE tasks SET heartbeat_at='2000-01-01T00:00:00' WHERE id='SEC'")
    con.close()
    stale = tqext(root, env, "--json", "claim", "--worker", "bob")
    sj = json.loads(stale.stdout)
    return {"impersonation": {"bob_heartbeat_rc": bob_hb.returncode,
                              "bob_complete_rc": bob_done.returncode,
                              "msg": json.loads(bob_hb.stderr)["error"][:90]},
            "self_cycle_rc": selfcyc.returncode,
            "self_cycle_msg": json.loads(selfcyc.stderr)["error"],
            "missing_dep_rc": ghost.returncode,
            "zombie": {"first": json.loads(z1.stdout)["zombie_suspect"],
                       "second": json.loads(z2.stdout)["zombie_suspect"],
                       "after_progress": json.loads(z3.stdout)["zombie_suspect"]},
            "stale_claim": {"rc": stale.returncode,
                            "got": sj["claimed"]["id"] if sj["claimed"] else None,
                            "by": sj["claimed"]["claimed_by"] if sj["claimed"] else None,
                            "attempts": sj["claimed"]["attempts"] if sj["claimed"] else None}}


def main() -> int:
    R = REPORT["scenarios"]
    print("== S1 =="); R["S1_concurrency"] = s1(); print(R["S1_concurrency"]["atomic_ok"])
    print("== S2 =="); R["S2_touch"] = s2(); print(R["S2_touch"]["blocked_then_picked_TC"])
    print("== MAIN =="); R["MAIN_kill_resume"] = main_kill()
    print(json.dumps({k: R["MAIN_kill_resume"][k] for k in
                      ("naked_claim_got", "soft_takeover_rc", "A_did", "B_trusted",
                       "B_did", "redo_overlap", "final_status", "zero_context_ok")},
                     ensure_ascii=False))
    print("== S4 =="); R["S4_yield"] = s4()
    print(R["S4_yield"]["final"], R["S4_yield"]["rollup_ok"], R["S4_yield"]["B_did"])
    print("== S5 =="); R["S5_verify_fail"] = s5(); print(R["S5_verify_fail"]["sequence"])
    print("== S6 =="); R["S6_timing"] = s6(); print(R["S6_timing"])
    print("== S7 =="); R["S7_wal"] = s7()
    print(R["S7_wal"]["journal_mode"], R["S7_wal"]["rows"], R["S7_wal"]["all_rc0"])
    print("== S8 =="); R["S8_attacks"] = s8(); print(json.dumps(R["S8_attacks"], ensure_ascii=False))
    (HERE / "probe_report2.json").write_text(
        json.dumps(REPORT, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = (R["S1_concurrency"]["atomic_ok"] and R["S2_touch"]["blocked_then_picked_TC"]
          and R["MAIN_kill_resume"]["zero_context_ok"] and R["S4_yield"]["rollup_ok"]
          and R["S5_verify_fail"]["blocked_ok"] and R["S7_wal"]["all_rc0"]
          and R["S8_attacks"]["impersonation"]["bob_heartbeat_rc"] == 2
          and R["S8_attacks"]["self_cycle_rc"] == 2
          and R["S8_attacks"]["stale_claim"]["got"] == "SEC")
    print("\nALL_CORE_ASSERTIONS =", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
