# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tools/test_a11y_jsdom_672d.py — jsdom 渲染后审计工具（672d C）的验收测试（≥10 断言）。

三类断言：
  1. 工具能跑：node / jsdom 入口可解析，audit(['index','cards']) 出全字段的 JSON；
  2. 渲染真实发生：cards 的 DOM 节点数渲染后**显著变多**（卡库网格是 JS 渲染的）；
  3. 规则不空转：构造一个带 `缺 alt` / `重复 id` 的坏页面喂给同一套规则，
     必须报 critical —— 防止"8 页 0 问题"是**因为检查根本没跑**的假绿。
"""
from __future__ import annotations

import json
import os
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

import a11y_audit_jsdom_672d as J  # noqa: E402
import a11y_audit_670c4 as STATIC  # noqa: E402


def test_node_and_jsdom_resolvable():
    node = J.find_node()
    assert node, "找不到 node（PATH / NODE_BIN）"
    entry = J.find_jsdom_entry(node)
    assert entry and os.path.isfile(entry), f"jsdom 入口不可用: {entry}"


def test_focus_ring_check_structure_and_ok():
    res = J.focus_ring_check()
    assert res["ok"] is True, f"焦点环 CSS 检查失败: {res['issues']}"
    assert "css/a11y.css" in res["css_files"], "焦点环检查应覆盖 a11y.css"
    assert isinstance(res["issues"], list)


def test_audit_two_pages_full_coverage():
    res = J.audit(["index", "cards"])
    assert res["coverage"] == "jsdom_rendered", "coverage 声明缺失"
    assert res["js_rendered_dom_audited"] is True
    assert len(res["pages"]) == 2, f"应审计 2 页，实际 {len(res['pages'])}"
    assert len(res["limitations"]) >= 5, "局限登记不足（jsdom 不是真实浏览器等）"
    assert isinstance(res["uncaught"], list)
    assert res["critical_total"] == 0, \
        f"出现 critical：{[i for p in res['pages'] for i in p['issues'] if i['severity'] == 'critical']}"


def test_rendering_actually_happens():
    """渲染真实发生：JS 往 DOM 里加了大量节点（cards 的卡库网格约 +1400 节点）。"""
    res = J.audit(["index", "cards"])
    by_page = {p["page"]: p for p in res["pages"]}
    for pg in ("index.html", "cards.html"):
        p = by_page[pg]
        assert p["nodes_rendered"] > p["nodes_static"], \
            f"{pg}: 渲染后节点数没变（{p['nodes_static']}→{p['nodes_rendered']}），jsdom boot 没生效"
        assert p["nodes_added_by_js"] > 20, f"{pg}: JS 新增节点过少（{p['nodes_added_by_js']}）"
        ok_modules = [m for m in p["modules"] if m["ok"]]
        assert ok_modules, f"{pg}: 没有任何模块执行成功"
    assert by_page["cards.html"]["nodes_added_by_js"] > by_page["index.html"]["nodes_added_by_js"], \
        "卡库网格的 JS 渲染量应显著大于首页"


def test_rules_not_vacuous():
    """规则不空转：坏页面喂进同一套判据，必须报 critical（否则"0 问题"无意义）。"""
    bad = os.path.join(ROOT, "data", "_tmp_672d_bad_page.html")
    try:
        with open(bad, "w", encoding="utf-8") as fh:
            fh.write("<!DOCTYPE html><html><head><meta name='viewport' content='w=1'></head><body>"
                     "<main><img src='x.png'>"                       # 缺 alt → critical
                     "<p id='dup'>a</p><p id='dup'>b</p>"            # 重复 id → critical
                     "<a href='t.html'></a>"                          # 空链接 → critical
                     "</main></body></html>")
        res = STATIC.audit_page(bad)
        rules = {i["rule"] for i in res["issues"] if i["severity"] == "critical"}
        assert "img-alt" in rules, f"缺 alt 未被抓到: {rules}"
        assert "dup-id" in rules, f"重复 id 未被抓到: {rules}"
        assert res["counts"]["critical"] >= 3, f"critical 计数异常: {res['counts']}"
    finally:
        if os.path.isfile(bad):
            os.remove(bad)


def test_json_serializable():
    """产物必须能整体 JSON 序列化（stdout --json 模式的契约）。"""
    res = J.audit(["index"])
    text = json.dumps(res, ensure_ascii=False)
    assert '"coverage"' in text and "jsdom_rendered" in text
