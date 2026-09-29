#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""web_ig_cards_665.py — 665 G1/G2：把 665 B1 的机器卡**如实**送进前端。

为什么不直接改 `web/data/status.json`
=====================================
那个文件由 `tools/web_status_655.py` 现算，手改就破坏了"数字可复算"这条性质。
本工具在它跑完之后**追加**两个字段（不覆盖它算出的任何字段），并另写一份卡索引。

红线（写在代码里，免得后人以为前端多出来的卡是"已核准知识"）
==============================================================
* IG 卡是 `status=machine-derived`，**无人签** ⇒ 前端必须标"机器卡·待人签"，
  且**不进** `web/data/cards.json`（那是学会系统用的台账，只收 atom 级卡）。
* 只统计、不美化：`four_state_dist` 原样透传（含 unknown 4 张）。

用法
====
    python tools/web_status_655.py          # 先现算主 status
    python tools/web_ig_cards_665.py        # 再追加 665 机器卡段落
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "web" / "data" / "status.json"
INDEX = ROOT / "data" / "cards_665" / "index_665.json"
OUT_CARDS = ROOT / "web" / "data" / "ig_cards_665.json"


def main() -> int:
    if not INDEX.is_file():
        print("[web_ig_cards_665] 缺 data/cards_665/index_665.json（先跑 tools/ig_cards_665.py --build）")
        return 1
    if not STATUS.is_file():
        print("[web_ig_cards_665] 缺 web/data/status.json（先跑 tools/web_status_655.py）")
        return 1
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    st = json.loads(STATUS.read_text(encoding="utf-8"))

    cards = [{"id": r["id"], "source_id": r["source_id"], "detector": r.get("detector"),
              "verdict": r["verdict"], "four_state": r["four_state"],
              "signature": r["signature"], "fixture": r["fixture_rel"],
              "measured_out": r.get("measured_out", ""),
              "assertion": r.get("assertion_under_test", ""),
              "counterexample": r.get("counterexample", ""),
              "needs_review": True}
             for r in idx["cards"]]
    OUT_CARDS.write_text(json.dumps({
        "schema": "queyi-ig-cards-web/v1",
        "generated_by": "tools/web_ig_cards_665.py",
        "generated_at": time.strftime("%Y-%m-%d"),
        "total": len(cards),
        "status": "machine-derived（无人签）",
        "note": ("这批卡是 665 B1 从 664 独立生成批次拆出来的**机器卡**："
                 "证据来自本机/WSL 真机复跑，但**没有人签过**，"
                 "因此**不进**学会系统的 cards.json 台账。"),
        "cards": cards,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    st["ig_cards_665"] = {
        "total": idx["total"],
        "verdict_dist": idx["verdict_dist"],
        "four_state_dist": idx["four_state_dist"],
        "agree_with_664": idx["agree_with_664"],
        "status": "机器卡 · machine-derived（无人签，不算 verified）",
        "source": "data/cards_665/index_665.json",
        "web_index": "web/data/ig_cards_665.json",
        "recheck_cmd": "python tools/ig_cards_665.py --check",
    }
    st["note"] = (st.get("note", "") +
                  " 665 G1 追加：ig_cards_665 为**机器卡**（无人签），与 atom 卡分开计数，不混入口径。")
    STATUS.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[web_ig_cards_665] status.json 追加 ig_cards_665={st['ig_cards_665']['total']} 张；"
          f"已写 {OUT_CARDS.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
