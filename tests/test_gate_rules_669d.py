# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tests/test_gate_rules_669d.py — 669d B 段六条门禁的回归测试。

纪律（669d B7）：**每条规则至少 1 个正例 + 1 个反例**。
反例的意义不只是"测得准"，更是**射程自检** —— 若改了事实源规则仍报绿，
说明这条门禁根本没进射程（666「81.2% 假绿」就是这个形态）。

所有用例在 `tmp_path` 里构造最小仓库，绝不触碰真实仓库。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import gate_rules_669d as G  # noqa: E402


# ─────────────────────────────────────────────────────────────────────────────
# 构造 helper
# ─────────────────────────────────────────────────────────────────────────────

def wj(root: Path, rel: str, obj) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8"))


def wt(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8"))


def card(root: Path, rel: str, meta: dict) -> None:
    """写一张 ATOM 卡（YAML frontmatter + 正文）。"""
    try:
        import yaml
    except ImportError:
        pytest.skip("pyyaml 未安装")
    body = yaml.safe_dump(meta, allow_unicode=True, sort_keys=True)
    wt(root, rel, f"---\n{body}---\n\n# {meta.get('id','')}\n")


# ─────────────────────────────────────────────────────────────────────────────
# B1 · G-RATE-CONSISTENCY
# ─────────────────────────────────────────────────────────────────────────────

def _rate_repo(root: Path, front_rate: float, paper_rate: float) -> None:
    wj(root, "data/holdout_reveal_3_665.json",
       {"error_subset": {"catch": 14, "miss": 2, "unknown": 1, "detect_rate_pct": 87.5}})
    wj(root, "web/data/experiments.json",
       {"corpus_rates": [{"label": "holdout", "rate": front_rate, "num": 14, "den": 16}]})
    wt(root, "research/paper_draft_v0.5.md", f"holdout 检出率 {paper_rate}%。\n")


def test_b1_positive_three_places_agree():
    root = Path(__import__("tempfile").mkdtemp(prefix="b1pos-"))
    _rate_repo(root, 87.5, 87.5)
    assert G.check_rate_consistency(root) == [], "三处一致却报红 ⇒ 误报"


def test_b1_negative_frontend_disagrees():
    root = Path(__import__("tempfile").mkdtemp(prefix="b1neg-"))
    _rate_repo(root, 50.0, 87.5)          # 前端写 50.0，产物现算 87.5
    f = G.check_rate_consistency(root)
    assert any(x["severity"] == G.BLOCK and "web/data" in x["target"] for x in f), \
        "前端与产物不一致仍报绿 ⇒ 无射程（假绿）"


def test_b1_negative_paper_disagrees():
    root = Path(__import__("tempfile").mkdtemp(prefix="b1neg2-"))
    _rate_repo(root, 87.5, 11.1)          # 论文写 11.1%
    f = G.check_rate_consistency(root)
    assert any(x["severity"] == G.BLOCK and "paper_draft" in x["target"] for x in f), \
        "论文与产物不一致仍报绿 ⇒ 无射程（假绿）"


def test_b1_scale_normalized_0to1_matches_100():
    """0–1 标度与百分比标度应视为一致（避免标度混用造成的假红）。"""
    root = Path(__import__("tempfile").mkdtemp(prefix="b1scale-"))
    wj(root, "data/counterfactual_cases_665.json",
       {"scores": {"f1": 1.0}, "confusion": {"tp": 2, "fp": 0, "tn": 8, "fn": 0}})
    wj(root, "web/data/experiments.json",
       {"corpus_rates": [{"label": "cf", "rate": 100.0, "num": 10, "den": 10}]})
    wt(root, "research/paper_draft_v0.5.md", "反事实 F1=1.0\n")
    assert G.check_rate_consistency(root) == []


# ─────────────────────────────────────────────────────────────────────────────
# B2 · G-DENOMINATOR
# ─────────────────────────────────────────────────────────────────────────────

def _den_ok(root: Path) -> None:
    wj(root, "data/external_corpus_reveal_665.json", {
        "catch": 14, "miss": 18, "unknown": 5, "not_error": 3, "total": 40,
        "detect_rate_pct": 43.8, "rate_pct_all_samples": 35.0,
        "denominator": {"value": 32, "meaning": "catch+miss",
                        "excluded": {"unknown": 5, "not_error": 3}, "all_samples": 40},
        "results": [{"id": f"d{i}", "verdict": "catch"} for i in range(14)] +
                   [{"id": f"m{i}", "verdict": "miss"} for i in range(18)] +
                   [{"id": f"u{i}", "verdict": "unknown"} for i in range(5)] +
                   [{"id": f"n{i}", "verdict": "not_error"} for i in range(3)],
    })


def test_b2_positive_denominator_declared_and_recomputable():
    root = Path(__import__("tempfile").mkdtemp(prefix="b2pos-"))
    _den_ok(root)
    assert G.check_denominator(root) == [], "分母齐全且可重算却报红 ⇒ 误报"


def test_b2_negative_rate_without_denominator():
    root = Path(__import__("tempfile").mkdtemp(prefix="b2neg-"))
    wj(root, "data/external_corpus_reveal_665.json",
       {"catch": 14, "miss": 18, "detect_rate_pct": 43.8})      # 无 denominator
    f = G.check_denominator(root)
    assert any(x["severity"] == G.BLOCK and "denominator 字段" in x["message"] for x in f)


def test_b2_negative_k_greater_than_denominator():
    root = Path(__import__("tempfile").mkdtemp(prefix="b2neg2-"))
    wj(root, "data/external_corpus_reveal_665.json",
       {"catch": 99, "miss": 18, "denominator": {"value": 32}})   # 99 > 32
    f = G.check_denominator(root)
    assert any(x["severity"] == G.BLOCK and "分子" in x["message"] for x in f)


def test_b2_negative_summary_disagrees_with_detail():
    root = Path(__import__("tempfile").mkdtemp(prefix="b2neg3-"))
    wj(root, "data/external_corpus_reveal_665.json", {
        "catch": 14, "miss": 18, "total": 40,
        "denominator": {"value": 32},
        "detect_rate_pct": 43.8, "rate_pct_all_samples": 35.0,
        # 明细里实际只有 10 条 catch，汇总却写 14
        "results": [{"id": f"d{i}", "verdict": "catch"} for i in range(10)] +
                   [{"id": f"m{i}", "verdict": "miss"} for i in range(18)],
    })
    f = G.check_denominator(root)
    assert any(x["severity"] == G.BLOCK and "逐样本明细重算" in x["message"] for x in f), \
        "汇总与明细不一致仍报绿 ⇒ 无射程"


def test_b2_negative_rate_not_recomputable():
    root = Path(__import__("tempfile").mkdtemp(prefix="b2neg4-"))
    wj(root, "data/external_corpus_reveal_665.json",
       {"catch": 14, "miss": 18, "detect_rate_pct": 99.9,       # 应为 43.8
        "denominator": {"value": 32}})
    f = G.check_denominator(root)
    assert any(x["severity"] == G.BLOCK and "重算" in x["message"] for x in f)


def test_b2_generated_by_is_not_a_rate():
    """回归：`generated_by/generated_at` 含子串 'rate'，不得被当成比率字段。"""
    root = Path(__import__("tempfile").mkdtemp(prefix="b2gen-"))
    wj(root, "data/holdout/holdout.json",
       {"generated_by": "660 C2", "generated_at": "2026-09-28", "samples": []})
    assert G.check_denominator(root) == []
    assert not G._is_rate_key("generated_by")
    assert G._is_rate_key("rate_pct")


# ─────────────────────────────────────────────────────────────────────────────
# B3 · G-STATS-FROZEN
# ─────────────────────────────────────────────────────────────────────────────

def test_b3_positive_protocol_frozen_and_implemented():
    root = Path(__import__("tempfile").mkdtemp(prefix="b3pos-"))
    wt(root, "research/05_evaluation_protocol.md",
       "# 协议\n\n- 区间估计：Clopper-Pearson 95% CI\n"
       "- 独立样本比较：Fisher 精确检验\n- 配对比较：McNemar 检验\n"
       "- 标注一致性：Cohen's kappa\n- 多重比较：BH 校正\n")
    wt(root, "tools/stats_ci_669.py",
       "def clopper_pearson(k, n): ...\ndef fisher_exact(a,b,c,d): ...\n"
       "def mcnemar(b, c): ...\n")
    f = G.check_stats_frozen(root)
    assert not any(x["severity"] == G.BLOCK for x in f), f


def test_b3_negative_protocol_missing_methods():
    root = Path(__import__("tempfile").mkdtemp(prefix="b3neg-"))
    wt(root, "research/05_evaluation_protocol.md", "# 协议\n\n只写了样本量。\n")
    f = G.check_stats_frozen(root)
    blocks = [x for x in f if x["severity"] == G.BLOCK]
    assert len(blocks) >= 3, "协议完全没冻结统计口径却未报红 ⇒ 无射程"
    assert any("Clopper-Pearson" in x["message"] for x in blocks)


def test_b3_negative_declared_but_not_implemented():
    root = Path(__import__("tempfile").mkdtemp(prefix="b3neg2-"))
    wt(root, "research/05_evaluation_protocol.md",
       "# 协议\n\n使用 Clopper-Pearson 与 Fisher 与 McNemar。\n")
    (root / "tools").mkdir(parents=True, exist_ok=True)
    wt(root, "tools/unrelated.py", "def foo(): pass\n")      # 无任何实现
    f = G.check_stats_frozen(root)
    assert any(x["severity"] == G.BLOCK and "找不到实现" in x["message"] for x in f), \
        "协议声明了但无实现仍报绿 ⇒ 无射程"


# ─────────────────────────────────────────────────────────────────────────────
# B4 · G-BOUNDARY-REQUIRED
# ─────────────────────────────────────────────────────────────────────────────

def test_b4_positive_verified_has_triple_and_draft_marked():
    root = Path(__import__("tempfile").mkdtemp(prefix="b4pos-"))
    card(root, "atoms/conc/ATOM-A.md", {
        "id": "ATOM-A", "status": "verified",
        "mutation_set_hash": "abc123", "mutation_count": 12, "generator_version": "669d",
    })
    card(root, "atoms/draft650/ATOM-B.md", {
        "id": "ATOM-B", "status": "draft", "boundary": "unknown",
    })
    assert G.check_boundary_required(root) == []


def test_b4_negative_verified_missing_triple():
    root = Path(__import__("tempfile").mkdtemp(prefix="b4neg-"))
    card(root, "atoms/mem/ATOM-C.md", {"id": "ATOM-C", "status": "verified"})
    f = G.check_boundary_required(root)
    assert any(x["severity"] == G.BLOCK and "provenance 三元组" in x["message"] for x in f), \
        "verified 卡缺 provenance 仍报绿 ⇒ 无射程"


def test_b4_negative_draft_without_boundary_marker():
    root = Path(__import__("tempfile").mkdtemp(prefix="b4neg2-"))
    card(root, "atoms/draft650/ATOM-D.md", {"id": "ATOM-D", "status": "draft"})
    f = G.check_boundary_required(root)
    assert any(x["severity"] == G.BLOCK and "boundary" in x["message"] for x in f), \
        "草稿卡未标 boundary 仍报绿 ⇒ 无射程"


def test_b4_positive_draft_exempt_with_claim_boundary():
    """草稿卡可用 claim_boundary 满足"显式标记"要求。"""
    root = Path(__import__("tempfile").mkdtemp(prefix="b4pos2-"))
    card(root, "atoms/draft650/ATOM-E.md", {
        "id": "ATOM-E", "status": "draft", "claim_boundary": {"standard": ["C++17"]}})
    assert G.check_boundary_required(root) == []


# ─────────────────────────────────────────────────────────────────────────────
# B5 · G-BASELINE-EXISTS
# ─────────────────────────────────────────────────────────────────────────────

def test_b5_positive_baseline_covers_metrics():
    root = Path(__import__("tempfile").mkdtemp(prefix="b5pos-"))
    wj(root, "web/data/experiments.json", {
        "corpus_rates": [{"label": "holdout（双档）", "rate": 87.5, "num": 14, "den": 16}],
        "mutation": [{"label": "core · on_scored", "rate": 97.3}],
    })
    wj(root, "data/baseline.json", {
        "holdout": {"static_gate_rate_pct": 12.5},
        "mutation": {"core_kill_rate_pct": 97.3},
    })
    assert G.check_baseline_exists(root) == []


def test_b5_negative_metric_without_baseline():
    root = Path(__import__("tempfile").mkdtemp(prefix="b5neg-"))
    wj(root, "web/data/experiments.json", {
        "corpus_rates": [{"label": "external 全样本", "rate": 35.0, "num": 14, "den": 40}]})
    wj(root, "data/baseline.json", {"mutation": {"core_kill_rate_pct": 97.3}})
    f = G.check_baseline_exists(root)
    assert any(x["severity"] == G.BLOCK and "无对应基线" in x["message"] for x in f), \
        "实验结果无基线仍报绿 ⇒ 无射程"


def test_b5_negative_baseline_file_missing():
    root = Path(__import__("tempfile").mkdtemp(prefix="b5neg2-"))
    wj(root, "web/data/experiments.json",
       {"mutation": [{"label": "core", "rate": 97.3}]})
    f = G.check_baseline_exists(root)
    assert any(x["severity"] == G.BLOCK and "baseline 文件不存在" in x["message"] for x in f)


def test_b5_rates_block_but_counts_warn():
    """率指标缺基线 ⇒ BLOCK；构成计数缺基线只 ⇒ WARN。"""
    root = Path(__import__("tempfile").mkdtemp(prefix="b5mix-"))
    wj(root, "web/data/experiments.json", {
        "corpus_rates": [{"label": "holdout", "rate": 87.5, "num": 14, "den": 16}],
        "ability": [{"label": "知识卡（实）", "value": 42}],
    })
    wj(root, "data/baseline.json", {})
    f = G.check_baseline_exists(root)
    sev = {x["target"].rsplit("←", 1)[-1].strip(): x["severity"] for x in f}
    assert sev.get("holdout") == G.BLOCK
    assert sev.get("知识卡（实）") == G.WARN


# ─────────────────────────────────────────────────────────────────────────────
# B6 · G-IRR（只 WARN）
# ─────────────────────────────────────────────────────────────────────────────

def test_b6_positive_irr_recorded():
    root = Path(__import__("tempfile").mkdtemp(prefix="b6pos-"))
    card(root, "atoms/conc/ATOM-F.md",
         {"id": "ATOM-F", "status": "verified", "verified_by": "human:alice"})
    wj(root, "data/irr_records.json",
       {"records": {"ATOM-F": {"raters": 2, "kappa": 0.8}}})
    f = G.check_irr(root)
    assert not any("无 IRR 记录" in x["message"] for x in f), f


def test_b6_negative_no_irr_record_warns_not_blocks():
    root = Path(__import__("tempfile").mkdtemp(prefix="b6neg-"))
    card(root, "atoms/conc/ATOM-G.md",
         {"id": "ATOM-G", "status": "verified", "verified_by": "human:alice"})
    f = G.check_irr(root)
    assert any(x["severity"] == G.WARN and "无 IRR 记录" in x["message"] for x in f)
    assert not any(x["severity"] == G.BLOCK for x in f), "B6 只 WARN，不得 BLOCK"


def test_b6_negative_kappa_too_low():
    root = Path(__import__("tempfile").mkdtemp(prefix="b6neg2-"))
    card(root, "atoms/conc/ATOM-H.md",
         {"id": "ATOM-H", "status": "verified", "verified_by": "human:alice"})
    wj(root, "data/irr_records.json",
       {"records": {"ATOM-H": {"raters": 2, "kappa": 0.3}}})
    f = G.check_irr(root)
    assert any("κ=0.3" in x["message"] for x in f)


def test_b6_machine_principal_is_not_human():
    """machine:/redteam: 前缀不算人工标注，不要求 IRR。"""
    root = Path(__import__("tempfile").mkdtemp(prefix="b6mach-"))
    card(root, "atoms/ub/ATOM-I.md",
         {"id": "ATOM-I", "status": "machine-verified", "verified_by": "machine:split_668"})
    f = G.check_irr(root)
    assert not any("ATOM-I" in x["target"] for x in f)


# ─────────────────────────────────────────────────────────────────────────────
# 注册表与射程
# ─────────────────────────────────────────────────────────────────────────────

def test_registry_has_six_rules():
    assert len(G.RULES669D) == 6, "669d 应为六条规则"
    ids = [r["id"] for r in G.RULES669D]
    assert ids == ["G-RATE-CONSISTENCY", "G-DENOMINATOR", "G-STATS-FROZEN",
                   "G-BOUNDARY-REQUIRED", "G-BASELINE-EXISTS", "G-IRR"]


def test_every_rule_has_id_name_fn():
    for r in G.RULES669D:
        assert r["id"] and r["name"] and callable(r["fn"]), r


def test_run_all_runs_every_rule():
    root = Path(__import__("tempfile").mkdtemp(prefix="runall-"))
    res = G.run_all(root)
    rules_hit = {x["rule"] for x in res}
    for r in G.RULES669D:
        assert r["id"] in rules_hit, f"{r['id']} 未执行（空目录应至少产出缺失告警）"


def test_run_all_survives_rule_exception():
    """规则自身异常不得让整条门禁崩掉。"""
    root = Path(__import__("tempfile").mkdtemp(prefix="exc-"))
    orig = G.RULES669D[0]["fn"]
    G.RULES669D[0]["fn"] = lambda _r: (_ for _ in ()).throw(RuntimeError("boom"))
    try:
        res = G.run_all(root, ["G-RATE-CONSISTENCY"])
        assert any("规则执行异常" in x["message"] for x in res)
    finally:
        G.RULES669D[0]["fn"] = orig
