"""580 任务 2/3 回归锁：卡间进程并行（`--jobs`）不得改判决、不得丢计数、不得静默丢卡。

纪律：`--jobs 1` 是今天的串行路径（默认 OFF）；`--jobs N` 走进程池（每 worker 一个 sandbox 根 +
各自 batch_root + 各自 baseline）。本文件锁：
(a) jobs1 / jobs2 / jobs4 的 `_variant_index()` **完全相等**（空 diff）；
(b) worker 的根与锁路径确实与本进程不同（异根⇒异锁，这是并行能成立的前提）；
(c) `results` **顺序**与串行一致（不只比计数）；
(d) 三个 STATS 计数 jobs1 == jobsN；
(e) worker 内异常 ⇒ 整批 fail-loud（含卡名），不静默丢卡（丢卡会改分母）；
(f) 真实根指纹在跑批前后一致，真实 `build/.replay_lock` 不被触碰。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import atom_evidence_replay as replay  # noqa: E402
import mutation_fuzz as mf  # noqa: E402


def _tiny_cards(n: int = 2) -> list[Path]:
    cards = sorted((ROOT / "evidence/mem").glob("EV-MEM-03*.md"))[:n]
    assert len(cards) == n, "夹具不足：需要 evidence/mem/EV-MEM-03*.md"
    return cards


def _order(rep: dict) -> list[tuple[str, str, str]]:
    return [(r["card"], r["op"], r["point"]) for r in rep["results"]]


def test_580_jobs_value_parsing():
    """`--jobs` 解析：默认 1；`auto` = min(4, cpu-1, 卡数)；非法值回落 1（绝不静默变成并行）。"""
    assert mf._jobs_value("1", 83) == 1
    assert mf._jobs_value("4", 83) == 4
    assert mf._jobs_value("xx", 83) == 1
    assert mf._jobs_value(0, 83) == 1
    auto = mf._jobs_value("auto", 83)
    assert 1 <= auto <= 4
    assert mf._jobs_value("auto", 1) == 1, "卡数不足时不许起多余 worker"


def test_580_jobs1_equals_jobsN_everywhere():
    """(a)(c)(d)(f) 主验收：jobs=1/2/4 的逐变体索引、结果顺序、三计数、真实根指纹全一致。"""
    cards = _tiny_cards(2)
    base = mf._run_jobs(cards, ["M6"], len(cards), jobs=1)
    idx1, order1 = mf._variant_index(base), _order(base)
    for jobsn in (2, 4):
        rep = mf._run_jobs(cards, ["M6"], len(cards), jobs=jobsn)
        assert rep["variants"] == base["variants"]
        assert mf._variant_index(rep) == idx1, f"jobs={jobsn} 判决与串行不一致"
        assert _order(rep) == order1, f"jobs={jobsn} 结果顺序与串行不一致"
        assert rep["by_operator"] == base["by_operator"]
        assert (rep["blocked"], rep["escaped"], rep["n_a"]) == \
               (base["blocked"], base["escaped"], base["n_a"])
        assert rep["ge_runs"] == base["ge_runs"], "ge_runs 必须同口径（逻辑扫描数）"
        assert rep["replay_runs"] == base["replay_runs"]
        assert rep["replay_skipped"] == base["replay_skipped"]
        assert rep["jobs"] == jobsn and rep["parallel"] is True
        assert rep["root_fingerprint_ok"] is True
        assert base["jobs"] == 1 and base["parallel"] is False


def test_580_worker_gets_own_root_and_lock():
    """(b) worker 内跑批根 = 自己的 `mutworker_*` tmp ⇒ 锁路径也随之分片（异根⇒异锁）。"""
    lock_before = replay._replay_lock_path()
    assert lock_before == replay.ROOT / "build" / ".replay_lock"
    mf._worker_init(["M6"])
    try:
        tmp = mf._MUT_WORKER["tmp"]
        assert tmp.name.startswith("mutworker_"), tmp
        assert replay.run_root() == tmp, "worker 内跑批根必须指向自己的 tmp"
        assert replay._replay_lock_path() == tmp / "build" / ".replay_lock", "锁必须分片到 worker 根"
        assert replay._replay_lock_path() != lock_before
        assert (tmp / "Examples").is_dir(), "工件树必须进 worker 根"
        assert mf._MUT_WORKER["baseline"], "worker 必须自带全库 baseline"
    finally:
        mf._worker_cleanup()
    assert replay.run_root() == replay.ROOT, "清理后必须还原"
    assert replay._replay_lock_path() == lock_before


def test_580_worker_failure_is_fail_loud():
    """(e) 卡不存在 ⇒ worker 内抛错 ⇒ 整批 `SystemExit` 且报出是哪张卡（不静默丢卡）。"""
    ghost = ROOT / "evidence" / "nope" / "EV-NOPE-999.md"
    with pytest.raises(SystemExit) as ei:
        mf.run_fuzz_parallel([ghost], ["M6"], 1, 2)
    msg = str(ei.value)
    assert "worker 失败" in msg and "EV-NOPE-999.md" in msg, msg


def test_580_parallel_leaves_real_root_and_lock_untouched(replay_serial):
    """(f) 跑完并行后：真实 `build/.replay_lock` 不存在；真实根指纹与跑前相同。

    本用例比对**真实根全树指纹** ⇒ 与 replay 共用同一把锁串行（`-n auto` 下防假红）。
    """
    cards = _tiny_cards(1)
    fp0 = mf._real_root_fingerprint()
    rep = mf._run_jobs(cards, ["M6"], 1, jobs=2)
    assert rep["root_fingerprint_ok"] is True
    assert mf._real_root_fingerprint() == fp0
    assert not (ROOT / "build" / ".replay_lock").exists(), \
        "并行期锁必须落在 worker tmp，不许碰真实 build/"
