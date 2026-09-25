"""640c A1 · 派生量单一权威源（`tools/w2_derived_640c.py`）回归测试。

锁三件事：
1. **两路交叉校验**：现算（事实源 → 610 B1 引擎）与读产物（`grounded_labels_w2.json`）
   在真实库上一致（不一致 ⇒ `mismatch` 列为漂移告警）；
2. **产物读数语义**（夹具：已知产物 ⇒ 已知派生量；含数字档 `credibility` 兼容）；
3. `--check` 自检 exit 0。
"""
from __future__ import annotations

import json
from pathlib import Path

import w2_derived_640c as wd


def test_two_paths_consistent_on_real_repo():
    d = wd.derived()
    assert d["consistent"], f"现算与入库产物不一致（漂移告警）：{d['mismatch']}"
    assert d["mismatch"] == []


def test_live_and_pinned_agree_on_key_derived_quantities():
    lv, pn = wd.live(), wd.pinned()
    assert lv["credibility_distribution"] == pn["credibility_distribution"]
    assert lv["out_mis"] == pn["out_mis"]
    assert (lv["in"], lv["out"], lv["undec"], lv["nodes"]) \
        == (pn["in"], pn["out"], pn["undec"], pn["nodes"])


def test_distribution_sums_to_node_count():
    lv = wd.live()
    assert sum(lv["credibility_distribution"].values()) == lv["nodes"]
    assert lv["in"] + lv["out"] + lv["undec"] == lv["nodes"]


def test_pinned_artifact_known_input(tmp_path: Path):
    """夹具（真验证力）：人造产物 ⇒ 已知派生量（含"数字档"回退路径）。"""
    doc = {"nodes": {
        "ATOM-X-001::prop-1": {"label": "IN", "type": "proposition", "confidence": "high"},
        "ATOM-Y-001::prop-1": {"label": "IN", "type": "proposition"},          # 缺 confidence
        "MIS-X-001": {"label": "OUT", "type": "misconception", "confidence": "medium"},
        "MIS-Y-001": {"label": "OUT", "type": "misconception", "credibility": 3},
        "MIS-Z-001": {"label": "UNDEC", "type": "misconception", "confidence": "low"},
    }, "edges": 7, "defeating_edges": 3, "rounds": 2}
    p = tmp_path / "w2.json"
    p.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    s = wd.pinned(p)
    assert s["nodes"] == 5 and s["in"] == 2 and s["out"] == 2 and s["undec"] == 1
    assert s["edges"] == 7 and s["defeating_edges"] == 3
    # `confidence` 优先；缺失时回退数字档 `credibility`（3 ⇒ high）
    assert s["credibility_distribution"] == {"high": 2, "medium": 1, "low": 1}
    assert s["out_mis"] == 2, "OUT MIS 只数 misconception（不混计数）"


def test_pinned_missing_file_fails_loud(tmp_path: Path):
    import pytest

    with pytest.raises(FileNotFoundError):
        wd.pinned(tmp_path / "nope.json")


def test_cli_check_passes(capsys):
    assert wd.main(["--check"]) == 0
    assert "PASS" in capsys.readouterr().out
