"""554 T1：Hypothesis stateful 自动攻击 task_queue（本批最高价值回归）。

纯测试侧：只调 `tools/task_queue` 的**库函数**，DB 重定向到临时 sqlite
（`db_path` 参数已可注入，**绝不打真实 data/tasks/**）。把 545/546 手工证明的攻击面
（A3 未来心跳占坑 / A5 yield 无限续命 / A7 verify 自证）变成自动、可 shrink、持续回归。

机器模型：
- 每用例独立临时库（`__init__` 建、`teardown` 清）；
- 模拟 3 个 worker（wA/wB/wC），参数用 bounded strategy；
- `@rule` 随机枚举 enqueue/claim/heartbeat/checkpoint/yield/next/done/fail/blocked；
- `@invariant` 每步后查库断言系统铁律（无双领 / 深度上界 / 预算账 / 未来心跳 clamp / deps 门）；
- 三洞 + 重试封顶 / deps / touch 归一另有**确定性回归**（spec 要求显式锁修复序列）。

标 fast：每用例独立临时库、无共享状态、不编译、不碰 replay 锁/asm 工件。
`complete` 不进随机机器（它跑 `git status` 审计真实仓库），只在确定性场景里用。
"""
import json
import shutil
import tempfile
import time
from pathlib import Path

import pytest
import task_queue as tq
from hypothesis import HealthCheck, settings
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, initialize, invariant, rule

WORKERS = ["wA", "wB", "wC"]
TYPES = ["research", "doc", "atom_produce", "redteam", "custom", "tool_change"]
VERIFY = ["", "exit 0", "exit 1"]
# 同一物理文件的多种写法（538/539 A1：大小写 / ./ / 正反斜杠必须撞同一把锁）
TOUCH_PHYS = "Examples/atoms/_atom_fence_vs_atomic.cpp"
TOUCH_VARIANTS = [
    TOUCH_PHYS,
    TOUCH_PHYS.upper(),                 # 大小写异体
    "./" + TOUCH_PHYS,                  # ./ 前缀
    TOUCH_PHYS.replace("/", "\\"),      # 反斜杠
]
MAX_YIELD_DEPTH = tq.MAX_YIELD_DEPTH
MAX_ATTEMPTS = tq.MAX_ATTEMPTS

# 固定策略对象（**不随外部状态变化**）：stateful 里从变长集合选元素时，必须用固定整数
# 策略取模，**不能**用 `st.sampled_from(变长 list)` —— 后者会让 hypothesis 报
# `FlakyStrategyDefinition: Inconsistent data generation!`（数据生成随外部状态变化）。
_IDX = st.integers(min_value=0, max_value=63)
_K2 = st.integers(min_value=0, max_value=2)


def _pick(data, seq):
    """从（可能为空的）序列里选一个；空 ⇒ None。

    **始终先抽 `_IDX`**：抽不抽不能取决于外部状态（否则同一 choice 前缀在不同 run 里
    产生的 draw 序列长度/类型不同 ⇒ hypothesis 报 FlakyStrategyDefinition，实测
    "first: integer, second: boolean"）。外部状态只决定"这个索引用不用得上"。
    """
    idx = data.draw(_IDX)
    if not seq:
        return None
    return seq[idx % len(seq)]


# ── 共享辅助 ────────────────────────────────────────────────────────────────
def _valid_handoff(for_yield: bool = False) -> dict:
    return {
        "schema": "tq-handoff/v1",
        "goal": "续跑目标是把剩下的步骤做完",
        "next_action": "领到后从 step 1 继续推进",
        "steps_done": [],
        "verified_facts": [{"trust": "L1", "anchor": "tools/task_queue.py"}],
        "steps_remaining": [{"n": 1, "title": "做点事"}] if for_yield else [],
        "touched_files": [],
    }


def _new_db() -> Path:
    d = Path(tempfile.mkdtemp(prefix="tqdet_"))
    db = d / "queue.db"
    tq.init(db)
    return db


def _write_handoff(db: Path, tid: str, for_yield: bool = False,
                   budget_used: int = 0) -> None:
    h = _valid_handoff(for_yield)
    h["budget_used"] = budget_used     # validate_handoff 要求非负整数
    tq.handoff_path_for(tid, db).write_text(
        json.dumps(h, ensure_ascii=False), encoding="utf-8")


def _row(db: Path, tid: str) -> dict:
    conn = tq._connect(db)
    try:
        r = conn.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
        return dict(tq._as_row_dict(r)) if r else {}
    finally:
        conn.close()


def _all_rows(db: Path) -> list[dict]:
    return tq.list_tasks(db_path=db)


def _descendants_sum(rows: list[dict], root_id: str) -> int:
    """root 所有后代（不含 root 自身）的 budget_calls 之和。"""
    by_parent: dict = {}
    for r in rows:
        by_parent.setdefault(r.get("parent_task"), []).append(r)
    total, stack, seen = 0, [root_id], set()
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        for c in by_parent.get(cur, []):
            total += int(c.get("budget_calls") or 0)
            stack.append(c["id"])
    return total


# ── 确定性回归：三洞 + 铁律 ─────────────────────────────────────────────────
def test_a3_future_heartbeat_clamped():
    """546 T-A3：未来心跳 > now+30s 必须被写端 clamp，不得永久占坑。"""
    db = _new_db()
    tid = tq.enqueue("research", "p", db_path=db)["id"]
    tq.claim("wA", db_path=db)
    fut = tq._fmt_utc(time.time() + 3600)           # 未来 1 小时
    tq.heartbeat(tid, "wA", at=fut, db_path=db)
    row = _row(db, tid)
    assert not tq._is_future_ts(row["heartbeat_at"]), \
        f"未来心跳未被 clamp，仍可被误认为有效租约：{row['heartbeat_at']}"
    # clamp 后心跳为 now ⇒ 仍在租约宽限内，裸接管被拒；人 --force 接管须成功
    res = tq.claim("wB", db_path=db, takeover=tid, force=True, reason="旧会话已死")
    assert res.get("claimed") or res.get("taken_over"), "force 接管应成功"


def test_a5_yield_depth_cap():
    """546 T-A5：子任务 depth = 父 depth+1，> MAX_YIELD_DEPTH 须拒（无 --force 不断续命）。"""
    db = _new_db()
    root = tq.enqueue("research", "root", budget=500, db_path=db)["id"]
    tq.claim("wA", db_path=db)
    # 让剩余 < YIELD_BUDGET_LEFT(100) ⇒ 无需 --force 即可让出（从而真正走到深度闸）
    _write_handoff(db, root, for_yield=True, budget_used=420)   # left=80<100
    tq.yield_task(root, "wA", db_path=db)                       # root(0) -> A(1)
    a = next(r["id"] for r in _all_rows(db)
              if r.get("parent_task") == root and r["status"] == "queued")
    tq.claim("wA", db_path=db)
    _write_handoff(db, a, for_yield=True, budget_used=0)         # 子预算 80，left=80<100
    tq.yield_task(a, "wA", db_path=db)                          # A(1) -> B(2)
    b = next(r["id"] for r in _all_rows(db)
              if r.get("parent_task") == a and r["status"] == "queued")
    tq.claim("wA", db_path=db)
    _write_handoff(db, b, for_yield=True, budget_used=0)
    tq.yield_task(b, "wA", db_path=db)                          # B(2) -> C(3)
    c = next(r["id"] for r in _all_rows(db)
              if r.get("parent_task") == b and r["status"] == "queued")
    tq.claim("wA", db_path=db)
    _write_handoff(db, c, for_yield=True, budget_used=0)
    with pytest.raises(SystemExit):                             # C(3) -> 4 必须拒（深度闸）
        tq.yield_task(c, "wA", db_path=db)
    for r in _all_rows(db):
        assert int(r.get("depth") or 0) <= MAX_YIELD_DEPTH, \
            f"出现超深任务：{r['id']} depth={r['depth']}"


def test_a7_verify_self_needs_review():
    """546 T-A7：custom verify（自带考卷）rc=0 且无异方/人签 ⇒ 不得裸 done（须 needs_review）。"""
    db = _new_db()
    tid = tq.enqueue("research", "p", verify_cmd="exit 0", db_path=db)["id"]
    tq.claim("wA", db_path=db)
    r = tq.complete(tid, "wA", result_ref="data/tasks/x.out", db_path=db)
    assert r["status"] == "needs_review", \
        f"custom verify 无 second-party 竟裸 done：{r}"
    r2 = tq.complete(tid, "wA", result_ref="data/tasks/x.out",
                     second_party="wB", db_path=db)
    assert r2["status"] == "done", "异方确认后应 done"
    # 另起一张卡测人签 --force
    tid2 = tq.enqueue("research", "p2", verify_cmd="exit 0", db_path=db)["id"]
    tq.claim("wA", db_path=db)
    r3 = tq.complete(tid2, "wA", result_ref="data/tasks/y.out",
                     force=True, reason="人签放行", db_path=db)
    assert r3["status"] == "done", "人签 --force 应 done"


def test_retry_cap_blocked():
    """attempts > MAX_ATTEMPTS ⇒ 自动 blocked（防无限重试）。"""
    db = _new_db()
    tid = tq.enqueue("research", "p", verify_cmd="exit 1", db_path=db)["id"]
    for _ in range(MAX_ATTEMPTS + 2):
        tq.claim("wA", db_path=db)
        try:
            tq.complete(tid, "wA", result_ref="data/tasks/x.out", db_path=db)
        except SystemExit:
            pass
        if _row(db, tid).get("status") == "blocked":
            break
    assert _row(db, tid).get("status") == "blocked", "超重试上限应 blocked"


def test_deps_gate():
    """依赖未 done 的任务不被 next/claim 放行。"""
    db = _new_db()
    a = tq.enqueue("research", "A", db_path=db)["id"]
    b = tq.enqueue("research", "B", deps=[a], db_path=db)["id"]
    res = tq.next_task(db_path=db)
    assert res.get("next") is None or res["next"]["id"] != b, "deps 未完成却被放行"
    tq.claim("wA", db_path=db)
    tq.done(a, "wA", db_path=db)
    res2 = tq.next_task(db_path=db)
    assert res2.get("next") and res2["next"]["id"] == b, "A done 后 B 应可 next"


def test_touch_normalization_same_lock():
    """538/539 A1：touch 的大小写 / ./ / 正反斜杠异体必须撞同一把锁。"""
    db = _new_db()
    # T1 给最高优先级 ⇒ claim 必领 T1（占用其 touch 锁）；T2 用异体应被挡下
    t1 = tq.enqueue("research", "T1", touch=[TOUCH_PHYS], priority=200, db_path=db)["id"]
    t2 = tq.enqueue("research", "T2", touch=[TOUCH_VARIANTS[1]], db_path=db)["id"]
    claimed_id = tq.claim("wA", db_path=db)["claimed"]["id"]   # 占住其 touch 锁
    nb = tq.next_task(db_path=db).get("blocked_by_touch", [])
    blocked_ids = {x["id"] for x in nb}
    # 归一化成立 ⇒ T1/T2 争同一把锁：被领走的那个之外，另一个必被挡下
    assert blocked_ids & {t1, t2} == {t1, t2} - {claimed_id}, \
        f"touch 异体未归一（应挡下 {t1, t2} - {claimed_id}）：{nb}"


# ── 随机状态机：自动找违反序列 ─────────────────────────────────────────────
class TQMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self._dir = Path(tempfile.mkdtemp(prefix="tqst_"))
        self.db = self._dir / "queue.db"
        tq.init(self.db)
        self._n = 0
        self.known: set[str] = set()          # 已知 task id
        self.claimed: dict[str, str] = {}     # task_id -> 有效持有者

    def teardown(self):
        shutil.rmtree(self._dir, ignore_errors=True)

    def _new_payload(self) -> str:
        self._n += 1
        return f"payload_{self._n}"

    @initialize()
    def seed(self):
        for _ in range(3):
            self.known.add(tq.enqueue("research", self._new_payload(),
                                      db_path=self.db)["id"])

    @rule(data=st.data())
    def enqueue_task(self, data):
        # 所有 draw **无条件、按固定顺序**执行（顺序/类型不随外部状态变）；
        # 外部状态（self.known / with_touch 之后的取值）只决定用哪几个值。
        ptype = data.draw(st.sampled_from(TYPES))
        priority = data.draw(st.integers(0, 200))
        budget = data.draw(st.integers(50, 1000))
        verify = data.draw(st.sampled_from(VERIFY))
        with_touch = data.draw(st.booleans())
        touch_variant = data.draw(st.sampled_from(TOUCH_VARIANTS))
        k = data.draw(_K2)                              # 依赖候选数 0..2
        dep_idxs = [data.draw(_IDX) for _ in range(k)]
        pool = sorted(self.known)
        touch = [touch_variant] if with_touch else None
        deps = [pool[i % len(pool)] for i in dep_idxs] if pool else []
        deps = list(dict.fromkeys(deps))                # 去重
        # 注：随机机器里 enqueue **不**带 parent——深度/预算账只由 yield 产生，
        # 这两个不变量（A5）按 spec 仅约束 yield 续命，避免 enqueue(parent) 的设计
        # 边界制造假阳性。enqueue(parent) 行为另行确定性覆盖。
        tid = tq.enqueue(ptype, self._new_payload(), priority=priority,
                         deps=deps, db_path=self.db,
                         touch=touch, verify_cmd=verify,
                         budget=budget, worker="enqueuer")["id"]
        self.known.add(tid)

    @rule(data=st.data())
    def claim_task(self, data):
        # 所有 draw 无条件（结构固定）；外部状态 self.claimed 只决定走 A 还是 B。
        takeover = data.draw(st.booleans())
        t_idx = data.draw(_IDX)
        o_idx = data.draw(_IDX)
        worker = data.draw(st.sampled_from(WORKERS))
        items = list(self.claimed.items())
        if takeover and items:
            # 模式 A：抢已被他人持有的任务（无 takeover/force 必须被拒）⇒ 无双领
            tid, owner = items[t_idx % len(items)]
            cands = [w for w in WORKERS if w != owner]
            other = cands[o_idx % len(cands)]
            try:
                res = tq.claim(other, db_path=self.db, takeover=tid,
                               force=False, reason="")
            except SystemExit:
                res = {"claimed": None}
            got = res.get("claimed")
            if got and got["id"] == tid:
                # 合法的 stale 接管（罕见：心跳已过期）→ 持有权转移
                self.claimed[tid] = other
            else:
                # 裸接管被拒（在租约内）⇒ 原持有仍有效，且不应出现别人抢到 tid
                assert got is None or got["id"] != tid, \
                    f"无双领被破坏：{other} 抢到了 {owner} 持有的 {tid}"
                assert self.claimed.get(tid) == owner, "被抢方仍应持有"
            return
        # 模式 B：派个 worker 去领（claim 自己挑最高优先级 queued）
        res = tq.claim(worker, db_path=self.db)
        if res.get("claimed"):
            # 记**实际领到**的 id（claim 按优先级挑，未必是某个特定候选）
            self.claimed[res["claimed"]["id"]] = worker

    @rule(data=st.data())
    def heartbeat_task(self, data):
        pick = _pick(data, list(self.claimed.items()))
        future = data.draw(st.booleans())
        if pick is None:
            return
        tid, owner = pick
        at = tq._fmt_utc(time.time() + 3600) if future else None
        try:
            tq.heartbeat(tid, owner, at=at, db_path=self.db)
        except SystemExit:
            pass

    @rule(data=st.data())
    def checkpoint_task(self, data):
        pick = _pick(data, list(self.claimed.items()))
        if pick is None:
            return
        tid, owner = pick
        _write_handoff(self.db, tid, for_yield=False)
        try:
            tq.checkpoint(tid, owner, db_path=self.db)
        except SystemExit:
            pass  # handoff 质量不过 ⇒ 拒绝（合理）

    @rule(data=st.data())
    def yield_task(self, data):
        pick = _pick(data, list(self.claimed.items()))
        if pick is None:
            return
        tid, owner = pick
        budget = int(_row(self.db, tid).get("budget_calls") or 0)
        # 让剩余 < YIELD_BUDGET_LEFT(100) ⇒ 无需 --force 即可让出（走到深度/预算闸）
        _write_handoff(self.db, tid, for_yield=True, budget_used=max(0, budget - 50))
        try:
            r = tq.yield_task(tid, owner, db_path=self.db)
        except SystemExit:
            return  # 预算/深度/质量闸门拒绝（合理）
        for c in r.get("children", []):
            self.known.add(c)   # 子任务切出为 queued，未被持有

    @rule(data=st.data())
    def next_task_rule(self, data):
        res = tq.next_task(db_path=self.db)
        nxt = res.get("next")
        if nxt:
            by_id = {r["id"]: r for r in _all_rows(self.db)}
            for d in nxt.get("deps", []):
                assert by_id.get(d, {}).get("status") == "done", \
                    f"next 返回 deps 未完成的任务 {nxt['id']}"

    @rule(data=st.data())
    def terminal_task(self, data):
        pick = _pick(data, list(self.claimed.items()))
        action = data.draw(st.sampled_from(["done", "fail", "blocked"]))  # 始终抽
        if pick is None:
            return
        tid, owner = pick
        if action == "done":
            tq.done(tid, owner, db_path=self.db)
        elif action == "fail":
            tq.fail(tid, owner, error="x", db_path=self.db)
        else:
            tq.blocked(tid, owner, reason="x", db_path=self.db)
        # 状态已变，inv_no_double 会把它从 self.claimed 清掉

    # ── invariants（每步后查库断言铁律）──
    @invariant()
    def inv_no_double(self):
        for tid, owner in list(self.claimed.items()):
            row = _row(self.db, tid)
            if not row or row.get("status") != "claimed":
                self.claimed.pop(tid, None)
            else:
                assert row.get("claimed_by") == owner, \
                    f"双领：{tid} claimed_by={row.get('claimed_by')} 但应 {owner}"

    @invariant()
    def inv_db_consistency(self):
        """深度上界 + yield 预算账 + 未来心跳 clamp：一次读库三查合一（省连接开销）。"""
        rows = _all_rows(self.db)
        now = time.time()
        for r in rows:
            assert int(r.get("depth") or 0) <= MAX_YIELD_DEPTH, \
                f"深度 {r.get('depth')} > {MAX_YIELD_DEPTH}"
            if not r.get("parent_task"):       # 每个根任务：后代预算和 ≤ 根预算
                desc = _descendants_sum(rows, r["id"])
                assert desc <= int(r.get("budget_calls") or 0), \
                    f"预算超发：{r['id']} 后代 {desc} > 根 {r.get('budget_calls')}"
            if r.get("status") == "claimed" and r.get("heartbeat_at"):
                assert not tq._is_future_ts(r["heartbeat_at"]), \
                    f"未来心跳未被 clamp：{r['heartbeat_at']} (now={now:.0f})"


class TestTQ(TQMachine.TestCase):
    # 100-200 例；deadline=None（状态机每步独立临时库，但可能较多 DB 往返）
    settings = settings(
        max_examples=120,
        deadline=None,
        # 抑制全部健康检查（stateful + 真实时钟/sqlite/临时文件的固有非确定性）：
        #  - filter_too_much：大量 rule 带前置条件（self.claimed 非空等），filter 率天然偏高；
        #  - differing_executors：机器触真实时钟（heartbeat）与 sqlite 文件 ⇒ 两次执行器可能
        #    观测到细微差异，属环境噪声而非被测逻辑的分歧，抑制之；
        #  - too_slow/data_too_large/large_base_example/nested_given：与本测试无关。
        suppress_health_check=list(HealthCheck),
    )
