#!/usr/bin/env python3
"""614 B4 回归测试：learner_argument_link（学习者-论证层联动）。"""
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import learner_argument_link as b4  # noqa: E402
import learner_behavior_logger as b1  # noqa: E402

KC = "ATOM-X"


def _mk_db(tmp_path: Path) -> Path:
    db = tmp_path / "props.db"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE props (prop_key TEXT, card TEXT, prop_id TEXT, claim_type TEXT, "
                 "statement TEXT, evidence TEXT, machine_verified INT, signoff_state TEXT)")
    rows = [
        (f"{KC}::prop-1", KC, "prop-1", "observation", "前提一", "EV", 1, "signed"),
        (f"{KC}::prop-2", KC, "prop-2", "observation", "前提二", "EV", 1, "signed"),
        (f"{KC}::prop-3", KC, "prop-3", "inference", "结论", "EV", 0, "unsigned"),
    ]
    conn.executemany("INSERT INTO props VALUES (?,?,?,?,?,?,?,?)", rows)
    conn.commit()
    conn.close()
    return db


def test_mastery_to_chain(tmp_path: Path) -> None:
    db = _mk_db(tmp_path)
    chain = b4.chains_for_kc(KC, db)
    assert [c["claim_type"] for c in chain] == ["observation", "observation", "inference"]
    assert all({"prop_key", "prop_id", "statement", "evidence"} <= set(c.keys()) for c in chain)


def test_understanding_record(tmp_path: Path) -> None:
    store = tmp_path / "u.jsonl"
    b4.record(store, "default", KC, f"{KC}::prop-1", True)
    b4.record(store, "default", KC, f"{KC}::prop-1", False)  # 后写覆盖（latest-wins）
    und = b4.understanding(store, "default", KC)
    assert und[f"{KC}::prop-1"] is False
    # append-only：两条记录都在
    assert len(b4.load_all(store)) == 2


def test_recommendation_impact(tmp_path: Path) -> None:
    db = _mk_db(tmp_path)
    store = tmp_path / "u.jsonl"
    lstore = tmp_path / "beh.jsonl"
    for _ in range(10):
        b1.record(lstore, "default", KC, "correct", "exercise", None, False)
    # 未标记理解 → 进入论证复盘推荐
    recs = b4.recommend_argument_review(lstore, store, "default", 0.5, db)
    assert KC in recs
    # 全部标记理解 → 移出
    for pid in ("prop-1", "prop-2", "prop-3"):
        b4.record(store, "default", KC, f"{KC}::{pid}", True)
    recs2 = b4.recommend_argument_review(lstore, store, "default", 0.5, db)
    assert KC not in recs2
