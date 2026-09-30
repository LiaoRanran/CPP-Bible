# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tests/test_drift_watch_670c.py — 670c D3 漂移监控的回归测试（>=5 断言）。

重点覆盖四件事：基线对比、**阈值边界（正好 10%）**、缺基线容错、有实验记录不标红。
所有用例在 tmp_path 里构造最小仓库，绝不触碰真实仓库。
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import drift_watch_670c as Drift  # noqa: E402

# ─────────────────────────────────────────────────────────────────────────────
# helper：最小仓库（六个关键数字的真实来源文件）
# ─────────────────────────────────────────────────────────────────────────────

def wj(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False) + "\n", encoding="utf-8")


def mk_root(tmp: Path, *, catch: int = 14, miss: int = 2, corpus: tuple = (14, 32),
            ledger: int = 452, mut: tuple = (110, 3), rules: int = 67) -> Path:
    wj(tmp / "data" / "holdout_reveal_3_665.json", {"error_subset": {"catch": catch, "miss": miss}})
    wj(tmp / "data" / "external_corpus_reveal_665.json", {"catch": corpus[0], "miss": corpus[1] - corpus[0]})
    wj(tmp / "data" / "656_mutation_report_core.json", {"killed": mut[0], "survived": mut[1]})
    wj(tmp / "data" / "_gate_rules.json", [{"rule": f"R{i}"} for i in range(rules)])
    (tmp / "data" / "authority").mkdir(parents=True, exist_ok=True)
    (tmp / "data" / "authority" / "decision_event_v2_ledger.jsonl").write_text(
        "".join(f'{{"i": {i}}}\n' for i in range(ledger)), encoding="utf-8")
    (tmp / "atoms" / "conc").mkdir(parents=True, exist_ok=True)
    (tmp / "atoms" / "conc" / "ATOM-A.md").write_text("---\nid: A\n---\n", encoding="utf-8")
    (tmp / "evidence" / "conc").mkdir(parents=True, exist_ok=True)
    (tmp / "evidence" / "conc" / "EV-A.md").write_text("---\nid: E\n---\n", encoding="utf-8")
    return tmp


def out_of(tmp: Path) -> Path:
    return tmp / "data" / "drift_report_670c.json"


def touch_future(p: Path, delta: float = 10.0) -> None:
    """把 mtime 设到未来（保证「比基线更新」），避免同秒跑导致的判定抖动。"""
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('{"experiment": "x"}\n', encoding="utf-8")
    t = time.time() + delta
    os.utime(p, (t, t))


# ─────────────────────────────────────────────────────────────────────────────
# ① 采集：六个数字必须来自真实来源文件
# ─────────────────────────────────────────────────────────────────────────────

def test_collect_metrics_from_real_sources(tmp_path):
    root = mk_root(tmp_path)
    vals = {m["key"]: m for m in Drift.collect_metrics(root)}
    assert vals["holdout_rate_pct"]["value"] == 87.5, "holdout 检出率应由 catch/(catch+miss) 现算"
    assert vals["corpus_rate_pct"]["value"] == 43.75
    assert vals["ledger_events"]["value"] == 452, "账本数应为 452 账本的非空行数"
    assert vals["mutation_core_pct"]["value"] == round(110 / 113 * 100, 4)
    assert vals["cards_total"]["value"] == 2, "卡数 = 原子卡 + 证据卡"
    assert vals["rules_total"]["value"] == 67
    assert all(m["source"] for m in vals.values()), "每个指标都必须写明来源文件"


# ─────────────────────────────────────────────────────────────────────────────
# ② 阈值边界：正好 10% 不算漂移，超过才算
# ─────────────────────────────────────────────────────────────────────────────

def test_threshold_boundary_exactly_ten_percent():
    assert Drift.pct_change(100, 110) == 0.1, "相对变化应为 0.1"
    assert Drift.is_drift(Drift.pct_change(100, 110), 0.10) is False, \
        "正好 10% 不该判漂移（判据是「超过」阈值）"
    assert Drift.is_drift(Drift.pct_change(100, 110.01), 0.10) is True, "10.01% 必须判漂移"
    assert Drift.is_drift(Drift.pct_change(100, 90), 0.10) is False, "正好 -10% 同理不算"
    assert Drift.is_drift(Drift.pct_change(100, 89.99), 0.10) is True
    assert Drift.is_drift(Drift.pct_change(None, 5), 0.10) is False, "缺一侧 ⇒ 不可比，不判漂移"
    assert Drift.is_drift(Drift.pct_change(0, 5), 0.10) is True, "基线 0 而现值非 0 ⇒ 从无到有，判漂移"


def test_full_cycle_at_exact_threshold_is_not_flagged(tmp_path):
    root = mk_root(tmp_path, catch=10, miss=0)          # 100%
    out = out_of(root)
    r1 = Drift.evaluate(root, out, 0.10, write=True)
    assert r1["overall"] == Drift.FIRST_RUN
    (root / "data" / "holdout_reveal_3_665.json").write_text(
        json.dumps({"error_subset": {"catch": 11, "miss": 0}}), encoding="utf-8")   # 110% ⇒ +10%
    r2 = Drift.evaluate(root, out, 0.10, write=True)
    assert r2["overall"] == Drift.PASS, "正好 +10% 不该标红"
    assert r2["drifted_unjustified"] == []
    assert r2["ok"], "未越阈值的指标应进入 ok 列表"


# ─────────────────────────────────────────────────────────────────────────────
# ③ 基线对比：越阈值且无实验记录 ⇒ 标红
# ─────────────────────────────────────────────────────────────────────────────

def test_drift_without_experiment_is_red(tmp_path, capsys):
    root = mk_root(tmp_path)
    out = out_of(root)
    capsys.readouterr()
    assert Drift.main(["--root", str(root), "--out", str(out)]) == 0, "首次只标定基线"
    capsys.readouterr()
    # 检出率 87.5% → 66.7%（-23.8%），且 data/experiments/ 下没有任何实验记录
    (root / "data" / "holdout_reveal_3_665.json").write_text(
        json.dumps({"error_subset": {"catch": 2, "miss": 1}}), encoding="utf-8")
    rc = Drift.main(["--root", str(root), "--out", str(out), "--json"])
    rep = json.loads(capsys.readouterr().out)
    assert rc == 1, "发现无人认领漂移时退出码必须非 0"
    assert rep["overall"] == Drift.DRIFT, "越阈值且无实验记录却未标红 ⇒ 无射程"
    assert len(rep["drifted_unjustified"]) == 1
    d0 = rep["drifted_unjustified"][0]
    assert d0["key"] == "holdout_rate_pct"
    assert d0["baseline"] == 87.5 and round(d0["current"], 4) == 66.6667


def test_fresh_experiment_record_justifies_drift(tmp_path):
    root = mk_root(tmp_path)
    out = out_of(root)
    Drift.evaluate(root, out, Drift.DEFAULT_THRESHOLD, write=True)
    (root / "data" / "holdout_reveal_3_665.json").write_text(
        json.dumps({"error_subset": {"catch": 2, "miss": 1}}), encoding="utf-8")
    touch_future(root / "data" / "experiments" / "669_experiments.json")
    rep = Drift.evaluate(root, out, Drift.DEFAULT_THRESHOLD, write=True)
    assert rep["overall"] == Drift.PASS, "有更新的实验记录时不该标红（变化有据可查）"
    assert rep["drifted_unjustified"] == []
    assert len(rep["drifted_justified"]) == 1, "越阈值但被实验记录认领的指标要单独列出（不静默）"
    assert rep["drifted_justified"][0]["evidence"], "justified 必须带上证据文件名"


# ─────────────────────────────────────────────────────────────────────────────
# ④ 缺基线 / 损坏基线容错 + 报告结构
# ─────────────────────────────────────────────────────────────────────────────

def test_missing_baseline_is_first_run(tmp_path):
    root = mk_root(tmp_path)
    rep = Drift.evaluate(root, out_of(root), Drift.DEFAULT_THRESHOLD, write=True)
    assert rep["overall"] == Drift.FIRST_RUN and rep["baseline_found"] is False
    assert rep["baseline"] == {} and rep["drifted_unjustified"] == []
    assert out_of(root).is_file(), "首次运行应把基线落盘"


def test_corrupt_baseline_is_tolerated(tmp_path):
    root = mk_root(tmp_path)
    out_of(root).parent.mkdir(parents=True, exist_ok=True)
    out_of(root).write_text("{ 这不是 JSON", encoding="utf-8")
    rep = Drift.evaluate(root, out_of(root), Drift.DEFAULT_THRESHOLD, write=True)
    assert rep["overall"] == Drift.FIRST_RUN, "基线损坏 ⇒ 退化为重新标定，不崩也不误红"
    assert json.loads(out_of(root).read_text(encoding="utf-8"))["schema"] == Drift.SCHEMA


def test_report_structure_and_threshold_flag(tmp_path, capsys):
    root = mk_root(tmp_path)
    out = out_of(root)
    capsys.readouterr()
    assert Drift.main(["--root", str(root), "--out", str(out), "--threshold", "5", "--json"]) == 0
    rep = json.loads(capsys.readouterr().out)
    for k in ("schema", "tool", "generated_at", "generated_at_epoch", "threshold",
              "threshold_pct", "overall", "values", "baseline", "metrics", "ok",
              "drifted_unjustified", "drifted_justified", "experiments", "notes",
              "baseline_values_for_next_run"):
        assert k in rep, f"报告缺字段 {k}"
    assert rep["threshold"] == 0.05, "--threshold 5 应解释为 5%（>1 视为百分数）"
    assert rep["threshold_pct"] == 5.0
    assert len(rep["metrics"]) == 6 and len(rep["values"]) == 6
    assert json.loads(out.read_text(encoding="utf-8"))["schema"] == Drift.SCHEMA
