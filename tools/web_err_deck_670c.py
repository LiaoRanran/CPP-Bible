#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""web_err_deck_670c.py — 670c A1：把 665 B1 的 16 张机器卡导出成学习页的「错例牌组」。

为什么单独出一份文件
====================
学习页要展示「错误断言 → 反例代码 → sanitizer 输出 → 正确断言」四段，
其中「反例代码」（fixtures/ig-NN.cpp 原文）不在任何 web/data 文件里，
而 data/cards_665/ 是只读输入。本工具只读输入、只写 web/data/，不碰受控目录。

诚实口径（关键，不许美化）
==========================
* 机器卡的 assertion_under_test 是【被反例推翻的错误断言】（b_refuted_664=true），
  不是"已核准知识"；导出时字段名直接用 wrong_assertion，免得前端误读。
* 机器卡【没有】"正确断言"字段。本工具用 counterexample 文本作为正确行为的陈述，
  并写 correct_source = "counterexample-text/machine-unsigned" 登记来源；
  另带 needs_review=True 与 signed=false，学习页必须显示"机器生成·未签"。
* measured_out 原样透传（真机复跑输出），不截断、不修饰。

用法
====
    python tools/web_err_deck_670c.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "cards_665" / "index_665.json"
OUT = ROOT / "web" / "data" / "err_deck_670c.json"
SCHEMA = "queyi-err-deck-web/v1"


def build() -> dict:
    if not INDEX.is_file():
        raise SystemExit("missing source: " + str(INDEX))
    src = json.loads(INDEX.read_text(encoding="utf-8"))
    cards = []
    for c in src.get("cards", []):
        rel = str(c.get("fixture_rel") or "").strip().replace(chr(92), "/")
        code = ""
        if rel:
            fp = ROOT.joinpath(*rel.split("/"))
            if fp.is_file():
                code = fp.read_text(encoding="utf-8", errors="replace")
        ctr = c.get("counterexample") or ""
        cards.append({
            "id": c.get("id"),
            "source_id": c.get("source_id"),
            "detector": c.get("detector") or "",
            "expect": c.get("expect") or "",
            "verdict": c.get("verdict") or "",
            "four_state": c.get("four_state") or "unknown",
            "four_state_reason": c.get("four_state_reason") or "",
            "signature": c.get("signature") or "",
            "note": c.get("note") or "",
            "support_reason": c.get("support_reason") or "",
            "boundary": c.get("boundary") or {},
            "wrong_assertion": c.get("assertion_under_test") or "",
            "refuted": bool(c.get("b_refuted_664", c.get("verdict") == "catch")),
            "counterexample": ctr,
            "fixture_path": rel,
            "fixture_code": code,
            "fixture_sha256": c.get("fixture_sha256") or "",
            "sanitizer_output": (c.get("measured_out") or "").strip(),
            "measured_at": c.get("measured_at") or "",
            "correct_assertion": ctr,
            "correct_source": "counterexample-text/machine-unsigned",
            "needs_review": True,
        })
    return {
        "schema": SCHEMA,
        "generated_by": "tools/web_err_deck_670c.py",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "data/cards_665/index_665.json + data/cards_665/fixtures/",
        "total": len(cards),
        "signed": False,
        "note": "机器卡（无人签），不进 cards.json 台账；correct_assertion 由 counterexample 文本派生，见 correct_source。",
        "cards": cards,
    }


def main() -> int:
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + chr(10), encoding="utf-8")
    n_code = sum(1 for c in data["cards"] if c["fixture_code"])
    n_out = sum(1 for c in data["cards"] if c["sanitizer_output"])
    print("wrote web/data/err_deck_670c.json: %d cards, %d with fixture code, %d with sanitizer output"
          % (data["total"], n_code, n_out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
