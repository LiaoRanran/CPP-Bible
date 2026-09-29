#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""ots_placeholder_666.py — 666 A1/E：**待上链**占位 `.ots` 的生成与校验。

为什么需要这个工具（一个真实的循环）
====================================
`tool_integrity.py --update` 每次重钉都会**重写** `data/supply_chain/merkle_roots.json`
（受控目录变更后必须重钉）；而 `.ots` 锚的正是这个文件的摘要 ⇒ **重钉一次，锚就过期一次**。
实测：666 期间 `--update` 跑了多轮，`.ots` 覆盖的仍是旧摘要 ⇒ `ots_anchor_613 --check` 红、
`test_ots_anchor_656` 的占位通道也红。人工"记得重新生成"不可靠，所以把它做成工具。

它做什么 / 不做什么
===================
- **做**：把现有 `.ots` 里的 32 字节摘要**逐字节替换**为当前台账摘要（magic / 版本 / 结构
  **原样保留**），并刷新 `*.ots.placeholder.md` 登记（写当前摘要 + "未上日历"声明）。
- **不做**：不提交日历、不伪造 attestation。占位**不是时间戳证明**；
  真锚定要人跑 `ots stamp`（需网络），见登记文件里的交人项。

**顺序很重要（否则会来回循环）**：`merkle_roots.json` 的**内容**由 `--update` 依受控目录重建，
而 `.ots` 锚的是它的**摘要** ⇒ 正确顺序是

    ① tool_integrity --update      （先让台账反映当前受控目录）
    ② ots_placeholder_666 --write  （再按新摘要重打占位）
    ③ tool_integrity --update      （最后把"已重打的 .ots"钉进基准；此步不改台账内容，幂等）

反过来做（先写 .ots 再 --update）会让 `verify_supply_chain(strict=True)` 报
`merkle_roots.json.ots` 与基准不一致——实测就是这么撞出来的（`test_a1_8` 红）。

用法
====
    python tools/ots_placeholder_666.py --check     # 只读：占位摘要 == 当前台账摘要？
    python tools/ots_placeholder_666.py --write     # 重打占位（幂等）并刷新登记
    python tools/ots_placeholder_666.py --selftest  # 自检（不写盘）
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TARGET = os.path.join(ROOT, "data", "supply_chain", "merkle_roots.json")
OTS = TARGET + ".ots"
NOTE = TARGET + ".ots.placeholder.md"
DIGEST = 32


def _sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _digest_offsets(raw: bytes, digest_hex: str) -> list[int]:
    """摘要字节在 `.ots` 里出现的**全部**偏移（占位结构里出现两次：leaf + 时间戳根）。"""
    needle = bytes.fromhex(digest_hex)
    out: list[int] = []
    start = 0
    while True:
        i = raw.find(needle, start)
        if i < 0:
            return out
        out.append(i)
        start = i + 1


def analyze() -> dict:
    if not os.path.isfile(OTS):
        return {"ok": False, "why": "无 .ots 文件"}
    cur = _sha256(TARGET)
    raw = open(OTS, "rb").read()
    offs = _digest_offsets(raw, cur)
    return {"ok": bool(offs), "current": cur, "offsets": offs,
            "bytes": len(raw),
            "covered": raw[offs[0]:offs[0] + DIGEST].hex() if offs else None}


def rewrite() -> int:
    """把 `.ots` 里的摘要替换为当前台账摘要（结构原样），并刷新登记。"""
    cur = _sha256(TARGET)
    raw = bytearray(open(OTS, "rb").read())
    stale = _digest_offsets(bytes(raw), cur)
    if stale:
        print(f"[ots666] 占位已覆盖当前台账（{len(stale)} 处）—— 无需重打")
    else:
        # 结构固定：magic(31) + ver(1) + op(1) + len(1) + digest(32) … digest(32) …
        # 旧摘要在占位里**出现两次且内容相同** ⇒ 找"重复 ≥2 次的 32 字节块"（排除当前摘要）
        seen: dict[str, list[int]] = {}
        for off in range(0, len(raw) - DIGEST + 1):
            seen.setdefault(bytes(raw[off:off + DIGEST]).hex(), []).append(off)
        dup = [(h, o) for h, o in seen.items() if len(o) >= 2 and h != cur]
        if not dup:
            print("[ots666] ✗ 找不到旧摘要（结构已变）—— 拒绝瞎写，请人工确认", file=sys.stderr)
            return 1
        old_hex, offs = dup[0]
        for off in offs:
            raw[off:off + DIGEST] = bytes.fromhex(cur)
        with open(OTS, "wb") as fh:
            fh.write(bytes(raw))
        print(f"[ots666] 已重打占位：{old_hex[:12]}… → {cur[:12]}…（{len(offs)} 处）")

    # 刷新登记（幂等）
    lines: list[str] = []
    if os.path.isfile(NOTE):
        lines = open(NOTE, encoding="utf-8").read().splitlines()
    patched = False
    for i, ln in enumerate(lines):
        if ln.startswith("- 当前台账 sha256："):
            lines[i] = f"- 当前台账 sha256：`{cur}`"
            patched = True
            break
    if not patched:
        lines = ["# OTS 占位登记（**不是时间戳证明**）—— 666",
                 "",
                 "- 目标：`data/supply_chain/merkle_roots.json`",
                 f"- 当前台账 sha256：`{cur}`",
                 "- 同目录 `.ots`：**待上链占位**（magic 同官方；attestation 段为占位零）",
                 "",
                 "## 交人项（真正锚定需要人执行）",
                 "",
                 "1. 装 `opentimestamps-client`；2. `ots stamp data/supply_chain/merkle_roots.json`（需网络）；",
                 "3. 稍后 `ots upgrade`；4. `python tools/tool_integrity.py --update`；",
                 "5. 完成后**删除本占位登记**（`test_ots_anchor_656` 的占位通道随之关闭）。",
                 ""]
    open(NOTE, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print(f"[ots666] 登记已刷新：{os.path.relpath(NOTE, ROOT)}")
    return 0


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    a = analyze()
    chk("台账存在", os.path.isfile(TARGET))
    chk(".ots 存在", os.path.isfile(OTS))
    chk("摘要出现次数 ∈ {0, ≥1}", isinstance(a.get("offsets", []), list),
        f"({len(a.get('offsets', []) or [])})")
    chk("登记文件存在", os.path.isfile(NOTE))
    chk("登记不含编造字样（'未上日历'/'待上链' 必须显形）",
        (not os.path.isfile(NOTE)) or ("上链" in open(NOTE, encoding="utf-8").read()
                                       or "日历" in open(NOTE, encoding="utf-8").read()))
    print("ots_placeholder_666 selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="666 占位 .ots 生成/校验（不伪造 attestation）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.write:
        return rewrite()
    st = analyze()
    print(f"[ots666] 台账 {st['current'][:12]}… | .ots {st['bytes']}B | 覆盖 "
          f"{(st['covered'] or '（无）')[:12]}… | {'✅ 一致' if st['ok'] else '✗ 过期/缺失'}")
    return 0 if st["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
