"""625 B2 · 雷2 稳定指标回归测试（≥4 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import loop_stability_metrics_625 as m  # noqa: E402


def test_metrics_reads_7_rounds():
    d = m.metrics()
    assert len(d["rows"]) == 7
    assert 0 < d["cum_touched"] <= 67
    assert d["blind"] == 67 - d["cum_touched"]


def test_trigger1_has_five_checks():
    t = m.trigger1(m.metrics())
    assert set(t["checks"]) == {"连续≥3轮", "最近一轮增长率<10%", "VFDR收敛率<1%",
                                "判决一致性>95%", "覆盖稳定性波动<5%"}
    assert t["total"] == 5


def test_latest_growth_below_10pct_and_consistency():
    d = m.metrics()
    assert d["rows"][-1]["growth"] < 0.10
    assert d["consistency"] > 0.95


def test_trigger1_partial_satisfied():
    t = m.trigger1(m.metrics())
    # 诚实结论：4/5 满足（覆盖稳定性波动 >5%）
    assert t["satisfied"] is False
    assert t["satisfied_count"] == 4
    assert t["checks"]["覆盖稳定性波动<5%"] is False


def test_report_exists():
    p = os.path.join(ROOT, "data", "loop_stability_report_625.md")
    assert os.path.exists(p) and os.path.getsize(p) > 300
    assert "触发标准①" in open(p, encoding="utf-8").read()


def test_selftest_passes():
    assert m.selftest() == 0
