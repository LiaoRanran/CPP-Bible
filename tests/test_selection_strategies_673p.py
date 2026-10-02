# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""673p B · 资产选择策略（`tools/selection_strategies_673p.py`）契约测试。

覆盖：三策略语义（FD 降序确定性 / random 可复现 / static 只用静态资产）/
预算约束生效（资产数 + 序数成本）/ fail-loud 边界 / 分配表形状 /
与 672g 抽样结果的一致性回归 / CLI 契约。
独立性：不读样本明细、不依赖 A5 运行器。
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
SEL_TOOL = TOOLS / "selection_strategies_673p.py"
sys.path.insert(0, str(TOOLS))


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    # 先注册进 sys.modules：① @dataclass 解析注解要用；② 让本模块内的
    # `import verifier_pool_673p` 命中同一实例（而非再加载一份）
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


VP = _load("verifier_pool_673p", "tools/verifier_pool_673p.py")
SS = _load("selection_strategies_673p", "tools/selection_strategies_673p.py")

SEED = 20260930
POOL = VP.ASSET_POOL
FH = {i: 0 for i in VP.selectable_ids(POOL)}
FH["asan"] = 25
FH["ubsan"] = 9
FH["tsan"] = 6


def _raises(fn) -> bool:
    try:
        fn()
    except (ValueError, TypeError, KeyError):
        return True
    return False


# ── 策略声明 ─────────────────────────────────────────────────────────────────
def test_strategies_declared():
    assert set(SS.STRATEGIES) == {"failure_driven", "random", "static"}


# ── failure_driven ───────────────────────────────────────────────────────────
def test_fd_descending_by_fail_hits():
    sel = SS.select("failure_driven", POOL, max_assets=3, fail_hits=FH)
    assert list(sel.assets) == ["asan", "ubsan", "tsan"]


def test_fd_tie_break_is_id_ascending():
    fh = {i: 0 for i in VP.selectable_ids(POOL)}
    sel = SS.select("failure_driven", POOL, max_assets=8, fail_hits=fh)
    assert list(sel.assets) == sorted(VP.selectable_ids(POOL))


def test_fd_is_deterministic():
    a = SS.select("failure_driven", POOL, max_assets=4, fail_hits=FH)
    b = SS.select("failure_driven", POOL, max_assets=4, fail_hits=FH)
    assert a == b


def test_fd_requires_fail_hits():
    assert _raises(lambda: SS.select("failure_driven", POOL, max_assets=2))


def test_fd_requires_complete_fail_hits():
    assert _raises(lambda: SS.select("failure_driven", POOL, max_assets=2, fail_hits={"asan": 1}))


# ── random ───────────────────────────────────────────────────────────────────
def test_random_reproducible_same_seed():
    a = SS.select("random", POOL, max_assets=4, seed=SEED)
    b = SS.select("random", POOL, max_assets=4, seed=SEED)
    assert a.assets == b.assets


def test_random_differs_across_seeds():
    a = SS.select("random", POOL, max_assets=4, seed=SEED)
    c = SS.select("random", POOL, max_assets=4, seed=99999)
    assert a.assets != c.assets


def test_random_length_unique_and_in_pool():
    a = SS.select("random", POOL, max_assets=5, seed=SEED)
    assert len(a.assets) == 5
    assert len(set(a.assets)) == 5
    assert set(a.assets) <= set(VP.selectable_ids(POOL))


def test_random_requires_seed():
    assert _raises(lambda: SS.select("random", POOL, max_assets=2))


def test_random_matches_672g_pick_regression():
    """回归钉：seed=20260930 / n=4 的抽样必须与 672g 权威实现逐位一致。

    672g `data/experiments/b3_real_672g.json::random_selection.picked`
      = ["wunsequenced", "cross-compile", "tsan", "compile-time"]
    """
    sel = SS.select("random", POOL, max_assets=4, seed=SEED)
    assert list(sel.assets) == ["wunsequenced", "cross-compile", "tsan", "compile-time"]


def test_random_matches_672g_pick_regression_n5():
    """672g corpus 臂：n=5 → ["wunsequenced","cross-compile","tsan","compile-time","compiler-warn"]。"""
    sel = SS.select("random", POOL, max_assets=5, seed=SEED)
    assert list(sel.assets) == ["wunsequenced", "cross-compile", "tsan", "compile-time", "compiler-warn"]


# ── static ───────────────────────────────────────────────────────────────────
def test_static_only_returns_static_assets():
    sel = SS.select("static", POOL, max_assets=4)
    assert set(sel.assets) <= set(VP.STATIC_ASSETS)
    assert list(sel.assets) == sorted(sel.assets)


def test_static_is_deterministic():
    assert SS.select("static", POOL, max_assets=3) == SS.select("static", POOL, max_assets=3)


def test_static_never_falls_back_to_runtime_assets():
    # static 预算给满 4 也只能是 4 个静态资产，不得用运行时资产补齐
    sel = SS.select("static", POOL, max_assets=4)
    assert set(sel.assets) == set(VP.STATIC_ASSETS)


def test_static_budget_overflow_fails_loud():
    assert _raises(lambda: SS.select("static", POOL, max_assets=5))


# ── 预算约束生效 ─────────────────────────────────────────────────────────────
def test_max_assets_enforced():
    for n in (0, 1, 4, 8):
        assert len(SS.select("random", POOL, max_assets=n, seed=SEED).assets) == n


def test_max_cost_enforced():
    sel = SS.select("failure_driven", POOL, max_cost=6, fail_hits=FH)
    assert sel.cost_units <= 6
    assert VP.total_cost(sel.assets) == sel.cost_units


def test_both_budget_dimensions_enforced():
    sel = SS.select("failure_driven", POOL, max_assets=8, max_cost=5, fail_hits=FH)
    assert len(sel.assets) <= 8
    assert sel.cost_units <= 5


def test_max_cost_truncation_is_reported_not_silent():
    sel = SS.select("failure_driven", POOL, max_assets=8, max_cost=5, fail_hits=FH)
    assert len(sel.assets) < 8
    assert "max_cost" in sel.notes


def test_zero_budget_returns_empty():
    assert SS.select("random", POOL, max_assets=0, seed=SEED).assets == ()


# ── fail-loud 边界 ───────────────────────────────────────────────────────────
def test_no_budget_dimension_fails_loud():
    assert _raises(lambda: SS.select("random", POOL, seed=SEED))


def test_max_assets_exceeds_candidates_fails_loud():
    assert _raises(lambda: SS.select("random", POOL, max_assets=9, seed=SEED))


def test_negative_max_assets_fails_loud():
    assert _raises(lambda: SS.select("random", POOL, max_assets=-1, seed=SEED))


def test_unknown_strategy_fails_loud():
    assert _raises(lambda: SS.select("greedy", POOL, max_assets=2))


def test_infeasible_max_cost_fails_loud():
    assert _raises(lambda: SS.select("static", POOL, max_cost=0))


def test_candidate_not_in_pool_fails_loud():
    assert _raises(lambda: SS.select("random", POOL, max_assets=1, seed=1, candidates=["nope"]))


def test_unimplemented_candidate_fails_loud():
    # 声明未接线资产无实测判决 ⇒ 不可作为候选（fail-loud，不静默跳过）
    assert _raises(lambda: SS.select("random", POOL, max_assets=1, seed=1, candidates=["valgrind"]))


# ── 分配表 / 输出格式 ────────────────────────────────────────────────────────
def test_allocation_table_shape():
    sel = SS.select("random", POOL, max_assets=4, seed=SEED)
    assert len(sel.allocation_table) == 4
    assert [r["rank"] for r in sel.allocation_table] == [1, 2, 3, 4]
    assert all({"asset", "rank", "cost_units"} <= set(r) for r in sel.allocation_table)
    assert [r["asset"] for r in sel.allocation_table] == list(sel.assets)


def test_seed_recorded_only_for_random():
    assert SS.select("random", POOL, max_assets=2, seed=SEED).seed == SEED
    assert SS.select("static", POOL, max_assets=2).seed is None
    assert SS.select("failure_driven", POOL, max_assets=2, fail_hits=FH).seed is None


def test_as_dict_is_json_serializable():
    doc = SS.select("random", POOL, max_assets=3, seed=SEED).as_dict()
    json.dumps(doc, ensure_ascii=False)                 # 不抛即通过
    assert doc["strategy"] == "random"
    assert len(doc["assets"]) == 3


# ── FD 预算锚（事后记账语义）──────────────────────────────────────────────────
def test_fd_budget_anchor_filters_pool_and_dedups():
    assert SS.fd_budget_anchor(["asan", "asan", "linker", "measure", "unknown"]) == ["asan", "linker"]


def test_fd_budget_anchor_ignores_unimplemented():
    assert SS.fd_budget_anchor(["asan", "valgrind", "gdb"]) == ["asan"]


# ── 自检 + CLI 契约 ──────────────────────────────────────────────────────────
def test_selftest_passes():
    assert SS.selftest() == 0


def test_cli_json_contract():
    r = subprocess.run([sys.executable, str(SEL_TOOL), "--strategy", "random",
                        "--max-assets", "4", "--seed", str(SEED), "--json"],
                       capture_output=True, text=True, check=True)
    doc = json.loads(r.stdout)
    assert doc["strategy"] == "random"
    assert doc["max_assets"] == 4
    assert doc["n_candidates"] == 8
    assert len(doc["assets"]) == 4


def test_cli_check_passes():
    r = subprocess.run([sys.executable, str(SEL_TOOL), "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 0
    assert "PASS" in r.stdout
