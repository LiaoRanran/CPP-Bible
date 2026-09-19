"""596 任务4 · 候选攻击边人审接口回归锁。

锁四件事：
  * 正例：approve/reject/modify 各追加一条记录（**只追加**），`stats` 反映进度；
  * fail-closed：缺理由 / edge_id 不存在 / 冒名 / git 不可用 / 无签名 ⇒ **一行都不写**；
  * 生效规则：reject 剔除、approve 升一级、modify 指定档、**同一 Id 取最后一条**；
  * W2 集成：reject 掉某个误解的全部"被击败"边 ⇒ 该误解**真的**翻成 IN（说明人审有后果，不是装饰）。
"""
from __future__ import annotations

import json
from pathlib import Path

import attack_edge_review as aer
import gate_engine as ge
import pytest
import weighted_af_solver as w2

EDGES = aer.load_edges()
ANNOTATED_ID = str(EDGES[0]["id"])


def _mis_of(edge_id: str) -> str:
    for e in EDGES:
        if str(e["id"]) == edge_id:
            return str(e["source"]) if e["direction"] == "mis_to_prop" else str(e["target"])
    raise AssertionError(edge_id)


@pytest.fixture(autouse=True)
def _git_author(monkeypatch: pytest.MonkeyPatch):
    """把误解卡作者钉成当前 git 用户（离线可复现；真实环境实测同为 LiaoRanran）。"""
    monkeypatch.setattr(ge, "_git_author_for", lambda _p: (aer.git_user_name(), "x@y"))


# ── 正例 ───────────────────────────────────────────────────────────────────────
def test_approve_appends_one_record(tmp_path: Path):
    p = tmp_path / "ann.jsonl"
    rec = aer.append_annotation(ANNOTATED_ID, "approve", "人审确认：该误解确实攻击这条命题",
                                path=p, edges_path=aer.DEFAULT_EDGES)
    assert rec["edge_id"] == ANNOTATED_ID and rec["action"] == "approve"
    assert rec["reviewer"] == aer.git_user_name() and rec["reason"]
    lines = p.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1 and json.loads(lines[0]) == rec
    assert p.read_text(encoding="utf-8").endswith("\n")
    st = aer.stats(EDGES, aer.load_annotations(p))
    assert st["approved"] == 1 and st["pending"] == len(EDGES) - 1
    assert aer.status_of(ANNOTATED_ID, aer.latest_by_edge([rec])) == "approved"


def test_reject_and_modify_records(tmp_path: Path):
    p = tmp_path / "ann.jsonl"
    aer.append_annotation(ANNOTATED_ID, "reject", "错的边：该卡与误解只是同域，无反驳关系",
                          path=p, edges_path=aer.DEFAULT_EDGES)
    other = str(EDGES[1]["id"])
    rec = aer.append_annotation(other, "modify", "语义强度不足，降档", new_confidence="low",
                                path=p, edges_path=aer.DEFAULT_EDGES)
    assert rec["new_confidence"] == "low"
    st = aer.stats(EDGES, aer.load_annotations(p))
    assert (st["rejected"], st["modified"], st["annotated_edges"]) == (1, 1, 2)
    assert st["reject_rate"] == 0.5


def test_append_only_history_same_edge_twice(tmp_path: Path):
    """同一条边审两次 ⇒ **两条历史**（不覆盖，"改主意"可追溯），生效取最后一条。"""
    p = tmp_path / "ann.jsonl"
    aer.append_annotation(ANNOTATED_ID, "reject", "先拒", path=p, edges_path=aer.DEFAULT_EDGES)
    aer.append_annotation(ANNOTATED_ID, "approve", "复审后接受", path=p, edges_path=aer.DEFAULT_EDGES)
    anns = aer.load_annotations(p)
    assert len(anns) == 2, "只追加：历史不许被覆盖"
    last = aer.latest_by_edge(anns)
    assert aer.status_of(ANNOTATED_ID, last) == "approved", "生效值取最后一条"
    eff = aer.effective_edges(EDGES, anns)
    assert ANNOTATED_ID in {str(e["id"]) for e in eff}


# ── fail-closed ────────────────────────────────────────────────────────────────
def test_missing_reason_refused(tmp_path: Path):
    p = tmp_path / "ann.jsonl"
    with pytest.raises(ValueError, match="缺 --reason"):
        aer.append_annotation(ANNOTATED_ID, "approve", "   ", path=p, edges_path=aer.DEFAULT_EDGES)
    assert not p.exists(), "缺理由时连文件都不许建"


def test_unknown_edge_id_refused(tmp_path: Path):
    p = tmp_path / "ann.jsonl"
    with pytest.raises(ValueError, match="edge_id 不存在"):
        aer.append_annotation("ae-NOPE->NOPE", "reject", "理由", path=p,
                              edges_path=aer.DEFAULT_EDGES)
    assert not p.exists()


def test_impersonation_refused(tmp_path: Path):
    p = tmp_path / "ann.jsonl"
    with pytest.raises(ValueError, match="不许冒名"):
        aer.append_annotation(ANNOTATED_ID, "approve", "理由", reviewer="Attacker",
                              path=p, edges_path=aer.DEFAULT_EDGES)
    assert not p.exists()


def test_git_unavailable_or_unsigned_refused(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    p = tmp_path / "ann.jsonl"
    monkeypatch.setattr(aer, "git_user_name", lambda: None)
    with pytest.raises(ValueError, match="git 不可用"):
        aer.append_annotation(ANNOTATED_ID, "approve", "理由", path=p, edges_path=aer.DEFAULT_EDGES)
    monkeypatch.setattr(aer, "git_user_name", lambda: "LiaoRanran")
    monkeypatch.setattr(ge, "_git_author_for", lambda _p: ("Somebody", "s@x"))
    with pytest.raises(ValueError, match="不是该误解卡"):
        aer.append_annotation(ANNOTATED_ID, "approve", "理由", path=p, edges_path=aer.DEFAULT_EDGES)
    monkeypatch.setattr(ge, "_git_author_for", lambda _p: None)
    with pytest.raises(ValueError, match="git 不可用"):
        aer.append_annotation(ANNOTATED_ID, "approve", "理由", path=p, edges_path=aer.DEFAULT_EDGES)
    assert not p.exists(), "任何失败路径都不得落行"


def test_bad_action_and_modify_without_confidence_refused(tmp_path: Path):
    p = tmp_path / "ann.jsonl"
    with pytest.raises(ValueError, match="action 须为"):
        aer.append_annotation(ANNOTATED_ID, "rubber-stamp", "理由", path=p,
                              edges_path=aer.DEFAULT_EDGES)
    with pytest.raises(ValueError, match="modify 须给 --confidence"):
        aer.append_annotation(ANNOTATED_ID, "modify", "理由", path=p,
                              edges_path=aer.DEFAULT_EDGES)


# ── 生效规则 ───────────────────────────────────────────────────────────────────
def test_effective_edges_rules():
    low = next(e for e in EDGES if e["confidence"] == "low")
    mid = {**low, "id": "ae-synth->x", "confidence": "medium"}
    high = {**low, "id": "ae-synth->y", "confidence": "high"}
    anns = [{"edge_id": str(low["id"]), "action": "approve"},
            {"edge_id": "ae-synth->x", "action": "modify", "new_confidence": "low"},
            {"edge_id": "ae-synth->y", "action": "reject"}]
    eff = {str(e["id"]): e for e in aer.effective_edges([low, mid, high], anns)}
    assert eff[str(low["id"])]["confidence"] == "medium", "approve 升一级"
    assert eff["ae-synth->x"]["confidence"] == "low", "modify 用指定档"
    assert "ae-synth->y" not in eff, "reject 剔除"


def test_w2_uses_effective_edges_and_reject_has_consequence(tmp_path: Path):
    """reject 掉某误解的全部'被击败'边 ⇒ 该误解翻成 IN（人审**有后果**，不是装饰）。"""
    mis = _mis_of(ANNOTATED_ID)
    to_reject = [e for e in EDGES if e["direction"] == "prop_to_mis" and str(e["target"]) == mis]
    assert to_reject, "该误解应至少有一条'被命题击败'边"
    anns = [{"edge_id": str(e["id"]), "action": "reject"} for e in to_reject]
    eff = aer.effective_edges(EDGES, anns)
    assert not ({str(e["id"]) for e in to_reject} & {str(e["id"]) for e in eff})
    base = w2.solve(EDGES)
    after = w2.solve(eff)
    assert base["nodes"][mis]["label"] == "OUT"
    assert after["nodes"][mis]["label"] == "IN", "拒绝掉全部击败边后，误解不再被击败 ⇒ 翻 IN"
    assert after["summary"]["IN_misconceptions"] == 1


def test_cli_roundtrip_and_check(tmp_path: Path):
    edges_path = tmp_path / "cand.jsonl"
    edges_path.write_bytes(aer.DEFAULT_EDGES.read_bytes())
    ann = tmp_path / "ann.jsonl"
    argv = ["--edges", str(edges_path), "--annotations", str(ann)]
    assert aer.main(["list", *argv, "--status", "pending"]) == 0
    assert aer.main(["show", ANNOTATED_ID, *argv]) == 0
    assert aer.main(["approve", ANNOTATED_ID, "--reason", "确认", *argv]) == 0
    assert aer.main(["modify", str(EDGES[1]["id"]), "--confidence", "high", "--reason", "提权",
                     *argv]) == 0
    assert aer.main(["reject", str(EDGES[2]["id"]), "--reason", "拒绝", *argv]) == 0
    assert aer.main(["stats", *argv, "--json"]) == 0
    assert aer.main(["--check", *argv]) == 0
    # 反例：缺理由 ⇒ exit 2；--check 抓到坏记录 ⇒ exit 2
    assert aer.main(["approve", str(EDGES[3]["id"]), "--reason", "", *argv]) == 2
    ann.write_text('{"edge_id": "ae-NOPE", "action": "approve", "reason": "r",'
                   ' "reviewer": "x", "timestamp": "t"}\n', encoding="utf-8")
    assert aer.main(["--check", *argv]) == 2


def test_real_annotations_file_is_empty_and_valid():
    """初始通道：真实标注文件必须存在、为空、校验通过（系统绝不自动产生标注）。"""
    assert aer.DEFAULT_ANN.is_file(), "人审通道文件必须入库"
    assert aer.load_annotations() == []
    assert aer.main(["--check"]) == 0
