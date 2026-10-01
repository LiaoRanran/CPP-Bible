# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671g A2/A4：锁定全量实验数字的**可复现性**与环境探测纯函数。

这些测试守的是 671g A 的红线：每个声称的数字必须能从事实源现算；
任何汇总字段与逐样本明细对不上、任何率与 k/n 算不回，都会在这里变红。
盲测冻结值与扩样累计值是**两个不同口径**，两组都锁定（不许互相覆盖）。
"""
from __future__ import annotations

import numbers_671g as N
import env_probe_671g as E


# ── A2：结构类数字 ──────────────────────────────────────────────────────────────

def test_ledger_452():
    m = N.metric_ledger(N.ROOT)
    assert m["available"] and m["value"] == 452 and m["match"]


def test_rules_67_with_severity():
    m = N.metric_rules(N.ROOT)
    assert m["available"] and m["value"] == 67
    assert m["severity"]["block"] == 44
    assert m["severity"]["warn"] == 16
    assert m["severity"]["advice"] == 7


def test_cards_atoms_real_42_but_total_123():
    m = N.metric_cards(N.ROOT)
    assert m["available"]
    assert m["value"]["atoms_real"] == 42          # 论文"42 张实卡"口径
    assert m["value"]["cards_total"] == 123        # 全量口径（不是 42）


# ── A2：holdout 双口径都要能复现 ─────────────────────────────────────────────

def test_holdout_blind_87_5():
    m = N.metric_holdout(N.ROOT)
    b = m["blind_reveal3"]
    assert (b["k"], b["n"]) == (14, 16)
    assert abs(b["rate_pct"] - 87.5) < 0.05
    assert b["cp95"][0] < 87.5 < b["cp95"][1]


def test_holdout_cumulative_recomputed_from_per_sample_81():
    m = N.metric_holdout(N.ROOT)
    c = m["cumulative_671a"]
    # 关键：k/n 是从 per_sample[] 独立重数出来的，不信任汇总字段
    assert (c["k"], c["n"]) == (17, 21)
    assert abs(c["rate_pct"] - 81.0) < 0.05       # 80.9524 → 81.0
    assert c["tally"]["catch"] == 17 and c["tally"]["miss"] == 4
    assert c["false_positive"] == 2                  # 对照 11 中 h3/h35 被 catch


# ── A2：corpus 双口径 + 分层 ────────────────────────────────────────────────

def test_corpus_blind_43_8_and_all_35():
    m = N.metric_corpus(N.ROOT)
    b = m["blind_665"]
    assert (b["measurable"]["k"], b["measurable"]["n"]) == (14, 32)
    assert abs(b["measurable"]["rate_pct"] - 43.8) < 0.05
    assert (b["all_samples"]["k"], b["all_samples"]["n"]) == (14, 40)
    assert abs(b["all_samples"]["rate_pct"] - 35.0) < 0.05


def test_corpus_cumulative_from_per_sample_54_2():
    m = N.metric_corpus(N.ROOT)
    c = m["cumulative_671a"]
    assert (c["k"], c["n"]) == (26, 48)
    assert abs(c["rate_pct"] - 54.2) < 0.05
    assert c["tally"] == {"catch": 26, "miss": 22, "unknown": 9, "not_error": 3}
    assert (c["layers"]["sanitizer"]["k"], c["layers"]["sanitizer"]["n"]) == (19, 24)
    assert (c["layers"]["compiler-warn"]["k"], c["layers"]["compiler-warn"]["n"]) == (6, 14)
    assert (c["layers"]["cross-compile"]["k"], c["layers"]["cross-compile"]["n"]) == (1, 10)
    # n=0 的层必须拒答率（fail-loud），不许编 0
    assert c["layers"]["perf"]["rate_pct"] is None
    assert c["layers"]["other"]["rate_pct"] is None


# ── A2：变异 / 反事实 / 重注入 ─────────────────────────────────────────────

def test_mutation_core_and_all():
    m = N.metric_mutation(N.ROOT)
    assert (m["core"]["k"], m["core"]["n"]) == (110, 113)
    assert abs(m["core"]["rate_pct"] - 97.3) < 0.05
    assert (m["all"]["k"], m["all"]["n"]) == (128, 157)
    assert abs(m["all"]["rate_pct"] - 81.5) < 0.05


def test_counterfactual_two_disjoint_sets_f1_one():
    m = N.metric_counterfactual(N.ROOT)
    assert m["cf_665_10"]["f1"] == 1.0 and m["cf_665_10"]["confusion"]["tp"] == 2
    assert m["cf_669d_20"]["f1"] == 1.0 and m["cf_669d_20"]["confusion"]["tp"] == 7
    # 两套不重叠、不合并：分母分别 10 和 20
    assert m["cf_665_10"]["f1"] == m["cf_669d_20"]["f1"] == 1.0


def test_defect_reinject_6_of_6():
    m = N.metric_defect_injection(N.ROOT)
    assert m["available"] and (m["k"], m["n"]) == (6, 6)
    assert m["rate_pct"] == 100.0
    assert m["total_defects"] == 15 and m["not_reinjectable"] == 9


def test_collect_no_self_inconsistency():
    rep = N.collect(N.ROOT)
    assert rep["self_inconsistent"] == []
    assert set(rep["order"]) >= {"holdout", "corpus", "ledger_events", "rules_total"}


# ── A2：率的 fail-loud 语义（n=0 不许给率）────────────────────────────

def test_rate_zero_denominator_refuses():
    r = N._rate(0, 0)
    assert r["rate_pct"] is None and r["cp95"] is None and "拒绝给率" in r["note"]


def test_rate_cp_matches_cp_bounds():
    r = N._rate(14, 16)
    assert 61.0 < r["cp95"][0] < 62.0 and 98.0 < r["cp95"][1] < 99.0


def test_tally_independent_of_summary_fields():
    rows = [{"verdict": "catch"}, {"verdict": "miss"}, {"verdict": "unknown"},
            {"verdict": "not_error"}, {"verdict": "catch"}]
    assert N._tally(rows) == {"catch": 2, "miss": 1, "unknown": 1, "not_error": 1}


# ── A3：逐样本导出 ────────────────────────────────────────────────────────────

def test_per_sample_export_counts_and_env():
    det = N.per_sample_export(N.ROOT, env={"schema": "x"})
    d = det["datasets"]
    assert d["holdout"]["n"] == 40 and d["corpus"]["n"] == 60
    assert d["counterfactual_cases"]["n"] == 30
    assert d["mutation_cases"]["n"] == 370
    assert det["env"]["schema"] == "x"
    # holdout 行必须带来源与盲态标记
    srcs = {r["source"] for r in d["holdout"]["rows"]}
    assert "reused_reveal_3" in srcs and "measured_671a" in srcs


# ── A4：环境探测纯函数（不起子进程）──────────────────────────────────────

def test_assemble_full_env():
    env = E.assemble(
        host={"system": "Windows"}, python_ver="3.13.13",
        wsl={"wsl_gpp": "g++ 13.3.0", "setarch": "setarch -R 可用", "aslr_sysctl": 2},
        local={"gpp": {"version": "g++ 13.1.0"}, "clang": {"version": "clang 22"}},
        aslr={"setarch_available": True}, opt_levels=["-O0", "-O2"])
    assert env["host_os"]["system"] == "Windows"
    assert env["wsl_gpp"] == "g++ 13.3.0"
    assert env["local_gpp"] == "g++ 13.1.0"
    assert env["aslr_control"]["setarch_available"] is True
    assert env["opt_levels"] == ["-O0", "-O2"]
    assert E.missing_required(env) == []


def test_missing_required_flags_gaps():
    env = E.assemble(host={"system": "Linux"}, python_ver="3.13", wsl={},
                    local={}, aslr={})
    miss = E.missing_required(env)
    assert "wsl_gpp" in miss and "local_gpp" in miss
    assert "aslr_control.setarch_available" in miss


def test_probe_compiler_missing_command():
    r = E.probe_compiler(["definitely_not_a_compiler_xyz_671g", "--version"])
    assert r["present"] is False and r["version"] is None


def test_real_machine_has_required_env():
    env = E.probe()
    # 本机实测：WSL g++ 与本地 g++ 都应可用（671g 运行机）
    assert env["wsl_gpp"] and "13.3.0" in env["wsl_gpp"]
    assert env["local_gpp"]
    assert env["aslr_control"]["setarch_available"] is True
    # ASLR 内核开关 2 = 开 ⇒ 实验必须 setarch -R（不能谎称已全局关闭）
    assert env["aslr_control"]["wsl_kernel_randomize_va_space"] == 2
