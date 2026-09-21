#!/usr/bin/env python3
"""615 A1 回归测试：human_review_honesty_615（人审诚实化标签）。"""
import hashlib
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
    cur = hashlib.sha256(a1.ANNOTATIONS.read_bytes()).hexdigest()
    assert cur == a1.ANNOTATIONS_SHA256
