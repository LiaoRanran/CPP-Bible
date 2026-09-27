#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""653 工具测试（前端 P0 数据层）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import web_data_653 as wd  # noqa: E402


def test_web_data_selftest():
    assert wd.selftest() == 0


def test_graph_matches_declared_w2_counts():
    g = wd.build_graph()
    c = g["meta"]["counts"]
    decl = g["meta"]["w2_declared"]
    assert c["by_kind"]["attack"] == decl["edges"] == 388
    assert c["defeated_links"] == decl["defeating_edges"] == 194


def test_graph_no_dangling_links_and_required_keys():
    g = wd.build_graph()
    ids = {n["id"] for n in g["nodes"]}
    assert all({"id", "kind", "state", "credibility"} <= set(n) for n in g["nodes"])
    assert all({"source", "target", "kind", "defeated"} <= set(lk) for lk in g["links"])
    assert all(lk["source"] in ids and lk["target"] in ids for lk in g["links"])


def test_graph_has_all_four_states_and_three_kinds():
    g = wd.build_graph()
    assert {n["state"] for n in g["nodes"]} == {"pass", "pass_with_exception", "fail", "unknown"}
    assert {n["kind"] for n in g["nodes"]} == {"card", "prop", "misconception"}


def test_manifest_hashes_are_real_sha256():
    m = wd.build_manifest()
    assert m["count"] > 0
    assert all(len(i["sha256"]) == 64 for i in m["items"])
    assert all(i["bytes"] > 0 for i in m["items"])
