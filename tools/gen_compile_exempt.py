#!/usr/bin/env python3
"""从 compile_report.json 生成 tools/compile_exempt.json（豁免清单生成器）。

依据「章号 -> 主豁免原因」映射 + 错误文本模式，把当前报告里的所有失败块
分类为已知豁免，写入豁免清单。生成的清单供 compile_gate.py 使用。

重要：本脚本仅生成「当前报告即真理」的豁免清单。若某块其实是真实 bug，
正确做法是修复源文件（见 ROADMAP L4），而非把它加入本清单——一旦加入，
该块未来的回归将不再被门禁捕获。对 UNCLASSIFIED 块脚本会显式告警，
要求人工复核。
"""
from __future__ import annotations

import argparse
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPORT = os.path.join(HERE, "compile_report.json")
DEFAULT_OUT = os.path.join(HERE, "compile_exempt.json")

# 章号 -> 主豁免原因（整章统一标签；块级差异在 note 体现）。
# 仅覆盖经人工逐块判定的设计性豁免；真实内容 bug 不应出现在此映射中。
CHAPTER_REASON = {
    11: "MODULE", 12: "MULTI_FILE", 13: "MULTI_FILE", 14: "GUARDED_COMPILE",
    18: "MULTI_FILE", 19: "MULTI_FILE", 23: "MODULE", 26: "INTENTIONAL_ERROR",
    28: "INTENTIONAL_UB", 29: "INTENTIONAL_ERROR", 35: "POSIX",
    39: "CROSS_BLOCK", 44: "MULTI_FILE", 65: "CROSS_BLOCK", 96: "CROSS_BLOCK",
    108: "CROSS_BLOCK", 117: "CROSS_BLOCK", 118: "MODULE", 124: "LIBSTDCPP",
    125: "MSVC", 126: "MSVC", 128: "EXT_LIB", 129: "EXT_LIB", 131: "EXT_LIB",
    135: "CROSS_BLOCK", 136: "CROSS_BLOCK", 138: "CROSS_BLOCK",
    142: "CROSS_BLOCK", 144: "MULTI_FILE", 145: "CROSS_BLOCK",
    146: "CROSS_BLOCK", 150: "EXT_LIB", 159: "CROSS_BLOCK",
    160: "CROSS_BLOCK", 161: "CROSS_BLOCK",
}

TAXONOMY = {
    "MULTI_FILE": "示例引用同章/外部 .cpp/.h，需多文件联合编译",
    "MODULE": "C++20 模块示例，需模块编译管线",
    "MSVC": "MSVC 专属 API/宏(_MSC_VER)，非 GCC/Clang 可编译",
    "POSIX": "POSIX 专属系统调用(<sys/mman.h>等)",
    "WINDOWS": "Windows 专属 API(<windows.h>)，非 Linux 可编译",
    "EXT_LIB": "依赖未分发的第三方库(boost/Qt/fmt/spdlog/gtest)",
    "INTENTIONAL_ERROR": "故意演示编译错误以教学，本就不应通过",
    "INTENTIONAL_UB": "故意演示未定义行为以教学",
    "CROSS_BLOCK": "符号定义在更早代码块，顺读可编；隔离审计看不到",
    "LIBSTDCPP": "窥探 libstdc++ 内部实现，非标准接口",
    "GUARDED_COMPILE": "需额外编译宏(如 -DTRACK_LEAK)才成立的受控示例",
}

NOTE_HINT = {
    "INTENTIONAL_ERROR": "教学用故意错误块",
    "INTENTIONAL_UB": "教学用故意 UB 块",
    "CROSS_BLOCK": "符号在前序块定义",
    "GUARDED_COMPILE": "需 -DTRACK_LEAK 等附加宏",
}

# 错误文本 -> 原因（兜底，CHAPTER_REASON 未覆盖时用）
ERR_PATTERNS = [
    (re.compile(r"(?i)windows\.h|winsock2\.h|GetProcAddress|GetLogicalProcessor|PDWORD|__declspec"), "WINDOWS"),
    (re.compile(r"(?i)sys/mman\.h|\bmmap\b"), "POSIX"),
    (re.compile(r"(?i)boost/|Qt|QObject|fmt/|spdlog|gtest|gmock|catch2"), "EXT_LIB"),
    (re.compile(r"(?i)export module|import std|module \w+;"), "MODULE"),
    (re.compile(r"(?i)_MSC_VER"), "MSVC"),
]


def chapter_no(filename: str):
    m = re.search(r"ch(\d+)", filename)
    return int(m.group(1)) if m else -1


def main() -> None:
    ap = argparse.ArgumentParser(description="生成编译豁免清单")
    ap.add_argument("--report", default=DEFAULT_REPORT)
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()
    report = json.load(open(args.report, encoding="utf-8"))

    exempt = []
    unclassified = []
    for ch in report.get("failures", []):
        f = ch["file"]
        cno = chapter_no(f)
        base = CHAPTER_REASON.get(cno)
        for fr in ch["failures"]:
            blk = fr["block"]
            err = fr.get("error", "")
            reason = base
            if reason is None:
                for pat, r in ERR_PATTERNS:
                    if pat.search(err):
                        reason = r
                        break
            if reason is None:
                reason = "UNCLASSIFIED"
                unclassified.append((f, blk))
            entry = {"file": f, "block": blk, "reason": reason}
            note = NOTE_HINT.get(reason)
            if note:
                entry["note"] = note
            exempt.append(entry)

    doc = {
        "version": 1,
        "generated_from": "compile_all.py --main-only",
        "gcc": report.get("gcc"),
        "taxonomy": TAXONOMY,
        "exempt": exempt,
    }
    with open(args.out, "w", encoding="utf-8") as fp:
        json.dump(doc, fp, indent=2, ensure_ascii=False)

    print(f"生成豁免清单: {args.out}")
    print(f"  豁免块数: {len(exempt)}")
    if unclassified:
        print(f"  [警告] 未归类块（请人工复核是否为真实 bug，勿直接提交）:")
        for f, blk in unclassified:
            print(f"    {f}#blk{blk}")
    else:
        print("  [OK] 所有失败块均已归类。")


if __name__ == "__main__":
    main()
