#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""615 B1 回归测试：ev_matrix_unbacked_v2（独立第二实现）。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ev_matrix_unbacked_v2 as v2  # noqa: E402

_IMPORT_RE = re.compile(r"^\s*(?:import|from)\s+gate_engine\b")


def test_no_gate_engine_import() -> None:
    src = (ROOT / "tools" / "ev_matrix_unbacked_v2.py").read_text(encoding="utf-8")
    # 只看真正的 import 语句（注释/文档串里的说明不算）
    assert not any(_IMPORT_RE.match(ln) for ln in src.splitlines())
    # 独立运行不崩
    c = v2.compare()
    assert c["n_crash"] == 0


def test_all_evidence_cards_get_verdict_or_skip() -> None:
    c = v2.compare()
    assert c["raw_cards"] >= 56            # 全证据卡被扫（历史下限；卡数只增不减）
    # 去写死（669 P0）：applicable 原写死 == 19，但新增带 matrix 的证据卡会使适用卡数
    # 随语料增长（669 新增 5 张 → 24）。改为现算一致式：compare() 现算的 applicable
    # 必须等于“独立重算的适用卡数”，且 natural/official 覆盖同一批卡。
    expected_applicable = sum(
        1 for _rel, text in v2._cards() if v2.judge(text) is not None)
    assert c["applicable"] == expected_applicable
    assert len(c["natural"]) == len(c["official"]) == c["applicable"]


def test_agreement_in_reasonable_range() -> None:
    c = v2.compare()
    rate = c["agree"] / c["applicable"]
    assert 0.50 <= rate <= 1.0
    # 去写死：rate 原写死 == 13/19（68.4%，615 历史快照）。随语料增长 rate 浮动，
    # 此处只锁“一致式不变式 + 区间”，不再锁精确历史值（历史：615 时 68.4%/6 分歧卡）。
    assert c["agree"] + len(c["diverge"]) == c["applicable"]
    # 回归锁保留：分歧卡集合必须等于历史登记集；任何新分歧须人工复核并写入
    # HISTORICAL_DIVERGENT，不许静默放过。
    assert {r["card"] for r in c["diverge"]} == v2.HISTORICAL_DIVERGENT
