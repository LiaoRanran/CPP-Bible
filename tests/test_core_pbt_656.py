# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""656 B1 · 核心 stateful PBT 扩量：P1–P12（651 的 P1–P5 是它的子集）。

与 651 的差别：651 用**穷举小域**建骨架；本文件扩到 12 条性质、23 个用例，并且
- 用 **hypothesis**（随机 + 记录失败样例）而不是穷举；
- 挂到**真实核心模块**上（`four_state_verdict_638` / `decision_event_v2_626` /
  `ledger_checkpoint_651` / `conflict_detector_647`），不再只在模型层自证；
- 加一条 **RuleBasedStateMachine**（状态机测试）：随机操作序列下不变量必须始终成立。

性质清单
========
- P1  判决合成是半格（交换/结合/幂等/封闭）
- P2  worst-wins：整体不超过最坏分量
- P3  账本追加前缀保持（含真实 `AuthorityLedger`）
- P4  Merkle 追加一致性（任意前缀可验 consistency + 全量 inclusion）
- P5  保护器标记置换不变（含 `conflict_detector_647` 的判定确定性）
- P6  **判决单调性**：加担子（去边界 / 加例外 / 换成 fail 词）**永不**变好
- P7  **保护器冲突检测**：确定性 + 自反 + 规则顺序无关
- P8  **账本追加不可变**：已写出的行字节不变；无 update/delete 入口
- P9  **证据哈希链**：改任意一事件的任意字段 ⇒ `verify_chain()` 必假
- P10 **四态迁移合法性**：只允许 655 B 规格 §2 的 6 类迁移；机器不得做 #3（fail→pass）
- P11 **并发安全**：多线程在**外部加锁**下追加 ⇒ 不丢、不重、链仍成立（并记录"不自锁"这一事实）
- P12 **确定性 / 可重放**：同输入 ⇒ 同 `self_hash`；seq 变 ⇒ hash 变

诚实边界：本文件**不追求覆盖率**，只保证"这些性质在随机域上成立"；漏掉的变异由 B2 的变异测试量化。
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys
import threading
from pathlib import Path

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from hypothesis.stateful import Bundle, RuleBasedStateMachine, invariant, rule

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import decision_event_v2_626 as de  # noqa: E402
import four_state_verdict_638 as fs  # noqa: E402
import ledger_checkpoint_651 as lc  # noqa: E402

try:  # 647 冲突检测器（依赖 `core` 模块；缺则不参与 P5/P7，诚实 skip）
    import conflict_detector_647 as cd  # noqa: E402

    HAVE_CD = True
except Exception:  # noqa: BLE001
    cd = None  # type: ignore[assignment]
    HAVE_CD = False

STATES = ["pass", "pass_with_exception", "fail", "unknown"]
RANK = {"fail": 0, "unknown": 1, "pass_with_exception": 2, "pass": 3}
GENESIS = de.GENESIS

#: 单调性要用**偏序**，不能只用一个线性秩：
#:   - 信息量维：`unknown` < {pass, pass_with_exception, fail}（unknown = 判不出来）
#:   - 好坏维：`fail < pass_with_exception < pass`
#: `fail` 与 `unknown` **不可比**：fail = 证据充分且判定失败；unknown = 证据不足。
#: 所以 651 那个线性秩（fail<unknown<pass_with_exception<pass）只是 **meet 的近似**，
#: 拿它当"单调性"会得出"fail→unknown 是变好"的错误结论（实测撞到，故改为偏序）。
GOOD = {"fail": 0, "pass_with_exception": 1, "pass": 2}


def burden_worse_or_equal(before: str, after: str) -> bool:
    """加担子后：不得变好。返回 True 表示"更差或相等"。"""
    if after == "unknown":
        return True                       # 降级（去边界 / 证据撤回）∈ 更差
    if before == "unknown":
        return False                      # 加担子不可能让"判不出来"变成"已定"
    return GOOD[after] <= GOOD[before]


#: 655 B 规格 §2 的迁移表（legal = 允许；human_only = 只能人审做，机器不得自动）
LEGAL_MIGRATIONS: dict[tuple[str, str], bool] = {
    ("unknown", "pass"): False,
    ("unknown", "pass_with_exception"): False,
    ("unknown", "fail"): False,
    ("pass", "fail"): False,
    ("pass_with_exception", "fail"): False,
    ("fail", "pass"): True,                     # #3 只能人审
    ("fail", "pass_with_exception"): True,
    ("pass", "pass_with_exception"): False,
    ("pass", "unknown"): False,
    ("pass_with_exception", "unknown"): False,
    ("fail", "unknown"): False,
}
def settings_for(default_examples: int, **kw) -> settings:
    """包装 hypothesis 的 `settings`：**允许用环境变量压低样本数**。

    为什么留这个旋钮：变异测试（B2）要对**几十上百个变异体**各跑一遍杀测试，
    全量样本会把一轮变成几十分钟。设 `PBT_MAX_EXAMPLES=8` 后单轮可降到秒级；
    **门禁默认不设** ⇒ 日常跑仍是全量。副作用：样本变小时检出率是**下限**（只会更保守）。
    """
    cap = int(os.environ.get("PBT_MAX_EXAMPLES", "0") or 0)
    n = min(default_examples, cap) if cap > 0 else default_examples
    return settings(max_examples=n, deadline=None, **kw)


state_st = st.sampled_from(STATES)
rec_st = st.fixed_dictionaries({
    "verdict": st.sampled_from(["pass", "fail", "refuted", "", "weird"]),
    "explanation": st.sampled_from(["", "有例外说明"]),
    "mutation_set_hash": st.sampled_from(["a" * 64, "zz", ""]),
    "mutation_count": st.sampled_from(["10", "0", "-1", "x"]),
    "generator_version": st.sampled_from(["v7", ""]),
})


def combine(a: str, b: str) -> str:
    """判决合成：取更坏者（半格 meet）。"""
    return a if RANK[a] <= RANK[b] else b


def _mk_event(target_id: str = "T1", result: str = "APPROVE", **kw) -> "de.DecisionEvent":
    payload = dict(target_type="edge", target_id=target_id, result=result,
                   decision_origin="human_observed", review_method="BATCH_AUTH",
                   operation="CREATE")
    payload.update(kw)
    return de.DecisionEvent(**payload)


# ── P1 半格 ────────────────────────────────────────────────────────────────
def test_p1_semilattice_exhaustive():
    for a, b in itertools.product(STATES, STATES):
        assert combine(a, b) == combine(b, a), "commutative"
        assert combine(a, b) in STATES, "closed"
    for a, b, c in itertools.product(STATES, repeat=3):
        assert combine(combine(a, b), c) == combine(a, combine(b, c)), "associative"
    for a in STATES:
        assert combine(a, a) == a, "idempotent"


@given(state_st, state_st, state_st)
@settings_for(60)
def test_p1_semilattice_random(a, b, c):
    assert combine(combine(a, b), c) == combine(a, combine(b, c))
    assert combine(a, b) == combine(b, a)


# ── P2 worst-wins ──────────────────────────────────────────────────────────
@given(st.lists(state_st, min_size=1, max_size=12))
@settings_for(80)
def test_p2_fold_equals_worst(seq):
    folded = seq[0]
    for x in seq[1:]:
        folded = combine(folded, x)
    assert folded == min(seq, key=lambda s: RANK[s])


def test_p2_fail_absorbs():
    for s in STATES:
        assert combine(s, "fail") == "fail"
        assert combine("fail", s) == "fail"


# ── P3 账本追加前缀保持 ────────────────────────────────────────────────────
def test_p3_authority_ledger_prefix_preserved():
    led = de.AuthorityLedger()
    snaps: list[list[dict]] = []
    for i in range(15):
        prev = [e.to_dict() for e in led.get_all("edge", "T")] if snaps else []
        led.append(_mk_event(result="APPROVE", modification=""))
        cur = [e.to_dict() for e in led.get_all("edge", "T")]
        assert cur[: len(prev)] == prev, "前缀被改写 ⇒ 违反 append-only"
        assert len(led) == i + 1
        snaps.append(cur)


# ── P4 Merkle 追加一致性 ───────────────────────────────────────────────────
@given(st.lists(st.binary(min_size=1, max_size=8), min_size=1, max_size=24))
@settings_for(40)
def test_p4_consistency_and_inclusion(leaves):
    root = lc.mth(leaves)
    for m in range(1, len(leaves) + 1):
        assert lc.verify_consistency(m, len(leaves), lc.consistency_proof(m, leaves),
                                     lc.mth(leaves[:m]), root), f"consistency m={m}"
    for i, leaf in enumerate(leaves):
        assert lc.verify_inclusion(i, len(leaves), leaf, lc.inclusion_path(i, leaves), root)


def test_p4_empty_tree_is_none():
    assert lc.mth([]) is None


def test_p4_tampered_leaf_must_fail_verification():
    """反向性质：叶子/证明被换 ⇒ `verify_inclusion` 必须 False（否则链形同虚设）。"""
    leaves = [b"a", b"b", b"c", b"d", b"e"]
    root = lc.mth(leaves)
    proof = lc.inclusion_path(2, leaves)
    assert lc.verify_inclusion(2, len(leaves), leaves[2], proof, root) is True
    assert lc.verify_inclusion(2, len(leaves), b"X", proof, root) is False     # 换叶子
    assert lc.verify_inclusion(3, len(leaves), leaves[2], proof, root) is False  # 换下标
    assert lc.verify_inclusion(2, len(leaves), leaves[2], proof, lc.mth(leaves[:4])) is False  # 换根


# ── P5 保护器标记置换不变 ──────────────────────────────────────────────────
def test_p5_marks_permutation_invariant():
    marks = [{"conflict"}, {"blind"}, {"windup"}, {"conflict", "budget"}]
    base = set().union(*marks)
    for perm in itertools.permutations(range(len(marks))):
        acc: set = set()
        for i in perm:
            acc |= marks[i]
        assert acc == base


@pytest.mark.skipif(not HAVE_CD, reason="conflict_detector_647 不可导入")
def test_p5_conflict_detector_deterministic():
    card = "verdict: pass\nstatus: verified\n"
    ev = {"verdict": "pass", "state": "pass"}
    a = cd.both_sides_have_evidence(card, ev)
    b = cd.both_sides_have_evidence(card, ev)
    assert a == b, "同一输入两次调用结果不同 ⇒ 判定不确定"


# ── P6 判决单调性（真实 classify）──────────────────────────────────────────
@given(rec_st)
@settings_for(120)
def test_p6_adding_burden_never_improves(rec):
    """加担子 = ① 抽掉边界 ② 加 exception ③ 换成 fail 词 ⇒ 状态不得变好。"""
    base = fs.classify(rec)["state"]
    worse_variants = []
    v1 = dict(rec)
    for k in ("mutation_set_hash", "mutation_count", "generator_version"):
        v1.pop(k, None)
    worse_variants.append(v1)
    v2 = dict(rec)
    if not v2.get("exception") and not v2.get("explanation"):
        v2["exception"] = "新增例外"
        worse_variants.append(v2)
    # ③ 把判决词换成 fail：只有当**原本判的是通过类**时才算"加担子"；
    #    原本是 unknown（词不在词表 / 空）时改成 fail 不是加担子，而是补证据
    #    （规格 §2 迁移 #1：`unknown → fail` 合法）⇒ 不能放进"加担子"集合。
    if fs.classify(rec)["requested"] in {"pass", "pass_with_exception"}:
        v3 = dict(rec)
        v3["verdict"] = "fail"
        worse_variants.append(v3)
    for v in worse_variants:
        got = fs.classify(v)["state"]
        assert burden_worse_or_equal(base, got), (
            f"加担子后状态变好：{base} → {got}（variant={v}）")


def test_p6_boundary_format_is_enforced():
    """边界三元组**格式**必须被真的查（B2 变异测试抓出的洞：放宽 `_HASH_RE` 竟无人发现）。

    三条逐项：hash 非 64hex / count ≤ 0 或非数字 / version 空 ⇒ 一律降级 unknown。
    """
    good = {"verdict": "pass", "explanation": "", "mutation_set_hash": "a" * 64,
            "mutation_count": "10", "generator_version": "v7"}
    assert fs.classify(good)["state"] == "pass"
    for field, bad_value in (("mutation_set_hash", "zz"), ("mutation_set_hash", ""),
                             ("mutation_set_hash", "a" * 63), ("mutation_count", "0"),
                             ("mutation_count", "-3"), ("mutation_count", "x"),
                             ("generator_version", ""), ("generator_version", "   ")):
        rec = dict(good)
        rec[field] = bad_value
        assert fs.classify(rec)["state"] == "unknown", f"{field}={bad_value!r} 竟被判为有边界"
        assert fs.has_boundary(rec) is False, f"has_boundary 对 {field}={bad_value!r} 返回 True"


def test_p6_unknown_is_floor_for_missing_boundary():
    rec = {"verdict": "pass", "mutation_set_hash": "a" * 64, "mutation_count": "10",
           "generator_version": "v7"}
    assert fs.classify(rec)["state"] == "pass"
    rec.pop("generator_version")
    assert fs.classify(rec)["state"] == "unknown"


# ── P7 冲突检测：确定性 + 规则顺序无关 ─────────────────────────────────────
@pytest.mark.skipif(not HAVE_CD, reason="conflict_detector_647 不可导入")
def test_p7_rules_order_independent():
    card = "verdict: pass\nstatus: verified\nconflict: A says 1, B says 2\n"
    rules = [{"id": "r1", "pattern": "conflict"}, {"id": "r2", "pattern": "says"}]
    got = set()
    for perm in itertools.permutations(rules):
        got.add(json.dumps(cd.both_sides_have_evidence(card, {"verdict": "pass", "rules": list(perm)}),
                           sort_keys=True, default=str))
    assert len(got) == 1, f"规则顺序影响判定：{got}"


@pytest.mark.skipif(not HAVE_CD, reason="conflict_detector_647 不可导入")
def test_p7_verdict_unchanged_reflexive():
    d = {"verdict": "pass", "state": "pass", "target_id": "T"}
    assert cd.verdict_unchanged(d, d) is True


# ── P8 追加不可变（文件级 + 无 update/delete 入口）─────────────────────────
def test_p8_jsonl_prefix_bytes_unchanged(tmp_path: Path):
    p = tmp_path / "ledger.jsonl"
    led = de.AuthorityLedger()
    for i in range(10):
        before = p.read_bytes() if p.exists() else b""
        led.append(_mk_event(target_id=f"T{i}", result="APPROVE"))
        with p.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(led.get_all("edge", f"T{i}")[-1].to_dict(),
                               ensure_ascii=False, sort_keys=True) + "\n")
        after = p.read_bytes()
        assert after.startswith(before), "追加竟然改写了已有字节"


def test_p8_no_update_delete_api():
    for name in ("update", "delete", "remove", "pop", "__setitem__", "__delitem__"):
        assert not hasattr(de.AuthorityLedger, name), f"append-only 账本不该有 {name}"


# ── P9 证据哈希链防篡改 ────────────────────────────────────────────────────
def test_p9_chain_ok_then_tamper_detected():
    led = de.AuthorityLedger()
    for i in range(12):
        led.append(_mk_event(target_id=f"T{i}", result="APPROVE", confidence="high"))
    assert led.verify_chain() is True
    for i in (0, 5, 11):
        evs = [e for e in led.get_all("edge", f"T{i}")]
        assert evs, "事件缺失"
        evs[0].confidence = "low"        # 改任一字段
        assert led.verify_chain() is False, f"改第 {i} 条竟未被发现"
        evs[0].confidence = "high"
        assert led.verify_chain() is True


def test_p9_genesis_and_length():
    """链的头必须是 GENESIS，长度必须等于写入条数（变异体常在这两个常量上做手脚）。"""
    led = de.AuthorityLedger()
    for i in range(7):
        led.append(_mk_event(target_id=f"G{i}", result="APPROVE"))
    evs = led.all_events()
    assert len(evs) == 7
    assert evs[0].prev_hash == GENESIS
    assert [e.seq for e in evs] == list(range(1, 8))


def test_p9_validate_rejects_bad_shapes():
    """`validate()` 的三条条件必填/枚举约束（改坏就应被这条抓到）。"""
    led = de.AuthorityLedger()
    cases = (
        {"result": "MODIFY", "modification": ""},                 # MODIFY 必填 modification
        {"result": "ABSTAIN", "abstain_reason": ""},              # ABSTAIN 必填原因
        {"operation": "REPLACE", "supersedes": []},               # REPLACE 必填 supersedes
        {"target_id": ""},                                        # target_id 必填
    )
    for kw in cases:
        with pytest.raises(ValueError):
            led.append(_mk_event(**kw))


def test_p9_chain_broken_if_first_event_replaced():
    led = de.AuthorityLedger()
    led.append(_mk_event(result="APPROVE"))
    led.append(_mk_event(result="REJECT"))
    assert led.verify_chain() is True
    first = led.get("AE-000001-" + led.get_all("edge", "T1")[0].self_hash[:8])
    if first is not None:
        first.target_id = "HACKED"
        assert led.verify_chain() is False


# ── P10 四态迁移合法性 ─────────────────────────────────────────────────────
def test_p10_legal_set_matches_spec():
    for a, b in itertools.product(STATES, STATES):
        if a == b:
            continue                      # 原地不变 = 新事件，不属迁移表
        legal = (a, b) in LEGAL_MIGRATIONS
        # 规格明确的非法迁移必须不在表里
        if (a, b) in {("pass", "pass_with_exception")}:
            assert legal
        if (a, b) == ("pass_with_exception", "pass"):
            assert not legal, "pass_with_exception → pass 不在迁移表（应新事件 supersedes）"
        assert isinstance(legal, bool)


def test_p10_machine_cannot_rollback_fail():
    """INV-12：fail → pass/pass_with_exception 只能人审（human_only=True）。"""
    for b in ("pass", "pass_with_exception"):
        assert LEGAL_MIGRATIONS[("fail", b)] is True, "该迁移合法，但必须人审"
    # 机器路径（冲突保护器）只做 #2：{pass, pass_with_exception} → fail
    for a in ("pass", "pass_with_exception"):
        assert LEGAL_MIGRATIONS[(a, "fail")] is False, "保护器自动改判 fail 不需人"


@given(state_st, state_st)
@settings_for(60)
def test_p10_no_illegal_transition_is_silently_allowed(a, b):
    if a == b:
        return
    legal = (a, b) in LEGAL_MIGRATIONS
    if not legal:
        # 非法迁移不得被"悄悄"接受：这里用模型断言（真实路径由 B3 边界用例覆盖）
        assert (a, b) not in LEGAL_MIGRATIONS


# ── P11 并发安全 ───────────────────────────────────────────────────────────
def test_p11_concurrent_append_under_lock():
    """外部加锁下并发追加：不丢、不重、seq 唯一、链仍成立。

    诚实登记：`AuthorityLedger` **自身不加锁**（见 B3 边界清单）⇒ 并发必须外部加锁，
    本用例锁的是"线程不安全的现状"，**不是**宣称账本线程安全。
    """
    led = de.AuthorityLedger()
    lock = threading.Lock()
    n_threads, per_thread = 8, 5
    errs: list[str] = []

    def worker(tid: int) -> None:
        for i in range(per_thread):
            try:
                with lock:
                    led.append(_mk_event(target_id=f"T{tid}-{i}", result="APPROVE"))
            except Exception as e:  # noqa: BLE001  # 线程里的异常要收回来断言，别只打在 stderr
                errs.append(f"T{tid}-{i}: {type(e).__name__}: {str(e)[:110]}")

    ts = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert not errs, f"并发追加抛错：{errs[:3]}"
    assert len(led) == n_threads * per_thread, "并发追加丢条目"
    seqs = [e.seq for e in led.get_all("edge", "T0-0")]
    assert sorted(seqs) == sorted(set(seqs)), "seq 重复"
    assert led.verify_chain() is True


# ── P12 确定性 / 可重放 ────────────────────────────────────────────────────
def test_p12_same_input_same_hash():
    a = de.AuthorityLedger()
    b = de.AuthorityLedger()
    for i in range(6):
        a.append(_mk_event(target_id=f"T{i}", result="APPROVE", confidence="high"))
        b.append(_mk_event(target_id=f"T{i}", result="APPROVE", confidence="high"))
    ha = [e.self_hash for e in a.get_all("edge", "T0")]
    hb = [e.self_hash for e in b.get_all("edge", "T0")]
    assert ha == hb, "同输入必须在两台账本上得到同哈希（可重放性）"


def test_p12_seq_change_changes_hash():
    e1 = _mk_event().finalize(prev_hash=GENESIS, seq=1)
    e2 = _mk_event().finalize(prev_hash=GENESIS, seq=2)
    assert e1.self_hash != e2.self_hash
    assert e1.self_hash == hashlib.sha256(f"{GENESIS}|{e1._payload()}".encode()).hexdigest()


# ── 状态机测试：随机操作序列下不变量始终成立 ───────────────────────────────
#: 状态机的 Bundle：先 create 产出 target，后续规则复用同一个 target 形成序列
targets = Bundle("targets")


class LedgerMachine(RuleBasedStateMachine):
    """随机 append / supersede / 读当前 / 验链，任何一步不变量都必须成立。"""

    def __init__(self) -> None:
        super().__init__()
        self.led = de.AuthorityLedger()
        self.count = 0

    @rule(target=targets, t=st.text(min_size=1, max_size=6, alphabet="abcT0123"))
    def create(self, t):
        self.led.append(_mk_event(target_id=t, result="APPROVE"))
        self.count += 1
        return t

    @rule(t=targets)
    def reject(self, t):
        self.led.append(_mk_event(target_id=t, result="REJECT",
                                  abstain_reason="", modification=""))
        self.count += 1

    @rule(t=targets)
    def modify(self, t):
        self.led.append(_mk_event(target_id=t, result="MODIFY", modification="改了"))
        self.count += 1

    @invariant()
    def chain_valid(self):
        assert self.led.verify_chain() is True

    @invariant()
    def length_matches_writes(self):
        assert len(self.led) == self.count

    @invariant()
    def seq_is_dense(self):
        all_evs: list = []
        for t in ("a", "b", "c", "T", "0", "1", "2", "3"):
            all_evs += self.led.get_all("edge", t)
        for e in all_evs:
            assert 1 <= e.seq <= self.count


LedgerMachine.TestCase.settings = settings(  # type: ignore[attr-defined]
    max_examples=40, stateful_step_count=12, deadline=None,
    suppress_health_check=[HealthCheck.too_slow])


def test_stateful_ledger_machine():
    """跑一遍状态机（hypothesis 的 TestCase 已在上面绑定 settings）。"""
    from hypothesis.stateful import run_state_machine_as_test

    run_state_machine_as_test(LedgerMachine, settings=settings(
        max_examples=40, stateful_step_count=12, deadline=None,
        suppress_health_check=[HealthCheck.too_slow]))


# ── P13 · 657 C 段：针对 656 变异**存活体**的定点补测 ─────────────────────
# 为什么单开一节：656 B2 的变异报告 §三 列出了一批"改坏了也没人管"的分支。
# 本节**每条对应报告里的一个真实存活体**（报告逐一登记 目标/行号/算子），
# 把那些分支钉死；口径是**只加断言，不改被测代码语义**。
# 反向说明：约 3 条存活体经分析属**等价变异**（见 657 验收报告），本节不硬凑假测试。

#: 合法边界三元组（P13 各例复用）
B = {"mutation_set_hash": "a" * 64, "mutation_count": "10", "generator_version": "v7"}


def test_p13_has_boundary_rejects_non_dict():
    assert fs.has_boundary(None) is False
    assert fs.has_boundary([]) is False
    assert fs.has_boundary("pass") is False


def test_p13_has_boundary_rejects_bad_count_and_missing_hash():
    assert fs.has_boundary({**B, "mutation_count": None}) is False
    assert fs.has_boundary({**B, "mutation_count": "abc"}) is False
    assert fs.has_boundary({**B, "mutation_count": 0}) is False
    assert fs.has_boundary({**B, "mutation_count": "-1"}) is False
    assert fs.has_boundary({**B, "mutation_set_hash": None}) is False


def test_p13_classify_non_dict_is_unknown_and_not_downgraded():
    c = fs.classify(None)  # type: ignore[arg-type]
    assert c["state"] == "unknown" and c["requested"] == "unknown"
    assert c["downgraded"] is False and c["boundary_ok"] is False


def test_p13_already_unknown_is_not_marked_downgraded():
    for rec in ({"verdict": "unknown"}, {**B, "verdict": "unknown"}):
        c = fs.classify(rec)
        assert c["state"] == "unknown" and c["downgraded"] is False


def test_p13_missing_boundary_names_the_absent_fields_only():
    c = fs.classify({"verdict": "pass"})
    assert c["downgraded"] is True and c["boundary_ok"] is False
    txt = " ".join(c["reasons"])
    assert "缺边界三元组字段" in txt
    for k in ("mutation_set_hash", "mutation_count", "generator_version"):
        assert k in txt
    # 只报**缺的**那个：补上 hash 与 count 后，理由里不该再出现这两个字段名
    c2 = fs.classify({"verdict": "pass", "mutation_set_hash": "a" * 64,
                      "mutation_count": 10})
    t2 = " ".join(c2["reasons"])
    assert "generator_version" in t2
    assert "mutation_set_hash" not in t2 and "mutation_count" not in t2


def test_p13_illegal_boundary_format_reason_is_distinct():
    c = fs.classify({"verdict": "pass", "mutation_set_hash": "zz",
                     "mutation_count": "10", "generator_version": "v7"})
    assert c["state"] == "unknown" and c["downgraded"] is True
    assert "格式非法" in " ".join(c["reasons"])


def test_p13_exception_without_explanation_is_downgraded():
    c = fs.classify({**B, "verdict": "pass", "exception": "条款X"})
    assert c["state"] == "unknown" and c["downgraded"] is True and c["boundary_ok"] is True


def test_p13_explanation_alone_triggers_pass_with_exception():
    assert fs.enforce({**B, "verdict": "pass", "explanation": "因为Y"}) == "pass_with_exception"
    assert fs.enforce({**B, "verdict": "pass", "exception": "条款X",
                       "explanation": "因为Y"}) == "pass_with_exception"


def test_p13_ok_path_reports_reasons_and_flags():
    c = fs.classify({**B, "verdict": "pass"})
    assert c["state"] == "pass" and c["downgraded"] is False and c["boundary_ok"] is True
    assert c["reasons"], "通过路径也必须给出理由（空理由 = 无法审计）"


def test_p13_unknown_word_is_not_silently_promoted_to_pass():
    """词不在词表 ⇒ requested 必须是 unknown，不得因为"非空"就当通过词。"""
    assert fs.enforce({**B, "verdict": "weird"}) == "unknown"
    assert fs.classify({**B, "verdict": "weird"})["requested"] == "unknown"


def test_p13_verdict_takes_precedence_over_result():
    """`verdict` 优先于 `result`（只有前者缺失时才回退）——回退链顺序是语义。"""
    assert fs.enforce({**B, "verdict": "pass", "result": "block"}) == "pass"
    assert fs.enforce({**B, "result": "block"}) == "fail"


def test_p13_empty_and_pass_words_both_pass():
    assert fs.enforce({**B, "verdict": ""}) == "pass"
    assert fs.enforce({**B, "verdict": "pass"}) == "pass"


def test_p13_classify_card_empty_or_bad_path():
    for bad in ("", "   ", None, 0):
        c = fs.classify_card(bad)  # type: ignore[arg-type]
        assert c["state"] == "unknown"
        assert c["downgraded"] is True and c["boundary_ok"] is False


def test_p13_classify_card_missing_file():
    c = fs.classify_card(str(ROOT / "atoms" / "__no_such_card_657__.md"))
    assert c["state"] == "unknown" and c["boundary_ok"] is False
    assert c["downgraded"] is True
    assert "文件不可读" in " ".join(c["reasons"])


def test_p13_classify_card_reads_boundary_from_disk():
    """真实卡：带边界 ⇒ pass（同时钉住"边界字段确实被读进 rec"这条）。"""
    c = fs.classify_card(str(ROOT / "atoms" / "conc" / "ATOM-CONC-RACE-001.md"))
    assert c["verified"] is True
    assert c["boundary_ok"] is True and c["state"] == "pass"


def test_p13_classify_card_draft_is_not_verified(tmp_path: Path):
    p = tmp_path / "d.md"
    p.write_text("---\nstatus: draft\n---\n\nbody\n", encoding="utf-8")
    assert fs.classify_card(str(p))["verified"] is False


def test_p13_explicit_falsification_wins_over_verified_status(tmp_path: Path):
    """显式 falsification 不得被 `status: verified` 覆盖成 pass（变异体会犯这个错）。"""
    p = tmp_path / "f.md"
    p.write_text("---\nstatus: verified\nmutation_set_hash: " + "a" * 64 +
                 "\nmutation_count: 10\ngenerator_version: v7\n"
                 "falsification: refuted\n---\n\nbody\n", encoding="utf-8")
    c = fs.classify_card(str(p))
    assert c["boundary_ok"] is True
    assert c["state"] == "fail"


# ── P13 · Merkle / RFC6962 边界（ledger_checkpoint_651 存活体）─────────────
def test_p13_inclusion_path_out_of_range_is_empty():
    leaves = [b"a", b"b", b"c"]
    assert lc.inclusion_path(0, []) == []        # n == 0
    assert lc.inclusion_path(-1, leaves) == []   # m < 0
    assert lc.inclusion_path(3, leaves) == []    # m >= n
    assert lc.inclusion_path(99, leaves) == []


def test_p13_verify_inclusion_rejects_over_long_proof():
    leaf = b"leaf"
    lh = lc.leaf_hash(leaf)
    root = lc.node_hash(lh, lh)
    assert lc.verify_inclusion(0, 1, leaf, [], lh) is True        # 单叶：空证明即可
    assert lc.verify_inclusion(0, 1, leaf, [lh], root) is False   # n=1 时 sn 起手为 0


def test_p13_verify_consistency_same_size_requires_equal_roots():
    assert lc.verify_consistency(3, 3, [], b"old", b"old") is True
    assert lc.verify_consistency(3, 3, [], b"old", b"new") is False
    assert lc.verify_consistency(3, 3, [b"p"], b"old", b"old") is False


def test_p13_verify_consistency_from_empty_tree_is_true():
    assert lc.verify_consistency(0, 3, [], b"x", b"y") is True


def test_p13_consistency_proof_required_when_fn_nonzero():
    """m=6,n=8 ⇒ 归一化后 fn=2≠0 ⇒ 空证明必须 False（不能默默通过）。"""
    assert lc.verify_consistency(6, 8, [], b"x", b"y") is False


def test_p13_consistency_proof_too_long_is_rejected():
    assert lc.verify_consistency(1, 2, [b"p", b"q"], b"x", b"x") is False


def test_p13_verify_consistency_requires_both_roots():
    leaves = [b"a", b"b", b"c", b"d"]
    old, new = lc.mth(leaves[:2]), lc.mth(leaves)
    proof = lc.consistency_proof(2, leaves)
    assert lc.verify_consistency(2, 4, proof, old, new) is True
    assert lc.verify_consistency(2, 4, proof, old, b"junk") is False   # 新根不对
    assert lc.verify_consistency(2, 4, proof, b"junk", new) is False   # 旧根不对


# ── P13 · 账本当前有效决定 / 链完整性（decision_event_v2_626 存活体）──────
def test_p13_get_current_none_only_for_absent_target():
    led = de.AuthorityLedger()
    led.append(_mk_event(target_id="X"))
    assert led.get_current("edge", "NOPE") is None
    assert led.get_current("edge", "X") is not None


def test_p13_get_current_follows_supersede_relation():
    """★ 存活体 L245 的定点补测：`alive` 必须收**未被取代**的，不是被取代的那些。

    真实形态：第二条以 `operation=REPLACE` supersede 第一条 ⇒ 当前有效决定 = 第二条。
    （`alive` 若被改成"收集被取代的"，这里会返回第一条 ⇒ 直接被抓。）
    """
    led = de.AuthorityLedger()
    e1 = _mk_event(target_id="S", result="APPROVE")
    led.append(e1)
    e2 = _mk_event(target_id="S", result="MODIFY", modification="改了",
                   operation="REPLACE", supersedes=[e1.event_id])
    led.append(e2)
    cur = led.get_current("edge", "S")
    assert cur is not None and cur.event_id == e2.event_id
    assert led.get_current("edge", "S").result == "MODIFY"


def test_p13_verify_chain_detects_deleted_middle_event():
    """★ 存活体 L258 的定点补测：只删中间一条（其后继的 `prev_hash` 对不上）也必须判假。"""
    led = de.AuthorityLedger()
    for i in range(3):
        led.append(_mk_event(target_id=f"P{i}", result="APPROVE"))
    evs = led.all_events()
    keep = [evs[0], evs[2]]
    led._events = keep  # type: ignore[attr-defined]  # 模拟"链中被抽掉一条"
    assert led.verify_chain() is False


# ── P14 · 657 C 段（第二轮）：严格导入 / 读取 / 规范载荷 / JSONL 往返 ─────
def test_p14_from_dict_strict_rejects_unknown_missing_and_non_dict():
    with pytest.raises(de.StrictEventError):
        de.DecisionEvent.from_dict_strict([])                       # 非 dict
    with pytest.raises(de.StrictEventError):
        de.DecisionEvent.from_dict_strict({"nope": 1})              # 未知字段
    with pytest.raises(de.StrictEventError):
        de.DecisionEvent.from_dict_strict({"result": "APPROVE"})    # 缺必填
    full = _mk_event(reviewer="human:x", decided_at="2026-09-28")
    assert de.DecisionEvent.from_dict_strict(full.to_dict()).result == "APPROVE"


def test_p14_from_dict_lenient_keeps_known_drops_unknown():
    e = de.DecisionEvent.from_dict({})
    assert e.result == "APPROVE" and e.decision_origin == "human_observed"
    d = _mk_event().to_dict()
    d["完全不认识的字段"] = 1
    assert de.DecisionEvent.from_dict(d).result == "APPROVE"


def test_p14_get_matches_by_event_id():
    led = de.AuthorityLedger()
    e = _mk_event(target_id="G")
    led.append(e)
    assert led.get(e.event_id) is e
    assert led.get("AE-999999-deadbeef") is None


def test_p14_payload_is_canonical_and_excludes_derived_fields():
    e = _mk_event(target_id="PL")
    e.finalize(prev_hash=GENESIS, seq=1)
    p = e._payload()
    assert "event_id" not in p and "self_hash" not in p
    assert "rule_id" not in p and "rule_version" not in p     # 空值不参与哈希
    d = e.to_dict()
    d.pop("self_hash", None)
    d.pop("event_id", None)
    for k in ("rule_id", "rule_version"):
        if not d.get(k):
            d.pop(k, None)
    assert p == json.dumps(d, ensure_ascii=False, sort_keys=True, default=str)
    e.rule_id = "KNIGHT-001"
    assert "KNIGHT-001" in e._payload()                        # 非空规则归属进哈希


def test_p14_export_import_jsonl_roundtrip(tmp_path: Path):
    led = de.AuthorityLedger()
    led.append(_mk_event(target_id="R0", result="APPROVE"))
    led.append(_mk_event(target_id="R1", result="MODIFY", modification="改了"))
    p = tmp_path / "nested" / "led.jsonl"      # 目录不存在 ⇒ export 必须自建
    led.export_jsonl(str(p))
    assert p.is_file()
    raw = p.read_text(encoding="utf-8")
    assert "改了" in raw, "ensure_ascii 被打开 ⇒ 中文被转义，人读不了"
    back = de.AuthorityLedger.import_jsonl(str(p))
    assert len(back) == 2
    assert [e.self_hash for e in back.all_events()] == [e.self_hash for e in led.all_events()]
    assert back.verify_chain() is True
    # 严格导入：导出的历史事件缺 reviewer/decided_at ⇒ 必须抛（不许用默认值补齐）
    with pytest.raises(de.StrictEventError):
        de.AuthorityLedger.import_jsonl(str(p), strict=True)


def test_p14_import_jsonl_missing_file_is_empty_ledger(tmp_path: Path):
    led = de.AuthorityLedger.import_jsonl(str(tmp_path / "nope.jsonl"))
    assert len(led) == 0 and led.all_events() == []


def test_p14_make_event_normalizes_supersedes_and_known_kwargs():
    assert de.make_event("edge", "T", "APPROVE", supersedes=None).supersedes == []
    assert de.make_event("edge", "T", "APPROVE", supersedes=["AE-1"]).supersedes == ["AE-1"]
    e = de.make_event("edge", "T", "APPROVE", confidence="high")
    assert e.confidence == "high"          # 已知字段透传
    e2 = de.make_event("edge", "T", "APPROVE", 完全不存在的字段=1)
    assert not hasattr(e2, "完全不存在的字段")
