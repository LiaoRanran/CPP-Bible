#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""615 A1 回归测试：human_review_honesty_615（人审诚实化标签）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import human_review_honesty_615 as a1  # noqa: E402


def test_label_lines_match_annotations() -> None:
    labels = a1.build()
    ann = a1.load_annotations()
    assert len(labels) == len(ann) == 388
    assert a1.LABELS.is_file()
    on_disk = [ln for ln in a1.LABELS.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(on_disk) == 388


def test_edge_id_one_to_one() -> None:
    labels = a1.build()
    ann = a1.load_annotations()
    assert [x["edge_id"] for x in labels] == [r.get("edge_id") for r in ann]
    assert len({x["edge_id"] for x in labels}) == len(labels)  # 无重复


def test_batch_authorization_stats() -> None:
    s = a1.summarize(a1.build())
    assert s["batch_authorization"] == 388
    assert s["item_by_item"] == 0
    assert s["mirror"] == 194
    # 分模板
    assert s["templates"].get("T1", 0) + s["templates"].get("T4", 0) == 194


def test_annotations_unmodified() -> None:
    # 674a：改用工具的 `annotations_sha256()`（CRLF→LF 归一）。
    # 原写法 `hashlib.sha256(a1.ANNOTATIONS.read_bytes())` 直接哈希**工作树原始字节**，
    # 而该文件在本机是混行（194 行 CRLF）、干净检出/CI 是 LF ⇒ 同一提交内容在两处 hash 不同，
    # 断言随检出环境翻转（本机绿 / CI 红）。**断言意图不变**（仍是"文件未被改过"），
    # 只是把"内容"口径从"字节含行尾"收敛为"归一后的内容"。
    cur = a1.annotations_sha256()
    assert cur == a1.ANNOTATIONS_SHA256
