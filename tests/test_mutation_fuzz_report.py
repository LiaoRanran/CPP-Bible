"""565 Part 2 · mutation 报告口径层（分子/分母 + C-P 双侧区间 + 活雷/样本不足标注）。

为什么不打门禁也能验：报告层是**纯函数**（吃 `per` 行的列表，吐口径块）。这里直接从**已提交的
真实基线** `data/mutation/full_baseline_v1.json` 的 `results` **派生**同样的行喂进去——既验了
口径数学，又保证标注与**真实数字**（M2 207/207、M5 可判 0、M3 13 可判）逐值勾稽，
且不需要跑 11 分钟的门禁扫描。

口径纪律（565b 监工确认）：
  * 拦截率/处置率/逃逸率一律**双侧** `cp_interval`（经 `proportion()`）；
  * 可判分母 = variants − n_a − malformed（**n_a/malformed 永不进分母**）；
  * 全分母率**正名** `treated_all`，不得叫 strict；
  * 可判样本 n=0 ⇒ `insufficient evidence`，**不算率、不填 0**。
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import mutation_fuzz as mf

BASELINE = mf.ROOT / "data" / "mutation" / "full_baseline_v1.json"


def _rows_from_baseline() -> list[dict]:
    """从已提交基线派生 (op, verdict, kind) 行——报告层只吃这三个字段。"""
    if not BASELINE.is_file():
        pytest.skip("full_baseline_v1.json 不在（基线未随仓保留）")
    d = json.loads(BASELINE.read_text(encoding="utf-8"))
    out = []
    for r in d["results"]:
        out.append({"op": r["op"], "verdict": r["verdict"], "kind": r.get("kind"),
                    "card": r.get("card", "")})
    return out


def test_baseline_denominator_and_rates():
    """可判分母 956；严格 615/956=64.33%；含 warn 729/956=76.26%；treated_all=729/1188。"""
    rows = _rows_from_baseline()
    variants = len(rows)
    blocked = sum(1 for r in rows if r["verdict"] == "blocked")
    escaped = sum(1 for r in rows if r["verdict"] == "escaped")
    n_a = sum(1 for r in rows if r["verdict"] == "n_a")
    strict = sum(1 for r in rows if r["verdict"] == "blocked" and r.get("kind") == "strict")
    judged = blocked + escaped
    assert (variants, blocked, escaped, n_a, strict) == (1188, 729, 227, 232, 615)
    assert judged == 956, "可判分母必须是 1188-232-0"
    assert abs(mf._rate_block(strict, judged)["point"] - 0.6433) < 1e-4
    assert abs(mf._rate_block(blocked, judged)["point"] - 0.7626) < 1e-4
    all_d = mf._rate_block(blocked, variants)
    # 报告块对浮点做 6 位取整（便于人读与逐字对账），断言按取整后的精度
    assert abs(all_d["point"] - 729 / 1188) < 1e-6, "全分母率口径 = treated_all"


def test_operator_blocks_match_baseline():
    """分算子口径块与基线 by_operator 逐值勾稽（可判 = blocked + escaped）。"""
    rows = _rows_from_baseline()
    op_rates, _flags = mf._op_rates(rows)
    d = json.loads(BASELINE.read_text(encoding="utf-8"))
    for op, v in d["by_operator"].items():
        blk = op_rates[op]
        assert blk["judged"] == v["blocked"] + v["escaped"], op
        assert blk["n_a"] == v["n_a"], op
        assert blk["treated"]["numerator"] == v["blocked"], op
        assert blk["escape"]["numerator"] == v["escaped"], op
    assert op_rates["M2"]["judged"] == 207 and op_rates["M5"]["judged"] == 0


def test_flags_m2_m5_m3():
    """三处必须显形：M2 活雷（区间 [98.24%,100%]）· M5 不可判 · M3 样本不足（n≥59）。"""
    _op_rates, flags = mf._op_rates(_rows_from_baseline())
    m2 = next(f for f in flags if f.startswith("M2"))
    assert "活雷" in m2 and "207/207" in m2
    # 真值 = 0.025**(1/207) = 0.9823372 ⇒ 显示 98.23%（提示词写 98.24% 是另一种取整，
    # 逐值以 `cp_interval` 为准；这里同时锁数值与显示串，避免"照抄提示词数字"）
    assert "[98.23%, 100.00%]" in m2, m2
    m5 = next(f for f in flags if f.startswith("M5"))
    assert "insufficient evidence" in m5 and "n=0" in m5
    m3 = next(f for f in flags if f.startswith("M3"))
    assert "样本不足" in m3 and "n≥59" in m3
    # 样本够且非全逃逸的算子不该被标注（防"逢算子必报"的噪声）
    for noisy in ("M1", "M4", "M6", "M7"):
        assert not any(f.startswith(noisy) for f in flags), noisy


def test_m2_escape_interval_is_two_sided():
    """M2 的逃逸区间必须是**双侧** C-P（98.24%~100%），不是单侧上界。"""
    import stat_bounds as sb
    lo, hi = sb.cp_interval(207, 207)
    assert abs(lo - 0.9823372) < 1e-6 and hi == 1.0, (lo, hi)   # 0.025**(1/207)
    blk = mf._rate_block(207, 207)
    assert abs(blk["cp_low"] - lo) < 1e-6 and blk["cp_high"] == hi   # 报告块 6 位取整
    # 单侧上界是另一个数（用于"零失效"陈述），别混用
    assert sb.cp_upper_one_sided(0, 207) < 0.02


def test_rate_block_zero_denominator_never_fills_zero():
    """n=0：点估计必须为 None + 带 note —— **不许填 0**（0 与"不可判"含义相反）。"""
    blk = mf._rate_block(0, 0)
    assert blk["denominator"] == 0 and blk["point"] is None
    assert "insufficient evidence" in blk["note"]
    line = mf._rate_line("M5 逃逸率", blk)
    assert "insufficient evidence" in line and "0.00%" not in line


def test_run_fuzz_report_has_rate_blocks():
    """真实一轮（单卡 M5，不跑 replay）必须带 rates/by_operator_rates/rate_flags 三块。"""
    card = mf.ROOT / "evidence" / "conc" / "EV-CONC-001.md"
    rep = mf.run_fuzz([card], ["M5"], 1)
    assert {"rates", "by_operator_rates", "rate_flags"} <= set(rep)
    assert rep["rates"]["judged"] == rep["blocked"] + rep["escaped"]
    assert abs(rep["rates"]["treated_all"]["point"] - 0) < 1e-12     # M5 在这卡上恒 n_a
    assert "1.0" not in str(rep["rates"]["treated_all"]["point"])
    # 既有字段逐字保留（548 对账锁与 T2 快照都依赖它们）
    assert {"variants", "blocked", "escaped", "n_a", "strict_blocked",
            "strict_rate", "treated_rate", "by_operator"} <= set(rep)
