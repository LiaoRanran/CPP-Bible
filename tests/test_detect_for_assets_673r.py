# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""673r · `tools/detect_for_assets.py` 契约测试。

覆盖：
* **红线守卫**：661 的 `detect` / `main` 一行未改（签名、双档 OPT_LEVELS、SAN 映射）；
* **聚合口径**：OR 语义 + unknown 绝不当 miss（666 的假 miss 教训）；
* **样本规格**：holdout 磁盘夹具 41 / corpus 内联 code 64；
* **fail-loud**：选中池外资产 ⇒ ValueError，绝不静默跳过；
* **解码兜底适配层**：装/卸必须完全还原（`subprocess.run` 与 `os.environ`）；
* **横幅剥离**：NUL 行与 `wsl:` 行去掉、正常编译输出保留；
* **保真**（慢档，真调编译器）：h41 × asan = catch（672h 冻结记录）。

独立性：不读 `data/experiments/asset_attribution_673r.json`，不依赖 A5 运行器。
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    if spec is None or spec.loader is None:
        raise ImportError(rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


VP = _load("verifier_pool_673p", "tools/verifier_pool_673p.py")
DFA = _load("detect_for_assets", "tools/detect_for_assets.py")
RV = _load("rv661", "tools/holdout_reveal_661.py")

POOL_IDS = VP.selectable_ids(VP.ASSET_POOL)


# ── 红线守卫：661 一行都不能改 ────────────────────────────────────────────────
def test_661_detect_signature_unchanged():
    assert RV.detect.__code__.co_argcount == 2
    assert RV.detect.__code__.co_varnames[:2] == ("kind", "files")


def test_661_opt_levels_still_two_tiers():
    assert tuple(RV.OPT_LEVELS) == ("-O0", "-O2")


def test_661_san_mapping_unchanged():
    assert RV.SAN == {"tsan": "thread", "asan": "address", "ubsan": "undefined"}


def test_661_main_still_has_refused_guard():
    src = (TOOLS / "holdout_reveal_661.py").read_text(encoding="utf-8")
    assert "[REFUSED]" in src and "correct_harness" in src


# ── 聚合口径 ────────────────────────────────────────────────────────────────
def test_or_any_catch_is_catch():
    assert DFA.aggregate({"asan": {"verdict": "miss"},
                          "ubsan": {"verdict": "catch"}})["verdict"] == "catch"


def test_or_all_miss_is_miss():
    assert DFA.aggregate({"asan": {"verdict": "miss"},
                          "ubsan": {"verdict": "miss"}})["verdict"] == "miss"


def test_or_all_unknown_is_unknown_not_miss():
    """666 的教训：unknown 绝不当 miss。"""
    out = DFA.aggregate({"asan": {"verdict": "unknown"}, "ubsan": {"verdict": "unknown"}})
    assert out["verdict"] == "unknown"


def test_or_unknown_plus_miss_is_miss():
    assert DFA.aggregate({"asan": {"verdict": "unknown"},
                          "ubsan": {"verdict": "miss"}})["verdict"] == "miss"


def test_or_empty_selection_is_miss_with_no_caught_by():
    out = DFA.aggregate({})
    assert out["verdict"] == "miss" and out["caught_by"] is None


def test_caught_by_all_lists_every_hitting_asset():
    out = DFA.aggregate({"asan": {"verdict": "catch"}, "tsan": {"verdict": "catch"},
                         "ubsan": {"verdict": "miss"}})
    assert out["caught_by_all"] == ["asan", "tsan"]


# ── 样本规格 ────────────────────────────────────────────────────────────────
def test_holdout_measurable_is_41():
    assert len(DFA.measurable_specs("holdout")) == 41


def test_corpus_measurable_is_64():
    assert len(DFA.measurable_specs("corpus")) == 64


def test_unknown_dataset_raises():
    with pytest.raises(ValueError):
        DFA.measurable_specs("nope")


def test_holdout_specs_carry_disk_fixtures():
    specs = DFA.measurable_specs("holdout")
    assert all(s.input_mode == "disk_fixtures" for s in specs)
    assert all(s.files for s in specs)


def test_corpus_specs_carry_inline_code():
    assert all(s.input_mode == "code_materialized" for s in DFA.measurable_specs("corpus"))


def test_specs_keep_frozen_detector_and_verdict():
    for s in DFA.measurable_specs("holdout") + DFA.measurable_specs("corpus"):
        assert s.recorded_detector and s.recorded_verdict in ("catch", "miss")


def test_corpus_code_map_covers_all_ids():
    cmap = DFA.corpus_code_map()
    ids = {s.id for s in DFA.measurable_specs("corpus")}
    assert ids <= set(cmap)


def test_pool_is_eight_selectable_assets():
    assert len(POOL_IDS) == 8 and "asan" in POOL_IDS and "valgrind" not in POOL_IDS


# ── fail-loud ───────────────────────────────────────────────────────────────
def test_selecting_unimplemented_asset_raises():
    sp = DFA.measurable_specs("holdout")[0]
    with pytest.raises(ValueError):
        DFA.detect_for_assets(sp, ["valgrind"], rv=RV, pool_ids=POOL_IDS)


def test_selecting_unknown_asset_raises():
    sp = DFA.measurable_specs("holdout")[0]
    with pytest.raises(ValueError):
        DFA.detect_for_assets(sp, ["not-an-asset"], rv=RV, pool_ids=POOL_IDS)


# ── 解码兜底适配层 ───────────────────────────────────────────────────────────
def test_adapter_not_installed_by_default():
    assert DFA.adapter_installed() is False
    assert subprocess.run is DFA._ORIG_RUN


def test_decode_safety_installs_and_fully_restores():
    before_run, before_env = subprocess.run, os.environ.get("WSL_UTF8")
    with DFA.decode_safety() as info:
        assert info["installed"] is True
        assert subprocess.run is not before_run
        assert os.environ.get("WSL_UTF8") == "1"
        assert len(info["layers"]) == 3
    assert subprocess.run is before_run
    assert os.environ.get("WSL_UTF8") == before_env
    assert DFA.adapter_installed() is False


def test_probe_returns_environment_facts():
    p = DFA.probe_wsl_banner()
    assert isinstance(p, dict) and "wsl_available" in p
    # 674d：`wsl` 命令不存在时（CI / 单层 Linux）probe 只回**缺环境事实**形态
    # （`{"wsl_available": False, "error": ...}`）——这是诚实报告而非缺陷；此时
    # "探测到了哪些 stderr 事实"不适用 ⇒ 条件 skip（断言在具备 WSL 的机器上不变）。
    if not p.get("wsl_available"):
        pytest.skip(f"本环境无 wsl 命令 ⇒ probe 只回缺环境事实：{p.get('error')!r}")
    assert "stderr_utf8_decodable" in p and "stderr_has_nul" in p


def test_strip_banner_removes_nul_and_wsl_lines():
    text = "before\nw\x00s\x00l\x00:\x00 \x00proxy\nwsl: some warning\nafter: real output\n"
    out = DFA._strip_banner(text)
    assert "before" in out and "after: real output" in out
    assert "proxy" not in out and "some warning" not in out


def test_strip_banner_keeps_ordinary_compiler_output():
    text = "x.cpp:3:5: warning: unused variable 'q' [-Wunused-variable]\nwarning: unsequenced\n"
    out = DFA._strip_banner(text)
    assert "unused variable" in out and "unsequenced" in out


def test_decode_safe_run_does_not_touch_binary_mode():
    cp = DFA._decode_safe_run([sys.executable, "-c", "print('hi')"], capture_output=True)
    assert cp.returncode == 0 and isinstance(cp.stdout, bytes)


# ── 保真报告（合成数据，不读产物）────────────────────────────────────────────
def test_fidelity_report_counts_agreements():
    doc = {"datasets": {"holdout": {"samples": [
        {"id": "h1", "recorded_detector": "asan", "recorded_verdict": "catch",
         "per_asset": {"asan": {"verdict": "catch"}}},
        {"id": "h2", "recorded_detector": "asan", "recorded_verdict": "catch",
         "per_asset": {"asan": {"verdict": "miss"}}},
    ]}}}
    rep = DFA.fidelity_report(doc)["holdout"]
    assert rep["n"] == 2 and rep["agree"] == 1 and rep["agree_pct"] == 50.0
    assert rep["disagreements"][0]["id"] == "h2"


def test_cli_probe_exit_zero():
    rc = subprocess.run([sys.executable, str(TOOLS / "detect_for_assets.py"), "--probe"],
                        capture_output=True, timeout=120)
    assert rc.returncode == 0


# ── 慢档：真调编译器 ─────────────────────────────────────────────────────────
@pytest.mark.slow
def test_h41_asan_reproduces_frozen_catch():
    """672h 冻结记录：h41 × asan = catch。若此条红 ⇒ 环境/适配层坏了，数字不可信。"""
    sp = next(s for s in DFA.measurable_specs("holdout") if s.id == "h41")
    with DFA.decode_safety():
        out = DFA.detect_for_assets(sp, ["asan"], rv=RV)
    assert out["verdict"] == "catch"
    assert "AddressSanitizer" in out["per_asset"]["asan"]["note"]


@pytest.mark.slow
def test_compile_time_asset_is_unknown_not_miss():
    sp = DFA.measurable_specs("holdout")[0]
    with DFA.decode_safety():
        out = DFA.detect_for_assets(sp, ["compile-time"], rv=RV)
    assert out["verdict"] == "unknown"
    assert "compile-time" in out["unknown_reasons"]


@pytest.mark.slow
def test_subset_or_keeps_individual_verdicts():
    sp = DFA.measurable_specs("holdout")[0]
    with DFA.decode_safety():
        out = DFA.detect_for_assets(sp, ["asan", "compile-time"], rv=RV)
    assert set(out["per_asset"]) == {"asan", "compile-time"}
    assert out["verdict"] == "catch"  # asan 命中即整条命中


@pytest.mark.slow
def test_corpus_code_materialization_runs():
    sp = DFA.measurable_specs("corpus")[0]
    with DFA.decode_safety():
        out = DFA.detect_for_assets(sp, ["asan"], rv=RV)
    assert out["verdict"] in ("catch", "miss", "unknown")
    assert out["input_mode"] == "code_materialized"


@pytest.mark.slow
def test_build_attribution_limit_two_smoke():
    doc = DFA.build_attribution("corpus", limit=2, verbose=False)
    assert doc["n_measurable"] == 2 and len(doc["samples"]) == 2
    assert all(set(s["per_asset"]) == set(POOL_IDS) for s in doc["samples"])
    assert doc["environment"]["installed"] is True


@pytest.mark.slow
def test_module_selftest_exits_zero():
    rc = subprocess.run([sys.executable, str(TOOLS / "detect_for_assets.py"), "--check"],
                        capture_output=True, timeout=900)
    assert rc.returncode == 0
