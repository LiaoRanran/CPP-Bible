"""610 D2 · 人审进度集成（tools/metrics_610.py::collect_human_review_progress）。

锁五件事（任务书 D2 的 5 例 + 2 例自加）：
  1. 键齐全（total/reviewed/unreviewed/approve/modify/reject/progress_percent/
     top_modify_mis/mis_groups/source）；
  2. `progress_percent` = **100.0**（人审全量完成）；
  3. approve **354** / modify **34** / reject **0**；
  4. `top_modify_mis` 首位 **MIS-LANG-001**（6/6 全 modify）；
  5. 文件缺失 ⇒ `{"error": ...}` + notes 记账；
  +. 与 608 的 `human_review` 同值（防两套数字打架）；
  +. 容器 `metrics_610` 已含 `human_review_progress` 键。
"""
from __future__ import annotations

import metrics_610 as m610
import metrics_collector as mc


def test_collect_human_review_progress():
    out = m610.collect_human_review_progress({})
    for k in ("total_edges", "reviewed", "unreviewed", "approve", "modify", "reject",
              "progress_percent", "top_modify_mis", "mis_groups", "source"):
        assert k in out, f"缺字段 {k}"
    assert out["source"].endswith("human_attack_edge_annotations.jsonl（用户授权人审）")


def test_progress_100_percent():
    out = m610.collect_human_review_progress({})
    assert out["progress_percent"] == 100.0
    assert out["reviewed"] == 388 and out["unreviewed"] == 0
    assert out["total_edges"] == 388 and out["mis_groups"] == 42


def test_approve_modify_counts():
    out = m610.collect_human_review_progress({})
    assert (out["approve"], out["modify"], out["reject"]) == (354, 34, 0)


def test_top_modify_mis():
    out = m610.collect_human_review_progress({})
    assert out["top_modify_mis"][0] == "MIS-LANG-001"
    assert len(out["top_modify_mis"]) == 5
    assert set(out["top_modify_mis"]) <= {"MIS-LANG-001", "MIS-MEM-001", "MIS-MEM-003",
                                         "MIS-UB-001", "MIS-UB-004", "MIS-UB-008", "MIS-UB-014"}


def test_file_not_found(monkeypatch):
    import human_review_report as hrr

    def boom(*_a, **_k):
        raise FileNotFoundError("annotation file gone")

    monkeypatch.setattr(hrr, "load_annotations", boom)
    notes: dict = {}
    out = m610.collect_human_review_progress({}, notes)
    assert "error" in out and "FileNotFoundError" in out["error"]
    assert "human_review_progress_610" in notes
    assert "reviewed" not in out, "失败路径不得给出半截进度数"


def test_agrees_with_608_human_review():
    """608 与 610 两套人审指标必须同值（防"两套数字打架"）。"""
    a = m610.collect_human_review_progress({})
    b = mc.collect_608_new_metrics({}, with_heavy=False)["human_review"]
    assert a["approve"] == b["approved"] == 354
    assert a["modify"] == b["modified"] == 34
    assert a["reject"] == b["rejected"] == 0
    assert a["reviewed"] == b["annotated_edges"] == 388


def test_container_includes_key():
    d = m610.collect_610_new_metrics({}, with_heavy=False)
    assert set(d) >= {"grounded_status", "human_review_progress"}
    assert d["human_review_progress"]["progress_percent"] == 100.0
