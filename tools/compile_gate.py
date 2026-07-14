#!/usr/bin/env python3
"""编译防回归门禁 (compile gate)。

读取 `compile_all.py --main-only` 产出的 `tools/compile_report.json`，
与 `tools/compile_exempt.json` 中的已知豁免清单比对：

  * 报告中的失败块若命中豁免清单（显式 (file, block) 或错误文本匹配
    平台 / 库专属模式），视为「已知豁免」，不阻断 CI。
  * 报告中的失败块若既不在豁免清单、也不匹配任何豁免模式，视为
    「新增回归」（真实语法 / 类型错误），令 CI 失败（exit 1）。
  * 豁免清单中存在、但当前报告已不再出现的条目，视为「已变干净」，
    打印告警（不失败），提示可清理清单（--strict-stale 可升级为失败）。

设计目标：未来任何编辑若引入新的 SYNTAX / TYPE_MISMATCH 内容 bug，
CI 立即变红；而多文件工程、模块、MSVC / POSIX 专属、外部库、故意演示的
编译错误 / UB、跨块增量教学等设计性豁免不误伤。

跨平台稳健性：CI (Linux / gcc13) 与本地 (Windows / mingw) 报告差异（如
POSIX 块在 Linux 可编、Windows 块在 Linux 不可编）由 AUTO_PATTERNS 错误
文本模式吸收，避免误报红。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPORT = os.path.join(HERE, "compile_report.json")
DEFAULT_EXEMPT = os.path.join(HERE, "compile_exempt.json")

# 平台 / 库专属错误模式 -> 豁免原因。命中即视为豁免（即使未显式列出），
# 用于吸收 CI (Linux) 与本地 (Windows) 间的报告差异，避免误报红。
AUTO_PATTERNS = [
    (re.compile(r"(?i)windows\.h|winsock2\.h|ws2tcpip\.h|winsock|GetProcAddress|GetLogicalProcessor|PDWORD|\bHANDLE\b|__declspec"), "WINDOWS"),
    (re.compile(r"(?i)sys/mman\.h|\bmmap\b|POSIX"), "POSIX"),
    (re.compile(r"(?i)boost/|Qt|QObject|QWidget|fmt/|spdlog|gtest|gmock|catch2|Catch"), "EXT_LIB"),
    (re.compile(r"(?i)export module|import std|import \w+;|module \w+;"), "MODULE"),
    (re.compile(r"(?i)_MSC_VER|__msvc|Microsoft Visual"), "MSVC"),
]


def load_json(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    ap = argparse.ArgumentParser(description="编译防回归门禁")
    ap.add_argument("--report", default=DEFAULT_REPORT)
    ap.add_argument("--exempt", default=DEFAULT_EXEMPT)
    ap.add_argument("--strict-stale", action="store_true",
                    help="若豁免清单存在已变干净的条目也视为失败")
    args = ap.parse_args()

    if not os.path.exists(args.report):
        print(f"[gate] ERROR: 报告不存在: {args.report}\n"
              f"       先运行: python3 tools/compile_all.py --main-only",
              file=sys.stderr)
        return 2
    report = load_json(args.report)
    exempt_data = load_json(args.exempt) if os.path.exists(args.exempt) else {"exempt": []}

    exempt_list = exempt_data.get("exempt", [])
    exempt_keys = {(e["file"], e["block"]) for e in exempt_list}
    exempt_reason = {(e["file"], e["block"]): e.get("reason", "?") for e in exempt_list}

    actual = []  # (file, block, error)
    for ch in report.get("failures", []):
        f = ch["file"]
        for fr in ch["failures"]:
            actual.append((f, fr["block"], fr.get("error", "")))

    exempt_hit = []   # (file, block, reason, kind)
    regressions = []  # (file, block, error)
    for f, blk, err in actual:
        key = (f, blk)
        if key in exempt_keys:
            exempt_hit.append((f, blk, exempt_reason[key], "explicit"))
        else:
            matched = None
            for pat, reason in AUTO_PATTERNS:
                if pat.search(err):
                    matched = reason
                    break
            if matched:
                exempt_hit.append((f, blk, matched, "auto"))
            else:
                regressions.append((f, blk, err))

    actual_keys = {(f, b) for f, b, _ in actual}
    stale = [e for e in exempt_list if (e["file"], e["block"]) not in actual_keys]

    print("=" * 68)
    print(f"编译门禁  gcc={report.get('gcc')}  main_only={report.get('main_only')}  "
          f"partial={report.get('partial')}")
    print(f"  报告失败块 : {len(actual)}")
    print(f"  已知豁免   : {len(exempt_hit)}  "
          f"(显式 {sum(1 for *_, k in exempt_hit if k == 'explicit')} / "
          f"模式 {sum(1 for *_, k in exempt_hit if k == 'auto')})")
    print(f"  新增回归   : {len(regressions)}")
    print(f"  清单冗余   : {len(stale)}")
    print("-" * 68)
    if exempt_hit:
        print("豁免块（不阻断）:")
        for f, blk, reason, kind in exempt_hit:
            print(f"  [{kind:7}] {reason:14} {f}#blk{blk}")
    if regressions:
        print("回归块（CI 失败）:")
        for f, blk, err in regressions:
            first = err.strip().splitlines()[0][:120] if err.strip() else "(无错误文本)"
            print(f"  REGRESSION {f}#blk{blk}: {first}")
    if stale:
        print("冗余豁免条目（建议清理）:")
        for e in stale:
            print(f"  STALE {e['file']}#blk{e['block']} ({e.get('reason')})")
    print("=" * 68)

    if regressions:
        print(f"[gate] FAIL: {len(regressions)} 个新增回归，请修复源文件或更新豁免清单。")
        return 1
    if stale and args.strict_stale:
        print(f"[gate] FAIL: {len(stale)} 个冗余豁免条目（--strict-stale）。")
        return 1
    print("[gate] PASS: 无新增回归。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
