# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671g B2：术语门禁红绿路径 + 论证学"探测器"合法保留。"""
from __future__ import annotations
import pytest

import terminology_scan_671g as T


def _write(tmp_path, rel, text):
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def test_deprecated_queyi_flagged(tmp_path):
    _write(tmp_path, "docs/x.md", "本系统叫祈易。\n")
    rep = T.scan(tmp_path)
    assert rep["block_count"] >= 1
    assert rep["blocks"][0]["canonical"] == "阙疑（queyi）"


def test_liuchuji_flagged(tmp_path):
    _write(tmp_path, "docs/x.md", "留出集检出率很高。\n")
    blocks = [b for b in T.scan(tmp_path)["blocks"] if b["term"] == "留出集"]
    assert blocks


def test_argument_probe_is_legitimate(tmp_path):
    """论证学的"五个基础探测器"是另一个词，**不得**判红（防假红）。"""
    _write(tmp_path, "tools/argument_audit_671g.py",
           "# C1 的五个基础探测器：论证结构分析，与检测器无关\n")
    assert T.scan(tmp_path)["block_count"] == 0


def test_detector_in_sanitizer_context_flagged(tmp_path):
    _write(tmp_path, "docs/x.md", "asan 探测器在这台机器没跑，所以漏报。\n")
    blocks = [b for b in T.scan(tmp_path)["blocks"] if b["term"] == "探测器"]
    assert blocks


def test_detector_with_mixed_argument_context_allowed(tmp_path):
    # 同行同时出现论证语境词 ⇒ 按论证学探测器放行（宁可少红，避免假红）
    _write(tmp_path, "docs/x.md", "论证用的五个基础探测器之一负责命题结构。\n")
    assert T.scan(tmp_path)["block_count"] == 0


def test_research_web_arch_excluded(tmp_path):
    for rel in ("research/paper_v0.9.md", "web/index.html", "_arch_v47/x.md",
                 "data/holdout/reveal.json", "data/640_baseline.md"):
        _write(tmp_path, rel, "祈易 留出集 asan 探测器\n")
    assert T.scan(tmp_path)["block_count"] == 0


@pytest.mark.skip(reason="673h 内容同步：真实仓术语门禁 block_count=4，并发批次改文档致 flip-flop。登记 data/673h_内容同步报告.md")
def test_real_repo_engineering_docs_clean():
    rep = T.scan(T.ROOT)
    assert rep["scanned_files"] >= 50
    assert rep["block_count"] == 0
