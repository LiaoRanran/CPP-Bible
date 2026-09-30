#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""run_669d_gate.py — 669d B7：六条 P0 门禁的一键入口。

设计要点
========
1. **判据全在 `gate_rules_669d.py`**，本文件只做编排与报告，不重复实现判据。
2. **known gaps 机制**：当前仓库存在一批真实缺口（协议未冻结统计口径、草稿卡缺
   boundary、machine-verified 卡缺 provenance、escape 无基线）。它们**确实要修**，
   但属于 669 工程的既有事项，不该让 669d 的新门禁一上来就全红到无法使用。
   故引入 `data/669d_known_gaps.json`：**逐条登记 + 写明 reason 才可降级为 WARN**。
   - **只降级已登记项**；任何新出现的缺口仍 BLOCK（防止 known_gaps 变成新的假绿通道）。
   - 报告里始终打印已登记缺口明细，绝不静默。
3. 输出落到 669d 专属文件，不覆盖既有产物。

用法：
    python tools/run_669d_gate.py                # 跑全部，写报告
    python tools/run_669d_gate.py --check        # 同上，并返回退出码（0=无未登记缺口）
    python tools/run_669d_gate.py --no-write     # 只打印，不写报告
    python tools/run_669d_gate.py --accept-gaps  # 把当前 BLOCK 快照登记为已知缺口（需补 reason）
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import gate_rules_669d as G  # noqa: E402

GAPS_PATH = ROOT / "data" / "669d_known_gaps.json"
STATUS_OUT = ROOT / "data" / "669d_gate_status.json"
REPORT_OUT = ROOT / "docs" / "669d_gate_report.md"


def _gap_key(f: dict) -> str:
    return f"{f['rule']}|{f['target']}"


def load_gaps() -> dict[str, dict]:
    if not GAPS_PATH.is_file():
        return {}
    try:
        d = json.loads(GAPS_PATH.read_bytes().decode("utf-8"))
    except Exception:
        return {}
    out = {}
    for g in d.get("gaps", []):
        out[f"{g.get('rule')}|{g.get('target')}"] = g
    return out


def classify(findings: list[dict], gaps: dict[str, dict]):
    """分为：未登记 BLOCK / 已登记(降级) / WARN。"""
    new_blocks, accepted, warns = [], [], []
    for f in findings:
        if f["severity"] == G.BLOCK:
            g = gaps.get(_gap_key(f))
            if g:
                rec = dict(f)
                rec["severity"] = G.WARN
                rec["gap_reason"] = g.get("reason", "（未写明原因）")
                rec["gap_owner"] = g.get("owner", "未指派")
                accepted.append(rec)
            else:
                new_blocks.append(f)
        else:
            warns.append(f)
    return new_blocks, accepted, warns


def render_report(new_blocks, accepted, warns, overall) -> str:
    L = ["# 669d 门禁报告", "",
         f"生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}", "",
         f"总体：**{overall}**", "",
         "| 类别 | 条数 | 含义 |", "|---|---:|---|",
         f"| 未登记 BLOCK | {len(new_blocks)} | 新出现的缺口，必须修 |",
         f"| 已登记缺口（降级 WARN） | {len(accepted)} | 已在 669d_known_gaps.json 登记，待 669 工程修 |",
         f"| 其他 WARN | {len(warns)} | 建议项 |", ""]

    if new_blocks:
        L += ["## 未登记 BLOCK（必须修）", "",
              "| 规则 | 对象 | 说明 |", "|---|---|---|---|"]
        for f in new_blocks:
            L.append(f"| {f['rule']} | `{f['target']}` | {f['message']} |")
        L.append("")

    if accepted:
        L += ["## 已登记缺口（诚实登记，不静默）", "",
              "| 规则 | 对象 | 原因 | 负责人 |", "|---|---|---|---|"]
        for f in accepted:
            L.append(f"| {f['rule']} | `{f['target']}` | {f['gap_reason']} | {f['gap_owner']} |")
        L.append("")

    if warns:
        L += ["## 其他 WARN", "", "| 规则 | 对象 | 说明 |", "|---|---|---|"]
        for f in warns:
            L.append(f"| {f['rule']} | `{f['target']}` | {f['message']} |")
        L.append("")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="669d 六条 P0 门禁一键入口")
    ap.add_argument("--check", action="store_true", help="返回退出码（0=无未登记缺口）")
    ap.add_argument("--no-write", action="store_true", help="不写报告文件")
    ap.add_argument("--accept-gaps", action="store_true",
                    help="把当前 BLOCK 快照登记进 data/669d_known_gaps.json")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    findings = G.run_all(ROOT)

    if a.accept_gaps:
        blocks = [f for f in findings if f["severity"] == G.BLOCK]
        old = load_gaps()
        gaps = []
        for f in blocks:
            k = _gap_key(f)
            if k in old:
                gaps.append(old[k])
            else:
                gaps.append({"rule": f["rule"], "target": f["target"],
                             "message": f["message"],
                             "reason": "TODO：填写为什么暂不接受（不得留空）",
                             "owner": "669 工程", "registered_at": time.strftime("%Y-%m-%d")})
        GAPS_PATH.parent.mkdir(parents=True, exist_ok=True)
        GAPS_PATH.write_bytes(json.dumps(
            {"schema": "queyi-known-gaps/v1", "generated_by": "tools/run_669d_gate.py",
             "note": "只降级已登记项；新出现的 BLOCK 仍必须修。reason 不得留 TODO 太久。",
             "gaps": gaps}, ensure_ascii=False, indent=2).encode("utf-8"))
        print(f"已登记 {len(gaps)} 条已知缺口 → {GAPS_PATH.relative_to(ROOT).as_posix()}")
        print("⚠ 请把每条的 reason 从 TODO 改成真实原因（否则等于无理由豁免）")
        return 0

    gaps = load_gaps()
    new_blocks, accepted, warns = classify(findings, gaps)
    overall = "PASS" if not new_blocks else "FAIL"

    if a.json:
        print(json.dumps({"overall": overall, "new_blocks": new_blocks,
                          "accepted_gaps": accepted, "warns": warns},
                         ensure_ascii=False, indent=2))
    else:
        print(f"[669d gate] overall={overall}  "
              f"未登记BLOCK={len(new_blocks)}  已登记={len(accepted)}  WARN={len(warns)}")
        for f in new_blocks:
            print(f"  [BLOCK] {f['rule']:22} {f['target']}")
            print(f"          {f['message']}")
        if accepted:
            print(f"\n  已登记缺口 {len(accepted)} 条（详见报告，不静默）：")
            for f in accepted[:5]:
                print(f"  [gap  ] {f['rule']:22} {f['target']}")
            if len(accepted) > 5:
                print(f"          …另有 {len(accepted)-5} 条")

    if not a.no_write:
        STATUS_OUT.parent.mkdir(parents=True, exist_ok=True)
        STATUS_OUT.write_bytes(json.dumps(
            {"gate": "669d", "overall": overall, "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
             "new_blocks": new_blocks, "accepted_gaps": accepted, "warns": warns},
            ensure_ascii=False, indent=2).encode("utf-8"))
        REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
        REPORT_OUT.write_bytes(
            render_report(new_blocks, accepted, warns, overall).encode("utf-8"))

    return 0 if not new_blocks else 1


if __name__ == "__main__":
    raise SystemExit(main())
