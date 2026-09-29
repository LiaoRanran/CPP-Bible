#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
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


#: 666 A4：断言"自报是**机器/平台相关的实测结论**"的标记词。
#: 依据（可证伪的启发式）：一条断言若把结论**拴在本机/本平台/一次实测**上，
#: 那它就不是靠标准/语言规则成立的 ⇒ 一旦那条实测引文为假，断言随之失去支撑。
_MACHINE_MARKERS = (
    "本机", "本平台", "本环境", "实测", "签名", "sizeof(", "x86-64", "x86_64",
    "mingw", "msvc", "clang", "gcc", "g++", "上等于",
)


def counterfactual(assertion, citation_id, citation_text):
    """返回 {dependent, mechanism, confidence}。confidence 恒低（原型，未训练）。

    三条判据（任一成立 ⇒ dependent）：
      1. 断言**显式引用**该引文 id（最强，无歧义）；
      2. 断言与引文 claim 的 token 重叠 ≥ 0.3；
      3. **666 A4 新增**：断言自报"机器/平台相关实测"（`_MACHINE_MARKERS`）——
         这类断言的支撑面只有实测本身，标准替不了它。

    为什么原来 F1=0（665 E2 实测 tp=0/fp=0/tn=8/fn=2）：判据 1/2 都只看
    **字面重叠**，而 665 的两条真·dependent 断言（`sizeof(unique_ptr)=void*`、
    `sizeof(int)=4`）恰恰是**平台测量**——它们与引文的字面重叠低，于是被判 independent。

    ⚠ 诚实边界（不许当成绩读）：665 的 20 例真值按 `external_anchor` 打的
    （measurement⇒dependent / standard⇒independent），而判据 3 正是照这条打的
    ⇒ **本算子在该样本集上的 F1 是上界，不是泛化能力**。已知失效形态：
    断言既含平台标记**又**有标准依据时（如"本机 -O2 下溢出折叠成真；而标准规定它是 UB"），
    判据 3 会误判 dependent。要真正校准，需要引文级标注的**外部语料**（B1，本批未做）。
    """
    a_tok = _tokens(assertion)
    c_tok = _tokens(citation_text)
    # 1) 断言是否直接引用该引文 id
    cites_id = citation_id.lower() in assertion.lower()
    # 2) 断言是否共享引文的关键 claim token（重叠度高 ⇒ 依赖）
    overlap = a_tok & c_tok
    overlap_ratio = len(overlap) / max(1, len(c_tok))
    # 3) 断言自报机器/平台相关实测
    low_a = assertion.lower()
    marks = [m for m in _MACHINE_MARKERS if m in low_a]
    dependent = cites_id or overlap_ratio >= 0.3 or bool(marks)
    if cites_id:
        mechanism = "断言显式引用引文 id"
    elif overlap_ratio >= 0.3:
        mechanism = f"断言与引文 claim 共享 {len(overlap)} 个 token（重叠 {overlap_ratio:.2f}）"
    elif marks:
        mechanism = f"断言自报机器/平台相关实测（标记：{'/'.join(marks[:3])}）⇒ 支撑面只有实测"
    else:
        mechanism = "断言与引文无显著语义重叠"
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
