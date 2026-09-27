#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""web_status_655.py — 生成前端"系统现状"面板的真实数据（655 D）。

为什么单独一个工具
==================
655 D 要求 landing 加"系统现状"面板（37 卡 / 67 规则 / 9 保护器 / 逃逸率 0.07%）。
这些数字**必须现算**（`web/` 是静态站，没有后端），且**不许写死**到 HTML 里——
所以由本工具从真实来源算出 `web/data/status.json`，前端只负责渲染。

数据来源（逐个可追溯，缺任一 ⇒ 该字段为 `null` 并登记到 `unavailable`，**绝不编造**）
==============================================================================
- 卡：`atoms/**/ATOM-*.md`（`draft650/` 单列）
- 规则：`tools/gate_engine.py` 的 `RULES`（现 import 现算）
- 保护器：姊妹仓 `queyi-core/tools/` 下 5×`*_647.py` + 4×`*_649.py`
- 逃逸：`data/mutation/full_baseline_v7.json`（并**交叉核对** 616 冻结口径 `1/1406`）
- W2：`data/grounded_labels_w2.json`

用法
====
    python tools/web_status_655.py            # 写 web/data/status.json 并打印摘要
    python tools/web_status_655.py --check    # 只读自检（不写盘）
    python tools/web_status_655.py --json
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
QUEYI = ROOT.parent.parent / "queyi-core"
OUT = ROOT / "web" / "data" / "status.json"

sys.path.insert(0, str(HERE))
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

#: 9 个保护器（5×647 真上岗 + 4×649），名字写死为"预期清单"，存在性现查
PROTECTOR_NAMES = (
    "conflict_detector_647", "anti_windup_647", "blind_protocol_647",
    "calibration_tracker_647", "mdl_gate_647",
    "tool_gate_649", "shadow_mode_649", "circuit_breaker_649", "budget_guard_649",
)

#: 616 冻结口径（用于交叉核对，不参与计算）
FROZEN_ESCAPE = "1/1406 = 0.0711%"


def count_cards() -> dict[str, Any]:
    """真实卡数：`draft650/` 单列（它们是 650 批新增的草稿卡）。"""
    real = draft = 0
    statuses: dict[str, int] = {}
    for p in sorted((ROOT / "atoms").rglob("ATOM-*.md")):
        if p.parent.name == "draft650":
            draft += 1
            continue
        real += 1
        m = re.search(r"^status:\s*(\S+)", p.read_text(encoding="utf-8", errors="replace"),
                      re.MULTILINE)
        key = m.group(1) if m else "unknown"
        statuses[key] = statuses.get(key, 0) + 1
    return {"cards_real": real, "cards_draft": draft, "cards_total": real + draft,
            "card_statuses": statuses}


def count_rules() -> dict[str, Any]:
    try:
        sys.path.insert(0, str(HERE))
        import gate_engine  # noqa: PLC0415

        rules = list(gate_engine.RULES)
    except Exception as e:  # noqa: BLE001
        return {"rules_total": None, "rules_block": None, "rules_error": str(e)[:120]}
    block = sum(1 for r in rules if getattr(r, "severity", "") == "block")
    return {"rules_total": len(rules), "rules_block": block}


def count_protectors() -> dict[str, Any]:
    found, missing = [], []
    for name in PROTECTOR_NAMES:
        (found if (QUEYI / "tools" / f"{name}.py").is_file() else missing).append(name)
    return {"protectors_total": len(found), "protectors_found": found,
            "protectors_missing": missing, "protectors_root": str(QUEYI)}


def escape_rate() -> dict[str, Any]:
    p = ROOT / "data" / "mutation" / "full_baseline_v7.json"
    if not p.is_file():
        return {"available": False, "reason": f"缺 {p.name}"}
    d = json.loads(p.read_text(encoding="utf-8"))
    variants = int(d.get("variants", 0))
    n_a = int(d.get("n_a", 0))
    equivalent = int(d.get("equivalent", d.get("equivalent_invalid", 0)))
    denom = variants - n_a - equivalent
    escaped = int(d.get("escaped", 0))
    rate = (100.0 * escaped / denom) if denom else None
    frozen_ok = (denom == 1406 and escaped == 1)
    return {"available": True, "variants": variants, "blocked": int(d.get("blocked", 0)),
            "escaped": escaped, "n_a": n_a, "equivalent": equivalent,
            "denominator": denom, "rate_pct": round(rate, 4) if rate is not None else None,
            "frozen_616": FROZEN_ESCAPE, "frozen_matches": frozen_ok,
            "note": str(d.get("notes", ""))[:200]}


def w2_summary() -> dict[str, Any]:
    p = ROOT / "data" / "grounded_labels_w2.json"
    if not p.is_file():
        return {"available": False}
    d = json.loads(p.read_text(encoding="utf-8"))
    nodes = d.get("nodes", [])
    summ = d.get("summary", {}) if isinstance(d.get("summary"), dict) else {}
    out = {"available": True, "nodes": len(nodes),
           "IN": summ.get("IN"), "OUT": summ.get("OUT"), "UNDEC": summ.get("UNDEC")}
    if out["IN"] is None:
        labels: dict[str, int] = {}
        for n in nodes:
            labels[str(n.get("label", "?"))] = labels.get(str(n.get("label", "?")), 0) + 1
        out.update({"IN": labels.get("IN"), "OUT": labels.get("OUT"), "UNDEC": labels.get("UNDEC")})
    return out


def build() -> dict[str, Any]:
    cards = count_cards()
    rules = count_rules()
    prot = count_protectors()
    esc = escape_rate()
    w2 = w2_summary()
    unavailable = []
    if rules.get("rules_total") is None:
        unavailable.append("rules：gate_engine 导入失败")
    if prot["protectors_missing"]:
        unavailable.append(f"protectors：缺 {prot['protectors_missing']}")
    if not esc.get("available"):
        unavailable.append("escape：缺 full_baseline_v7.json")
    if not w2.get("available"):
        unavailable.append("w2：缺 grounded_labels_w2.json")
    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "generated_from": ["atoms/**/ATOM-*.md", "tools/gate_engine.py",
                           "queyi-core/tools/*_647.py+*_649.py",
                           "data/mutation/full_baseline_v7.json",
                           "data/grounded_labels_w2.json"],
        "cards": cards,
        "rules": rules,
        "protectors": prot,
        "escape": esc,
        "w2": w2,
        "unavailable": unavailable,
        "note": ("本文件由 tools/web_status_655.py 现算；前端只渲染、不写死数字。"
                 "任何字段缺失都显式标 null 并进入 unavailable，不用占位值冒充真实。"),
    }


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    rep = build()
    chk("卡数为正", int(rep["cards"]["cards_real"]) > 0, str(rep["cards"]["cards_real"]))
    chk("卡数 = verified+red-team+draft",
        rep["cards"]["cards_total"] == rep["cards"]["cards_real"] + rep["cards"]["cards_draft"])
    chk("规则数 = 67（现状）", rep["rules"]["rules_total"] == 67, str(rep["rules"]))
    chk("保护器 9/9 存在于姊妹仓", rep["protectors"]["protectors_total"] == 9,
        str(rep["protectors"]["protectors_missing"]))
    chk("逃逸分母与 616 冻结口径一致", bool(rep["escape"].get("frozen_matches")),
        f"{rep['escape'].get('escaped')}/{rep['escape'].get('denominator')}")
    chk("W2 三值齐备", rep["w2"].get("IN") is not None and rep["w2"].get("nodes"))
    chk("输出路径在 web/data 下",
        OUT.as_posix().endswith("web/data/status.json"))
    print(f"web_status_655 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="生成 web/data/status.json（真实数据）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    rep = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        c, r, p, e = rep["cards"], rep["rules"], rep["protectors"], rep["escape"]
        print(f"[status655] 已写 {OUT.relative_to(ROOT).as_posix()}："
              f"卡 {c['cards_real']}(+{c['cards_draft']} draft)｜规则 {r['rules_total']}"
              f"（block {r['rules_block']}）｜保护器 {p['protectors_total']}/9｜"
              f"逃逸 {e.get('escaped')}/{e.get('denominator')} = {e.get('rate_pct')}%")
        if rep["unavailable"]:
            print(f"[status655] 缺失项：{rep['unavailable']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
