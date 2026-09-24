"""632 C1 · autoimmune_human_fill_helper_632 单测（≥5 例，全只读/纯标准库）。"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import autoimmune_human_fill_helper_632 as hf  # noqa: E402


def _qitem(**kw):
    base = {"card_id": "ATOM-X-001", "card_rel": "atoms/x/ATOM-X-001.md",
            "prop_id": "prop-1", "rule": "RULE", "field": "object",
            "suggest": None, "priority": "高"}
    base.update(kw)
    return base


def test_load_queue(tmp_path):
    q = tmp_path / "q.jsonl"
    q.write_text("\n".join(json.dumps(_qitem()) for _ in range(3)) + "\n", encoding="utf-8")
    assert len(hf.load_queue(q)) == 3


def test_locate_in_card_finds_line(tmp_path):
    card = tmp_path / "ATOM-X-001.md"
    card.write_text("frontmatter\nproperties:\n  - id: prop-1\n  - id: prop-2\n", encoding="utf-8")
    line, snip = hf.locate_in_card(str(card.relative_to(tmp_path)), "prop-1", tmp_path)
    assert line == 3 and "prop-1" in snip


def test_locate_in_card_missing(tmp_path):
    line, snip = hf.locate_in_card("atoms/nope.md", "prop-1", tmp_path)
    assert line == 0 and snip == ""


def test_candidate_for_object_no_suggest():
    s = hf.candidate_for(_qitem(field="object", suggest=None))
    assert "无候选" in s


def test_candidate_for_object_with_suggest():
    s = hf.candidate_for(_qitem(field="object", suggest="语义A"))
    assert s == "语义A"


def test_candidate_for_signed_by_is_reminder():
    s = hf.candidate_for(_qitem(field="signed_by"))
    assert "human:<在册实名>" in s and "§零.3" in s


def test_authority_for_signed_by_cites_rule():
    s = hf.authority_for(_qitem(field="signed_by", rule="INFERENCE-NOT-MACHINE-VERIFIED"))
    assert "INFERENCE-NOT-MACHINE-VERIFIED" in s and "§零.3" in s


def test_synthesize_and_main_check(tmp_path):
    q = tmp_path / "q.jsonl"
    card = tmp_path / "ATOM-X-001.md"
    card.write_text("properties:\n  - id: prop-1\n", encoding="utf-8")
    q.write_text(json.dumps(_qitem(card_rel=str(card.relative_to(tmp_path)))) + "\n", encoding="utf-8")
    recs = hf.digest(hf.load_queue(q), tmp_path)
    assert recs[0]["location"].endswith(":2")
    assert hf.main(["--check", "--queue", str(q)]) == 0
