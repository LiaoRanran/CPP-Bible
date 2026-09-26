"""647 B2 · anti-windup 真上岗回归锁（编号 B2-1..B2-7）。"""
from __future__ import annotations

import hashlib
import json
import os

import anti_windup_642 as base
import anti_windup_647 as A
import protector_mode_647 as M

OVER = base.queue_state(n=51, weekly_new=21)
NORMAL = base.queue_state(n=1, weekly_new=1)


def test_b2_1_enforce_freezes_low_priority(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    r = A.admit("低", OVER)
    assert r["frozen"] is True and r["enqueued"] is False and r["frozen_enforced"] is True
    assert A.admit("高", OVER)["enqueued"] is True
    assert A.admit("低", NORMAL)["enqueued"] is True


def test_b2_2_shadow_never_drops_requests(monkeypatch):
    monkeypatch.setenv(M.ENV, "shadow")
    r = A.admit("低", OVER)
    assert r["enqueued"] is True and r["frozen"] is True and r["frozen_enforced"] is False


def test_b2_3_aging_upgrade_not_frozen(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    r = A.admit("低", OVER, age_days=31.0)
    assert r["upgraded"] is True and r["enqueued"] is True


def test_b2_4_backlog_alert_boundary():
    assert A.backlog_alert(base.queue_state(n=81, weekly_new=1))["alert"] is True
    assert A.backlog_alert(base.queue_state(n=80, weekly_new=1))["alert"] is False
    a = A.backlog_alert(base.queue_state(n=101, weekly_new=21))
    assert a["needs_human_cleanup"] is True, "积压只喊人，不自动丢请求"


def test_b2_5_budget_configurable_and_boundary(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    assert A.base.CAPACITY_PER_WEEK == 20
    assert A.admit("低", base.queue_state(n=10, weekly_new=20))["enqueued"] is True
    assert A.admit("低", base.queue_state(n=10, weekly_new=21))["enqueued"] is False


def test_b2_6_queue_file_untouched(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    before = hashlib.sha256(open(A.QUEUE, "rb").read()).hexdigest()
    r = A.replay_queue()
    after = hashlib.sha256(open(A.QUEUE, "rb").read()).hexdigest()
    assert before == after and r["n"] >= 1


def test_b2_7_report_and_selftest():
    assert A.selftest() == 0
    assert A.main(["--report"]) == 0
    doc = json.load(open(A.OUT_JSON, encoding="utf-8"))
    assert doc["mode"] in M.MODES and "backlog" in doc
    assert os.path.isfile(A.OUT_MD)
