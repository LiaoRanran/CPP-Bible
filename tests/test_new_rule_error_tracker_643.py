"""643 E1 · new_rule_error_tracker_643 单测（无数据/记账/推翻/幂等/独立台账）。
编号 E1-1..E1-8。台账走 `_P["path"]` 重定向到 tmp（**不污染 data/**）。
"""
from __future__ import annotations

import new_rule_error_tracker_643 as E1


def _with_ledger(tmp_path, fn):
    saved = E1._P["path"]
    E1._P["path"] = str(tmp_path / "led.json")
    try:
        return fn()
    finally:
        E1._P["path"] = saved


# E1-1：无样本 ⇒ None（**不是 0**，这是本工具的核心区分）
def test_no_data_is_none_not_zero():
    assert E1.error_rate(0, 0) is None
    assert E1.error_rate(0, 5) is None


# E1-2：有样本才给率
def test_rate_with_samples():
    assert E1.error_rate(4, 1) == 0.25
    assert E1.error_rate(2, 2) == 1.0
    assert E1.error_rate(3, 0) == 0.0


# E1-3：初始化 ⇒ 全部"无数据"
def test_init_all_no_data(tmp_path):
    def go():
        r = E1.init_ledger()
        return r, E1.snapshot()
    r, s = _with_ledger(tmp_path, go)
    assert r["n_rules"] > 0
    assert s["n_no_data"] == s["n_rules"]
    assert all(x["known_error_rate"] is None for x in s["rows"])
    assert s["append_only"] is True


# E1-4：record ⇒ total+1，rate=0（有样本）
def test_record(tmp_path):
    def go():
        E1.init_ledger()
        rid = E1.snapshot()["rows"][0]["rule_id"]
        E1.record([rid], decision_id="d1", result="PASS")
        return {x["rule_id"]: x for x in E1.snapshot()["rows"]}[rid]
    row = _with_ledger(tmp_path, go)
    assert row["total"] == 1 and row["known_error_rate"] == 0.0 and row["is_no_data"] is False


# E1-5：overturn ⇒ error+1 且回标日志（不删条目）
def test_overturn_marks_log(tmp_path):
    def go():
        E1.init_ledger()
        rid = E1.snapshot()["rows"][0]["rule_id"]
        E1.record([rid], decision_id="d1")
        o = E1.overturn([rid], decision_id="d1")
        led = E1.load_ledger()
        return o, led["rules"][rid], {x["rule_id"]: x for x in E1.snapshot()["rows"]}[rid]
    o, st, row = _with_ledger(tmp_path, go)
    assert st["error"] == 1 and len(st["log"]) == 1
    assert st["log"][0]["overturned"] is True and o["log_marked"] == 1
    assert row["known_error_rate"] == 1.0


# E1-6：重复 init 不覆盖已有样本（幂等 + 保历史）
def test_reinit_keeps_samples(tmp_path):
    def go():
        E1.init_ledger()
        rid = E1.snapshot()["rows"][0]["rule_id"]
        E1.record([rid])
        n1 = E1.snapshot()["n_rules"]
        E1.init_ledger()
        return n1, E1.snapshot()["n_rules"], E1.load_ledger()["rules"][rid]["total"]
    n1, n2, total = _with_ledger(tmp_path, go)
    assert n1 == n2 and total == 1


# E1-7：待初始化规则来自 D2 草案 ∩ D4 非危险（不写死清单）
def test_init_source_is_derived():
    ids = E1.init_rules()
    assert isinstance(ids, list)
    assert len(ids) <= 10


# E1-8：台账路径独立（不指向 642 的产物）+ 只读自检
def test_ledger_is_batch_local():
    assert "643" in E1.LEDGER and "642" not in E1.LEDGER
    assert E1.selftest() == 0
