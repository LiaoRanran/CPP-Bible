"""628 D1 · 学习者镜像门监控 单测（9 例）。

覆盖任务书 4 项必测：采集器运行且不改源文件 / 门状态计算 / append-only / 阈值可配置。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import learner_behavior_collector_628 as C
import learner_twin_gate_monitor_628 as M


def _snapshot_learning_files() -> dict:
    snap = {}
    for d in C.LEARNING_DIRS:
        base = os.path.join(C.ROOT, d)
        for dirpath, _dirs, files in os.walk(base):
            for fn in files:
                p = os.path.join(dirpath, fn)
                st = os.stat(p)
                snap[os.path.relpath(p, C.ROOT)] = (st.st_size, round(st.st_mtime, 3))
    return snap


def test_collector_runs_and_does_not_modify_sources():
    before = _snapshot_learning_files()
    r = C.collect()
    after = _snapshot_learning_files()
    assert r["candidates"] >= 0
    assert before == after, "采集器修改了学习内容源文件"


def test_events_file_append_only():
    line_count = len(open(C.EVENTS, encoding="utf-8").read().splitlines())
    first = open(C.EVENTS, encoding="utf-8").readline()
    assert C.collect()["added"] == 0                    # 重跑幂等
    assert len(open(C.EVENTS, encoding="utf-8").read().splitlines()) == line_count
    assert open(C.EVENTS, encoding="utf-8").readline() == first


def test_event_schema_complete():
    events = C.load_events()
    assert events
    keys = {"event_id", "kind", "source", "ref", "agent_assisted", "detail", "observed_at"}
    assert all(keys <= set(e) for e in events)
    assert len({e["event_id"] for e in events}) == len(events)   # id 唯一
    assert {e["kind"] for e in events} >= {"git_commit", "batch_record", "file_mtime"}


def test_gate_state_thresholds():
    assert M.gate_state(0) == "closed"
    assert M.gate_state(39) == "closed"
    assert M.gate_state(40) == "opening"
    assert M.gate_state(49) == "opening"
    assert M.gate_state(50) == "open"
    assert M.gate_state(99) == "open"


def test_threshold_is_configurable():
    assert M.gate_state(60, threshold=100) == "closed"
    assert M.gate_state(80, threshold=100) == "opening"
    assert M.gate_state(100, threshold=100) == "open"
    assert M.build(threshold=100)["threshold"] == 100


def test_classify_three_states():
    assert C.classify("628 D1：学习者镜像门监控") is True
    assert C.classify("feat(atoms): 新增卡片") is True
    assert C.classify("G5 MEM 批量生产 原子8") is True
    assert C.classify("学习笔记：模板偏特化整理") is False
    assert C.classify("无任何标识的普通句子") is None


def test_current_state_is_closed_and_zero():
    d = M.build()
    assert d["threshold"] == 50
    assert d["state"] == "closed"
    assert d["real_learning_events"] == 0          # 尚无用户亲手学习事件
    assert d["real_learning_events"] <= d["candidates_total"]
    assert 0.0 <= d["progress"] < 1.0


def test_report_written_with_gate_state():
    p = M.write_report()
    body = open(p, encoding="utf-8").read()
    assert os.path.exists(p)
    for kw in ("门状态", "采集来源", "开门建议", "closed"):
        assert kw in body


def test_selftest_exit_zero():
    assert C.selftest() == 0
    assert M.selftest() == 0
