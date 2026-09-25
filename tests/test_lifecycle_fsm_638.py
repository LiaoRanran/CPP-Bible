"""638 3.2 · Lifecycle FSM 单测（>=6 例，纯标准库；不碰真实 ledger）。"""
from __future__ import annotations

import json
import os

import tools.lifecycle_fsm_638 as m


# 3.2-1：五态定义与迁移表完备
def test_states_and_legal_table():
    assert m.STATES == ["draft", "verified", "stale", "disputed", "retired"]
    assert set(m.LEGAL) == set(m.STATES)
    assert m.LEGAL["retired"] == {"draft"}


# 3.2-2：全部合法迁移（§三.3.2.2 共 11 条）逐一放行
def test_all_legal_transitions():
    legal = [("draft", "verified"), ("draft", "retired"), ("verified", "stale"),
             ("verified", "disputed"), ("verified", "retired"), ("stale", "verified"),
             ("stale", "disputed"), ("stale", "retired"), ("disputed", "verified"),
             ("disputed", "retired")]
    for s, d in legal:
        ok, why = m.can_transition(s, d)
        assert ok, f"{s}->{d} 应合法：{why}"
    assert m.can_transition("retired", "draft", "new_evidence")[0] is True


# 3.2-3：非法迁移被拒（含跨级/回退/越界）
def test_illegal_transitions_rejected():
    for s, d in [("draft", "stale"), ("draft", "disputed"), ("verified", "draft"),
                 ("stale", "draft"), ("disputed", "stale"), ("retired", "verified"),
                 ("retired", "stale"), ("retired", "disputed")]:
        ok, why = m.can_transition(s, d)
        assert not ok, f"{s}->{d} 应非法"
        assert "非法" in why or "不允许" in why
    assert not m.can_transition("nope", "draft")[0]
    assert not m.can_transition("draft", "nope")[0]


# 3.2-4：复活必须给合法复活条件
def test_revival_requires_condition():
    ok, why = m.can_transition("retired", "draft")
    assert not ok and "复活" in why
    for bad in ("", "随便", "EXPIRED"):
        assert not m.can_transition("retired", "draft", bad)[0]
    for good in m.REVIVAL_CONDITIONS:
        assert m.can_transition("retired", "draft", good)[0]


# 3.2-5：矩阵 25 组合 + 合法数正确
def test_matrix_shape():
    pairs = m.all_pairs()
    assert len(pairs) == 25
    assert {p["legal"] for p in pairs} == {True, False}
    assert sum(1 for p in pairs if p["legal"]) == 11   # §三.3.2.2 共 11 条


# 3.2-6：append-only ledger 追写 + 哈希链校验
def test_ledger_append_and_verify(tmp_path):
    led = str(tmp_path / "led.jsonl")
    r1 = m.append_transition("atoms/x.md", "draft", "verified", "首次验证", path=led)
    assert r1["ok"] and r1["record"]["seq"] == 1
    assert r1["record"]["prev_hash"] == "GENESIS"
    r2 = m.append_transition("atoms/x.md", "verified", "stale", "边界漂移", path=led)
    assert r2["ok"] and r2["record"]["seq"] == 2
    assert r2["record"]["prev_hash"] == r1["record"]["self_hash"]
    recs = m.load_ledger(led)
    assert len(recs) == 2 and m.verify_ledger(recs) == []
    # append-only：原行未被改写
    first_line = open(led, encoding="utf-8").readline()
    assert json.loads(first_line)["self_hash"] == r1["record"]["self_hash"]


# 3.2-7：非法迁移不写 ledger
def test_illegal_transition_not_recorded(tmp_path):
    led = str(tmp_path / "led.jsonl")
    r = m.append_transition("atoms/x.md", "draft", "stale", "非法", path=led)
    assert r["ok"] is False
    assert not os.path.exists(led)


# 3.2-8：篡改可被 verify_ledger 检出
def test_verify_detects_tamper(tmp_path):
    led = str(tmp_path / "led.jsonl")
    m.append_transition("a.md", "draft", "verified", path=led)
    recs = m.load_ledger(led)
    recs[0]["reason"] = "被篡改"
    errs = m.verify_ledger(recs)
    assert any("self_hash" in e for e in errs)


# 3.2-9：当前态查询（lifecycle 优先 / status 映射 / 默认 draft）
def test_current_state_derivation(tmp_path):
    p1 = tmp_path / "a.md"
    p1.write_text("---\nlifecycle: disputed\n---\n", encoding="utf-8")
    assert m.current_state(str(p1))["state"] == "disputed"
    assert m.current_state(str(p1))["source"] == "lifecycle 字段"
    p2 = tmp_path / "b.md"
    p2.write_text("---\nstatus: red-team-verified\n---\n", encoding="utf-8")
    assert m.current_state(str(p2))["state"] == "verified"
    p3 = tmp_path / "c.md"
    p3.write_text("---\nid: X\n---\n", encoding="utf-8")
    assert m.current_state(str(p3))["state"] == "draft"
    assert m.current_state(str(tmp_path / "missing.md"))["state"] == "draft"


# 3.2-10：全库普查与输出路径
def test_census_and_paths():
    c = m.census()
    assert c["n"] >= 1 and sum(c["dist"].values()) == c["n"]
    assert set(c["dist"]) <= set(m.STATES)
    assert c["ledger_errs"] == []
    assert m.OUT_MD.startswith(os.path.join(m.ROOT, "data"))
    assert m.LEDGER.startswith(os.path.join(m.ROOT, "data"))
