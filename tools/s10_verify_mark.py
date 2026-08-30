#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
s10_verify_mark.py — §10 验证标记「半自动分诊」注入器（方向 B 落地，E12）
================================================================================
背景
----
E11 侦察（verification_audit.py）判定：147 主章中 74 含验证标记，其余「高风险」
章 **73 章零 `[VERIFIED]/[UNVERIFIED]/[NEEDS-VERIFY]` 标记**。§10 + 宪章 §0 硬规则：
「无法实际验证的内容一律标 `[UNVERIFIED]`，绝不伪装成已验证」；`[VERIFIED]` 须
「已编译/运行/UB sanitizer/反汇编/跨编译器/跨标准版本实际复现」。

批量无脑打标违反 §0（平均用力 / 伪验证）。本工具按「**是否有机器可验证复现链**」
做有依据、可复核的分诊：

  复现链判定（确定性）：
    - D5 基准：章内含 `基准源码见库根 `_bench_d5_X.cpp`` 声明（E11 已证 115/115
      全过 GCC 15.3.0 编译门禁）→ 性能断言已编译/运行复现。
    - ASM 证据：章内含 ```asm 围栏块（book_asm_freshness 已证为真实反汇编）
      → 汇编/微架构断言已反汇编复现。
  任一成立 → [VERIFIED]；皆无 → [UNVERIFIED]（诚实默认，明确「待逐条核验」）。

安全约束（守 §0 / §10 / LF 红线）
--------------------------------
  - 仅处理「零标记」章；已含任一 §10 标记的章一律跳过（尊重既有人工标注）。
  - 标记置于章首 H1 标题后一行 blockquote，透明写明证据类型，绝不谎称。
  - 写入保原生换行（LF）；幂等：已注入「验证状态：」blockquote 则跳过，复跑不重复。
  - 绝不改动语义层、围栏内代码、既有标记、既有时序。
  - 生成审计清单 build/s10_audit.json + 可读报告，供作者逐条复核 / 纠偏。

CLI
---
  python3 tools/s10_verify_mark.py --report     # 仅审计清单，不落盘
  python3 tools/s10_verify_mark.py --apply      # 落盘注入标记
  python3 tools/s10_verify_mark.py --check      # 门禁：任一章仍零标记则 exit 1（防回归）
  python3 tools/s10_verify_mark.py --json        # 机器可读
"""

import os
import re
import sys
import json
import argparse
import subprocess

ROOT = os.getcwd()
BOOK = os.path.join(ROOT, "Book")

MARK_RE = re.compile(r"\[(VERIFIED|UNVERIFIED|NEEDS-VERIFY)\]")
BENCH_RE = re.compile(r"_bench_d5_[A-Za-z0-9_]+\.cpp")          # 章内 D5 基准声明
ASM_FENCE_RE = re.compile(r"^(`{3,}|~{3,})\s*asm\b", re.MULTILINE)
H1_RE = re.compile(r"^(#\s+.+)$", re.MULTILINE)
INJECTED_RE = re.compile(r"^>\s*验证状态：", re.MULTILINE)
CHNUM_RE = re.compile(r"ch(\d+)", re.IGNORECASE)


def git_tracked_files(pattern):
    out = subprocess.run(["git", "ls-files", pattern], cwd=ROOT,
                         capture_output=True, text=True).stdout.split()
    return set(os.path.basename(x) for x in out)


def chapter_files():
    """仅处理 147 个「活的」主章：Book/partNN/chNN_*.md（basename 以 ch<数字>_ 开头，
    且位于 part<数字> 目录下）。刻意排除：
      - _legacy_ModernCppBible/**（7 个陈旧副本，审计单独计为 legacy，不注入）；
      - GLOSSARY/SUMMARY/PREREQUISITES/00_*/MANIFEST 等索引/元数据文件（非高风险断言载体）；
      - 任何 basename 不以 ch<数字>_ 开头的杂项文件。
    与 verification_audit 的「147 主章 / 73 零标记」口径严格对齐。"""
    files = []
    for dp, _, fns in os.walk(BOOK):
        if "_legacy" in dp.replace("\\", "/"):
            continue
        for f in fns:
            if not f.lower().endswith(".md"):
                continue
            if not re.match(r"^ch\d+_", f):
                continue
            if not re.search(r"/part\d+", dp.replace("\\", "/")):
                continue
            files.append(os.path.join(dp, f))
    return sorted(files)


def analyze(path):
    text = open(path, encoding="utf-8", newline="").read()
    has_mark = bool(MARK_RE.search(text))
    if has_mark:
        m = MARK_RE.search(text)
        return {"path": path, "already_marked": True,
                "existing": m.group(1), "verified_chain": None,
                "marker": None, "injected": False, "skipped": True}
    has_d5 = bool(BENCH_RE.search(text))
    has_asm = bool(ASM_FENCE_RE.search(text))
    verified = has_d5 or has_asm
    marker = "VERIFIED" if verified else "UNVERIFIED"
    return {
        "path": path,
        "already_marked": False,
        "has_d5": has_d5,
        "has_asm": has_asm,
        "verified_chain": verified,
        "marker": marker,
        "injected": False,
        "skipped": False,
    }


def blockquote_for(rec):
    if rec["marker"] == "VERIFIED":
        ev = []
        if rec.get("has_d5"):
            ev.append("D5 基准源码（经 E11 编译门禁）")
        if rec.get("has_asm"):
            ev.append("书内 `asm` 反汇编证据（book_asm_freshness 校验）")
        return ("> 验证状态：[VERIFIED] — 复现链：" + " / ".join(ev) + "。\n")
    return ("> 验证状态：[UNVERIFIED] — 本章高风险断言尚未接入机器可验证复现链"
            "（无 D5 基准 / ASM 证据 / 已编译练习），待逐条核验。\n")


def inject(path, rec):
    text = open(path, encoding="utf-8", newline="").read()
    if INJECTED_RE.search(text):
        return False  # 已注入，幂等跳过
    m = H1_RE.search(text)
    if not m:
        return False  # 无 H1 标题，保守跳过
    insert_at = m.end()
    # 在 H1 行后插入一个空行 + blockquote（若 H1 后已紧跟内容，仍插其后的新行）
    tail = text[insert_at:]
    # 去掉紧随 H1 的可能空行，统一为：H1 \n <blockquote> \n <原后续>
    block = "\n" + blockquote_for(rec)
    new_text = text[:insert_at] + block + tail
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(new_text)
    return True


def main():
    ap = argparse.ArgumentParser(description="§10 verification-mark semi-auto triage")
    ap.add_argument("--report", action="store_true", help="仅审计清单，不落盘")
    ap.add_argument("--apply", action="store_true", help="落盘注入标记")
    ap.add_argument("--check", action="store_true", help="门禁：任一章仍零标记则 exit 1")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    args = ap.parse_args()

    files = chapter_files()
    recs = [analyze(f) for f in files]

    already = [r for r in recs if r["already_marked"]]
    zero = [r for r in recs if not r["already_marked"]]
    to_verify = [r for r in zero if r["verified_chain"]]
    to_unver = [r for r in zero if not r["verified_chain"]]

    if args.apply:
        for r in zero:
            if inject(r["path"], r):
                r["injected"] = True
        # 重新分析以确认
        recs = [analyze(f) for f in files]
        zero = [r for r in recs if not r["already_marked"]]

    os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
    manifest = {
        "already_marked": len(already),
        "zero_marker_total": len([r for r in recs if not r["already_marked"]]),
        "proposed_VERIFIED": len(to_verify),
        "proposed_UNVERIFIED": len(to_unver),
        "records": recs,
    }
    with open(os.path.join(ROOT, "build", "s10_audit.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)

    if args.json:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    else:
        print("=" * 64)
        print("§10 验证标记半自动分诊")
        print("=" * 64)
        print(f"  扫描章文件    : {len(recs)}")
        print(f"  已含标记(跳过): {len(already)}")
        print(f"  零标记章      : {len(zero) if not args.apply else manifest['zero_marker_total']}")
        if not args.apply:
            print(f"    → 拟 [VERIFIED] : {len(to_verify)} (有 D5/ASM 复现链)")
            print(f"    → 拟 [UNVERIFIED]: {len(to_unver)} (无复现链，诚实默认)")
        else:
            print(f"  注入后零标记  : {manifest['zero_marker_total']}")
            inj = sum(1 for r in recs if r.get("injected"))
            print(f"  本次新注入    : {inj}")
        print("  审计清单      : build/s10_audit.json")

    if args.check:
        remaining = [r for r in recs if not r["already_marked"]]
        if remaining:
            for r in remaining:
                print(f"[FAIL] 仍零标记: {os.path.relpath(r['path'], ROOT)}")
            return 1
        print("[OK] 全部章均已含 §10 验证标记")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
