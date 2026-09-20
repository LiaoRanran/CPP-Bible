"""604 任务4 · 群组级人审 + automation bias + 反馈闭环 回归锁。

锁六件事：
  * mis_groups() 返回 42 个群组、按歧义度降序、Top1 = MIS-MEM-028；
  * approve_group() 选命题后自动 approve 对应 MIS→命题边 + 对称边；
  * record_review() 检测理由过短 / agree_rate>90% / 陷阱题答错；
  * progress_summary() 初始 0%、完成后正确反映；
  * feedback_summary() 返回 reject 原因和改进建议；
  * CLI queue/progress/feedback --json 输出合法。
"""
from __future__ import annotations

import json
from pathlib import Path

import attack_edge_review as aer
import gate_engine as ge
import pytest

EDGES = aer.load_edges()


@pytest.fixture(autouse=True)
def _git_author(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(ge, "_git_author_for", lambda _p: (aer.git_user_name(), "x@y"))


# ── mis_groups ─────────────────────────────────────────────────────────────────
def test_mis_groups_returns_42():
    groups = aer.mis_groups(EDGES)
    assert len(groups) == 42
    assert all("mis_id" in g and "ambiguity" in g for g in groups)


def test_mis_groups_sorted_by_ambiguity_desc():
    groups = aer.mis_groups(EDGES)
    ambiguities = [g["ambiguity"] for g in groups]
    assert ambiguities == sorted(ambiguities, reverse=True)


def test_mis_groups_top1_is_mem_028():
    groups = aer.mis_groups(EDGES)
    assert groups[0]["mis_id"] == "MIS-MEM-028"
    assert groups[0]["ambiguity"] > 2.0
    assert groups[0]["n_cards"] == 3
    assert groups[0]["n_edges"] == 18


def test_mis_groups_total_edges_388():
    groups = aer.mis_groups(EDGES)
    assert sum(g["n_edges"] for g in groups) == 388


# ── approve_group ──────────────────────────────────────────────────────────────
def test_approve_group_appends_corresponding_edges(tmp_path: Path):
    p = tmp_path / "ann.jsonl"
    # MIS-MEM-028 关联 ATOM-MEM-PERF-003 的 prop-1
    prop_ids = ["ATOM-MEM-PERF-003::prop-1"]
    recs = aer.approve_group("MIS-MEM-028", prop_ids,
                              "群组审核：该误解确实攻击 prop-1",
                              annotations_path=p, edges_path=aer.DEFAULT_EDGES)
    # 应该有 2 条：MIS→prop 边 + 对称边
    assert len(recs) == 2
    assert all(r["action"] == "approve" for r in recs)
    # 检查这两条边确实涉及该命题
    by_id = {str(e["id"]): e for e in EDGES}
    for r in recs:
        e = by_id[r["edge_id"]]
        other = e["target"] if e["source"] == "MIS-MEM-028" else e["source"]
        assert other == "ATOM-MEM-PERF-003::prop-1"


def test_approve_group_missing_reason_refused(tmp_path: Path):
    p = tmp_path / "ann.jsonl"
    with pytest.raises(ValueError, match="缺 --reason"):
        aer.approve_group("MIS-MEM-028", ["ATOM-MEM-PERF-003::prop-1"],
                           "", annotations_path=p, edges_path=aer.DEFAULT_EDGES)
    assert not p.exists()


# ── automation bias ────────────────────────────────────────────────────────────
def test_load_audit_default_empty():
    audit = aer.load_audit("/nonexistent/path.json")
    assert audit["total_reviews"] == 0
    assert audit["approve_count"] == 0
    assert audit["alerts"] == []


def test_record_review_suspicious_short_reason():
    audit = aer.load_audit("/nonexistent/path.json")
    alerts = aer.record_review(audit, "approve", "ok", 2.0)
    assert audit["suspicious_count"] == 1
    assert any("suspicious" in a for a in alerts)


def test_record_review_agree_rate_alert():
    audit = aer.load_audit("/nonexistent/path.json")
    # 前 9 次 approve（理由充分、时间充足）
    for i in range(9):
        aer.record_review(audit, "approve", f"充分的审核理由第{i}条", 30.0)
    # 第 10 次 approve 触发 agree_rate>90%
    alerts = aer.record_review(audit, "approve", "第十条充分理由", 30.0)
    assert audit["total_reviews"] == 10
    assert any("agree_rate" in a for a in alerts)


def test_record_review_trap_wrong():
    audit = aer.load_audit("/nonexistent/path.json")
    alerts = aer.record_review(audit, "approve", "陷阱题答错了", 10.0,
                                is_trap=True, trap_correct=False)
    assert audit["trap_total"] == 1
    assert audit["trap_correct"] == 0
    assert any("TRAP" in a for a in alerts)


def test_save_and_load_audit_roundtrip(tmp_path: Path):
    p = tmp_path / "audit.json"
    audit = aer.load_audit("/nonexistent/path.json")
    aer.record_review(audit, "approve", "测试审核理由", 15.0)
    aer.save_audit(audit, p)
    loaded = aer.load_audit(p)
    assert loaded["total_reviews"] == 1
    assert loaded["approve_count"] == 1


# ── progress ───────────────────────────────────────────────────────────────────
def test_progress_summary_zero_initially():
    groups = aer.mis_groups(EDGES)
    prog = aer.progress_summary(EDGES, [], groups)
    assert prog["total_groups"] == 42
    assert prog["done_groups"] == 0
    assert prog["pending_groups"] == 42
    assert prog["completion_pct"] == 0.0
    assert prog["est_remaining_minutes"] == 24.5  # 42 * 35 / 60


def test_progress_summary_after_approval(tmp_path: Path):
    p = tmp_path / "ann.jsonl"
    aer.approve_group("MIS-MEM-028", ["ATOM-MEM-PERF-003::prop-1"],
                       "审核通过", annotations_path=p, edges_path=aer.DEFAULT_EDGES)
    anns = aer.load_annotations(p)
    groups = aer.mis_groups(EDGES)
    prog = aer.progress_summary(EDGES, anns, groups)
    # MIS-MEM-028 还有其他 pending 边，所以群组不算 done
    assert prog["done_edges"] == 2
    assert prog["pending_edges"] == 386


# ── feedback ───────────────────────────────────────────────────────────────────
def test_feedback_summary_empty():
    fb = aer.feedback_summary([])
    assert fb["total_annotations"] == 0
    assert fb["reject_count"] == 0
    assert len(fb["suggestions"]) == 3


def test_feedback_summary_with_rejects(tmp_path: Path):
    p = tmp_path / "ann.jsonl"
    aer.append_annotation(str(EDGES[0]["id"]), "reject",
                           "该边关联过宽，误解与命题无直接反驳关系",
                           path=p, edges_path=aer.DEFAULT_EDGES)
    anns = aer.load_annotations(p)
    fb = aer.feedback_summary(anns)
    assert fb["total_annotations"] == 1
    assert fb["reject_count"] == 1
    assert "关联过宽" in fb["reject_reasons"][0]


# ── CLI --json ─────────────────────────────────────────────────────────────────
def test_cli_queue_json():
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = aer.main(["queue", "--json"])
    assert rc == 0
    data = json.loads(buf.getvalue())
    assert data["count"] == 42
    assert data["groups"][0]["mis_id"] == "MIS-MEM-028"


def test_cli_progress_json():
    """人审全量完成（388/388）⇒ progress 反映真实完成度（不再假设"零人审"）。"""
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = aer.main(["progress", "--json"])
    assert rc == 0
    data = json.loads(buf.getvalue())
    assert data["total_groups"] == 42
    assert data["done_groups"] == 42 and data["pending_groups"] == 0
    assert data["done_edges"] == 388 and data["pending_edges"] == 0
    assert data["completion_pct"] == 100.0


def test_cli_feedback_json():
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = aer.main(["feedback", "--json"])
    assert rc == 0
    data = json.loads(buf.getvalue())
    assert "suggestions" in data
    assert len(data["suggestions"]) == 3
