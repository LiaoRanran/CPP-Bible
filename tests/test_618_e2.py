#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 E2 · human_review_todo_generator_618 单测（≥3 例）"""
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import human_review_todo_generator_618 as g  # noqa: E402


def _seed_ev(tmp, names):
    ev = os.path.join(tmp, "evidence")
    os.makedirs(ev, exist_ok=True)
    for n in names:
        with open(os.path.join(ev, n), "w", encoding="utf-8") as f:
            f.write("# %s\nmirror edge present\n" % n)


def test_collect_ev_cards_sorts_and_limits():
    with tempfile.TemporaryDirectory() as d:
        _seed_ev(d, ["EV-003.md", "EV-001.md", "EV-002.md", "EV-010.md"])
        cards = g.collect_ev_cards(os.path.join(d, "evidence"), limit=30)
        assert cards == ["evidence/EV-001.md", "evidence/EV-002.md",
                         "evidence/EV-003.md", "evidence/EV-010.md"]


def test_build_has_30_when_enough():
    with tempfile.TemporaryDirectory() as d:
        ev = os.path.join(d, "evidence")
        os.makedirs(ev)
        for i in range(40):
            open(os.path.join(ev, "EV-%03d.md" % i), "w").write("x")
        items = g.build(limit=30, ev_dir=ev)
        assert len(items) == 30
        assert all(it["status"] == "pending" for it in items)
        assert all(it["decision_options"] == ["approve", "modify", "reject"] for it in items)


def test_detect_mirror_edge():
    with tempfile.TemporaryDirectory() as d:
        ev = os.path.join(d, "evidence")
        os.makedirs(ev)
        open(os.path.join(ev, "EV-m.md"), "w").write("this card has 镜像 edge\n")
        open(os.path.join(ev, "EV-n.md"), "w").write("plain card\n")
        cards = g.collect_ev_cards(ev, limit=30)
        m = {c: g.detect_mirror_edge(c, ev) for c in cards}
        assert m["evidence/EV-m.md"] is True
        assert m["evidence/EV-n.md"] is False


def test_build_marks_mirror():
    with tempfile.TemporaryDirectory() as d:
        ev = os.path.join(d, "evidence")
        os.makedirs(ev)
        open(os.path.join(ev, "EV-a.md"), "w", encoding="utf-8").write("this card has 镜像 edge\n")
        open(os.path.join(ev, "EV-b.md"), "w", encoding="utf-8").write("plain card only\n")
        items = g.build(limit=30, ev_dir=ev)
        by_card = {it["card"]: it for it in items}
        assert by_card["evidence/EV-a.md"]["mirror_edge"] is True
        assert by_card["evidence/EV-b.md"]["mirror_edge"] is False


def test_render_markdown_contains_header():
    with tempfile.TemporaryDirectory() as d:
        _seed_ev(d, ["EV-001.md", "EV-002.md"])
        ev = os.path.join(d, "evidence")
        items = g.build(limit=30, ev_dir=ev)
        txt = g.render_markdown(items)
        assert "30" in txt or "2" in txt
        assert "逐项语义审查" in txt
        assert "| 序号 |" in txt


if __name__ == "__main__":
    test_collect_ev_cards_sorts_and_limits()
    test_build_has_30_when_enough()
    test_detect_mirror_edge()
    test_build_marks_mirror()
    test_render_markdown_contains_header()
    print("ALL E2 TESTS PASSED")
