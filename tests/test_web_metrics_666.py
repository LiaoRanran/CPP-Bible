# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""666 B2 · 首页指标工具（`tools/web_metrics_666.py`）回归锁。

锁四件事：① 现算字段与事实源一致；② 落盘文件与现算一致（漂移可见）；
③ 拿不到的项必须显式登记（不许占位冒充）；④ 时间线/提交列表结构可用。
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import counts_659 as counts  # noqa: E402
import gate_engine as ge  # noqa: E402
import web_metrics_666 as W  # noqa: E402


def test_selftest_passes():
    assert W.selftest() == 0


def test_cards_and_rules_match_fact_sources():
    m = W.collect()["metrics"]
    assert m["cards_real"] == counts.ATOMS_REAL
    assert m["cards_draft"] == counts.ATOMS_DRAFT
    assert m["rules_total"] == len(ge.RULES)


def test_holdout_rate_is_dual_opt_caliber():
    """检出率必须带**双档口径**说明（否则会被当"能力提升"误读）。"""
    h = W.collect()["metrics"]["holdout"]
    assert h and isinstance(h["rate_pct"], float)
    assert "双档" in h["caliber"] and "-O0" in h["caliber"] and "-O2" in h["caliber"]
    assert h["catch"] + h["miss"] + h["unknown"] > 0


def test_ledger_count_read_only_and_matches_file():
    m = W.collect()["metrics"]
    n = sum(1 for ln in open(os.path.join(ROOT, m["ledger_path"]), encoding="utf-8") if ln.strip())
    assert m["ledger_events"] == n, "账本只读计数必须与文件行数一致（452 红线所在文件）"


def test_timeline_and_commits_shape():
    d = W.collect()
    assert len(d["timeline"]) >= 5
    for m in d["timeline"]:
        assert set(m) >= {"batch", "date", "state", "what", "why"}
    assert isinstance(d["commits"], list)


def test_unavailable_registered_not_hidden():
    d = W.collect()
    assert isinstance(d["unavailable"], list)
    # 缺失项必须显式登记：拿不到就 null + unavailable，而不是塞占位值
    for k in ("ledger_events", "transparency_log_entries"):
        if d["metrics"].get(k) is None:
            assert d["unavailable"], f"{k} 为 None 却没有任何 unavailable 登记"


def test_write_then_check_is_consistent(tmp_path, monkeypatch):
    """`--write` 落盘后 `--check` 必须一致（幂等：同一天重复跑不漂移）。"""
    out = tmp_path / "metrics_666.json"
    monkeypatch.setattr(W, "OUT", str(out))
    assert W.main(["--write"]) == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["schema"] == "queyi-web-metrics/666"
    assert data["metrics"]["cards_real"] > 0
    assert W.main(["--check"]) == 0
