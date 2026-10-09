# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""712 批测试：数字审计器依赖就绪聚合的反例测试（元验证）。

背景（评审阻塞项 1）：`tools/verify_paper_numbers.py::check_dependencies` 原先用

    ready = ready or ok

聚合依赖组状态。这意味着只要组内**任意一个**文件满足条件，整组就被标记为
ready，即使其余必需文件缺失或数量不足——676f 组矩阵文件只有 673/1147 与
1054/1147、676g 组检查点矩阵完全缺失，却都显示 ready。

修复：改为严格合取（all），并用 `state ∈ {ready, partial, not_ready}` 把
「部分就绪」与「完全就绪」分开表示。

本文件的断言全部是**反例**：构造缺失/不足的依赖组，断言聚合结果必须为 False。
这些用例在修复前的 `or` 逻辑下会失败（即修复前会通过、修复后失败的语义被反转）。

跑法：python -m pytest tests/test_712.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import verify_paper_numbers as vpn  # noqa: E402

# --------------------------------------------------------------------------
# 一、反例：单个必需文件不满足 ⇒ 整组不得为 ready
# --------------------------------------------------------------------------


def test_single_missing_file_fails_group():
    """反例 A：组内 2 个文件满足、1 个文件缺失 ⇒ ready 必须为 False。

    修复前（or 逻辑）此用例会得到 ready=True（缺陷）；修复后为 False。
    """
    entry = {
        "a/stats.json": {"n": 1, "need": 1},
        "b/matrix.jsonl": {"n": 1147, "need": 1147},
        "c/ckpt.jsonl": {"n": None, "need": 3126},  # 缺失
    }
    agg = vpn.aggregate_dep_state(entry)
    assert agg["ready"] is False
    assert agg["state"] == "partial"
    assert agg["n_ready"] == 2
    assert agg["n_total"] == 3
    assert agg["missing"] == ["c/ckpt.jsonl"]
    assert agg["short"] == []


def test_insufficient_line_count_fails_group():
    """反例 B：文件存在但行数不足 ⇒ ready 必须为 False。

    对应 676f 真实情形：local=673/1147、san=1054/1147，任一不足即整组不就绪。
    """
    entry = {
        "data/a5_676f_results.json": {"n": 1, "need": 1},
        "data/a5_676f_matrix_local.jsonl": {"n": 673, "need": 1147},
        "data/a5_676f_matrix_san.jsonl": {"n": 1054, "need": 1147},
    }
    agg = vpn.aggregate_dep_state(entry)
    assert agg["ready"] is False
    assert agg["state"] == "partial"
    assert agg["n_ready"] == 1
    assert [s[0] for s in agg["short"]] == [
        "data/a5_676f_matrix_local.jsonl",
        "data/a5_676f_matrix_san.jsonl",
    ]


def test_all_files_missing_is_not_ready():
    """反例 C：全部文件缺失 ⇒ ready=False 且 state='not_ready'（不是 partial）。"""
    entry = {
        "x.jsonl": {"n": None, "need": 10},
        "y.jsonl": {"n": None, "need": 20},
    }
    agg = vpn.aggregate_dep_state(entry)
    assert agg["ready"] is False
    assert agg["state"] == "not_ready"
    assert agg["n_ready"] == 0
    assert len(agg["missing"]) == 2


def test_boundary_exactly_at_threshold_is_ready():
    """边界：n == need 恰好达标 ⇒ 视为满足（>= 语义，与修复前一致）。"""
    entry = {"m.jsonl": {"n": 1147, "need": 1147}}
    agg = vpn.aggregate_dep_state(entry)
    assert agg["ready"] is True
    assert agg["state"] == "ready"
    assert agg["n_ready"] == agg["n_total"] == 1


def test_one_below_threshold_is_not_ready():
    """边界：n = need - 1 ⇒ 不就绪（不能因为'差不多'而通过）。"""
    entry = {"m.jsonl": {"n": 1146, "need": 1147}}
    assert vpn.aggregate_dep_state(entry)["ready"] is False


def test_empty_group_is_not_ready():
    """空依赖组不得被判定为 ready（避免 0 个文件'全部满足'的伪真）。"""
    assert vpn.aggregate_dep_state({})["ready"] is False
    assert vpn.aggregate_dep_state({})["n_total"] == 0


# --------------------------------------------------------------------------
# 二、元验证：证明修复前的 `or` 语义确实会让反例通过（回归锁）
# --------------------------------------------------------------------------


def _legacy_or_aggregate(entry: dict) -> bool:
    """复刻修复前的聚合语义，用于证明本批发现的是真缺陷而非误报。"""
    ready = False
    for info in entry.values():
        n = info.get("n")
        need = info.get("need")
        ok = n is not None and need is not None and n >= need
        ready = ready or ok
    return ready


def test_legacy_or_logic_would_pass_the_counterexample():
    """元验证：同一反例在旧 `or` 逻辑下为 True（通过），在新逻辑下为 False（失败）。

    这条断言把「反例确实是反例」钉死：如果哪天有人把聚合改回 or，本测试先失败。
    """
    entry = {
        "a/stats.json": {"n": 1, "need": 1},
        "c/ckpt.jsonl": {"n": None, "need": 3126},
    }
    assert _legacy_or_aggregate(entry) is True  # 旧逻辑：漏过
    assert vpn.aggregate_dep_state(entry)["ready"] is False  # 新逻辑：拦住


# --------------------------------------------------------------------------
# 三、与真实仓库状态对齐（只读，不跑 detect）
# --------------------------------------------------------------------------


def test_real_repo_676f_and_676g_are_not_ready():
    """对当前工作树真实状态断言：676f / 676g 两组都不是 ready。

    依据 2026-10-10 实测：
      676f: results.json=1/1 OK；local=673/1147 不足；san=1054/1147 不足
      676g: stats.json=1/1 OK；ckpt_san.jsonl 缺失
    """
    deps = vpn.check_dependencies()
    assert set(deps) == {"676f", "676g"}
    for name in ("676f", "676g"):
        d = deps[name]
        assert d["ready"] is False, f"{name} 不应被判定为 ready"
        assert d["state"] == "partial"
        assert d["n_ready"] < d["n_total"]
        # 组级 ready 必须等于「全部文件 ready 的合取」
        assert d["ready"] == all(f["ready"] for f in d["files"].values())


def test_dependency_declaration_is_nonempty():
    """依赖声明本身不得为空（空声明会让合取恒真，是另一种静默通过）。"""
    for name, files in vpn.DEPENDENCY_FILES.items():
        assert len(files) >= 1, f"{name} 依赖声明为空"
        for rel, need in files:
            assert need >= 1, f"{name}/{rel} 的 need 必须为正"


# --------------------------------------------------------------------------
# 四、权威重算源（712 新增）
# --------------------------------------------------------------------------


def test_recompute_sources_are_available_and_sized():
    """陌生研究者重算关键数字所需的完整检测矩阵必须可加载、且样本数达标。

    676f：n_samples=1137（论文里 1137/1147 脚注的来处）
    676g：n_samples=1147
    """
    rs = vpn.check_recompute_sources()
    assert set(rs) == {"676f", "676g"}
    for name, rec in rs.items():
        assert rec["error"] is None, f"{name} 重算源加载异常：{rec['error']}"
        assert rec["ok"] is True, f"{name} 重算源样本数不足：{rec['n']} < {rec['need']}"
    assert rs["676f"]["n"] == 1137
    assert rs["676g"]["n"] == 1147


def test_recompute_sources_are_separate_from_declared_dependencies():
    """重算源不得被塞进 DEPENDENCY_FILES 用来'顶绿'声明依赖。

    防的是最容易被做的手脚：把缺失的 .jsonl 换成完整的 .json，让 partial 变 ready。
    """
    declared_paths = {rel for files in vpn.DEPENDENCY_FILES.values() for rel, _ in files}
    for _name, (rel, _need) in vpn.RECOMPUTE_SOURCES.items():
        assert rel not in declared_paths, f"{rel} 不应同时作为声明依赖项出现"
