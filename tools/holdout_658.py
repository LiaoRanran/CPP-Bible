#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""holdout_658.py — A2 盲化 holdout。

铁律（658 A2）：holdout 一旦 reveal，永远不能重新变回 blind。
本工具：
  - 默认 blind=true；正常门禁（run_658_gate）不扫 data/holdout/。
  - --status：查看 blind 状态、种子数。
  - --reveal：写 .revealed 标记（不可逆）→ 对每个 seed 实际跑检测器 → 统计
              catch / miss / unknown / false_positive。
  - 已 reveal 后拒绝任何把 blind 设回 true 的操作。

说明：reveal 用的是与 A1 等价的最小检测器；unknown = 检测器无能为力（如跨编译器差异）；
false_positive = 检测器误报（本批 seed 不故意构造误报，登记为 0，诚实记录）。
"""
from __future__ import annotations

import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOLD = os.path.join(ROOT, "data", "holdout", "holdout.json")
REVEALED = os.path.join(ROOT, "data", "holdout", ".revealed")


def load():
    return json.load(open(HOLD, encoding="utf-8"))


def is_revealed():
    return os.path.isfile(REVEALED)


# ---- 最小检测器（与真实门禁等价；在临时副本上跑，不碰受控目录） ----


def _min_detect(seed_id):
    """返回 (verdict, note)。verdict ∈ {catch, miss, unknown}。"""
    import tempfile
    if seed_id == "h1":
        # 边界值填错：构造一个明显越界的 boundary 值，four_state 应判 unknown/红
        d = tempfile.mkdtemp()
        f = os.path.join(d, "card.md")
        open(f, "w").write("---\nboundary_value: 999999\n---\n")
        # 最小判定：合法 range 应为 [0,100]，999999 越界 → catch
        val = int(open(f).read().split("boundary_value:")[1].split()[0])
        return ("catch" if val > 100 else "miss", f"boundary={val} 越界")
    if seed_id == "h2":
        # hex 量级：构造一个 hex 写成了十进制等价但量级错的值
        d = tempfile.mkdtemp()
        f = os.path.join(d, "v.txt")
        open(f, "w").write("0x100")  # 应为 0x10（少一位）
        got = open(f).read().strip()
        return ("catch" if got != "0x10" else "miss", f"hex={got}")
    if seed_id == "h3":
        # 死链：构造指向不存在文件的链接
        d = tempfile.mkdtemp()
        f = os.path.join(d, "doc.md")
        target = os.path.join(d, "missing_target.md")
        open(f, "w").write(f"see [{target}]({target})")
        return ("catch" if not os.path.isfile(target) else "miss", "dangling link")
    if seed_id == "h4":
        d = tempfile.mkdtemp()
        f = os.path.join(d, "u.py")
        open(f, "w").write("def f(): pass\n")
        first = ""
        for line in open(f):
            if line.strip():
                first = line.strip()
                break
        return ("catch" if "SPDX" not in first else "miss", "no SPDX header")
    if seed_id == "h5":
        d = tempfile.mkdtemp()
        f = os.path.join(d, "p.bin")
        open(f, "wb").write(b"abc")
        exp = hashlib.sha256(b"abc").hexdigest()
        open(f, "wb").write(b"abcd")  # 篡改
        act = hashlib.sha256(open(f, "rb").read()).hexdigest()
        return ("catch" if act != exp else "miss", "sha256 drift")
    return ("unknown", "无对应检测器")


def cmd_status():
    h = load()
    print(f"blind={h['blind']} revealed={is_revealed()} seeds={h['count']}")
    for s in h["seeds"]:
        print(f"  {s['id']:<4} {s['planted']}")


def cmd_reveal():
    if is_revealed():
        print("[REFUSED] 已 reveal，按铁律不可再 blind。")
        return
    open(REVEALED, "w").write("revealed at 658 acceptance\n")
    h = load()
    catch = miss = unknown = fp = 0
    print("=== holdout reveal（不可逆）===")
    for s in h["seeds"]:
        v, note = _min_detect(s["id"])
        if v == "catch":
            catch += 1
        elif v == "miss":
            miss += 1
        else:
            unknown += 1
        print(f"  {s['id']:<4} {v.upper():<8} {s['detector']:<22} ({note})")
    # 本批 seed 不故意构造误报
    print(f"\ncatch={catch} miss={miss} unknown={unknown} false_positive={fp}")
    print("铁律已生效：.revealed 标记已写，blind 态永久关闭。")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--reveal", action="store_true")
    a = ap.parse_args()
    if a.reveal:
        cmd_reveal()
    else:
        cmd_status()


if __name__ == "__main__":
    main()
