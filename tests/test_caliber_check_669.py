# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""669 P1 回归锁：口径清场（区间存在性 / 分母声明 / 声称值↔现算值）。

锁四件事：
  ① `ci_check` 的射程：**缺 CI 必红**、带 CI 必绿（含围栏 / 豁免注释 / 日期 / 编号误判的阴性）；
  ② `caliber_check_669` 的产物自洽：改一个 k ⇒ `G-RATE-PRODUCT` 必红；
  ③ 现算率必须等于产物自称的率（防止"改了生成器没重跑"的 668 事故形态复发）；
  ④ 活跃文档（research/paper_v0.4.md + README）当前**全绿**——
     这条会随文档改动而红，红时说明口径真的漂了（不是测试写死数字）。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import caliber_check_669 as C  # noqa: E402
import ci_check as ci  # noqa: E402


# ── ① ci_check 射程 ────────────────────────────────────────────────────────
def test_ci_check_flags_missing_ci(tmp_path: Path):
    f = tmp_path / "a.md"
    f.write_text("- holdout 检出率 14/16 = 87.5%\n", encoding="utf-8")
    findings, seen = ci.scan([f])
    assert len(findings) == 1 and findings[0]["k"] == 14, findings


def test_ci_check_green_with_ci(tmp_path: Path):
    f = tmp_path / "b.md"
    f.write_text("- holdout 检出率 14/16 = 87.5%（95% CI 61.7–98.4）\n", encoding="utf-8")
    findings, seen = ci.scan([f])
    assert findings == [] and len(seen) == 1


def test_ci_check_negative_cases(tmp_path: Path):
    """阴性：围栏内 / 显式豁免 / 日期 / 威胁编号 / 标识符路径 都不该误判。"""
    cases = [
        "```\n14/16 = 87.5% 检出率\n```\n",
        "- 检出率 14/16 <!-- ci-check: ignore（本节是历史记录） -->\n",
        "- 日期 2026/09/30 的批次\n",
        "- **度量混淆**：威胁 7/8 的量化\n",
        "- 指标分层（A5 / 08_metrics）\n",
        "- 0/0 不可判\n",
    ]
    for i, text in enumerate(cases):
        f = tmp_path / f"n{i}.md"
        f.write_text(text, encoding="utf-8")
        findings, _ = ci.scan([f])
        assert findings == [], (i, text, findings)


# ── ② 产物自洽：改一个 k 必红 ──────────────────────────────────────────────
def test_caliber_product_self_consistency_is_red_on_tamper():
    rates = C.compute_rates()
    assert C.check_products(rates) == [], "现算率与产物自称不一致（产物或事实源漂了）"
    tampered = [dict(r) for r in rates]
    tampered[0]["k"] = tampered[0]["k"] + 1
    assert C.check_products(tampered), "改一个 k 仍报绿 ⇒ 自洽判据没进射程"


# ── ③ 现算值 == 产物自称值（四个事实源逐一钉） ──────────────────────────────
def test_rates_match_products():
    by_id = {r["id"]: r for r in C.compute_rates()}
    ext = C._j("data/external_corpus_reveal_665.json")
    assert by_id["external.valid"]["rate_pct"] == ext["detect_rate_pct"], by_id["external.valid"]
    assert by_id["external.all"]["rate_pct"] == ext["rate_pct_all_samples"]
    assert by_id["external.c.total"]["k"] == 0 and by_id["external.c.total"]["cp_hi_pct"] == 60.2, \
        "零计数上界必须显形（0/4 ⇒ 60.2%）"
    ho = C._j("data/holdout_reveal_3_665.json")
    assert by_id["holdout.valid"]["k"] == ho["error_subset"]["catch"]
    mut = C._j("data/656_mutation_report_all.json")
    assert by_id["mutation.all"]["rate_pct"] == mut["kill_rate_on_scored"]


# ── ④ 当前活跃文档必须全绿（红 = 口径真的漂了）─────────────────────────────
def test_live_docs_are_caliber_clean():
    rates = C.compute_rates()
    bad_docs, seen = C.check_docs(rates)
    assert bad_docs == [], bad_docs
    assert C.check_caliber_per_doc(seen) == [], C.check_caliber_per_doc(seen)
    assert len(seen) >= 10, "文档率断言太少 ⇒ 扫描可能失效（射程自检）"


def test_research_ci_gate_is_green():
    rc, out = C.run_ci_check()
    assert rc == 0, out[-500:]


@pytest.mark.parametrize("frozen", ["research/paper_v0.1.md", "research/paper_v0.2.md",
                                    "research/paper_v0.3.md"])
def test_frozen_papers_are_exempt_but_declared(frozen: str):
    """冻结稿必须**显式**登记在豁免台账里（不是靠"扫不到"而绿）。"""
    assert ci.exempt_reason(frozen), f"{frozen} 未在 EXEMPT 台账里 ⇒ 射程静默漏掉"
