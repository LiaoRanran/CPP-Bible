#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""616 B2 回归测试：ev_matrix_unbacked_v2 补全语义。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ev_matrix_unbacked_v2 as v2  # noqa: E402

_IMPORT_RE = re.compile(r"^\s*(?:import|from)\s+gate_engine\b")


def test_sha256_preprocessing_implemented() -> None:
    assert v2.strip_sha_lines("artifact_sha256: " + "a" * 64) == ""
    # 含 sha 行的文本在补全语义下不被误收为 run 锚
    text = "compiler: [gcc, clang]\nartifact_sha256: " + "0" * 64 + "\n"
    j_legacy = v2.judge(text, strip_sha=False)
    j_full = v2.judge(text, strip_sha=True)
    assert j_legacy is not None and j_full is not None
    assert j_legacy["anchors"] >= 1 and j_full["anchors"] == 0


def test_agreement_at_least_95() -> None:
    c = v2.compare_full()
    # 去写死（669 P0）：applicable 原写死 == 19。改为现算一致式：natural/official 必须
    # 覆盖同一批适用卡（若 compare() 漏算一张卡，此处即红）。
    assert len(c["natural"]) == len(c["official"]) == c["applicable"]
    assert c["agree"] / c["applicable"] >= 0.95
    assert c["agree"] == c["applicable"]          # 补全后 100%


def test_no_gate_engine_import() -> None:
    src = (ROOT / "tools" / "ev_matrix_unbacked_v2.py").read_text(encoding="utf-8")
    assert not any(_IMPORT_RE.match(ln) for ln in src.splitlines())


def test_check_passes() -> None:
    assert v2.check() == []
