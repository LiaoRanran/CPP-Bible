"""591 任务 1 · v7 基线冻结回归锁（认账 589 T2 的 M2 un-mask）。

v7 = 1593 变体 / blocked 1405 / escaped 1 / n_a 179 / equivalent 8 / 可判 1406。
M2 可判 141→168（589 T2 注释净化 un-mask 27 条真实 fixture 路径变异，非回归）。
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V7 = ROOT / "data" / "mutation" / "full_baseline_v7.json"
V6 = ROOT / "data" / "mutation" / "full_baseline_v6.json"


def _load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def test_v7_exists_and_frozen_at_commit():
    assert V7.is_file(), "缺 data/mutation/full_baseline_v7.json"
    d = _load(V7)
    assert d["frozen_at_commit"] == "d36d5c8"
    assert "M2 可判 141→168" in d["notes"]


def test_v7_top_level_numbers():
    d = _load(V7)
    assert d["variants"] == 1593
    assert d["blocked"] == 1405
    assert d["escaped"] == 1
    assert d["n_a"] == 179
    assert d["equivalent"] == 8
    assert d["blocked"] + d["escaped"] == 1406, "可判分母必须 = blocked + escaped"


def test_v7_m2_judged_is_168():
    d = _load(V7)
    r = [x for x in d["results"] if x["op"] == "M2"]
    blk = sum(1 for x in r if x["verdict"] == "blocked")
    esc = sum(1 for x in r if x["verdict"] == "escaped" and not x.get("equivalent"))
    na = sum(1 for x in r if x["verdict"] == "n_a")
    eq = sum(1 for x in r if x.get("equivalent"))
    assert (blk, esc, na, eq) == (168, 0, 27, 0), (blk, esc, na, eq)


def test_v6_kept_and_superseded():
    assert V6.is_file(), "v6 文件不得删除"
    d6 = _load(V6)
    assert d6["superseded_by"] == "full_baseline_v7.json"
    assert d6["frozen_at_commit"] == "55c01c8"


def test_only_escaped_is_frozen_m1_tce():
    d = _load(V7)
    esc = [x for x in d["results"] if x["verdict"] == "escaped" and not x.get("equivalent")]
    assert len(esc) == 1, f"唯一 escaped 应为 1，实得 {len(esc)}"
    e = esc[0]
    assert e["op"] == "M1"
    assert e["card"] == "evidence/conc/EV-CONC-001.md"
    assert "negative_controls" in e["point"]
