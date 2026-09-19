"""609 A4 · 人审反馈闭环回归锁（拒绝原因 4 分类 + 反馈规则）。

锁的是 4 类发动机our == 4 类 action 的**逐类正确性**，以及"闭环止于建议"这条边界：
 1. reason 含"误解不成立"        ⇒ misconception_invalid / downgrade_weight
 2. reason 含"目标命题错误"      ⇒ target_mapping_error   / force_mapping
 3. reason 含"与 X 重复"         ⇒ duplicate_edge         / deduplicate
 4. apply 合法 rule_id ⇒ applied=true；不存在 ⇒ exit 1
 5. report 含分布 + 预计提升（降权/强制映射/去重）
 +. 不命中 ⇒ other/none（**不猜分类**）；applied 默认 false，且 analyze 重跑不撤销人的确认。

所有用例走 tmp 路径，**不写真实 data/** 下的规则文件。
"""
from __future__ import annotations

import json
from pathlib import Path

import human_review_cli as hrc
import human_review_feedback as hrf
import pytest

EDGE = sorted(hrc.load_edge_ids())[0]
EDGE2 = sorted(hrc.load_edge_ids())[1]


def _rec(edge_id: str, reason: str) -> dict:
    return {"edge_id": edge_id, "kind": "reject", "reviewer": "human",
            "timestamp": "2026-09-19T10:00:00+08:00", "reason": reason}


@pytest.fixture
def paths(tmp_path: Path):
    class P:
        ann = tmp_path / "ann.jsonl"
        rules = tmp_path / "rules.json"
    return P()


def _write_ann(paths, rows: list[dict]) -> None:
    paths.ann.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                         encoding="utf-8", newline="\n")


def _analyze(paths) -> list[dict]:
    assert hrf.main(["--annotations", str(paths.ann), "--rules", str(paths.rules),
                     "analyze"]) == 0
    return hrf.load_rules(paths.rules)


@pytest.mark.parametrize("reason,category,action", [
    ("经复核该误解不成立，攻击证据为空壳", "misconception_invalid", "downgrade_weight"),
    ("目标命题错误：这条驳斥的其实是另一条命题", "target_mapping_error", "force_mapping"),
    ("与 ae-MIS-MEM-032->ATOM-MEM-PERF-003::prop-3 重复，合并处理",
     "duplicate_edge", "deduplicate"),
    ("这条边需要人再想想，暂无明确归类", "other", "none"),
])
def test_reason_classification(paths, reason: str, category: str, action: str):
    _write_ann(paths, [_rec(EDGE, reason)])
    rules = _analyze(paths)
    assert len(rules) == 1
    assert (rules[0]["category"], rules[0]["action"]) == (category, action)
    assert rules[0]["applied"] is False, "applied 必须默认 false（需人显式确认）"
    assert rules[0]["rule_id"] == "FB-001"
    assert rules[0]["source_edge_id"] == EDGE
    assert hrf.check(paths.rules) == []


def test_action_params_are_populated(paths):
    _write_ann(paths, [_rec(EDGE, "经复核该误解不成立：MIS 组本身的描述有误"),
                       _rec(EDGE2, "目标命题错误：映射到了相邻命题")])
    rules = {r["source_edge_id"]: r for r in _analyze(paths)}
    assert rules[EDGE]["param"] == {"from": "low", "to": "very_low"}
    assert rules[EDGE2]["param"] == {"mapping": "strict", "allow_fuzzy": False}


def test_apply_marks_rule_and_unknown_id_exits_1(paths, capsys):
    _write_ann(paths, [_rec(EDGE, "经复核该误解不成立，建议降权")])
    rules = _analyze(paths)
    rid = rules[0]["rule_id"]
    capsys.readouterr()
    assert hrf.main(["--rules", str(paths.rules), "apply", rid]) == 0
    assert f"APPLIED: {rid}" in capsys.readouterr().out
    assert hrf.load_rules(paths.rules)[0]["applied"] is True
    assert hrf.main(["--rules", str(paths.rules), "apply", "FB-999"]) == 1
    # 已确认状态不被 analyze 重跑静默撤销（人的判断是权威）
    _analyze(paths)
    assert hrf.load_rules(paths.rules)[0]["applied"] is True


def test_report_contains_distribution_and_expected_gain(paths, capsys):
    _write_ann(paths, [_rec(EDGE, "经复核该误解不成立"),
                       _rec(EDGE2, "与相邻边重复，去重处理")])
    _analyze(paths)
    capsys.readouterr()
    assert hrf.main(["--rules", str(paths.rules), "report"]) == 0
    out = capsys.readouterr().out
    for key in ("拒绝原因分布", "预计下一轮质量提升", "降权", "强制映射", "去重"):
        assert key in out, f"报告缺 {key}"
    s = hrf.summarize(hrf.load_rules(paths.rules))
    assert s["rules"] == 2 and s["pending"] == 2
    assert s["expected_actions"]["downgrade_weight"] == 1
    assert s["expected_actions"]["deduplicate"] == 1


def test_only_rejects_produce_rules(paths):
    """approve/modify 不产生反馈规则（反馈闭环只处理**拒绝**）。"""
    _write_ann(paths, [{"edge_id": EDGE, "kind": "approve", "reviewer": "human",
                        "timestamp": "2026-09-19T10:00:00+08:00",
                        "reason": "人审确认：该误解不成立的说法不成立"}])
    assert _analyze(paths) == []


def test_missing_rules_file_check_is_green(tmp_path: Path):
    assert hrf.main(["--rules", str(tmp_path / "none.json"), "--check"]) == 0
