"""405 闪卡导出回归锁：卡型生成/Anki CSV 格式/全量覆盖/空字段零容忍。"""
from __future__ import annotations

import csv
import io
from pathlib import Path

import flashcard_export as fe
import gate_engine as ge


def _atoms() -> list[dict]:
    return [ge._meta(p) for p in ge._cards(ge.ATOMS, "ATOM-*.md")]


def _mises() -> list[dict]:
    return [ge._meta(p) for p in ge._cards(ge.MISCONCEPTIONS, "MIS-*.md")]


def test_atom_claim_card_generation():
    meta = _atoms()[0]
    card = fe.atom_claim_card(meta, {})
    assert card["type"] == "atom_claim" and card["id"] == str(meta["id"])
    assert str(meta["claim"]) in card["front"], "Front 须含问题化论断"
    assert "论断：" in card["back"] and "边界：" in card["back"], "Back 须含论断与边界"


def test_misconception_card_generation():
    meta = next(m for m in _mises() if fe._lines(m.get("refutations"), 3))
    card = fe.misconception_card(meta)
    assert card["type"] == "misconception" and card["id"] == str(meta["id"])
    assert "为什么错" in card["back"], "Back 须解释为什么错"
    assert "反例" in card["back"], "Back 须含反例"


def test_anki_csv_format():
    cards = fe.build_cards()[:5]
    rows = list(csv.reader(io.StringIO(fe._anki_csv(cards))))
    assert rows[0] == ["Front", "Back", "Tags", "Deck"], "首行须为表头"
    assert len(rows) == 6, "表头 + 每卡一行"
    assert all(len(r) == 4 for r in rows), "每行 4 字段"
    assert all(r[3].startswith("CPP-Bible::") for r in rows[1:]), "Deck 须 :: 分层"
    assert all(r[0].strip() and r[1].strip() for r in rows[1:]), "Front/Back 非空"


def test_all_atoms_exported():
    ids = {str(m["id"]) for m in _atoms()}
    cards = {c["id"] for c in fe.build_cards() if c["type"] == "atom_claim"}
    assert cards == ids, "每颗原子恰好 1 张 claim 卡"


def test_all_misconceptions_exported():
    ids = {str(m["id"]) for m in _mises()}
    cards = {c["id"] for c in fe.build_cards() if c["type"] == "misconception"}
    assert cards == ids, "每条误解恰好 1 张反例卡"


def test_no_empty_fields():
    empty = [c["id"] for c in fe.build_cards()
             if not c["front"].strip() or not c["back"].strip()]
    assert empty == [], f"Front/Back 为空的卡：{empty}"


def test_export_writes_files(tmp_path: Path):
    data = fe.export(tmp_path, "both")
    assert data["total_cards"] == len(fe.build_cards())
    assert (tmp_path / "anki.csv").is_file()
    md = tmp_path / "markdown"
    assert md.is_dir()
    assert len(list(md.glob("*.md"))) == data["total_cards"]
    assert data["empty_front_or_back"] == []
