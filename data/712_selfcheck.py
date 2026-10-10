# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""712_selfcheck.py — 712 批次自检：把 712 报告里引用的关键数字逐条对回原始证据。

为什么需要它：712 的红线之一是"所有数字必须可追溯，不编造"。批次报告里的数字如果
只靠人抄，就会出现"报告写 55.65%、实测 56.0071%"这类漂移（此前批次踩过）。
本脚本把报告里的**关键主张**与**原始证据**机械对齐，跑一次就能证明报告没有预写未核实数字。

跑法：python data/712_selfcheck.py
退出码：0 = 全部一致；1 = 存在不一致（会打印具体项）
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)  # 仓库根
STEPS = os.path.join(HERE, "712_复现步骤逐条记录.json")

checks: list[tuple[str, object, object, bool]] = []


def ck(label: str, got, want) -> None:
    checks.append((label, got, want, str(got) == str(want)))


def nlines(p: str) -> int:
    n = 0
    with open(p, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.strip():
                n += 1
    return n


def main() -> int:
    if not os.path.exists(STEPS):
        print(f"[712-selfcheck] 缺少证据文件：{STEPS}")
        return 1
    steps = json.load(open(STEPS, encoding="utf-8"))
    by_id = {s["id"]: s for s in steps}

    # ---- A. 复现报告 §1 表的逐行 —----------------------------------------
    ck("16 条命令", len(steps), 16)
    ck("非 0 条数（应为 1）", sum(1 for s in steps if s["exit"] != 0), 1)
    ck("S03 exit", by_id["S03"]["exit"], 0)
    ck("S03 输出 124/0/112",
       "124 条；missing 0；consistent 112" in by_id["S03"]["stdout_tail"], True)
    ck("S04 exit（by design）", by_id["S04"]["exit"], 1)
    ck("S05 清单 15 项 0 失配",
       ("清单 15 项" in by_id["S05"]["stdout_tail"]
        and "失配 0 项" in by_id["S05"]["stdout_tail"]), True)
    ck("S06 exit", by_id["S06"]["exit"], 0)
    ck("S08 exit", by_id["S08"]["exit"], 0)
    ck("S09 PASS", "PASS" in by_id["S09"]["stdout_tail"], True)
    ck("S10 NOT_APPLICABLE", "NOT_APPLICABLE" in by_id["S10"]["stdout_tail"], True)
    ck("S12 exit", by_id["S12"]["exit"], 0)
    ck("S15 n=17", "n=17" in by_id["S15"]["stdout_tail"], True)
    ck("S16 exit", by_id["S16"]["exit"], 0)

    # ---- B. 数字审计器修复报告 §1.2 的真实行数 -----------------------------
    ck("676f local 非空行", nlines(os.path.join(SRC, "data", "a5_676f_matrix_local.jsonl")), 673)
    ck("676f san 非空行", nlines(os.path.join(SRC, "data", "a5_676f_matrix_san.jsonl")), 1054)
    ck("676g ckpt 不存在",
       os.path.exists(os.path.join(SRC, "data", "blindspot_676g_ckpt_san.jsonl")), False)

    # ---- C. 重算源样本数 ---------------------------------------------------
    m676f = json.load(open(os.path.join(SRC, "data", "a5_676f_detection_matrix.json"),
                           encoding="utf-8"))
    ck("676f 重算源 n_samples", m676f["n_samples"], 1137)
    m676g = json.load(open(os.path.join(SRC, "data", "blindspot_676g_detection_matrix.json"),
                           encoding="utf-8"))
    ck("676g 重算源 n_samples", m676g["n_samples"], 1147)

    # ---- D. 修复后的审计产物 ------------------------------------------------
    aud = json.load(open(os.path.join(SRC, "data", "676h_number_audit.json"), encoding="utf-8"))
    ck("676f 组 state", aud["deps"]["676f"]["state"], "partial")
    ck("676g 组 state", aud["deps"]["676g"]["state"], "partial")
    ck("676f 组 ready", aud["deps"]["676f"]["ready"], False)
    ck("检察条数", len(aud["results"]), 130)

    ok = sum(1 for c in checks if c[3])
    print(f"[712-selfcheck] {len(checks)} 项；通过 {ok}；失败 {len(checks) - ok}")
    for label, got, want, good in checks:
        if not good:
            print(f"  [FAIL] {label}: got={got!r} want={want!r}")
    print("[712-selfcheck] " + ("PASS" if ok == len(checks) else "FAIL"))
    return 0 if ok == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
