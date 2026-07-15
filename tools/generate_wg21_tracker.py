#!/usr/bin/env python3
"""
generate_wg21_tracker.py — WG21 提案实现进度自动核对工具 (B3.3)

从 WG21/TRACKER.md 解析 feature-test macro 与声称的 GCC 支持状态,
对比 _cpp_probe_gcc.json 的本机实测探测值, 输出差异报告。

用途: 每季度工具链升级后, 核对 TRACKER.md 的 GCC 列是否已过期。

用法:
  python3 tools/generate_wg21_tracker.py
  python3 tools/generate_wg21_tracker.py --probe _cpp_probe_gcc.json --tracker WG21/TRACKER.md
  python3 tools/generate_wg21_tracker.py --gcc "C:/.../g++.exe"   # 现场探测(无probe文件时)

退出码: 0 = 无差异; 1 = 有差异需人工更新
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

# TRACKER.md 表格中 GCC 列的状态符号 → 期望「宏是否定义」
#   ✅ = 期望已定义;  ❌ = 期望未定义(<undef>);  🚧 = 部分/条件, 不强判
STATUS_DEFINED = "✅"
STATUS_UNDEF = "❌"
STATUS_PARTIAL = "🚧"

MACRO_RE = re.compile(r"`(__cpp_[a-zA-Z0-9_]+)`")


def load_probe(path):
    """读取 _cpp_probe_gcc.json → {macro: value_or_None}"""
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    macros = d.get("macros", d)
    out = {}
    for k, v in macros.items():
        if isinstance(v, dict):
            val = v.get("gcc_value", v.get("value"))
        else:
            val = v
        if val in ("<undef>", "", None):
            out[k] = None
        else:
            out[k] = str(val)
    return out


def live_probe(gcc, macros):
    """现场探测一组宏 (无 probe 文件时)。返回 {macro: value_or_None}"""
    lines = ["#include <version>"]
    for m in macros:
        lines.append(f'#ifdef {m}\n#pragma message("PROBE {m}=" _CB_STR({m}))\n#else\n#pragma message("PROBE {m}=<undef>")\n#endif')
    src = '#define _CB_STR2(x) #x\n#define _CB_STR(x) _CB_STR2(x)\n' + "\n".join(lines) + "\nint main(){}\n"
    with tempfile.NamedTemporaryFile("w", suffix=".cpp", delete=False, encoding="utf-8") as f:
        f.write(src)
        fp = f.name
    try:
        r = subprocess.run([gcc, "-std=c++23", "-fsyntax-only", fp],
                           capture_output=True, text=True, timeout=60)
        out = {}
        for line in (r.stderr or "").splitlines():
            m = re.search(r"PROBE (__cpp_[a-zA-Z0-9_]+)=(.*)", line)
            if m:
                name, val = m.group(1), m.group(2).strip().strip('"')
                out[name] = None if val == "<undef>" else val
        return out
    finally:
        os.unlink(fp)


def parse_tracker(path):
    """解析 TRACKER.md 表格行 → [(macro, gcc_status_symbol, line_no)]"""
    rows = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if not line.lstrip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 4:
                continue
            # 找含 __cpp_ 的单元格
            macro = None
            for c in cells:
                mm = MACRO_RE.search(c)
                if mm:
                    macro = mm.group(1)
                    break
            if not macro:
                continue
            # GCC 列 = macro 单元格之后第一个含状态符号的列
            gcc_sym = None
            for c in cells:
                if STATUS_DEFINED in c or STATUS_UNDEF in c or STATUS_PARTIAL in c:
                    gcc_sym = (STATUS_DEFINED if STATUS_DEFINED in c
                               else STATUS_UNDEF if STATUS_UNDEF in c
                               else STATUS_PARTIAL)
                    break
            rows.append((macro, gcc_sym, i))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", default="_cpp_probe_gcc.json")
    ap.add_argument("--tracker", default="WG21/TRACKER.md")
    ap.add_argument("--gcc", default=None, help="现场探测用的 g++ 路径(无 probe 文件时)")
    args = ap.parse_args()

    rows = parse_tracker(args.tracker)
    macros = [m for m, _, _ in rows]
    print(f"[TRACKER] {args.tracker}: 解析出 {len(rows)} 条带 feature-test macro 的提案")

    if os.path.exists(args.probe):
        probe = load_probe(args.probe)
        print(f"[PROBE]   {args.probe}: {len(probe)} 个宏 (本机实测)")
    elif args.gcc:
        probe = live_probe(args.gcc, macros)
        print(f"[PROBE]   现场探测 {args.gcc}: {len(probe)} 个宏")
    else:
        print("ERROR: 无 probe 文件且未提供 --gcc, 无法核对", file=sys.stderr)
        return 2

    diffs = []
    unknown = []
    for macro, sym, ln in rows:
        if macro not in probe:
            unknown.append((macro, ln))
            continue
        actual_defined = probe[macro] is not None
        actual = probe[macro] if actual_defined else "<undef>"
        if sym == STATUS_DEFINED and not actual_defined:
            diffs.append(f"  行{ln} {macro}: TRACKER 声称 ✅已支持, 实测 <undef> → 应改 ❌/🚧")
        elif sym == STATUS_UNDEF and actual_defined:
            diffs.append(f"  行{ln} {macro}: TRACKER 声称 ❌未支持, 实测 {actual} → 应改 ✅")
        # 🚧 部分支持不强制核对(可能条件编译)

    print(f"\n=== 核对结果 ===")
    print(f"差异(GCC 列过期): {len(diffs)}")
    for d in diffs:
        print(d)
    if unknown:
        print(f"探测集未覆盖的宏(需补入 verify_compiler_features.py): {len(unknown)}")
        for m, ln in unknown:
            print(f"  行{ln} {m}")
    if not diffs:
        print("✅ TRACKER.md GCC 列与本机实测一致, 无需更新")
    return 1 if diffs else 0


if __name__ == "__main__":
    sys.exit(main())
