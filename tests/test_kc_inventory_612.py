#!/usr/bin/env python3
"""D1 回归测试：KC 知识组件台账（只读）。"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from pathlib import Path as _P  # noqa: E402

import kc_inventory as d1  # noqa: E402

ROOT = _P(__file__).resolve().parents[1]


def test_total_kc():
    d = d1.build()
    assert d["total_kc"] == 27, d["total_kc"]


def test_difficulty_range():
    d = d1.build()
    assert all(1 <= k["difficulty"] <= 5 for k in d["kcs"])


def test_prerequisites_exist():
    d = d1.build()
    assert any(k["prerequisites"] for k in d["kcs"])


def test_propositions_extracted():
    d = d1.build()
    assert all(k["n_propositions"] >= 1 for k in d["kcs"])
    # 每个 KC 的 propositions 至少有 id 与 claim_type
    for k in d["kcs"]:
        for pr in k["propositions"]:
            assert "id" in pr and "claim_type" in pr


def test_mis_reverse_index():
    idx = d1.mis_reverse_index()
    # MIS-MEM-001（关联原子：ATOM-MEM-MOVE-002）应被索引到
    assert "ATOM-MEM-MOVE-002" in idx
    assert "misconception_MIS-MEM-001" in idx["ATOM-MEM-MOVE-002"]


def test_difficulty_level_bands():
    assert d1.difficulty_level(2, 0) == 1
    assert d1.difficulty_level(9, 0) == 5
    assert d1.difficulty_level(0, 8) == 5


def test_main_check_passes():
    assert d1.main(["--check"]) == 0


def test_json_roundtrip():
    d = d1.build()
    txt = json.dumps(d, ensure_ascii=False)
    back = json.loads(txt)
    assert back["total_kc"] == 27
