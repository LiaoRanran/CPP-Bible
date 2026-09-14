"""质量度量 L1 回归锁（508 任务6）。

提示词要求 2 个测试（采集不崩溃 / jsonl 可解析）；本文件再加 2 个把阈值告警与
"缺数据不编造" 这两条纪律钉住——它们是本工具唯一会误导使用者的地方。
测试一律用 `tmp` 落盘路径，绝不写真实 `data/metrics.jsonl`。
"""
from __future__ import annotations

from pathlib import Path

import metrics_collector as mc


def test_collect_does_not_crash_and_has_all_metrics(tmp_path: Path):
    """① 采集不崩溃且 27 个键齐全（缺失语义上是 None，而不是键不存在）。"""
    snap = mc.collect(with_heavy=False)
    assert set(snap["metrics"]) == set(mc.ALL_METRICS), "指标键集合必须与 ALL_METRICS 一致"
    assert len(mc.ALL_METRICS) == 27, "提示词写 25，逐条数列实为 27（Quality9+Assets7+Perf4+Cost3+Health4）"
    assert isinstance(snap["alerts"], list) and isinstance(snap["notes"], dict)
    assert snap["timestamp"]


def test_append_and_history_are_parseable(tmp_path: Path):
    """② 落盘的一行必须是可解析 JSON，且 history 能读回；坏行不拖垮历史。"""
    f = tmp_path / "metrics.jsonl"
    snap = mc.collect(with_heavy=False)
    mc.append(snap, f)
    mc.append(snap, f)
    with f.open("a", encoding="utf-8") as fh:
        fh.write("{ 这不是合法 JSON\n")     # 模拟半行/损坏行
    rows = mc.read_history(f)
    assert len(rows) == 2, "坏行必须被跳过而不是抛异常"
    assert rows[0]["metrics"].keys() == snap["metrics"].keys()


def test_thresholds_warn_only_on_real_violation():
    """③ 阈值：0 block / 0 refute 不告警；一旦越线必须报出且**不阻断**（返回列表）。"""
    assert mc.evaluate_alerts({"gate_block_count": 0, "replay_refute_count": 0,
                               "pytest_wall_seconds": 10,
                               "poison_coverage_pct": 90}) == []
    bad = mc.evaluate_alerts({"gate_block_count": 2, "replay_refute_count": 1,
                              "pytest_wall_seconds": 301, "poison_coverage_pct": 49})
    assert {a["metric"] for a in bad} == {"gate_block_count", "replay_refute_count",
                                         "pytest_wall_seconds", "poison_coverage_pct"}
    assert [a["level"] for a in bad].count("ERROR") == 2


def test_replay_counts_fall_back_to_manifest(tmp_path: Path):
    """⑤ 增量"全命中缓存"无汇总行时，计数取自 replay 清单（且能区分 refute/infra）。"""
    man = tmp_path / "man.json"
    man.write_text(__import__("json").dumps({
        "a": {"verdict": "confirm"}, "b": {"verdict": "confirm"},
        "c": {"verdict": "refute:run_mismatch"},
        "d": {"verdict": "infra_error:compile_timeout"}}), encoding="utf-8")
    assert mc.replay_counts_from_manifest(man) == {
        "confirm": 2, "refute": 1, "infra_error": 1, "_total": 4}
    assert mc.replay_counts_from_manifest(tmp_path / "nope.json") is None


def test_golden_state_metric_uses_assets_not_own_dict():
    """⑥ 回归锁：`golden_state_atoms_match` 必须拿**磁盘实算**的原子数去比（508 首版
    读了自己那份只含 HEALTH 键的 out ⇒ 恒 None，是"指标静默失效"的典型）。"""
    notes: dict = {}
    assets = mc.collect_assets(notes)
    h = mc.collect_health(notes, assets)
    if (mc.ROOT / "tools" / "golden_state.json").is_file():
        assert h["golden_state_atoms_match"] in (True, False), \
            "台账存在时必须给出布尔判定，不得是 None"
    # 不传 assets 时（调用方漏传）也应是明确的 None + note，而不是静默当 True
    assert mc.collect_health(notes)["golden_state_atoms_match"] is None


def test_missing_data_is_null_not_fabricated(tmp_path: Path, monkeypatch):
    """④ 无来源的指标必须是 None + note（铁律 #4：不编数据）——以 pytest 墙钟为样本。"""
    monkeypatch.setattr(mc, "ROOT", tmp_path)      # tmp 下无 data/pytest_last.txt
    snap = mc.collect(with_heavy=False, with_gate=False)
    assert snap["metrics"]["pytest_wall_seconds"] is None
    assert "pytest_wall_seconds" in snap["notes"]
    assert snap["notes"]["pytest_wall_seconds"] != ""
