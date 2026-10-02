# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""673p B · 验证资产池（`tools/verifier_pool_673p.py`）契约测试。

覆盖：池完整性（id/成本/能力/适用类型）/ 受控词表 / 实测-声明标记自洽 /
排除测量仪器 / 静态子集 / 与 672g 池的一致性 / CLI 契约。
独立性：不读任何样本明细，只测池定义本身。
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
POOL_TOOL = TOOLS / "verifier_pool_673p.py"
sys.path.insert(0, str(TOOLS))


def _load():
    spec = importlib.util.spec_from_file_location("verifier_pool_673p", str(POOL_TOOL))
    mod = importlib.util.module_from_spec(spec)
    # 必须先注册进 sys.modules：@dataclass 会读 sys.modules[cls.__module__] 解析注解
    sys.modules["verifier_pool_673p"] = mod
    spec.loader.exec_module(mod)
    return mod


VP = _load()

#: 672g 权威池（拆仓验证器 `tools/select_assets_672g.py::ASSET_POOL`）——次序必须一致，
#: 否则 673p 的 random 抽样结果与 672g 不可对照。
POOL_672G = ("asan", "compile-time", "compiler-warn", "cross-compile",
             "linker", "tsan", "ubsan", "wunsequenced")
DECLARED_UNIMPLEMENTED = ("coredump", "gdb", "ptrace", "valgrind")


# ── 池形状 ───────────────────────────────────────────────────────────────────
def test_pool_size_is_12():
    assert len(VP.ASSET_POOL) == 12


def test_pool_is_lexicographically_sorted():
    names = VP.ids()
    assert names == sorted(names), "池次序必须钉死为字典序（random.sample 依赖次序）"


def test_pool_has_no_duplicate_ids():
    assert len(VP.ids()) == len(set(VP.ids()))


def test_implemented_subset_matches_672g_pool():
    # 已实测子集 = 672g 池，且次序一致 ⇒ 两批的选择结果可直接对照
    assert tuple(VP.implemented_ids()) == POOL_672G


def test_declared_unimplemented_are_exactly_the_four():
    assert tuple(VP.ids(i for i in VP.ASSET_POOL if not i.implemented)) == DECLARED_UNIMPLEMENTED


# ── 每个资产的元数据完整性（验收项：id/成本/能力/适用类型）──────────────────────
def test_every_asset_has_required_metadata():
    for a in VP.ASSET_POOL:
        assert a.id, f"{a} 缺 id"
        assert isinstance(a.cost_units, int) and a.cost_units >= 1, f"{a.id} 成本非法"
        assert a.cost_basis, f"{a.id} 缺 cost_basis"
        assert a.capabilities, f"{a.id} 缺 capabilities"
        assert a.defect_types, f"{a.id} 缺 defect_types"
        assert a.kind, f"{a.id} 缺 kind"


def test_capabilities_within_controlled_vocabulary():
    for a in VP.ASSET_POOL:
        assert set(a.capabilities) <= set(VP.CAPABILITIES), a.id


def test_defect_types_within_controlled_vocabulary():
    for a in VP.ASSET_POOL:
        assert set(a.defect_types) <= set(VP.DEFECT_TYPES), a.id


def test_implemented_flag_matches_evidence_source():
    for a in VP.ASSET_POOL:
        if a.implemented:
            assert a.evidence_source != "declared", f"{a.id} 标实测却无来源"
        else:
            assert a.evidence_source == "declared", f"{a.id} 未标实测却有来源"


def test_costs_are_declared_not_measured():
    # 诚实边界：本批没有实测墙钟 ⇒ 每个资产的 cost_basis 必须是 declared_ordinal
    assert {a.cost_basis for a in VP.ASSET_POOL} == {"declared_ordinal"}


# ── 排除项 / 静态子集 ─────────────────────────────────────────────────────────
def test_pool_excludes_measurement_instruments():
    assert "measure" not in VP.ids()
    assert "perf-counter" not in VP.ids()
    assert set(VP.EXCLUDED_MEASUREMENT_INSTRUMENTS) == {"measure", "perf-counter"}


def test_static_assets_are_subset_of_pool():
    assert set(VP.STATIC_ASSETS) <= set(VP.ids())


def test_static_assets_are_all_implemented():
    assert set(VP.STATIC_ASSETS) <= set(VP.implemented_ids())


# ── 查询辅助 ─────────────────────────────────────────────────────────────────
def test_by_id_returns_spec_and_raises_on_unknown():
    assert VP.by_id("asan").kind == "sanitizer"
    try:
        VP.by_id("nope")
    except KeyError:
        pass
    else:
        raise AssertionError("未知 id 必须 KeyError（fail-loud）")


def test_total_cost_sums_ordinal_costs():
    assert VP.total_cost(["asan", "compile-time"]) == 4


def test_selectable_ids_are_implemented_only():
    assert VP.selectable_ids() == VP.implemented_ids()
    assert set(VP.selectable_ids()) == set(POOL_672G)


# ── 自洽性检查 ───────────────────────────────────────────────────────────────
def test_verify_pool_integrity_clean():
    assert VP.verify_pool_integrity() == []


def test_verify_pool_integrity_detects_broken_pool():
    bad = (VP.ASSET_POOL[1], VP.ASSET_POOL[0])          # 次序被打乱
    probs = VP.verify_pool_integrity(bad)
    assert any("字典序" in p for p in probs)


def test_selftest_passes():
    assert VP.selftest() == 0


# ── CLI 契约 ─────────────────────────────────────────────────────────────────
def test_cli_check_passes():
    r = subprocess.run([sys.executable, str(POOL_TOOL), "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 0
    assert "PASS" in r.stdout


def test_cli_list_json_contract():
    r = subprocess.run([sys.executable, str(POOL_TOOL), "--list", "--json"],
                       capture_output=True, text=True, check=True)
    doc = json.loads(r.stdout)                          # stdout 必须是纯 JSON
    assert doc["pool_size"] == 12
    assert doc["implemented"] == list(POOL_672G)
    assert doc["excluded_measurement_instruments"] == ["measure", "perf-counter"]
    assert len(doc["pool"]) == 12
    assert all({"id", "cost_units", "capabilities", "defect_types"} <= set(a) for a in doc["pool"])
