# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""628 A4 · DEBT-001 + replay manifest 修复 单测（5 例）。"""
import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import pytest  # noqa: E402  672h：slow 标记
import replay_manifest_fix_628 as R


def _manifest_entries() -> int:
    """`build/replay_manifest.json` 的条目数（缺失/坏 ⇒ 0）。674a。"""
    import json
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "build", "replay_manifest.json")
    if not os.path.exists(p):
        return 0
    try:
        d = json.load(open(p, encoding="utf-8"))
    except ValueError:
        return 0
    return len(d) if isinstance(d, dict) else 0


def test_debt_001_fixture_dynamized():
    # fixture 日期动态化：clean 场景 due 在未来
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = open(os.path.join(here, "tests", "test_s1_s6.py"), encoding="utf-8").read()
    assert "today + timedelta(days=30)" in src or "timedelta(days=30)" in src
    assert '"due": "2026-09-20"' not in src
    assert (date.today() + timedelta(days=30)) > date.today()


@pytest.mark.slow
def test_clean_ledger_test_passes():
    import subprocess
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proc = subprocess.run(
        [sys.executable, "-m", "pytest",
         os.path.join(here, "tests", "test_s1_s6.py"), "-q"],
        capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stdout[-400:]


def test_manifest_consistency_zero_mismatch():
    c = R.check()
    assert c["consistent"]
    assert c["stale_count"] == 0 and c["missing_count"] == 0


@pytest.mark.skipif(
    _manifest_entries() == 0,
    reason="674a：`build/replay_manifest.json` 是**构建产物**（gitignore），干净检出/CI 里没有"
           "任何卡被 replay 过 ⇒ 清单为空。本用例的不变量要求**非空**清单（`0 < len(m) ≤ 卡数`），"
           "只能由 `atom_evidence_replay.py --rebuild-manifest` 产出（需真编译，属交人项）。"
           "注：同一文件的 `test_manifest_consistency_zero_mismatch` 对空清单仍成立，CI 里照跑。",
)
def test_manifest_covers_evidence_subset_and_is_consistent():
    """670a 去写死：`build/replay_manifest.json` 是**构建产物**（gitignore；按"已 replay 过的卡"
    增量累积），新卡未跑 replay 前条目数 **< 证据卡数** ⇒ 既不能写死 56、也不能与
    `counts.EVIDENCE_TOTAL` 划等号（那是卡口径）。

    改锁三条真不变量：① 无幽灵条目（每个 key 都必须是真实证据卡）；
    ② 指纹/文件一致性 0 失配；③ 条目数 ≤ 证据卡数。
    （"条目齐全"须跑 `atom_evidence_replay.py --rebuild-manifest`，属交人项。）
    """
    import json

    import counts_659 as counts
    import gate_engine as ge
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    m = json.load(open(os.path.join(here, "build", "replay_manifest.json"), encoding="utf-8"))
    cards = set()
    for p in ge.EVIDENCE.rglob("EV-*.md"):
        if "README" in p.name:
            continue
        cards.add(str(ge._meta(p).get("id") or p.stem))
    keys = {os.path.basename(k)[:-len(".md")] for k in m}
    assert keys <= cards, f"幽灵条目（清单里有、事实源没有）：{sorted(keys - cards)}"
    c = R.check()
    assert c["entries"] == len(m)
    assert c["stale_count"] == 0 and c["missing_count"] == 0
    assert 0 < len(m) <= counts.EVIDENCE_TOTAL


def test_disposition_report_exists():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(here, "data", "debt_001_disposition_628.md")
    assert os.path.exists(p)
    txt = open(p, encoding="utf-8").read()
    assert "DEBT-001" in txt and "closed" in txt.lower()
