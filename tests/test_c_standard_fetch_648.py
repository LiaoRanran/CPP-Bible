"""648 A0 · C 标准原文抓取回归锁（编号 S-1..S-4）。

**不联网**：只锁"已落盘的事实"（`data/648_c_standard.json` 与它给的引用可复核性）。
真抓取（`--fetch`）只由人工/批次显式触发，不进 CI。
"""
from __future__ import annotations

import json
import os
import re

import c_standard_fetch_648 as S


def _data() -> dict:
    with open(S.OUT_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def test_s1_selftest():
    assert S.selftest() == 0


def test_s2_ten_clauses_all_found_with_verbatim_quote():
    d = _data()
    assert d["n_clauses"] == 10 and d["n_found"] == 10
    for key, c in d["clauses"].items():
        assert c["found"] is True, key
        assert c["via"] in ("anchor", "phrase")
        assert len(c["quote"]) >= 60, key
        assert c["offset"] >= 0
        assert c["url"].endswith("#" + c["anchor"])
        # 抽取物不得残留 HTML 标签 / 段号残留
        assert "<" not in c["quote"] and "href=" not in c["quote"]
        assert not re.match(r"^\d+\s", c["quote"]), key


def test_s3_three_standards_downloaded_with_sha256():
    d = _data()
    assert set(d["docs"]) == {"C11", "C17", "C23"}
    for tag, doc in d["docs"].items():
        assert doc["ok"] is True, tag
        assert doc["bytes"] > 100_000
        assert re.fullmatch(r"[0-9a-f]{64}", doc["sha256"]), tag
    assert d["docs"]["C11"]["doc"] == "N1570"
    assert d["docs"]["C17"]["doc"] == "N2310"
    assert d["docs"]["C23"]["doc"] == "N3096"


def test_s4_pdf_limitation_is_registered_not_hidden():
    """C17/C23 是 PDF 且本环境无解析库 ⇒ 必须**显式登记**未抽取，不许假装核对过。"""
    d = _data()
    assert len(d["limitations"]) == 2
    joined = " ".join(d["limitations"])
    assert "PDF" in joined and "未抽取原文" in joined
    assert "sha256" in joined


def test_s5_clause_keys_match_target_fixtures():
    """标准条款与 648 的 10 张卡一一对应（防两边漂移）。"""
    import c_target_648 as T
    keys = {f["clause"] for f in T.FIXTURES}
    assert keys == set(_data()["clauses"]), keys ^ set(_data()["clauses"])
    assert os.path.isfile(S.OUT_MD)
