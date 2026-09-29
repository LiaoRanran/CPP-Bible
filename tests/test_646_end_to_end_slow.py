# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""646 阶段 C2 · 端到端慢测（真实全链路，标 slow，串行跑）。

覆盖：规则→卡映射 → 三层编排（真实 gate 扫描 + 充分性 + 反例）→ 清债达标断言。
本测真跑全库 gate（~数秒），故标 `slow`（两阶段跑法里 slow 段串行执行）。
"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import counts_659 as counts  # noqa: E402  666 A2：去写死（卡域现算）
import perf_646 as perf  # noqa: E402
import rule_card_mapper_646 as a1  # noqa: E402
import three_layer_orchestrator_646 as c2  # noqa: E402


@pytest.mark.slow
def test_mapping_and_coupling_end_to_end():
    """真实端到端：映射完整 + 三层打通达标（清债 1）。"""
    perf.clear()
    c2.clear_caches()
    m = a1.build_mapping()
    # 666 A2：去写死。原写死 `card_count == 27`（646 时点语料 27 张）——630–652 扩库后
    # 工具口径（`evidence_base_644.list_atoms()`）随语料涨到 37，写死值让它假红。
    # 注意：这里的"卡域"就是**实卡域**（ATOMS_REAL），不是 draft650 的全量域。
    assert m["rule_count"] == 67 and m["card_count"] == counts.ATOMS_REAL
    res = c2.orchestrate(min_chains=5)
    assert res["chains_with_evidence"] >= 5
    assert res["attribution_rate"] >= 0.5
    assert res["met"] is True


@pytest.mark.slow
def test_sufficiency_and_ledger_end_to_end():
    """真实端到端：充分性 27/27 + 账本注释 452 条且原账本未改（清债 3/B3）。"""
    import authority_rule_annotator_646 as a5
    import evidence_sufficiency_646 as b3
    perf.clear()
    suff = b3.judge()
    # 666 A2：去写死（同上一处，口径 = 实卡域）。
    assert suff["cards_total"] == counts.ATOMS_REAL
    assert suff["sufficient"] == counts.ATOMS_REAL
    before = a5._ledger_sha256()
    ann = a5.annotate()
    assert ann["events"] == 452 and ann["rules_with_events"] == 67
    assert a5._ledger_sha256() == before
