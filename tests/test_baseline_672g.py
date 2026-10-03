# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""672g · W2 真 B3（拆仓 select_assets + 真 B3 三臂 + 数字同步）测试（≥30 条断言）。

覆盖：
* 任务 A：拆仓 `select_assets` 接口可用（subprocess 调用），策略/契约/fail-loud；
* 任务 B：真 B3 三臂结果现算，带 CP95% CI；预算对齐；连跑 2 次哈希一致；
* 任务 E：双路径交叉复现 < 0.1pp；
* 任务 C：论文 Random† → 真 Random；current_numbers / baseline_random 同步。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
SEED = 20260930
QUEYI_VERIFIER = Path(os.environ.get("QUEYI_VERIFIER", r"C:/CodeLearnling/queyi-verifier"))
SELECTOR = QUEYI_VERIFIER / "tools" / "select_assets_672g.py"

# 674d：拆仓 `queyi-verifier`（真资产池选择器）**不在本仓/CI 检出中**（CI 只 checkout 本仓）
# ⇒ 依赖它的 5 个用例显式跳过；兄弟仓可用时（本机双仓布局）行为**完全不变**、仍真跑。
# 不改成"缺选择器也绿"——那会让"拆仓未检出"本身不可见（与 conftest 的 660 B6 口径一致）。
_NEEDS_SPLIT_REPO = pytest.mark.skipif(
    not SELECTOR.is_file(),
    reason=(
        "拆仓 queyi-verifier 未检出 ⇒ 无 select_assets_672g.py，"
        f"跳过接口类用例（路径探测：{SELECTOR}）"
    ),
)


def _json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _selector(*args: str) -> dict:
    proc = subprocess.run([sys.executable, str(SELECTOR), *args, "--json"],
                          capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


def _meas(doc: dict, set_: str) -> dict:
    return doc[set_]["measurable"]


# ── 任务 A：拆仓接口（均需兄弟仓，未检出时 skip）───────────────────────────────
@_NEEDS_SPLIT_REPO
def test_selector_exists_and_runs():
    assert SELECTOR.is_file(), f"拆仓选择器不存在：{SELECTOR}"
    doc = _selector("--print-pool")
    assert doc["pool_size"] == 8
    assert set(doc["pool"]) == {
        "asan", "compile-time", "compiler-warn", "cross-compile",
        "linker", "tsan", "ubsan", "wunsequenced"}


@_NEEDS_SPLIT_REPO
def test_selector_pool_excludes_measurement_instruments():
    pool = set(_selector("--print-pool")["pool"])
    assert "measure" not in pool
    assert "perf-counter" not in pool


@_NEEDS_SPLIT_REPO
def test_selector_random_reproducible():
    a = _selector("--n", "4", "--strategy", "random", "--seed", str(SEED))
    b = _selector("--n", "4", "--strategy", "random", "--seed", str(SEED))
    assert a["picked"] == b["picked"]
    assert len(a["picked"]) == 4
    assert set(a["picked"]) <= set(a["pool"])


@_NEEDS_SPLIT_REPO
def test_selector_failure_driven_and_static_strategies():
    fd = _selector("--pool-json", '[{"id":"a","fail_hits":1},{"id":"b","fail_hits":9}]',
                   "--n", "1", "--strategy", "failure_driven")
    assert fd["picked"] == ["b"]
    st = _selector("--n", "2", "--strategy", "static")
    assert set(st["picked"]) <= {"compiler-warn", "wunsequenced", "cross-compile", "linker"}


@_NEEDS_SPLIT_REPO
def test_selector_fail_loud_on_overflow():
    proc = subprocess.run([sys.executable, str(SELECTOR), "--n", "99", "--strategy", "random",
                           "--seed", str(SEED), "--json"], capture_output=True, text=True)
    assert proc.returncode != 0


# ── 任务 B：真 B3 三臂 ────────────────────────────────────────────────────────
def test_prereg_672g_locked():
    p = _json("data/experiments/prereg_672g.json")
    for key in ("research_question", "hypotheses", "methods", "decision_thresholds",
                "exclusion_criteria", "registered_at", "registrant"):
        assert key in p, f"预注册缺字段 {key}"
    assert p["status"] == "locked_before_experiment"
    assert p["methods"]["seed"] == SEED
    assert p["methods"]["asset_pool"]["size"] == 8
    assert "measure" in p["methods"]["asset_pool"]["rationale"]
    assert {"H1", "H2", "H3", "H0"} <= set(p["hypotheses"])


def test_b3_real_artifact_shape():
    r = _json("data/experiments/b3_real_672g.json")
    assert r["schema"] == "queyi-baseline-experiment/672g"
    assert r["seed"] == SEED
    assert len(r["asset_pool"]) == 8
    assert "queyi-verifier" in r["pool_owner"]
    for set_ in ("holdout", "corpus"):
        blk = r[set_]
        for arm in ("fd", "static", "random"):
            c = blk[arm]
            assert c["catch"] + c["miss"] + c["unknown"] + c["not_error"] == c["total"]
            assert c["measurable"]["n"] == c["catch"] + c["miss"]


def test_b3_real_denominators_and_rates():
    r = _json("data/experiments/b3_real_672g.json")
    fd_h = r["holdout"]["fd"]["measurable"]
    fd_c = r["corpus"]["fd"]["measurable"]
    assert (fd_h["k"], fd_h["n"]) == (17, 21)
    assert (fd_c["k"], fd_c["n"]) == (26, 48)
    assert r["holdout"]["random"]["measurable"]["k"] == 2
    assert r["corpus"]["random"]["measurable"]["k"] == 8
    assert r["holdout"]["random"]["measurable"]["n"] == 21
    assert r["corpus"]["random"]["measurable"]["n"] == 48


def test_b3_random_budget_aligned_and_pooled():
    r = _json("data/experiments/b3_real_672g.json")
    for set_ in ("holdout", "corpus"):
        sel = r[set_]["random_selection"]
        assert len(sel["picked"]) == len(sel["fd_used"]) > 0
        assert sel["seed"] == SEED
        assert set(sel["picked"]) <= set(sel["pool"])
        assert sel["pool"] == r["asset_pool"]
        assert len(sel["allocation_table"]) == len(sel["picked"])


def test_b3_random_is_subset_of_fd():
    r = _json("data/experiments/b3_real_672g.json")
    for set_ in ("holdout", "corpus"):
        assert r[set_]["random"]["catch"] <= r[set_]["fd"]["catch"]


def test_b3_carries_cp_intervals_and_stats():
    r = _json("data/experiments/b3_real_672g.json")
    for set_ in ("holdout", "corpus"):
        for arm in ("fd", "static", "random"):
            mm = r[set_][arm]["measurable"]
            assert mm["cp_low"] <= mm["point"] <= mm["cp_high"]
            assert mm["conf"] == 0.95
        for cmp_ in ("fd_vs_static", "fd_vs_random"):
            c = r[set_][cmp_]
            assert c["mcnemar_p"] is not None and c["cohens_h"] is not None
            assert c["discordant_other_catch"] == 0        # random ⊆ fd


def test_b3_reproducible_two_runs():
    r = _json("data/experiments/b3_real_672g.json")
    rep = r["reproducibility"]
    assert rep["identical"] is True
    assert rep["run1_sha256"] == rep["run2_sha256"]
    assert rep["picks_identical"] is True


# ── 任务 E：双路径 ────────────────────────────────────────────────────────────
def test_dual_path_pass():
    v = _json("data/experiments/baseline_verify_672g.json")
    assert v["verdict"] == "PASS"
    assert v["path_a_vs_b"]["ok"] is True
    assert v["path_a_vs_b"]["problems"] == []
    assert v["path_a_vs_b"]["tolerance_pp"] <= 0.1


def test_dual_path_reproduces_rates_and_picks():
    v = _json("data/experiments/baseline_verify_672g.json")
    assert (v["holdout"]["fd"]["k"], v["holdout"]["fd"]["n"]) == (17, 21)
    assert (v["corpus"]["fd"]["k"], v["corpus"]["fd"]["n"]) == (26, 48)
    assert (v["corpus"]["random"]["k"], v["corpus"]["random"]["n"]) == (8, 48)
    r = _json("data/experiments/b3_real_672g.json")
    for set_ in ("holdout", "corpus"):
        assert set(v[set_]["random_picked"]) == set(r[set_]["random_selection"]["picked"])


# ── 任务 C：数字同步 ──────────────────────────────────────────────────────────
def test_baseline_random_upgraded_to_real_b3():
    # 672h 重分类：random_proxy 为「仪器级预算对齐代理，**非论文 B3**」，不再是 672g 原义的「真 B3」。
    # 此处同步到 672h 现行权威口径（current_numbers caveat），不再断言「真 B3」。
    rn = _json("data/experiments/baseline_random.json")
    assert "非论文 B3" in rn["arm"]
    assert "仪器级" in rn["arm"]                         # 明示为仪器级预算对齐代理
    assert rn["seed"] == SEED
    for set_ in ("holdout", "corpus"):
        sel = rn["selection"][set_]
        assert len(sel["picked"]) == len(sel["fd_used"]) > 0
        assert sel["seed"] == SEED
        assert set(sel["picked"]) <= set(sel["pool"])
    assert (rn["holdout"]["measurable"]["k"], rn["holdout"]["measurable"]["n"]) == (4, 41)
    assert (rn["corpus"]["measurable"]["k"], rn["corpus"]["measurable"]["n"]) == (14, 64)


def test_current_numbers_has_real_b3_provenance():
    # 672h 已移除顶层 b3_random_672g 键，并将 random 重分类为「非真 B3 / 仪器级代理」，
    # 基线臂键名由 random 改为 random_proxy。此处只校验仍成立的口径与 caveat 表述。
    cn = _json("data/current_numbers.json")
    assert cn["baseline_arms"]["holdout"]["random_proxy"]["k"] == 4
    assert cn["baseline_arms"]["corpus"]["random_proxy"]["k"] == 14
    cap = cn["baseline_arms"]["caveat"]
    assert "非真 B3" in cap or "仪器级代理" in cap


def test_paper_random_dagger_replaced():
    paper = (ROOT / "research" / "paper_v0.9.md").read_text(encoding="utf-8")
    assert "Random†" not in paper, "论文仍残留 Random†"
    assert "†" not in paper, "论文仍残留 † 符号"
    assert "真 B3" in paper
    assert "queyi-verifier" in paper
    # 数字保持（真 B3 与代理一致）
    assert "16.7% (8/48)" in paper and "+37.5pp" in paper


def test_paper_stale_corpus_row_fixed():
    # 672f 遗漏的 §6.5 FD vs Random corpus 行（旧值 24/1.24）已修正为 18/0.81
    paper = (ROOT / "research" / "paper_v0.9.md").read_text(encoding="utf-8")
    assert "1.24" not in paper, "论文 §6.5 仍残留旧 Cohen's h=1.24"
    assert "(18, 0)" in paper and "0.81" in paper
