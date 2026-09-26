"""644 D1 标准文档获取器单测（F1-1..F1-4）。"""
from __future__ import annotations

import evidence_base_644 as base
import standard_fetcher_644 as d1


# F1-1：parse_search_results 抽取 top 3
def test_parse_search_results():
    html = '<a href="/w/cpp/a" title="x">a</a><a href="/w/cpp/b">b</a><a href="/other">c</a><a href="/w/cpp/d">d</a>'
    links = d1.parse_search_results(html)
    assert len(links) == 3
    assert all("/w/" in ln for ln in links)


# F1-2：网络降级（无效 host → (None, error) 不崩溃）
def test_network_degradation():
    txt, err = d1.fetch_url("http://127.0.0.1:0/impossible")
    assert txt is None and err is not None


# F1-3：acquire 结构正确，网络受限时不写 store
def test_acquire_no_write():
    before = len(base.iter_stored())
    r = d1.acquire("nullptr")
    after = len(base.iter_stored())
    assert before == after
    assert "ok" in r and "fetched" in r and "errors" in r


# F1-4：selftest 通过
def test_selftest():
    assert d1.selftest() == 0
