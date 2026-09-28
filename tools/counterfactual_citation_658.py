#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""counterfactual_citation_658.py — H2 反事实引文算子（最小原型）。

问题（v41）：打开 RAG 下游验证器位置。给定一条断言 + 一条引文，
问"如果引文是假的，断言还成立吗？"

原型范围（658 H2）：**不追求准确率，先跑通流程**。
用最小启发式：若断言文本显式提及引文的关键 claim token，则断言"依赖"该引文 →
反事实（引文为假）下断言变不确定。否则视为"独立"。

用法：
    python tools/counterfactual_citation_658.py --assertion "X 因为 Cit-7 证明 Y" --citation-id Cit-7 --citation-text "Y 成立"
    python tools/counterfactual_citation_658.py --demo
"""
from __future__ import annotations
import argparse
import json
import re


def _tokens(text):
    return set(re.findall(r"[一-鿿a-zA-Z0-9_]+", text.lower()))


def counterfactual(assertion, citation_id, citation_text):
    """返回 {dependent, mechanism, confidence}。confidence 恒低（原型，未训练）。"""
    a_tok = _tokens(assertion)
    c_tok = _tokens(citation_text)
    # 1) 断言是否直接引用该引文 id
    cites_id = citation_id.lower() in assertion.lower()
    # 2) 断言是否共享引文的关键 claim token（重叠度高 ⇒ 依赖）
    overlap = a_tok & c_tok
    overlap_ratio = len(overlap) / max(1, len(c_tok))
    dependent = cites_id or overlap_ratio >= 0.3
    mechanism = (
        "断言显式引用引文 id" if cites_id
        else f"断言与引文 claim 共享 {len(overlap)} 个 token（重叠 {overlap_ratio:.2f}）"
        if dependent else "断言与引文无显著语义重叠"
    )
    return {
        "citation_id": citation_id,
        "dependent": dependent,
        "mechanism": mechanism,
        "verdict_if_citation_false": "UNCERTAIN（需重新取证）" if dependent else "仍成立（独立）",
        "confidence": "low(prototype)",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--assertion")
    ap.add_argument("--citation-id")
    ap.add_argument("--citation-text")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo or not a.assertion:
        cases = [
            ("std::atomic 无锁因 Cit-3 证其顺序一致", "Cit-3", "顺序一致性由 C++ 标准保证"),
            ("该卡结论基于作者直觉", "Cit-9", "UB 在 -O2 下被优化掉"),
        ]
        for ast, cid, ctext in cases:
            print(json.dumps(counterfactual(ast, cid, ctext), ensure_ascii=False, indent=2))
        return
    print(json.dumps(counterfactual(a.assertion, a.citation_id, a.citation_text),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
