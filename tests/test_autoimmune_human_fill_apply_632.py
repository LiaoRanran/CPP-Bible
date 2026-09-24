"""632 C2 · autoimmune_human_fill_apply_632 单测（≥5 例）。"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import autoimmune_human_fill_apply_632 as ap  # noqa: E402

CARD = """---
id: ATOM-X-001
claim_structured:
  - id: prop-1
    subject: s
    object: 旧值
    claim_type: observation
  - id: prop-2
    subject: s2
    claim_type: inference
claim_boundary:
  standard: [C++11]
---
body
"""


def _dec(field, value, prop="prop-1"):
    return {"card_id": "ATOM-X-001", "card_rel": "atoms/x/ATOM-X-001.md",
            "prop_id": prop, "field": field, "value": value}


def test_signed_by_shell_wraps_v02():
    assert ap._signed_by_shell("human:张三") == "v0.2:human:张三"
    assert ap._signed_by_shell("v0.2:human:张三") == "v0.2:human:张三"


def test_apply_decision_sets_existing_object():
    new = ap.apply_decision(CARD, "prop-1", "object", "新语义")
    assert "object: 新语义" in new
    assert "object: 旧值" not in new


def test_apply_decision_adds_missing_signed_by():
    new = ap.apply_decision(CARD, "prop-2", "signed_by", "human:张三")
    assert "signed_by: v0.2:human:张三" in new


def test_apply_decision_does_not_touch_other_prop():
    new = ap.apply_decision(CARD, "prop-1", "object", "X")
    assert "prop-2" in new  # 另一命题块保留


def test_load_decisions(tmp_path):
    d = tmp_path / "dec.jsonl"
    d.write_text(json.dumps(_dec("object", "X")) + "\n", encoding="utf-8")
    assert len(ap.load_decisions(d)) == 1


def test_dry_run_does_not_write(tmp_path, monkeypatch):
    card = tmp_path / "atoms" / "x" / "ATOM-X-001.md"
    card.parent.mkdir(parents=True)
    card.write_text(CARD, encoding="utf-8")
    monkeypatch.setattr(ap, "REPO_ROOT", tmp_path)
    diffs = ap.apply_decisions([_dec("object", "新语义")], tmp_path, dry_run=True)
    assert diffs and "object: 新语义" in diffs[0]
    assert "object: 旧值" in card.read_text(encoding="utf-8")  # 未写盘


def test_apply_writes_to_disk(tmp_path, monkeypatch):
    card = tmp_path / "atoms" / "x" / "ATOM-X-001.md"
    card.parent.mkdir(parents=True)
    card.write_text(CARD, encoding="utf-8")
    monkeypatch.setattr(ap, "REPO_ROOT", tmp_path)
    ap.apply_decisions([_dec("object", "新语义")], tmp_path, dry_run=False)
    assert "object: 新语义" in card.read_text(encoding="utf-8")
    assert "object: 旧值" not in card.read_text(encoding="utf-8")


def test_main_check_exit_0(tmp_path, monkeypatch):
    d = tmp_path / "dec.jsonl"
    d.write_text(json.dumps(_dec("object", "X")) + "\n", encoding="utf-8")
    monkeypatch.setattr(ap, "DECISIONS", d)
    assert ap.main(["--check", "--decisions", str(d)]) == 0
