# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""672i W4 LLM 裁判臂测试（mock LLM 响应，≥20 条断言，不联网）。"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def _load(rel: str):
    spec = importlib.util.spec_from_file_location(Path(rel).stem, str(ROOT / rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


L = _load("tools/llm_arm_672i.py")


# ── 预注册与抽样（可复算、非随机）────────────────────────────────────────────
def test_prereg_locked_and_availability_registered():
    p = json.loads((ROOT / "data/experiments/prereg_672i.json").read_text(encoding="utf-8"))
    assert p["status"] == "locked_before_experiment"
    assert p["methods"]["prompt"]["version"] == "v1"
    assert p["methods"]["api_protocol"]["model"] == "glm-4"
    avail = p["context"]["model_availability"]
    # GPT-4/Claude 与 DeepSeek 的不可用必须如实登记（不许假装用了它们）
    assert "不可用" in avail["gpt4_claude"] and "401" in avail["deepseek"]
    assert "glm-4" in avail["zhipu_glm"].lower()
    # 反泄漏条款必须在预注册里
    assert any("注释" in x for x in p["methods"]["prompt"]["answer_leak_control"])


def test_sampling_is_reproducible_stratified():
    s = L.select_samples()
    assert len(s) == 20
    assert sum(1 for x in s if x["planted"] is True) == 12
    assert sum(1 for x in s if x["planted"] is False) == 8
    assert sum(1 for x in s if x["planted"] is True and x["verdict_fd"] == "catch") == 6
    assert sum(1 for x in s if x["planted"] is True and x["verdict_fd"] == "miss") == 6
    assert [x["id"] for x in s] == sorted(x["id"] for x in s)
    # 抽样必须稳定（两次调用一致）
    assert [x["id"] for x in L.select_samples()] == [x["id"] for x in s]
    # 每个样本的源文件必须存在（否则 LLM 看不到代码）
    assert all((ROOT / x["src"]).is_file() for x in s)


# ── 反泄漏：注释剥离 ─────────────────────────────────────────────────────────
def test_strip_comments_removes_answers_but_keeps_code():
    src = ("// 故意双重释放（ASan 取证）\n"
           "int* p = new int(7); /* 这是答案 */\n"
           "std::printf(\"%s\", \"http://x/y\");  // 行注释\n")
    out = L.strip_comments(src)
    assert "故意" not in out and "ASan" not in out and "答案" not in out
    assert "行注释" not in out
    assert "new int(7)" in out and "http://x/y" in out
    assert "//" not in out.replace("http://", "")


def test_strip_comments_handles_real_fixtures():
    # 真夹具：头注释是"答案"，剥后不得残留
    code = L.strip_comments((ROOT / "Appendix/ub/ub_double_free.cpp").read_text(encoding="utf-8"))
    assert "ASan" not in code and "double-free" not in code.lower()
    assert "std::free(p)" in code and "int main" in code


# ── 解析与假裁判 ─────────────────────────────────────────────────────────────
def test_parse_verdict_robustness():
    fenced = '```json\n{"has_defect": true, "category": "UB", "confidence": 0.8}\n```'
    v = L.parse_verdict(fenced)
    assert v and v["has_defect"] is True and v["category"] == "UB"
    prose = 'Sure. {"has_defect": false, "reason": "clean"} thanks'
    assert L.parse_verdict(prose)["has_defect"] is False
    assert L.parse_verdict("no json") is None
    assert L.parse_verdict('{"category":"x"}') is None
    assert L.parse_verdict('{"has_defect": 1}')["has_defect"] is True   # 真值强制转换


def test_mock_judge_is_deterministic_and_parseable():
    a = L.mock_judge("int main(){}", "h1")
    b = L.mock_judge("int main(){}", "h1")
    assert a == b and a["mock"] is True
    assert L.parse_verdict(a["text"]) is not None


def test_mock_run_pipeline_metrics_internal_consistency():
    rep = L.run(use_mock=True, write=False)
    m = rep["metrics"]
    assert rep["mode"].startswith("mock")
    assert m["llm_n"] + len(rep["unknown_samples"]) == 12
    assert m["llm_k"] <= m["llm_n"] and m["fd_k"] <= m["llm_n"]
    assert m["llm_false_positive"]["n"] == 8
    assert m["llm_false_positive"]["fp"] <= 8
    assert 0.0 <= m["agreement"]["rate"] <= 1.0
    assert m["delta_fd_minus_llm_pp"] == round((m["fd_k"] - m["llm_k"]) / m["llm_n"] * 100, 1)
    assert set(rep["hypothesis_verdicts"]) == {"H1_fd_minus_llm_gt_20pp",
                                               "H2_llm_fp_lt_25pct",
                                               "H3_agreement_ge_0.6",
                                               "H4_layer_delta_gt_20pp"}
    assert all(r["truth"] in ("error", "control") for r in rep["per_sample"])
    assert all(r["fd"] in ("catch", "miss") for r in rep["per_sample"] if r["truth"] == "error")


# ── 真产物（若已跑）──────────────────────────────────────────────────────────
def test_live_product_consistency():
    p = ROOT / "data/experiments/llm_arm_672i.json"
    raw = ROOT / "data/experiments/llm_arm_672i_raw.jsonl"
    if not p.is_file():
        return
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d["schema"] == "queyi-llm-arm/672i"
    assert d["mode"] == "live_api" and d["model"]["name"] == "glm-4"
    m = d["metrics"]
    assert m["llm_n"] + len(d["unknown_samples"]) == 12
    assert m["llm_false_positive"]["n"] == 8
    # 逐条原始响应可审计：raw 行数 ≥ 样本数，且 model 全是 glm-4（mock 行不得混入）
    rows = [json.loads(x) for x in raw.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) >= 20
    assert {r["model"] for r in rows} == {"glm-4"}
    assert all(r["prompt_version"] == "v1" for r in rows)
    assert sum(int(r["usage"].get("total_tokens") or 0) for r in rows) > 0
    # token 记账与 raw 对得上
    assert d["usage_total"]["total_tokens"] == sum(
        int(r["usage"].get("total_tokens") or 0) for r in rows
        if not r.get("retry"))
    # 泄漏风险样本必须显式列出（本批 h1 的路径名含 race）
    assert "h1" in d["answer_leak_risk_samples"]
    # 判决方向：本批实测 LLM 检出 > FD（与 H1 预期相反）——只断言"已如实落盘"，不断言方向
    assert "不成立" in d["hypothesis_verdicts"]["H1_fd_minus_llm_gt_20pp"]
