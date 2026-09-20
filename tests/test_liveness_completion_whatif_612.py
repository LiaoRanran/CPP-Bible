#!/usr/bin/env python3
"""B3 回归测试：活性锚补全 what-if（只读复用 gate_engine 判定）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from pathlib import Path as _P  # noqa: E402

import liveness_completion_whatif as b3  # noqa: E402

ROOT = _P(__file__).resolve().parents[1]


def test_pid_from():
    assert b3._pid_from("命题 prop-3（observation）缺活性对照") == "prop-3"
    assert b3._pid_from("命题 ATOM-X::prop-1 的锚缺失") == "ATOM-X::prop-1"


def test_load_review_anchors_empty():
    # 真实仓的 B2 日志当前为空 ⇒ 返回 {}
    assert b3.load_review_anchors() == {}


def test_project_invariants():
    d = b3.project()
    # 与 memory/门禁实测一致：baseline 50 warn；全部可锚（引用卡均有合法非通用符号）
    assert d["baseline_warn"] == 50, d["baseline_warn"]
    assert d["anchorable"] == 50, d["anchorable"]
    assert d["must_reclassify"] == 0
    assert d["deferred"] == 0
    # 自洽：可锚+须改标+deferred == 总数；full_anchor 残留 == 须改标
    assert d["anchorable"] + d["must_reclassify"] + d["deferred"] == d["total_obs"]
    assert d["full_anchor_warn_after"] == d["must_reclassify"]
    assert d["full_anchor_warn_after"] == 0


def test_full_anchor_eliminates_all():
    d = b3.project()
    # 每条 observation 命题在 full_anchor 情景下都应判 "ok"（无残留 warn）
    non_ok = [r for r in d["rows"] if r["full"] != "ok"]
    assert non_ok == [], [(r["card"], r["prop_id"], r["full"]) for r in non_ok]


def test_baseline_rows_all_branch1():
    d = b3.project()
    # 当前无任何 liveness ⇒ baseline 全为 branch1（缺命题级锚）
    base = [r for r in d["rows"] if r["base"] != "branch1"]
    assert base == [], [(r["card"], r["prop_id"], r["base"]) for r in base]


def test_main_check_passes():
    assert b3.main(["--check"]) == 0
